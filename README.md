# 🦠 CDC Pertussis Document AI Platform

A Streamlit application for processing CDC pertussis surveillance documents using Snowflake's AI capabilities.

## 🚀 Quick Start

### Prerequisites
- Snowflake account with Cortex AI enabled
- Documents stored in `ORBIT.DOC_AI.DOC_AI_STAGE`
- Trained Document AI models available

### Setup in Snowflake

1. **Create Streamlit App:**
```sql
CREATE STREAMLIT "ORBIT"."DOC_AI"."PERTUSSIS_DOC_AI"
  ROOT_LOCATION = '@ORBIT.DOC_AI.DOC_AI_STAGE/streamlit_app'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = 'YOUR_WAREHOUSE';
```

2. **Copy Files to Snowflake:**
   - Copy all files from this repo into your Snowflake Streamlit app
   - Files will be automatically uploaded to the stage location

3. **Update Configuration:**
   - Edit `config.py` to match your specific model names and settings
   - All database/schema/stage settings are pre-configured for ORBIT.DOC_AI

4. **Run the App:**
   - Click "Run App" in Snowflake UI
   - Test all three tools with your data

## 📁 File Structure

```
streamlit_app.py              # Main home page
config.py                     # Configuration (pre-set for ORBIT.DOC_AI)
pages/
  ├── DocumentProcessor.py    # Upload & process documents with AI models
  ├── AI_EXTRACT.py          # Extract specific pertussis data fields  
  └── NaturalLanguageChatBot.py # Chat interface for data analysis
```

## 🛠️ Available Tools

### 1. 📊 Document Processor
- **Purpose:** Upload and process CDC pertussis surveillance documents
- **Features:**
  - Select from multiple trained AI models
  - PDF preview and processing
  - Automatic data extraction and structuring
  - Results stored in organized tables
  - Edit extracted data before saving

### 2. 🔍 AI Extract  
- **Purpose:** Extract specific epidemiological data fields
- **Features:**
  - Two input methods: file upload or text input
  - Pre-configured with 10 key pertussis surveillance questions
  - Custom JSON schema support for text input
  - Structured output for analysis
  - Save results to database or copy data

### 3. 💬 Natural Language Chat
- **Purpose:** Query processed data using natural language
- **Features:**
  - Ask questions about surveillance data in plain English
  - Automatic SQL generation using Cortex Analyst
  - Interactive charts and visualizations
  - Export chat history and results

## ⚙️ Configuration Details

### Pre-configured Settings (config.py)
```python
DATABASE_NAME = "ORBIT"
SCHEMA_NAME = "DOC_AI" 
STAGE_NAME = "ORBIT.DOC_AI.DOC_AI_STAGE"
```

### Tables Created Automatically
- `ORBIT.DOC_AI.PREDICTION_RESULTS` - Document processing results
- `ORBIT.DOC_AI.FLATTENED_DATA` - Structured extracted data
- `ORBIT.DOC_AI.INFECTIOUS_DISEASE_EXTRACTIONS` - AI Extract results

### AI Extract Schema (10 Key Fields)
1. Disease/Pathogen identification
2. Reporting area/jurisdiction
3. Reporting period (dates/timeframes)
4. Case counts and statistics
5. Population data and demographics
6. Incidence rates and attack rates
7. Trend analysis and comparisons
8. Outbreak status determination
9. Data source identification
10. Public health actions and recommendations

## 🔧 Customization

### Pre-configured Model
The app is configured with your trained CDC pertussis model:
```python
AVAILABLE_MODELS = {
    "CDC Pertussis Table Extraction": "ORBIT.DOC_AI.PERTUSSIS_CDC!PREDICT",
}
```

This model is specifically trained for extracting tables from CDC pertussis surveillance documents.

### Custom Branding
Update `APP_TITLE` and related settings in `config.py`:
```python
APP_TITLE = "Your Organization Document AI Platform"
APP_SUBTITLE = "Your custom description"
```

### Semantic Model for Chat
- Upload your semantic model YAML file to the stage
- Update `SEMANTIC_MODEL_FILE` in config.py
- The chat interface will use this for natural language queries

## 🎯 Usage Examples

### Document Processor
1. Select appropriate AI model from dropdown
2. Upload CDC pertussis surveillance document (PDF, DOC, etc.)
3. Preview document content
4. Click "Process Document" 
5. Review and edit extracted data
6. Save results to database tables

### AI Extract
1. **File Upload Tab:**
   - Upload pertussis surveillance document
   - AI extracts 10 key surveillance fields
   - Edit results and save to database

2. **Text Input Tab:**
   - Paste surveillance report text
   - Choose default schema or create custom JSON schema
   - Extract structured data from text

### Natural Language Chat
1. Ask questions like:
   - "How many pertussis cases were reported last month?"
   - "What are the trends by geographic area?"
   - "Show me outbreak status distribution"
2. View auto-generated SQL queries
3. Explore results with interactive charts

## 🔍 Troubleshooting

### Model Access Issues
```sql
-- Check if your models exist
DESCRIBE FUNCTION ORBIT.DOC_AI.YOUR_MODEL_NAME;
```

### Stage Access Issues  
```sql
-- Verify stage and list files
LIST @ORBIT.DOC_AI.DOC_AI_STAGE;
```

### Permission Issues
```sql
-- Check Cortex permissions
SHOW GRANTS OF DATABASE ROLE SNOWFLAKE.CORTEX_USER;
```

## 📊 Data Flow

1. **Documents** → Upload to `DOC_AI_STAGE`
2. **AI Models** → Process documents and extract data
3. **Database Tables** → Store structured results
4. **Chat Interface** → Query and analyze processed data
5. **Visualizations** → Interactive charts and exports

## 🎉 Ready to Go!

Your CDC Pertussis Document AI Platform is configured and ready to process surveillance documents. Upload your documents and start extracting valuable epidemiological insights!

---

**💡 Need Help?** 
- Check the sidebar instructions in each tool
- Review the configuration in `config.py`
- Test with sample documents first
- Use the Natural Language Chat to explore your processed data