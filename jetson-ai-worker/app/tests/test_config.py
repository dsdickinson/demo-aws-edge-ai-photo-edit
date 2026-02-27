import tempfile
import yaml
from config import load_config

def test_load_config_reads_yaml():
    test_data = {
        "app": {"environment": "dev"},
        "aws": {"region": "us-east-1"}
    }

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        yaml.dump(test_data, tmp)
        tmp_path = tmp.name

    config = load_config(tmp_path)

    assert config["app"]["environment"] == "dev"
    assert config["aws"]["region"] == "us-east-1"
