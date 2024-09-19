import os

GATUS_API_URL = os.environ.get("GATUS_API_URL")
if GATUS_API_URL:

    if not GATUS_API_URL.startswith(("http://", "https://")):
        GATUS_API_URL = "http://" + GATUS_API_URL

    GATUS_API_URL = GATUS_API_URL.rstrip('/')
    if not GATUS_API_URL.endswith('/api'):
        GATUS_API_URL += '/api'

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
