import os
import smtplib
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    # for row in sheet:
    #     if row['prices'] > api_flight['prices']:
    #         send message

    def __init__(self):
        self.client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'))
        self.my_email = os.getenv('MY_EMAIL')
        self.password = os.getenv('EMAIL_PASSWORD')

    def send_message(self, body):
        message = self.client.messages.create(
            from_='whatsapp:+14155238886',
            body=body,
            to='whatsapp:+18599072271'
        )

        print(message.status)


    def send_mail(self, body, email_list):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.password)
            connection.sendmail(from_addr=self.my_email, to_addrs=email_list, msg=body)
