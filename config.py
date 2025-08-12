# =============================================================================
# GINGKO DOCUMENT AI PLATFORM - CONFIGURATION FILE
# =============================================================================
# 
# Instructions for customization:
# 1. Replace all placeholder values with your actual Snowflake configurations
# 2. Update database names, schema names, and stage names to match your environment
# 3. Modify the semantic model file path for your Cortex Analyst setup
# 4. Customize the application branding and context as needed
#
# =============================================================================

# =============================================================================
# SNOWFLAKE DATABASE CONFIGURATION
# =============================================================================

# Main database for document processing
DATABASE_NAME = "YOUR_DATABASE_NAME"  # e.g., "DOCAI_DB"

# Schema for storing processed data
SCHEMA_NAME = "YOUR_SCHEMA_NAME"  # e.g., "PUBLIC"

# Stage for file uploads and processing
STAGE_NAME = f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_STAGE_NAME"  # e.g., "DOCAI_DB.PUBLIC.INFECTIOUS_DISEASES"

# =============================================================================
# TABLE CONFIGURATIONS
# =============================================================================

# Table for storing predictions from your document AI model
PREDICTION_RESULTS_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_PREDICTION_TABLE"  # e.g., "DOCAI_DB.PUBLIC.CDC_PREDICTION_RESULTS"

# Flattened data table for structured results
FLATTENED_DATA_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_FLATTENED_TABLE"  # e.g., "DOCAI_DB.PUBLIC.PERTUSSIS_DATA_FLATTENED"

# AI Extract results table
AI_EXTRACT_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_AI_EXTRACT_TABLE"  # e.g., "DOCAI_DB.PUBLIC.INFECTIOUS_DISEASE_EXTRACTIONS"

# =============================================================================
# DOCUMENT AI MODEL CONFIGURATION
# =============================================================================

# Define multiple CDC infectious disease document AI models
# Add as many models as you have - customers can select at runtime
AVAILABLE_MODELS = {
    "CDC Pertussis Surveillance": f"{DATABASE_NAME}.{SCHEMA_NAME}.GINKGO_TABLE_EXTRACTION_SIMPLE!PREDICT",
    "MMWR Weekly Reports": f"{DATABASE_NAME}.{SCHEMA_NAME}.MMWR_WEEKLY_MODEL!PREDICT", 
    "Outbreak Investigation Reports": f"{DATABASE_NAME}.{SCHEMA_NAME}.OUTBREAK_INVESTIGATION_MODEL!PREDICT",
    "Surveillance Summaries": f"{DATABASE_NAME}.{SCHEMA_NAME}.SURVEILLANCE_SUMMARY_MODEL!PREDICT",
    "NNDSS Annual Reports": f"{DATABASE_NAME}.{SCHEMA_NAME}.NNDSS_ANNUAL_MODEL!PREDICT",
    "State Health Dept Reports": f"{DATABASE_NAME}.{SCHEMA_NAME}.STATE_HEALTH_MODEL!PREDICT",
    "Laboratory Reports": f"{DATABASE_NAME}.{SCHEMA_NAME}.LAB_REPORT_MODEL!PREDICT",
    "Epidemiological Studies": f"{DATABASE_NAME}.{SCHEMA_NAME}.EPI_STUDY_MODEL!PREDICT",
    # Add more CDC-specific models as needed:
    # "Influenza Surveillance": f"{DATABASE_NAME}.{SCHEMA_NAME}.INFLUENZA_MODEL!PREDICT",
    # "COVID-19 Reports": f"{DATABASE_NAME}.{SCHEMA_NAME}.COVID_MODEL!PREDICT",
}

# Default model to select (must be a key from AVAILABLE_MODELS)
DEFAULT_MODEL = "CDC Pertussis Surveillance"

# Legacy setting for backward compatibility
DOCUMENT_AI_MODEL = AVAILABLE_MODELS[DEFAULT_MODEL]

# =============================================================================
# CORTEX ANALYST CONFIGURATION
# =============================================================================

# Semantic model file for Cortex Analyst (update path and filename)
SEMANTIC_MODEL_FILE = f"@{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_SEMANTIC_STAGE/your_semantic_model.yaml"  # e.g., "@DOCAI_DB.PUBLIC.INFECTIOUS_DISEASES/epidemiology.yaml"

# =============================================================================
# APPLICATION BRANDING & CONTEXT
# =============================================================================

# Application title and branding
APP_TITLE = "CDC Document AI Platform"  # e.g., "Gingko Document AI Platform"
APP_SUBTITLE = "Advanced AI-powered document processing for infectious disease surveillance and epidemiological data"

# Domain-specific terminology (customize for your use case)
DOMAIN_NAME = "CDC Infectious Disease Surveillance"
DOCUMENT_TYPE = "CDC surveillance documents"
PRIMARY_USE_CASE = "epidemiological data"

# =============================================================================
# AI EXTRACT SCHEMA CONFIGURATION
# =============================================================================

# Default extraction schema for CDC infectious disease documents
DEFAULT_EXTRACTION_SCHEMA = {
    "disease_pathogen": "What infectious disease or pathogen is this document about?",
    "reporting_area": "What geographic area, region, or jurisdiction is being reported?",
    "reporting_period": "What time period does this report cover (dates, weeks, months)?",
    "case_counts": "What are the case numbers, counts, or statistics mentioned?",
    "population_data": "What population size or demographic information is provided?",
    "incidence_rates": "What are the incidence rates, attack rates, or rates per population?",
    "trend_analysis": "What trends, changes, or comparisons to previous periods are mentioned?",
    "outbreak_status": "Is this an outbreak, epidemic, or routine surveillance? What is the status?",
    "data_source": "What is the source of the data or who reported this information?",
    "public_health_actions": "What public health actions, interventions, or recommendations are mentioned?"
}

