from memphis.producer import Producer
from fastapi import APIRouter


class ProducerRouter(APIRouter):

    def __init__(self, producer: Producer):
        super().__init__()
        self._memphis: Producer = producer
