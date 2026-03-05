# Design Document: Bharat-Setu

## Overview

Bharat-Setu is a serverless, event-driven platform built on AWS that enables rural economic empowerment through three integrated modules: Carbon-Kosh (satellite-verified carbon credits), Gram-Twin (ecological planning), and Migration-Shield (predictive migration analytics). The architecture follows a "frugal innovation" philosophy, maintaining costs under $2.50/month per village cluster while serving thousands of farmers, village leaders, and government officials.

**Pilot-Ready Architecture Principles:**

This design addresses four critical gaps identified in the strategic vision to ensure pilot readiness:

1. **Adversarial Trust Model**: Implements a Traffic Light Protocol to detect VLE fraud by comparing ground reports against satellite verification in real-time
2. **Sovereign Payment Rails**: Uses e-RUPI vouchers (CSR) and PFMS-DBT (Government) instead of commodity market trading to ensure regulatory compliance and zero market risk for farmers
3. **Frugal Edge Computing**: Employs on-device transcription (Vosk-Lite) and duty-cycled sensors to achieve 8-hour battery life on budget smartphones with intermittent 2G connectivity
4. **Boolean Threshold Logic**: Replaces weighted-average risk scoring with one-strike crisis detection to prevent false negatives in distress prediction

The system implements a 70/30 effort split: 70% focused on Carbon-Kosh as the core data engine, and 30% on downstream applications (Gram-Twin and Migration-Shield) that reuse carbon verification data. This design leverages AWS Lambda for compute, S3 for storage, Amazon Aurora Serverless v2 (PostgreSQL with PostGIS extension) for geospatial data, and a lean AI strategy combining deep learning (SageMaker for Sentinel-1 SAR analysis) with generative AI (Bedrock Claude 3 Haiku for intent extraction).

## Indo-Cloud Hybrid Stack (Pilot-Ready)

This is the definitive, **lean** technology stack that marries AWS computational power with India's Digital Public Infrastructure (DPI). It includes **only what is necessary** to make the pilot work.

### 1. The Brain (Cloud & AI Logic)

| Component | Service | Purpose |
|-----------|---------|---------|
| **Core Compute** | AWS Lambda (Python) | Runs the "Traffic Light" algorithm and LSI threshold checks. Serverless architecture keeps costs within $2.50/village/month cap. |
| **GenAI Intelligence** | Amazon Bedrock (Claude 3 Haiku) | Intent Extraction: Takes farmer's translated text from Bhashini and converts it into structured JSON actions (e.g., `{ "action": "check_weather", "location": "pune" }`). |
| **Satellite Analysis** | Amazon SageMaker | Hosts the Multi-Modal Satellite Engine: Sentinel-2 (Optical NDVI) for fair-weather precision + Sentinel-1 (SAR Backscatter) for all-weather monsoon verification. Pilot focuses on demonstrating SAR capability. |

### 2. The Context (India Stack Integrations)

| Component | Service | Purpose |
|-----------|---------|---------|
| **Voice Layer** | Bhashini API (ULCA) | The only way to accurately handle rural dialects (Marathi, Hindi, Tamil). Converts Speech → Text with dialect-specific acoustic models. |
| **Map Layer** | MapMyIndia APIs (Mappls) | Provides "Cadastral Map" with Survey Numbers for VLE app. Critical because Google Maps often misses village farm boundaries. |
| **Payment Layer** | e-RUPI (Mock Adapter for Pilot) | Generates "Voucher String" (simulated) for CSR payments. No crypto, no blockchain. Standard API call via NPCI. |

### 3. The Data (Storage & Speed)

| Component | Service | Purpose |
|-----------|---------|---------|
| **Primary Database** | Amazon Aurora Serverless v2 (PostgreSQL with PostGIS) | Single Source of Truth: Stores Farmer Profiles, VLE Trust Scores, Transaction Logs, and geospatial data. Scales to zero when not used (cost savings). |
| **Evidence Vault** | Amazon S3 | Stores compressed photos, satellite tiles, and "Traffic Light" audit reports. Lifecycle policies move old data to Glacier. |
| **Government API Adapters** | Configurable Adapter Pattern | Mock Adapters for Pilot (PM-KISAN, e-NAM, PFMS) simulate government API responses for end-to-end workflow demonstration. Production-ready for hot-swap to live API Setu integration. |

### 4. The Edge (Mobile App)

| Component | Service | Purpose |
|-----------|---------|---------|
| **Framework** | Flutter (Dart) | Builds the VLE App for Android. Cross-platform capability for future iOS support. |
| **Offline AI** | Vosk (Model: Small-Hindi) | Runs on-device to detect simple keywords (e.g., "Start Survey") without internet/battery drain. Handles 90% of transcriptions locally. |

### The Logic Flow (How It All Fits Together)

```
1. INPUT:
   VLE presses Push-to-Talk button
   → Speaks in Marathi
   → Vosk (Edge) wakes up app and transcribes locally
   → If confidence < 80%: Bhashini (Cloud) translates to English

2. REASONING:
   English Text → Amazon Bedrock (Claude 3 Haiku)
   → Extracts structured claim: "High Biomass on Plot #123"

3. VERIFICATION (Traffic Light Protocol):
   System queries SageMaker (Multi-Modal Satellite Engine)
   → IF cloud_cover < 30%: Use Sentinel-2 Optical (NDVI precision)
   → IF cloud_cover >= 30%: Use Sentinel-1 SAR (All-weather capability)
   → Calculates variance: |VLE_Claim - Satellite_Data| / Satellite_Data * 100
   
   Logic:
   IF variance < 10%: GREEN (Auto-approve)
   IF variance 10-30%: YELLOW (Flag for call)
   IF variance > 30%: RED (Freeze VLE account)

4. ACTION:
   Financial: Trigger e-RUPI Mock Adapter → Log "Success" in Aurora DB
   Visual: Show "Green Polygon" on MapMyIndia layer in VLE app
   Trust: Update VLE_Trust_Score in Aurora (+2 for GREEN, -15 for RED)
```

### Why This Stack is Lean & Pilot-Ready

**Removed from Original Design:**
- ❌ Amazon QLDB (replaced by Aurora transaction logs)
- ❌ DigiLocker (certificates stored in S3 for pilot)
- ❌ API Setu PM-KISAN/e-NAM live integration (using Mock Adapters for pilot, production-ready for hot-swap)
- ❌ Ayushman Bharat live integration (using Mock Adapter for pilot)
- ❌ Amazon Forecast (replaced by Boolean thresholds)
- ❌ Amazon Q (replaced by simple NDVI trend analysis)

**Kept for Pilot:**
- ✅ AWS Lambda (Python) - Core compute
- ✅ Amazon Bedrock (Claude 3 Haiku) - Intent extraction
- ✅ Amazon SageMaker - Multi-Modal Satellite Engine (Sentinel-2 + Sentinel-1 SAR)
- ✅ Bhashini API - Dialect-heavy ASR
- ✅ MapMyIndia - Cadastral survey numbers
- ✅ e-RUPI Mock Adapter - Payment simulation (production-ready for NPCI integration)
- ✅ PFMS Mock Adapter - DBT simulation (production-ready for API Setu integration)
- ✅ PM-KISAN Mock Adapter - Farmer validation simulation (production-ready for API Setu integration)
- ✅ Amazon Aurora Serverless v2 - PostgreSQL + PostGIS
- ✅ Amazon S3 - Evidence storage
- ✅ Flutter - Mobile app framework
- ✅ Vosk - On-device transcription

### Latency Optimization

**The Constraint**: Calling Bhashini (External) + Bedrock (AWS) + MapMyIndia (External) can make the app slow.

**The Fix**: Frugal Edge Protocol
- **VLE App**: Uses on-device Vosk for 90% of commands (offline, <500ms)
- **Cloud**: Only calls Bhashini/Bedrock for complex queries or low-confidence transcriptions
- **Async Processing**: Uses AWS SQS + Lambda to prevent mobile app from freezing
- **Caching**: MapMyIndia tiles cached for 7 days, Bhashini responses cached for common phrases

### Cost Breakdown (Per Village/Month)

| Service | Cost | Notes |
|---------|------|-------|
| AWS Lambda | $0.30 | Serverless compute for all business logic |
| Amazon Bedrock (Claude 3 Haiku) | $0.15 | Intent extraction (10% of requests, 90% handled by Vosk) |
| Amazon SageMaker | $0.40 | Sentinel-1 SAR inference (once per 10 days) |
| Bhashini API | $0.05 | Fallback only (10% of transcriptions) |
| MapMyIndia API | $0.10 | Tile caching reduces calls |
| Amazon Aurora Serverless v2 | $0.50 | Scales to zero when idle |
| Amazon S3 + Glacier | $0.20 | Lifecycle policies for old data |
| e-RUPI Mock Adapter | $0.00 | Free for pilot (mock) |
| **Total** | **$1.70/village/month** | **Well within $2.50 budget** |

**Remaining Budget**: $0.80/village/month for scaling and contingency.

## Architecture

### System Architecture Diagram (Pilot-Ready)

