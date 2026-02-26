from ultralytics import YOLO
import logging

logger = logging.getLogger("inference")

class InferenceEngine:
    def __init__(self, config):
        self.model = YOLO(config["inference"]["model_path"])
        self.conf_threshold = config["inference"]["confidence_threshold"]

    def run(self, image_path):
        results = self.model(image_path)
        labels = set()

        for r in results:
            for box in r.boxes:
                if float(box.conf) >= self.conf_threshold:
                    labels.add(self.model.names[int(box.cls)])

        logger.info(f"Detected labels: {labels}")
        return list(labels)
