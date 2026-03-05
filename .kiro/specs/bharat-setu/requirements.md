# Requirements Document

## Introduction

Bharat-Setu (The Unified Rural Intelligence Platform) is a frugal innovation platform that integrates Carbon Finance, Ecological Planning, and Crisis Detection to empower rural India. The system enables small farmers (1-2 acres) to earn guaranteed service payments through satellite-verified carbon sequestration, helps village leaders plan ecological projects scientifically, and detects acute distress crises using Boolean threshold logic. Built on AWS Serverless architecture with frugal edge computing, the platform maintains operational costs under $2.50/month per village cluster while serving farmers, VLEs (Village Level Entrepreneurs), Sarpanches (village heads), and district officials.

**Pilot-Ready Architecture**: This system implements adversarial trust verification (Traffic Light Protocol), sovereign payment rails (e-RUPI/PFMS), frugal edge computing (on-device transcription, duty cycling), and transparent crisis detection (Boolean thresholds) to ensure legal compliance, fraud prevention, field usability, and regulatory transparency.

## Glossary

- **Bharat_Setu_Platform**: The unified rural intelligence system comprising Carbon-Kosh, Gram-Twin, and Migration Shield modules
- **Carbon_Kosh**: The core satellite verification engine that enables carbon credit generation for small farmers
- **Gram_Twin**: The ecological planning module that creates digital twins of villages for scientific project planning
- **Migration_Shield**: The predictive analytics module that forecasts distress migration risks
- **Farmer**: A rural agricultural worker with 1-2 acres of land seeking carbon credit income
- **VLE**: Village Level Entrepreneur; a digitally literate local intermediary who assists farmers with registration and verification in exchange for commission
- **Sarpanch**: An elected village head responsible for planning Viksit Bharat G-RAM projects
- **District_Official**: A government administrator monitoring migration risks and rural development
- **Voice_Interface**: The hybrid edge/cloud multilingual voice interaction system using Vosk-Lite (on-device) and Bhashini API (cloud fallback)
- **Satellite_Verification_Engine**: The Amazon SageMaker-based Multi-Modal Satellite Engine using Sentinel-2 (Optical NDVI) for fair weather and Sentinel-1 (SAR Backscatter) for all-weather monsoon verification
- **Bedrock_Agent**: The Amazon Bedrock orchestration layer that interprets intent and triggers workflows
- **NDVI**: Normalized Difference Vegetation Index, a satellite-derived metric for measuring green cover
- **Service_Payment_Certificate**: A government-compliant document certifying verified carbon sequestration for CSR/Grant disbursement (not tradeable on commodity exchanges)
- **Village_Cluster**: A geographic grouping of villages sharing infrastructure and cost allocation
- **LSI**: Livelihood Security Index; a Boolean threshold-based system that triggers alerts when critical vital signs fail
- **Degradation_Hotspot**: A geographic area identified by Amazon Q as having high erosion or drought risk
- **Offline_Queue**: A local storage mechanism that buffers transcribed text when internet connectivity is lost
- **Frugal_Budget**: The architectural constraint of maintaining costs under $2.50/month per village cluster
- **Traffic_Light_Protocol**: An adversarial verification system that compares VLE input against satellite data to detect fraud
- **e-RUPI**: Government-backed digital voucher system for purpose-locked payments (agricultural inputs only)
- **PFMS**: Public Financial Management System for government grant disbursement with audit trails
- **Trust_Score**: A 0-100 metric tracking VLE verification accuracy and honesty over time
- **Duty_Cycling**: Battery optimization technique where sensors (mic/GPS) sleep until explicitly activated
- **Push_to_Talk**: User interaction pattern where voice recording only occurs while button is physically held

## Requirements

### Requirement 1: Voice-Based Farm Registration (VLE-Assisted)

**User Story:** As a VLE, I want to assist farmers with farm plot registration using voice commands in their native language, so that farmers can participate in the carbon sequestration program without requiring literacy or smartphone expertise.

#### Acceptance Criteria

