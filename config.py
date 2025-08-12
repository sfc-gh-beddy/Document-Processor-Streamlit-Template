# =============================================================================
# CDC PERTUSSIS DOCUMENT AI PLATFORM - CONFIGURATION
# =============================================================================

import streamlit as st

# =============================================================================
# SNOWFLAKE ENVIRONMENT CONFIGURATION
# =============================================================================

DATABASE_NAME = "ORBIT"
SCHEMA_NAME = "DOC_AI" 
STAGE_NAME = "ORBIT.DOC_AI.DOC_AI_STAGE"

# =============================================================================
# DOCUMENT AI MODEL CONFIGURATION  
# =============================================================================

AVAILABLE_MODELS = {
    "CDC Pertussis Table Extraction": f"{DATABASE_NAME}.{SCHEMA_NAME}.PERTUSSIS_CDC!PREDICT",
}

DEFAULT_MODEL = "CDC Pertussis Table Extraction"

# =============================================================================
# DATA TABLES CONFIGURATION
# =============================================================================

PREDICTION_RESULTS_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.CDC_PERTUSSIS_PREDICTION_RESULTS"
AI_EXTRACT_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.INFECTIOUS_DISEASE_EXTRACTIONS"

# =============================================================================
# APPLICATION BRANDING
# =============================================================================

APP_TITLE = "🦠 CDC Pertussis Document AI Platform"
APP_SUBTITLE = "Advanced AI-powered document processing for pertussis surveillance and epidemiological data"
DOMAIN_NAME = "CDC Pertussis Surveillance"
DOCUMENT_TYPE = "CDC pertussis surveillance documents"
PRIMARY_USE_CASE = "pertussis epidemiological data"

# =============================================================================
# AI EXTRACT SCHEMA FOR PERTUSSIS DOCUMENTS
# =============================================================================

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
# SEMANTIC MODEL CONFIGURATION
# =============================================================================
# hold off on this for now, we will cover this at a later date
# SEMANTIC_MODEL_FILE = f"@{STAGE_NAME}/epidemiology.yaml"

# =============================================================================
# TABLE CREATION FUNCTIONS
# =============================================================================

def create_tables_if_not_exist(session):
    """Create all necessary tables if they don't exist"""
    
    # Prediction Results Table
    create_prediction_table = f"""
    CREATE TABLE IF NOT EXISTS {PREDICTION_RESULTS_TABLE} (
        FILE_NAME VARCHAR,
        MODEL_USED VARCHAR,
        JSON VARIANT,
        CREATED_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
    )
    """
    
    # AI Extract Results Table
    create_extract_table = f"""
    CREATE TABLE IF NOT EXISTS {AI_EXTRACT_TABLE} (
        extraction_id VARCHAR PRIMARY KEY,
        file_name VARCHAR,
        extraction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
        disease_pathogen VARCHAR,
        reporting_area VARCHAR,
        reporting_period VARCHAR,
        case_counts VARCHAR,
        population_data VARCHAR,
        incidence_rates VARCHAR,
        trend_analysis VARCHAR,
        outbreak_status VARCHAR,
        data_source VARCHAR,
        public_health_actions VARCHAR,
        raw_json VARIANT
    )
    """
    
    try:
        session.sql(create_prediction_table).collect()
        session.sql(create_extract_table).collect()
        st.success("✅ Database tables ready")
    except Exception as e:
        st.error(f"❌ Error creating tables: {str(e)}")

# =============================================================================
# SNOWFLAKE SESSION SETUP
# =============================================================================

def get_snowflake_session():
    """Get Snowflake session with error handling"""
    try:
        from snowflake.snowpark.context import get_active_session
        session = get_active_session()
        
        # Create tables on session start
        create_tables_if_not_exist(session)
        
        return session
    except Exception as e:
        st.error(f"❌ Error connecting to Snowflake: {str(e)}")
        return None