# =============================================================================
# FILE PROCESSING CONFIGURATION
# =============================================================================

# Supported file types for upload
SUPPORTED_FILE_TYPES = ['pdf', 'png', 'jpg', 'jpeg', 'docx', 'doc', 'txt', 'html', 'pptx']

# Maximum file size (in bytes) - adjust as needed
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# =============================================================================
# UI CUSTOMIZATION
# =============================================================================

# Status badges for tools
TOOL_STATUS = {
    "document_processor": "Ready",  # or "In Development", "Beta", etc.
    "ai_extract": "Ready",         # or "Enhanced", "New", etc.
    "natural_language_chat": "Ready"
}

# Platform statistics (update with your actual capabilities)
PLATFORM_STATS = {
    "file_formats": "10+",
    "languages": "25+", 
    "ai_tools": "3",
    "custom_extractions": "∞"
}

# =============================================================================
# EXAMPLE PRESET DATA
# =============================================================================

# Example text for different CDC infectious disease document presets
PRESET_EXAMPLES = {
    "custom": {
        "text": "Enter your custom text here...",
        "schema": {
            "field1": "What information do you want to extract?",
            "field2": "Add more fields as needed..."
        }
    },
    "cdc_pertussis_report": {
        "name": "CDC Pertussis Surveillance Report",
        "text": """PERTUSSIS SURVEILLANCE WEEKLY REPORT - Week 15, 2025
U.S. Department of Health and Human Services, Centers for Disease Control and Prevention

NATIONALLY NOTIFIABLE INFECTIOUS DISEASES - PERTUSSIS DATA

Reporting Area: New England Region
Current Week (Week 15): 8 confirmed cases
Cumulative Year-to-Date 2024: 136 cases reported
Cumulative Year-to-Date 2025: 198 cases reported  
52-Week Maximum: 89 cases (peak season)
Population: 14.8 million residents
Incidence Rate: 13.4 cases per 100,000 population
Trend: 45% increase compared to same period last year

Data as of: April 12, 2025
Report Date: April 15, 2025""",
        "schema": {
            "disease": "What disease is being reported?",
            "reporting_area": "What geographic area is being reported?",
            "current_week": "How many cases in the current week?",
            "week_number": "What week number is this?",
            "ytd_2024": "What is the 2024 year-to-date count?",
            "ytd_2025": "What is the 2025 year-to-date count?",
            "population": "What is the population size?",
            "incidence_rate": "What is the incidence rate?",
            "trend": "What trend is mentioned?"
        }
    },
    "outbreak_investigation": {
        "name": "Outbreak Investigation Report",
        "text": """OUTBREAK INVESTIGATION REPORT
Disease: Salmonella Enteritidis food poisoning
Location: Springfield County Health District
Investigation Period: March 10-20, 2025
Cases: 47 confirmed, 23 probable, 12 suspected
Hospitalizations: 8 patients admitted
Deaths: 0
Attack Rate: 35% among exposed individuals
Source: Contaminated eggs from Farm Fresh Poultry
Control Measures: Product recall, restaurant inspection, public health alert
Epidemiological Curve: Peak occurred March 15-16
Laboratory Confirmation: PFGE pattern match confirmed outbreak strain""",
        "schema": {
            "pathogen": "What specific pathogen caused the outbreak?",
            "location": "Where did the outbreak occur?",
            "case_numbers": "List: What are the case counts (confirmed, probable, suspected)?",
            "severity": "How many hospitalizations and deaths?",
            "attack_rate": "What was the attack rate?",
            "source": "What was the source of the outbreak?",
            "control_measures": "List: What control measures were implemented?",
            "investigation_period": "What was the investigation timeframe?",
            "lab_confirmation": "What laboratory methods confirmed the outbreak?"
        }
    },
    "mmwr_report": {
        "name": "MMWR Weekly Report",
        "text": """Morbidity and Mortality Weekly Report (MMWR)
Week Ending April 15, 2025 / Vol. 74 / No. 15

Surveillance for Viral Hepatitis — United States, 2024

During 2024, a total of 3,269 cases of acute hepatitis A, 3,192 cases of acute hepatitis B, and 4,090 cases of hepatitis C were reported to CDC through the National Notifiable Diseases Surveillance System (NNDSS). Compared with 2023, reported cases of acute hepatitis A decreased 12%, acute hepatitis B increased 8%, and hepatitis C increased 15%.

Geographic Distribution: Highest rates of hepatitis A were observed in Kentucky (8.2 cases per 100,000 population), West Virginia (7.8), and Indiana (6.9). The national rate was 1.0 cases per 100,000 population.

Age Distribution: Among hepatitis A cases, 68% occurred among adults aged 30-59 years. For hepatitis B, 45% occurred among adults aged 30-49 years.

Recommendations: Vaccination programs should target high-risk populations, including men who have sex with men, persons who use injection drugs, and international travelers.""",
        "schema": {
            "report_type": "What type of report is this?",
            "reporting_period": "What time period is covered?",
            "diseases_covered": "List: What diseases are covered in this report?",
            "case_counts": "What are the case numbers for each disease?",
            "geographic_patterns": "What geographic patterns are described?",
            "demographic_patterns": "What age or demographic patterns are noted?",
            "trends": "What trends compared to previous periods?",
            "recommendations": "What public health recommendations are made?"
        }
    }
}

# =============================================================================
# VALIDATION SETTINGS
# =============================================================================

# Enable/disable certain features
ENABLE_DATABASE_SAVE = True
ENABLE_FILE_PREVIEW = True
ENABLE_PROGRESS_TRACKING = True

# Error handling
DEBUG_MODE = False  # Set to True for development, False for production