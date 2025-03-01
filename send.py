import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
my_phone_number = os.environ["MY_PHONE_NUMBER"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='whatsapp:+14155238886',
    # content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
    body="Namaste!!",
    to='whatsapp:' + my_phone_number
)

print(message.sid)