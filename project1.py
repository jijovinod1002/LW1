import pywhatkit
import streamlit as st
import datetime
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

st.title("Whatsapp Message Sender App")

phone = st.text_input("Enter your phone number with country code (+91)")
message = st.text_area("Enter your message in here")

now = datetime.datetime.now()
hour = st.number_input("Hour (24-hour format)", min_value=0, max_value=23, value=now.hour)
minute = st.number_input("Minute (Disclaimer: Make sure to enter a time 2 minutes ahead of current time to avoid error)", min_value=0, max_value=59, value=(now.minute + 2) % 60)

send_WA  = st.button("Send Message", key="WA")

if send_WA:
    try:
        st.success(f"Sending message to {phone} at {hour}:{minute}... (You will have to wait for the whatsapp message to send, to send an sms)")
        pywhatkit.sendwhatmsg(phone, message, int(hour), int(minute))
        st.info("Please wait, WhatsApp Web will open.")
    except Exception as e:
        st.error(f"Failed to send message: {e}")
        
account_sid = "ACaf51957d3b2037a0d0f909424fe60970"
auth_token = "6874df88f9d9bd378cb9530b7b5fced3"
twilio_number = '+17856452753'

st.title("SMS Sender App")
st.write("Send text messages using Python + Twilio")

to_number = st.text_input("Enter recipient phone number (with country code)", "+91")

message_body = st.text_area("Enter your message")

if st.button("Send SMS", key="SMS"):
    if to_number and message_body:
        try:
            client = Client(account_sid, auth_token)
            account = client.api.accounts(account_sid).fetch()
            st.success(f"✅ Authenticated: {account.friendly_name}")

            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=to_number
            )
            st.success(f"✅ Message sent! SID: {message.sid}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            if "21608" in str(e):
                st.error("This number is not verified. Twilio trial accounts can only send messages to verified numbers.\n\n👉 Please verify the number at https://www.twilio.com/console/phone-numbers/verified or upgrade your account.")
            else:
                st.warning("Error at {e}")

st.title("Mail Sender App")
st.write("Send Mail using through SMTP")

sendgrid_api = "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"  # ⚠️ Consider using st.secrets
from_email = "vinodjijo12@gmail.com"
to_emails = st.text_input("Enter receiver's email address")
plain_text_content = st.text_area("Enter your message", key="mail")

def send_mail():
    try:
        email = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject="Message from Streamlit App",
            plain_text_content=plain_text_content
        )
        sg = SendGridAPIClient(sendgrid_api)
        response = sg.send(email)
        if response.status_code == 202:
            st.success("✅ Email sent successfully!")
        else:
            st.error(f"❌ Failed to send email, status code: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Failed to send Email: {e}")

if st.button("Send Mail", key="mail1"):
    if sendgrid_api and from_email and to_emails and plain_text_content:
        send_mail()
    else:
        st.error("Please fill in all the fields before sending")