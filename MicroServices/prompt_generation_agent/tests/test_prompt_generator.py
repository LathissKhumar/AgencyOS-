from models import (
    BusinessIntelligence,
    BusinessProblem,
    BusinessProfile,
    CustomerAnalysis,
    CustomerSegment,
    Evidence,
    IssueFinding,
    Opportunity,
    PageFinding,
    PromptType,
    Service,
    ServiceAnalysis,
    WebsiteIntelligence,
)
from prompt_generator import (
    build_prompt_context,
    extract_clean_prompt,
    format_context_for_llm,
    normalize_service_name,
)


# -- normalize_service_name --


def test_normalize_service_name_simple():
    assert normalize_service_name("Dental Implants") == "dental-implants"


def test_normalize_service_name_special_chars():
    assert normalize_service_name("Root Canal & Therapy") == "root-canal-therapy"


def test_normalize_service_name_leading_trailing():
    assert normalize_service_name("  Implants  ") == "implants"


def test_normalize_service_name_single_word():
    assert normalize_service_name("Consultation") == "consultation"


# -- extract_clean_prompt --


def test_extract_clean_prompt_empty():
    assert extract_clean_prompt("") == ""


def test_extract_clean_prompt_no_role():
    assert extract_clean_prompt("Some random text without ROLE header.") == ""


def test_extract_clean_prompt_with_all_sections():
    lines = []
    sections = [
        "ROLE", "WEBSITE PURPOSE", "BUSINESS CONTEXT", "TARGET AUDIENCE",
        "WEBSITE GOALS", "BRAND DIRECTION", "SITE ARCHITECTURE", "NAVIGATION",
        "HOMEPAGE", "ABOUT PAGE", "SERVICE PAGES", "CONTACT PAGE",
        "UI DESIGN", "UX DESIGN", "CONTENT REQUIREMENTS", "SEO IMPLEMENTATION",
        "LOCAL SEO", "CONVERSION FLOW", "MOBILE EXPERIENCE", "TRUST ELEMENTS",
        "PRESERVATION RULES", "DO NOT INVENT", "SUCCESS CRITERIA",
        "FINAL IMPLEMENTATION INSTRUCTION",
    ]
    for s in sections:
        lines.append(s)
        lines.append(f"Content for {s.lower()}.")
    prompt = "\n".join(lines)
    result = extract_clean_prompt(prompt)
    assert result.startswith("ROLE\n")
    assert "FINAL IMPLEMENTATION INSTRUCTION" in result


def test_extract_clean_prompt_strips_thinking_before_role():
    thinking = "Hmm, let me think about this...\nStep 1: analyze\nStep 2: write\n\n"
    sections = "ROLE\nYou are a designer.\nFINAL IMPLEMENTATION INSTRUCTION\nDo the work."
    result = extract_clean_prompt(thinking + sections)
    assert result.startswith("ROLE\n")
    assert "Hmm, let me think" not in result


def test_extract_clean_prompt_finds_first_role():
    # Two ROLE occurrences — should use the first one
    prompt = "Blah\nROLE\nIntro content.\nFINAL IMPLEMENTATION INSTRUCTION\nDone.\nMore text\nROLE\nDuplicate."
    result = extract_clean_prompt(prompt)
    assert result.startswith("ROLE\n")


# -- format_context_for_llm --


