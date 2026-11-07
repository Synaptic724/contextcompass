"""Source-policy and real board-conformance checks, not live hosting or agent tests."""

import re

import pytest

from conftest import PKG_ROOT
from package_manifest import apply_eol, detect_eol
from update_context_compass import conform_text

pytestmark = pytest.mark.unit


def normalized(path):
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def test_issue_board_allows_independent_comments_without_body_custody():
    text = normalized(PKG_ROOT / "issue_board.md")
    for phrase in (
        "append-only comments", "no body-writer permission", "editorial relay",
        "no comment-count cap", "no forced copying", "full-body", "overlapping",
        "latest-content", "owner-reserved body/closure custody", "readback",
        "denied operation", "material transitions",
    ):
        assert phrase in text, phrase
    assert "agents send findings through" not in text
    assert "for the primary writer to append" not in text


@pytest.mark.parametrize("skill", ["codex_mcp.md", "claude_internal_communication.md"])
def test_chat_transports_do_not_assign_worker_owned_boards_to_a_coordinator(skill):
    text = normalized(PKG_ROOT / "agent_onboarding/default/general/skills" / skill)
    for phrase in (
        "transport does not assign board custody", "owner-selected worker-owned policy",
        "their own assigned board, claim and route entries", "routinely repair",
        "without a coordinator gate", "explicit applicable owner delegation",
        "unknown ownership", "peer claim collisions", "unrelated authorized work",
        "owner-reserved body/closure custody", "platform denials",
    ):
        assert phrase in text, phrase
    assert "leave shared-board updates to the designated coordinator" not in text
    assert "full-body replacements" in text and "overlapping mutable fields" in text


@pytest.mark.parametrize("eol", [b"\n", b"\r\n"])
def test_upgrade_preserves_repaired_own_entry_peer_claim_and_history(tmp_path, eol):
    incoming = (PKG_ROOT / "issue_board.md").read_bytes()
    seed = incoming.decode("utf-8")
    own = ("| https://github.com/example/project/issues/1 | primary | owner | worker_1 | "
           "repaired route | topic | 2026-10-16T12:00:00Z |\n")
    peer = ("| https://github.com/example/project/issues/1 | review | owner | reviewer_1 | "
            "source review | topic | 2026-10-16T12:00:00Z |\n")
    history = ("| https://github.com/example/project/issues/2 | worker_2 | completed | accepted | "
               "2026-10-15T12:00:00Z |\n")
    notes = "Reserved body/closure custody: owner-selected editor.\n" + "\n".join(
        f"- Attributed evidence: https://github.com/example/project/issues/1#issuecomment-{n}"
        for n in range(1, 4)
    ) + "\n"
    current = re.sub(
        r"(<!-- BEGIN MANAGED: BoardContract -->\n).*?(<!-- END MANAGED: BoardContract -->)",
        r"\1Older managed contract.\n\2", seed, flags=re.S,
    )
    for region, body in (("active_claims", own + peer), ("released_claims", history), ("notes", notes)):
        current = current.replace(f"<!-- END USER-DEFINED: {region} -->",
                                  body + f"<!-- END USER-DEFINED: {region} -->")
    installed = tmp_path / "issue_board.md"
    before = current.encode("utf-8").replace(b"\n", eol)
    installed.write_bytes(before)
    merged, carried, orphaned = conform_text(incoming, installed)
    result = apply_eol(merged, detect_eol(installed))

    def regions(raw):
        return {m[1]: m[2] for m in re.finditer(
            rb"<!-- BEGIN USER-DEFINED: ([^\r\n]+?) -->\r?\n(.*?)<!-- END USER-DEFINED: \1 -->",
            raw, re.S,
        )}

    assert regions(result) == regions(before)
    assert set(carried) == {"active_claims", "released_claims", "notes"}
    assert orphaned == []
    assert "Older managed contract." not in result.decode("utf-8")
    assert own.strip() in result.decode("utf-8").replace("\r\n", "\n")
    assert peer.strip() in result.decode("utf-8").replace("\r\n", "\n")
