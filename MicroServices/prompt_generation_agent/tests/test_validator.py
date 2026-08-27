from models import RecommendedChanges, StructuredOutput
from validator import PromptValidator


# -- helpers --


SECTIONS_24 = [
    "ROLE", "WEBSITE PURPOSE", "BUSINESS CONTEXT", "TARGET AUDIENCE",
    "WEBSITE GOALS", "BRAND DIRECTION", "SITE ARCHITECTURE", "NAVIGATION",
    "HOMEPAGE", "ABOUT PAGE", "SERVICE PAGES", "CONTACT PAGE",
    "UI DESIGN", "UX DESIGN", "CONTENT REQUIREMENTS", "SEO IMPLEMENTATION",
    "LOCAL SEO", "CONVERSION FLOW", "MOBILE EXPERIENCE", "TRUST ELEMENTS",
    "PRESERVATION RULES", "DO NOT INVENT", "SUCCESS CRITERIA",
    "FINAL IMPLEMENTATION INSTRUCTION",
]

# SUSPECTED BUG: The SYSTEM_PROMPT and validator both list 24 section names,
# but the validator checks for exactly 25. This means a prompt generated from
# the SYSTEM_PROMPT will ALWAYS fail _check_exact_25_sections.
# We pin this by counting the list length.
assert len(SECTIONS_24) == 24, "Validator's section list has 24 items but checks for 25"


def _build_valid_prompt(minimal=False):
    """Build a prompt string with all 24 section headers + filler content."""
    parts = []
    for section in SECTIONS_24:
        parts.append(section)
        if not minimal:
            parts.append("This is placeholder content for the section. " * 10)
    return "\n".join(parts)


def _build_valid_output(prompt=None):
    if prompt is None:
        prompt = _build_valid_prompt()
    return StructuredOutput(
        company_name="Atlas Kliniek",
        website="https://atlaskliniek.nl",
        prompt_type="WEBSITE_REDESIGN",
        source_files={"seo": "/seo.json", "biz": "/biz.json"},
        recommended_changes=RecommendedChanges(),
        generated_prompt=prompt,
        business_summary={"company_name": "Atlas Kliniek", "primary_services": ["Implants"]},
        preservation_rules=[
            "Company name: Atlas Kliniek",
            "Location: Amsterdam",
            "Contact information from existing website",
            "Verified services: Implants",
        ],
        success_criteria=[
            "Address identified on-page SEO weaknesses",
            "Resolve identified high-severity technical issues",
            "Improve performance issues",
        ],
    )


def _valid_context():
    return {
        "top_seo_issues": [
            {"type": "missing_h1", "title": "Missing H1 on homepage", "url": "https://atlaskliniek.nl/"},
        ],
        "important_pages": [{"url": "https://atlaskliniek.nl/"}],
        "service_pages": [],
    }


# -- company name checks --


def test_validator_rejects_missing_company_name():
    out = _build_valid_output()
    out.company_name = ""
    v = PromptValidator()
    is_valid, errors, _ = v.validate(out, _valid_context())
    assert not is_valid
    assert any("Company name" in e for e in errors)


def test_validator_rejects_whitespace_company_name():
    out = _build_valid_output()
    out.company_name = "   "
    v = PromptValidator()
    is_valid, errors, _ = v.validate(out, _valid_context())
    assert not is_valid
    assert any("Company name" in e for e in errors)


# -- website checks --


def test_validator_rejects_missing_website():
    out = _build_valid_output()
    out.website = ""
    v = PromptValidator()
    is_valid, errors, warnings = v.validate(out, _valid_context())
    assert not is_valid
    assert any("Website URL" in e for e in errors)


def test_validator_warns_website_no_protocol():
    out = _build_valid_output()
    out.website = "atlaskliniek.nl"
    v = PromptValidator()
    _, errors, warnings = v.validate(out, _valid_context())
    assert any("protocol" in w for w in warnings)


# -- prompt type checks --


def test_validator_rejects_invalid_prompt_type():
    out = _build_valid_output()
    out.prompt_type = "INVALID_TYPE"
    v = PromptValidator()
    is_valid, errors, _ = v.validate(out, _valid_context())
    assert not is_valid
    assert any("Invalid or missing prompt type" in e for e in errors)


