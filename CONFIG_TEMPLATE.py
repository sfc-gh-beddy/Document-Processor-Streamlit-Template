# =============================================================================
# CUSTOMER CONFIGURATION TEMPLATE
# =============================================================================
# 
# INSTRUCTIONS:
# 1. Replace ALL values in this file with your actual Snowflake configurations
# 2. Save this file as "config.py" in your project root
# 3. Test your configuration by running the application locally
#
# =============================================================================

# =============================================================================
# 🏢 YOUR SNOWFLAKE ENVIRONMENT - REQUIRED
# =============================================================================

# Replace with your actual Snowflake database information
DATABASE_NAME = "YOUR_DATABASE_NAME"        # Example: "DOCUMENT_AI_DB"
SCHEMA_NAME = "YOUR_SCHEMA_NAME"             # Example: "PUBLIC" or "PROCESSING"
STAGE_NAME = f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_STAGE_NAME"  # Example: "DOCUMENT_AI_DB.PUBLIC.FILE_UPLOADS"

# =============================================================================
# 📊 YOUR DATA TABLES - REQUIRED
# =============================================================================

# These tables will be auto-created if they don't exist
PREDICTION_RESULTS_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_PREDICTION_TABLE"    # Example: "DOCUMENT_AI_DB.PUBLIC.PREDICTION_RESULTS"
FLATTENED_DATA_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_FLATTENED_TABLE"        # Example: "DOCUMENT_AI_DB.PUBLIC.DOCUMENT_DATA_FLATTENED"
AI_EXTRACT_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_AI_EXTRACT_TABLE"           # Example: "DOCUMENT_AI_DB.PUBLIC.AI_EXTRACTIONS"

# =============================================================================
# 🤖 YOUR TRAINED DOCUMENT AI MODELS - REQUIRED
# =============================================================================

# List ALL your trained Document AI models here
# Users will select from this dropdown in the Document Processor
AVAILABLE_MODELS = {
    "Your Model 1 Name": f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_MODEL_1_NAME!PREDICT",
    "Your Model 2 Name": f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_MODEL_2_NAME!PREDICT", 
    "Your Model 3 Name": f"{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_MODEL_3_NAME!PREDICT",
    # Add more models as needed:
    # "Invoice Processing": f"{DATABASE_NAME}.{SCHEMA_NAME}.INVOICE_MODEL!PREDICT",
    # "Contract Analysis": f"{DATABASE_NAME}.{SCHEMA_NAME}.CONTRACT_MODEL!PREDICT",
}

# Set which model is selected by default (must be a key from AVAILABLE_MODELS above)
DEFAULT_MODEL = "Your Model 1 Name"

# Legacy setting for backward compatibility
DOCUMENT_AI_MODEL = AVAILABLE_MODELS[DEFAULT_MODEL]

# =============================================================================
# 💬 CORTEX ANALYST CONFIGURATION - OPTIONAL
# =============================================================================

# If you want to use the Natural Language Chat feature, create a semantic model YAML file
# and upload it to your Snowflake stage, then update the path below
SEMANTIC_MODEL_FILE = f"@{DATABASE_NAME}.{SCHEMA_NAME}.YOUR_STAGE_NAME/your_semantic_model.yaml"

# =============================================================================
# 🎨 YOUR APPLICATION BRANDING - OPTIONAL
# =============================================================================

# Customize these to match your organization and use case
APP_TITLE = "Your Document AI Platform"
APP_SUBTITLE = "Your document processing description"

# Domain-specific terminology
DOMAIN_NAME = "Your Domain"                    # Example: "Financial Document Processing"
DOCUMENT_TYPE = "your document types"          # Example: "invoices and contracts"
PRIMARY_USE_CASE = "your use case"             # Example: "financial data extraction"

# =============================================================================
# 🔍 AI EXTRACT SCHEMA CONFIGURATION - OPTIONAL
# =============================================================================

# Customize these questions based on what you want to extract from your documents
DEFAULT_EXTRACTION_SCHEMA = {
    "field_1": "What is your first extraction question?",
    "field_2": "What is your second extraction question?",
    "field_3": "What is your third extraction question?",
    "field_4": "What is your fourth extraction question?",
    "field_5": "What is your fifth extraction question?",
    "field_6": "What is your sixth extraction question?",
    "field_7": "What is your seventh extraction question?",
    "field_8": "What is your eighth extraction question?",
    "field_9": "What is your ninth extraction question?",
    "field_10": "What is your tenth extraction question?"
}

# =============================================================================
# 📁 FILE PROCESSING CONFIGURATION - OPTIONAL
# =============================================================================

# File types that can be uploaded and processed
SUPPORTED_FILE_TYPES = ['pdf', 'png', 'jpg', 'jpeg', 'docx', 'doc', 'txt', 'html', 'pptx']

# Maximum file size (in bytes) - adjust as needed
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# =============================================================================
# 🎛️ UI CUSTOMIZATION - OPTIONAL
# =============================================================================

# Status badges for tools in the home page
TOOL_STATUS = {
    "document_processor": "Ready",
    "ai_extract": "Ready", 
    "natural_language_chat": "Ready"
}

# Platform statistics displayed on home page
PLATFORM_STATS = {
    "file_formats": "10+",
    "languages": "25+", 
    "ai_tools": "3",
    "custom_extractions": "∞"
}

# =============================================================================
# 📝 PRESET EXAMPLES - OPTIONAL
# =============================================================================

# Example text and schemas for the AI Extract text input tab
# Customize these with examples relevant to your document types
PRESET_EXAMPLES = {
    "custom": {
        "text": "Enter your custom text here...",
        "schema": {
            "field1": "What information do you want to extract?",
            "field2": "Add more fields as needed..."
        }
    },
    "your_example_1": {
        "name": "Your Document Type 1",
        "text": "Example text from your document type 1...",
        "schema": {
            "field1": "Example question 1?",
            "field2": "Example question 2?"
        }
    },
    "your_example_2": {
        "name": "Your Document Type 2", 
        "text": "Example text from your document type 2...",
        "schema": {
            "field1": "Different question 1?",
            "field2": "Different question 2?"
        }
    }
}

# =============================================================================
# ⚙️ SYSTEM SETTINGS - OPTIONAL
# =============================================================================

# Enable/disable certain features
ENABLE_DATABASE_SAVE = True
ENABLE_FILE_PREVIEW = True
ENABLE_PROGRESS_TRACKING = True

# Error handling
DEBUG_MODE = False  # Set to True for development, False for production

# =============================================================================
# ✅ CONFIGURATION COMPLETE
# =============================================================================
# 
# After updating this file:
# 1. Save as "config.py" 
# 2. Test by running: streamlit run streamlit_app.py
# 3. Verify all models are accessible
# 4. Test document upload and processing
# 5. Deploy to production
#
# =============================================================================