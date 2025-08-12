# 🚀 Customer Deployment Guide

This guide helps you quickly deploy and customize the Document AI Platform for your specific use case.

## 📋 Pre-Deployment Checklist

### ✅ Snowflake Requirements
- [ ] Snowflake account with Cortex AI enabled
- [ ] Database and schema created
- [ ] File upload stage configured  
- [ ] Document AI model trained or available
- [ ] User permissions configured

### ✅ Application Files
- [ ] All template files copied to your environment
- [ ] `config.py` updated with your settings
- [ ] Template files renamed (remove `_template` suffix)
- [ ] Semantic model YAML created for your data

## 🔧 Step-by-Step Setup

### Step 1: Database Setup (5 minutes)

```sql
-- Create your database and schema
CREATE DATABASE YOUR_DATABASE_NAME;
USE DATABASE YOUR_DATABASE_NAME;
CREATE SCHEMA YOUR_SCHEMA_NAME;
USE SCHEMA YOUR_SCHEMA_NAME;

-- Create file upload stage
CREATE STAGE YOUR_STAGE_NAME;

-- Verify stage creation
DESC STAGE YOUR_STAGE_NAME;
```

### Step 2: Configure Application (10 minutes)

Edit `config.py` and replace these key variables:

```python
# 🏢 ORGANIZATION SETTINGS
DATABASE_NAME = "CDC_SURVEILLANCE"         # Your database
SCHEMA_NAME = "PUBLIC"                     # Your schema
STAGE_NAME = "CDC_SURVEILLANCE.PUBLIC.INFECTIOUS_DISEASES"  # Your stage

# 🎯 DOMAIN CUSTOMIZATION  
APP_TITLE = "CDC Document AI Platform"    # Your app name
DOMAIN_NAME = "CDC Infectious Disease Surveillance"  # Your domain
DOCUMENT_TYPE = "CDC surveillance documents"     # Your document types
PRIMARY_USE_CASE = "epidemiological data"  # Your use case

# 🤖 AI MODEL CONFIGURATION - Multiple CDC Models Support
AVAILABLE_MODELS = {
    "CDC Pertussis Surveillance": "CDC_SURVEILLANCE.PUBLIC.GINKGO_TABLE_EXTRACTION_SIMPLE!PREDICT",
    "MMWR Weekly Reports": "CDC_SURVEILLANCE.PUBLIC.MMWR_WEEKLY_MODEL!PREDICT",
    "Outbreak Investigation Reports": "CDC_SURVEILLANCE.PUBLIC.OUTBREAK_INVESTIGATION_MODEL!PREDICT",
    "Surveillance Summaries": "CDC_SURVEILLANCE.PUBLIC.SURVEILLANCE_SUMMARY_MODEL!PREDICT",
    "NNDSS Annual Reports": "CDC_SURVEILLANCE.PUBLIC.NNDSS_ANNUAL_MODEL!PREDICT",
    "State Health Dept Reports": "CDC_SURVEILLANCE.PUBLIC.STATE_HEALTH_MODEL!PREDICT"
}
DEFAULT_MODEL = "CDC Pertussis Surveillance"

# 📊 SEMANTIC MODEL
SEMANTIC_MODEL_FILE = "@CDC_SURVEILLANCE.PUBLIC.INFECTIOUS_DISEASES/epidemiology.yaml"
```

### Step 3: Customize Extraction Schema (5 minutes)

Update the extraction questions for CDC infectious disease documents:

```python
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
```

### Step 4: Create Semantic Model (15 minutes)

Create `epidemiology.yaml`:

```yaml
name: epidemiology
tables:
  - name: PERTUSSIS_DATA_FLATTENED
    base_table:
      database: CDC_SURVEILLANCE
      schema: PUBLIC
      table: PERTUSSIS_DATA_FLATTENED
    dimensions:
      - name: REPORTING_AREA
        expr: REPORTING_AREA
        data_type: VARCHAR
        description: Geographic area where the case was reported
        synonyms: [region, location, area, jurisdiction]
      - name: OUTBREAK_STATUS  
        expr: OUTBREAK_STATUS
        data_type: VARCHAR
        description: Status of outbreak or surveillance
        synonyms: [status, classification, level]
    facts:
      - name: CURRENT_WEEK
        expr: CURRENT_WEEK  
        data_type: NUMBER
        description: Current week case count
        synonyms: [weekly_cases, week_count, current_cases]
      - name: CUM_YTD_2024
        expr: CUM_YTD_2024
        data_type: NUMBER 
        description: Cumulative year-to-date 2024 cases
        synonyms: [ytd_2024, cumulative_2024, total_2024]
      - name: CUM_YTD_2025
        expr: CUM_YTD_2025
        data_type: NUMBER 
        description: Cumulative year-to-date 2025 cases
        synonyms: [ytd_2025, cumulative_2025, total_2025]
```

Upload to Snowflake:
```sql
PUT file://epidemiology.yaml @CDC_SURVEILLANCE.PUBLIC.INFECTIOUS_DISEASES;
```

### Step 5: File Rename and Deploy (2 minutes)

