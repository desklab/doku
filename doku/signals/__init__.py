__all__ = ["signals", "model_created", "model_updated"]

from blinker import Namespace


signals = Namespace()

model_created = signals.signal("model-created")
model_updated = signals.signal("model-updated")
