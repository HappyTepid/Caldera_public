import requests
import time


class PushFailure(Exception):
    pass


def __handleSMSFailure(user_key, message):
    while True:
        try:
            resp = _send_push(user_key, message)
            break
        except PushFailure:
            time.sleep(5)
            pass
    return

def __send_push(user_key, message):
    url = "https://api.pushover.net/1/messages.json"
    querystring = {"token":"TOKEN_HERE","user": user_key,"message": message}
    try:
        response = requests.request("POST", url, params=querystring)
        return response
    except:
        raise PushFailure
        pass

def public_push(user_keys, message):
    for user_key in user_keys:
        try:
            __send_push(user_key, message)
        except PushFailure:
            __handle_push_failure(user_key, message)
