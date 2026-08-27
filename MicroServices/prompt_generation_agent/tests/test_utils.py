import json

from utils import (
    count_findings_by_severity,
    extract_domain_from_url,
    find_json_files,
    format_issue_summary,
    get_filename_stem,
    load_json_file,
    normalize_string,
    similarity,
    truncate_text,
)


# -- normalize_string --


def test_normalize_string_empty():
    assert normalize_string("") == ""


def test_normalize_string_simple():
    assert normalize_string("Hello World") == "helloworld"


def test_normalize_string_special_chars():
    assert normalize_string("foo-bar_baz.qux") == "foobarbazqux"


def test_normalize_string_mixed_separators():
    assert normalize_string("A B-C_D.E") == "abcde"


# -- similarity --


def test_similarity_identical():
    assert similarity("abc", "abc") == 1.0


def test_similarity_completely_different():
    assert similarity("aaa", "bbb") == 0.0


def test_similarity_partial():
    score = similarity("abc", "abcd")
    assert 0.0 < score < 1.0


# -- load_json_file --


def test_load_json_file_valid(tmp_path):
    p = tmp_path / "data.json"
    p.write_text(json.dumps({"key": "value"}), encoding="utf-8")
    data, error = load_json_file(str(p))
    assert data == {"key": "value"}
    assert error is None


def test_load_json_file_missing():
    data, error = load_json_file("/nonexistent/path.json")
    assert data is None
    assert "File not found" in error


def test_load_json_file_empty(tmp_path):
    p = tmp_path / "empty.json"
    p.write_text("", encoding="utf-8")
    data, error = load_json_file(str(p))
    assert data is None
    assert "File is empty" in error


def test_load_json_file_invalid_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("not json at all {{{", encoding="utf-8")
    data, error = load_json_file(str(p))
    assert data is None
    assert "Failed to parse" in error


def test_load_json_file_utf8_bom(tmp_path):
    p = tmp_path / "bom.json"
    p.write_bytes(b'\xef\xbb\xbf{"key": "bom"}')
    data, error = load_json_file(str(p))
    assert data == {"key": "bom"}
    assert error is None


# -- find_json_files --


def test_find_json_files_nonexistent_dir():
    assert find_json_files("/nonexistent/dir") == []


def test_find_json_files_with_files(tmp_path):
    (tmp_path / "a.json").write_text("{}")
    (tmp_path / "b.txt").write_text("text")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "c.json").write_text("{}")
    result = find_json_files(str(tmp_path))
    assert len(result) == 2
    assert all(f.endswith(".json") for f in result)


# -- extract_domain_from_url --


def test_extract_domain_from_url_with_www():
    assert extract_domain_from_url("https://www.example.com/path") == "example.com"


def test_extract_domain_from_url_without_www():
    assert extract_domain_from_url("https://example.com/path") == "example.com"


def test_extract_domain_from_url_http():
    assert extract_domain_from_url("http://test.org") == "test.org"


def test_extract_domain_from_url_empty():
    assert extract_domain_from_url("") == ""


def test_extract_domain_from_url_no_protocol():
    assert extract_domain_from_url("example.com/path") == ""


# -- get_filename_stem --


def test_get_filename_stem():
    assert get_filename_stem("/path/to/file.json") == "file"


def test_get_filename_stem_no_extension():
    assert get_filename_stem("myfile") == "myfile"


# -- truncate_text --


def test_truncate_text_short():
    assert truncate_text("hello", 10) == "hello"


def test_truncate_text_exact():
    assert truncate_text("hello", 5) == "hello"


def test_truncate_text_long():
    result = truncate_text("hello world", 5)
    assert result == "hello... [truncated]"


# -- format_issue_summary --


def test_format_issue_summary_empty():
    assert format_issue_summary([]) == "None"


def test_format_issue_summary_normal():
    findings = [
        {"severity": "high", "title": "Missing H1", "url": "https://example.com"},
    ]
    result = format_issue_summary(findings)
    assert "[HIGH]" in result
    assert "Missing H1" in result


def test_format_issue_summary_max_items():
    findings = [{"severity": "low", "title": f"Issue {i}", "url": ""} for i in range(15)]
    result = format_issue_summary(findings, max_items=10)
    assert "... and 5 more issues" in result


# -- count_findings_by_severity --


def test_count_findings_by_severity_empty():
    result = count_findings_by_severity([])
    assert result == {"critical": 0, "high": 0, "medium": 0, "low": 0}


def test_count_findings_by_severity_mixed():
    findings = [
        {"severity": "critical"},
        {"severity": "high"},
        {"severity": "high"},
        {"severity": "low"},
        {"severity": "unknown"},
    ]
    result = count_findings_by_severity(findings)
    assert result == {"critical": 1, "high": 2, "medium": 0, "low": 1}
