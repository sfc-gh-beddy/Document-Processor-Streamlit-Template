# 🦠 CDC Pertussis Document AI Platform

A streamlined Streamlit application for processing CDC pertussis surveillance documents using Snowflake's AI capabilities.

## 🚀 Quick Start (2 minutes)

### 1. Create Streamlit App in Snowflake
```sql
CREATE STREAMLIT "ORBIT"."DOC_AI"."CDC_PERTUSSIS_APP"
  ROOT_LOCATION = '@ORBIT.DOC_AI.DOC_AI_STAGE/streamlit_app'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = 'YOUR_WAREHOUSE';
```

### 2. Copy Files to Snowflake
Simply drag and drop these files into your Snowflake Streamlit app:

1. **`streamlit_app.py`** → Main application file
2. **`pages/DocumentProcessor.py`** → Document processing page  
3. **`pages/AI_EXTRACT.py`** → AI extraction page
4. **`pages/NaturalLanguageChatBot.py`** → Chat interface page

### 3. Run and Test
Click "Run App" in Snowflake - that's it! The app is pre-configured for your ORBIT.DOC_AI environment.

## 📁 Files Included

```
streamlit_app.py                 # Main home page with tool overview
pages/
  ├── DocumentProcessor.py       # Upload & process documents with trained AI models
  ├── AI_EXTRACT.py             # Extract specific pertussis surveillance fields  
  └── NaturalLanguageChatBot.py  # Natural language chat interface
environment.yml                  # Conda dependencies
```

## 🛠️ What Each Tool Does

### 📊 Document Processor
- **Upload CDC pertussis documents** (PDF, DOC, images)
- **Process with trained model:** `ORBIT.DOC_AI.PERTUSSIS_CDC!PREDICT`
- **Extract tables and structured data**
- **Save results to:** `ORBIT.DOC_AI.CDC_PERTUSSIS_PREDICTION_RESULTS`

### 🔍 AI Extract  
- **Two modes:** Upload documents OR paste text directly
- **Extracts 10 key surveillance fields:**
  1. Disease being reported
  2. Reporting area/jurisdiction
  3. Time period covered
  4. Case counts
  5. Population affected
  6. Symptoms described
  7. Transmission method
  8. Prevention measures
  9. Public health response
  10. Data source
- **Save results to:** `ORBIT.DOC_AI.CDC_PERTUSSIS_AI_EXTRACTIONS`

### 💬 Natural Language Chat
- **Query processed data** using natural language
- **Powered by Snowflake Cortex Analyst**
- **Automatic SQL generation** and execution
- **Interactive visualizations** and insights

## 🔧 Pre-configured Settings

All Snowflake resources are pre-configured:

- **Database:** `ORBIT`
- **Schema:** `DOC_AI` 
- **Stage:** `ORBIT.DOC_AI.DOC_AI_STAGE` (your documents)
- **Model:** `ORBIT.DOC_AI.PERTUSSIS_CDC!PREDICT`
- **Tables:** Automatically created on first run

## 📋 Requirements

- Snowflake account with Cortex AI enabled
- CDC pertussis documents in `ORBIT.DOC_AI.DOC_AI_STAGE`
- Trained `PERTUSSIS_CDC` model deployed
- Streamlit-enabled warehouse

## 🎯 Workflow

1. **Upload documents** → Document Processor extracts structured data
2. **Extract key fields** → AI Extract pulls surveillance information  
3. **Analyze results** → Natural Language Chat for insights

Perfect for CDC surveillance teams processing pertussis outbreak data! 🦠📊