1. WHEN a VLE presses and holds the Push_to_Talk button, THE mobile app SHALL activate the microphone and transcribe speech to text on-device using Vosk-Lite
2. WHEN on-device transcription confidence is below 80%, THE Voice_Interface SHALL fall back to Bhashini API for cloud-based transcription
3. WHEN the Voice_Interface receives a farm registration request, THE Bedrock_Agent SHALL extract farm location, size, and crop type from the transcribed text
4. WHEN the Bedrock_Agent cannot extract required information, THE Voice_Interface SHALL prompt the VLE with clarifying questions in the selected language
5. WHEN farm details are complete, THE Bharat_Setu_Platform SHALL store the farm plot data in PostGIS with GeoJSON geometry and associate it with the VLE's ID for commission tracking

### Requirement 2: Satellite-Based Green Cover Verification

**User Story:** As a Farmer, I want my green cover to be verified automatically using satellite data, so that I can receive carbon credits without installing expensive sensors or waiting for manual inspections.

#### Acceptance Criteria

1. WHEN a carbon credit verification is requested, THE Satellite_Verification_Engine SHALL retrieve the most recent satellite imagery (Sentinel-2 Optical or Sentinel-1 SAR) for the farm plot from AWS S3
2. WHEN cloud cover is less than 30%, THE Satellite_Verification_Engine SHALL use Sentinel-2 Optical imagery to calculate NDVI values for high-precision biomass estimation
3. WHEN cloud cover exceeds 30% or during monsoon season, THE Satellite_Verification_Engine SHALL automatically switch to Sentinel-1 SAR imagery for all-weather biomass estimation using backscatter analysis
4. WHEN biomass values indicate green cover increase above baseline, THE Satellite_Verification_Engine SHALL quantify carbon sequestration in metric tons CO2 equivalent
5. WHEN biomass values indicate no significant green cover change, THE Bharat_Setu_Platform SHALL notify the Farmer with improvement recommendations via voice
6. WHEN satellite imagery is unavailable for both sources, THE Bharat_Setu_Platform SHALL schedule automatic retry within 7 days and notify the Farmer

### Requirement 3: Service Payment Certificate Generation

**User Story:** As a Farmer, I want to receive a government-compliant service payment certificate as a PDF document, so that I can present it to receive my guaranteed service payment through e-RUPI vouchers or PFMS direct benefit transfer.

#### Acceptance Criteria

1. WHEN carbon sequestration is verified above threshold and Traffic Light status is GREEN, THE Bharat_Setu_Platform SHALL generate a GCP-compliant certificate containing farmer details, plot location, verification date, carbon quantity, and VLE verification details
2. WHEN the certificate is generated, THE Bharat_Setu_Platform SHALL store the PDF in AWS S3 with encrypted access
3. WHEN the certificate is stored, THE Bharat_Setu_Platform SHALL send a download link to the Farmer via SMS and trigger the Escrow_Settlement_Engine for payment processing
4. WHEN the Farmer requests certificate retrieval, THE Bharat_Setu_Platform SHALL provide the PDF within 3 seconds
5. WHEN certificate generation fails, THE Bharat_Setu_Platform SHALL log the error and notify support personnel for manual review

### Requirement 4: Village Digital Twin Visualization

**User Story:** As a Sarpanch, I want to view a 3D digital twin of my village showing ecological data, so that I can plan Viksit Bharat G-RAM projects scientifically and allocate resources to areas with highest need.

#### Acceptance Criteria

1. WHEN a Sarpanch accesses Gram_Twin, THE Bharat_Setu_Platform SHALL aggregate all farm plot data within the village boundary from PostGIS
2. WHEN aggregated data is available, THE Gram_Twin SHALL overlay NDVI data, soil organic carbon estimates, and MapMyIndia geospatial features on a 3D map
3. WHEN the 3D map is rendered, THE Gram_Twin SHALL display village boundaries, water bodies, roads, and farm plots with color-coded health indicators
4. WHEN the Sarpanch selects a farm plot, THE Gram_Twin SHALL display detailed metrics including NDVI trend, carbon sequestration history, and crop type
5. WHEN the map is loaded, THE Gram_Twin SHALL render the initial view within 5 seconds on standard mobile devices

### Requirement 5: Ecological Degradation Hotspot Identification

