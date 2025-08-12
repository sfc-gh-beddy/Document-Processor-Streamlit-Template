# 📄 Document AI Platform - Customer Package

Welcome! This package contains a complete Document AI platform that works with your existing Snowflake environment and trained models.

## 🎯 What You Get

A ready-to-deploy Streamlit application with:

- **📊 Document Processor** - Process documents with your trained AI models
- **🔍 AI Extract** - Extract information using Snowflake's AI_EXTRACT function  
- **💬 Natural Language Chat** - Query your data using natural language

## 📋 Prerequisites

✅ **You already have:**
- Snowflake account with Cortex AI enabled
- Trained Document AI models
- Snowflake stages with documents
- Database and schema set up

## 🚀 Quick Start (5 minutes)

### 1. Setup Files
```bash
# Rename template files
mv streamlit_app_template.py streamlit_app.py
mv pages/DocumentProcessor_template.py pages/DocumentProcessor.py  
mv pages/AI_EXTRACT_template.py pages/AI_EXTRACT.py
mv pages/NaturalLanguageChatBot_template.py pages/NaturalLanguageChatBot.py

# Copy configuration template
cp CONFIG_TEMPLATE.py config.py
```

### 2. Configure Your Environment
Edit `config.py` and update these required fields:

```python
# Your Snowflake environment
DATABASE_NAME = "YOUR_DATABASE_NAME"
SCHEMA_NAME = "YOUR_SCHEMA_NAME"  
STAGE_NAME = "YOUR_DATABASE.YOUR_SCHEMA.YOUR_STAGE"

# Your trained models
AVAILABLE_MODELS = {
    "Your Model 1": "YOUR_DATABASE.YOUR_SCHEMA.YOUR_MODEL_1!PREDICT",
    "Your Model 2": "YOUR_DATABASE.YOUR_SCHEMA.YOUR_MODEL_2!PREDICT",
    # Add all your models...
}
DEFAULT_MODEL = "Your Model 1"

# Your data tables
PREDICTION_RESULTS_TABLE = "YOUR_DATABASE.YOUR_SCHEMA.YOUR_RESULTS_TABLE"
FLATTENED_DATA_TABLE = "YOUR_DATABASE.YOUR_SCHEMA.YOUR_FLATTENED_TABLE"
AI_EXTRACT_TABLE = "YOUR_DATABASE.YOUR_SCHEMA.YOUR_EXTRACT_TABLE"
```

### 3. Test Your Setup
```bash
streamlit run streamlit_app.py
```

Visit `http://localhost:8501` and test:
1. ✅ Document Processor with your models
2. ✅ AI Extract with your document types
3. ✅ Natural Language Chat (if semantic model configured)

### 4. Deploy to Production
Once tested locally, deploy to your Snowflake environment or cloud platform.

## 📁 File Structure

```
your-project/
├── config.py                    # Your configuration (created from template)
├── streamlit_app.py             # Home page
├── pages/
│   ├── DocumentProcessor.py     # Document processing with your models
│   ├── AI_EXTRACT.py           # AI extraction tool
│   └── NaturalLanguageChatBot.py # Data analysis chat
├── CONFIG_TEMPLATE.py           # Configuration template (reference)
├── QUICK_SETUP_GUIDE.md        # Detailed setup instructions  
└── README_FOR_CUSTOMERS.md     # This file
```

## 🔧 Customization Options

### Add Your Branding
```python
APP_TITLE = "Your Company Document AI"
DOMAIN_NAME = "Your Domain" 
DOCUMENT_TYPE = "your document types"
```

### Customize AI Extract Questions
```python
DEFAULT_EXTRACTION_SCHEMA = {
    "vendor": "What is the vendor name?",
    "amount": "What is the total amount?",
    "date": "What is the document date?",
    # Add questions for your document types
}
```

### Add Preset Examples
```python
PRESET_EXAMPLES = {
    "invoice_example": {
        "name": "Invoice Processing",
        "text": "Your invoice example text...",
        "schema": {"vendor": "What vendor?", "amount": "What amount?"}
    }
}
```

## 📊 Features Overview

### Document Processor
- **Multi-Model Support**: Select from your trained models
- **Model Validation**: Test model accessibility
- **Progress Tracking**: Real-time processing status
- **Results Display**: View extracted data and raw JSON
- **Model Tracking**: Track which model processed each document

### AI Extract  
- **Dual Interface**: Upload files OR paste text
- **Custom Schemas**: Define your own extraction questions
- **Multiple Formats**: PDF, Word, images, text files
- **Export Options**: JSON, CSV formats for easy integration
- **Database Storage**: Save results for analysis

### Natural Language Chat
- **Data Analysis**: Ask questions about your processed data
- **Auto Visualizations**: Charts and graphs generated automatically
- **SQL Generation**: See the SQL queries behind your questions
- **Conversation History**: Track your analysis sessions

## 🛠️ Advanced Configuration

### Semantic Model for Chat (Optional)
Create a YAML file describing your data structure:

```yaml
name: your_model
tables:
  - name: YOUR_DATA_TABLE
    base_table:
      database: YOUR_DATABASE
      schema: YOUR_SCHEMA
      table: YOUR_TABLE
    dimensions:
      - name: CATEGORY_FIELD
        expr: CATEGORY_FIELD
        data_type: VARCHAR
        description: "Description of this field"
    facts:
      - name: NUMERIC_FIELD
        expr: NUMERIC_FIELD  
        data_type: NUMBER
        description: "Description of this metric"
```

Upload to Snowflake and update config:
```python
SEMANTIC_MODEL_FILE = "@YOUR_DATABASE.YOUR_SCHEMA.YOUR_STAGE/your_model.yaml"
```

## 🆘 Support

### Common Issues

**"Model not found" error:**
- Check model names in `AVAILABLE_MODELS` match your actual models
- Verify database/schema permissions

**"Stage not accessible" error:**
- Verify `STAGE_NAME` is correct
- Check stage permissions

**Tables not created:**
- Verify database/schema permissions
- Check if tables exist with different structure

### Configuration Help
- See `QUICK_SETUP_GUIDE.md` for detailed instructions
- Check `CONFIG_TEMPLATE.py` for all available options
- Test locally before deploying to production

## ✅ Success Checklist

- [ ] `config.py` created and updated with your settings
- [ ] All models listed in `AVAILABLE_MODELS`
- [ ] Stage and table names verified
- [ ] Local testing completed successfully
- [ ] Document processing tested with your models
- [ ] AI extraction tested with your document types
- [ ] Branding customized (optional)
- [ ] Ready for production deployment

## 🎉 You're All Set!

Your Document AI platform is now configured for your environment. You can:

- Process documents with your trained models
- Extract custom information using AI
- Analyze your data with natural language queries
- Scale to handle your document processing workflows

**Questions?** Refer to the detailed guides included in this package or test locally to troubleshoot any issues.