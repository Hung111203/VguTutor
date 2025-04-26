import streamlit as st
import db

def run(user):
    st.header("Chat")
    # Get list of users to chat with (excluding self)
    users = db.get_all_users()
    user_options = [u['username'] for u in users if u['id'] != user['id']]
    username_to_id = {u['username']: u['id'] for u in users}

    chat_with = st.selectbox("Chat with", user_options)
    if chat_with:
        other_id = username_to_id[chat_with]
        # Display chat messages
        messages = db.get_messages_between(user['id'], other_id)
        for m in messages:
            sender = db.get_user_by_id(m['sender_id'])
            timestamp = m['timestamp']
            st.write(f"{sender['username']} ({timestamp}): {m['message']}")

        # Enter a new message
        new_msg = st.text_input("New message")
        if st.button("Send"):
            if new_msg:
                db.add_message(user['id'], other_id, new_msg)
                st.experimental_rerun()
            else:
                st.error("Cannot send empty message.")
