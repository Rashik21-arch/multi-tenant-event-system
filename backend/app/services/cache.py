import redis
import json

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def set_event_cache(event_id: int, event_data: dict):
    redis_client.setex(
        f"event:{event_id}",
        300,
        json.dumps(event_data)
    )


def get_event_cache(event_id: int):
    data = redis_client.get(f"event:{event_id}")

    if data:
        return json.loads(data)

    return None


def delete_event_cache(event_id: int):
    redis_client.delete(f"event:{event_id}")