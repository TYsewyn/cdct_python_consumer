from time import sleep
from unittest import TestCase
from listener import Listener
import requests


class IntegrationTest(TestCase):

    _received_messages = []

    def setUp(self):
        self._received_messages = []
        self.listener = Listener(on_message_callback=self.__receive_messages)

    def __receive_messages(self, channel, method, properties, body):
        self._received_messages.append(body.decode("utf-8"))

    def test_listen(self):
        print("Going to listen for incoming messages")
        self.listener.listen()
        print("Going to send a message to rabbitmq")
        response = requests.post(url="http://localhost:8750/triggers/group:application/ping_pong")
        self.assertEqual(response.status_code, 200, "Couldn't send trigger")
        print("Waiting 2 seconds for the message to be received")
        sleep(2)
        self.assertEqual(len(self._received_messages), 1)
        self.assertEqual(self._received_messages[0], '{"message":"pong"}')
