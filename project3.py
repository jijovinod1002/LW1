import streamlit as st
import tweepy
import os
import tempfile
from PIL import Image
import io

st.set_page_config(layout="centered", page_title="Twitter Post Maker (X)")

st.title("╰(°▽°)╯ Twitter Post Maker (X) ")
st.markdown("---")

st.info("""
    ⚠ *Important Notes for Twitter API (X API):*
    1.  *Developer Account Required:* You need a Twitter Developer Account and a Project/App to get API credentials.
        * Go to [developer.twitter.com/en/portal/projects-and-apps](https://developer.twitter.com/en/portal/projects-and-apps)
        * Create a Project and an App within it.
        * Ensure your App has *"Read and Write"* permissions.
    2.  *API Keys & Tokens:* You will need:
        * Consumer Key (API Key)
        * Consumer Secret (API Secret)
        * Access Token
        * Access Token Secret
        * These are found under your App's "Keys and tokens" tab. Regenerate if permissions are changed.
    3.  *Rate Limits & Tiers:* Twitter's API has strict rate limits and different access tiers (Free, Basic, Pro, Enterprise). The "Free" tier has very limited write access. If you encounter errors like "403 Forbidden" or "Rate limit exceeded," it's likely due to these restrictions.
""")

st.subheader("Twitter API Credentials")
consumer_key = st.text_input("Enter your Consumer Key (API Key):", type="password", key="consumer_key")
consumer_secret = st.text_input("Enter your Consumer Secret (API Secret):", type="password", key="consumer_secret")
access_token = st.text_input("Enter your Access Token:", type="password", key="access_token")
access_token_secret = st.text_input("Enter your Access Token Secret:", type="password", key="access_token_secret")

st.subheader("Tweet Details")
tweet_text = st.text_area("What's happening?", max_chars=280, key="tweet_text")
image_file = st.file_uploader(label="Upload an image (optional):", type=["jpg", "jpeg", "png"], key="tweet_image_uploader")

st.markdown("---")

if st.button(label=" Post Tweet!", key="post_tweet_button"):
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        st.error("Please enter all Twitter API credentials.")
    elif not tweet_text and image_file is None:
        st.error("Please enter some text or upload an image for your tweet.")
    elif not tweet_text and image_file is not None:
        st.warning("You're about to post an image without text. Are you sure?")
        if not st.checkbox("Yes, post image without text", key="confirm_no_text"):
            st.stop()
    else:
        with st.spinner("Posting your tweet... This might take a moment."):
            temp_image_path = None

            try:
                client = tweepy.Client(
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret
                )

                auth_v1_1 = tweepy.OAuth1UserHandler(
                    consumer_key, consumer_secret, access_token, access_token_secret
                )
                api_v1_1 = tweepy.API(auth_v1_1)

                media_ids = []
                if image_file is not None:
                    st.write("Uploading image to Twitter media library...")
                    bytes_data = image_file.getvalue()
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                        tmp_file.write(bytes_data)
                        temp_image_path = tmp_file.name

                    media_upload_response = api_v1_1.media_upload(temp_image_path)
                    media_ids.append(media_upload_response.media_id)
                    st.success("Image uploaded to Twitter media library!")

                st.write("Creating tweet...")
                response = client.create_tweet(text=tweet_text, media_ids=media_ids if media_ids else None)

                if response.data and 'id' in response.data:
                    tweet_id = response.data['id']
                    tweet_link = f"https://twitter.com/user/status/{tweet_id}"
                    st.success(f"🎉 Tweet posted successfully! [View Tweet]({tweet_link})")
                    st.balloons()
                else:
                    st.error("Unknown error Occured.")
                    if response.errors:
                        for error in response.errors:
                            st.error(f"API Error: {error.get('message', 'No message')} (Code: {error.get('code', 'N/A')})")

            except tweepy.TweepyException as e:
                st.error(f"Twitter API Error: {e}")
                st.error("Please check your API credentials and ensure your app has 'Read and Write' permissions. Also, be mindful of Twitter's API rate limits and access tiers.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                st.error("Please ensure all inputs are correct and try again.")
            finally:
                if temp_image_path and os.path.exists(temp_image_path):
                    os.remove(temp_image_path)
                    st.info("Temporary image file cleaned up.")

st.markdown("---")