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

# Your trained document AI model name (replace with your actual model)
DOCUMENT_AI_MODEL = f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_MODEL_NAME!PREDICT"  # e.g., "DOCAI_DB.PUBLIC.GINKGO_TABLE_EXTRACTION_SIMPLE!PREDICT"

# =============================================================================
# CORTEX ANALYST CONFIGURATION
# =============================================================================

# Semantic model file for Cortex Analyst (update path and filename)
SEMANTIC_MODEL_FILE = f"@{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_SEMANTIC_STAGE/your_semantic_model.yaml"  # e.g., "@DOCAI_DB.PUBLIC.INFECTIOUS_DISEASES/epidemiology.yaml"

# =============================================================================
# APPLICATION BRANDING & CONTEXT
# =============================================================================

# Application title and branding
APP_TITLE = "Your Document AI Platform"  # e.g., "Gingko Document AI Platform"
APP_SUBTITLE = "Your document processing context here"  # e.g., "Advanced AI-powered document processing for infectious disease surveillance"

# Domain-specific terminology (customize for your use case)
DOMAIN_NAME = "Your Domain"  # e.g., "Infectious Disease Surveillance"
DOCUMENT_TYPE = "your document type"  # e.g., "surveillance documents"
PRIMARY_USE_CASE = "your primary use case"  # e.g., "epidemiological data"

# =============================================================================
# AI EXTRACT SCHEMA CONFIGURATION
# =============================================================================

# Default extraction schema for your domain (customize these questions for your use case)
DEFAULT_EXTRACTION_SCHEMA = {
    "field_1": "Your first extraction question?",  # e.g., "What infectious disease or pathogen is this document about?"
    "field_2": "Your second extraction question?",  # e.g., "What geographic area is being reported?"
    "field_3": "Your third extraction question?",   # e.g., "What time period does this report cover?"
    "field_4": "Your fourth extraction question?",  # e.g., "What are the case numbers mentioned?"
    "field_5": "Your fifth extraction question?",   # e.g., "What population data is provided?"
    "field_6": "Your sixth extraction question?",   # e.g., "What rates or statistics are mentioned?"
    "field_7": "Your seventh extraction question?", # e.g., "What trends are mentioned?"
    "field_8": "Your eighth extraction question?",  # e.g., "What is the status or classification?"
    "field_9": "Your ninth extraction question?",   # e.g., "What is the data source?"
    "field_10": "Your tenth extraction question?"   # e.g., "What actions or recommendations are mentioned?"
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

# Example text for different presets (customize for your domain)
PRESET_EXAMPLES = {
    "custom": {
        "text": "Enter your custom text here...",
        "schema": {
            "field1": "What information do you want to extract?",
            "field2": "Add more fields as needed..."
        }
    },
    "domain_example_1": {
        "name": "Your Domain Example 1",  # e.g., "CDC Pertussis Report"
        "text": "Your example text here...",
        "schema": {
            "field1": "Example question 1?",
            "field2": "Example question 2?"
        }
    },
    "domain_example_2": {
        "name": "Your Domain Example 2",  # e.g., "Outbreak Investigation"
        "text": "Your second example text here...",
        "schema": {
            "field1": "Example question 1?",
            "field2": "Example question 2?"
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