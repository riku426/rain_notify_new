#coding:UTF-8
import requests

def rain_notify(grounds='どこか'):
    url = "https://notify-api.line.me/api/notify"
    token = "G4JwRdZdmnodYGy65ZWB51E1O5yo8CREmS5MKNvKqsR"
    headers = {"Authorization" : "Bearer "+ token}

    message = ''
    for g in grounds:
        message += g + 'でコート不良でたよ\n'
    payload = {"message" :  message}

    r = requests.post(url ,headers = headers ,params=payload)

if __name__ == '__main__':
    rain_notify()