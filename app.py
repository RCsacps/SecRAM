import streamlit as st

st.set_page_config(page_title="Security Risk Scorer", layout="centered")

st.title("🛡️ Security Risk Assessment Tool")
st.write("Complete the form below to calculate the event risk score and generate a summary.")

# --- Data Structure ---
# Mapping choices to their (Score, Label)
criteria_data = {
    "Event Duration": {"weight": 0.05, "options": {"N/A": 0, "Under 2 hours": 1, "2-4 hours": 3, "Over 4 hours": 5}},
    "Recurring Event": {"weight": 0.05, "options": {"N/A": 0, "Annual or Monthly": 1, "Weekly": 5}},
    "Publicising of Event": {"weight": 0.10, "options": {"No advertising": 0, "Venue/timing not publicised": 1, "Venue OR timing publicised": 3, "Venue AND timing advertised": 5}},
    "Advertisement Medium": {"weight": 0.06, "options": {"No advertising": 0, "Closed social media/Email": 1, "WhatsApp groups": 3, "Public social media/Press": 5}},
    "Access Control": {"weight": 0.15, "options": {"100% known guests": 0, "Invitation-only, ID required": 1, "Guest list + basic checks": 3, "Open/public access": 5}},
    "Guest Vetting": {"weight": 0.10, "options": {"Personally known": 0, "All attendees verified": 1, "Basic vetting": 3, "No vetting": 5}},
    "Venue Access": {"weight": 0.05, "options": {"N/A": 0, "Sole occupancy/Road with TMO": 1, "Shared/Venue Security": 3, "Road without TMO": 5}},
    "Staff Validation": {"weight": 0.05, "options": {"No staff": 0, "All staff pre-vetted": 1, "Partial vetting": 3, "No vetting": 5}},
    "Date of Event": {"weight": 0.03, "options": {"N/A": 0, "No risk date": 1, "Somewhat significant": 3, "High-risk anniversary": 5}},
    "Event Theme": {"weight": 0.05, "options": {"N/A": 0, "No link": 1, "Potential protest risk": 3, "Highly controversial": 5}},
    "Public Nature": {"weight": 0.05, "options": {"N/A": 0, "Indoors (Not public)": 1, "Outdoors (Mitigated) / Indoors (Visible)": 3, "Outdoors (Public/No control)": 5}},
    "Attendee Profile": {"weight": 0.02, "options": {"N/A": 0, "No VIPs": 1, "Unprotected VIPs": 3, "Protected VIPs": 5}},
    "Max Guest Count": {"weight": 0.05, "options": {"Under 25": 0, "25-249": 1, "250-500": 3, "Over 500": 5}},
}

# --- Form UI ---
with st.form("assessment_form"):
    user_responses = {}
    
    # Create inputs for each criteria
    for label, info in criteria_data.items():
        user_responses[label] = st.selectbox(label, options=list(info["options"].keys()))
    
    submitted = st.form_submit_button("Generate Assessment")

# --- Logic & Output ---
if submitted:
    total_weighted_score = 0
    summary_text = "SECURITY ASSESSMENT SUMMARY\n"
    summary_text += "---------------------------\n"
    
    for label, selected_option in user_responses.items():
        score = criteria_data[label]["options"][selected_option]
        weight = criteria_data[label]["weight"]
        weighted_score = score * weight
        total_weighted_score += weighted_score
        
        summary_text += f"- {label}: {selected_option} (Score: {score})\n"
    
    summary_text += "---------------------------\n"
    summary_text += f"FINAL CALCULATED SCORE: {round(total_weighted_score, 2)} / 5.0"

    st.subheader("Results")
    st.metric("Total Risk Score", f"{round(total_weighted_score, 2)} / 5.0")
    
    st.write("### Calendar Invite Text")
    st.info("Copy the text below into your calendar invite details.")
    st.text_area(label="Copy-pasteable Output", value=summary_text, height=400)
