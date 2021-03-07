import attr
import requests
from bs4 import BeautifulSoup, Tag
from typing import List

from .constants import FAQ_PAGE_URL


ignored_tags = ["a", "b", "u", "i", "s", "code", "pre"]


def parse_contents(contents: Tag) -> str:
    text = ""
    for content in contents:
        if isinstance(content, Tag):
            if content.name in ignored_tags:
                text += str(content)
            elif content.name == "ul":
                text += parse_contents(content)
            elif content.name == "br":
                text += "\n"
            elif content.name == "li":
                text += "● " + str(content) + "\n"
            else:
                text += str(content) + "\n"
            continue
        text += str(content)
    return text.strip()


@attr.dataclass(slots=True)
class Faq:
    question: str
    answer: str
    link: str

    def __str__(self) -> str:
        return f"Q: {self.question}\nA: {self.answer}\nSumber: {self.link}"

    @property
    def html(self) -> str:
        return (
            f'<b>{self.question}<b/>\n\n{self.answer}\n<a href="{self.link}">Sumber<a/>'
        )

    @classmethod
    def from_panel(cls, panel: Tag, url: str) -> "Faq":
        a = panel.find("a")
        body = panel.find("div", class_="panel-body")
        answer = parse_contents(body)
        return Faq(
            question=a.get_text(strip=True),
            answer=answer or str(body),
            link=url + a["href"],
        )

    @classmethod
    def fetch_faqs(cls, url: str = FAQ_PAGE_URL) -> List["Faq"]:
        results: List["Faq"] = list()
        res = requests.get(url)
        if not res.ok:
            pass
        soup = BeautifulSoup(res.text, "lxml").find(
            "div", {"id": "accordion2", "class": "panel-group"}
        )
        for panel in soup.findAll("div", class_=["panel", "panel-primary"]):
            try:
                results.append(cls.from_panel(panel, url))
            except Exception:
                pass
        return results
