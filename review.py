import streamlit as st
import db

def run(user):
    st.header("Rate and Review a Tutor")
    # Get list of tutors
    tutors = db.get_tutors()
    tutor_options = [t['username'] for t in tutors]
    tutor_usernames = {t['username']: t['id'] for t in tutors}

    selected_tutor = st.selectbox("Select a tutor", tutor_options)
    rating = st.slider("Rating (1-5)", 1, 5, 3)
    comment = st.text_area("Comment")

    if st.button("Submit Review"):
        if selected_tutor:
            tutor_id = tutor_usernames[selected_tutor]
            db.add_review(user['id'], tutor_id, rating, comment)
            st.success("Review submitted.")
        else:
            st.error("Please select a tutor to review.")

    # Display reviews for selected tutor
    if selected_tutor:
        st.subheader("Reviews for " + selected_tutor)
        tutor_id = tutor_usernames[selected_tutor]
        reviews = db.get_reviews_for_tutor(tutor_id)
        for r in reviews:
            reviewer = db.get_user_by_id(r['reviewer_id'])
            st.write(f"{reviewer['username']} rated {r['rating']} stars: {r['comment']} ({r['timestamp']})")
