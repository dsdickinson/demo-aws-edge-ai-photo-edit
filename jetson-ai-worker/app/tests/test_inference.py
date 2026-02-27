from inference import InferenceEngine

class DummyBox:
    def __init__(self, cls, conf):
        self.cls = cls
        self.conf = conf

class DummyResult:
    def __init__(self):
        self.boxes = [
            DummyBox(0, 0.9),
            DummyBox(1, 0.3)
        ]

class DummyModel:
    names = {0: "heron", 1: "marsh"}

    def __call__(self, image_path):
        return [DummyResult()]

def test_inference_filters_by_confidence(monkeypatch):
    config = {
        "inference": {
            "model_path": "fake.pt",
            "confidence_threshold": 0.5
        }
    }

    engine = InferenceEngine.__new__(InferenceEngine)
    engine.model = DummyModel()
    engine.conf_threshold = 0.5

    labels = engine.run("fake.jpg")

    assert "heron" in labels
    assert "marsh" not in labels
