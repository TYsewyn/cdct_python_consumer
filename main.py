import os

from caller import Caller
from listener import Listener

if __name__ == "__main__":
    caller = Caller(os.environ.get('API_BASE_URL', 'http://localhost:8000'))
    print(caller.make_request())
    listener = Listener()
    listener.listen()