```mermaid
graph TB
    subgraph "Client Layer"
        MobileApp[Flutter Mobile App<br/>Push-to-Talk + On-Device Vosk]
        WebDash[React.js Admin Dashboard<br/>Crisis Map + Traffic Light UI]
    end
    
    subgraph "API Layer"
        APIGateway[AWS API Gateway<br/>REST + WebSocket]
        Cognito[AWS Cognito<br/>JWT Auth + RBAC]
        SyncMeta[/sync/metadata<br/>Instant, Light]
        SyncMedia[/sync/media<br/>WiFi Only, Heavy]
    end
    
    subgraph "Orchestration Layer"
        BedrockAgent[Amazon Bedrock<br/>Claude 3 Haiku Intent Extraction]
        EventBridge[Amazon EventBridge<br/>Event Router]
    end

    subgraph "Service Layer - Carbon-Kosh (70%)"
        VoiceLambda[Voice Processing Lambda<br/>Hybrid Edge/Cloud]
        SatelliteLambda[Satellite Acquisition Lambda<br/>Sentinel-1 SAR Downloader]
        VerificationLambda[Verification Lambda<br/>SageMaker Biomass Analysis]
        TrafficLightLambda[Traffic Light Verifier<br/>VLE Fraud Detection]
        EscrowLambda[Escrow & Settlement Engine<br/>e-RUPI Mock Adapter]
    end
    
    subgraph "Service Layer - Gram-Twin (15%)"
        TwinLambda[Digital Twin Lambda<br/>3D Map Aggregator]
        HotspotLambda[Hotspot Detection Lambda<br/>NDVI Trend Analysis]
    end
    
    subgraph "Service Layer - Migration-Shield (15%)"
        ThresholdLambda[Threshold Monitor Lambda<br/>Boolean Crisis Detection]
        AlertLambda[Alert Notification Lambda<br/>SNS/SES]
    end
    
    subgraph "Data Layer"
        S3[AWS S3<br/>Satellite Imagery + Evidence Vault]
        Aurora[(Amazon Aurora Serverless v2<br/>PostgreSQL + PostGIS)]
        SageMaker[Amazon SageMaker<br/>Sentinel-1 SAR Model]
    end
    
    subgraph "External Integrations"
        Bhashini[Bhashini API<br/>Cloud Fallback Only]
        Sentinel[Sentinel-1 SAR<br/>Copernicus Hub]
        MapMyIndia[MapMyIndia Mappls<br/>Cadastral Survey Numbers]
        eRUPI[e-RUPI Mock Adapter<br/>NPCI Voucher Simulation]
    end
    
    MobileApp --> SyncMeta
    MobileApp --> SyncMedia
    SyncMeta --> APIGateway
    SyncMedia --> APIGateway
    WebDash --> APIGateway
    APIGateway --> Cognito
    Cognito --> BedrockAgent
    BedrockAgent --> EventBridge
    
    EventBridge --> VoiceLambda
    EventBridge --> SatelliteLambda
    EventBridge --> VerificationLambda
    EventBridge --> TrafficLightLambda
    EventBridge --> EscrowLambda
    EventBridge --> TwinLambda
    EventBridge --> HotspotLambda
    EventBridge --> ThresholdLambda
    
    VoiceLambda -.->|Fallback Only| Bhashini
    SatelliteLambda --> Sentinel
    SatelliteLambda --> S3
    VerificationLambda --> S3
    VerificationLambda --> SageMaker
    VerificationLambda --> Aurora
    TrafficLightLambda --> Aurora
    TrafficLightLambda --> SageMaker
    EscrowLambda --> eRUPI
    EscrowLambda --> Aurora
    
    TwinLambda --> Aurora
    TwinLambda --> MapMyIndia
    HotspotLambda --> Aurora
    
    ThresholdLambda --> Aurora
    AlertLambda --> WebDash
```

### Event-Driven Architecture

The platform uses Amazon EventBridge as the central event bus, enabling loose coupling between services:

1. **Voice Request Event**: Triggered when farmer submits voice input → Routes to VoiceLambda
2. **Farm Registration Event**: Triggered when farm plot is created → Routes to SatelliteLambda to subscribe to imagery
3. **Satellite Data Available Event**: Triggered when new Sentinel-1 SAR imagery arrives → Routes to VerificationLambda
4. **Verification Complete Event**: Triggered when biomass analysis finishes → Routes to TrafficLightLambda for fraud detection
5. **Traffic Light Green Event**: Triggered when variance < 10% → Routes to EscrowLambda for payment processing
6. **Traffic Light Red Event**: Triggered when variance > 30% → Routes to AlertLambda for VLE account freeze
7. **Threshold Breach Event**: Triggered when any critical vital sign fails → Routes to AlertLambda for district officials
8. **Payment Approved Event**: Triggered when escrow releases funds → Routes to notification services

This event-driven design minimizes Lambda cold starts by using EventBridge's built-in retry and DLQ capabilities.


## Components and Interfaces

### 1. Voice Processing Component (VoiceLambda) - UPDATED FOR PILOT

**Responsibility**: Transcribe farmer voice input using on-device Vosk-Lite, with cloud fallback to Bhashini only when needed.

**Interface**:
```typescript
interface VoiceRequest {
  transcribedText: string;    // Pre-transcribed on-device (not raw audio)
  language: 'hi' | 'mr' | 'ta'; // Hindi, Marathi, Tamil
  userId: string;
  timestamp: number;
  gpsCoordinates?: {
    latitude: number;
    longitude: number;
  };
  transcriptionSource: 'VOSK_EDGE' | 'BHASHINI_CLOUD'; // Track which engine was used
  batteryLevel?: number;      // For monitoring duty cycling effectiveness
}

interface VoiceResponse {
  intent: 'REGISTER_FARM' | 'REQUEST_VERIFICATION' | 'VIEW_CERTIFICATE' | 'QUERY_STATUS';
  extractedData: {
    farmSize?: number;        // In acres
    cropType?: string;
    location?: string;
  };
  responseText: string;       // Text response (TTS happens on-device)
  processingTimeMs: number;
}
```

**Dependencies**:
- Vosk-Lite (on-device, primary)
- Bhashini API (cloud fallback, only when Vosk confidence < 80%)
- Amazon Bedrock Agent for intent extraction
- EventBridge for publishing farm registration events

**Cost Optimization**:
- 90% of transcriptions happen on-device (zero API cost)
- Bhashini API only called for low-confidence cases
- Use Lambda ARM64 architecture for 20% cost reduction
- Set memory to 512MB (optimal for text processing, not audio)

### 2. Satellite Acquisition Component (SatelliteLambda)

**Responsibility**: Download multi-modal satellite imagery (Sentinel-2 Optical + Sentinel-1 SAR) for registered farm plots and store in S3. Pilot focuses on demonstrating SAR capability.

**Interface**:
```typescript
interface SatelliteRequest {
  farmPlotId: string;
  boundingBox: {
    minLat: number;
    minLon: number;
    maxLat: number;
    maxLon: number;
  };
  startDate: string;          // ISO 8601 format
  endDate: string;
  preferredSource?: 'OPTICAL' | 'SAR' | 'AUTO'; // AUTO selects based on cloud cover
}

interface SatelliteResponse {
  tileIds: string[];
  acquisitionDates: string[];
  cloudCoverPercentages: number[]; // Only for optical
  satelliteSource: 'SENTINEL_2_OPTICAL' | 'SENTINEL_1_SAR';
  s3Keys: string[];           // S3 object keys for downloaded tiles
  qualityScore: number;       // 0-100, based on cloud cover or signal quality
}
```

**Dependencies**:
- Sentinel Hub API or Copernicus Open Access Hub (Sentinel-2 Optical + Sentinel-1 SAR data)
- AWS S3 for tile storage
- Amazon Aurora Serverless v2 (PostgreSQL with PostGIS) for spatial queries

**Cost Optimization**:
- Download Sentinel-2 (B4, B8 bands) for fair weather, Sentinel-1 (VV, VH polarization) for monsoon
- Use S3 Intelligent-Tiering for automatic cost optimization
- Implement tile deduplication to avoid re-downloading existing data

### 3. Verification Component (VerificationLambda)

**Responsibility**: Calculate biomass using Multi-Modal Satellite Engine (Sentinel-2 NDVI for fair weather + Sentinel-1 SAR backscatter for monsoon) and quantify carbon sequestration. Pilot demonstrates SAR capability.

**Interface**:
```typescript
interface VerificationRequest {
  farmPlotId: string;
  s3TileKeys: string[];
  satelliteSource: 'SENTINEL_2_OPTICAL' | 'SENTINEL_1_SAR';
  baselineDate?: string;      // For comparison
}

interface VerificationResponse {
  biomassScore: number;       // 0 to 1 (normalized)
  biomassBaseline?: number;
  biomassChange: number;
  carbonSequestrationTons: number;
  verificationStatus: 'APPROVED' | 'REJECTED' | 'NEEDS_REVIEW';
  confidenceScore: number;    // 0-100
  satelliteSource: 'SENTINEL_2_OPTICAL' | 'SENTINEL_1_SAR';
  recommendations?: string[]; // If rejected
}
```

**Dependencies**:
- Amazon SageMaker endpoint hosting Multi-Modal Satellite Engine (Sentinel-2 NDVI + Sentinel-1 SAR biomass models)
- AWS S3 for reading satellite tiles
- Amazon Aurora Serverless v2 (PostgreSQL with PostGIS) for storing verification results

**Algorithm**:
```
// Fair Weather (Cloud Cover < 30%)
NDVI = (NIR - Red) / (NIR + Red)
Biomass Score = f(NDVI)

// Monsoon / Cloudy (Cloud Cover >= 30%)
Biomass Score = f(VV_backscatter, VH_backscatter)
where VV = Vertical-Vertical polarization, VH = Vertical-Horizontal polarization

Carbon Sequestration (tons CO2) = 
  (Biomass_change * plot_area_hectares * 3.67 * biomass_factor)
  
biomass_factor varies by crop type:
  - Trees: 0.5
  - Crops: 0.2
  - Grassland: 0.15
```

**Cost Optimization**:
- Use SageMaker Serverless Inference (pay per invocation)
- Batch multiple farm plots in single inference call
- Cache biomass results for 30 days to avoid recomputation
- Prioritize Sentinel-1 SAR for pilot demonstration (all-weather USP)


### 4. Service Payment Certificate Generation Component (Integrated into EscrowLambda)

**Note:** This component has been integrated into the Escrow & Settlement Engine (EscrowLambda) in the pilot-ready architecture.

**Responsibility**: Generate GCP-compliant service payment certificates as PDF documents after Traffic Light verification.

**Interface**:
```typescript
interface CertificateRequest {
  farmerId: string;
  farmPlotId: string;
  verificationId: string;
  vleId: string;
  carbonTons: number;
  verificationDate: string;
  trafficLightStatus: 'GREEN' | 'YELLOW' | 'RED';
  variance: number;
}

interface CertificateResponse {
  certificateId: string;
  s3Key: string;
  downloadUrl: string;        // Pre-signed URL, expires in 7 days
  expiryDate: string;
  paymentInfo: {
    paymentType: 'E_RUPI_VOUCHER' | 'PFMS_DBT';
    voucherCode?: string;
    pfmsBatchId?: string;
  };
}
```

**Dependencies**:
- Amazon Bedrock (Claude) for generating certificate text
- PDF generation library (e.g., PDFKit or Puppeteer)
- AWS S3 for PDF storage with encryption
- EscrowLambda for payment processing

**Certificate Template**:
- Header: "Green Credit Programme (GCP) Service Payment Certificate"
- Farmer details: Name, ID, Village
- VLE details: Name, ID, Trust Score
- Plot details: Location (lat/lon), Size, Crop type
- Verification: Date, NDVI values, Carbon tons, Traffic Light status
- Payment: Fixed service payment amount, voucher/batch ID
- QR code: Links to audit trail verification
- Digital signature: AWS KMS-signed hash

