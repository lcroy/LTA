# Client of Virtual Assistant Max
"""
max_client_test version 1.0.0

Description:
Max is following client-server style architecture.
Max client will send the REST API calls to the server for NLU service.
"""

import requests
import time
import json

class MaxClient():

    def __init__(self):
        # self.host = "http://130.226.98.77:5001/"
        # host: 172.27.15.18:5001 (the Max server ip address)
        self.host = "http://172.27.15.18:5001/"
        # self.headers = {'Content-Type': 'application/json', 'Accept-Language': 'en_US'}
        # self.host = "http://127.0.0.1:5000/"
        self.headers = {'Content-Type': 'text/plain', 'Accept-Language': 'en_US'}

    # get the response from Max Server
        # message: the text results of ASR (string type)
        # Speaker: the identified speaker (string type)
    def get_response(self, message, speaker):
        # parameters will be send to the Max server. It includes user speech(i.e. text message) and speaker
        parameters = {'message':message,'speaker':speaker}
        # {'message': message, 'requested_intent': requested_intent, 'requested_slot': {}, requested_service: requested_service}
        # results will be the json type
        # Example of result:{'intent': 'None', 'parameters': 'Hey tom, I will come to you.', 'result': 'good_request'}
        # 'get_task' is the function defined at server side for interpreting the user intent
        result = requests.get(self.host + 'get_task/', params=parameters, headers=self.headers)

        return result.json()

    def get_file(self):
        result = requests.get(self.host + 'download', headers=self.headers)

        return result.json()

    def set_face(self, max_id):
        parameters = {'max_id': max_id}
        # {'message': message, 'requested_intent': requested_intent, 'requested_slot': {}, requested_service: requested_service}
        # results will be the json type
        # Example of result:{'intent': 'None', 'parameters': 'Hey tom, I will come to you.', 'result': 'good_request'}
        # 'get_task' is the function defined at server side for interpreting the user intent
        result = requests.get(self.host + 'get_max_id/', params=parameters, headers=self.headers)

        return result

    def get_conv(self):
        result = requests.get(self.host + 'get_conv/', headers=self.headers)

        print(result.json())

max = MaxClient()

text = max.get_file()

with open('test.json', 'w') as outfile:
    json.dump(text, outfile)



