from Webapplicatie import *
from Webapplicatie.message import *
from Webapplicatie.TFA import *
from Webapplicatie.models import *

if __name__ == '__main__':
    user = User.query.filter_by(username='BastiaanMeijer').first()
    msg = Two_Factor_Auth(user)
    msg.start()
