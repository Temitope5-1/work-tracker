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
    .day-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 2px solid #e5e7eb;
    }
    .today-card {
        border: 3px solid #667eea;
    }
    .weekend {
        color: #dc2626;
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


def save_data():
    with open('work_hours_data.json', 'w') as f:
        json.dump(st.session_state.entries, f)


# Load data on startup
load_data()

# Header
st.markdown("<h1 style='text-align: center; color: white;'>⏰ Work Hours Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; font-size: 1.2rem;'>February 2026</p>", unsafe_allow_html=True)


# Calculate stats
def calculate_stats():
    if not st.session_state.entries:
        return 0, 0, 0, 0

    total_hours = sum(entry['hours'] for entry in st.session_state.entries.values())
    logged_days = len(st.session_state.entries)
    avg_hours = total_hours / logged_days if logged_days > 0 else 0
    multiplied_total = total_hours * 260

    return total_hours, logged_days, avg_hours, multiplied_total


total_hours, logged_days, avg_hours, multiplied_total = calculate_stats()

# Stats display
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Hours", f"{total_hours:.1f}")
    st.metric("Days Logged", logged_days)
with col2:
    st.metric("Avg/Day", f"{avg_hours:.1f}")
    st.metric("Total × 260", f"{multiplied_total:,.0f}")

st.markdown("---")

# All days of February 2026
st.subheader("📅 February 2026 - All Days")

# Generate all days in February 2026
year = 2026
month = 2
num_days = calendar.monthrange(year, month)[1]  # 28 days in Feb 2026

today = date.today()

# Display each day
for day in range(1, num_days + 1):
    current_date = date(year, month, day)
    date_key = current_date.strftime("%Y-%m-%d")
    day_name = current_date.strftime("%A")
    is_weekend = current_date.weekday() >= 5  # Saturday = 5, Sunday = 6
    is_today = current_date == today

    # Check if entry exists
    has_entry = date_key in st.session_state.entries

    # Create expander for each day
    day_label = f"{'🔵 ' if is_today else ''}Feb {day} - {day_name}"
    if is_weekend:
        day_label += " 🏖️"
    if has_entry:
        entry = st.session_state.entries[date_key]
        day_label += f" ✅ ({entry['hours']} hrs)"
    else:
        day_label += " ⚪ Not logged"

    with st.expander(day_label, expanded=is_today and not has_entry):
        col1, col2 = st.columns([1, 2])

        with col1:
            hours = st.number_input(
                "Hours worked",
                min_value=0.0,
                max_value=24.0,
                step=0.5,
                value=entry['hours'] if has_entry else 0.0,
                key=f"hours_{date_key}"
            )

        with col2:
            notes = st.text_input(
                "Notes (optional)",
                value=entry.get('notes', '') if has_entry else '',
                key=f"notes_{date_key}"
            )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("💾 Save", key=f"save_{date_key}", use_container_width=True):
                if hours > 0:
                    st.session_state.entries[date_key] = {
                        'hours': hours,
                        'notes': notes,
                        'date': date_key
                    }
                    save_data()
                    st.success(f"Saved {hours} hours!")
                    st.rerun()
                else:
                    st.error("Please enter hours > 0")

        with col_btn2:
            if has_entry:
                if st.button("🗑️ Delete", key=f"delete_{date_key}", use_container_width=True):
                    del st.session_state.entries[date_key]
                    save_data()
                    st.success("Entry deleted!")
                    st.rerun()

# Settings in sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    st.subheader("Data Management")
    if st.button("🗑️ Clear All Data"):
        if st.checkbox("Are you sure?"):
            st.session_state.entries = {}
            save_data()
            st.success("All data cleared!")
            st.rerun()

    st.markdown("---")
    st.markdown("**Export/Import**")

    # Export
    if st.session_state.entries:
        json_data = json.dumps(st.session_state.entries, indent=2)
        st.download_button(
            label="📥 Export Data",
            data=json_data,
            file_name="work_hours_backup.json",
            mime="application/json"
        )

    # Import
    uploaded_file = st.file_uploader("📤 Import Data", type=['json'])
    if uploaded_file is not None:
        imported_data = json.load(uploaded_file)
        st.session_state.entries = imported_data
        save_data()
        st.success("Data imported!")
        st.rerun()

    st.markdown("---")
    st.info(f"**Total Days:** {num_days}\n\n**Logged:** {logged_days}\n\n**Remaining:** {num_days - logged_days}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: white; opacity: 0.8;'>Track your work hours effortlessly!</p>",
            unsafe_allow_html=True)