### 5. Digital Twin Component (TwinLambda)

**Responsibility**: Aggregate village data and generate 3D map visualization payload.

**Interface**:
```typescript
interface DigitalTwinRequest {
  villageId: string;
  includeHistorical: boolean; // Include 6-month trends
}

interface DigitalTwinResponse {
  villageGeometry: GeoJSON.Polygon;
  farmPlots: Array<{
    id: string;
    geometry: GeoJSON.Polygon;
    ndviCurrent: number;
    ndviTrend: 'IMPROVING' | 'STABLE' | 'DECLINING';
    carbonTotal: number;
    cropType: string;
  }>;
  infrastructure: {
    roads: GeoJSON.MultiLineString;
    waterBodies: GeoJSON.MultiPolygon;
    buildings: GeoJSON.MultiPoint;
  };
  degradationHotspots: Array<{
    location: GeoJSON.Point;
    severity: number;         // 0-100
    type: 'EROSION' | 'DROUGHT' | 'DEFORESTATION';
  }>;
}
```

**Dependencies**:
- Amazon Aurora Serverless v2 (PostgreSQL with PostGIS) for spatial aggregation queries
- MapMyIndia API for infrastructure data
- Simple NDVI trend analysis (no ML model needed)

**Cost Optimization**:
- Cache village-level data for 24 hours
- Use PostGIS spatial indexes for fast queries
- Limit MapMyIndia API calls to once per week per village

### 6. Hotspot Detection Component (HotspotLambda)

**Responsibility**: Identify ecological degradation areas using simple NDVI trend analysis.

**Interface**:
```typescript
interface HotspotRequest {
  villageId: string;
  analysisWindow: number;     // Days to analyze (default: 180)
}

interface HotspotResponse {
  hotspots: Array<{
    id: string;
    location: GeoJSON.Point;
    severity: number;
    type: 'EROSION' | 'DROUGHT' | 'DEFORESTATION';
    affectedAreaHectares: number;
    recommendations: string[];
    estimatedCost: number;    // INR for intervention
  }>;
  overallVillageHealth: number; // 0-100
}
```

**Algorithm**:
1. Query Amazon Aurora (PostGIS) for all farm plots in village with NDVI history
2. Calculate NDVI slope (rate of change) for each plot
3. Identify plots with negative slope < -0.05 per month
4. Cluster adjacent declining plots into hotspots
5. Use rule-based logic to recommend interventions based on decline patterns

### 7. DEPRECATED - Risk Calculation Component (Replaced by ThresholdLambda)

**Note:** This component has been replaced by the Threshold Monitor Component (ThresholdLambda) in the pilot-ready architecture. The weighted average approach has been replaced with Boolean threshold logic for transparent crisis detection.

**Original Responsibility**: Calculate migration risk score by correlating income and climate data.

**Replacement**: See Component 12 (Threshold Monitor Component) for the pilot-ready implementation using Boolean thresholds instead of weighted averages.

### 8. DEPRECATED - Prediction Component (Replaced by Boolean Thresholds)

**Note:** This component has been removed in the pilot-ready architecture. Time-series forecasting with Amazon Forecast has been replaced with simple Boolean threshold checks for regulatory transparency and cost optimization.

**Original Responsibility**: Run time-series forecasting to predict migration 90 days ahead.

**Replacement**: See Component 12 (Threshold Monitor Component) for the pilot-ready implementation using rule-based threshold logic.

### 9. Alert Notification Component (AlertLambda)

**Responsibility**: Send migration risk alerts to district officials.

**Interface**:
```typescript
interface AlertRequest {
  riskScore: number;
  villageClusterId: string;
  districtOfficialIds: string[];
}

interface AlertResponse {
  alertId: string;
  notificationsSent: number;
  deliveryStatus: Array<{
    officialId: string;
    channel: 'EMAIL' | 'SMS' | 'DASHBOARD';
    status: 'SENT' | 'FAILED';
  }>;
}
```

**Dependencies**:
- Amazon SNS for SMS notifications
- Amazon SES for email notifications
- WebSocket API for real-time dashboard updates

**Alert Throttling**:
- Maximum 1 alert per village cluster per week
- Batch multiple villages in single email if risk detected simultaneously
- Use SNS topic subscriptions for official preferences

---

## Pilot-Ready Components (Gap Closure)

### 10. Traffic Light Verifier Component (TrafficLightLambda)

**Responsibility**: Detect VLE fraud by comparing VLE-reported data against satellite verification in real-time.

**Interface**:
```typescript
interface TrafficLightRequest {
  vleId: string;
  farmPlotId: string;
  vleReportedData: {
    gpsPolygon: GeoJSON.Polygon;
    cropType: string;
    estimatedBiomass: number;  // VLE's visual assessment
    photos: string[];          // S3 keys for ground photos
  };
  satelliteData: {
    ndviCurrent: number;
    biomassEstimate: number;
    confidenceScore: number;
  };
}

interface TrafficLightResponse {
  status: 'GREEN' | 'YELLOW' | 'RED';
  variance: number;           // Percentage difference
  action: 'AUTO_APPROVE' | 'FLAG_FOR_CALL' | 'FREEZE_ACCOUNT';
  trustScoreUpdate: number;   // New VLE trust score (0-100)
  commissionStatus: 'APPROVED' | 'HELD' | 'FORFEITED';
  reasoning: string;          // Explanation for the decision
}
```

**Algorithm**:
```typescript
function calculateVariance(vleData, satelliteData): number {
  const biomassDiff = Math.abs(vleData.estimatedBiomass - satelliteData.biomassEstimate);
  const variance = (biomassDiff / satelliteData.biomassEstimate) * 100;
  return variance;
}

function determineStatus(variance: number, confidenceScore: number): TrafficLightStatus {
  if (confidenceScore < 80) {
    return 'YELLOW'; // Satellite data uncertain, manual review needed
  }
  
  if (variance < 10) {
    return 'GREEN'; // Auto-approve
  } else if (variance >= 10 && variance <= 30) {
    return 'YELLOW'; // Flag for verification call
  } else {
    return 'RED'; // Freeze account and audit
  }
}

function updateTrustScore(currentScore: number, status: TrafficLightStatus): number {
  if (status === 'GREEN') {
    return Math.min(100, currentScore + 2); // Reward accuracy
  } else if (status === 'YELLOW') {
    return currentScore; // No change, needs clarification
  } else {
    return Math.max(0, currentScore - 15); // Penalize fraud
  }
}
```

**Dependencies**:
- Amazon Aurora Serverless v2 (PostgreSQL with PostGIS) for VLE trust score storage
- SageMaker for satellite biomass estimation
- EventBridge for triggering audit workflows

**Cost Optimization**:
- Run verification only after satellite data is available (not real-time)
- Batch multiple verifications in single SageMaker call
- Cache satellite data for 30 days to avoid recomputation

### 11. Escrow & Settlement Engine (EscrowLambda)

**Responsibility**: Generate sovereign payment vouchers (e-RUPI or PFMS) instead of routing to commodity markets. Uses Configurable Adapter Pattern for pilot-to-production transition.

**Pilot Strategy**: The architecture is designed for API Setu integration (e-RUPI, PFMS, PM-KISAN). For the Pilot Phase, we deploy Mock Adapters that simulate these Government API responses. This allows us to demonstrate the full end-to-end digital workflow and statutory compliance logic without requiring live production credentials. The adapter pattern enables hot-swapping to live APIs when credentials are available.

**Interface**:
```typescript
interface PaymentRequest {
  farmerId: string;
  verificationId: string;
  carbonTons: number;
  paymentSource: 'CSR' | 'GOVERNMENT_GRANT';
  amount: number;             // Fixed service payment (not market price)
}

interface PaymentResponse {
  paymentId: string;
  paymentType: 'E_RUPI_VOUCHER' | 'PFMS_DBT';
  voucherCode?: string;       // For e-RUPI
  pfmsBatchId?: string;       // For PFMS
  redemptionInstructions: string;
  expiryDate: string;
  auditTrail: {
    source: string;
    amount: number;
    purposeCode: string;
    timestamp: string;
  };
}
```

**Adapter Pattern Implementation**:
```typescript
interface IPaymentGateway {
  issueVoucher(request: PaymentRequest): Promise<PaymentResponse>;
  checkStatus(paymentId: string): Promise<PaymentStatus>;
}

class MockPaymentAdapter implements IPaymentGateway {
  // For demos and testing
  async issueVoucher(request: PaymentRequest): Promise<PaymentResponse> {
    return {
      paymentId: `MOCK-${Date.now()}`,
      paymentType: request.paymentSource === 'CSR' ? 'E_RUPI_VOUCHER' : 'PFMS_DBT',
      voucherCode: `DEMO-${Math.random().toString(36).substr(2, 9)}`,
      redemptionInstructions: "Demo voucher - not redeemable",
      expiryDate: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString(),
      auditTrail: {
        source: request.paymentSource,
        amount: request.amount,
        purposeCode: 'AGRI_INPUT',
        timestamp: new Date().toISOString()
      }
    };
  }
  
  async checkStatus(paymentId: string): Promise<PaymentStatus> {
    return { status: 'PENDING', message: 'Mock payment in demo mode' };
  }
}

class LivePaymentAdapter implements IPaymentGateway {
  // For production with API Setu / NPCI
  async issueVoucher(request: PaymentRequest): Promise<PaymentResponse> {
    if (request.paymentSource === 'CSR') {
      return this.generateERUPIVoucher(request);
    } else {
      return this.generatePFMSBatch(request);
    }
  }
  
  private async generateERUPIVoucher(request: PaymentRequest): Promise<PaymentResponse> {
    // Call NPCI e-RUPI API via API Setu
    const response = await fetch('https://api-setu.npci.org.in/erupi/v1/voucher', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.NPCI_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        beneficiaryId: request.farmerId,
        amount: request.amount,
        purposeCode: 'AGRI_INPUT', // Purpose-locked for agricultural inputs only
        expiryDays: 90
      })
    });
    
    const data = await response.json();
    return {
      paymentId: data.voucherId,
      paymentType: 'E_RUPI_VOUCHER',
      voucherCode: data.voucherCode,
      redemptionInstructions: "Redeem at authorized agricultural input dealers",
      expiryDate: data.expiryDate,
      auditTrail: {
        source: 'CSR',
        amount: request.amount,
        purposeCode: 'AGRI_INPUT',
        timestamp: new Date().toISOString()
      }
    };
  }
  
  private async generatePFMSBatch(request: PaymentRequest): Promise<PaymentResponse> {
    // Generate PFMS XML batch file for DBT
    const pfmsXML = `
      <?xml version="1.0" encoding="UTF-8"?>
      <PaymentBatch>
        <BeneficiaryId>${request.farmerId}</BeneficiaryId>
        <Amount>${request.amount}</Amount>
        <SchemeCode>VB-GRAM-G-2025</SchemeCode>
        <VerificationId>${request.verificationId}</VerificationId>
      </PaymentBatch>
    `;
    
    // Upload to PFMS via API Setu
    const batchId = await this.uploadToPFMS(pfmsXML);
    
    return {
      paymentId: batchId,
      paymentType: 'PFMS_DBT',
      pfmsBatchId: batchId,
      redemptionInstructions: "Direct Benefit Transfer to registered bank account",
      expiryDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
      auditTrail: {
        source: 'GOVERNMENT_GRANT',
        amount: request.amount,
        purposeCode: 'VB_GRAM_G',
        timestamp: new Date().toISOString()
      }
    };
  }
  
  async checkStatus(paymentId: string): Promise<PaymentStatus> {
    // Query NPCI/PFMS for payment status
    // Implementation depends on specific API
    return { status: 'PROCESSING', message: 'Payment in progress' };
  }
}

// Factory pattern for environment-based adapter selection
function createPaymentGateway(): IPaymentGateway {
  if (process.env.ENVIRONMENT === 'PRODUCTION') {
    return new LivePaymentAdapter();
  } else {
    return new MockPaymentAdapter();
  }
}
```

