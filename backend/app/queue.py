import os

from redis import Redis
from rq import Queue

redis_connection = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
)
queue = Queue(
    "default",
    connection=redis_connection,
)
