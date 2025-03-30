import json
from pathlib import Path

DATA_DIR = Path("data")
DB_FILE = DATA_DIR / "links.db"


class LinkStore:
    def __init__(self) -> None:
        self._links: dict[str, str] = {}
        self._load()

    def __getitem__(self, link_id: str) -> str:
        return self._links[link_id]

    def __setitem__(self, link_id: str, url: str) -> None:
        self._links[link_id] = url
        self._save()

    def _save(self) -> None:
        json_repr = json.dumps(
            self._links,
            separators=(",", ":"),
        )
        DB_FILE.write_text(json_repr)

    def _load(self) -> None:
        if DB_FILE.is_dir():
            msg = f"{DB_FILE} exists and is a directory"
            raise RuntimeError(msg)

        if not DB_FILE.exists():
            DATA_DIR.mkdir(exist_ok=True)
            DB_FILE.touch()

        text = DB_FILE.read_text()
        if not text or text.isspace():
            DB_FILE.write_text("{}")
        else:
            self._links = json.loads(text)