**Mock Adapter Strategy (Pilot-to-Production Transition)**:

The Configurable Adapter Pattern enables seamless transition from pilot to production:

| Component | Pilot Phase | Production Phase | Transition Strategy |
|-----------|-------------|------------------|---------------------|
| **e-RUPI Vouchers** | MockPaymentAdapter generates demo voucher codes | LivePaymentAdapter calls NPCI API via API Setu | Environment variable switch, zero code changes |
| **PFMS-DBT** | MockPaymentAdapter generates simulated batch XMLs | LivePaymentAdapter uploads to PFMS portal | Hot-swappable adapter, same interface |
| **PM-KISAN Validation** | Pre-seeded sandbox data (representing API Setu inputs) | Live API Setu PM-KISAN validation | Adapter pattern with configurable data source |
| **e-NAM Market Prices** | Simulated compliance check (mocking e-NAM) | Live API Setu e-NAM integration | Same adapter interface, different implementation |

**Why This Works**:
- **Ambition**: Architecture designed for full API Setu integration from day one
- **Realism**: Acknowledges that government API credentials require months of approval
- **Competence**: Software simulator demonstrates complete digital workflow without manual fallbacks
- **Compliance**: Mock adapters follow exact same data schemas as live APIs

**Deployment Configuration**:
```typescript
// .env.pilot
ENVIRONMENT=PILOT
PAYMENT_ADAPTER=MOCK
PM_KISAN_ADAPTER=MOCK
E_NAM_ADAPTER=MOCK

// .env.production
ENVIRONMENT=PRODUCTION
PAYMENT_ADAPTER=LIVE
PM_KISAN_ADAPTER=LIVE
E_NAM_ADAPTER=LIVE
NPCI_API_KEY=<actual_key>
API_SETU_KEY=<actual_key>
```

**Dependencies**:
- API Setu for NPCI e-RUPI integration (production)
- PFMS API for government DBT (production)
- Amazon Aurora Serverless v2 (PostgreSQL with PostGIS) for audit trail storage
- EventBridge for payment confirmation events

**Cost Optimization**:
- Batch multiple payments in single PFMS XML file
- Cache payment status for 1 hour to reduce API calls
- Use SQS for payment queue management

### 12. Threshold Monitor Component (ThresholdLambda)

**Responsibility**: Implement Boolean threshold logic to detect acute crises instead of weighted averages.

**Interface**:
```typescript
interface ThresholdRequest {
  villageClusterId: string;
  analysisWindow: number;     // Days to analyze (default: 30)
}

interface ThresholdResponse {
  criticalAlerts: Array<{
    type: 'RAINFALL_FAILURE' | 'WATER_CRISIS' | 'DEBT_CRISIS' | 'HEALTH_SHOCK' | 'CROP_FAILURE';
    severity: 'CRITICAL' | 'HIGH';
    value: number;
    threshold: number;
    affectedPopulation: number;
    recommendedAction: string;
  }>;
  overallStatus: 'SAFE' | 'WARNING' | 'CRITICAL';
  triggeredThresholds: number; // Count of failed vital signs
}
```

**Boolean Threshold Algorithm**:
```typescript
function checkCriticalThresholds(villageData: VillageData): ThresholdResponse {
  const alerts: CriticalAlert[] = [];
  
  // Threshold 1: Rainfall Failure
  if (villageData.rainfallPercentage < 50) {
    alerts.push({
      type: 'RAINFALL_FAILURE',
      severity: 'CRITICAL',
      value: villageData.rainfallPercentage,
      threshold: 50,
      affectedPopulation: villageData.totalPopulation,
      recommendedAction: 'Deploy water tankers, activate MGNREGA for water conservation projects'
    });
  }
  
  // Threshold 2: Water Access Crisis
  if (villageData.waterAccessPercentage < 30) {
    alerts.push({
      type: 'WATER_CRISIS',
      severity: 'CRITICAL',
      value: villageData.waterAccessPercentage,
      threshold: 30,
      affectedPopulation: villageData.totalPopulation * (1 - villageData.waterAccessPercentage / 100),
      recommendedAction: 'Emergency water supply, fast-track check dam construction'
    });
  }
  
  // Threshold 3: Debt Crisis (Health Expenditure > Income)
  if (villageData.avgHealthExpenditure > villageData.avgHouseholdIncome) {
    alerts.push({
      type: 'HEALTH_SHOCK',
      severity: 'CRITICAL',
      value: villageData.avgHealthExpenditure,
      threshold: villageData.avgHouseholdIncome,
      affectedPopulation: villageData.householdsInDebt,
      recommendedAction: 'Activate Ayushman Bharat coverage, provide interest-free loans'
    });
  }
  
  // Threshold 4: Crop Failure (NDVI decline > 30%)
  if (villageData.avgNDVIDecline > 30) {
    alerts.push({
      type: 'CROP_FAILURE',
      severity: 'HIGH',
      value: villageData.avgNDVIDecline,
      threshold: 30,
      affectedPopulation: villageData.farmerPopulation,
      recommendedAction: 'Crop insurance claims, alternative livelihood programs'
    });
  }
  
  // Threshold 5: Debt Ratio Crisis
  if (villageData.debtToIncomeRatio > 2.0) {
    alerts.push({
      type: 'DEBT_CRISIS',
      severity: 'CRITICAL',
      value: villageData.debtToIncomeRatio,
      threshold: 2.0,
      affectedPopulation: villageData.householdsInDebt,
      recommendedAction: 'Debt restructuring, NABARD refinancing schemes'
    });
  }
  
  // Determine overall status using ONE-STRIKE logic
  const overallStatus = alerts.some(a => a.severity === 'CRITICAL') ? 'CRITICAL' :
                        alerts.length > 0 ? 'WARNING' : 'SAFE';
  
  return {
    criticalAlerts: alerts,
    overallStatus,
    triggeredThresholds: alerts.length
  };
}
```

**Dependencies**:
- Amazon Aurora Serverless v2 (PostgreSQL with PostGIS) for village vital signs data
- EventBridge for triggering alerts
- No ML models (transparent, rule-based logic)

**Cost Optimization**:
- Run threshold checks weekly (not real-time)
- Cache village data for 24 hours
- Use simple SQL queries instead of complex ML inference

## Data Models

### User Schema (Updated for VLE Support)

```json
{
  "userId": "string (UUID)",
  "role": "FARMER | VLE | SARPANCH | DISTRICT_OFFICIAL | ADMIN",
  "profile": {
    "name": "string",
    "phone": "string",
    "language": "hi | mr | ta",
    "village": "string",
    "district": "string",
    "state": "string"
  },
  "auth": {
    "cognitoId": "string",
    "createdAt": "timestamp",
    "lastLogin": "timestamp"
  },
  "preferences": {
    "voiceSpeed": "number (0.8-1.2)",
    "notificationChannels": ["EMAIL", "SMS", "PUSH"]
  },
  "vleProfile": {
    "trustScore": "number (0-100)",
    "totalVerifications": "number",
    "successfulVerifications": "number",
    "fraudDetections": "number",
    "accountStatus": "ACTIVE | SUSPENDED | TRAINING_REQUIRED",
    "commissionRate": "number (5-12%)",
    "pendingCommission": "number",
    "totalEarnings": "number",
    "lastAuditDate": "timestamp"
  }
}
```

### FarmPlot Schema (GeoJSON)

```json
{
  "type": "Feature",
  "id": "string (UUID)",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [longitude, latitude],
        [longitude, latitude],
        [longitude, latitude],
        [longitude, latitude]
      ]
    ]
  },
  "properties": {
    "farmerId": "string (UUID)",
    "sizeAcres": "number",
    "cropType": "string",
    "registrationDate": "timestamp",
    "lastVerificationDate": "timestamp",
    "ndviHistory": [
      {
        "date": "timestamp",
        "value": "number (0 to 1)",
        "satelliteSource": "Sentinel-1 SAR"
      }
    ],
    "carbonCreditsTotal": "number",
    "status": "ACTIVE | INACTIVE | PENDING_VERIFICATION"
  }
}
```

### Crisis Alert Schema (Updated - Boolean Threshold Logic)

```json
{
  "alertId": "string (UUID)",
  "villageClusterId": "string",
  "generatedAt": "timestamp",
  "overallStatus": "SAFE | WARNING | CRITICAL",
  "triggeredThresholds": "number",
  "criticalAlerts": [
    {
      "type": "RAINFALL_FAILURE | WATER_CRISIS | DEBT_CRISIS | HEALTH_SHOCK | CROP_FAILURE",
      "severity": "CRITICAL | HIGH",
      "value": "number",
      "threshold": "number",
      "affectedPopulation": "number",
      "recommendedAction": "string"
    }
  ],
  "vitalSigns": {
    "rainfallPercentage": "number",
    "waterAccessPercentage": "number",
    "avgHealthExpenditure": "number",
    "avgHouseholdIncome": "number",
    "avgNDVIDecline": "number",
    "debtToIncomeRatio": "number"
  },
  "notifiedOfficials": ["string (userId)"],
  "status": "ACTIVE | ACKNOWLEDGED | RESOLVED",
  "interventionsTaken": [
    {
      "type": "string",
      "date": "timestamp",
      "officialId": "string",
      "notes": "string",
      "budgetAllocated": "number"
    }
  ],
  "resolutionDate": "timestamp"
}
```

