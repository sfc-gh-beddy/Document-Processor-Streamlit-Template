import streamlit as st
from config import *

# Must be the first Streamlit command
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🔬",  # Customize this emoji for your domain
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the home page
st.markdown("""
<style>
/* Main header styling */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
}

.main-header p {
    margin: 10px 0 0 0;
    font-size: 1.2rem;
    opacity: 0.9;
}

/* Option cards styling */
.option-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #e9ecef;
    margin: 20px 0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.option-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.option-number {
    background: linear-gradient(135deg, #007acc 0%, #0056b3 100%);
    color: white;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
    margin-right: 20px;
    box-shadow: 0 4px 12px rgba(0,122,204,0.3);
}

/* Status badges */
.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-left: 10px;
}

.status-ready {
    background-color: #d1edff;
    color: #0056b3;
    border: 1px solid #b3d9ff;
}

.status-new {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

/* Stats section */
.stats-container {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 25px;
    border-radius: 12px;
    margin: 25px 0;
}

.stat-item {
    text-align: center;
    padding: 15px;
}

.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: #007acc;
    margin: 0;
}

.stat-label {
    color: #6c757d;
    font-size: 0.9rem;
    margin: 5px 0 0 0;
}
</style>
""", unsafe_allow_html=True)

# Welcome section
st.markdown(f"""
<div class="main-header">
    <h1>🔬 {APP_TITLE}</h1>
    <p>{APP_SUBTITLE}</p>
</div>
""", unsafe_allow_html=True)

# Platform overview
st.markdown("## 🌟 Platform Overview")
st.markdown(f"""
Welcome to the {APP_TITLE}! This comprehensive suite of tools leverages cutting-edge AI to transform 
how you process, extract, and analyze {DOCUMENT_TYPE} and {PRIMARY_USE_CASE}.
""")

# Stats section
st.markdown("""
<div class="stats-container">
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #495057;">Platform Capabilities</h3>
    </div>
""", unsafe_allow_html=True)

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown(f"""
    <div class="stat-item">
        <p class="stat-number">{PLATFORM_STATS['file_formats']}</p>
        <p class="stat-label">File Formats Supported</p>
    </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown(f"""
    <div class="stat-item">
        <p class="stat-number">{PLATFORM_STATS['languages']}</p>
        <p class="stat-label">Languages Supported</p>
    </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown(f"""
    <div class="stat-item">
        <p class="stat-number">{PLATFORM_STATS['ai_tools']}</p>
        <p class="stat-label">AI-Powered Tools</p>
    </div>
    """, unsafe_allow_html=True)

with stat_col4:
    st.markdown(f"""
    <div class="stat-item">
        <p class="stat-number">{PLATFORM_STATS['custom_extractions']}</p>
        <p class="stat-label">Custom Extractions</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Tools section
st.markdown("## 🛠️ Available Tools")
st.markdown("Choose the right tool for your specific needs:")

# Option 1 - Document Processor
st.markdown(f"""
<div class="option-card">
    <h3><span class="option-number">1</span>📊 Document Processor 
    <span class="status-badge status-ready">{TOOL_STATUS['document_processor']}</span></h3>
</div>
""", unsafe_allow_html=True)

# Option 2 - AI Extract  
st.markdown(f"""
<div class="option-card">
    <h3><span class="option-number">2</span>🔍 AI Extract 
    <span class="status-badge status-ready">{TOOL_STATUS['ai_extract']}</span></h3>
</div>
""", unsafe_allow_html=True)

# Option 3 - Natural Language Chat
st.markdown(f"""
<div class="option-card">
    <h3><span class="option-number">3</span>💬 Natural Language Chat 
    <span class="status-badge status-ready">{TOOL_STATUS['natural_language_chat']}</span></h3>
</div>
""", unsafe_allow_html=True)

# Getting started
st.markdown("## 🚀 Get Started")
st.info("👈 **Use the sidebar navigation** to access each tool. Each page provides detailed instructions and examples to help you get started quickly.")