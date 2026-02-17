import os

from .base import VectorizerBase
from .tfidf import Tfidf

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_CURRENT_DIR)))
DEFAULT_MODEL_PATH = os.path.join(_PROJECT_ROOT, "models", "base_tfidf_asm.pkl")


def get_vectorizer(model_type: str = "tfidf", **kwargs) -> VectorizerBase:
    """
    Factory function to get a vectorizer instance.
    """
    if model_type == "tfidf":
        return Tfidf(**kwargs)
    else:
        raise ValueError(f"Unknown vectorizer type: {model_type}")

def load_vectorizer(path: str = DEFAULT_MODEL_PATH, model_type: str = "tfidf") -> VectorizerBase:
    """
    Load a vectorizer from a file.
    """
    if model_type == "tfidf":
        return Tfidf().load(path)
    else:
        raise ValueError(f"Unknown vectorizer type: {model_type}")
