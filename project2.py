import streamlit as st
import instabot
import os
from PIL import Image
import io
import tempfile

st.set_page_config(layout="centered", page_title="Instagram Post Maker")

st.title("Instagram Post Maker ✨")
st.markdown("---")

st.info("⚠ *Important:* This application uses the instabot library, which simulates browser actions. Using automated tools may go against Instagram's terms of service and could lead to temporary or permanent account restrictions. Use responsibly!")
st.info("Also make sure you have python v3.12 or any earlier versions along with the rest of the required libraries which are streamlit, pillow and instabot")

st.subheader("Login Credentials")
user = st.text_input("Enter your Instagram username:", key="username_input")
passwd = st.text_input("Enter your Instagram password:", type="password", key="password_input")

st.subheader("Post Details")
image_file = st.file_uploader(label="Choose an image for your post:", type=["jpg", "jpeg", "png"], key="image_uploader")
caption = st.text_area("Enter the caption for your Instagram post:", max_chars=2200, key="caption_input")

st.markdown("---")

if st.button(label="🚀 Click to Post!", key="post_button"):
    if not user or not passwd:
        st.error("Please enter both username and password.")
    elif image_file is None:
        st.error("Please upload an image for your post.")
    elif not caption:
        st.warning("You're about to post without a caption. Are you sure?")
        if not st.checkbox("Yes, post without caption", key="confirm_no_caption"):
            st.stop()

    else:
        with st.spinner("Posting to Instagram... This might take a moment."):
            mybot = instabot.Bot()
            temp_image_path = None

            try:
                st.write("Attempting to log in...")
                mybot.login(username=user, password=passwd)
                st.success("Logged in successfully!")

                bytes_data = image_file.getvalue()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                    tmp_file.write(bytes_data)
                    temp_image_path = tmp_file.name

                st.write(f"Uploading image: {image_file.name} with caption...")
                if mybot.upload_photo(temp_image_path, caption=caption):
                    st.success("🎉 Post made successfully!! Check your Instagram profile.")
                else:
                    st.error("❌ An unknown error occurred during the post upload. Please try again.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.error("Please ensure your username and password are correct and try again. If the issue persists, consider running this in a Linux environment (like WSL on Windows) as instabot can have compatibility issues on Windows.")
            finally:
                try:
                    mybot.logout()
                    st.info("Logged out from Instagram.")
                except Exception as e:
                    st.warning(f"Could not log out cleanly: {e}")
                if temp_image_path and os.path.exists(temp_image_path):
                    os.remove(temp_image_path)
                    st.info("Temporary image file cleaned up.")

st.markdown("---")
st.markdown("Developed with ❤ using Streamlit and instabot.")