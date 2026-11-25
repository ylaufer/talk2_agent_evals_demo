"""Small, framework-neutral agent evaluation example."""
import os

# Live mode model. Override without editing code: HF_MODEL_ID=<model id>
DEFAULT_MODEL_ID = "Qwen/Qwen3-Next-80B-A3B-Instruct"


def live_model_id() -> str:
    return os.getenv("HF_MODEL_ID") or DEFAULT_MODEL_ID
