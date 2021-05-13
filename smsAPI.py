import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="I facked your mouth",
                     from_='+17472258602',
                     to='+380956756721'
                 )

# print(message.sid)