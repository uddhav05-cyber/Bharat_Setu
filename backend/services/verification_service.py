"""
Verification Service
Orchestrates the full carbon credit verification pipeline:
Satellite → NDVI/SAR → Biomass → Carbon → Traffic Light → Payment
"""
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from models.verification import Verification
from models.farm_plot import FarmPlot
from models.user import User
from services.satellite_service import satellite_service
from services.traffic_light_service import traffic_light_service
from adapters.payment_adapter import payment_gateway
from events.event_bus import event_bus, Events

logger = logging.getLogger(__name__)


class VerificationService:
    """End-to-end carbon credit verification pipeline."""

    async def run_verification(
        self, db: Session, farm_plot_id: str, vle_estimated_biomass: float = 0.5
    ) -> dict:
        """
        Run the full verification pipeline for a farm plot.
        Flow: Satellite → Biomass → Traffic Light → Payment (if GREEN)
        """
        # 1. Get farm plot
        farm = db.query(FarmPlot).filter(FarmPlot.id == farm_plot_id).first()
        if not farm:
            return {"error": "Farm plot not found"}

        # 2. Acquire satellite imagery (mock)
        imagery = satellite_service.acquire_imagery(
            farm_plot_id=farm.id,
            centroid_lat=farm.centroid_lat or 19.0,
            centroid_lon=farm.centroid_lon or 73.0,
        )

        satellite_source = imagery["satellite_source"]
        cloud_cover = imagery["cloud_cover_percentages"][0]

        # 3. Calculate biomass based on satellite source
        # Load mock tile data
        import json, os
        tile_path = imagery["storage_paths"][0]
        if os.path.exists(tile_path):
            with open(tile_path, "r") as f:
                tile_data = json.load(f)
            bands = tile_data.get("bands", {})
        else:
            bands = {}

        if satellite_source == "SENTINEL_2_OPTICAL":
            red = bands.get("B4_RED", 0.05)
            nir = bands.get("B8_NIR", 0.4)
            biomass_score = satellite_service.calculate_ndvi(red, nir)
        else:
            vv = bands.get("VV", -12)
            vh = bands.get("VH", -18)
            biomass_score = satellite_service.calculate_sar_biomass(vv, vh)

        # 4. Get baseline (last verification or default)
        last_verification = (
            db.query(Verification)
            .filter(Verification.farm_plot_id == farm_plot_id)
            .filter(Verification.verification_status == "APPROVED")
            .order_by(Verification.completed_at.desc())
            .first()
        )
        baseline = last_verification.biomass_score if last_verification else 0.3
        biomass_change = biomass_score - baseline

        # 5. Calculate carbon sequestration
        plot_area_hectares = (farm.size_acres or 1.0) * 0.4047
        carbon_tons = satellite_service.calculate_carbon_sequestration(
            biomass_change, plot_area_hectares, farm.crop_type or "crops"
        )

        # 6. Traffic Light Protocol - fraud detection
        confidence_score = imagery["quality_score"]
        variance = traffic_light_service.calculate_variance(
            vle_estimated_biomass, biomass_score
        )
        tl_status, action, reasoning = traffic_light_service.determine_status(
            variance, confidence_score
        )

        # 7. Determine commission status
        vle = db.query(User).filter(User.id == farm.vle_id).first() if farm.vle_id else None
        trust_score = vle.trust_score if vle else 50.0
        commission_status = traffic_light_service.determine_commission_status(
            tl_status, confidence_score, trust_score
        )

        # 8. Update VLE trust score
        new_trust_score = traffic_light_service.update_trust_score(trust_score, tl_status)
        trust_score_update = new_trust_score - trust_score

        if vle:
            vle.trust_score = new_trust_score
            vle.total_verifications = (vle.total_verifications or 0) + 1
            if tl_status == "GREEN":
                vle.successful_verifications = (vle.successful_verifications or 0) + 1
            elif tl_status == "RED":
                vle.fraud_detections = (vle.fraud_detections or 0) + 1
                # Check account suspension
                if traffic_light_service.check_account_suspension(new_trust_score):
                    vle.account_status = "SUSPENDED"

        # 9. Create verification record
        verification = Verification(
            farm_plot_id=farm_plot_id,
            vle_id=farm.vle_id,
            satellite_source=satellite_source,
            s3_tile_keys=imagery["storage_paths"],
            biomass_score=biomass_score,
            biomass_baseline=baseline,
            biomass_change=biomass_change,
            carbon_sequestration_tons=carbon_tons,
            confidence_score=confidence_score,
            traffic_light_status=tl_status,
            variance=variance,
            vle_estimated_biomass=vle_estimated_biomass,
            verification_status="APPROVED" if tl_status == "GREEN" else (
                "NEEDS_REVIEW" if tl_status == "YELLOW" else "REJECTED"
            ),
            action=action,
            reasoning=reasoning,
            commission_status=commission_status,
            trust_score_update=trust_score_update,
            completed_at=datetime.utcnow(),
            cloud_cover=cloud_cover,
        )

        db.add(verification)

        # 10. Update farm plot
        ndvi_entry = {
            "date": datetime.utcnow().isoformat(),
            "value": biomass_score,
            "satellite_source": satellite_source,
        }
        farm.ndvi_history = (farm.ndvi_history or []) + [ndvi_entry]
        farm.last_verification_date = datetime.utcnow()
        if tl_status == "GREEN":
            farm.carbon_credits_total = (farm.carbon_credits_total or 0) + carbon_tons
            farm.status = "ACTIVE"

        db.commit()
        db.refresh(verification)

        # 11. Publish events
        if tl_status == "GREEN":
            await event_bus.publish(Events.TRAFFIC_LIGHT_GREEN, {
                "verification_id": verification.id,
                "farm_plot_id": farm_plot_id,
                "carbon_tons": carbon_tons,
            })
        elif tl_status == "RED":
            await event_bus.publish(Events.TRAFFIC_LIGHT_RED, {
                "verification_id": verification.id,
                "vle_id": farm.vle_id,
                "variance": variance,
            })

        # 12. Process payment if GREEN
        payment_info = None
        if tl_status == "GREEN" and carbon_tons > 0:
            try:
                payment = await payment_gateway.issue_voucher(
                    farmer_id=farm.farmer_id,
                    verification_id=verification.id,
                    carbon_tons=carbon_tons,
                    payment_source="CSR",
                    amount=carbon_tons * 500,  # ₹500 per ton (fixed service payment)
                )
                payment_info = payment.to_dict()
            except Exception as e:
                logger.error(f"Payment processing failed: {e}")

        return {
            "verification_id": verification.id,
            "biomass_score": biomass_score,
            "biomass_change": biomass_change,
            "carbon_tons": carbon_tons,
            "satellite_source": satellite_source,
            "cloud_cover": cloud_cover,
            "confidence_score": confidence_score,
            "traffic_light": {
                "status": tl_status,
                "action": action,
                "variance": variance,
                "reasoning": reasoning,
            },
            "vle_trust": {
                "previous_score": trust_score,
                "new_score": new_trust_score,
                "update": trust_score_update,
            },
            "commission_status": commission_status,
            "payment": payment_info,
        }


verification_service = VerificationService()