# -- existing website acknowledgment --


def test_validator_warns_no_existing_website_acknowledgment():
    out = _build_valid_output(prompt="ROLE\nSome content without the phrase.\n" + "\n".join(SECTIONS_24[1:]))
    v = PromptValidator()
    _, _, warnings = v.validate(out, _valid_context())
    assert any("existing website" in w.lower() for w in warnings)


# -- business context --


def test_validator_warns_missing_business_services():
    out = _build_valid_output()
    out.business_summary = {"company_name": "Co"}
    v = PromptValidator()
    _, _, warnings = v.validate(out, _valid_context())
    assert any("primary services" in w.lower() for w in warnings)


def test_validator_rejects_missing_business_context_company():
    out = _build_valid_output()
    out.business_summary = {}
    v = PromptValidator()
    _, errors, _ = v.validate(out, _valid_context())
    assert any("Business context missing company name" in e for e in errors)


# -- SEO issues representation --


def test_validator_warns_no_seo_issues_in_context():
    out = _build_valid_output()
    v = PromptValidator()
    _, _, warnings = v.validate(out, {"top_seo_issues": []})
    assert any("No SEO issues" in w for w in warnings)


# -- business problems --


def test_validator_warns_no_business_problems():
    out = _build_valid_output()
    out.identified_problems = []
    v = PromptValidator()
    _, _, warnings = v.validate(out, _valid_context())
    assert any("No business problems" in w for w in warnings)


# -- opportunities --


def test_validator_warns_no_opportunities():
    out = _build_valid_output()
    out.business_opportunities = []
    v = PromptValidator()
    _, _, warnings = v.validate(out, _valid_context())
    assert any("No business opportunities" in w for w in warnings)


# -- preservation rules --


def test_validator_warns_insufficient_preservation_rules():
    out = _build_valid_output()
    out.preservation_rules = ["Only one rule"]
    v = PromptValidator()
    _, _, warnings = v.validate(out, _valid_context())
    assert any("Preservation rules" in w for w in warnings)


# -- success criteria --


def test_validator_warns_insufficient_success_criteria():
    out = _build_valid_output()
    out.success_criteria = ["Just one"]
    v = PromptValidator()
    _, _, warnings = v.validate(out, _valid_context())
    assert any("Success criteria" in w for w in warnings)


def test_validator_warns_success_criteria_not_measurable():
    out = _build_valid_output()
    out.success_criteria = ["Rule one", "Rule two", "Rule three"]
    v = PromptValidator()
    _, _, warnings = v.validate(out, _valid_context())
    assert any("measurable" in w for w in warnings)


# -- prompt length --


def test_validator_warns_prompt_too_short():
    out = _build_valid_output(prompt="ROLE\nShort prompt.")
    v = PromptValidator()
    _, _, warnings = v.validate(out, _valid_context())
    assert any("too short" in w.lower() or "too brief" in w.lower() for w in warnings)


# -- 25-section check (SUSPECTED BUG) --


def test_validator_exacts_25_sections_rejects_24():
    """The validator expects 25 sections but the SYSTEM_PROMPT only lists 24.
    A correctly-generated prompt with all 24 sections will be rejected."""
    prompt = _build_valid_prompt()
    out = _build_valid_output(prompt=prompt)
    v = PromptValidator()
    _, errors, _ = v.validate(out, _valid_context())
    assert any("24 sections" in e and "expected exactly 25" in e for e in errors), (
        f"Expected section count error but got: {errors}"
    )


# -- forbidden build-from-scratch phrases --


def test_validator_warns_build_from_scratch_in_prompt():
    prompt = _build_valid_prompt().replace(
        "FINAL IMPLEMENTATION INSTRUCTION",
        "build from scratch\nFINAL IMPLEMENTATION INSTRUCTION",
    )
    out = _build_valid_output(prompt=prompt)
    v = PromptValidator()
    _, _, warnings = v.validate(out, _valid_context())
    assert any("build from scratch" in w.lower() for w in warnings)