**User Story:** As a Sarpanch, I want the system to automatically identify degradation hotspots in my village, so that I can prioritize water conservation and soil restoration projects in the most critical areas.

#### Acceptance Criteria

1. WHEN Gram_Twin analyzes village data, THE Amazon_Q SHALL identify areas with declining NDVI trends over 6 months as degradation hotspots
2. WHEN degradation hotspots are identified, THE Gram_Twin SHALL rank them by severity score (0-100) based on rate of decline and affected area
3. WHEN hotspots are ranked, THE Gram_Twin SHALL overlay them on the digital twin map with red markers for high severity and yellow for moderate
4. WHEN a Sarpanch selects a hotspot, THE Gram_Twin SHALL display recommended interventions such as check dams, tree plantation, or contour bunding
5. WHEN no degradation hotspots exist, THE Gram_Twin SHALL display a positive message and show areas with improving ecological health

### Requirement 6: Crisis Detection with Boolean Thresholds

**User Story:** As a District_Official, I want to receive immediate alerts when any critical vital sign fails in a village (rainfall, water, health, crop, debt), so that I can deploy targeted interventions before acute crises escalate into distress migration.

#### Acceptance Criteria

1. WHEN the Threshold_Monitor analyzes village data, THE Bharat_Setu_Platform SHALL evaluate each critical threshold independently (Rainfall < 50%, Water Access < 30%, Health_Exp > Income, NDVI_Decline > 30%, Debt_Ratio > 2.0)
2. WHEN any single threshold is breached, THE Bharat_Setu_Platform SHALL trigger a RED_ALERT with the specific failure type (RAINFALL_FAILURE, WATER_CRISIS, HEALTH_SHOCK, CROP_FAILURE, DEBT_CRISIS)
3. WHEN an alert is generated, THE Bharat_Setu_Platform SHALL notify District_Officials via secure dashboard and email within 1 hour with specific crisis type and recommended interventions
4. WHEN a District_Official views an alert, THE Crisis_Map SHALL display the specific vital sign that failed, the current value vs. threshold, and affected population
5. WHEN multiple thresholds are breached simultaneously, THE Crisis_Map SHALL display all active crisis triggers ranked by severity with specific intervention recommendations for each

### Requirement 7: Offline-First Mobile Application with Edge Transcription

**User Story:** As a VLE, I want the mobile app to work even when I have no internet connection, so that I can transcribe voice requests on-device and sync the text data automatically when connectivity returns.

#### Acceptance Criteria

1. WHEN the mobile app detects no internet connectivity, THE Offline_Queue SHALL store transcribed text locally with timestamp and GPS coordinates (not raw audio)
2. WHEN internet connectivity is restored, THE Offline_Queue SHALL automatically upload queued text data to the Bharat_Setu_Platform in chronological order via /sync/metadata endpoint
3. WHEN text data is uploading, THE mobile app SHALL display upload progress and estimated completion time
4. WHEN all queued data is uploaded, THE mobile app SHALL notify the VLE and display processing status for each request
5. WHEN local storage exceeds 100MB, THE Offline_Queue SHALL prompt the VLE to connect to internet or delete old data

### Requirement 8: Role-Based Access Control

**User Story:** As a System_Administrator, I want to enforce strict role-based access control, so that Farmers cannot access migration prediction data and District_Officials cannot access farmer bank account information, ensuring privacy and data security.

#### Acceptance Criteria

1. WHEN a user authenticates, THE Bharat_Setu_Platform SHALL assign role-specific permissions (Farmer, Sarpanch, District_Official, Administrator) via AWS Cognito JWT tokens
2. WHEN a Farmer attempts to access Migration_Shield data, THE Bharat_Setu_Platform SHALL deny the request and return a 403 Forbidden error
3. WHEN a District_Official attempts to access farmer bank account details, THE Bharat_Setu_Platform SHALL deny the request and return a 403 Forbidden error
4. WHEN a Sarpanch accesses Gram_Twin, THE Bharat_Setu_Platform SHALL display only aggregated village-level data without individual farmer financial information
5. WHEN an unauthorized access attempt occurs, THE Bharat_Setu_Platform SHALL log the event with user ID, timestamp, and attempted resource for security audit

