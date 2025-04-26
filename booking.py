import streamlit as st
import db

def run(user):
    st.header("Book a Tutoring Session")
    # Get list of tutors
    tutors = db.get_tutors()
    tutor_options = [t['username'] for t in tutors]
    tutor_usernames = {t['username']: t['id'] for t in tutors}

    selected_tutor = st.selectbox("Select a tutor", tutor_options)
    date = st.date_input("Session Date")
    time = st.time_input("Session Time")
    subject = st.text_input("Subject/Topic")

    if st.button("Book Session"):
        if selected_tutor and subject:
            tutor_id = tutor_usernames[selected_tutor]
            # Add booking to DB
            db.add_booking(user['id'], tutor_id, str(date), str(time), subject)
            st.success("Session booked successfully!")
        else:
            st.error("Please select a tutor and subject.")

    # Display existing bookings for student
    st.subheader("My Bookings")
    bookings = db.get_bookings_for_student(user['id'])
    for b in bookings:
        tutor = db.get_user_by_id(b['tutor_id'])
        st.write(f"Tutor: {tutor['username']} - Date: {b['date']} - Time: {b['time']} - Subject: {b['subject']}")
