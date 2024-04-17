import threading

import socketio
from aiomisc import entrypoint
from dotenv import load_dotenv
from keycloak import KeycloakOpenID
import os

from memphis import Memphis
import socketio
from workers.MemphisWorker import MemphisWorker
from workers.security.Config import Config
from workers.security.Worker import Worker

config = Config()
keycloak = KeycloakOpenID(server_url=config.keycloak_url,
                          client_id=config.client_id,
                          client_secret_key=config.client_secret,
                          realm_name=config.realm_name)
sio = socketio.Client(logger=True, engineio_logger=True)


def connect_error(err):
    print(err)


sio.on("connect_error", connect_error)
sio.on("*", lambda msg: print(msg))
sio.connect("http://localhost:8000", transports=["websocket"])
memphis = Memphis()


def start_worker(worker: MemphisWorker):
    with entrypoint(worker) as loop:
        loop.run_forever()


if __name__ == "__main__":
    security_worker = Worker(memphis, sio, keycloak, config)
    t1 = threading.Thread(target=start_worker, args=(security_worker,), daemon=True)
    t1.start()
    t1.join()
