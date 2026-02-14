from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer


def vectorize(
    doc: List[str],
    *,
    max_features: int | None = None,
    ngram_range: Tuple[int, int] = (1, 1),
    min_df: int = 1,
    max_df: float | int = 1.0,
    use_idf: bool = True,
    norm: str | None = "l2"
):
    """
    Convert single instruction list → TF-IDF vector

    Parameters
    ----------
    doc : List[str]
        List of instruction tokens
    max_features : int | None
        Limit vocabulary size
    ngram_range : tuple
        Instruction sequence length
    min_df : int
        Ignore rare tokens
    max_df : float | int
        Ignore overly common tokens
    use_idf : bool
        Use IDF weighting
    norm : str | None
        'l1', 'l2', or None

    Returns
    -------
    vector : list[float]
    feature_names : list[str]
    """

    vectorizer = TfidfVectorizer(
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

    X = vectorizer.fit_transform([doc])

    return X.toarray()[0], vectorizer.get_feature_names_out().tolist()
