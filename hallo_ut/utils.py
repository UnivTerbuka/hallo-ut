import json
import os

from typing import List, Optional

from . import Faq
from .constants import CACHE_FAQ_FILEPATH


def save_faqs(faqs: List["Faq"]):
    with open(CACHE_FAQ_FILEPATH, "w") as fp:
        json.dump(faqs, fp)


def load_faqs() -> Optional[List["Faq"]]:
    if not os.path.isfile(CACHE_FAQ_FILEPATH):
        return None
    results: List[dict] = list()
    with open(CACHE_FAQ_FILEPATH, "r") as fp:
        results = json.load(fp)
    return [Faq(**dat) for dat in results]
