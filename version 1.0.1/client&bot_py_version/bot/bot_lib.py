import json
from datetime import datetime


def bot_call(input_message):
    with open('bot_base.json', 'r', encoding='utf-8') as f:

        if '@father_bot' in input_message[0]:
            data = json.load(f)

            for element in input_message[1::]:
                for key, value in data.items():
                    if element in value:
                        if 'time.time()' in key:
                            return str('Current time - ' + datetime.now().strftime('%X'))
                        else:
                            return key

            return 'Sry, I cant understand u'