```bash
# Rename template files
mv streamlit_app_template.py streamlit_app.py
mv pages/DocumentProcessor_template.py pages/DocumentProcessor.py
mv pages/AI_EXTRACT_template.py pages/AI_EXTRACT.py  
mv pages/NaturalLanguageChatBot_template.py pages/NaturalLanguageChatBot.py

# Test locally
streamlit run streamlit_app.py
```

## 🎨 Quick Customization Examples

### Financial Services
```python
APP_TITLE = "Financial Document AI"
DOMAIN_NAME = "Financial Processing"
DOCUMENT_TYPE = "invoices, statements, and reports"
PRIMARY_USE_CASE = "financial data extraction"

DEFAULT_EXTRACTION_SCHEMA = {
    "vendor": "What is the vendor name?",
    "amount": "What is the total amount?", 
    "date": "What is the invoice date?",
    "account": "What is the account number?",
    "description": "What services were provided?"
}
```

### Healthcare  
```python
APP_TITLE = "Medical Records AI"
DOMAIN_NAME = "Healthcare Document Processing"
DOCUMENT_TYPE = "medical records and reports"
PRIMARY_USE_CASE = "clinical data extraction"

DEFAULT_EXTRACTION_SCHEMA = {
    "patient_id": "What is the patient ID?",
    "diagnosis": "What is the primary diagnosis?",
    "medications": "List: What medications are prescribed?",
    "provider": "Who is the healthcare provider?",
    "visit_date": "What is the visit date?"
}
```

### Legal Documents
```python
APP_TITLE = "Legal Document AI"  
DOMAIN_NAME = "Legal Document Processing"
DOCUMENT_TYPE = "contracts and legal documents"
PRIMARY_USE_CASE = "legal data extraction"

DEFAULT_EXTRACTION_SCHEMA = {
    "parties": "List: Who are the parties in this contract?",
    "effective_date": "What is the effective date?",
    "term_length": "What is the contract term?",
    "value": "What is the contract value?",
    "obligations": "List: What are the key obligations?"
}
```

## 🔍 Testing Your Deployment

### Test Document Processor
1. **Select appropriate model** from the dropdown in the sidebar
2. **Test model accessibility** using the "Test Model" button
3. Upload a sample PDF document
4. Verify processing pipeline completes
5. Check that data appears in your tables
6. Verify model tracking in results

### Test AI Extract  
1. Try the file upload tab with a sample document
2. Test the text input tab with sample text
3. Verify results are saved to database

### Test Natural Language Chat
1. Ask a simple question about your data
2. Verify SQL generation works
3. Check that visualizations display correctly

## 🛠️ Troubleshooting

### Common Configuration Issues

**Database Connection Errors:**
```python
# Verify these settings in config.py
DATABASE_NAME = "YOUR_ACTUAL_DATABASE"  # Must exist in Snowflake
SCHEMA_NAME = "YOUR_ACTUAL_SCHEMA"      # Must exist in database
```

**Stage Access Errors:**
```sql
-- Check stage exists and has permissions
DESC STAGE YOUR_STAGE_NAME;
SHOW GRANTS ON STAGE YOUR_STAGE_NAME;
```

**Model Not Found Errors:**
```python
# Verify model exists and is accessible
DOCUMENT_AI_MODEL = "DATABASE.SCHEMA.MODEL_NAME!PREDICT"  # Full path required
```

**Semantic Model Errors:**
```sql
-- Verify file uploaded correctly
LIST @YOUR_STAGE_NAME;

-- Check file contents
SELECT $1 FROM @YOUR_STAGE_NAME/your_model.yaml;
```

### Performance Optimization

**Large File Processing:**
- Increase timeout values in processing functions
- Consider file size limits in configuration
- Implement chunking for very large documents

**Database Performance:**
- Add indexes on frequently queried columns
- Consider partitioning large tables by date
- Optimize semantic model for common queries

## 📞 Support Resources

### Documentation Links
- [Snowflake Cortex AI Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [AI_EXTRACT Function Reference](https://docs.snowflake.com/LIMITEDACCESS/document-ai/ai_extract)

### Common Questions

**Q: Can I use this with my existing document AI model?**
A: Yes, update the `DOCUMENT_AI_MODEL` setting in config.py with your model name.

**Q: How do I add new file types?**
A: Update `SUPPORTED_FILE_TYPES` in config.py and ensure AI_EXTRACT supports the format.

**Q: Can I customize the UI colors and styling?**
A: Yes, modify the CSS sections in each template file to match your branding.

**Q: How do I add new extraction fields?**
A: Update `DEFAULT_EXTRACTION_SCHEMA` in config.py and modify the database table schema accordingly.

## ✅ Deployment Checklist

- [ ] Database and schema created
- [ ] Stage configured and accessible
- [ ] Config.py fully customized
- [ ] Template files renamed
- [ ] Semantic model created and uploaded
- [ ] Local testing completed
- [ ] Document Processor tested with sample file
- [ ] AI Extract tested with both tabs
- [ ] Natural Language Chat tested
- [ ] Error handling verified
- [ ] Performance acceptable
- [ ] Ready for production deployment

## 🎉 Go Live!

Once all tests pass, you're ready to deploy to production and start processing your documents with AI!