from abc import ABC, abstractmethod
from typing import List, Union
from pathlib import Path

class VectorizerBase(ABC):
    """
    Abstract base class for all vectorizers.
    """

    @abstractmethod
    def fit(self, documents: List[List[str]]):
        """
        Fit the vectorizer to the documents.
        """
        pass

    @abstractmethod
    def transform(self, documents: List[List[str]]):
        """
        Transform documents to vectors.
        """
        pass

    @abstractmethod
    def fit_transform(self, documents: List[List[str]]):
        """
        Fit to data, then transform it.
        """
        pass

    @abstractmethod
    def transform_one(self, document: List[str]):
        """
        Transform a single document to a vector.
        """
        pass
    
    @abstractmethod
    def save(self, path: Union[str, Path]):
        """
        Save the vectorizer to a file.
        """
        pass
    
    @abstractmethod
    def load(self, path: Union[str, Path]):
        """
        Load the vectorizer from a file.
        """
        pass
