import json

from report_discovery import (
    MatchResult,
    load_business_report_metadata,
    load_seo_report_metadata,
    score_business_match,
    score_seo_match,
    select_best_match,
    validate_website_exists,
)


# -- MatchResult --


def test_match_result_attributes():
    mr = MatchResult(filepath="/a.json", score=0.8, match_signals={"x": 1}, json_data={"k": "v"})
    assert mr.filepath == "/a.json"
    assert mr.score == 0.8


# -- load_seo_report_metadata --


def test_load_seo_report_metadata_valid(tmp_path):
    report = {
        "url": "https://example.com",
        "base_url": "https://example.com",
        "status": "completed",
        "raw_crawl_data": {"summary": {"total_pages_crawled": 25}},
    }
    p = tmp_path / "report.json"
    p.write_text(json.dumps(report))
    meta = load_seo_report_metadata(str(p))
    assert meta["domain_name"] == "example.com"
    assert meta["crawl_status"] == "completed"
    assert meta["pages_crawled"] == 25


def test_load_seo_report_metadata_missing_file():
    meta = load_seo_report_metadata("/nonexistent.json")
    assert meta == {}


def test_load_seo_report_metadata_not_dict(tmp_path):
    p = tmp_path / "list.json"
    p.write_text("[]")
    meta = load_seo_report_metadata(str(p))
    assert meta == {}


# -- load_business_report_metadata --


def test_load_business_report_metadata_valid(tmp_path):
    report = {
        "company_name": "TestCo",
        "website": "https://testco.com",
        "industry": "Dental",
        "location": "Amsterdam",
    }
    p = tmp_path / "biz.json"
    p.write_text(json.dumps(report))
    meta = load_business_report_metadata(str(p))
    assert meta["company_name"] == "TestCo"
    assert meta["domain_name"] == "testco.com"


def test_load_business_report_metadata_missing_file():
    assert load_business_report_metadata("/nonexistent.json") == {}


# -- validate_website_exists --


def test_validate_website_exists_true():
    data = {
        "status": "completed",
        "url": "https://example.com",
        "raw_crawl_data": {"summary": {"total_pages_crawled": 10}},
    }
    assert validate_website_exists(data) is True


def test_validate_website_exists_status_not_completed():
    data = {
        "status": "failed",
        "url": "https://example.com",
        "raw_crawl_data": {"summary": {"total_pages_crawled": 10}},
    }
    assert validate_website_exists(data) is False


def test_validate_website_exists_no_pages():
    data = {
        "status": "completed",
        "url": "https://example.com",
        "raw_crawl_data": {"summary": {"total_pages_crawled": 0}},
    }
    assert validate_website_exists(data) is False


def test_validate_website_exists_no_url():
    data = {
        "status": "completed",
        "raw_crawl_data": {"summary": {"total_pages_crawled": 10}},
    }
    assert validate_website_exists(data) is False


# -- score_seo_match --


def test_score_seo_match_exact_filename():
    meta = {"domain_name": "example.com", "crawl_status": "completed", "pages_crawled": 20}
    score, signals = score_seo_match("Example", "example", "/path/example_report.json", meta)
    assert score > 0.5
    assert signals["crawl_completed"] is True


def test_score_seo_match_no_crawl():
    meta = {"domain_name": "other.com", "crawl_status": "failed", "pages_crawled": 0}
    score, signals = score_seo_match("Example", "example", "/path/other.json", meta)
    assert signals["crawl_completed"] is False
    # When pages_crawled == 0, the "has_pages" key is never set in signals
    assert "has_pages" not in signals


# -- score_business_match --


def test_score_business_match_exact():
    meta = {"company_name": "Example Corp", "domain_name": "example.com", "industry": "Dental"}
    score, signals = score_business_match("Example Corp", "examplecorp", "/path/example.json", meta)
    assert score > 0.3
    assert signals.get("dental_industry") is True


def test_score_business_match_no_dental():
    meta = {"company_name": "TechCo", "domain_name": "techco.com", "industry": "Software"}
    _, signals = score_business_match("TechCo", "techco", "/path/tech.json", meta)
    assert "dental_industry" not in signals


# -- select_best_match --


def test_select_best_match_empty():
    assert select_best_match([], "SEO", "Co") is None


def test_select_best_match_single():
    mr = MatchResult(filepath="/a.json", score=0.9, match_signals={}, json_data={})
    result = select_best_match([mr], "SEO", "Co")
    assert result is mr


def test_select_best_match_returns_first():
    # select_best_match always returns candidates[0] — caller must pre-sort
    a = MatchResult(filepath="/a.json", score=0.3, match_signals={}, json_data={})
    b = MatchResult(filepath="/b.json", score=0.9, match_signals={}, json_data={})
    result = select_best_match([a, b], "SEO", "Co")
    assert result is a  # pinned: always first element
