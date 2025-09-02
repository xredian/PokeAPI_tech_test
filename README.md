# Poke-berries statistics API
A Poke-berries statistics API as a part of technical test.\
FastAPI for getting statistics on all berries from PokeAPI with Redis caching and pytest testing.

## Installing

### On local machine
1. Clone the project
    ```bash
    git clone git@github.com:xredian/PokeAPI_tech_test.git
    cd PokeAPI_tech_test
    ```
2. Create and activate virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate/    # Linux/MacOs
    venv\Scripts\activate        # Windows
    ```
3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
4. Copy example.env to .env:
    ```bash
    cp example.env .env
    ```
5. Edit the following variables in .env file
    ```bash
    CACHE_KEY_STATS = "your_key_name"
    CACHE_KEY_NAMES = "another_key_name"
    CACHE_TTL = "360"                              # time for caching data in Redis, 360 = 1 hour, can be changed
    REDIS_HOST = "localhost"
    REDIS_PORT = "6379"
    REDIS_DB = "0"
    ```
6. Run Redis
    ```bash
    redis-server
    ```

7. Run the project
    ```bash
    uvicorn poke_api:app --reload
    ```
   * By default, FastAPI will be available at http://127.0.0.1:8000
   * OpenAPI documentation is available:
     - Swagger UI: http://127.0.0.1:8000/docs
     - ReDoc: http://127.0.0.1:8000/redoc

### In Docker
1. Clone the project as in the 1st step above
2. Copy example.env to .env and edit it as in the steps 4 and 5 above.
3. Build and start Docker container with the application
    ```bash
    docker-compose up --build api redis
    ```

## Endpoints

**GET** ```/allBerryStats``` \
returns statistics for all berries

Can be reached, for example, by curl:
```curl
curl http://127.0.0.1:8000/allBerryStats
```

Example response:
```json
{
  "berries_names": ["cheri", "chesto"],
  "min_growth_time": 3,
  "median_growth_time": 5,
  "max_growth_time": 7,
  "variance_growth_time": 4,
  "mean_growth_time": 5,
  "frequency_growth_time": {"3": 1, "7": 1}
}
```

 or with -i to see additional info
```curl
curl -i http://127.0.0.1:8000/allBerryStats
```

Data is cached in Redis for 1 hour.

## Testing
The project uses pytest and FastAPI TestClient.

To run all the test
```bash
pytest
```
To run all the test with detailed output
```bash
pytest -v
```
To run tests in docker
```bash
docker-compose run --rm test
```

### Mockes and isolation
* Tests are completely isolated from web and real Redis server
* Used FakeRedis to emulate cache 
* PokeAPI requests are replaced with mocks (```get_all_berries```, ```get_berry_by_url```)

## Project structure
```bash
poke_api.py               # main API code
models/
  |-- model.py            # pydantic response model
tests/
  |-- test_poke_api.py    # pytest tests
README.md                 # instructions and description
requirements.txt          # dependencies
docker-compose.yml
Dockerfile
example.env               # example of .env file
.env                      # environment variables
.dockerignore
.gitignore
```

## Useful links
* [FactAPI Documentation](https://fastapi.tiangolo.com/)
* [redis-py](https://redis.io/docs/latest/develop/clients/redis-py/) and [redis-server](https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/)
* [pytest](https://docs.pytest.org/en/stable/)

## Copyright
Copyright (©) 2025 by [Uliana Diakova](https://github.com/xredian) as test task for [Globant](https://www.globant.com/)
