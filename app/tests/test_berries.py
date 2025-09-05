from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api import api
from app.main import app
from app.core.config import config

client = TestClient(app)


class FakeRedis:
    def __init__(self):
        self.storage = {}

    def get(self, key):
        return self.storage.get(key)

    def setex(self, key, ttl, value):
        self.storage[key] = value


@pytest.fixture
def mocked(monkeypatch):
    monkeypatch.setattr(api, "get_all_berries", lambda: [
        {"name": "cheri", "url": "http://test/cheri"},
        {"name": "chesto", "url": "http://test/chesto"}]
    )

    monkeypatch.setattr(api, "get_berry_by_url", lambda url:
        {"name": "cheri", "growth_time": 3} if "cheri" in url else
        {"name": "chesto", "growth_time": 7}
    )

    monkeypatch.setattr(api, "redis_cache", FakeRedis())

    with patch("app.api.api.get_all_berries") as mock_all, \
            patch("app.api.api.get_berry_by_url") as mock_by_url:
        mock_all.return_value = [
            {"name": "cheri", "url": "http://test/cheri"},
            {"name": "chesto", "url": "http://test/chesto"}]
        mock_by_url.side_effect = lambda url: {"name": "cheri", "growth_time": 3}\
            if "cheri" in url else {"name": "chesto", "growth_time": 7}
        yield


@pytest.mark.parametrize(
    "key, expected",
    [
        ("berries_names", ["cheri", "chesto"]),
        ("min_growth_time", 3),
        ("max_growth_time", 7),
        ("mean_growth_time", 5),
        ("median_growth_time", 5),
        ("variance_growth_time", 4),
        ("frequency_growth_time", {"3": 1, "7": 1}),
    ]
)
def test_get_all_berry_stats(mocked, key, expected):
    response = client.get("/allBerryStats")
    assert response.status_code == 200
    data = response.json()
    assert data[key] == expected

    fake_redis = getattr(api, "redis_cache")
    cached = fake_redis.get(config.cache_key_stats)
    assert cached is not None


@pytest.mark.parametrize(
    "attr, expected",
    [
        ("min_growth_time", 3),
        ("max_growth_time", 7),
        ("mean_growth_time", 5),
        ("median_growth_time", 5),
        ("variance_growth_time", 4),
        ("frequency_growth_time", {3: 1, 7: 1}),
    ]
)
def test_calculate_statistics(mocked, attr, expected):
    statistics = api.calculate_statistics()
    assert getattr(statistics, attr) == expected


def test_get_all_berries(monkeypatch):
    monkeypatch.setattr(api, "get_all_berries",
                        lambda: [{"name": "cheri", "url": "http://test/cheri"}])
    berries = api.get_all_berries()
    assert isinstance(berries, list)
    assert berries[0]["name"] == "cheri"


def test_get_berry_by_url(monkeypatch):
    monkeypatch.setattr(api, "get_berry_by_url",
                        lambda url: {"name": "cheri", "growth_time": 3})
    berry = api.get_berry_by_url("http://test/cheri")
    assert berry["name"] == "cheri"
    assert berry["growth_time"] == 3
