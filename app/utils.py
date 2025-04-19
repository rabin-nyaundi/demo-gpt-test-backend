import time
from functools import wraps
from typing import Callable
import redis
import logging
import json
from dotenv import load_dotenv
import os
from fastapi import HTTPException, Request, status


load_dotenv()

logger = logging.getLogger(__name__)


redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST",""),
    port=14992,
    decode_responses=True,
    username="developer",
    password=os.environ.get("REDIS_PASSWORD", "")
)


def format_travel_response(raw_response: str) -> str:
    """
        Takes raw response from the Model
        Body:
            raw response:string
        Returns:
            formatted response by adding mardown(double arsterics) which will denote as bold
            joins the lines innew line
    """
    lines = raw_response.split("\n\n")
    structured_response = []
    for line in lines:
        line = line.strip()
        if line.lower().startswith("visa") or "visa" in line.lower():
            structured_response.append(f"**Visa**: {line}")
        elif line.lower().startswith("passport") or "passport" in line.lower():
            structured_response.append(f"**Passport**: {line}")
        elif line.lower().startswith("advis") or "advisory" in line.lower():
            structured_response.append(f"**Travel Advisories**: {line}")
        else:
            structured_response.append(line)
    return "\n".join(structured_response) if structured_response else raw_response



def rate_limiter(max_calls: int, time_frame: int) -> Callable:
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            now = time.time()

            # Get client IP
            client_host = request.headers.get("X-Forwarded-For", request.client.host or "unknown")
            redis_key = f"rate_limit:{client_host}"

            data = redis_client.get(redis_key)
            logger.debug(f"Redis get: key={redis_key}, data={data}")

            if data:
                rate_data = json.loads(data)
                calls = rate_data["calls"]
                last_call_time = rate_data["last_call_time"]
            else:
                calls = 0
                last_call_time = 0.0

            logger.debug(f"Rate limiter: IP={client_host}, calls={calls}, last_call={last_call_time}")

            # Calculate time elapsed since last call
            time_elapsed = now - last_call_time

            if time_elapsed > time_frame:
                calls = 1
                last_call_time = now
                logger.debug(f"Reset rate limit for IP={client_host}")
            else:
                print("rate limit reached ===")
                if calls >= max_calls:
                    logger.debug(f"Rate limit exceeded for IP={client_host}")
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit reached"
                    )
                calls += 1

            rate_data = {"calls": calls, "last_call_time": last_call_time}
            redis_client.setex(redis_key, time_frame, json.dumps(rate_data))
            logger.debug(f"Redis setex: key={redis_key}, data={rate_data}, expiry={time_frame}")

            stored_data = redis_client.get(redis_key)
            logger.debug(f"Redis verify: key={redis_key}, stored_data={stored_data}")


            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
