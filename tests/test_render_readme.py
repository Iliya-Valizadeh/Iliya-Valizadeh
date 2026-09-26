"""Offline tests for scripts/render_readme.py. No network call, per ADR 0001/0002."""

from __future__ import annotations

import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from scripts import render_readme as rr

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
ROC_AUC_ROW = (
    "[ROC-AUC](docs/glossary.md#roc-auc) and [PR-AUC](docs/glossary.md#pr-auc) "
    "by model, with 95% intervals"
)


def real_config() -> list[rr.ProjectConfig]:
    return rr.load_config(ROOT / "projects.toml")


def real_template() -> str:
    return (ROOT / "README.template.md").read_text(encoding="utf-8")


# --- format_number -----------------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "decimals", "percent", "thousands", "expected"),
    [
        (Decimal("0.7687397655034531"), 3, False, False, "0.769"),
        (Decimal("0.7524034704425905"), 3, False, False, "0.752"),
        (Decimal("12"), 0, False, False, "12"),
        (Decimal("0.4589"), 0, True, False, "46%"),
        (Decimal("61502"), 0, False, True, "61,502"),
        (Decimal("-1.005"), 2, False, False, "-1.01"),
    ],
)
def test_format_number(
    value: Decimal, decimals: int, percent: bool, thousands: bool, expected: str
) -> None:
    config = rr.NumberConfig(
        id="x", path="x", row="x", decimals=decimals, percent=percent, thousands=thousands
    )
    assert rr.format_number(value, config) == expected


# --- source_matches ------------------------------------------------------------------


def test_source_matches_no_key() -> None:
    # By the time source_matches() runs, parse_claims_table() has already stripped
    # the backticks off the Source cell (see ClaimRow construction).
    assert rr.source_matches(
        "reports/metrics.json", "reports/metrics.json", "models.lightgbm.roc_auc"
    )


def test_source_matches_with_key_prefix() -> None:
    assert rr.source_matches(
        "reports/metrics.json#n_questions.verified", "reports/metrics.json", "n_questions.verified"
    )


def test_source_matches_wrong_file() -> None:
    assert not rr.source_matches("other/file.json", "reports/metrics.json", "a.b")


def test_source_matches_key_not_prefix() -> None:
    assert not rr.source_matches("reports/metrics.json#other.key", "reports/metrics.json", "a.b")


# --- value_cell_matches ---------------------------------------------------------------


def test_value_cell_matches_plain_number() -> None:
    config = rr.NumberConfig(id="x", path="x", row="x", decimals=0, percent=False, thousands=False)
    assert rr.value_cell_matches("12", "12", config)


def test_value_cell_matches_among_several_numbers() -> None:
    config = rr.NumberConfig(id="x", path="x", row="x", decimals=3, percent=False, thousands=False)
    value_cell = (
        "0.752 (0.745-0.759); 0.227 (0.216-0.238); 0.769 (0.762-0.775); 0.254 (0.242-0.265)"
    )
    assert rr.value_cell_matches(value_cell, "0.769", config)
    assert rr.value_cell_matches(value_cell, "0.752", config)


def test_value_cell_matches_missing_number() -> None:
    config = rr.NumberConfig(id="x", path="x", row="x", decimals=3, percent=False, thousands=False)
    assert not rr.value_cell_matches("0.500 (0.400-0.600)", "0.769", config)


def test_value_cell_matches_percent_form() -> None:
    config = rr.NumberConfig(id="x", path="x", row="x", decimals=0, percent=True, thousands=False)
    assert rr.value_cell_matches("58%", "58%", config)


def test_value_cell_matches_both_ends_of_a_hyphen_range() -> None:
    """A range such as 0.762-0.775 holds 0.762 and 0.775, as tools/claims_check.py reads it."""
    config = rr.NumberConfig(id="x", path="x", row="x", decimals=3, percent=False, thousands=False)
    assert rr.value_cell_matches("0.769 (0.762-0.775)", "0.762", config)
    assert rr.value_cell_matches("0.769 (0.762-0.775)", "0.775", config)
    assert not rr.value_cell_matches("0.769 (0.762-0.775)", "-0.775", config)


def test_value_cell_matches_a_real_negative_number() -> None:
    config = rr.NumberConfig(id="x", path="x", row="x", decimals=2, percent=False, thousands=False)
    assert rr.value_cell_matches("3; -0.20; 9", "-0.20", config)
    assert not rr.value_cell_matches("3; -0.20; 9", "0.20", config)


# --- json_value ------------------------------------------------------------------------


def test_json_value_nested_path() -> None:
    data = {"a": {"b": {"c": 0.5}}}
    assert rr.json_value(data, "a.b.c") == Decimal("0.5")


def test_json_value_missing_path() -> None:
    with pytest.raises(rr.RenderError):
        rr.json_value({"a": 1}, "a.b")


def test_json_value_not_a_number() -> None:
    with pytest.raises(rr.RenderError):
        rr.json_value({"a": "text"}, "a")