### Service Payment Certificate Schema (Updated - Not Tradeable)

```json
{
  "certificateId": "string (UUID)",
  "farmerId": "string (UUID)",
  "farmPlotId": "string (UUID)",
  "verificationId": "string (UUID)",
  "vleId": "string (UUID)",
  "issuedAt": "timestamp",
  "expiresAt": "timestamp",
  "carbonTons": "number",
  "verificationPeriod": {
    "startDate": "timestamp",
    "endDate": "timestamp"
  },
  "complianceInfo": {
    "standard": "GCP (Green Credit Programme - MoEFCC)",
    "methodology": "Domestic Green Credit Rules 2023",
    "verificationBody": "Satellite + Ground Truth Hybrid"
  },
  "s3Key": "string",
  "downloadUrl": "string (pre-signed)",
  "status": "ACTIVE | EXPIRED | REVOKED",
  "paymentInfo": {
    "paymentType": "E_RUPI_VOUCHER | PFMS_DBT",
    "paymentSource": "CSR | GOVERNMENT_GRANT",
    "fixedServicePayment": "number (INR)",
    "voucherCode": "string",
    "pfmsBatchId": "string",
    "redemptionStatus": "PENDING | REDEEMED | EXPIRED",
    "redemptionDate": "timestamp",
    "purposeCode": "AGRI_INPUT | VB_GRAM_G"
  },
  "trafficLightVerification": {
    "status": "GREEN | YELLOW | RED",
    "variance": "number (%)",
    "satelliteConfidence": "number (0-100)",
    "vleCommissionStatus": "APPROVED | HELD | FORFEITED"
  },
  "auditTrail": [
    {
      "event": "VERIFICATION_COMPLETE | PAYMENT_ISSUED | VOUCHER_REDEEMED",
      "timestamp": "timestamp",
      "actor": "string (userId)",
      "details": "string"
    }
  ]
}
```

### VillageCluster Schema (Updated for Frugal Edge)

```json
{
  "clusterId": "string (UUID)",
  "name": "string",
  "district": "string",
  "state": "string",
  "villages": ["string (village IDs)"],
  "geometry": {
    "type": "MultiPolygon",
    "coordinates": "GeoJSON coordinates"
  },
  "statistics": {
    "totalFarmers": "number",
    "totalVLEs": "number",
    "totalFarmPlots": "number",
    "totalCarbonTons": "number",
    "averageNDVI": "number",
    "criticalAlertsActive": "number"
  },
  "costTracking": {
    "monthlyBudget": 2.50,
    "currentMonthSpend": "number",
    "breakdown": {
      "lambda": "number",
      "s3": "number",
      "rds": "number",
      "sagemaker": "number",
      "bedrock": "number",
      "bhashini": "number (should be near zero with edge transcription)",
      "apiSetu": "number"
    },
    "edgeOptimizationSavings": {
      "voiceTranscriptionSaved": "number (90% of calls avoided)",
      "dataBandwidthSaved": "number (MB)",
      "batteryLifeImprovement": "number (hours)"
    }
  },
  "vitalSigns": {
    "rainfallPercentage": "number",
    "waterAccessPercentage": "number",
    "avgHealthExpenditure": "number",
    "avgHouseholdIncome": "number",
    "avgNDVIDecline": "number",
    "debtToIncomeRatio": "number",
    "lastUpdated": "timestamp"
  }
}
```


## Data Flow

### The Data Cascade: Satellite → S3 → SageMaker → Bedrock → PostGIS → Frontend

#### Flow 1: Carbon Credit Verification with Traffic Light Protocol (Primary Flow - 70% of System)

```
1. VLE assists Farmer with Voice Input (Push-to-Talk)
   ↓
2. Mobile App transcribes on-device using Vosk-Lite
   ↓
3. Mobile App → /sync/metadata → API Gateway → VoiceLambda (text only, no audio)
   ↓
4. Bedrock Agent (Intent: "REQUEST_VERIFICATION")
   ↓
5. EventBridge publishes "VerificationRequested" event
   ↓
6. SatelliteLambda triggered
   ↓
7. Query Copernicus Hub for latest imagery
   → IF cloud_cover < 30%: Download Sentinel-2 Optical (NDVI precision)
   → IF cloud_cover >= 30%: Download Sentinel-1 SAR (All-weather capability)
   ↓
8. Download tiles → Store in S3 (s3://bharat-setu-satellite/farm-{id}/tile-{date}.tif)
   ↓
9. EventBridge publishes "SatelliteDataReady" event
   ↓
10. VerificationLambda triggered
    ↓
11. Read tiles from S3 → Invoke SageMaker Multi-Modal Satellite Engine
    → IF Sentinel-2: Calculate NDVI → Convert to biomass
    → IF Sentinel-1 SAR: Calculate backscatter → Convert to biomass
    ↓
12. SageMaker returns biomass scores
    ↓
13. Calculate carbon sequestration
    ↓
14. Store results in Amazon Aurora (farm_verifications table)
    ↓
15. EventBridge publishes "VerificationComplete" event
    ↓
16. TrafficLightLambda triggered (NEW - Fraud Detection)
    ↓
17. Compare VLE_GPS_Polygon vs. Sentinel_Biomass_Signature
    ↓
18. Calculate variance percentage
    ↓
19. IF variance < 10%: GREEN → Auto-approve, update VLE Trust Score (+2)
    IF variance 10-30%: YELLOW → Flag for manual call
    IF variance > 30%: RED → Freeze VLE account, forfeit commission
    ↓
20. IF GREEN: EventBridge publishes "PaymentApproved" event
    ↓
21. EscrowLambda triggered (NEW - Sovereign Payment Rails)
    ↓
22. Determine payment source (CSR or Government Grant)
    ↓
23. IF CSR: Generate e-RUPI voucher (Purpose Code: AGRI_INPUT)
    IF Govt: Generate PFMS-DBT batch XML
    ↓
24. Store payment record in Amazon Aurora (audit trail)
    ↓
25. Send notification to Mobile App via WebSocket
    ↓
26. Farmer receives voucher code + redemption instructions
    ↓
27. VLE receives commission (if Trust Score > 40 and variance < 10%)
```

#### Flow 2: Digital Twin Visualization (15% of System)

```
1. Sarpanch opens Gram-Twin dashboard
   ↓
2. Web Dashboard → API Gateway → TwinLambda
   ↓
3. Amazon Aurora (PostGIS) spatial query: SELECT * FROM farm_plots WHERE village_id = ?
   ↓
4. Aggregate biomass data for all plots
   ↓
5. MapMyIndia API call for infrastructure (roads, water bodies)
   ↓
6. HotspotLambda triggered for degradation analysis
   ↓
7. Simple NDVI trend analysis → Identifies declining areas
   ↓
8. Combine all data into DigitalTwinResponse JSON
   ↓
9. Frontend renders 3D map using Three.js + Mapbox GL
   ↓
10. Sarpanch interacts with map (click plot → show details)
```

#### Flow 3: Crisis Detection with Boolean Thresholds (15% of System)

```
1. Scheduled EventBridge rule (runs weekly)
   ↓
2. ThresholdLambda triggered for all village clusters
   ↓
3. Amazon Aurora (PostGIS) query: Fetch vital signs (rainfall, water, health exp, income, NDVI, debt)
   ↓
4. Check each threshold independently (Boolean logic, not weighted average):
   - IF rainfall < 50% → TRIGGER RAINFALL_FAILURE alert
   - IF water_access < 30% → TRIGGER WATER_CRISIS alert
   - IF health_exp > income → TRIGGER HEALTH_SHOCK alert
   - IF NDVI_decline > 30% → TRIGGER CROP_FAILURE alert
   - IF debt_ratio > 2.0 → TRIGGER DEBT_CRISIS alert
   ↓
5. IF any threshold breached:
   ↓
6. Store crisis alert in Amazon Aurora (crisis_alerts table) with specific failure reasons
   ↓
7. AlertLambda triggered
   ↓
8. SNS sends SMS to district officials with specific crisis type
   ↓
9. SES sends detailed email with recommended interventions
   ↓
10. WebSocket pushes alert to Crisis Map dashboard
    ↓
11. District Official views Crisis Map showing WHY village is red (e.g., "Water Failure")
    ↓
12. Dashboard displays specific vital sign that failed, not generic score
```

### Frugal Edge Data Sync Flow (Updated for Battery & Data Optimization)

```
1. VLE presses and holds Push-to-Talk button in field
   ↓
2. Mobile App activates microphone (Duty Cycling - sensors sleep by default)
   ↓
3. Vosk-Lite transcribes speech to text ON-DEVICE (no cloud call)
   ↓
4. VLE releases button → Transcription complete
   ↓
5. Mobile App displays transcribed text for VLE confirmation
   ↓
6. IF internet available (2G/3G):
   ↓
7. App uploads ONLY text JSON via /sync/metadata (Instant, <5KB)
   ↓
8. VoiceLambda processes text immediately
   ↓
9. IF WiFi detected:
   ↓
10. App uploads queued photos/documents via /sync/media (Heavy, queued)
    ↓
11. S3 stores media files
    ↓
12. IF no internet:
    ↓
13. App stores transcribed text in local SQLite (not raw audio)
    ↓
14. App periodically checks connectivity (every 5 minutes)
    ↓
15. When online: Upload queued text in chronological order
    ↓
16. Send results back to mobile app via push notification
    ↓
17. App displays processing status for each queued request

Battery Life Optimization:
- Mic/GPS sleep 99% of the time (only active during button press)
- No raw audio upload (saves 95% bandwidth)
- Text-only sync uses <1% battery per hour
- Target: 8 hours field operation on single charge
```

### Cost Optimization Data Flow (Updated for Pilot-Ready Architecture)

To maintain the $2.50/month per village cluster budget:

