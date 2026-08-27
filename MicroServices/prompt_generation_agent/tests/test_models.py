import pytest
from pydantic import ValidationError

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
    PagePlan,
    PromptType,
    RecommendedChanges,
    SeverityLevel,
    Service,
    ServiceAnalysis,
    StructuredOutput,
    WebsiteIntelligence,
)


# -- Enums --


def test_prompt_type_enum_values():
    assert set(PromptType) == {
        PromptType.WEBSITE_REDESIGN,
        PromptType.SEO_OPTIMIZATION,
        PromptType.UX_CONVERSION_OPTIMIZATION,
        PromptType.COMBINED_WEBSITE_OPTIMIZATION,
    }


def test_prompt_type_is_str_enum():
    assert PromptType.WEBSITE_REDESIGN == "WEBSITE_REDESIGN"
    assert isinstance(PromptType.WEBSITE_REDESIGN, str)


def test_severity_level_enum_values():
    assert SeverityLevel.CRITICAL == "critical"
    assert SeverityLevel.HIGH == "high"
    assert SeverityLevel.MEDIUM == "medium"
    assert SeverityLevel.LOW == "low"


# -- IssueFinding --


def test_issue_finding_required_fields():
    f = IssueFinding(
        id="1", category="SEO", type="missing_h1", severity="high",
        url="https://example.com", title="Missing H1", description="No h1 tag",
    )
    assert f.id == "1"
    assert f.evidence == {}


def test_issue_finding_missing_required_raises():
    with pytest.raises(ValidationError):
        IssueFinding(id="1")


# -- PageFinding --


def test_pageFinding_defaults():
    pf = PageFinding(url="https://example.com")
    assert pf.title == ""
    assert pf.meta_description == ""
    assert pf.h1 == ""
    assert pf.word_count == 0
    assert pf.status_code == 0
    assert pf.issues == []


# -- WebsiteIntelligence --


def test_website_intelligence_required_fields():
    wi = WebsiteIntelligence(
        website_url="https://example.com",
        website_exists=True,
        crawl_status="completed",
        pages_analyzed=10,
        overall_score=75,
    )
    assert wi.category_scores == {}
    assert wi.strengths == []
    assert wi.weaknesses == []


# -- BusinessProfile --


def test_business_profile_all_none_defaults():
    bp = BusinessProfile()
    assert bp.business_name is None
    assert bp.primary_offerings == []
    assert bp.evidence_ids == []


# -- CustomerSegment --


def test_customer_segment_required_fields():
    cs = CustomerSegment(
        segment_name="Anxious Patients",
        description="Dental phobia patients",
        is_primary=True,
        why_it_matters="High value",
    )
    assert cs.needs == []
    assert cs.confidence == 0.0


# -- CustomerAnalysis --


def test_customer_analysis_defaults():
    ca = CustomerAnalysis()
    assert ca.segments == []
    assert ca.primary_segments == []
    assert ca.journey == []


# -- Service --


def test_service_defaults():
    s = Service(name="Implants", description="Dental implants")
    assert s.category is None
    assert s.has_dedicated_page is False
    assert s.confidence == 0.0


# -- ServiceAnalysis --


def test_service_analysis_defaults():
    sa = ServiceAnalysis()
    assert sa.services == []
    assert sa.key_gaps == []


# -- BusinessProblem --


def test_business_problem_required_fields():
    bp = BusinessProblem(
        id="bp1", title="Low traffic", problem="Few visitors",
        description="SEO issues", type="seo", status="open",
    )
    assert bp.business_impact == 0
    assert bp.evidence_ids == []


# -- Opportunity --


def test_opportunity_required_fields():
    opp = Opportunity(
        problem_reference="bp1", opportunity="Improve SEO",
    )
    assert opp.recommended_services == []
    assert opp.priority == 0


# -- Evidence --


def test_evidence_fields():
    e = Evidence(
        id="ev1", claim="Test claim", source="seo",
        source_type="automated", supporting_text="text",
        confidence=0.9, relevance=0.8, timestamp="2024-01-01",
    )
    assert e.confidence == 0.9


# -- BusinessIntelligence --


def test_business_intelligence_construction():
    bi = BusinessIntelligence(
        company_name="TestCo",
        website="https://testco.com",
        industry="Dental",
        location="Amsterdam",
        business_profile=BusinessProfile(),
        customer_analysis=CustomerAnalysis(),
        service_analysis=ServiceAnalysis(),
    )
    assert bi.evidence == []
    assert bi.warnings == []


# -- PagePlan --


def test_page_plan_required_fields():
    pp = PagePlan(
        page_url="/home/", page_name="Home",
        current_problem="slow", required_improvement="speed up",
        business_reason="retain users", seo_reason="core web vitals",
        ux_reason="faster load", conversion_reason="lower bounce",
    )
    assert pp.page_url == "/home/"


# -- RecommendedChanges --


def test_recommended_changes_defaults():
    rc = RecommendedChanges()
    assert rc.seo == []
    assert rc.design == []


# -- StructuredOutput --


def test_structured_output_required_fields():
    so = StructuredOutput(
        company_name="Co",
        website="https://co.com",
        prompt_type="WEBSITE_REDESIGN",
        source_files={"seo": "/a.json", "biz": "/b.json"},
        recommended_changes=RecommendedChanges(),
    )
    assert so.generated_prompt == ""
    assert so.confidence == 0.0
    assert so.page_plan == []


def test_structured_output_missing_required_raises():
    with pytest.raises(ValidationError):
        StructuredOutput(company_name="Co")