def test_json_value_rejects_bool() -> None:
    with pytest.raises(rr.RenderError):
        rr.json_value({"a": True}, "a")


# --- parse_claims_table ------------------------------------------------------------------


def test_parse_claims_table_reads_rows() -> None:
    text = (
        "# Claims\n\n"
        "| Claim | Value | Source | Command |\n"
        "|---|---|---|---|\n"
        "| Hand-checked questions | 12"
        " | `reports/metrics.json#n_questions.verified` | `make eval` |\n"
    )
    rows = rr.parse_claims_table(text)
    assert len(rows) == 1
    assert rows[0].claim == "Hand-checked questions"
    assert rows[0].value == "12"
    assert rows[0].source == "reports/metrics.json#n_questions.verified"


def test_parse_claims_table_ignores_non_claims_tables() -> None:
    text = "| A | B |\n|---|---|\n| 1 | 2 |\n"
    assert rr.parse_claims_table(text) == []


def test_parse_claims_table_on_real_fixtures() -> None:
    for repo in ("credit-risk-scorecard", "bank-filings-rag", "second-look"):
        text = (FIXTURES / repo / "CLAIMS.md").read_text(encoding="utf-8")
        rows = rr.parse_claims_table(text)
        assert rows, f"{repo}: expected at least one claim row"


# --- OfflineFetcher ------------------------------------------------------------------------


def test_offline_fetcher_reads_recorded_commits() -> None:
    fetcher = rr.OfflineFetcher(FIXTURES)
    assert fetcher.commit("credit-risk-scorecard") == "35a17fd2454ced157bdab00dc6b0301e67893240"
    assert fetcher.commit("bank-filings-rag") == "45246f8af21e907912d5611ccadb9158315255a3"


def test_offline_fetcher_unknown_repo() -> None:
    fetcher = rr.OfflineFetcher(FIXTURES)
    with pytest.raises(rr.RenderError):
        fetcher.commit("not-a-real-repo")


def test_offline_fetcher_reads_files() -> None:
    fetcher = rr.OfflineFetcher(FIXTURES)
    commit = fetcher.commit("credit-risk-scorecard")
    text = fetcher.read("credit-risk-scorecard", commit, "reports/metrics.json")
    assert json.loads(text)["models"]["lightgbm"]["roc_auc"]


def test_offline_fetcher_missing_file(tmp_path: Path) -> None:
    (tmp_path / "SOURCES.md").write_text("- `repo` at `abc1234`\n", encoding="utf-8")
    fetcher = rr.OfflineFetcher(tmp_path)
    with pytest.raises(rr.RenderError):
        fetcher.read("repo", "abc1234", "reports/metrics.json")


# --- render: end to end on the real files ------------------------------------------------


def test_render_matches_committed_readme() -> None:
    rendered, sources = rr.render(real_template(), real_config(), rr.OfflineFetcher(FIXTURES))
    committed = (ROOT / "README.md").read_text(encoding="utf-8")
    assert rendered == committed
    assert sources == {
        "credit-risk-scorecard": "35a17fd2454ced157bdab00dc6b0301e67893240",
        "bank-filings-rag": "45246f8af21e907912d5611ccadb9158315255a3",
    }


def test_render_skips_a_project_with_no_numbers() -> None:
    """ds-project-standard and .github have no metrics.json, so a repo entry with an
    empty number list must never be fetched (per ADR 0002: they get no number)."""

    class ExplodingForOneRepo(rr.OfflineFetcher):
        def commit(self, repo: str) -> str:
            if repo == "ds-project-standard":
                raise AssertionError("should never fetch a commit for a repo with no numbers")
            return super().commit(repo)

    no_numbers = rr.ProjectConfig(
        repo="ds-project-standard", metrics_file="reports/metrics.json", numbers=()
    )
    rendered, sources = rr.render(
        real_template(), [no_numbers, *real_config()], ExplodingForOneRepo(FIXTURES)
    )
    assert rendered == (ROOT / "README.md").read_text(encoding="utf-8")
    assert "ds-project-standard" not in sources


def test_render_is_idempotent() -> None:
    first, _ = rr.render(real_template(), real_config(), rr.OfflineFetcher(FIXTURES))
    second, _ = rr.render(real_template(), real_config(), rr.OfflineFetcher(FIXTURES))
    assert first == second


# --- render: error cases -----------------------------------------------------------------


def test_render_fails_on_unknown_placeholder() -> None:
    template = real_template() + "\n{{ nonsense.value }}\n"
    with pytest.raises(rr.RenderError, match="not in projects.toml"):
        rr.render(template, real_config(), rr.OfflineFetcher(FIXTURES))


def test_render_fails_on_unused_config_number() -> None:
    extra = rr.ProjectConfig(
        repo="second-look",
        metrics_file="reports/metrics.json",
        numbers=(
            rr.NumberConfig(
                id="second_look.recall",
                path="engine.recurring.recall.value",
                row="Recurring recall",
                decimals=4,
                percent=False,
                thousands=False,
            ),
        ),
    )
    with pytest.raises(rr.RenderError, match="never shows"):
        rr.render(real_template(), [*real_config(), extra], rr.OfflineFetcher(FIXTURES))