1. **Satellite Data**: Download only once per 10 days (Sentinel-2/Sentinel-1 revisit cycle). Pilot prioritizes Sentinel-1 SAR for all-weather demonstration.
2. **Caching**: Cache biomass results for 30 days in Amazon Aurora
3. **Batching**: Batch multiple farm plots in single SageMaker inference call
4. **Lifecycle**: Move S3 satellite tiles to Glacier after 90 days
5. **Connection Pooling**: Reuse Aurora connections across Lambda invocations
6. **Serverless Inference**: Use SageMaker Serverless (pay per invocation, not per hour)
7. **Lambda ARM64**: 20% cost reduction vs. x86
8. **Reserved Capacity**: Use Aurora Serverless v2 with auto-scaling (scales to zero when idle)
9. **Edge Transcription**: 90% of voice transcriptions happen on-device (zero Bhashini API cost)
10. **Text-Only Sync**: Upload transcribed text (5KB) instead of raw audio (500KB) - 99% bandwidth savings
11. **WiFi-Only Media**: Queue photos/documents for WiFi sync to avoid cellular data charges
12. **Boolean Thresholds**: Replace ML-based risk scoring with simple SQL queries (zero Bedrock/Forecast cost for crisis detection)
13. **Payment Batching**: Batch multiple e-RUPI vouchers or PFMS transfers to reduce API Setu transaction fees
14. **Mock Adapters**: Zero API costs during pilot phase (e-RUPI, PFMS, PM-KISAN, e-NAM all simulated)


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Voice Transcription Accuracy and Latency

*For any* voice input in Hindi, Marathi, or Tamil, the Voice_Interface should transcribe the speech to text with at least 95% accuracy and complete the transcription within 2 seconds.

**Validates: Requirements 1.1**

### Property 2: Farm Data Extraction Completeness

*For any* transcribed text containing farm registration information, the Bedrock_Agent should extract all required fields (location, size, crop type) or generate clarifying questions in the correct language when information is incomplete.

**Validates: Requirements 1.2, 1.3**

### Property 3: Farm Plot Storage Round-Trip

*For any* complete farm details, storing the data in PostGIS and then retrieving it should produce an equivalent farm plot with valid GeoJSON geometry.

**Validates: Requirements 1.4**

### Property 4: Offline Queue Synchronization Order

*For any* sequence of voice recordings stored offline, when connectivity is restored, the recordings should be uploaded and processed in chronological order based on their timestamps.

**Validates: Requirements 1.5, 7.2**

### Property 5: Biomass Calculation Validity

*For any* satellite imagery (Sentinel-2 Optical or Sentinel-1 SAR), the calculated biomass scores should be within the valid range of 0 to 1, and the calculation should use the correct formula for the respective satellite source.

**Validates: Requirements 2.2**

### Property 6: Carbon Sequestration Calculation Accuracy

*For any* biomass change and farm plot area, the carbon sequestration calculation should apply the correct formula with appropriate biomass factors based on crop type.

**Validates: Requirements 2.3**

### Property 7: Certificate Completeness

*For any* verified carbon sequestration above threshold with GREEN traffic light status, the generated certificate should contain all required fields: farmer details, VLE details, plot location, verification date, carbon quantity, traffic light status, and GCP compliance information.

**Validates: Requirements 3.1**

### Property 8: Certificate Retrieval Latency

*For any* certificate retrieval request, the system should provide the PDF within 3 seconds.

**Validates: Requirements 3.4**

### Property 9: Village Boundary Aggregation Completeness

*For any* village, when aggregating farm plot data, all plots whose geometry intersects with the village boundary should be included in the result set.

**Validates: Requirements 4.1**

### Property 10: Digital Twin Data Layer Completeness

*For any* village digital twin request, the response should include all required layers: biomass data, soil organic carbon estimates, MapMyIndia geospatial features, village boundaries, water bodies, roads, and farm plots.

**Validates: Requirements 4.2, 4.3**

### Property 11: Digital Twin Rendering Performance

*For any* village with up to 500 farm plots, the initial digital twin view should render within 5 seconds.

**Validates: Requirements 4.5**

### Property 12: Degradation Hotspot Detection

*For any* farm plot with NDVI declining by more than 0.05 per month over 6 months, the system should identify it as part of a degradation hotspot.

**Validates: Requirements 5.1**

### Property 13: Hotspot Severity Ranking

*For any* set of degradation hotspots, they should be ranked by severity score (0-100) in descending order, where severity is calculated from rate of decline and affected area.

**Validates: Requirements 5.2**

### Property 14: Hotspot Visualization and Recommendations

*For any* degradation hotspot, the system should provide both correct color coding (red for high severity > 70, yellow for moderate 40-70) and appropriate intervention recommendations based on hotspot type.

**Validates: Requirements 5.3, 5.4**

### Property 15: Migration Risk Score Validity

*For any* village cluster, the calculated Migration_Risk_Score should be within the valid range of 0-100 and should increase when income stability decreases or climate risk increases.

**Validates: Requirements 6.2**

### Property 16: High Risk Alert Generation

*For any* village cluster with Migration_Risk_Score exceeding 70, an alert should be generated containing all required fields: village name, risk score, primary risk factors, and affected population estimate.

**Validates: Requirements 6.3**

### Property 17: Alert Notification Timeliness

*For any* generated migration alert, District_Officials should be notified via dashboard and email within 1 hour.

**Validates: Requirements 6.4**

### Property 18: Offline Storage Metadata Completeness

*For any* voice recording stored offline, it should be stored with both timestamp and GPS coordinates metadata.

**Validates: Requirements 7.1**

### Property 19: Upload Progress Feedback

*For any* queued voice recordings being uploaded, the mobile app should display upload progress and estimated completion time.

**Validates: Requirements 7.3**

### Property 20: Role-Based Access Control Enforcement

*For any* user with role R attempting to access resource X, if R does not have permission for X, the system should deny the request with a 403 Forbidden error and log the unauthorized attempt.

**Validates: Requirements 8.2, 8.3, 8.5**

### Property 21: Data Filtering by Role

*For any* Sarpanch accessing Gram_Twin data, the response should contain only aggregated village-level data and should not include individual farmer financial information.

**Validates: Requirements 8.4**

### Property 22: Lambda Memory Limit Compliance

*For any* Lambda function execution, the function should complete within its allocated memory limit without exceeding it.

**Validates: Requirements 9.1**

### Property 23: Request Batching Optimization

*For any* set of AI/ML inference requests arriving within a 5-second window, the system should batch them into a single API call where possible to reduce costs.

**Validates: Requirements 9.4**

### Property 24: Cost Threshold Alerting

*For any* village cluster, when monthly costs are calculated, if the cost exceeds $2.50, the system should flag it in the cost report.

**Validates: Requirements 9.5**

### Property 25: End-to-End Voice Response Latency

*For any* farmer voice input, the total time from input completion to voice response playback should not exceed 3 seconds, and any violations should be logged.

**Validates: Requirements 10.1, 10.2, 10.3, 10.4**

### Property 26: Language Persistence

*For any* farmer who selects a language, all subsequent voice interactions in that session should use the selected language for both transcription and synthesis.

**Validates: Requirements 11.2, 11.3**

### Property 27: Low Confidence Re-prompting

*For any* voice transcription with confidence below 80%, the system should ask the farmer to repeat the input in their selected language.

**Validates: Requirements 11.5**

### Property 28: JWT Token Security Properties

*For any* issued JWT token, it should be signed with RS256 algorithm, have an expiration time of 1 hour for access tokens, and invalid tokens should be rejected by API Gateway.

**Validates: Requirements 12.2, 12.5**

### Property 29: Satellite Data Subscription

*For any* newly registered farm plot, the system should create a subscription for multi-modal satellite data updates (Sentinel-2 Optical + Sentinel-1 SAR) covering the plot's geographic bounding box.

**Validates: Requirements 13.1**

### Property 30: Satellite Imagery Metadata Completeness

*For any* downloaded satellite tile (Sentinel-2 or Sentinel-1 SAR), it should be stored in S3 with complete metadata including acquisition date, satellite source, and quality metrics (cloud cover for optical, signal quality for SAR).

**Validates: Requirements 13.3**

### Property 31: Satellite Data Quality Filtering

*For any* satellite imagery, the system should mark low-quality data (cloud cover > 30% for Sentinel-2, low signal quality for Sentinel-1 SAR) and schedule a retry for the next acquisition cycle.

**Validates: Requirements 13.4**

### Property 32: DEPRECATED - Replaced by Property 45 (Fixed Service Payment Display)

**Note:** This property has been deprecated. Farmers do not view market prices. See Property 45 for the pilot-ready requirement.

### Property 33: DEPRECATED - Replaced by Requirement 17 (Sovereign Payment Rails)

**Note:** This property has been deprecated. Farmers do not connect with buyers. See Requirement 17 for the pilot-ready payment flow.

### Property 34: DEPRECATED - Replaced by Property 44 (Payment Audit Trail)

**Note:** This property has been deprecated. See Property 44 for the pilot-ready audit trail requirements.

### Property 35: Dashboard Metrics Completeness

*For any* District_Official accessing the dashboard, the system should display all required metrics: total carbon credits generated, active farmers count, and migration risk distribution.

**Validates: Requirements 15.1**

### Property 36: Dashboard Filter Performance

*For any* village filter applied by a District_Official, the dashboard should update all metrics to show village-specific data within 2 seconds.

**Validates: Requirements 15.3**

### Property 37: Data Export Completeness

*For any* dashboard data export request, the generated CSV or PDF should contain all currently displayed metrics and charts.

**Validates: Requirements 15.4**

---

## Pilot-Ready Correctness Properties (Gap Closure)

### Property 38: Traffic Light Variance Calculation Accuracy

*For any* VLE-reported biomass estimate and satellite-derived biomass estimate, the variance calculation should use the formula: `variance = |VLE_biomass - Satellite_biomass| / Satellite_biomass * 100`, and the result should be within the range 0-100%.

**Validates: Requirements 16.1**

### Property 39: Traffic Light Status Assignment Correctness

*For any* calculated variance and satellite confidence score, the system should assign GREEN status if variance < 10% and confidence > 80%, YELLOW if variance is 10-30% or confidence < 80%, and RED if variance > 30% and confidence > 80%.

**Validates: Requirements 16.2, 16.3, 16.4**

### Property 40: VLE Trust Score Update Logic

*For any* VLE with current trust score S and traffic light status T, the updated trust score should be: min(100, S+2) if T=GREEN, S if T=YELLOW, or max(0, S-15) if T=RED.

**Validates: Requirements 16.5, 20.3**

### Property 41: Commission Release Conditional Logic

*For any* verification with satellite confidence score C and VLE trust score T, commission should be released only if C > 80 AND T > 40, otherwise commission should be held or forfeited.

**Validates: Requirements 16.5, 20.2**