### Requirement 9: Frugal Architecture Cost Optimization

**User Story:** As a Platform_Operator, I want the system to maintain operational costs under $2.50/month per village cluster, so that the platform remains financially sustainable and scalable to thousands of villages across India.

#### Acceptance Criteria

1. WHEN the Bharat_Setu_Platform processes requests, THE AWS_Lambda_Functions SHALL execute within allocated memory limits to minimize compute costs
2. WHEN satellite imagery is retrieved, THE Bharat_Setu_Platform SHALL cache Sentinel-2 tiles in S3 with lifecycle policies to archive data older than 90 days to Glacier
3. WHEN database queries are executed, THE PostGIS_Database SHALL use connection pooling and query optimization to minimize RDS instance hours
4. WHEN AI/ML models are invoked, THE Bharat_Setu_Platform SHALL batch requests where possible to reduce Amazon Bedrock and SageMaker API call costs
5. WHEN monthly costs are calculated, THE Bharat_Setu_Platform SHALL generate a cost report showing per-village-cluster expenses and flag any cluster exceeding $2.50 threshold

### Requirement 10: Voice Response Latency

**User Story:** As a Farmer, I want to receive voice responses within 3 seconds of speaking my request, so that the interaction feels natural and I remain engaged with the system rather than abandoning the session.

#### Acceptance Criteria

1. WHEN a Farmer completes a voice input, THE Voice_Interface SHALL begin transcription within 500 milliseconds
2. WHEN transcription is complete, THE Bedrock_Agent SHALL process intent and trigger appropriate workflow within 1 second
3. WHEN workflow processing is complete, THE Voice_Interface SHALL generate and play voice response within 1.5 seconds
4. WHEN total response time exceeds 3 seconds, THE Bharat_Setu_Platform SHALL log the latency event for performance optimization analysis
5. WHEN network latency is high, THE Bharat_Setu_Platform SHALL prioritize voice response generation over non-critical background tasks

### Requirement 11: Multi-Language Voice Support

**User Story:** As a Farmer, I want to interact with the system in my native language (Hindi, Marathi, or Tamil), so that I can use the platform without language barriers or requiring English proficiency.

#### Acceptance Criteria

1. WHEN a Farmer first launches the app, THE Voice_Interface SHALL prompt language selection with voice samples in Hindi, Marathi, and Tamil
2. WHEN a language is selected, THE Voice_Interface SHALL configure Bhashini API with the selected language for all subsequent interactions
3. WHEN the Voice_Interface generates responses, THE Bhashini_API SHALL synthesize speech in the Farmer's selected language with natural prosody
4. WHEN a Farmer switches language mid-session, THE Voice_Interface SHALL update the language setting and confirm the change via voice in the new language
5. WHEN voice transcription confidence is below 80%, THE Voice_Interface SHALL ask the Farmer to repeat the input in their selected language

### Requirement 12: Secure Data Transmission

**User Story:** As a Security_Officer, I want all data transmitted between mobile apps and backend services to be encrypted, so that sensitive farmer information and government data remain protected from interception or tampering.

#### Acceptance Criteria

1. WHEN the mobile app communicates with API Gateway, THE Bharat_Setu_Platform SHALL enforce TLS 1.3 encryption for all HTTP requests
2. WHEN JWT tokens are issued, THE AWS_Cognito SHALL sign tokens with RS256 algorithm and set expiration to 1 hour for access tokens
3. WHEN sensitive data is stored in S3, THE Bharat_Setu_Platform SHALL enable server-side encryption with AWS KMS-managed keys
4. WHEN database connections are established, THE PostGIS_Database SHALL require SSL/TLS connections and reject unencrypted attempts
5. WHEN API requests are received, THE API_Gateway SHALL validate JWT token signature and expiration before forwarding to Lambda functions

### Requirement 13: Satellite Data Acquisition and Storage

**User Story:** As a Data_Engineer, I want the system to automatically acquire and store multi-modal satellite imagery for registered farm plots, so that verification can occur without manual data procurement delays and works in all weather conditions.

#### Acceptance Criteria

