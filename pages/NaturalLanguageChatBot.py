import streamlit as st
import pandas as pd
import json
import _snowflake
from snowflake.snowpark.context import get_active_session

# =============================================================================
# CONFIGURATION
# =============================================================================

DATABASE_NAME = "ORBIT"
SCHEMA_NAME = "DOC_AI"
STAGE_NAME = f"{DATABASE_NAME}.{SCHEMA_NAME}.DOC_AI_STAGE"
SEMANTIC_MODEL_FILE = f"@{STAGE_NAME}/epidemiology.yaml"

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Natural Language Chat",
    page_icon="💬",
    layout="wide"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
    .chat-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .user-message {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1976d2;
        margin: 0.5rem 0;
    }
    
    .assistant-message {
        background: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #7b1fa2;
        margin: 0.5rem 0;
    }
    
    .sql-code {
        background: #263238;
        color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
    
    .query-examples {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# MAIN INTERFACE
# =============================================================================

st.title("💬 Natural Language Chat")
st.markdown("Ask questions about your CDC pertussis surveillance data using natural language")

# =============================================================================
# SNOWFLAKE SESSION
# =============================================================================

session = get_active_session()
if not session:
    st.error("❌ Cannot connect to Snowflake. Please check your connection.")
    st.stop()

# =============================================================================
# CHAT INTERFACE
# =============================================================================

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.markdown("## 💭 Chat History")

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <strong>🧑 You:</strong> {message['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <strong>🤖 Assistant:</strong> {message['content']}
        </div>
        """, unsafe_allow_html=True)
        
        # Display SQL and results if available
        if 'sql' in message:
            st.markdown("**Generated SQL:**")
            st.code(message['sql'], language='sql')
        
        if 'results' in message:
            st.markdown("**Query Results:**")
            if isinstance(message['results'], pd.DataFrame):
                st.dataframe(message['results'], use_container_width=True)
            else:
                st.write(message['results'])

# =============================================================================
# QUERY INPUT
# =============================================================================

st.markdown("## 🔍 Ask a Question")

# Example queries
st.markdown("""
<div class="query-examples">
    <h4>💡 Example Questions You Can Ask:</h4>
    <ul>
        <li>"How many pertussis cases were reported last month?"</li>
        <li>"What are the trends in pertussis incidence by geographic area?"</li>
        <li>"Show me the outbreak status distribution"</li>
        <li>"Which data sources have the highest case counts?"</li>
        <li>"What public health actions were most commonly recommended?"</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Chat input
user_question = st.chat_input("Ask about your pertussis surveillance data...")

if user_question:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Display user message
    st.markdown(f"""
    <div class="user-message">
        <strong>🧑 You:</strong> {user_question}
    </div>
    """, unsafe_allow_html=True)
    
    # Process with Cortex Analyst
    with st.spinner("🤔 Analyzing your question..."):
        try:
            # Use Cortex Analyst to generate SQL
            analyst_query = f"""
            SELECT SNOWFLAKE.CORTEX.ANALYST(
                '{user_question}',
                STAGE => '@{SEMANTIC_MODEL_FILE.split("@")[1].split("/")[0]}',
                FILE => '{SEMANTIC_MODEL_FILE.split("/")[-1]}'
            ) as response
            """
            
            result = session.sql(analyst_query).collect()
            
            if result and result[0]['RESPONSE']:
                response_data = result[0]['RESPONSE']
                
                # Parse the response
                if isinstance(response_data, str):
                    try:
                        response_json = json.loads(response_data)
                    except:
                        response_json = {"answer": response_data}
                else:
                    response_json = response_data
                
                # Extract answer and SQL
                answer = response_json.get('answer', 'I was able to process your question.')
                sql_query = response_json.get('sql', '')
                
                # Display assistant response
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>🤖 Assistant:</strong> {answer}
                </div>
                """, unsafe_allow_html=True)
                
                # Execute SQL if available
                query_results = None
                if sql_query:
                    st.markdown("**Generated SQL:**")
                    st.code(sql_query, language='sql')
                    
                    try:
                        # Execute the generated SQL
                        if sql_query.strip().upper().startswith('SELECT'):
                            query_results = session.sql(sql_query).to_pandas()
                            
                            if not query_results.empty:
                                st.markdown("**Query Results:**")
                                st.dataframe(query_results, use_container_width=True)
                                
                                # Simple visualization for numeric data
                                numeric_cols = query_results.select_dtypes(include=['int64', 'float64']).columns
                                if len(numeric_cols) > 0 and len(query_results) > 1:
                                    if st.checkbox("📊 Show Chart"):
                                        if len(query_results.columns) >= 2:
                                            chart_type = st.selectbox(
                                                "Chart Type:",
                                                ["line_chart", "bar_chart", "area_chart"]
                                            )
                                            
                                            if chart_type == "line_chart":
                                                st.line_chart(query_results.set_index(query_results.columns[0]))
                                            elif chart_type == "bar_chart":
                                                st.bar_chart(query_results.set_index(query_results.columns[0]))
                                            elif chart_type == "area_chart":
                                                st.area_chart(query_results.set_index(query_results.columns[0]))
                            else:
                                st.info("Query executed successfully but returned no results.")
                    
                    except Exception as e:
                        st.warning(f"⚠️ Could not execute generated SQL: {str(e)}")
                        query_results = f"SQL execution error: {str(e)}"
                
                # Add to chat history
                message_data = {
                    "role": "assistant", 
                    "content": answer
                }
                if sql_query:
                    message_data["sql"] = sql_query
                if query_results is not None:
                    message_data["results"] = query_results
                
                st.session_state.messages.append(message_data)
            
            else:
                error_msg = "I couldn't process your question. Please try rephrasing it or check that your semantic model is properly configured."
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>🤖 Assistant:</strong> {error_msg}
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        except Exception as e:
            error_msg = f"Error processing your question: {str(e)}"
            st.error(f"❌ {error_msg}")
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# =============================================================================
# SIDEBAR CONTROLS
# =============================================================================

st.sidebar.markdown("## 💬 Chat Controls")

if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

if st.sidebar.button("💾 Export Chat"):
    if st.session_state.messages:
        chat_export = []
        for msg in st.session_state.messages:
            export_msg = {
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": "exported"
            }
            if "sql" in msg:
                export_msg["sql"] = msg["sql"]
            chat_export.append(export_msg)
        
        st.sidebar.download_button(
            "📥 Download Chat JSON",
            data=json.dumps(chat_export, indent=2),
            file_name="chat_history.json",
            mime="application/json"
        )

st.sidebar.markdown("## 📊 Semantic Model Info")
st.sidebar.markdown(f"""
**Model File:** `{SEMANTIC_MODEL_FILE}`

This chat interface uses Snowflake Cortex Analyst to:
- Parse natural language questions
- Generate SQL queries automatically  
- Execute queries against your data
- Provide human-readable answers
""")

st.sidebar.markdown("## 💡 Tips")
st.sidebar.markdown("""
- Ask specific questions about your data
- Use terms from your semantic model
- Try different phrasings if needed
- Request charts for numeric results
- Export chat history for records
""")

# =============================================================================
# DATA PREVIEW SECTION
# =============================================================================

if st.checkbox("📋 Preview Available Data"):
    st.markdown("### 📊 Data Tables Overview")
    
    try:
        # Check available tables
        from config import PREDICTION_RESULTS_TABLE, AI_EXTRACT_TABLE, FLATTENED_DATA_TABLE
        
        tables_to_check = [
            ("Prediction Results", PREDICTION_RESULTS_TABLE),
            ("AI Extractions", AI_EXTRACT_TABLE),
            ("Flattened Data", FLATTENED_DATA_TABLE)
        ]
        
        for table_name, table_path in tables_to_check:
            try:
                sample_data = session.sql(f"SELECT * FROM {table_path} LIMIT 5").to_pandas()
                
                if not sample_data.empty:
                    st.markdown(f"#### {table_name}")
                    st.dataframe(sample_data, use_container_width=True)
                    
                    # Row count
                    count_result = session.sql(f"SELECT COUNT(*) as count FROM {table_path}").collect()
                    row_count = count_result[0]['COUNT'] if count_result else 0
                    st.caption(f"Total rows: {row_count}")
                else:
                    st.info(f"{table_name}: No data available")
                    
            except Exception as e:
                st.warning(f"{table_name}: Table not accessible ({str(e)})")
        
    except Exception as e:
        st.error(f"Error checking data tables: {str(e)}")

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
**🔍 Natural Language Chat Features:**
- Ask questions in plain English about your pertussis surveillance data
- Automatic SQL generation and execution using Cortex Analyst
- Interactive charts and visualizations for numeric results
- Export chat history and query results
- Works with your configured semantic model and data tables
""")