### Property 42: Payment Source Routing Correctness

*For any* approved verification with payment source S, the system should generate an e-RUPI voucher with purpose code AGRI_INPUT if S = CSR, or generate a PFMS-DBT batch XML if S = GOVERNMENT_GRANT.

**Validates: Requirements 17.2, 17.3**

### Property 43: Voucher Purpose-Locking Enforcement

*For any* generated e-RUPI voucher, the purpose code should be set to AGRI_INPUT, ensuring the voucher can only be redeemed for agricultural inputs and not for other purposes.

**Validates: Requirements 17.2**

### Property 44: Payment Audit Trail Completeness

*For any* processed payment, the audit trail should contain all required fields: payment source, amount, voucher ID or PFMS batch ID, purpose code, timestamp, and redemption status.

**Validates: Requirements 17.4**

### Property 45: Fixed Service Payment Display

*For any* farmer viewing payment information, the system should display fixed service payment rates instead of volatile commodity exchange prices, ensuring zero market risk.

**Validates: Requirements 17.5**

### Property 46: On-Device Transcription Priority

*For any* voice input, the mobile app should attempt transcription using Vosk-Lite on-device first, and only fall back to Bhashini API if Vosk confidence is below 80%.

**Validates: Requirements 18.2**

### Property 47: Text-Only Upload Bandwidth Optimization

*For any* transcribed voice input, the mobile app should upload only the text JSON (not raw audio) to minimize data usage, resulting in uploads of <5KB instead of >500KB.

**Validates: Requirements 18.3**

### Property 48: Duty Cycling Sensor Sleep State

*For any* time when the Push-to-Talk button is not pressed, the mobile app should keep microphone and GPS sensors in sleep mode to conserve battery.

**Validates: Requirements 18.1**

### Property 49: Sync Strategy Differentiation

*For any* data sync operation, metadata (text, coordinates) should be uploaded immediately via /sync/metadata when internet is available, while media files (photos, documents) should be queued for WiFi-only upload via /sync/media.

**Validates: Requirements 18.4, 18.5**

### Property 50: Boolean Threshold Independence

*For any* village vital signs evaluation, each critical threshold (rainfall, water access, health expenditure, crop yield, debt ratio) should be evaluated independently, and a failure in any single threshold should trigger an alert regardless of other factors.

**Validates: Requirements 19.1**

### Property 51: Rainfall Threshold Alert Trigger

*For any* village where rainfall drops below 50% of seasonal average, the system should trigger a RED_ALERT with type RAINFALL_FAILURE, regardless of the status of other vital signs.

**Validates: Requirements 19.2**

### Property 52: Health Expenditure Threshold Alert Trigger

*For any* village where average health expenditure exceeds average household income, the system should trigger a RED_ALERT with type HEALTH_SHOCK, regardless of the status of other vital signs.

**Validates: Requirements 19.3**

### Property 53: Crisis Reason Specificity

*For any* triggered crisis alert, the dashboard should display the specific failure reason (e.g., "Water Failure", "Debt Crisis", "Rainfall Failure") instead of a generic composite score.

**Validates: Requirements 19.4**

### Property 54: Multiple Threshold Breach Handling

*For any* village where multiple critical thresholds are breached simultaneously, the dashboard should display all active crisis triggers ranked by severity in a Crisis Map view.

**Validates: Requirements 19.5**

### Property 55: VLE Commission Hold Until Verification

*For any* VLE-completed farm registration, the calculated commission (5-10% of service payment value) should be marked as HELD until satellite verification completes with confidence score above 80%.

**Validates: Requirements 20.1, 20.2**

### Property 56: Commission Forfeiture on Red Status

*For any* verification that results in RED traffic light status (variance > 30%), the VLE's pending commission should be forfeited and the VLE trust score should be decremented by 15 points.

**Validates: Requirements 20.3**

### Property 57: VLE Account Suspension Threshold

*For any* VLE whose trust score drops below 40, the system should automatically suspend the VLE account and require re-training before reactivation.

**Validates: Requirements 20.4**

### Property 58: VLE Performance Bonus Eligibility

*For any* VLE who maintains a trust score above 90 for 6 consecutive months, the system should increase their commission rate by 2% as a performance bonus.

**Validates: Requirements 20.5**


## Error Handling

### Error Categories and Strategies

#### 1. Voice Processing Errors

**Scenarios**:
- Bhashini API unavailable or rate-limited
- Audio quality too poor for transcription
- Unsupported language or dialect

**Handling**:
- Implement exponential backoff with jitter for API retries (3 attempts)
- Store failed audio in DLQ for manual review
- Respond to farmer with voice message: "I couldn't understand that. Please try again in a quieter location."
- Log error with audio metadata for debugging

**Recovery**:
- Queue audio for retry when Bhashini API recovers
- Notify support team if failure rate exceeds 5% in 1 hour

#### 2. Satellite Data Errors

**Scenarios**:
- Satellite imagery unavailable for requested date range
- High cloud cover (>30%) preventing Sentinel-2 optical analysis
- Low signal quality for Sentinel-1 SAR
- S3 download failures or corrupted tiles

**Handling**:
- Automatically switch from Sentinel-2 to Sentinel-1 SAR if cloud cover > 30%
- Schedule automatic retry in 7 days for next satellite pass
- Notify farmer via voice: "Satellite images are not clear. We'll check again next week."
- Mark verification as "PENDING_RETRY" in database
- Use CloudWatch alarms to detect S3 download failures

**Recovery**:
- Implement S3 multipart download with retry for large tiles
- Multi-modal approach ensures 365-day coverage (optical for fair weather, SAR for monsoon)
- Fall back to alternative SAR sources (ALOS-2) if both Sentinel satellites unavailable for 30 days

#### 3. Biomass Calculation Errors

**Scenarios**:
- SageMaker endpoint unavailable or throttled
- Invalid biomass values (outside 0 to 1 range)
- Insufficient historical baseline data

**Handling**:
- Use SageMaker endpoint auto-scaling to handle traffic spikes
- Validate biomass values and reject outliers with error log
- Require minimum 3 months of baseline data before verification
- Return error to farmer: "We need more time to establish your baseline. Please try again in [X] weeks."

**Recovery**:
- Cache biomass calculations for 30 days to reduce recomputation
- Implement circuit breaker pattern for SageMaker calls (open after 5 consecutive failures)

#### 4. Certificate Generation Errors

**Scenarios**:
- Bedrock API rate limits or service unavailable
- PDF generation library crashes
- S3 upload failures

**Handling**:
- Queue certificate generation requests in SQS with visibility timeout
- Implement idempotency using certificate ID to prevent duplicates
- Store partial certificate data in PostGIS for recovery
- Notify support team for manual intervention if generation fails after 3 attempts

**Recovery**:
- Retry certificate generation from stored verification data
- Generate certificate manually using stored data if automated generation fails

#### 5. Authentication and Authorization Errors

**Scenarios**:
- Expired JWT tokens
- Invalid or tampered tokens
- User attempting unauthorized access

**Handling**:
- Return 401 Unauthorized for expired/invalid tokens with refresh token flow
- Return 403 Forbidden for unauthorized access with clear error message
- Log all unauthorized attempts with user ID, resource, and timestamp
- Implement rate limiting (10 failed auth attempts per minute triggers temporary ban)

**Recovery**:
- Mobile app automatically refreshes tokens before expiration
- Prompt user to re-authenticate if refresh token expired

#### 6. Database Errors

**Scenarios**:
- Amazon Aurora connection pool exhausted
- Query timeout (>30 seconds)
- Deadlocks or constraint violations

**Handling**:
- Implement connection pooling with max 20 connections per Lambda
- Set query timeout to 30 seconds and return error if exceeded
- Use optimistic locking for concurrent updates
- Retry transient errors (connection failures) up to 3 times

**Recovery**:
- Scale Aurora Serverless v2 ACUs if connection pool consistently exhausted
- Add Aurora read replicas for read-heavy queries (dashboard analytics)
- Implement database query caching using ElastiCache

#### 7. Offline Sync Errors

**Scenarios**:
- Local storage full on mobile device
- Sync interrupted mid-upload
- Duplicate recordings uploaded

**Handling**:
- Check available storage before recording and prompt user if <50MB free
- Implement resumable uploads using multipart upload
- Use recording hash to detect and skip duplicates
- Store sync state in local SQLite to resume from last successful upload

**Recovery**:
- Allow user to delete old recordings to free space
- Retry failed uploads automatically when connectivity improves

#### 8. Crisis Alert Errors (Updated for Boolean Thresholds)

**Scenarios**:
- Threshold calculation errors (division by zero, missing data)
- Insufficient historical data for threshold evaluation
- Alert notification delivery failures (email/SMS)

**Handling**:
- Require minimum 30 days of historical data before enabling threshold checks
- Use default safe values if data is missing (e.g., assume worst case)
- Implement SNS delivery status tracking and retry failed notifications
- Store alerts in database even if notification fails

**Recovery**:
- Recalculate thresholds with corrected data if calculation fails
- Display undelivered alerts in dashboard for officials to view manually
- Send digest email with all pending alerts if individual notifications fail

### Error Monitoring and Alerting

**CloudWatch Alarms**:
- Lambda error rate > 5% in 5 minutes → Page on-call engineer
- SageMaker endpoint latency > 10 seconds → Scale endpoint
- Aurora CPU > 80% for 10 minutes → Scale ACUs
- S3 download failures > 10 in 1 hour → Check Copernicus Hub status (Sentinel-2 + Sentinel-1)
- Cost per village cluster > $2.50 → Alert platform operator

**Error Dashboards**:
- Real-time error rate by component (Voice, Satellite, Verification, etc.)
- Error distribution by type (transient, permanent, user error)
- Mean time to recovery (MTTR) for each error category
- User impact metrics (farmers affected, verifications delayed)

### Graceful Degradation

When critical services are unavailable, the platform should degrade gracefully:

1. **Bhashini API down**: Fall back to on-device Vosk-Lite transcription (already primary method)
2. **SageMaker unavailable**: Queue verifications and process when service recovers
3. **Bedrock unavailable**: Use template-based certificate generation
4. **MapMyIndia API down**: Display digital twin without infrastructure layer
5. **API Setu unavailable**: Queue payment vouchers and process when service recovers
6. **Threshold calculation errors**: Use cached vital signs data and alert administrators


## Testing Strategy

### Dual Testing Approach

The Bharat-Setu platform requires both unit tests and property-based tests to ensure comprehensive correctness:

