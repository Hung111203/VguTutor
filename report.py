import streamlit as st
import os
import db

def run(user):
    st.header("Report a User")
    # Get list of users to report (excluding self)
    users = db.get_all_users()
    user_options = [u['username'] for u in users if u['id'] != user['id']]
    user_map = {u['username']: u['id'] for u in users}

    reported = st.selectbox("Select a user to report", user_options)
    reason = st.text_area("Reason for report")
    evidence = st.file_uploader("Upload evidence (optional)", type=['png', 'jpg', 'pdf'])

    if st.button("Submit Report"):
        if reported and reason:
            reported_id = user_map[reported]
            evidence_path = None
            if evidence is not None:
                # Save file to uploads directory
                os.makedirs('uploads', exist_ok=True)
                file_path = os.path.join('uploads', evidence.name)
                with open(file_path, 'wb') as f:
                    f.write(evidence.getbuffer())
                evidence_path = file_path
            db.add_report(user['id'], reported_id, reason, evidence_path)
            st.success("Report submitted.")
        else:
            st.error("Please select a user and provide a reason.")
