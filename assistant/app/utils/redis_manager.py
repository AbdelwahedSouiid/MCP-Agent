import json
import redis
from typing import Optional, Dict, Any
from app.config.redis_settings import redis_settings
from app.config.settings import settings

class RedisManager:
    """Repository layer - Only handles raw Redis operations"""
    def __init__(self):
        self.client = redis.Redis.from_url(
            redis_settings.get_redis_url(),
            decode_responses=True,
            socket_timeout=5,
            retry_on_timeout=True
        )
        self.session_id = settings.SESSION_COOKIE_NAME
        self.expiration = 86400  # 24h

    def _get_key(self) -> str:
        return f"session:{self.session_id}:history"

    async def save_data(self, data: Dict[str, Any]) -> bool:
        """Save raw data to Redis"""
        try:
            key = self._get_key()
            self.client.set(key, json.dumps(data, ensure_ascii=False, default=str))
            self.client.expire(key, self.expiration)
            return True
        except Exception as e:
            raise RedisOperationError(f"Error saving data to Redis: {str(e)}")

    async def get_data(self) -> Optional[Dict[str, Any]]:
        """Get raw data from Redis"""
        try:
            key = self._get_key()
            raw_data = self.client.get(key)
            return json.loads(raw_data) if raw_data else None
        except Exception as e:
            raise RedisOperationError(f"Error getting data from Redis: {str(e)}")

    async def delete_data(self) -> bool:
        """Delete data from Redis"""
        try:
            key = self._get_key()
            return self.client.delete(key) > 0
        except Exception as e:
            raise RedisOperationError(f"Error deleting data from Redis: {str(e)}")

class RedisOperationError(Exception):
    """Custom exception for Redis operations"""
    pass