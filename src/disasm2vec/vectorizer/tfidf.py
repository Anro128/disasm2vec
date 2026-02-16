from typing import List, Iterable, Optional, Tuple
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer


class Tfidf:
    """
    TF-IDF vectorizer for assembly instruction tokens.

    Input format
    ------------
    documents must be:
        List[List[str]]

    where:
        outer list  = files
        inner list  = instructions
    """

    def __init__(
        self,
        *,
        max_features: Optional[int] = None,
        ngram_range: Tuple[int, int] = (1, 2),
        min_df: int = 1,
        max_df: float | int = 1.0,
        use_idf: bool = True,
        norm: str | None = "l2",
    ):
        self.vectorizer = TfidfVectorizer(
            tokenizer=lambda x: x,
            preprocessor=lambda x: x,
            token_pattern=None,
            lowercase=False,
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df,
            use_idf=use_idf,
            norm=norm,
        )
        self._fitted = False

    # FIT
    def fit(self, documents: List[List[str]]):
        """
        Fit vocabulary + IDF from corpus.
        """
        self._validate_docs(documents)

        self.vectorizer.fit(documents)
        self._fitted = True
        return self

    # TRANSFORM
    def transform(self, documents: List[List[str]]):
        """
        Transform documents → vectors.
        """
        self._check_fitted()
        self._validate_docs(documents)

        X = self.vectorizer.transform(documents)
        return X

    # FIT + TRANSFORM
    def fit_transform(self, documents: List[List[str]]):
        """
        Fit then transform.
        """
        self._validate_docs(documents)

        X = self.vectorizer.fit_transform(documents)
        self._fitted = True
        return X

    # SINGLE DOC
    def transform_one(self, document: List[str]):
        """
        Transform single file → vector
        """
        self._check_fitted()
        return self.vectorizer.transform([document])

    # FEATURES
    def features(self) -> List[str]:
        self._check_fitted()
        return self.vectorizer.get_feature_names_out().tolist()

    # SAVE / LOAD
    def save(self, path: str | Path):
        self._check_fitted()

        with open(path, "wb") as f:
            pickle.dump(self.vectorizer, f)

    def load(self, path: str | Path):
        with open(path, "rb") as f:
            self.vectorizer = pickle.load(f)

        self._fitted = True
        return self
    
    def _validate_docs(self, docs):
        if not isinstance(docs, Iterable):
            raise TypeError("documents must be iterable")

        for d in docs:
            if not isinstance(d, list):
                raise TypeError(
                    "Each document must be List[str]"
                )

    def _check_fitted(self):
        if not self._fitted:
            raise RuntimeError(
                "Vectorizer not fitted. Call fit() first."
            )
