import streamlit as st
import pandas as pd
import uuid
import pypdfium2 as pdfium
from snowflake.snowpark.context import get_active_session

# =============================================================================
# CONFIGURATION
# =============================================================================

DATABASE_NAME = "ORBIT"
SCHEMA_NAME = "DOC_AI"
STAGE_NAME = f"{DATABASE_NAME}.{SCHEMA_NAME}.DOC_AI_STAGE"

AVAILABLE_MODELS = {
    "CDC Pertussis Table Extraction": f"{DATABASE_NAME}.{SCHEMA_NAME}.PERTUSSIS_CDC!PREDICT",
}

DEFAULT_MODEL = "CDC Pertussis Table Extraction"
PREDICTION_RESULTS_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.CDC_PERTUSSIS_PREDICTION_RESULTS"
FLATTENED_DATA_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.CDC_PERTUSSIS_FLATTENED_DATA"
AI_EXTRACT_TABLE = f"{DATABASE_NAME}.{SCHEMA_NAME}.CDC_PERTUSSIS_AI_EXTRACTIONS"

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Document Processor",
    page_icon="📊", 
    layout="wide"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
    .upload-section {
        border: 2px dashed #1f4e79;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    
    .model-info {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1976d2;
        margin: 1rem 0;
    }
    
    .processing-status {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    .success-status {
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

st.title("📊 Document Processor")
st.markdown("Upload CDC pertussis surveillance documents for AI-powered data extraction")

# =============================================================================
# SIDEBAR - MODEL SELECTION & INSTRUCTIONS
# =============================================================================

st.sidebar.title("Model Selection")
selected_model = st.sidebar.selectbox(
    "Choose Document AI Model:",
    options=list(AVAILABLE_MODELS.keys()),
    index=list(AVAILABLE_MODELS.keys()).index(DEFAULT_MODEL),
    help="Select the AI model that best matches your document type"
)

current_model = AVAILABLE_MODELS[selected_model]

st.sidebar.markdown(f"""
<div class="model-info">
    <h4>🤖 Selected Model</h4>
    <p><strong>{selected_model}</strong></p>
    <p><em>Optimized for CDC pertussis surveillance documents</em></p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 📋 Instructions")
st.sidebar.markdown("""
1. **Select Model** - Choose the AI model above
2. **Upload Document** - PDF, DOC, DOCX, or images
3. **Preview** - Review document content  
4. **Process** - Run AI extraction
5. **Review Results** - Edit and save data
""")

st.sidebar.markdown("## 📄 Supported Formats")
st.sidebar.markdown("""
- **PDF** documents
- **Word** (.doc, .docx) 
- **Images** (.png, .jpg, .jpeg)
- **Text** (.txt)
- **PowerPoint** (.pptx)
""")

# =============================================================================
# SNOWFLAKE SESSION
# =============================================================================

session = get_active_session()
if not session:
    st.error("❌ Cannot connect to Snowflake. Please check your connection.")
    st.stop()

# =============================================================================
# TABLE CREATION
# =============================================================================

@st.cache_resource
def create_tables():
    """Create necessary tables if they don't exist"""
    try:
        # Prediction Results Table
        create_prediction_table = f"""
        CREATE TABLE IF NOT EXISTS {PREDICTION_RESULTS_TABLE} (
            FILE_NAME VARCHAR,
            MODEL_USED VARCHAR,
            JSON VARIANT,
            CREATED_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
        """
        
        # AI Extract Table
        create_extract_table = f"""
        CREATE TABLE IF NOT EXISTS {AI_EXTRACT_TABLE} (
            EXTRACTION_ID VARCHAR,
            SOURCE_TYPE VARCHAR,
            FILE_NAME VARCHAR,
            EXTRACTED_DATA VARIANT,
            CREATED_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
        """
        
        # Flattened Data Table
        create_flattened_table = f"""
        CREATE TABLE IF NOT EXISTS {FLATTENED_DATA_TABLE} (
            FILE_NAME VARCHAR,
            REPORTING_AREA VARCHAR,
            PERTUSSIS_CURRENT_WEEK INTEGER,
            PERTUSSIS_PREVIOUS_52_WEEKS_MAX INTEGER,
            PERTUSSIS_PREVIOUS_52_WEEKS_TOTAL INTEGER,
            PERTUSSIS_CUMULATIVE_YTD_CURRENT_YEAR INTEGER,
            PERTUSSIS_CUMULATIVE_YTD_PREVIOUS_YEAR INTEGER,
            MODEL_USED VARCHAR,
            EXTRACTION_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
        """
        
        session.sql(create_prediction_table).collect()
        session.sql(create_extract_table).collect()
        session.sql(create_flattened_table).collect()
        return True
    except Exception as e:
        st.error(f"Failed to create tables: {str(e)}")
        return False

# Create tables on app startup
if create_tables():
    st.success("✅ Database tables ready")

# =============================================================================
# FILE UPLOAD SECTION
# =============================================================================

st.markdown("## 📁 Upload Document")

uploaded_file = st.file_uploader(
    "Choose a CDC pertussis surveillance document",
    type=['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'txt', 'pptx'],
    help="Upload documents for AI processing and data extraction"
)

if uploaded_file is not None:
    # File details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("File Name", uploaded_file.name)
    with col2:
        st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
    with col3:
        st.metric("File Type", uploaded_file.type)
    
    # =============================================================================
    # PDF PREVIEW
    # =============================================================================
    
    if uploaded_file.type == "application/pdf":
        st.markdown("## 👁️ Document Preview")
        
        # Display PDF preview
        try:
            pdf_document = pdfium.PdfDocument(uploaded_file.getvalue())
            
            # Show first page preview
            if len(pdf_document) > 0:
                page = pdf_document[0]
                pil_image = page.render(scale=2).to_pil()
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.image(pil_image, caption=f"Page 1 of {len(pdf_document)}", use_column_width=True)
                with col2:
                    st.info(f"📄 **{len(pdf_document)}** pages total")
            
        except Exception as e:
            st.warning(f"Could not preview PDF: {str(e)}")
    
    # =============================================================================
    # PROCESSING SECTION
    # =============================================================================
    
    st.markdown("## 🚀 Process Document")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div class="processing-status">
            <h4>📋 Processing Details</h4>
            <p><strong>Model:</strong> {selected_model}</p>
            <p><strong>Document:</strong> {uploaded_file.name}</p>
            <p><strong>Stage:</strong> {STAGE_NAME}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        process_button = st.button("🚀 Process Document", type="primary", use_container_width=True)
    
    # =============================================================================
    # DOCUMENT PROCESSING
    # =============================================================================
    
    if process_button:
        with st.spinner("Processing document with AI model..."):
            try:
                # Generate unique filename
                file_extension = uploaded_file.name.split('.')[-1]
                unique_filename = f"{uuid.uuid4()}.{file_extension}"
                
                # Upload file to stage
                session.file.put_stream(
                    uploaded_file,
                    f"@{STAGE_NAME}/{unique_filename}",
                    auto_compress=False,
                    overwrite=True
                )
                
                # Run prediction and insert directly into permanent table
                insert_sql = f"""
                    INSERT INTO {PREDICTION_RESULTS_TABLE} (FILE_NAME, MODEL_USED, JSON, CREATED_TIMESTAMP)
                    SELECT '{uploaded_file.name}' as FILE_NAME,
                           '{selected_model}' as MODEL_USED,
                           {current_model}(
                               GET_PRESIGNED_URL(@{STAGE_NAME}, '{unique_filename}')
                           ) as JSON,
                           CURRENT_TIMESTAMP() as CREATED_TIMESTAMP
                """
                
                session.sql(insert_sql).collect()
                
                # Get the results we just inserted
                results_df = session.sql(f"""
                    SELECT JSON FROM {PREDICTION_RESULTS_TABLE} 
                    WHERE FILE_NAME = '{uploaded_file.name}' 
                    AND MODEL_USED = '{selected_model}'
                    ORDER BY CREATED_TIMESTAMP DESC 
                    LIMIT 1
                """).to_pandas()
                
                # Store results in session state to persist across reruns
                if not results_df.empty:
                    st.session_state.processing_results = {
                        'json_data': results_df.iloc[0]['JSON'],
                        'file_name': uploaded_file.name,
                        'model_used': selected_model,
                        'processed_at': pd.Timestamp.now().strftime('%H:%M:%S')
                    }
                
                if not results_df.empty:
                    st.markdown("""
                    <div class="success-status">
                        <h4>✅ Processing Complete!</h4>
                        <p>Document has been successfully processed and results saved.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # =============================================================================
                    # RESULTS DISPLAY & EDITING
                    # =============================================================================
                    
                    st.markdown("## 📊 Extraction Results")
                    
                    # Parse JSON results
                    json_data = results_df.iloc[0]['JSON']
                    
                    if json_data:
                        # Convert to DataFrame for editing
                        try:
                            if isinstance(json_data, dict):
                                # Flatten the JSON for editing
                                flattened_data = {}
                                for key, value in json_data.items():
                                    if isinstance(value, (dict, list)):
                                        flattened_data[key] = str(value)
                                    else:
                                        flattened_data[key] = value
                                
                                edit_df = pd.DataFrame([flattened_data])
                            elif isinstance(json_data, list):
                                # Handle list data
                                edit_df = pd.DataFrame(json_data)
                            else:
                                edit_df = pd.DataFrame([{"Raw_Output": str(json_data)}])
                            
                            # Editable dataframe
                            st.markdown("### ✏️ Review and Edit Extracted Data")
                            edited_df = st.data_editor(
                                edit_df,
                                use_container_width=True,
                                hide_index=True,
                                num_rows="fixed"
                            )
                        except Exception as e:
                            st.error(f"Error creating DataFrame: {str(e)}")
                            st.write("Raw JSON data:")
                            st.json(json_data)
                            # Create a fallback simple DataFrame
                            edited_df = pd.DataFrame([{'data': str(json_data)}])
                        
                        # =============================================================================
                        # SAVE TO FLATTENED TABLE
                        # =============================================================================
                        
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            dest_table = st.text_input(
                                "Table Name (optional):",
                                value=FLATTENED_DATA_TABLE,
                                help="Specify custom table name or use default"
                            )
                        
                        with col2:
                            save_button = st.button("💾 Save Results", type="secondary")
                        
                        with col3:
                            copy_button = st.button("📋 Copy JSON", type="secondary")
                        
                        if save_button:
                            try:
                                # First ensure the destination table exists
                                create_dest_table_sql = f"""
                                CREATE TABLE IF NOT EXISTS {dest_table} (
                                    FILE_NAME VARCHAR,
                                    REPORTING_AREA VARCHAR,
                                    PERTUSSIS_CURRENT_WEEK INTEGER,
                                    PERTUSSIS_PREVIOUS_52_WEEKS_MAX INTEGER,
                                    PERTUSSIS_PREVIOUS_52_WEEKS_TOTAL INTEGER,
                                    PERTUSSIS_CUMULATIVE_YTD_CURRENT_YEAR INTEGER,
                                    PERTUSSIS_CUMULATIVE_YTD_PREVIOUS_YEAR INTEGER,
                                    MODEL_USED VARCHAR,
                                    EXTRACTION_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
                                )
                                """
                                session.sql(create_dest_table_sql).collect()
                                
                                # Prepare data for insertion with file name
                                columns = list(edited_df.columns)
                                
                                # Pad with empty values if needed (assuming 5 field structure)
                                while len(columns) < 5:
                                    columns.append(f"Field_{len(columns)+1}")
                                
                                row_values = [f"'{uploaded_file.name}'"]  # Start with filename
                                for col in columns[:5]:  # Take first 5 columns
                                    if col in edited_df.columns:
                                        value = edited_df.iloc[0][col]
                                        escaped_value = str(value).replace("'", "''") if value is not None else None
                                        row_values.append(f"'{escaped_value}'" if escaped_value is not None else "NULL")
                                    else:
                                        row_values.append("NULL")
                                
                                # Add model used (don't include timestamp as it has DEFAULT)
                                row_values.append(f"'{selected_model}'")
                                
                                insert_flattened_sql = f"""
                                    INSERT INTO {dest_table} (
                                        FILE_NAME, REPORTING_AREA, PERTUSSIS_CURRENT_WEEK, 
                                        PERTUSSIS_PREVIOUS_52_WEEKS_MAX, PERTUSSIS_PREVIOUS_52_WEEKS_TOTAL,
                                        PERTUSSIS_CUMULATIVE_YTD_CURRENT_YEAR, PERTUSSIS_CUMULATIVE_YTD_PREVIOUS_YEAR,
                                        MODEL_USED
                                    ) VALUES ({', '.join(row_values)})
                                """
                                
                                session.sql(insert_flattened_sql).collect()
                                
                                # Store success message in session state
                                st.session_state.save_success = f"✅ Results saved to {dest_table} at {pd.Timestamp.now().strftime('%H:%M:%S')}"
                                st.rerun()  # Rerun to show success message
                                
                            except Exception as e:
                                st.session_state.save_error = f"❌ Error saving results: {str(e)}"
                                st.rerun()
                        
                        # Display success/error messages from session state
                        if hasattr(st.session_state, 'save_success'):
                            st.success(st.session_state.save_success)
                            # Clear the message after displaying
                            del st.session_state.save_success
                        
                        if hasattr(st.session_state, 'save_error'):
                            st.error(st.session_state.save_error)
                            # Clear the message after displaying
                            del st.session_state.save_error
                        
                        if copy_button:
                            # Display JSON for copying
                            st.code(str(json_data), language='json')
                        
                        # =============================================================================
                        # RAW JSON DISPLAY
                        # =============================================================================
                        
                        with st.expander("🔍 View Raw JSON Output"):
                            st.json(json_data)
                    
                    else:
                        st.warning("⚠️ No data extracted from document. Please try a different model or check document quality.")
                
                # Cleanup temporary files
                try:
                    session.sql(f"REMOVE '@{STAGE_NAME}/{unique_filename}'").collect()
                except:
                    pass  # Ignore cleanup errors
                
            except Exception as e:
                st.error(f"❌ Error processing document: {str(e)}")

# =============================================================================
# DISPLAY RESULTS FROM SESSION STATE (PERSISTS ACROSS RERUNS)
# =============================================================================

if hasattr(st.session_state, 'processing_results') and st.session_state.processing_results:
    results = st.session_state.processing_results
    
    st.markdown(f"""
    <div class="success-status">
        <h4>✅ Last Processing Complete! (at {results['processed_at']})</h4>
        <p>File: <strong>{results['file_name']}</strong> | Model: <strong>{results['model_used']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 📊 Current Results")
    
    json_data = results['json_data']
    
    if json_data:
        # Convert to DataFrame for editing
        try:
            if isinstance(json_data, dict):
                if 'data' in json_data:
                    df_data = json_data['data']
                else:
                    df_data = json_data
                
                # If it's a single dict, wrap it in a list
                if isinstance(df_data, dict):
                    df_for_editor = pd.DataFrame([df_data])
                else:
                    df_for_editor = pd.DataFrame(df_data)
            elif isinstance(json_data, list):
                df_for_editor = pd.DataFrame(json_data)
            else:
                # If it's not dict or list, create a simple DataFrame
                df_for_editor = pd.DataFrame([{'data': str(json_data)}])
            
            # Create editable dataframe
            edited_df = st.data_editor(
                df_for_editor,
                use_container_width=True,
                num_rows="dynamic"
            )
        except Exception as e:
            st.error(f"Error creating DataFrame: {str(e)}")
            st.write("Raw JSON data:")
            st.json(json_data)
            # Create a fallback simple DataFrame
            edited_df = pd.DataFrame([{'data': str(json_data)}])
        
        # =============================================================================
        # SAVE TO FLATTENED TABLE
        # =============================================================================
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            dest_table = st.text_input(
                "Table Name (optional):",
                value=FLATTENED_DATA_TABLE,
                help="Specify custom table name or use default",
                key="persistent_table_name"
            )
        
        with col2:
            save_button = st.button("💾 Save Results", type="secondary", key="persistent_save")
        
        with col3:
            copy_button = st.button("📋 Copy JSON", type="secondary", key="persistent_copy")
            clear_button = st.button("🗑️ Clear Results", type="secondary", key="clear_results")
        
        if clear_button:
            del st.session_state.processing_results
            st.rerun()
        
        if save_button:
            try:
                # First ensure the destination table exists
                create_dest_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {dest_table} (
                    FILE_NAME VARCHAR,
                    REPORTING_AREA VARCHAR,
                    PERTUSSIS_CURRENT_WEEK INTEGER,
                    PERTUSSIS_PREVIOUS_52_WEEKS_MAX INTEGER,
                    PERTUSSIS_PREVIOUS_52_WEEKS_TOTAL INTEGER,
                    PERTUSSIS_CUMULATIVE_YTD_CURRENT_YEAR INTEGER,
                    PERTUSSIS_CUMULATIVE_YTD_PREVIOUS_YEAR INTEGER,
                    MODEL_USED VARCHAR,
                    EXTRACTION_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
                )
                """
                session.sql(create_dest_table_sql).collect()
                
                # Prepare data for insertion with file name
                columns = list(edited_df.columns)
                
                # Pad with empty values if needed (assuming 5 field structure)
                while len(columns) < 5:
                    columns.append(f"Field_{len(columns)+1}")
                
                row_values = [f"'{results['file_name']}'"]  # Start with filename
                for col in columns[:5]:  # Take first 5 columns
                    if col in edited_df.columns:
                        value = edited_df.iloc[0][col]
                        escaped_value = str(value).replace("'", "''") if value is not None else None
                        row_values.append(f"'{escaped_value}'" if escaped_value is not None else "NULL")
                    else:
                        row_values.append("NULL")
                
                # Add model used (don't include timestamp as it has DEFAULT)
                row_values.append(f"'{results['model_used']}'")
                
                insert_flattened_sql = f"""
                    INSERT INTO {dest_table} (
                        FILE_NAME, REPORTING_AREA, PERTUSSIS_CURRENT_WEEK, 
                        PERTUSSIS_PREVIOUS_52_WEEKS_MAX, PERTUSSIS_PREVIOUS_52_WEEKS_TOTAL,
                        PERTUSSIS_CUMULATIVE_YTD_CURRENT_YEAR, PERTUSSIS_CUMULATIVE_YTD_PREVIOUS_YEAR,
                        MODEL_USED
                    ) VALUES ({', '.join(row_values)})
                """
                
                session.sql(insert_flattened_sql).collect()
                st.success(f"✅ Results saved to {dest_table} at {pd.Timestamp.now().strftime('%H:%M:%S')}")
                
            except Exception as e:
                st.error(f"❌ Error saving results: {str(e)}")
        
        if copy_button:
            # Display JSON for copying
            st.code(str(json_data), language='json')
        
        # =============================================================================
        # RAW JSON DISPLAY
        # =============================================================================
        
        with st.expander("🔍 View Raw JSON Output"):
            st.json(json_data)

# =============================================================================
# RECENT RESULTS TABLE
# =============================================================================

if st.checkbox("📈 Show Recent Processing Results"):
    try:
        recent_results = session.sql(f"""
            SELECT FILE_NAME, MODEL_USED, CREATED_TIMESTAMP
            FROM {PREDICTION_RESULTS_TABLE}
            ORDER BY CREATED_TIMESTAMP DESC
            LIMIT 10
        """).to_pandas()
        
        if not recent_results.empty:
            st.markdown("### 📋 Recent Processed Documents")
            st.dataframe(recent_results, use_container_width=True)
        else:
            st.info("No recent results found.")
            
    except Exception as e:
        st.warning(f"Could not load recent results: {str(e)}")

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
**💡 Tips:**
- Use high-quality scans for better extraction results
- Select the model that best matches your document type  
- Review and edit extracted data before saving
- Check recent results to track processing history
""")