"""NIAPI CORS config."""
from litestar.config.cors import CORSConfig

from niapi.lib import settings

config = CORSConfig(allow_origins=settings.app.BACKEND_CORS_ORIGINS)
"""Default CORS config."""
