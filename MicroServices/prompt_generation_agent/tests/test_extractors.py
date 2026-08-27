from unittest.mock import patch

from models import (
    BusinessIntelligence,
    BusinessProfile,
    CustomerAnalysis,
    IssueFinding,
    PageFinding,
    PromptType,
    Service,
    ServiceAnalysis,
    WebsiteIntelligence,
)
from extractors import classify_prompt_type, extract_business_intelligence


# -- classify_prompt_type --


def _make_seo(
    overall_score=70,
    critical_count=0,
    high_count=0,
    on_page=70,
    technical=70,
    content=70,
    page_findings_count=0,
    contact_no_meta=False,
):
    findings = []
    for i in range(critical_count):
        findings.append(IssueFinding(
            id=f"c{i}", category="Tech", type="t", severity="critical",
            url="https://x.com", title="t", description="d",
        ))
    for i in range(high_count):
        findings.append(IssueFinding(
            id=f"h{i}", category="Tech", type="t", severity="high",
            url="https://x.com", title="t", description="d",
        ))

    page_findings = []
    for i in range(page_findings_count):
        url = "https://x.com/contact" if (contact_no_meta and i == 0) else f"https://x.com/p{i}"
        pf = PageFinding(url=url)
        if contact_no_meta and i == 0:
            pf.url = "https://x.com/contact"
            pf.meta_description = ""
        page_findings.append(pf)

    return WebsiteIntelligence(
        website_url="https://x.com",
        website_exists=True,
        crawl_status="completed",
        pages_analyzed=10,
        overall_score=overall_score,
        category_scores={
            "On-Page SEO": on_page,
            "Technical SEO": technical,
            "Content Quality": content,
        },
        critical_findings=findings[:critical_count],
        high_findings=findings[critical_count:critical_count + high_count],
        page_findings=page_findings,
    )


def _make_biz(services=None, primary_segments=None):
    services = services or []
    segments = primary_segments or []
    return BusinessIntelligence(
        company_name="TestCo",
        website="https://testco.com",
        industry="Dental",
        location="Amsterdam",
        business_profile=BusinessProfile(),
        customer_analysis=CustomerAnalysis(segments=segments),
        service_analysis=ServiceAnalysis(services=services),
    )


def test_classify_website_poor():
    """Overall score < 50 → WEBSITE_REDESIGN."""
    seo = _make_seo(overall_score=30)
    biz = _make_biz()
    assert classify_prompt_type(seo, biz) == PromptType.WEBSITE_REDESIGN


def test_classify_website_poor_critical():
    """Critical count > 5 → WEBSITE_REDESIGN."""
    seo = _make_seo(overall_score=80, critical_count=6)
    biz = _make_biz()
    assert classify_prompt_type(seo, biz) == PromptType.WEBSITE_REDESIGN


def test_classify_seo_optimization():
    """Tech SEO issues without UX issues → SEO_OPTIMIZATION."""
    seo = _make_seo(overall_score=80, technical=40)
    biz = _make_biz()
    assert classify_prompt_type(seo, biz) == PromptType.SEO_OPTIMIZATION


def test_classify_seo_optimization_high_issues():
    """High count > 10 without UX issues → SEO_OPTIMIZATION."""
    seo = _make_seo(overall_score=80, high_count=11)
    biz = _make_biz()
    assert classify_prompt_type(seo, biz) == PromptType.SEO_OPTIMIZATION


def test_classify_ux_conversion():
    """UX issues without tech issues → UX_CONVERSION_OPTIMIZATION."""
    seo = _make_seo(overall_score=80, page_findings_count=11)
    biz = _make_biz()
    assert classify_prompt_type(seo, biz) == PromptType.UX_CONVERSION_OPTIMIZATION


def test_classify_ux_no_dedicated_page():
    """Service without dedicated page triggers UX path."""
    svc = Service(name="Implants", description="d", has_dedicated_page=False)
    seo = _make_seo(overall_score=80)
    biz = _make_biz(services=[svc])
    assert classify_prompt_type(seo, biz) == PromptType.UX_CONVERSION_OPTIMIZATION


def test_classify_combined():
    """Both tech and UX issues → COMBINED_WEBSITE_OPTIMIZATION."""
    seo = _make_seo(
        overall_score=80,
        technical=40,
        page_findings_count=11,
    )
    biz = _make_biz()
    assert classify_prompt_type(seo, biz) == PromptType.COMBINED_WEBSITE_OPTIMIZATION


def test_classify_no_issues():
    """Good scores, no issues → COMBINED_WEBSITE_OPTIMIZATION (else branch)."""
    seo = _make_seo(overall_score=80)
    biz = _make_biz()
    assert classify_prompt_type(seo, biz) == PromptType.COMBINED_WEBSITE_OPTIMIZATION


# -- extract_business_intelligence --


def test_extract_business_intelligence_minimal():
    biz_data = {
        "company_name": "TestCo",
        "website": "https://testco.com",
        "industry": "Dental",
        "location": "Amsterdam",
        "business_profile": {},
        "customer_analysis": {},
        "service_analysis": {},
    }
    result = extract_business_intelligence(biz_data, "/fake/report.json")
    assert result.company_name == "TestCo"
    assert result.website == "https://testco.com"
    assert result.service_analysis.services == []
    assert result.customer_analysis.segments == []


def test_extract_business_intelligence_with_services():
    biz_data = {
        "company_name": "Co",
        "website": "https://co.com",
        "industry": "Tech",
        "location": "Berlin",
        "business_profile": {},
        "customer_analysis": {},
        "service_analysis": {
            "services": [
                {"name": "Implants", "description": "Dental implants", "importance": "core"},
            ],
            "overall_visibility": "low",
            "key_gaps": ["no page for implants"],
        },
    }
    result = extract_business_intelligence(biz_data, "/fake/r.json")
    assert len(result.service_analysis.services) == 1
    assert result.service_analysis.services[0].name == "Implants"
    assert result.service_analysis.key_gaps == ["no page for implants"]


def test_extract_business_intelligence_with_segments():
    biz_data = {
        "company_name": "Co",
        "website": "https://co.com",
        "industry": "X",
        "location": "Y",
        "business_profile": {},
        "customer_analysis": {
            "segments": [
                {
                    "segment_name": "Anxious",
                    "description": "Dental fear patients",
                    "is_primary": True,
                    "why_it_matters": "High value",
                    "needs": ["sedation"],
                    "confidence": 0.85,
                },
            ],
        },
        "service_analysis": {},
    }
    result = extract_business_intelligence(biz_data, "/fake/r.json")
    assert len(result.customer_analysis.segments) == 1
    assert result.customer_analysis.primary_segments[0].segment_name == "Anxious"


def test_extract_business_intelligence_empty_profile_fields():
    """Missing nested 'value' keys should produce None/default."""
    biz_data = {
        "company_name": "",
        "website": "",
        "industry": "",
        "location": "",
        "business_profile": {
            "business_name": {},
            "industry": {},
        },
        "customer_analysis": {},
        "service_analysis": {},
    }
    result = extract_business_intelligence(biz_data, "/fake/r.json")
    assert result.business_profile.business_name is None
    assert result.business_profile.industry is None
