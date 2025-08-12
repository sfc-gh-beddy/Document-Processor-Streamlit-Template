# 🚀 Quick Setup Guide for Customers

**For customers who already have:**
- ✅ Snowflake stages with documents
- ✅ Trained Document AI models
- ✅ Basic Snowflake environment set up

## ⏰ 5-Minute Setup Process

### Step 1: Copy Template Files (1 minute)
```bash
# Copy all template files to your project directory
# Rename template files to remove "_template" suffix:
mv streamlit_app_template.py streamlit_app.py
mv pages/DocumentProcessor_template.py pages/DocumentProcessor.py
mv pages/AI_EXTRACT_template.py pages/AI_EXTRACT.py
mv pages/NaturalLanguageChatBot_template.py pages/NaturalLanguageChatBot.py
```

### Step 2: Update Configuration (3 minutes)

**Edit `config.py` - Replace these key values:**

```python
# =============================================================================
# 🏢 YOUR SNOWFLAKE ENVIRONMENT
# =============================================================================
DATABASE_NAME = "YOUR_DATABASE_NAME"        # Replace with your database
SCHEMA_NAME = "YOUR_SCHEMA_NAME"             # Replace with your schema
STAGE_NAME = "YOUR_DATABASE.YOUR_SCHEMA.YOUR_STAGE"  # Replace with your stage

# =============================================================================
# 🤖 YOUR TRAINED MODELS
# =============================================================================
AVAILABLE_MODELS = {
    "Your Model 1": "YOUR_DATABASE.YOUR_SCHEMA.YOUR_MODEL_1!PREDICT",
    "Your Model 2": "YOUR_DATABASE.YOUR_SCHEMA.YOUR_MODEL_2!PREDICT",
    "Your Model 3": "YOUR_DATABASE.YOUR_SCHEMA.YOUR_MODEL_3!PREDICT",
    # Add all your trained models here
}
DEFAULT_MODEL = "Your Model 1"  # Set your default model

# =============================================================================
# 📊 YOUR DATA TABLES
# =============================================================================
PREDICTION_RESULTS_TABLE = "YOUR_DATABASE.YOUR_SCHEMA.YOUR_RESULTS_TABLE"
FLATTENED_DATA_TABLE = "YOUR_DATABASE.YOUR_SCHEMA.YOUR_FLATTENED_TABLE"
AI_EXTRACT_TABLE = "YOUR_DATABASE.YOUR_SCHEMA.YOUR_EXTRACT_TABLE"

# =============================================================================
# 🎨 YOUR BRANDING (Optional)
# =============================================================================
APP_TITLE = "Your Document AI Platform"
DOMAIN_NAME = "Your Domain"
DOCUMENT_TYPE = "your document types"
PRIMARY_USE_CASE = "your use case"
```

### Step 3: Test Your Setup (1 minute)

```bash
# Run locally to test
streamlit run streamlit_app.py

# Test each tool:
# 1. Document Processor - Select your model, upload a document
# 2. AI Extract - Try text extraction with your documents
# 3. Natural Language Chat - Ask questions about your data
```

## 🔧 Configuration Details

### Your Document AI Models
**List all your trained models in `AVAILABLE_MODELS`:**
```python
AVAILABLE_MODELS = {
    "Invoice Model": "YOURDB.YOURSCHEMA.INVOICE_MODEL!PREDICT",
    "Contract Model": "YOURDB.YOURSCHEMA.CONTRACT_MODEL!PREDICT", 
    "Report Model": "YOURDB.YOURSCHEMA.REPORT_MODEL!PREDICT",
    # Add as many as you have...
}
```

### Your Data Structure
**If your flattened data has specific fields, update the table creation in:**
- `pages/DocumentProcessor.py` - Lines 136-148 (create_destination_table function)
- Update field names to match your data structure

### Your AI Extract Questions
**Customize extraction questions in `config.py`:**
```python
DEFAULT_EXTRACTION_SCHEMA = {
    "field1": "Your question 1?",
    "field2": "Your question 2?",
    "field3": "Your question 3?",
    # Customize for your document types
}
```

## 🎯 Ready-to-Go Features

### Document Processor
- ✅ Model selection dropdown
- ✅ PDF preview
- ✅ Progress tracking
- ✅ Results display
- ✅ Model usage tracking

### AI Extract
- ✅ File upload processing
- ✅ Text input with custom schemas
- ✅ Copy/paste results
- ✅ Database saving
- ✅ Multiple preset examples

### Natural Language Chat
- ✅ Data analysis queries
- ✅ Automatic visualizations
- ✅ SQL generation
- ✅ Conversation history

## 🚨 Important Notes

### Required Tables
The app will auto-create these tables if they don't exist:
- Prediction results table
- AI extract results table
- Flattened data table

### Semantic Model (Optional)
For Natural Language Chat, create a semantic model YAML file:
```yaml
name: your_model
tables:
  - name: YOUR_TABLE
    base_table:
      database: YOUR_DATABASE
      schema: YOUR_SCHEMA
      table: YOUR_TABLE
    # Add dimensions and facts for your data
```

Upload to your stage:
```sql
PUT file://your_model.yaml @YOUR_STAGE;
```

Update in config.py:
```python
SEMANTIC_MODEL_FILE = "@YOUR_DATABASE.YOUR_SCHEMA.YOUR_STAGE/your_model.yaml"
```

## ✅ Deployment Checklist

- [ ] Template files renamed
- [ ] `config.py` updated with your database/schema/stage
- [ ] `AVAILABLE_MODELS` contains your trained models
- [ ] `DEFAULT_MODEL` set to your preferred model
- [ ] App tested locally
- [ ] Document Processor tested with your documents
- [ ] AI Extract tested with your document types
- [ ] Natural Language Chat tested (if semantic model created)
- [ ] Ready for production deployment

## 🆘 Quick Troubleshooting

**Model Not Found:**
- Verify model names in `AVAILABLE_MODELS` match your actual models
- Check database/schema permissions

**Stage Access Error:**
- Verify `STAGE_NAME` is correct
- Check stage permissions

**Table Creation Error:**
- Verify database/schema permissions
- Check if tables already exist with different structure

**No Results from AI Extract:**
- Test with simple text first
- Verify your extraction schema is valid JSON
- Check file upload permissions

## 🎉 You're Ready!

Once configuration is complete, your Document AI platform is ready to process your documents with your trained models!

**What you get:**
- Multi-model document processing
- Flexible AI extraction
- Natural language data analysis
- Professional UI matching your branding
- Database integration for all results