from canonical_evidence import (
    CanonicalEvidence,
    CanonicalEvidenceItem,
    EvidenceSource,
    EvidenceType,
    _make_id,
    normalize_evidence,
)


# -- _make_id --


def test_make_id_format():
    assert _make_id("fact", 1) == "fact_0001"
    assert _make_id("svc", 42) == "svc_0042"
    assert _make_id("unknown", 9999) == "unknown_9999"


# -- CanonicalEvidenceItem --


def test_canonical_evidence_item_to_dict():
    item = CanonicalEvidenceItem(
        id="fact_0001",
        type=EvidenceType.VERIFIED_FACT,
        source=EvidenceSource.BUSINESS_ANALYSIS,
        category="company_name",
        claim="Company name: TestCo",
        raw_data={"field": "business_name", "value": "TestCo"},
        confidence=1.0,
        urls=["https://testco.com"],
    )
    d = item.to_dict()
    assert d["id"] == "fact_0001"
    assert d["type"] == "VERIFIED_FACT"
    assert d["source"] == "BUSINESS_ANALYSIS"
    assert d["urls"] == ["https://testco.com"]


def test_canonical_evidence_item_default_confidence():
    item = CanonicalEvidenceItem(
        id="x", type=EvidenceType.UNKNOWN, source=EvidenceSource.BOTH,
        category="c", claim="claim", raw_data={},
    )
    assert item.confidence == 1.0
    assert item.urls == []


# -- CanonicalEvidence --


def test_canonical_evidence_all_items_empty():
    ce = CanonicalEvidence()
    assert ce.all_items() == []


def test_canonical_evidence_all_items_populated():
    ce = CanonicalEvidence()
    ce.verified_business_facts.append(
        CanonicalEvidenceItem(
            id="f1", type=EvidenceType.VERIFIED_FACT, source=EvidenceSource.BUSINESS_ANALYSIS,
            category="name", claim="c", raw_data={},
        )
    )
    ce.seo_findings.append(
        CanonicalEvidenceItem(
            id="s1", type=EvidenceType.GROUNDED_FINDING, source=EvidenceSource.SEO_REPORT,
            category="seo", claim="c", raw_data={},
        )
    )
    assert len(ce.all_items()) == 2


def test_canonical_evidence_to_dict():
    ce = CanonicalEvidence()
    ce.verified_services.append(
        CanonicalEvidenceItem(
            id="svc1", type=EvidenceType.VERIFIED_FACT, source=EvidenceSource.BUSINESS_ANALYSIS,
            category="service", claim="c", raw_data={},
        )
    )
    d = ce.to_dict()
    assert len(d["verified_services"]) == 1
    assert d["verified_services"][0]["id"] == "svc1"
    assert d["unknown_information"] == []


def test_canonical_evidence_save(tmp_path):
    ce = CanonicalEvidence()
    ce.verified_business_facts.append(
        CanonicalEvidenceItem(
            id="f1", type=EvidenceType.VERIFIED_FACT, source=EvidenceSource.BUSINESS_ANALYSIS,
            category="name", claim="Company: X", raw_data={},
        )
    )
    path = str(tmp_path / "evidence.json")
    ce.save(path)
    import json
    with open(path) as f:
        data = json.load(f)
    assert len(data["verified_business_facts"]) == 1


# -- normalize_evidence --


def test_normalize_evidence_empty():
    ce = normalize_evidence({}, {})
    # Should still produce unknown_information items
    assert len(ce.unknown_information) == 10


def test_normalize_evidence_with_business_profile():
    seo_intel = {}
    biz_intel = {
        "business_profile": {
            "business_name": {"value": "TestCo"},
            "industry": {"value": "Dental"},
        },
        "location": "Amsterdam",
        "website": "https://testco.com",
        "service_analysis": {
            "services": [
                {
                    "name": "Implants",
                    "importance": "core",
                    "has_dedicated_page": False,
                    "confidence": 0.9,
                },
            ],
        },
    }
    ce = normalize_evidence(seo_intel, biz_intel)

    fact_names = [f.category for f in ce.verified_business_facts]
    assert "company_name" in fact_names
    assert "industry" in fact_names
    assert "website_url" in fact_names

    assert len(ce.verified_services) == 1
    assert ce.verified_services[0].raw_data["name"] == "Implants"


def test_normalize_evidence_core_service_without_page_creates_recommendation():
    seo_intel = {}
    biz_intel = {
        "business_profile": {},
        "service_analysis": {
            "services": [
                {
                    "name": "Root Canal",
                    "importance": "core",
                    "has_dedicated_page": False,
                    "confidence": 0.8,
                },
            ],
        },
    }
    ce = normalize_evidence(seo_intel, biz_intel)
    rec_pages = [p for p in ce.recommended_pages if "Root Canal" in p.claim]
    assert len(rec_pages) == 1
    assert rec_pages[0].type == EvidenceType.GROUNDED_RECOMMENDATION


def test_normalize_evidence_preservation_requirements_from_facts():
    seo_intel = {}
    biz_intel = {
        "business_profile": {
            "business_name": {"value": "Co"},
            "industry": {"value": "Tech"},
        },
        "location": "Berlin",
        "website": "https://co.com",
        "service_analysis": {
            "services": [
                {"name": "S1", "importance": "core", "has_dedicated_page": True, "confidence": 0.9},
            ],
        },
    }
    ce = normalize_evidence(seo_intel, biz_intel)
    pres_claims = [p.claim for p in ce.preservation_requirements]
    assert any("Company name" in c for c in pres_claims)
    assert any("Location" in c for c in pres_claims)
    assert any("Website" in c for c in pres_claims)


def test_normalize_evidence_seo_findings():
    seo_intel = {
        "overall_score": 65,
        "category_scores": {"On-Page SEO": 70},
        "technical_findings": [
            {"title": "Slow load", "type": "performance", "severity": "high", "url": "https://x.com", "category": "Technical"},
        ],
    }
    ce = normalize_evidence(seo_intel, {})
    seo_claims = [f.claim for f in ce.seo_findings]
    assert any("Overall SEO score: 65" in c for c in seo_claims)
    assert any("On-Page SEO" in c for c in seo_claims)
    assert any("Slow load" in c for c in seo_claims)


def test_normalize_evidence_unknown_information_always_present():
    ce = normalize_evidence({}, {})
    unknown_cats = [u.category for u in ce.unknown_information]
    assert "phone" in unknown_cats
    assert "email" in unknown_cats
    assert "pricing" in unknown_cats
    assert "traffic_stats" in unknown_cats