1. WHEN a new farm plot is registered, THE Bharat_Setu_Platform SHALL subscribe to both Sentinel-2 Optical and Sentinel-1 SAR data updates for the plot's geographic bounding box
2. WHEN new satellite imagery is available, THE Bharat_Setu_Platform SHALL download relevant tiles from Copernicus Open Access Hub within 24 hours
3. WHEN Sentinel-2 imagery is downloaded, THE Bharat_Setu_Platform SHALL store raw tiles in S3 with metadata including acquisition date, cloud cover percentage, and tile ID
4. WHEN Sentinel-1 SAR imagery is downloaded, THE Bharat_Setu_Platform SHALL store raw tiles in S3 with metadata including acquisition date, polarization bands, and signal quality
5. WHEN cloud cover exceeds 30% for Sentinel-2, THE Bharat_Setu_Platform SHALL automatically prioritize Sentinel-1 SAR data for verification
6. WHEN storage quota is reached, THE Bharat_Setu_Platform SHALL archive oldest imagery to S3 Glacier and maintain only recent 6 months in standard storage

### Requirement 14: DEPRECATED - Replaced by Requirement 17 (Sovereign Payment Rails)

**Note:** This requirement has been deprecated in the pilot-ready architecture. Farmers do not access commodity markets directly. Instead, they receive guaranteed service payments through e-RUPI vouchers (CSR) or PFMS-DBT (Government Grants) as specified in Requirement 17.

**Rationale:** Under the Green Credit Programme (GCP) and VB-GRAM-G Act 2025, smallholder carbon credits are not tradeable on commodity exchanges like NCDEX. Farmers receive fixed service payments to eliminate market risk and ensure regulatory compliance.

### Requirement 15: Crisis Map Dashboard for Officials

**User Story:** As a District_Official, I want to view a Crisis Map showing specific vital sign failures across all villages in my district, so that I can identify acute crises, allocate budgets to specific interventions, and report progress to state government.

#### Acceptance Criteria

1. WHEN a District_Official accesses the dashboard, THE Bharat_Setu_Platform SHALL display total service payments issued, active farmers, active VLEs, and crisis alert distribution across the district
2. WHEN the Crisis Map is displayed, THE dashboard SHALL show villages color-coded by status (Green = Safe, Yellow = Warning, Red = Critical) with specific crisis types labeled
3. WHEN the District_Official filters by village, THE dashboard SHALL update all metrics to show village-specific data within 2 seconds, including which vital signs failed
4. WHEN the District_Official exports data, THE Bharat_Setu_Platform SHALL generate CSV or PDF reports with all displayed metrics, crisis types, and recommended interventions
5. WHEN data is refreshed, THE dashboard SHALL pull latest vital signs data from PostGIS and update visualizations without requiring page reload

---

## Pilot-Ready Requirements (Gap Closure)

### Requirement 16: VLE Trust Verification (Traffic Light Protocol)

**User Story:** As a System_Administrator, I want to automatically detect fraudulent VLE registrations by comparing VLE-reported data against satellite verification, so that commission-based fraud is prevented and statutory audit compliance is maintained.

#### Acceptance Criteria

1. WHEN a VLE submits farm registration data with GPS coordinates, THE Traffic_Light_Verifier SHALL compare the VLE_GPS_Polygon against satellite biomass signature (from Sentinel-2 or Sentinel-1 depending on weather) within 24 hours
2. WHEN the variance between VLE data and satellite data is less than 10%, THE Bharat_Setu_Platform SHALL assign a GREEN status and auto-approve the registration
3. WHEN the variance is between 10% and 30%, THE Bharat_Setu_Platform SHALL assign a YELLOW status and flag the registration for manual verification call
4. WHEN the variance exceeds 30%, THE Bharat_Setu_Platform SHALL assign a RED status, freeze the VLE account, and trigger an audit workflow
5. WHEN a VLE completes a verification, THE Bharat_Setu_Platform SHALL update the VLE_Trust_Score based on historical accuracy and only release commission if Satellite_Confidence_Score exceeds 80%

### Requirement 17: Sovereign Payment Rails (Escrow & Settlement)

**User Story:** As a Farmer, I want to receive guaranteed service payments through government-approved voucher systems rather than market-traded credits, so that I have zero market risk and my payments are purpose-locked for agricultural inputs.

