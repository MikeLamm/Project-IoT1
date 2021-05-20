import random
import string
from twilio.rest import Client


class SendAuth:
    def __init__(self, code, tel):
        self.client = client = Client("AC13126afe315bed81fc1cf46855f951af", "6932f95caa652f7efc061e559064cc9d")
        self.code = code
        self.tel = tel


    def Send(self):
        message = self.code
        self.client.messages.create(to=self.tel, 
                            from_="+18327726149", 
                            body=message)

class Two_Factor_Auth:

    def __init__(self, user):
        self.user = user
        self.tel = f'+31{str(self.user.tel)}'
        self.code = ''

    def generate_code(self):
        for i in range(5):
            self.code += random.choice(string.hexdigits)

    def send_auth(self):
        msg = SendAuth(self.code, self.tel)
        msg.Send()

    def send_code(self):
        self.generate_code()
        self.send_auth()
        return self.code






