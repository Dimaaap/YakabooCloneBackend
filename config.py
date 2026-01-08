import os

import redis.asyncio as redis

HOST, PORT, PASSWORD = os.getenv("REDIS_HOST"), os.getenv("REDIS_PORT"), os.getenv("REDIS_PASSWORD")
redis_client = redis.Redis(host=HOST, port=int(PORT), password=PASSWORD, db=0, decode_responses=True)