from prompts import (
    REQUIRED_SECTIONS,
    SYSTEM_PROMPT,
    build_repair_prompt,
    build_user_prompt,
)


def test_required_sections_count():
    assert len(REQUIRED_SECTIONS) == 25


def test_required_sections_starts_with_role():
    assert REQUIRED_SECTIONS[0] == "ROLE"


def test_required_sections_ends_with_final_instruction():
    assert REQUIRED_SECTIONS[-1] == "FINAL IMPLEMENTATION INSTRUCTION"


def test_system_prompt_mentions_25_sections():
    assert "25 SECTIONS" in SYSTEM_PROMPT


def test_system_prompt_contains_role_header():
    lines = SYSTEM_PROMPT.split("\n")
    role_lines = [l.strip() for l in lines if l.strip() == "ROLE"]
    assert len(role_lines) >= 1


def test_build_user_prompt_contains_context():
    result = build_user_prompt("Company: TestCo\nScore: 80")
    assert "Company: TestCo" in result
    assert "25-section" in result


def test_build_user_prompt_mentions_implementation():
    result = build_user_prompt("ctx")
    assert "implementation prompt" in result.lower()


def test_build_repair_prompt_contains_errors():
    result = build_repair_prompt(
        "original prompt",
        ["Error 1", "Error 2"],
        ["Warning 1"],
        {},
    )
    assert "original prompt" in result
    assert "Error 1" in result
    assert "Warning 1" in result
    assert "ERRORS TO FIX" in result
    assert "WARNINGS TO ADDRESS" in result


def test_build_repair_prompt_no_warnings_section_when_empty():
    result = build_repair_prompt("prompt", ["err1"], [], {})
    assert "WARNINGS TO ADDRESS" not in result


def test_build_repair_prompt_no_errors_section_when_empty():
    result = build_repair_prompt("prompt", [], ["warn1"], {})
    assert "ERRORS TO FIX" not in result
    assert "WARNINGS TO ADDRESS" in result
