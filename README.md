# 🔬 Document AI Platform Template

This is a customizable template for building AI-powered document processing platforms using Snowflake. It provides three core tools for document upload, AI extraction, and natural language data analysis.

## 🚀 Quick Start

### 1. Prerequisites
- Snowflake account with Cortex AI enabled
- Python environment with Streamlit
- Document AI model trained (or use Snowflake's pre-built models)

### 2. Setup Instructions

#### Step 1: Clone and Customize Configuration
1. Copy all template files to your project directory
2. Rename `streamlit_app_template.py` to `streamlit_app.py`
3. Rename page template files (remove `_template` suffix)
4. Edit `config.py` with your Snowflake configurations

#### Step 2: Configure Your Database
Update these key settings in `config.py`:

```python
# Your Snowflake database and schema
DATABASE_NAME = "YOUR_DATABASE_NAME"
SCHEMA_NAME = "YOUR_SCHEMA_NAME"
STAGE_NAME = "YOUR_DATABASE.YOUR_SCHEMA.YOUR_STAGE"

# Your trained document AI model
DOCUMENT_AI_MODEL = "YOUR_DATABASE.YOUR_SCHEMA.YOUR_MODEL!PREDICT"

# Your semantic model for Cortex Analyst
SEMANTIC_MODEL_FILE = "@YOUR_DATABASE.YOUR_SCHEMA.YOUR_STAGE/your_model.yaml"
```

#### Step 3: Customize for Your Domain
Replace these placeholders throughout `config.py`:

```python
# Application branding
APP_TITLE = "Your Document AI Platform"
DOMAIN_NAME = "Your Domain"  # e.g., "Financial Document Processing"
DOCUMENT_TYPE = "your document type"  # e.g., "financial reports"
PRIMARY_USE_CASE = "your use case"  # e.g., "financial data analysis"
```

#### Step 4: Define Your Extraction Schema
Update the `DEFAULT_EXTRACTION_SCHEMA` in `config.py` with questions relevant to your documents:

```python
DEFAULT_EXTRACTION_SCHEMA = {
    "field_1": "What is the document type?",
    "field_2": "What is the reporting period?",
    "field_3": "What are the key metrics?",
    # Add up to 10 fields specific to your use case
}
```

### 3. Required Snowflake Setup

#### Create Database and Schema
```sql
CREATE DATABASE YOUR_DATABASE_NAME;
USE DATABASE YOUR_DATABASE_NAME;
CREATE SCHEMA YOUR_SCHEMA_NAME;
USE SCHEMA YOUR_SCHEMA_NAME;
```

#### Create Stage for File Uploads
```sql
CREATE STAGE YOUR_STAGE_NAME;
```

#### Create Required Tables
The application will auto-create these tables, but you can create them manually:

```sql
-- For Document Processor results
CREATE TABLE YOUR_PREDICTION_TABLE (
    FILE_NAME VARCHAR,
    JSON VARIANT,
    CREATED_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- For AI Extract results  
CREATE TABLE YOUR_AI_EXTRACT_TABLE (
    extraction_id VARCHAR PRIMARY KEY,
    file_name VARCHAR,
    extraction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    field_1 VARCHAR,
    field_2 VARCHAR,
    -- Add fields matching your extraction schema
    raw_json VARIANT
);
```

### 4. Customize Document Processing Logic

#### Document Processor (`pages/DocumentProcessor_template.py`)
- Update the `DOCUMENT_AI_MODEL` configuration
- Modify `create_flattened_table_if_not_exists()` function for your data structure
- Customize the extraction query in `run_pipeline()` function

#### AI Extract (`pages/AI_EXTRACT_template.py`)
- Update `DEFAULT_EXTRACTION_SCHEMA` for your domain
- Modify preset examples in `PRESET_EXAMPLES`
- Customize the database save logic

#### Natural Language Chat (`pages/NaturalLanguageChatBot_template.py`)
- Create a semantic model YAML file for your data
- Update `SEMANTIC_MODEL_FILE` path in config
- Customize example questions in the sidebar

### 5. Create Your Semantic Model

Create a YAML file describing your data for Cortex Analyst:

```yaml
name: your_domain_model
tables:
  - name: YOUR_FLATTENED_TABLE
    base_table:
      database: YOUR_DATABASE
      schema: YOUR_SCHEMA  
      table: YOUR_FLATTENED_TABLE
    dimensions:
      - name: FIELD_1
        expr: FIELD_1
        data_type: VARCHAR
        description: Description of field 1
    facts:
      - name: FIELD_2
        expr: FIELD_2
        data_type: NUMBER
        description: Description of field 2
```

Upload this to your Snowflake stage:
```sql
PUT file://your_model.yaml @YOUR_STAGE_NAME;
```

## 🛠️ Customization Guide

### Adding New File Types
Update `SUPPORTED_FILE_TYPES` in `config.py`:
```python
SUPPORTED_FILE_TYPES = ['pdf', 'png', 'jpg', 'docx', 'your_new_type']
```

### Adding New Extraction Fields
1. Update `DEFAULT_EXTRACTION_SCHEMA` in `config.py`
2. Modify the database table creation SQL in AI_EXTRACT_template.py
3. Update the insert SQL to include new fields

### Customizing UI Branding
- Update `APP_TITLE`, `DOMAIN_NAME`, and related variables in `config.py`
- Modify CSS colors and styling in the template files
- Replace emojis and icons throughout the templates

### Adding New Preset Examples
Update `PRESET_EXAMPLES` in `config.py`:
```python
PRESET_EXAMPLES = {
    "your_new_example": {
        "name": "Your Example Name",
        "text": "Example text content...",
        "schema": {
            "field1": "Question 1?",
            "field2": "Question 2?"
        }
    }
}
```

## 📁 File Structure

```
your-project/
├── config.py                              # Main configuration file
├── streamlit_app.py                       # Home page (rename from template)
├── pages/
│   ├── DocumentProcessor.py              # Document processing tool
│   ├── AI_EXTRACT.py                     # AI extraction tool  
│   └── NaturalLanguageChatBot.py         # Data analysis chat
├── your_semantic_model.yaml              # Cortex Analyst model
└── README.md                             # This file
```

## 🔧 Environment Setup

### Requirements
Create `requirements.txt`:
```
streamlit
snowflake-snowpark-python
pandas
pypdfium2
```

### Environment File
Create `environment.yml`:
```yaml
name: your_app_environment
channels:
  - snowflake
dependencies:
  - pypdfium2=4.19.0
  - python=3.11.*
  - snowflake-snowpark-python
  - streamlit
```

## 🚀 Deployment

### Local Development
```bash
streamlit run streamlit_app.py
```

### Snowflake Deployment
1. Upload all files to your Snowflake stage
2. Create Streamlit app in Snowflake
3. Configure environment and dependencies

## 📊 Example Use Cases

### Financial Document Processing
- Process financial reports, invoices, statements
- Extract revenue, expenses, dates, account numbers
- Analyze financial trends and patterns

### Healthcare Document Analysis  
- Process patient records, lab reports, clinical notes
- Extract patient info, diagnoses, medications, dates
- Analyze treatment patterns and outcomes

### Legal Document Review
- Process contracts, legal briefs, court documents
- Extract parties, dates, clauses, obligations
- Analyze contract terms and legal patterns

### Research Paper Analysis
- Process academic papers, research reports
- Extract authors, methodologies, findings, citations
- Analyze research trends and insights

## 🆘 Troubleshooting

### Common Issues

**Configuration Errors:**
- Verify all placeholders in `config.py` are updated
- Check database/schema/stage names match your Snowflake setup
- Ensure your Document AI model exists and is accessible

**Permission Errors:**
- Verify Snowflake user has required permissions
- Check Cortex AI access is enabled
- Ensure stage and table permissions are correct

**Processing Errors:**
- Verify file upload stage exists and is accessible
- Check document AI model is properly deployed
- Ensure semantic model YAML is valid and uploaded

### Support
- Review Snowflake Cortex documentation
- Check Streamlit documentation for UI issues
- Validate SQL queries in Snowflake worksheet

## 📝 License

This template is provided as-is for customization. Modify according to your needs and organizational requirements.