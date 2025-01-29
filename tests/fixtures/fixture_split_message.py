import pytest


@pytest.fixture
def sample_html_no_split():
    """Fixture for simple HTML content that does not require splitting."""
    return "<p>Basic HTML (No Splitting Required)</p>"


@pytest.fixture
def sample_html_long_text():
    """Fixture for long plain text wrapped in HTML."""
    return "<p>" + "A" * 5000 + "</p>"


@pytest.fixture
def sample_html_edge_case_text():
    """Fixture where length text equal fragment max length."""
    return "<p>" + "A" * 4089 + "</p>"


@pytest.fixture
def sample_html_nested_tags_source_result():
    """Fixture for HTML with nested tags with lenght 4097."""
    source = "<p><b>Hello, <i>world</i></b> " + "A" * 4063 + "</p>"
    result = ["<p><b>Hello, <i>world</i></b></p>", "<p> " + "A" * 4063 + "</p>"]
    return source, result
