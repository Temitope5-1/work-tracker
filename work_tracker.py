import streamlit as st
from datetime import datetime, date, timedelta
import json
import calendar

# Page config
st.set_page_config(
    page_title="Work Hours Tracker",
    page_icon="⏰",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'entries' not in st.session_state:
    st.session_state.entries = {}

# Load data from file (persistence)
def load_data():
    try:
        with open('work_hours_data.json', 'r') as f:
            st.session_state.entries = json.load(f)
    except FileNotFoundError:
        st.session_state.entries = {}

def save_d
