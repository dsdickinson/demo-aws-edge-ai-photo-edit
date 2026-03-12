import yaml
import os

def load_config(path="/app/config.yaml"):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    # Allow environment override
    config["app"]["environment"] = os.getenv(
        "APP_ENV",
        config["app"]["environment"]
    )

    return config
