import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src import jsonparser as jp
from twilio.rest import Client



class SMS():
    
    def __init__(self, to):
        self.client_ = Client(jp.getJsonValue("TWILIO_ACCOUNT_SID"), jp.getJsonValue("TWILIO_AUTH_TOKEN"))
        self.to_ = to
        
        
    def send(self, body):
        self.client_.messages.create(
            to=self.to_,
            from_=jp.getJsonValue("TWILIO_PHONE_NUMBER"),
            body=body
        )
        

if __name__=="__main__":
    sms = SMS("")
    sms.send("Test for Check")