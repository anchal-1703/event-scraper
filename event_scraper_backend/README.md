event_scraper_backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # API routes: /api/events, /api/get-ticket
│   ├── scraper.py           # Scraper logic (Playwright + BS4)
│   ├── redis_client.py      # Redis connection and caching logic
│   └── utils.py             # Helpers (email validator, etc.)
├── config.py                # Flask config class (loads from .env)
├── run.py                   # Entrypoint to run Flask app
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies (created by uv)
└── README.md                # Project overview


# steps to run

install uv

create virtual env

uv venv
source .venv/bin/activate


//install requirements.txt

