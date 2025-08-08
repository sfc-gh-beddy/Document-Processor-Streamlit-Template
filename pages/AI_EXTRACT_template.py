import streamlit as st
import snowflake.connector
import pandas as pd
import json
import io
import time
from snowflake.snowpark.context import get_active_session
from config import *

# -------------------------
# Page Config & Custom CSS
# -------------------------
st.set_page_config(
    page_title=f"{DOMAIN_NAME} Document Extraction",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
.header {
    background-color: #f0f4f8;
    padding: 20px;
    border-bottom: 2px solid #d0dae0;
    text-align: center;
}
.footer {
    background-color: #f0f4f8;
    padding: 10px;
    text-align: center;
    font-size: 0.8em;
    color: #555;
}
.extraction-results {
    background-color: #e8f5e8;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #c3e6cb;
    margin: 15px 0;
}
.copy-section {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #dee2e6;
    margin: 10px 0;
}
.instructions {
    background-color: #e7f3ff;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #007acc;
    margin: 15px 0;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.markdown(
    '<div class="header">'
    f'<h1>🔍 {DOMAIN_NAME} Document Extraction</h1>'
    f'<p>Upload {DOCUMENT_TYPE} and extract key {PRIMARY_USE_CASE}</p>'
    '</div>',
    unsafe_allow_html=True
)

# -------------------------
# Sidebar Information
# -------------------------
st.sidebar.title("Instructions")
st.sidebar.markdown(f"""
### How to Use:
1. **Upload Document**: Select a {DOCUMENT_TYPE}
2. **Automatic Extraction**: Key fields are extracted automatically
3. **Copy Results**: Copy the structured data for use elsewhere
4. **Save to Database**: Results are automatically stored for analysis

### Supported Formats:
{', '.join(SUPPORTED_FILE_TYPES)}

### What Gets Extracted:
- Your key field 1
- Your key field 2  
- Your key field 3
- Your key field 4
- Your key field 5
""")

# -------------------------
# Snowflake Session Setup
# -------------------------
try:
    session = get_active_session()
    st.sidebar.success("✅ Connected to Snowflake")
except Exception as e:
    st.sidebar.error(f"❌ Snowflake connection error: {e}")
    st.error("Please ensure you're connected to Snowflake to use this demo.")
    st.stop()

# -------------------------
# Main Extraction Interface with Tabs
# -------------------------
st.markdown(f"""
<div class="instructions">
<h3>📋 Upload a {DOMAIN_NAME} Document</h3>
<p>Upload {DOCUMENT_TYPE}, case studies, or other {PRIMARY_USE_CASE} documents. 
The system will automatically extract key data fields.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📄 Upload Document", "📝 Enter Text Manually"])

with tab1:
    st.markdown(f"### Upload a {DOMAIN_NAME} Document")
    st.markdown(f"Upload any {DOCUMENT_TYPE} and extract key data automatically.")
    
    uploaded_file = st.file_uploader(
        f"Select a {DOCUMENT_TYPE}:",
        type=SUPPORTED_FILE_TYPES,
        help=f"Supported formats: {', '.join(SUPPORTED_FILE_TYPES)}",
        key="file_upload_tab1"
    )

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### 📄 Document Information")
            st.write(f"**Filename:** {uploaded_file.name}")
            st.write(f"**File size:** {uploaded_file.size:,} bytes")
            st.write(f"**File type:** {uploaded_file.type}")
            
            # Show preview for text files
            if uploaded_file.type == "text/plain":
                content = str(uploaded_file.read(), "utf-8")
                st.markdown("**Preview:**")
                st.text_area("Document content", value=content[:500] + "..." if len(content) > 500 else content, height=150, disabled=True)
        
        with col2:
            st.markdown("#### 🔍 Extraction Process")
            
            if st.button(f"🔍 Extract {DOMAIN_NAME} Data", key="extract_main", type="primary"):
                try:
                    with st.spinner(f"Processing document and extracting {PRIMARY_USE_CASE}..."):
                        # Convert DEFAULT_EXTRACTION_SCHEMA to JSON string
                        extraction_schema_json = json.dumps(DEFAULT_EXTRACTION_SCHEMA)
                        
                        # Upload file to Snowflake stage
                        stage_name = STAGE_NAME
                        file_name = f"extracted_{int(time.time())}_{uploaded_file.name}"
                        
                        # Reset file pointer and upload
                        uploaded_file.seek(0)
                        session.file.put_stream(
                            input_stream=io.BytesIO(uploaded_file.read()),
                            stage_location=f"@{stage_name}/{file_name}",
                            overwrite=True,
                            auto_compress=False
                        )
                        
                        # Extract using AI_EXTRACT
                        query = f"""
                        SELECT AI_EXTRACT(
                            file => TO_FILE('@{stage_name}', '{file_name}'),
                            responseFormat => PARSE_JSON('{extraction_schema_json.replace("'", "''")}')
                        ) as extracted_data
                        """
                        
                        result = session.sql(query).collect()
                        
                        if result:
                            extracted_data = result[0]['EXTRACTED_DATA']
                            
                            # Display results
                            st.markdown("### ✅ Extraction Complete!")
                            
                            st.markdown("""
                            <div class="extraction-results">
                            <h4>📊 Extracted Data</h4>
                            """, unsafe_allow_html=True)
                            
                            # Show as formatted table
                            if isinstance(extracted_data, dict):
                                df = pd.DataFrame([
                                    {"Field": k.replace("_", " ").title(), "Extracted Value": v}
                                    for k, v in extracted_data.items()
                                ])
                                st.dataframe(df, use_container_width=True, hide_index=True)
                                
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                                st.markdown("""
                                <div class="copy-section">
                                <h4>📋 Copy Results</h4>
                                <p>Copy the extracted data below for use in reports, spreadsheets, or other systems:</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # JSON format for copying
                                json_str = json.dumps(extracted_data, indent=2)
                                st.code(json_str, language="json")
                                
                                # CSV format for copying
                                st.markdown("**CSV Format:**")
                                csv_str = df.to_csv(index=False)
                                st.code(csv_str, language="text")
                                
                                # Save to database option
                                if st.button("💾 Save to Database", key="save_to_db_tab1"):
                                    try:
                                        # Create table if it doesn't exist
                                        create_table_sql = f"""
                                        CREATE TABLE IF NOT EXISTS {AI_EXTRACT_TABLE} (
                                            extraction_id VARCHAR PRIMARY KEY,
                                            file_name VARCHAR,
                                            extraction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                                            field_1 VARCHAR,
                                            field_2 VARCHAR,
                                            field_3 VARCHAR,
                                            field_4 VARCHAR,
                                            field_5 VARCHAR,
                                            field_6 VARCHAR,
                                            field_7 VARCHAR,
                                            field_8 VARCHAR,
                                            field_9 VARCHAR,
                                            field_10 VARCHAR,
                                            raw_json VARIANT
                                        )
                                        """
                                        session.sql(create_table_sql).collect()
                                        
                                        # Insert the extracted data
                                        extraction_id = f"extract_{int(time.time())}"
                                        
                                        def escape_sql(val):
                                            if val is None:
                                                return 'NULL'
                                            return f"'{str(val).replace(chr(39), chr(39)+chr(39))}'"
                                        
                                        # CUSTOMIZE: Update field names to match your DEFAULT_EXTRACTION_SCHEMA
                                        field_keys = list(DEFAULT_EXTRACTION_SCHEMA.keys())
                                        field_values = [escape_sql(extracted_data.get(key)) for key in field_keys]
                                        
                                        insert_sql = f"""
                                        INSERT INTO {AI_EXTRACT_TABLE}
                                        (extraction_id, file_name, field_1, field_2, field_3, field_4, field_5,
                                         field_6, field_7, field_8, field_9, field_10, raw_json)
                                        VALUES (
                                            '{extraction_id}',
                                            '{uploaded_file.name}',
                                            {field_values[0] if len(field_values) > 0 else 'NULL'},
                                            {field_values[1] if len(field_values) > 1 else 'NULL'},
                                            {field_values[2] if len(field_values) > 2 else 'NULL'},
                                            {field_values[3] if len(field_values) > 3 else 'NULL'},
                                            {field_values[4] if len(field_values) > 4 else 'NULL'},
                                            {field_values[5] if len(field_values) > 5 else 'NULL'},
                                            {field_values[6] if len(field_values) > 6 else 'NULL'},
                                            {field_values[7] if len(field_values) > 7 else 'NULL'},
                                            {field_values[8] if len(field_values) > 8 else 'NULL'},
                                            {field_values[9] if len(field_values) > 9 else 'NULL'},
                                            PARSE_JSON('{json_str.replace(chr(39), chr(39)+chr(39))}')
                                        )
                                        """
                                        
                                        session.sql(insert_sql).collect()
                                        st.success(f"✅ Data saved to database with ID: {extraction_id}")
                                        
                                    except Exception as e:
                                        st.error(f"Error saving to database: {str(e)}")
                            
                            else:
                                st.json(extracted_data)
                                 
                        else:
                            st.warning("No results returned from AI_EXTRACT")
                            
                except Exception as e:
                    st.error(f"Error during extraction: {str(e)}")
                    
    else:
        # Show example when no file is uploaded
        st.markdown("### 📝 Example: What Gets Extracted")
        
        # Create example data from your configuration
        example_data = {f"Field {i+1}": f"Example value {i+1}" for i in range(len(DEFAULT_EXTRACTION_SCHEMA))}
        
        df_example = pd.DataFrame(list(example_data.items()), columns=['Field', 'Example Value'])
        st.dataframe(df_example, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("### Enter Text and Custom Questions")
    st.markdown("Enter raw text and define your own JSON structure for extracting specific information.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Input Text")
        
        # Preset examples from configuration
        preset_options = ["Custom Text"] + [preset["name"] for preset in PRESET_EXAMPLES.values() if "name" in preset]
        preset_option = st.selectbox(
            "Choose a preset example or enter custom text:",
            options=preset_options,
            key="preset_selector_tab2"
        )
        
        # Get the selected preset data
        if preset_option == "Custom Text":
            default_text = PRESET_EXAMPLES["custom"]["text"]
            default_schema = json.dumps(PRESET_EXAMPLES["custom"]["schema"], indent=2)
        else:
            # Find the matching preset
            selected_preset = None
            for preset in PRESET_EXAMPLES.values():
                if preset.get("name") == preset_option:
                    selected_preset = preset
                    break
            
            if selected_preset:
                default_text = selected_preset["text"]
                default_schema = json.dumps(selected_preset["schema"], indent=2)
            else:
                default_text = "Enter your text here..."
                default_schema = json.dumps({"field1": "What information do you want to extract?"}, indent=2)
        
        input_text = st.text_area(
            "Enter text to analyze:",
            value=default_text,
            height=200,
            key="input_text_tab2"
        )
    
    with col2:
        st.markdown("#### 🔧 Extraction Schema")
        st.markdown("Define your questions in JSON format:")
        
        extraction_schema = st.text_area(
            "JSON Schema (questions to ask):",
            value=default_schema,
            height=200,
            key="extraction_schema_tab2"
        )
        
        if st.button("🔍 Extract Information", key="extract_text_tab2", type="primary"):
            try:
                with st.spinner("Extracting information from text..."):
                    # Validate JSON schema
                    try:
                        json.loads(extraction_schema)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON format in extraction schema. Please check your syntax.")
                        st.stop()
                    
                    # Escape single quotes for SQL
                    escaped_text = input_text.replace("'", "''")
                    escaped_schema = extraction_schema.replace("'", "''")
                    
                    # Run AI_EXTRACT query
                    query = f"""
                    SELECT AI_EXTRACT(
                        text => '{escaped_text}',
                        responseFormat => PARSE_JSON('{escaped_schema}')
                    ) as extracted_data
                    """
                    
                    result = session.sql(query).collect()
                    
                    if result:
                        extracted_data = result[0]['EXTRACTED_DATA']
                        
                        st.markdown("### ✅ Extraction Complete!")
                        
                        st.markdown("""
                        <div class="extraction-results">
                        <h4>📊 Extracted Information</h4>
                        """, unsafe_allow_html=True)
                        
                        # Show as formatted table
                        if isinstance(extracted_data, dict):
                            df = pd.DataFrame([
                                {"Field": k.replace("_", " ").title(), "Extracted Value": v}
                                for k, v in extracted_data.items()
                            ])
                            st.dataframe(df, use_container_width=True, hide_index=True)
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.markdown("""
                            <div class="copy-section">
                            <h4>📋 Copy Results</h4>
                            <p>Copy the extracted data below:</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # JSON format for copying
                            json_str = json.dumps(extracted_data, indent=2)
                            st.code(json_str, language="json")
                            
                            # CSV format for copying
                            st.markdown("**CSV Format:**")
                            csv_str = df.to_csv(index=False)
                            st.code(csv_str, language="text")
                        
                        else:
                            st.json(extracted_data)
                    
                    else:
                        st.warning("No results returned from AI_EXTRACT")
                        
            except Exception as e:
                st.error(f"Error during extraction: {str(e)}")
                st.code(f"Query attempted:\n{query}")
    
    # Help section for text tab
    st.markdown("---")
    st.markdown("### 💡 Tips for Custom Extraction")
    
    tip_col1, tip_col2 = st.columns(2)
    
    with tip_col1:
        st.markdown("""
        **JSON Schema Tips:**
        - Use clear, specific questions
        - Add "List:" prefix to extract multiple items
        - Questions can be descriptive or interrogative
        """)
    
    with tip_col2:
        st.markdown("""
        **Example Question Types:**
        - `"name": "What is the person's name?"`
        - `"locations": "List: What locations are mentioned?"`
        - `"summary": "Provide a brief summary"`
        """)

# -------------------------
# Footer
# -------------------------
st.markdown(
    f'<div class="footer">Powered by {APP_TITLE} | {DOMAIN_NAME} Document Processing</div>',
    unsafe_allow_html=True
)