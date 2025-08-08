import streamlit as st
import snowflake.connector
import pandas as pd
import io
import time
import pypdfium2 as pdfium
from snowflake.snowpark.context import get_active_session
from config import *

# -------------------------
# Page Config & Custom CSS
# -------------------------
st.set_page_config(
    page_title=f"{DOMAIN_NAME} Document Processor",
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
.upload-section, .preview-section, .progress-section, .dataframe-container {
    margin-top: 20px;
    margin-bottom: 20px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.markdown(
    '<div class="header">'
    f'<h1>Document Processor</h1>'
    f'<p>Upload {DOCUMENT_TYPE}, preview them, run predictions, and edit the extracted data before saving.</p>'
    '</div>',
    unsafe_allow_html=True
)

# -------------------------
# Sidebar Instructions
# -------------------------
st.sidebar.title("How to Use")
st.sidebar.markdown(f"""
1. **Upload PDF**: Select a PDF file.
2. **Preview**: The first page of the PDF is shown immediately.
3. **Processing**: A multi-step progress bar indicates the pipeline steps.
4. **Edit & Save**: Edit the extracted table and save it with timestamps—no re-processing occurs on save.

Note: this app is using a pre-built {DOMAIN_NAME} document extraction model. Customize for your document types.
""")

# -------------------------
# Snowflake Session
# -------------------------
session = get_active_session()

# -------------------------
# Configuration from config.py
# -------------------------
stage_name = STAGE_NAME
internal_predict_table = PREDICTION_RESULTS_TABLE
flattened_table = FLATTENED_DATA_TABLE

# Ensure the stage exists
try:
    session.sql(f"DESC STAGE {stage_name}").collect()
except Exception as e:
    st.error(f"Error verifying or creating stage '{stage_name}': {e}")
    st.stop()

# -------------------------
# Session State
# -------------------------
if "predict_results" not in st.session_state:
    st.session_state["predict_results"] = None
if "extracted_df" not in st.session_state:
    st.session_state["extracted_df"] = None
if "current_file_name" not in st.session_state:
    st.session_state["current_file_name"] = None

# -------------------------
# Helper Functions - CUSTOMIZE THESE FOR YOUR DATA STRUCTURE
# -------------------------
def create_destination_table_if_not_exists(dest_table: str):
    """
    Create a new table (if it doesn't exist) with your data structure.
    CUSTOMIZE THIS SQL based on your expected data fields!
    """
    try:
        session.sql(f"DESC TABLE {dest_table}").collect()
        return  # If no exception, table already exists
    except:
        pass  # Table does not exist, so create it

    # CUSTOMIZE: Replace these fields with your actual data structure
    create_sql = f"""
        CREATE TABLE {dest_table} (
            Field_1 VARCHAR,              -- Replace with your field names
            Field_2 VARCHAR,              -- Replace with your field names  
            Field_3 VARCHAR,              -- Replace with your field names
            Field_4 VARCHAR,              -- Replace with your field names
            Field_5 VARCHAR,              -- Replace with your field names
            EXTRACTION_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
    """
    session.sql(create_sql).collect()
    st.info(f"Created new table: {dest_table}")

def create_flattened_table_if_not_exists(flat_table: str):
    """
    Create a flattened table for your processed results.
    CUSTOMIZE THIS SQL based on your document AI model output!
    """
    try:
        session.sql(f"DESC TABLE {flat_table}").collect()
        return
    except:
        pass

    # CUSTOMIZE: Replace this with your actual flattening logic
    flattened_sql = f"""
    CREATE OR REPLACE TABLE {flat_table} AS
    SELECT
        -- CUSTOMIZE: Replace these with your actual field extractions
        -- Example for extracting from JSON results:
        extracted_data.value:"field_1"::STRING AS field_1,
        extracted_data.value:"field_2"::STRING AS field_2,
        extracted_data.value:"field_3"::STRING AS field_3,
        extracted_data.value:"field_4"::STRING AS field_4,
        extracted_data.value:"field_5"::STRING AS field_5,
        CURRENT_TIMESTAMP() as extraction_timestamp
    FROM {internal_predict_table},
    LATERAL FLATTEN(input => JSON:"YourJsonStructure") AS extracted_data
    WHERE FILE_NAME IS NOT NULL
    """
    session.sql(flattened_sql).collect()
    st.info(f"Created flattened table: {flat_table}")

def insert_edited_data(edited_df: pd.DataFrame, dest_table: str):
    """
    Insert edited data into destination table.
    CUSTOMIZE: Update field names to match your data structure!
    """
    for _, row in edited_df.iterrows():
        def esc(val):
            return str(val).replace("'", "''")

        # CUSTOMIZE: Replace these field names with your actual fields
        values = (
            f"'{esc(row['Field_1'])}'",     # Replace with your field names
            f"'{esc(row['Field_2'])}'",     # Replace with your field names
            f"'{esc(row['Field_3'])}'",     # Replace with your field names
            f"'{esc(row['Field_4'])}'",     # Replace with your field names
            f"'{esc(row['Field_5'])}'"      # Replace with your field names
        )

        insert_sql = f"""
            INSERT INTO {dest_table}
            (Field_1, Field_2, Field_3, Field_4, Field_5)  -- CUSTOMIZE: Your field names
            VALUES ({', '.join(values)})
        """
        session.sql(insert_sql).collect()

def run_step(step_name, progress_value, step_func):
    """Runs a single pipeline step with progress tracking."""
    status_text.text(step_name)
    progress_bar.progress(progress_value)

    start_time = time.time()
    step_func()
    elapsed = time.time() - start_time

    if elapsed > 7:
        wait_message = st.info("This step is taking a bit longer than usual. Please hold on...")
        time.sleep(1)
        wait_message.empty()

    time.sleep(1)  # Animation delay

def run_pipeline(file_name: str, file_content: bytes):
    """
    Runs the document processing pipeline.
    CUSTOMIZE: Update the prediction model and extraction logic!
    """
    with st.expander("Stage Upload Details", expanded=False) as stage_expander:
        stage_placeholder = st.empty()
        stage_placeholder.write("Preparing to upload to Snowflake stage...")

    def step_analyze_pdf():
        # CUSTOMIZE: Add your PDF analysis logic here
        pass

    def step_upload_to_stage():
        session.file.put_stream(
            input_stream=io.BytesIO(file_content),
            stage_location=f"@{stage_name}/{file_name}",
            overwrite=True,
            auto_compress=False
        )
        stage_placeholder.write(f"File '{file_name}' uploaded to stage: {stage_name}")

    def step_run_predictions():
        session.sql(f"DELETE FROM {internal_predict_table} WHERE FILE_NAME = '{file_name}'").collect()
        
        # CUSTOMIZE: Replace with your actual document AI model
        predict_sql = f"""
            INSERT INTO {internal_predict_table}
            SELECT '{file_name}' as FILE_NAME, 
                   {DOCUMENT_AI_MODEL} (
                     GET_PRESIGNED_URL(@{stage_name}, '{file_name}')
                   ) as JSON;
        """
        session.sql(predict_sql).collect()

    def step_extract_data():
        # CUSTOMIZE: Add your data extraction and transformation logic
        pass

    # Run pipeline steps
    run_step("Analyzing PDF: text extraction, image capturing, and layout analysis...", 10, step_analyze_pdf)
    run_step("Uploading file to Snowflake stage...", 30, step_upload_to_stage)
    run_step("Running predictions on extracted data...", 60, step_run_predictions)
    run_step("Extracting structured document data...", 80, step_extract_data)

    # Retrieve predictions
    predict_results = session.sql(
        f"SELECT * FROM {internal_predict_table} WHERE FILE_NAME = '{file_name}'"
    ).to_pandas()

    # CUSTOMIZE: Update this extraction query based on your model output structure
    extraction_query = f"""
        WITH extracted AS (
            SELECT FILE_NAME, prediction.value:"value"::STRING AS data_raw
            FROM {internal_predict_table} t,
                 LATERAL FLATTEN(input => t.JSON:"YourResultStructure") prediction  -- CUSTOMIZE
            WHERE FILE_NAME = '{file_name}'
        )
        SELECT 
            FILE_NAME,
            -- CUSTOMIZE: Replace these with your actual field parsing logic
            SPLIT_PART(data_raw, '|', 1) AS Field_1,
            SPLIT_PART(data_raw, '|', 2) AS Field_2,
            SPLIT_PART(data_raw, '|', 3) AS Field_3,
            SPLIT_PART(data_raw, '|', 4) AS Field_4,
            SPLIT_PART(data_raw, '|', 5) AS Field_5
        FROM extracted;
    """

    try:
        extracted_results_df = session.sql(extraction_query).to_pandas()
    except Exception as e:
        st.error(f"Error extracting document data: {e}")
        raise

    # Finalize
    status_text.text("Finalizing...")
    progress_bar.progress(95)
    time.sleep(1)
    status_text.text("Done!")
    progress_bar.progress(100)

    time.sleep(1)
    progress_bar.empty()
    status_text.empty()

    return predict_results, extracted_results_df

# -------------------------
# Main App
# -------------------------
st.subheader(f"Upload a {DOCUMENT_TYPE.upper()}")

uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"], help="Only PDF format is supported.")

# Initialize progress/status placeholders
progress_bar = st.progress(0)
status_text = st.empty()

if uploaded_file is not None:
    uploaded_filename = uploaded_file.name.upper()
    file_content = uploaded_file.read()

    # 1) PDF Preview
    with st.expander("Preview Uploaded PDF", expanded=True):
        try:
            pdf = pdfium.PdfDocument(io.BytesIO(file_content))
            page = pdf[0]
            bitmap = page.render(scale=4, rotation=0)
            pil_image = bitmap.to_pil()
            st.image(pil_image, caption="Uploaded Document Preview", use_column_width=True)
        except Exception as e:
            st.error(f"Error rendering PDF preview: {e}")

    # 2) Run pipeline
    if (st.session_state["current_file_name"] != uploaded_filename):
        with st.spinner("Processing the file..."):
            try:
                predict_results, extracted_df = run_pipeline(uploaded_filename, file_content)
                st.session_state["predict_results"] = predict_results
                st.session_state["extracted_df"] = extracted_df
                st.session_state["current_file_name"] = uploaded_filename
            except:
                st.session_state["predict_results"] = None
                st.session_state["extracted_df"] = None
                st.session_state["current_file_name"] = None
                st.stop()
    else:
        predict_results = st.session_state["predict_results"]
        extracted_df = st.session_state["extracted_df"]

    # 3) Display results
    if predict_results is not None and extracted_df is not None:
        with st.expander("View Prediction Results and Extracted Data", expanded=True):
            st.subheader("Prediction Results and Extracted Document Data")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Raw Prediction JSON")
                if not predict_results.empty:
                    st.json(predict_results.to_dict(orient='records'))
                else:
                    st.warning("No raw prediction data available.")
            with col2:
                st.markdown("### Extracted Document Data")
                # CUSTOMIZE: Update this to query your actual flattened table
                st.dataframe(session.sql(f"SELECT * FROM {flattened_table}").to_pandas())

# Footer
st.markdown(
    f'<div class="footer">Powered by {APP_TITLE} Document AI</div>',
    unsafe_allow_html=True
)