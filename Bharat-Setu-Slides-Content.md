# Bharat-Setu Presentation Slides Content

---

## SLIDE 1: Brief about the idea

### Bharat-Setu: The Unified Rural Intelligence Platform

A frugal innovation platform empowering rural India through three integrated modules:

**• Carbon-Kosh**: Enables small farmers (1-2 acres) to earn guaranteed service payments through satellite-verified carbon sequestration

**• Gram-Twin**: Creates 3D digital twins of villages for scientific ecological planning by Sarpanches

**• Migration-Shield**: Detects acute distress crises using Boolean threshold logic to prevent migration

#### Key Innovation
Voice-first, multilingual platform (Hindi, Marathi, Tamil) with on-device AI transcription, working offline on 2G networks with 8-hour battery life

#### Impact
Maintains operational costs under $2.50/month per village cluster while serving farmers, VLEs, village leaders, and district officials

---

## SLIDE 2: How is it different from existing ideas?

### Pilot-Ready Architecture with 4 Critical Innovations

#### 1. Adversarial Trust Model (Traffic Light Protocol)
- Detects VLE fraud by comparing ground reports vs. satellite verification
- **GREEN** (<10% variance): Auto-approve
- **YELLOW** (10-30%): Manual review
- **RED** (>30%): Freeze account

#### 2. Sovereign Payment Rails (Not Market-Based)
- e-RUPI vouchers (CSR) + PFMS-DBT (Government) instead of commodity trading
- Zero market risk, purpose-locked for agricultural inputs only

#### 3. Frugal Edge Computing
- 90% transcriptions on-device (Vosk-Lite), 10% cloud fallback (Bhashini)
- Text-only uploads (<5KB vs 500KB audio) saves 99% bandwidth
- Duty-cycled sensors achieve 8-hour battery life

#### 4. Boolean Threshold Logic (Not Weighted Averages)
- One-strike crisis detection: ANY vital sign failure triggers alert
- Transparent, explainable (e.g., "Water Failure" not "Risk Score 73")

---

## SLIDE 3: USP (Unique Selling Proposition)

### 1. Multi-Modal Satellite Verification (365-Day Coverage)
- **Sentinel-2 Optical (NDVI)** for fair weather (<30% cloud cover)
- **Sentinel-1 SAR (Backscatter)** for monsoon/cloudy conditions (≥30% cloud cover)
- **USP**: Works in all weather conditions, no ground sensors needed

### 2. Frugal Innovation at Scale
- $1.70/village/month actual cost (30% under $2.50 budget)
- Scales to 10,000+ villages without infrastructure investment

### 3. India Stack Integration
- **Bhashini API** for rural dialect accuracy (Marathi, Hindi, Tamil)
- **MapMyIndia** for cadastral survey numbers (Google Maps misses farm boundaries)
- **e-RUPI/PFMS** for government-compliant payments

### 4. Offline-First Design
- Works on intermittent 2G connectivity
- On-device AI handles 90% of operations without internet

---

## SLIDE 4: Feature List & Technical Vision

### Core Features

#### Carbon-Kosh (70% of system)
- Voice-based farm registration (Push-to-Talk, multilingual)
- Satellite-verified carbon sequestration (Sentinel-2 + Sentinel-1 SAR)
- GCP-compliant service payment certificates (PDF with QR code)
- Traffic Light fraud detection (VLE Trust Score 0-100)
- Sovereign payment vouchers (e-RUPI/PFMS-DBT)

#### Gram-Twin (15% of system)
- 3D village digital twin with NDVI overlay
- Degradation hotspot identification (NDVI decline >30%)
- Intervention recommendations (check dams, tree plantation)

#### Migration-Shield (15% of system)
- Boolean threshold crisis detection (Rainfall, Water, Health, Crop, Debt)
- Crisis Map dashboard with specific failure reasons
- Real-time alerts to district officials (<1 hour)

---

## SLIDE 5: Use Case Diagram

### Primary Actors & Use Cases

#### 1. Farmer
- Register farm plot via voice (assisted by VLE)
- Request carbon verification
- Receive service payment certificate
- Redeem e-RUPI voucher for agricultural inputs

#### 2. VLE (Village Level Entrepreneur)
- Assist farmers with voice registration
- Capture GPS coordinates and photos
- Earn commission (5-10%) after satellite verification
- Maintain Trust Score >40 to stay active

#### 3. Sarpanch (Village Head)
- View 3D digital twin of village
- Identify degradation hotspots
- Plan Viksit Bharat G-RAM projects
- Allocate resources scientifically

#### 4. District Official
- Monitor Crisis Map dashboard
- Receive alerts when vital signs fail
- Deploy targeted interventions
- Export reports for state government

---

## SLIDE 6: Architecture diagram of the proposed solution

### Event-Driven Serverless Architecture (AWS)

#### Client Layer
- **Flutter Mobile App** (Push-to-Talk + Vosk on-device)
- **React.js Admin Dashboard** (Crisis Map + Traffic Light UI)

#### API Layer
- **AWS API Gateway** (REST + WebSocket)
- **AWS Cognito** (JWT Auth + RBAC)
- **/sync/metadata** (instant, <5KB) | **/sync/media** (WiFi-only, heavy)

#### Orchestration Layer
- **Amazon Bedrock** (Claude 3 Haiku for intent extraction)
- **Amazon EventBridge** (event router)

