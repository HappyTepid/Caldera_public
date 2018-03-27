import urllib
import time


class SMSFailure(Exception):
    pass


def __sendSMS(uname, hashCode, numbers, sender, message):
    data = urllib.parse.urlencode({'username': uname, 'hash': hashCode, 'numbers': numbers,
                                   'message': message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("http://api.txtlocal.com/send/?")
    try:
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        return (fr)
    except urllib.error.URLError:
        raise SMSFailure
        pass


def __handleSMSFailure(mobile_number, message):
    while True:
        try:
            resp = __sendSMS('webmaster@rcvs.org.uk', 'KEY', mobile_number, 'Caldera', message)
            break
        except SMSFailure:
            time.sleep(5)
            pass
    return


def publicSMS(mobile_numbers, message):
    for mobile_number in mobile_numbers:
        try:
            resp = __sendSMS('webmaster@rcvs.org.uk', 'KEY', mobile_number, 'Caldera', message)
        except SMSFailure:
            __handleSMSFailure(mobile_number, message)
