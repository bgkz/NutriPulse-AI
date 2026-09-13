from redis import Redis
from rq import Queue

redis_connection = Redis(
    host="localhost",
    port=6379,
)

queue = Queue(
    "default",
    connection=redis_connection,
)
