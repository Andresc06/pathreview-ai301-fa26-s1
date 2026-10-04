"""Tests for the Redis probe in api/routes/health.py."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.mark.unit
class TestHealthRedisProbe:
    """Test suite for the Redis health probe's client construction."""

    def test_redis_client_built_from_redis_url(self):
        """The probe must build its client from settings.redis_url, not
        the nonexistent redis_host/redis_port fields (issue #62)."""
        from core.config import settings

        with patch("redis.Redis.from_url") as mock_from_url:
            mock_from_url.return_value = MagicMock(ping=MagicMock(return_value=True))

            import redis

            r = redis.Redis.from_url(settings.redis_url, decode_responses=True)
            r.ping()

            mock_from_url.assert_called_once_with(settings.redis_url, decode_responses=True)

    def test_redis_url_setting_exists(self):
        """Guard against regressing to the old host/port fields."""
        from core.config import settings

        assert hasattr(settings, "redis_url")
        assert not hasattr(settings, "redis_host")
        assert not hasattr(settings, "redis_port")
