import streamlit as st
import auth
import db
import booking
import chat
import review
import report

# Initialize the database (tables will be created at import)
st.set_page_config(page_title="VGtutor Platform")

# Session state for logged-in user
if 'user' not in st.session_state:
    st.session_state.user = None

# Login / Register
if st.session_state.user is None:
    st.title("Welcome to VGtutor!")
    choice = st.selectbox("Login or Sign Up", ["Login", "Sign Up"])

    if choice == "Sign Up":
        st.subheader("Create a new account")
        new_username = st.text_input("Username", key="new_username")
        new_password = st.text_input("Password", type='password', key="new_password")
        is_tutor = st.checkbox("Register as a tutor")

        if st.button("Register"):
            if new_username and new_password:
                try:
                    success = auth.register_user(new_username, new_password, is_tutor)
                    if success:
                        st.success("Account created successfully. You can now log in.")
                    else:
                        st.error("Username already exists.")
                except Exception as e:
                    st.error(f"Registration failed: {e}")
            else:
                st.error("Please enter a username and password.")

    elif choice == "Login":
        st.subheader("Login to your account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type='password', key="login_password")

        if st.button("Login"):
            try:
                user = auth.authenticate_user(username, password)
                if user:
                    st.session_state.user = {
                        "id": user['id'],
                        "username": user['username'],
                        "is_tutor": user['is_tutor']
                    }
                    st.success(f"Logged in as {user['username']}")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password.")
            except Exception as e:
                st.error(f"Login failed: {e}")

else:
    # Logged in
    st.sidebar.title("Menu")
    st.sidebar.write(f"Logged in as {st.session_state.user['username']}")
    page = st.sidebar.selectbox("Go to", ["Book Session", "Chat", "Review", "Report", "Logout"])

    if page == "Book Session":
        booking.run(st.session_state.user)
    elif page == "Chat":
        chat.run(st.session_state.user)
    elif page == "Review":
        review.run(st.session_state.user)
    elif page == "Report":
        report.run(st.session_state.user)
    elif page == "Logout":
        st.session_state.user = None
        st.experimental_rerun()
