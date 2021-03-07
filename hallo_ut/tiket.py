import attr
import requests
from bs4 import BeautifulSoup, Tag
from typing import List

from .constants import STATUS_TIKET_URL


def status_from_page_top(section: Tag) -> bool:
    span: Tag = section.find("span")
    return "OPEN" in span.getText()


@attr.dataclass(slots=True)
class Tiket:
    status: bool
    judul: str
    nama: str
    email: str
    topik: str
    nomer: str
    pesan: str

    @classmethod
    def from_noticket(cls, noticket: str) -> "Tiket":
        params = {"noticket": noticket}
        res = requests.get(STATUS_TIKET_URL, params=params)
        if not res.ok or not res.text or "Tiket Tidak Ditemukan" in res.text:
            raise ValueError("Tiket tidak ditemukan atau Hallo-ut tidak bisa dihubungi")
        soup = BeautifulSoup(res.text, "html.parser")
        status = status_from_page_top(soup.find("section", class_="page-top"))
        return cls.from_tbody(
            tbody=soup.find("tbody"),
            status=status,
        )

    @classmethod
    def from_tbody(cls, tbody: Tag, status: bool) -> "Tiket":
        judul, nama, email, topik, nomer, pesan = "", "", "", "", "", ""
        nama = tbody.contents[0].contents[2].getText()
        judul = tbody.contents[0].contents[6].getText()
        email = tbody.contents[1].contents[2].getText()
        topik = tbody.contents[1].contents[6].getText()
        nomer = tbody.contents[2].contents[2].getText()
        pesan = tbody.contents[2].contents[6]
        return cls(
            status=status,
            judul=judul,
            nama=nama,
            email=email,
            topik=topik,
            nomer=nomer,
            pesan=pesan,
        )