#### Acceptance Criteria

1. WHEN a carbon sequestration verification is approved, THE Escrow_Settlement_Engine SHALL determine the payment source (CSR or Government Grant)
2. WHEN the payment source is CSR, THE Bharat_Setu_Platform SHALL generate an e-RUPI voucher with purpose code AGRI_INPUT that can only be redeemed for agricultural supplies
3. WHEN the payment source is Government Grant, THE Bharat_Setu_Platform SHALL generate a PFMS-DBT batch XML file for direct benefit transfer with full audit trail
4. WHEN a payment is processed, THE Bharat_Setu_Platform SHALL record the transaction in the audit ledger with source, amount, voucher ID, and redemption status
5. WHEN a Farmer attempts to view market prices, THE Bharat_Setu_Platform SHALL display fixed service payment rates instead of volatile commodity exchange prices

### Requirement 18: Frugal Edge Protocol (Battery & Data Optimization)

**User Story:** As a VLE, I want the mobile app to work for a full 8-hour field day on a single battery charge with intermittent 2G connectivity, so that I can assist multiple farmers without worrying about power or data costs.

#### Acceptance Criteria

1. WHEN the mobile app is idle, THE Bharat_Setu_Platform SHALL keep microphone and GPS sensors in sleep mode (Duty Cycling) to conserve battery
2. WHEN a VLE presses and holds the Push_to_Talk button, THE mobile app SHALL activate the microphone and transcribe speech to text on-device using Vosk-Lite
3. WHEN transcription is complete, THE mobile app SHALL immediately upload only the text JSON (not raw audio) to minimize data usage
4. WHEN internet connectivity is available, THE mobile app SHALL sync metadata immediately via /sync/metadata endpoint (lightweight, <5KB per request)
5. WHEN WiFi connectivity is detected, THE mobile app SHALL queue and upload media files (photos, documents) via /sync/media endpoint to avoid cellular data charges

### Requirement 19: One-Strike Distress Alert System (Boolean Threshold Logic)

**User Story:** As a District_Official, I want to receive immediate alerts when any critical vital sign fails in a village, so that I can deploy interventions before acute crises escalate into distress migration.

#### Acceptance Criteria

1. WHEN the Migration_Shield analyzes village data, THE Bharat_Setu_Platform SHALL evaluate each critical threshold independently (Rainfall, Water Access, Health Expenditure, Crop Yield, Debt Ratio)
2. WHEN Rainfall drops below 50% of seasonal average, THE Bharat_Setu_Platform SHALL trigger a RED_ALERT regardless of other factors
3. WHEN Health_Expenditure exceeds household income, THE Bharat_Setu_Platform SHALL trigger a RED_ALERT regardless of other factors
4. WHEN any critical threshold is breached, THE dashboard SHALL display the specific failure reason (e.g., "Water Failure", "Debt Crisis") instead of a generic composite score
5. WHEN multiple thresholds are breached simultaneously, THE dashboard SHALL rank alerts by severity and display all active crisis triggers in a Crisis Map view

### Requirement 20: VLE Commission Accountability

**User Story:** As a Platform_Operator, I want VLE commissions to be released only after satellite verification confirms accuracy, so that VLEs are incentivized to provide truthful data rather than maximize registrations.

#### Acceptance Criteria

1. WHEN a VLE completes a farm registration, THE Bharat_Setu_Platform SHALL calculate a Pending_Commission (5-10% of service payment value) but mark it as HELD
2. WHEN satellite verification completes with Confidence_Score above 80%, THE Bharat_Setu_Platform SHALL release the commission to the VLE's account
3. WHEN satellite verification shows variance above 30% (RED status), THE Bharat_Setu_Platform SHALL forfeit the commission and deduct points from VLE_Trust_Score
4. WHEN a VLE's Trust_Score drops below 40, THE Bharat_Setu_Platform SHALL suspend the VLE account and require re-training before reactivation
5. WHEN a VLE maintains Trust_Score above 90 for 6 months, THE Bharat_Setu_Platform SHALL increase their commission rate by 2% as a performance bonus
