import requests
import time
import bot_lib as libs

after = time.time() - 24 * 60 * 60
url = 'http://127.0.0.1:5000/'
while True:
    response = requests.get(f'{url}messages', params={'after': after})
    messages = response.json()['messages']
    for message in messages:
        in_message = message['text'].lower().split()
        after = message['time']

        if '@father_bot' in in_message[0]:
            text_out = libs.bot_call(in_message)
            message = {'name': "Father_bot",
                       'password': 'your_father',
                       'text': text_out}
            response = requests.post(
                f'{url}send',
                json=message
            )
    time.sleep(6)

