"""Application configuration."""

import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Server settings
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    log_level: str = "INFO"
    json_logging: bool = True

    # Paths
    project_root: Path = Path(__file__).parent.parent.parent.parent.resolve()
    outputs_dir: Path = project_root / "outputs"
    static_dir: Path | None = None

    # Download settings
    ffmpeg_location: str = "/usr/bin/ffmpeg"
    max_workers: int = 8

    # YouTube client settings
    youtube_timeout: int = 30

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    def __init__(self, **kwargs):
        """Initialize settings."""
        super().__init__(**kwargs)

        # Override debug from environment variable
        flask_debug = os.environ.get("FLASK_DEBUG")
        if flask_debug == "True":
            self.debug = True

        # Create outputs directory if it doesn't exist
        self.outputs_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
