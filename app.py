import streamlit as st

st.set_page_config(page_title="Security Risk Scorer", layout="centered")

st.title("🛡️ Security Risk Assessment Tool")
st.write("Fill in the details below. Hover over the **?** for specific criteria instructions.")

# --- Data Structure with Instructions ---
criteria_data = {
    "Event Duration": {
        "help": "Impact of event length on risk.",
        "weight": 0.05, 
        "options": {"N/A": 0, "Under 2 hours": 1, "2-4 hours": 3, "Over 4 hours": 5}
    },
    "Recurring Event": {
        "help": "Recurring event taking place on a similar date and place.",
        "weight": 0.05, 
        "options": {"N/A": 0, "Annual or Monthly": 1, "Weekly": 5}
    },
    "Publicising of Event": {
        "help": "Contents of the advertisement.",
        "weight": 0.10, 
        "options": {"No advertising": 0, "Venue/timing not publicised": 1, "Venue OR timing publicised": 3, "Venue AND timing advertised": 5}
    },
    "Advertisement Medium": {
        "help": "Where the event is advertised.",
        "weight": 0.06, 
        "options": {"No advertising": 0, "Closed social media/Email": 1, "WhatsApp groups": 3, "Public social media/Press": 5}
    },
    "Access Control": {
        "help": "How guests are admitted.",
        "weight": 0.15, 
        "options": {"100% known guests": 0, "Invitation-only, ID required": 1, "Guest list + basic checks": 3, "Open/public access": 5}
    },
    "Guest Vetting": {
        "help": "Are attendees known or vetted?",
        "weight": 0.10, 
        "options": {"Personally known": 0, "All attendees verified": 1, "Basic vetting": 3, "No vetting": 5}
    },
    "Venue Access / Road": {
        "help": "Sole occupancy of venue OR is the event on a road?",
        "weight": 0.05, 
        "options": {"N/A": 0, "Sole occupancy/Road with TMO": 1, "Shared/Venue Security": 3, "Road without TMO": 5}
    },
    "Staff Validation": {
        "help": "Are venue staff / contractors vetted?",
        "weight": 0.05, 
        "options": {"No staff": 0, "All staff pre-vetted": 1, "Partial vetting": 3, "No vetting": 5}
    },
    "Date of Event": {
        "help": "Relevance to significant anniversaries.",
        "weight": 0.03, 
        "options": {"N/A": 0, "No risk date": 1, "Somewhat significant": 3, "High-risk anniversary": 5}
    },
    "Event Theme": {
        "help": "Link to controversial themes or protest risk.",
        "weight": 0.05, 
        "options": {"N/A": 0, "No link": 1, "Potential protest risk": 3, "Highly controversial": 5}
    },
    "Public Nature": {
        "help": "Opportunity for spontaneous or public attack.",
        "weight": 0.05, 
        "options": {"N/A": 0, "Indoors (Not public)": 1, "Outdoors (Mitigated) / Indoors (Visible)": 3, "Outdoors (Public/No control)": 5}
    },
    "Attendee Profile": {
        "help": "Presence of VIPs.",
        "weight": 0.02, 
        "options": {"N/A": 0, "No VIPs": 1, "Unprotected VIPs": 3, "Protected VIPs": 5}
    },
    "Max Guest Count": {
        "help": "Total number of attendees.",
        "weight": 0.05, 
        "options": {"Under 25": 0, "25-249": 1, "250-500": 3, "Over 500": 5}
    },
}

# --- Reset Logic ---
if "form_key" not in st.session_state:
    st.session_state.form_key = 0

def reset_form():
    st.session_state.form_key += 1

# --- Form UI ---
with st.form(key=f"assessment_form_{st.session_state.form_key}"):
    user_responses = {}
    
    # Create inputs for each criteria with help text
    for label, info in criteria_data.items():
        user_responses[label] = st.selectbox(
            label, 
            options=list(info["options"].keys()),
            help=info["help"]
        )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        submitted = st.form_submit_button("Generate Assessment", use_container_width=True)
    with col2:
        st.form_submit_button("Reset Form", on_click=reset_form, use_container_width=True)

# --- Logic & Output ---
if submitted:
    total_weighted_score = 0
    summary_text = "SECURITY ASSESSMENT SUMMARY\n"
    summary_text += "===========================\n\n"
    
    for label, selected_option in user_responses.items():
        score = criteria_data[label]["options"][selected_option]
        weight = criteria_data[label]["weight"]
        weighted_score = score * weight
        total_weighted_score += weighted_score
        
        summary_text += f"• {label}: {selected_option}\n"
    
    summary_text += f"\nFINAL CALCULATED RISK SCORE: {round(total_weighted_score, 2)} / 5.0"

    st.divider()
    st.subheader("Results")
    st.metric("Total Risk Score", f"{round(total_weighted_score, 2)} / 5.0")
    
    st.write("### Calendar Invite Summary")
    st.caption("Click the icon in the top right of the box below to copy all text.")
    # st.code provides a built-in copy button
    st.code(summary_text, language="text")