- **Unit tests**: Verify specific examples, edge cases, and error conditions
- **Property tests**: Verify universal properties across all inputs

Both testing approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing Framework

**Framework Selection**: 
- **Python Lambda functions**: Use `hypothesis` library
- **TypeScript/Node.js Lambda functions**: Use `fast-check` library
- **Flutter mobile app**: Use `fast-check` with Jest or Dart's built-in test framework

**Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Each property test must reference its design document property
- Tag format: `Feature: bharat-setu, Property {number}: {property_text}`

**Example Property Test (Python with Hypothesis)**:

```python
from hypothesis import given, strategies as st
import pytest

# Feature: bharat-setu, Property 5: Biomass Calculation Validity
@given(
    vv_backscatter=st.floats(min_value=-30, max_value=0),
    vh_backscatter=st.floats(min_value=-30, max_value=0)
)
def test_biomass_calculation_validity(vv_backscatter, vh_backscatter):
    """
    For any Sentinel-1 SAR imagery, the calculated biomass scores should be 
    within the valid range of 0 to 1.
    """
    biomass = calculate_biomass(vv_backscatter, vh_backscatter)
    assert 0 <= biomass <= 1, f"Biomass {biomass} outside valid range"
```

**Example Property Test (TypeScript with fast-check)**:

```typescript
import fc from 'fast-check';

// Feature: bharat-setu, Property 3: Farm Plot Storage Round-Trip
describe('Farm Plot Storage', () => {
  it('should preserve farm plot data through storage round-trip', () => {
    fc.assert(
      fc.property(
        fc.record({
          farmerId: fc.uuid(),
          sizeAcres: fc.float({ min: 0.1, max: 10 }),
          cropType: fc.constantFrom('rice', 'wheat', 'cotton'),
          location: fc.record({
            latitude: fc.float({ min: 8, max: 37 }),
            longitude: fc.float({ min: 68, max: 97 })
          })
        }),
        async (farmPlot) => {
          const stored = await storeFarmPlot(farmPlot);
          const retrieved = await retrieveFarmPlot(stored.id);
          expect(retrieved).toEqual(farmPlot);
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

### Unit Testing Strategy

**Test Organization**:
- Co-locate tests with source files using `.test.py` or `.test.ts` suffix
- Group tests by component (Voice, Satellite, Verification, etc.)
- Use descriptive test names that explain the scenario

**Coverage Targets**:
- Core business logic: 90% code coverage
- Error handling paths: 80% code coverage
- Integration points: 70% code coverage

**Key Unit Test Scenarios**:

1. **Voice Processing**:
   - Test Bhashini API integration with mock responses
   - Test intent extraction for each supported intent type
   - Test error handling for poor audio quality
   - Test language switching mid-session

2. **Satellite Acquisition**:
   - Test Multi-Modal Satellite API integration with mock imagery (Sentinel-2 + Sentinel-1)
   - Test cloud cover filtering and automatic SAR fallback
   - Test S3 storage with encryption verification
   - Test retry logic for failed downloads

3. **Biomass Calculation**:
   - Test NDVI calculation (Sentinel-2) with known input/output pairs
   - Test SAR backscatter analysis (Sentinel-1) with known input/output pairs
   - Test carbon sequestration calculation for each crop type
   - Test handling of invalid biomass values
   - Test baseline comparison logic

4. **Service Payment Certificate Generation**:
   - Test GCP-compliant certificate format
   - Test PDF generation with all required fields (including VLE and Traffic Light data)
   - Test S3 pre-signed URL generation
   - Test certificate expiration handling
   - Test integration with Escrow & Settlement Engine

5. **Digital Twin**:
   - Test PostGIS spatial aggregation queries
   - Test MapMyIndia API integration
   - Test 3D map payload generation
   - Test rendering performance with large datasets

6. **Crisis Detection with Boolean Thresholds**:
   - Test threshold calculation for each vital sign independently
   - Test alert generation when any single threshold is breached
   - Test Crisis Map visualization with specific failure reasons
   - Test notification delivery (email, SMS, dashboard)
   - Test multiple simultaneous threshold breaches

7. **Traffic Light Protocol**:
   - Test variance calculation with known VLE and satellite data
   - Test GREEN/YELLOW/RED status assignment
   - Test VLE Trust Score updates
   - Test commission release/hold/forfeit logic
   - Test VLE account suspension when Trust Score < 40

8. **Sovereign Payment Rails**:
   - Test e-RUPI voucher generation with purpose code AGRI_INPUT
   - Test PFMS-DBT batch XML generation
   - Test payment adapter pattern (mock vs. live)
   - Test audit trail completeness

7. **Authentication**:
   - Test JWT token generation and validation
   - Test role-based access control for each role
   - Test unauthorized access denial
   - Test token refresh flow

8. **Offline Sync**:
   - Test local storage of voice recordings
   - Test chronological upload order
   - Test duplicate detection
   - Test storage quota management

### Integration Testing

**Test Environments**:
- **Dev**: Isolated environment for development testing
- **Staging**: Production-like environment for pre-release testing
- **Production**: Live environment with canary deployments

**Integration Test Scenarios**:

1. **End-to-End Voice Flow**:
   - Farmer records voice → Transcription → Intent extraction → Verification → Certificate generation
   - Verify all components work together correctly
   - Measure end-to-end latency (<3 seconds)

2. **Satellite Data Pipeline**:
   - Farm registration → Multi-Modal satellite subscription → Imagery download (Sentinel-2/Sentinel-1) → Biomass calculation → Result storage
   - Verify data flows correctly through all stages
   - Test with real Sentinel-2 and Sentinel-1 SAR data
   - Verify automatic fallback from optical to SAR when cloud cover > 30%

3. **Digital Twin Rendering**:
   - Sarpanch login → Village data aggregation → Hotspot detection → 3D map generation
   - Verify all data layers are included
   - Test with villages of varying sizes

4. **Migration Alert Pipeline**:
   - Risk calculation → Forecast prediction → Alert generation → Notification delivery
   - Verify alerts reach officials within 1 hour
   - Test with historical migration data

5. **Offline-to-Online Sync**:
   - Record voice offline → Restore connectivity → Upload queue → Process recordings
   - Verify chronological order is maintained
   - Test with multiple queued recordings

### Performance Testing

**Load Testing**:
- Simulate 1000 concurrent farmers using the voice interface
- Measure Lambda cold start times and optimize
- Test SageMaker endpoint auto-scaling under load
- Verify RDS connection pool handles concurrent queries

**Latency Testing**:
- Voice response latency: Target <3 seconds, measure p50, p95, p99
- Certificate retrieval: Target <3 seconds
- Dashboard filter: Target <2 seconds
- Digital twin rendering: Target <5 seconds

**Cost Testing**:
- Monitor actual AWS costs per village cluster
- Verify costs stay under $2.50/month target
- Identify cost optimization opportunities
- Test lifecycle policies for S3 archival

### Security Testing

**Penetration Testing**:
- Test JWT token tampering and replay attacks
- Test SQL injection in PostGIS queries
- Test unauthorized API access attempts
- Test S3 bucket permissions and encryption

**Compliance Testing**:
- Verify TLS 1.3 enforcement for all API calls
- Verify S3 server-side encryption with KMS
- Verify database SSL/TLS connections
- Verify audit logging for unauthorized access

### Testing with Kiro MCP Server

**Local AWS Testing Strategy**:

Kiro's MCP Server enables safe local testing of AWS Bedrock calls without deploying to AWS:

1. **Setup MCP Server**:
   - Configure `.kiro/settings/mcp.json` with AWS credentials
   - Add Bedrock MCP server for local testing
   - Configure auto-approve for safe operations

2. **Local Bedrock Testing**:
   - Test intent extraction with sample voice transcriptions
   - Test certificate text generation with mock verification data
   - Test correlation analysis with sample income/climate data
   - Verify Bedrock responses before deploying Lambda functions

3. **Mock External Services**:
   - Mock Bhashini API responses for voice testing
   - Mock Copernicus Hub for multi-modal satellite data testing (Sentinel-2 + Sentinel-1)
   - Mock MapMyIndia API for geospatial data testing
   - Mock API Setu adapters (e-RUPI, PFMS, PM-KISAN, e-NAM) for government integration testing
   - Use LocalStack for S3, Lambda, and Aurora local testing

4. **Iterative Development**:
   - Write Lambda function locally
   - Test with MCP Server and mocked services
   - Verify correctness with unit and property tests
   - Deploy to AWS only after local validation

**Example MCP Configuration**:

```json
{
  "mcpServers": {
    "aws-bedrock": {
      "command": "uvx",
      "args": ["mcp-server-aws-bedrock"],
      "env": {
        "AWS_REGION": "us-east-1",
        "AWS_PROFILE": "bharat-setu-dev"
      },
      "disabled": false,
      "autoApprove": ["bedrock:InvokeModel"]
    }
  }
}
```

### Continuous Integration

**CI Pipeline**:
1. Run unit tests on every commit
2. Run property tests on every pull request
3. Run integration tests on staging deployment
4. Run performance tests weekly
5. Run security scans on every release

**Quality Gates**:
- All unit tests must pass (100%)
- Property tests must pass with 100 iterations
- Code coverage must be >80%
- No critical security vulnerabilities
- Performance benchmarks must meet targets

### Test Data Management

**Synthetic Data Generation**:
- Generate synthetic farm plots with realistic coordinates (India bounding box)
- Generate synthetic NDVI time series with seasonal patterns
- Generate synthetic voice transcriptions in Hindi, Marathi, Tamil
- Generate synthetic migration data based on historical patterns

**Test Data Privacy**:
- Never use real farmer data in tests
- Anonymize any production data used for testing
- Use synthetic PII (names, phone numbers, addresses)
- Comply with data protection regulations

### Monitoring and Observability

**Metrics to Track**:
- Voice transcription accuracy (target: >95%)
- NDVI calculation success rate (target: >98%)
- Certificate generation success rate (target: >99%)
- End-to-end latency (target: <3 seconds)
- Cost per village cluster (target: <$2.50/month)
- Error rate by component (target: <1%)

**Logging Strategy**:
- Structured JSON logs for all Lambda functions
- Include correlation ID for request tracing
- Log all errors with stack traces
- Log performance metrics (latency, memory usage)
- Use CloudWatch Logs Insights for analysis

**Distributed Tracing**:
- Use AWS X-Ray for end-to-end request tracing
- Trace voice request through all components
- Identify bottlenecks and optimization opportunities
- Monitor cold start impact on latency
