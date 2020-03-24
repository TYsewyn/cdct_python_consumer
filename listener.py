from threading import Thread
from time import sleep

import pika


class Listener:

    _connection = None
    _thread = None

    _host: str = 'localhost'
    _port: int = 5672
    _username: str = 'guest'
    _password: str = 'guest'
    _virtualhost: str = '/'
    _exchange: str = 'output'
    _queue: str = 'input'
    _on_message_callback = None

    def __init__(self,
                 host: str = 'localhost',
                 port: int = 5672,
                 username: str = 'guest',
                 password: str = 'guest',
                 virtualhost: str = '/',
                 exchange: str = 'output',
                 queue: str = 'input',
                 on_message_callback=None) -> None:
        super().__init__()
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._virtualhost = virtualhost
        self._exchange = exchange
        self._queue = queue
        self._on_message_callback = on_message_callback

    def listen(self):
        if self._thread is None:
            self._thread = ListenerThread(host=self._host,
                                          port=self._port,
                                          username=self._username,
                                          password=self._password,
                                          virtualhost=self._virtualhost,
                                          exchange=self._exchange,
                                          queue=self._queue,
                                          on_message_callback=self._on_message_callback)
            self._thread.setDaemon(True)
            self._thread.start()


class ListenerThread(Thread):

    _channel = None

    def __init__(self,
                 host: str = 'localhost',
                 port: int = 5672,
                 username: str = 'guest',
                 password: str = 'guest',
                 virtualhost: str = '/',
                 exchange: str = 'output',
                 queue: str = 'input',
                 on_message_callback=None):
        Thread.__init__(self)
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=host,
                                               port=port,
                                               virtual_host=virtualhost,
                                               credentials=credentials,
                                               socket_timeout=10,
                                               retry_delay=5,
                                               connection_attempts=3)
        connection = pika.BlockingConnection(parameters=parameters)
        self._channel = connection.channel()
        self._channel.queue_declare(queue)
        self._channel.queue_bind(exchange=exchange, queue=queue)
        self._channel.basic_consume(queue, on_message_callback=on_message_callback, auto_ack=True)

    def run(self):
        while self.is_alive():
            sleep(1)
            self._channel.start_consuming()
        self._channel.stop_consuming()
