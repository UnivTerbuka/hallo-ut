import requests
from fuzzywuzzy import process
from typing import List

from . import Faq


class HalloUt:
    def __init__(self):
        self.faqs = Faq.fetch_faqs()
        self.faq_q_dict = dict(enumerate([faq.question for faq in self.faqs]))

    def __call__(self, query: str, limit: int = 10) -> List[Faq]:
        return self.faq(query, limit)

    def faq(self, query: str, limit: int = 10, score_cutoff: int = 60) -> List[Faq]:
        best_faq = process.extractBests(
            query, self.faq_q_dict, score_cutoff=score_cutoff, limit=10
        )
        return [self.faqs[z] for (x, y, z) in best_faq] if best_faq else []