def test_render_fails_when_claims_row_missing() -> None:
    bad = rr.ProjectConfig(
        repo="bank-filings-rag",
        metrics_file="reports/metrics.json",
        numbers=(
            rr.NumberConfig(
                id="bank_filings_rag.n_verified",
                path="n_questions.verified",
                row="This row does not exist",
                decimals=0,
                percent=False,
                thousands=False,
            ),
        ),
    )
    config = [p for p in real_config() if p.repo != "bank-filings-rag"] + [bad]
    with pytest.raises(rr.RenderError, match="no row"):
        rr.render(real_template(), config, rr.OfflineFetcher(FIXTURES))


def test_render_fails_when_source_cell_does_not_cover_path() -> None:
    bad = rr.ProjectConfig(
        repo="credit-risk-scorecard",
        metrics_file="reports/metrics.json",
        numbers=(
            rr.NumberConfig(
                id="credit_risk_scorecard.lightgbm_roc_auc",
                path="models.lightgbm.roc_auc",
                row="Retrain trigger (lower bound of test interval)",
                decimals=3,
                percent=False,
                thousands=False,
            ),
            rr.NumberConfig(
                id="credit_risk_scorecard.logreg_roc_auc",
                path="models.logreg.roc_auc",
                row=ROC_AUC_ROW,
                decimals=3,
                percent=False,
                thousands=False,
            ),
        ),
    )
    config = [p for p in real_config() if p.repo != "credit-risk-scorecard"] + [bad]
    with pytest.raises(rr.RenderError, match="does not cover"):
        rr.render(real_template(), config, rr.OfflineFetcher(FIXTURES))


class _FakeFetcher(rr.Fetcher):
    """A fetcher over hand-built strings, for a case the real fixtures can't reach:
    a row whose Source cell really does cover the path, but whose Value cell
    doesn't hold the number the source file gives."""

    def __init__(self, metrics: dict[str, Any], claims_md: str) -> None:
        self._metrics = metrics
        self._claims_md = claims_md

    def commit(self, repo: str) -> str:
        return "fake0000"

    def read(self, repo: str, commit: str, file: str) -> str:
        return json.dumps(self._metrics) if file.endswith(".json") else self._claims_md


def test_render_fails_when_value_not_in_claims_cell() -> None:
    metrics = {"n": {"verified": 12}}
    claims_md = (
        "| Claim | Value | Source | Command |\n"
        "|---|---|---|---|\n"
        "| Some claim | 99 | `reports/metrics.json#n.verified` | `make eval` |\n"
    )
    config = [
        rr.ProjectConfig(
            repo="fake-repo",
            metrics_file="reports/metrics.json",
            numbers=(
                rr.NumberConfig(
                    id="fake_repo.n",
                    path="n.verified",
                    row="Some claim",
                    decimals=0,
                    percent=False,
                    thousands=False,
                ),
            ),
        )
    ]
    with pytest.raises(rr.RenderError, match="not in CLAIMS.md"):
        rr.render("{{ fake_repo.n }}", config, _FakeFetcher(metrics, claims_md))


# --- main() / CLI --------------------------------------------------------------------------


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "render_readme.py"), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_cli_offline_check_passes_with_no_upstream_change() -> None:
    result = run_cli("--offline", "--check")
    assert result.returncode == 0
    assert "already up to date" in result.stdout


def test_cli_writes_readme_only_when_changed(tmp_path: Path) -> None:
    """Run the renderer in a scratch copy of the repo; a second run writes nothing new."""
    import shutil

    work = tmp_path / "repo"
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"))
    (work / "README.md").unlink()

    first = subprocess.run(
        [sys.executable, "scripts/render_readme.py", "--offline"],
        cwd=work,
        capture_output=True,
        text=True,
    )
    assert first.returncode == 0
    assert "wrote README.md" in first.stdout
    written = (work / "README.md").read_text(encoding="utf-8")
    assert written == (ROOT / "README.md").read_text(encoding="utf-8")

    second = subprocess.run(
        [sys.executable, "scripts/render_readme.py", "--offline"],
        cwd=work,
        capture_output=True,
        text=True,
    )
    assert second.returncode == 0
    assert "already up to date, not written" in second.stdout


def test_cli_check_exits_nonzero_on_missing_readme(tmp_path: Path) -> None:
    import shutil

    work = tmp_path / "repo2"
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"))
    (work / "README.md").unlink()
    (work / "data" / "sources.json").unlink()

    result = subprocess.run(
        [sys.executable, "scripts/render_readme.py", "--offline", "--check"],
        cwd=work,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "would change" in result.stdout


def test_main_handles_render_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def boom(*_args: object, **_kwargs: object) -> tuple[str, dict[str, str]]:
        raise rr.RenderError("boom")

    monkeypatch.setattr(rr, "render", boom)
    assert rr.main(["--offline"]) == 1
    assert "render failed: boom" in capsys.readouterr().err
