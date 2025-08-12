import streamlit as st
import pandas as pd
import json
import uuid
from config import (
    STAGE_NAME, AI_EXTRACT_TABLE, DEFAULT_EXTRACTION_SCHEMA,
    get_snowflake_session
)

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="AI Extract",
    page_icon="🔍",
    layout="wide"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
    .extraction-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .schema-preview {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1976d2;
        margin: 1rem 0;
    }
    
    .results-section {
        background: #fff3cd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# MAIN INTERFACE
# =============================================================================

st.title("🔍 AI Extract")
st.markdown("Extract structured data from CDC pertussis surveillance documents using AI")

# =============================================================================
# SNOWFLAKE SESSION
# =============================================================================

session = get_snowflake_session()
if not session:
    st.error("❌ Cannot connect to Snowflake. Please check your connection.")
    st.stop()

# =============================================================================
# TABS INTERFACE
# =============================================================================

tab1, tab2 = st.tabs(["📄 Upload Document", "📝 Enter Text Manually"])

# =============================================================================
# TAB 1: DOCUMENT UPLOAD
# =============================================================================

with tab1:
    st.markdown("### 📄 Document Upload for Pertussis Data Extraction")
    
    # Show extraction schema
    st.markdown("""
    <div class="schema-preview">
        <h4>🎯 Pertussis Surveillance Fields</h4>
        <p>The AI will extract the following 10 key fields from your document:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display schema questions
    col1, col2 = st.columns(2)
    schema_items = list(DEFAULT_EXTRACTION_SCHEMA.items())
    
    for i, (field, question) in enumerate(schema_items):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.markdown(f"**{i+1}. {field.replace('_', ' ').title()}**")
            st.markdown(f"*{question}*")
    
    st.markdown("---")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CDC pertussis surveillance document",
        type=['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'txt', 'html', 'pptx'],
        help="Upload documents for AI extraction of pertussis surveillance data"
    )
    
    if uploaded_file is not None:
        # File info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Name", uploaded_file.name)
        with col2:
            st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
        with col3:
            st.metric("File Type", uploaded_file.type)
        
        # Process button
        if st.button("🚀 Extract Pertussis Data", type="primary", use_container_width=True):
            with st.spinner("Extracting pertussis surveillance data..."):
                try:
                    # Upload file to stage
                    file_extension = uploaded_file.name.split('.')[-1]
                    unique_filename = f"extract_{uuid.uuid4()}.{file_extension}"
                    
                    session.file.put_stream(
                        uploaded_file,
                        f"@{STAGE_NAME}/{unique_filename}",
                        auto_compress=False,
                        overwrite=True
                    )
                    
                    # Prepare schema for SQL
                    schema_json = json.dumps(DEFAULT_EXTRACTION_SCHEMA)
                    escaped_schema = schema_json.replace("'", "''")
                    
                    # Run AI_EXTRACT
                    query = f"""
                    SELECT AI_EXTRACT(
                        file => TO_FILE('@{STAGE_NAME}', '{unique_filename}'),
                        responseFormat => PARSE_JSON('{escaped_schema}')
                    ) as extracted_data
                    """
                    
                    result = session.sql(query).collect()
                    
                    if result and result[0]['EXTRACTED_DATA']:
                        extracted_data = result[0]['EXTRACTED_DATA']
                        
                        st.markdown("""
                        <div class="success-message">
                            <h4>✅ Extraction Complete!</h4>
                            <p>Successfully extracted pertussis surveillance data from your document.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # =============================================================================
                        # DISPLAY RESULTS
                        # =============================================================================
                        
                        st.markdown("## 📊 Extracted Data")
                        
                        # Create DataFrame for display
                        results_data = []
                        for field, question in DEFAULT_EXTRACTION_SCHEMA.items():
                            value = extracted_data.get(field, "Not found")
                            results_data.append({
                                "Field": field.replace('_', ' ').title(),
                                "Question": question,
                                "Extracted Value": value
                            })
                        
                        results_df = pd.DataFrame(results_data)
                        
                        # Editable results
                        st.markdown("### ✏️ Review and Edit Extracted Data")
                        edited_df = st.data_editor(
                            results_df,
                            use_container_width=True,
                            hide_index=True,
                            disabled=["Field", "Question"],
                            column_config={
                                "Extracted Value": st.column_config.TextColumn(
                                    "Extracted Value",
                                    help="Edit the extracted values if needed",
                                    width="large"
                                )
                            }
                        )
                        
                        # =============================================================================
                        # SAVE AND COPY OPTIONS
                        # =============================================================================
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("💾 Save to Database", type="secondary"):
                                try:
                                    # Generate unique extraction ID
                                    extraction_id = str(uuid.uuid4())
                                    
                                    # Prepare values for insertion
                                    values = [
                                        extraction_id,
                                        uploaded_file.name,
                                        "CURRENT_TIMESTAMP()"
                                    ]
                                    
                                    # Add extracted field values
                                    for field in DEFAULT_EXTRACTION_SCHEMA.keys():
                                        # Find corresponding value in edited dataframe
                                        field_title = field.replace('_', ' ').title()
                                        row = edited_df[edited_df['Field'] == field_title]
                                        if not row.empty:
                                            value = row.iloc[0]['Extracted Value']
                                            escaped_value = str(value).replace("'", "''") if value else ''
                                            values.append(f"'{escaped_value}'")
                                        else:
                                            values.append("NULL")
                                    
                                    # Add raw JSON
                                    raw_json = json.dumps(extracted_data).replace("'", "''")
                                    values.append(f"PARSE_JSON('{raw_json}')")
                                    
                                    # Insert into database
                                    insert_sql = f"""
                                    INSERT INTO {AI_EXTRACT_TABLE} (
                                        extraction_id, file_name, extraction_timestamp,
                                        disease_pathogen, reporting_area, reporting_period, 
                                        case_counts, population_data, incidence_rates,
                                        trend_analysis, outbreak_status, data_source, 
                                        public_health_actions, raw_json
                                    ) VALUES (
                                        '{values[0]}', '{values[1]}', {values[2]},
                                        {values[3]}, {values[4]}, {values[5]}, {values[6]}, 
                                        {values[7]}, {values[8]}, {values[9]}, {values[10]}, 
                                        {values[11]}, {values[12]}, {values[13]}
                                    )
                                    """
                                    
                                    session.sql(insert_sql).collect()
                                    st.success(f"✅ Results saved to database with ID: {extraction_id}")
                                    
                                except Exception as e:
                                    st.error(f"❌ Error saving results: {str(e)}")
                        
                        with col2:
                            # Copy as JSON
                            if st.button("📋 Copy as JSON", type="secondary"):
                                st.code(json.dumps(extracted_data, indent=2), language='json')
                        
                        with col3:
                            # Copy as CSV
                            if st.button("📊 Copy as CSV", type="secondary"):
                                csv_data = edited_df.to_csv(index=False)
                                st.text_area("CSV Data (copy this):", csv_data, height=100)
                        
                        # Raw JSON view
                        with st.expander("🔍 View Raw JSON"):
                            st.json(extracted_data)
                    
                    else:
                        st.warning("⚠️ No data extracted. Please try a different document or check document quality.")
                    
                    # Cleanup
                    try:
                        session.sql(f"REMOVE '@{STAGE_NAME}/{unique_filename}'").collect()
                    except:
                        pass
                        
                except Exception as e:
                    st.error(f"❌ Error during extraction: {str(e)}")

# =============================================================================
# TAB 2: MANUAL TEXT INPUT
# =============================================================================

with tab2:
    st.markdown("### 📝 Manual Text Input with Custom Schema")
    
    # Text input
    st.markdown("#### 📄 Enter Text to Analyze")
    input_text = st.text_area(
        "Paste your CDC pertussis surveillance text here:",
        height=200,
        placeholder="Enter the text content from your pertussis surveillance document..."
    )
    
    # Schema input
    st.markdown("#### 🎯 Extraction Schema")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        schema_option = st.radio(
            "Choose extraction schema:",
            ["Use Default Pertussis Schema", "Custom JSON Schema"]
        )
    
    with col2:
        if schema_option == "Use Default Pertussis Schema":
            st.info("Using pre-defined 10 pertussis surveillance questions")
            current_schema = DEFAULT_EXTRACTION_SCHEMA
        else:
            st.info("Define your own extraction fields")
    
    if schema_option == "Custom JSON Schema":
        custom_schema_text = st.text_area(
            "Enter your custom JSON schema:",
            value=json.dumps(DEFAULT_EXTRACTION_SCHEMA, indent=2),
            height=300,
            help="Define your extraction fields as JSON key-value pairs"
        )
        
        try:
            current_schema = json.loads(custom_schema_text)
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON format. Please check your schema.")
            current_schema = DEFAULT_EXTRACTION_SCHEMA
    
    # Process text
    if st.button("🚀 Extract Data from Text", type="primary", use_container_width=True):
        if input_text.strip():
            with st.spinner("Extracting data from text..."):
                try:
                    # Escape text and schema for SQL
                    escaped_text = input_text.replace("'", "''")
                    schema_json = json.dumps(current_schema)
                    escaped_schema = schema_json.replace("'", "''")
                    
                    # Run AI_EXTRACT on text
                    query = f"""
                    SELECT AI_EXTRACT(
                        text => '{escaped_text}',
                        responseFormat => PARSE_JSON('{escaped_schema}')
                    ) as extracted_data
                    """
                    
                    result = session.sql(query).collect()
                    
                    if result and result[0]['EXTRACTED_DATA']:
                        extracted_data = result[0]['EXTRACTED_DATA']
                        
                        st.markdown("""
                        <div class="success-message">
                            <h4>✅ Text Analysis Complete!</h4>
                            <p>Successfully extracted structured data from your text.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display results
                        st.markdown("## 📊 Extracted Data")
                        
                        # Create results DataFrame
                        results_data = []
                        for field, question in current_schema.items():
                            value = extracted_data.get(field, "Not found")
                            results_data.append({
                                "Field": field.replace('_', ' ').title(),
                                "Question": question,
                                "Extracted Value": value
                            })
                        
                        results_df = pd.DataFrame(results_data)
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Copy options
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("📋 Copy JSON", type="secondary"):
                                st.code(json.dumps(extracted_data, indent=2), language='json')
                        
                        with col2:
                            if st.button("📊 Copy CSV", type="secondary"):
                                csv_data = results_df.to_csv(index=False)
                                st.text_area("CSV Data:", csv_data, height=100)
                    
                    else:
                        st.warning("⚠️ No data extracted from text. Please try different text or schema.")
                        
                except Exception as e:
                    st.error(f"❌ Error during text extraction: {str(e)}")
        else:
            st.warning("⚠️ Please enter some text to analyze.")

# =============================================================================
# SIDEBAR INSTRUCTIONS
# =============================================================================

st.sidebar.markdown("## 📋 How to Use AI Extract")

st.sidebar.markdown("""
### 📄 Document Upload Tab
1. **Upload** CDC pertussis document
2. **Review** the 10 extraction fields  
3. **Click Extract** to process
4. **Edit** results if needed
5. **Save** to database or copy data

### 📝 Text Input Tab  
1. **Paste** your surveillance text
2. **Choose** default or custom schema
3. **Define** extraction questions (if custom)
4. **Extract** structured data
5. **Copy** results as JSON or CSV
""")

st.sidebar.markdown("## 🎯 Default Schema Fields")
st.sidebar.markdown("""
- Disease/Pathogen
- Reporting Area  
- Reporting Period
- Case Counts
- Population Data
- Incidence Rates
- Trend Analysis
- Outbreak Status
- Data Source
- Public Health Actions
""")

# =============================================================================
# RECENT EXTRACTIONS
# =============================================================================

if st.checkbox("📈 Show Recent Extractions"):
    try:
        recent_extractions = session.sql(f"""
            SELECT extraction_id, file_name, extraction_timestamp, 
                   disease_pathogen, reporting_area
            FROM {AI_EXTRACT_TABLE}
            ORDER BY extraction_timestamp DESC
            LIMIT 10
        """).to_pandas()
        
        if not recent_extractions.empty:
            st.markdown("### 📋 Recent AI Extractions")
            st.dataframe(recent_extractions, use_container_width=True)
        else:
            st.info("No recent extractions found.")
            
    except Exception as e:
        st.warning(f"Could not load recent extractions: {str(e)}")

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
**💡 Tips:**
- Use clear, well-formatted documents for better extraction
- Custom schemas allow targeting specific data fields
- Review and edit extracted data before saving
- Both file and text input support the same extraction capabilities
""")