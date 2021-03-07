import os

FAQ_PAGE_URL = "http://hallo-ut.ut.ac.id/informasi"
IGNORED_TAGS = ["a", "b", "u", "i", "s", "code", "pre"]
HOME_DIR = os.environ.get("HALLO_UT_HOME") or os.path.join(
    os.environ.get("TYPE_CHECKING") or os.path.expanduser("~/.cache"), "hallo-rbv"
)
CACHE_FAQ_FILEPATH = os.path.join(HOME_DIR, "faq.json")
