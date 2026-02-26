import logging
from config import load_config
from logging_config import setup_logging
from inference import InferenceEngine
from worker import JetsonWorker

def main():
    config = load_config()
    setup_logging(config["app"]["log_level"])

    logger = logging.getLogger("app")
    logger.info("Starting Jetson Edge Worker")

    inference_engine = InferenceEngine(config)
    worker = JetsonWorker(config, inference_engine)

    worker.run()

if __name__ == "__main__":
    main()