#### Service Layer
- **VoiceLambda** (hybrid edge/cloud transcription)
- **SatelliteLambda** (Sentinel-1 SAR downloader)
- **VerificationLambda** (SageMaker biomass analysis)
- **TrafficLightLambda** (VLE fraud detection)
- **EscrowLambda** (e-RUPI mock adapter)
- **ThresholdLambda** (Boolean crisis detection)

#### Data Layer
- **Amazon Aurora Serverless v2** (PostgreSQL + PostGIS)
- **AWS S3** (satellite imagery + evidence vault)
- **Amazon SageMaker** (Sentinel-1 SAR model)

---

## SLIDE 7: Technologies to be used in the solution (Part 1)

### Cloud & AI (AWS)
- **AWS Lambda (Python)**: Serverless compute for all business logic
- **Amazon Bedrock (Claude 3 Haiku)**: Intent extraction from voice text
- **Amazon SageMaker**: Multi-Modal Satellite Engine (Sentinel-2 NDVI + Sentinel-1 SAR)
- **Amazon Aurora Serverless v2**: PostgreSQL + PostGIS for geospatial data
- **AWS S3 + Glacier**: Satellite imagery storage with lifecycle policies
- **Amazon EventBridge**: Event-driven architecture orchestration

### India Stack Integrations
- **Bhashini API (ULCA)**: Rural dialect ASR (Marathi, Hindi, Tamil)
- **MapMyIndia (Mappls)**: Cadastral survey numbers for farm boundaries
- **e-RUPI Mock Adapter**: NPCI voucher simulation (production-ready)
- **PFMS Mock Adapter**: DBT simulation (production-ready)

---

## SLIDE 8: Technologies to be used in the solution (Part 2)

### Mobile & Edge Computing
- **Flutter (Dart)**: Cross-platform mobile app (Android, future iOS)
- **Vosk-Lite (Small-Hindi model)**: On-device voice transcription (90% of calls)
- **SQLite**: Local offline queue storage
- **Push-to-Talk**: Battery-optimized voice input

### Satellite Data Sources
- **Sentinel-2 Optical**: NDVI calculation (fair weather, <30% cloud cover)
- **Sentinel-1 SAR**: Backscatter analysis (all-weather, monsoon capability)
- **Copernicus Open Access Hub**: Free satellite data download

### Security & Compliance
- **AWS Cognito**: JWT authentication with RS256 signing
- **AWS KMS**: Server-side encryption for S3 and Aurora
- **TLS 1.3**: All API communications encrypted
- **GCP Compliance**: Green Credit Programme (MoEFCC) standards

---

## SLIDE 9: Estimated implementation cost (optional)

### Monthly Operational Cost (Per Village Cluster)

| Service | Cost | Notes |
|---------|------|-------|
| AWS Lambda | $0.30 | Serverless compute (ARM64 for 20% savings) |
| Amazon Bedrock | $0.15 | Intent extraction (10% of requests) |
| Amazon SageMaker | $0.40 | Sentinel-1 SAR inference (once per 10 days) |
| Bhashini API | $0.05 | Fallback only (10% of transcriptions) |
| MapMyIndia API | $0.10 | Tile caching reduces calls |
| Aurora Serverless v2 | $0.50 | Scales to zero when idle |
| S3 + Glacier | $0.20 | Lifecycle policies for old data |
| e-RUPI Mock Adapter | $0.00 | Free for pilot (mock) |
| **Total** | **$1.70/village/month** | **32% under $2.50 budget** |

### Pilot Phase (6 months, 100 villages)
- **Infrastructure**: $10,200 ($1.70 × 100 villages × 6 months)
- **Development**: $50,000 (one-time)
- **Total Pilot Cost: $60,200**

---

## SLIDE 10: Impact & Scalability

### Expected Impact

#### For Farmers
- Guaranteed service payments (no market risk)
- Zero upfront investment (no sensors/equipment)
- Multilingual voice interface (no literacy barrier)
- Offline-capable (works on 2G networks)

#### For Village Leaders
- Scientific ecological planning with 3D digital twins
- Data-driven resource allocation
- Transparent degradation hotspot identification

#### For Government
- Early crisis detection (prevents distress migration)
- Transparent Boolean thresholds (regulatory compliance)
- Audit trail for all payments (e-RUPI/PFMS)
- Cost-effective at scale ($1.70/village/month)

### Scalability Roadmap
- **Pilot**: 100 villages (6 months)
- **Phase 1**: 1,000 villages (Year 1)
- **Phase 2**: 10,000 villages (Year 2)
- **National**: 600,000+ villages (Year 5)

---

## Additional Notes for Presentation

### Key Talking Points
1. **Frugal Innovation**: $1.70/village/month vs. $2.50 budget (32% savings)
2. **All-Weather Capability**: Sentinel-1 SAR works during monsoon (unique differentiator)
3. **Fraud Prevention**: Traffic Light Protocol ensures VLE accountability
4. **Offline-First**: 90% operations work without internet (critical for rural India)
5. **Government Compliance**: e-RUPI/PFMS integration ensures regulatory adherence

### Demo Flow Suggestion
1. Show VLE assisting farmer with voice registration (Push-to-Talk)
2. Display satellite verification (Sentinel-2 vs Sentinel-1 SAR comparison)
3. Show Traffic Light status (GREEN/YELLOW/RED)
4. Display 3D digital twin of village
5. Show Crisis Map with specific vital sign failures

---

**Document Created**: Based on comprehensive analysis of Bharat-Setu requirements.md and design.md
**Total Slides**: 10 (excluding title slide)
**Format**: Ready for PowerPoint import
