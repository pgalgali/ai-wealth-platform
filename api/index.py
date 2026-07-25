import sys
from pathlib import Path

from fastapi import FastAPI

backend_path = Path(__file__).resolve().parents[1] / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app as backend_app  # noqa: E402

app = FastAPI(title="Astra Wealth Vercel API")
app.mount("/api", backend_app)
