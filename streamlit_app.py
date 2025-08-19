import streamlit as st

# =============================================================================
# CONFIGURATION
# =============================================================================

APP_TITLE = "CDC Pertussis Document AI Platform"
APP_SUBTITLE = "Advanced AI-powered document processing and epidemiological data extraction"

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="CDC Pertussis Document AI", 
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1f4e79 0%, #2e8b57 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .option-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f4e79;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .option-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .option-number {
        background: #1f4e79;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 50%;
        font-weight: bold;
        margin-right: 1rem;
    }
    
    .status-badge {
        float: right;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-ready {
        background: #d4edda;
        color: #155724;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #1f4e79;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# MAIN HEADER
# =============================================================================

st.markdown(f"""
<div class="main-header">
    <h1>{APP_TITLE}</h1>
    <p>{APP_SUBTITLE}</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# PLATFORM STATISTICS
# =============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">3</div>
        <div class="stat-label">AI-Powered Tools</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">10+</div>
        <div class="stat-label">Data Fields Extracted</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">Multiple</div>
        <div class="stat-label">Document Formats</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">Real-time</div>
        <div class="stat-label">Processing</div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# AVAILABLE TOOLS
# =============================================================================

st.markdown("## 🛠️ Available Tools")

# Document Processor
st.markdown("""
<div class="option-card">
    <h3><span class="option-number">1</span>📊 Document Processor 
    <span class="status-badge status-ready">Ready</span></h3>
    <p><strong>Upload and process CDC pertussis surveillance documents</strong></p>
    <p>• Select from multiple trained AI models<br>
    • Automatic data extraction and structuring<br>
    • Results stored in organized tables</p>
</div>
""", unsafe_allow_html=True)

# AI Extract
st.markdown("""
<div class="option-card">
    <h3><span class="option-number">2</span>🔍 AI Extract 
    <span class="status-badge status-ready">Ready</span></h3>
    <p><strong>Extract specific epidemiological data fields</strong></p>
    <p>• Upload documents or paste text directly<br>
    • 10 key pertussis surveillance questions<br>
    • Structured JSON output for analysis</p>
</div>
""", unsafe_allow_html=True)

# Natural Language Chat  
st.markdown("""
<div class="option-card">
    <h3><span class="option-number">3</span>💬 Natural Language Chat
    <span class="status-badge status-ready">Ready</span></h3>
    <p><strong>Query your processed data using natural language</strong></p>
    <p>• Ask questions about surveillance data<br>
    • Automatic SQL generation and execution<br>
    • Interactive charts and visualizations</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# GETTING STARTED
# =============================================================================

st.markdown("## 🚀 Getting Started")

st.markdown("""
1. **📊 Start with Document Processor** - Upload your CDC pertussis documents to extract and structure data
2. **🔍 Use AI Extract** - Pull specific epidemiological fields from documents or text
3. **💬 Explore with Chat** - Ask natural language questions about your processed data

**👈 Select a tool from the sidebar to begin!**
""")

# =============================================================================
# SIDEBAR INSTRUCTIONS
# =============================================================================

st.sidebar.markdown("## 📋 Quick Guide")
st.sidebar.markdown("""
**Document Processor:**
- Upload PDF, DOC, or image files
- Select appropriate AI model
- Review extracted data
- Copy or save results

**AI Extract:** 
- Upload documents OR paste text
- Automatic pertussis field extraction
- 10 key surveillance questions
- JSON formatted output

**Natural Language Chat:**
- Ask questions about your data
- View generated SQL queries
- Interactive visualizations
- Export results
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**💡 Need Help?**")
st.sidebar.markdown("Check the documentation in each tool for detailed instructions.")