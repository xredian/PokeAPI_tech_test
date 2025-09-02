from json import loads
from os import getenv
from statistics import mean, median, pvariance

import redis
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from models.model import BerryStatistics

load_dotenv()

app = FastAPI(title="Poke-berries statistics API")

pokeapi = getenv("POKEAPI")
cache_key_stats = getenv("CACHE_KEY_STATS")
cache_key_names = getenv("CACHE_KEY_NAMES")
cache_ttl = int(getenv("CACHE_TTL"))
redis_port = int(getenv("REDIS_PORT"))
redis_host = getenv("REDIS_HOST")
redis_db = int(getenv("REDIS_DB"))

redis_cache = redis.Redis(host=redis_host,
                          port=redis_port,
                          db=redis_db,
                          decode_responses=True)


def get_all_berries() -> list:
    response = requests.get(f"{pokeapi}?limit=100")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail="Can't get berries")
    return response.json()["results"]


def get_berry_by_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Can't get berry number {url.split('/')[-1]}, {url}")
    return response.json()


def calculate_statistics() -> BerryStatistics:
    berries = get_all_berries()
    names = [berry["name"] for berry in berries]
    urls = [berry["url"] for berry in berries]

    berries_data = [get_berry_by_url(url) for url in urls]
    growth_times = [berry["growth_time"] for berry in berries_data]

    min_gt = min(growth_times)
    median_gt = median(growth_times)
    max_gt = max(growth_times)
    mean_gt = mean(growth_times)
    variance_gt = pvariance(growth_times, mean_gt)

    frequency_gt = {}
    for time in growth_times:
        frequency_gt[time] = frequency_gt.get(time, 0) + 1

    return BerryStatistics(
        berries_names=names,
        min_growth_time=min_gt,
        median_growth_time=median_gt,
        max_growth_time=max_gt,
        variance_growth_time=variance_gt,
        mean_growth_time=mean_gt,
        frequency_growth_time=frequency_gt
    )


@app.get("/allBerryStats", response_model=BerryStatistics)
def get_all_berry_stats():
    cached = redis_cache.get(cache_key_stats)
    if cached:
        return BerryStatistics(**loads(cached))
    else:
        stats = calculate_statistics()
        redis_cache.setex(cache_key_stats, cache_ttl, stats.model_dump_json())
        return stats