def _minimal_context():
    return {
        "company_name": "TestCo",
        "website": "https://testco.com",
        "industry": "Dental",
        "location": "Amsterdam",
        "prompt_type": "WEBSITE_REDESIGN",
        "website_summary": {
            "url": "https://testco.com",
            "overall_score": 65,
            "category_scores": {"On-Page SEO": 70},
            "pages_analyzed": 15,
            "strengths": ["Good title tags"],
            "weaknesses": ["Missing H1"],
        },
        "business_summary": {
            "company_name": "TestCo",
            "industry": "Dental",
            "location": "Amsterdam",
            "primary_services": ["Implants"],
            "services_without_dedicated_pages": ["Implants"],
            "primary_customers": ["Anxious patients"],
            "customer_needs": ["sedation", "trust"],
            "business_score": 70,
        },
        "top_seo_issues": [
            {"type": "missing_h1", "title": "Missing H1 on homepage", "url": "https://testco.com/"},
        ],
        "important_pages": [
            {"url": "https://testco.com/", "title": "Home", "meta_description": "Welcome", "h1": "TestCo", "word_count": 500, "issues": ["missing_h1"]},
        ],
        "service_pages": [],
        "business_problems": [
            {"id": "bp1", "title": "Low traffic", "problem": "Few visitors", "description": "", "impact": 8, "urgency": 7, "affected_service": None, "affected_segment": None},
        ],
        "opportunities": [
            {"problem_reference": "bp1", "opportunity": "Improve SEO rankings", "recommended_services": ["SEO"], "expected_outcome": "More traffic", "priority": 1},
        ],
        "competitor_gaps": [],
        "evidence_ids": ["ev1"],
    }


def test_format_context_for_llm_contains_company():
    result = format_context_for_llm(_minimal_context())
    assert "TestCo" in result
    assert "Dental" in result
    assert "Amsterdam" in result


def test_format_context_for_llm_truncated_at_1800():
    ctx = _minimal_context()
    ctx["top_seo_issues"] = [
        {"type": "x", "title": "A" * 100, "url": "https://x.com"} for _ in range(50)
    ]
    result = format_context_for_llm(ctx)
    assert len(result) <= 1800


# -- build_prompt_context --


def _minimal_seo():
    return WebsiteIntelligence(
        website_url="https://testco.com",
        website_exists=True,
        crawl_status="completed",
        pages_analyzed=15,
        overall_score=65,
        category_scores={"On-Page SEO": 70},
        critical_findings=[],
        high_findings=[],
        important_pages=[],
        service_page_findings=[],
    )


def _minimal_biz():
    return BusinessIntelligence(
        company_name="TestCo",
        website="https://testco.com",
        industry="Dental",
        location="Amsterdam",
        business_profile=BusinessProfile(),
        customer_analysis=CustomerAnalysis(),
        service_analysis=ServiceAnalysis(),
    )


def test_build_prompt_context_returns_dict():
    ctx = build_prompt_context(_minimal_seo(), _minimal_biz(), PromptType.WEBSITE_REDESIGN)
    assert ctx["company_name"] == "TestCo"
    assert ctx["prompt_type"] == "WEBSITE_REDESIGN"
    assert "website_summary" in ctx
    assert "business_summary" in ctx


def test_build_prompt_context_services_without_pages():
    svc = Service(name="Implants", description="d", importance="core", has_dedicated_page=False)
    biz = _minimal_biz()
    biz.service_analysis.services = [svc]
    ctx = build_prompt_context(_minimal_seo(), biz, PromptType.SEO_OPTIMIZATION)
    assert "Implants" in ctx["business_summary"]["services_without_dedicated_pages"]


def test_build_prompt_context_primary_customer_needs():
    seg = CustomerSegment(
        segment_name="Anxious", description="d", is_primary=True,
        why_it_matters="m", needs=["sedation", "empathy"],
    )
    biz = _minimal_biz()
    biz.customer_analysis.segments = [seg]
    biz.customer_analysis.primary_segments = [seg]
    ctx = build_prompt_context(_minimal_seo(), biz, PromptType.UX_CONVERSION_OPTIMIZATION)
    assert "sedation" in ctx["business_summary"]["customer_needs"]
    assert "empathy" in ctx["business_summary"]["customer_needs"]


def test_build_prompt_context_top_seo_issues():
    seo = _minimal_seo()
    seo.critical_findings = [
        IssueFinding(id="c1", category="Tech", type="slow_load", severity="critical",
                     url="https://testco.com", title="Slow Load", description="3s LCP"),
    ]
    ctx = build_prompt_context(seo, _minimal_biz(), PromptType.WEBSITE_REDESIGN)
    assert len(ctx["top_seo_issues"]) == 1
    assert ctx["top_seo_issues"][0]["type"] == "slow_load"
