import time
from twilio.rest import Client

class SendPushNotification:
    def __init__(self, animal, residence):
        self.client = client = Client("AC13126afe315bed81fc1cf46855f951af", "6932f95caa652f7efc061e559064cc9d")
        self.animal = animal
        self.residence = residence

    def Send(self):
        message = f'{self.animal} is ontsnapt uit {self.residence}'
        self.client.messages.create(to="+31640765598", 
                            from_="+18327726149", 
                            body=message)


  
if __name__ == "__main__":
    sms = SendPushNotification('Tijger', 'Verblijf1')
    sms.Send()