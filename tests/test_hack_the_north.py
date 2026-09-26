"""The Hack the North guard.

Per docs/decisions/0004-checks-and-the-hack-the-north-guard.md: the "Also" block
(the fixture's lines 39 to 45, `git show fe5d040:README.md`) must never change,
move or be reformatted, in README.md, in README.template.md, or in a fresh render.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "readme_fe5d040.md"

FIXTURE_SHA256 = "e3d9f5b99329e30eb93087f673535aa4288cd4421dafa75d7a067a5f54f64603"
LINE_41_SHA256 = "43601ec39830bc17c221247c1f9f440528cb226b6ebd724b5723f86c4bcfbf22"
ALSO_BLOCK_SHA256 = "ee0af9367052ab40a4575f4c77727eb007b4eec5e3de25dc25027805f3dd9bf7"
HACK_RE = re.compile(r"hack\W*the\W*north", re.IGNORECASE)


def _fixture_bytes() -> bytes:
    data = FIXTURE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == FIXTURE_SHA256, (
        "tests/fixtures/readme_fe5d040.md has been edited"
    )
    return data


def _line_41(data: bytes) -> str:
    return data.decode("utf-8").splitlines()[40]


def _also_block(data: bytes) -> str:
    lines = data.decode("utf-8").splitlines()
    return "\n".join(lines[38:45]) + "\n"


def test_fixture_matches_fe5d040() -> None:
    _fixture_bytes()


def test_line_41_hash() -> None:
    line = _line_41(_fixture_bytes())
    assert hashlib.sha256(line.encode("utf-8")).hexdigest() == LINE_41_SHA256


def test_also_block_hash() -> None:
    block = _also_block(_fixture_bytes())
    assert hashlib.sha256(block.encode("utf-8")).hexdigest() == ALSO_BLOCK_SHA256


def _check_file(text: str, label: str) -> None:
    data = text.encode("utf-8")
    assert b"\r" not in data, f"{label}: has a carriage return"

    line41 = _line_41(_fixture_bytes())
    assert text.count(line41) == 1, f"{label}: the Hack the North line does not appear exactly once"

    block = _also_block(_fixture_bytes())
    assert text.count(block) == 1, f"{label}: the Also block does not appear exactly once"
    assert text.endswith(block), f"{label}: the Also block is not the last thing in the file"

    matches = HACK_RE.findall(text)
    assert len(matches) == 1, f"{label}: 'hack the north' matches {len(matches)} time(s), want 1"


def test_readme_md() -> None:
    _check_file((ROOT / "README.md").read_text(encoding="utf-8"), "README.md")


def test_readme_template() -> None:
    _check_file((ROOT / "README.template.md").read_text(encoding="utf-8"), "README.template.md")


def test_fresh_offline_render_matches_committed_readme() -> None:
    """A render with no upstream changes must reproduce README.md byte for byte."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "render_readme.py"), "--offline", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_hack_the_north_not_in_config_or_data() -> None:
    """Nothing the renderer reads or writes may add a second mention."""
    projects_toml = ROOT / "projects.toml"
    assert not HACK_RE.search(projects_toml.read_text(encoding="utf-8"))
    data_dir = ROOT / "data"
    if data_dir.is_dir():
        for path in data_dir.rglob("*"):
            if path.is_file():
                assert not HACK_RE.search(path.read_text(encoding="utf-8", errors="ignore"))
