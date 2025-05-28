import os

class Config:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/sydney_events")
    EVENTS_KEY = "sydney:events"
    EMAIL_LIST_KEY = "email:subscribers"
    TTL_SECONDS = 6 * 60 * 60  # 6 hours
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")
