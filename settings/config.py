import tomli
from pathlib import Path


class Settings:
    def __init__(self):
        self.prompts = None
        self.config = {}
        self.load_config()

    def load_config(self):
        """Load configuration from TOML files"""
        config_path = Path(__file__).parent.parent / "settings"
        print(config_path)
        # Load main configuration
        with open(config_path / "configuration.toml", "rb") as f:
            self.config = tomli.load(f)

        # Load prompts
        with open(config_path / "prompts.toml", "rb") as f:
            self.prompts = tomli.load(f)

    def get(self, key, default=None):
        """Get a configuration value using dot notation"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default


_settings = None


def get_settings():
    """Returns singleton Settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings