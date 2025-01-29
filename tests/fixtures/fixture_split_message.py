import pytest


@pytest.fixture
def sample_html_no_split():
    """Fixture for simple HTML content that does not require splitting."""
    return "<p>Basic HTML (No Splitting Required)</p>"


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


@pytest.fixture
def sample_html_multiple_splits():
    """Fixture for HTML content that will require multiple splits."""
    return ("<p>" + "A" * 93 + "</p>") * 3


@pytest.fixture
def sample_html_long_single_tag():
    """Fixture for a single long tag that exceeds max_len."""
    return "<p>" + "A" * 5000 + "</p>"


@pytest.fixture
def sample_html_split_at_block_tag():
    """Fixture for HTML that should split at a tag boundary."""
    return "<p>Text</p><b>" + "B" * 393 + "</b><i>" + "C" * 393 + "</i>"


@pytest.fixture
def sample_html_with_special_chars_list():
    """Fixture for HTML content with special characters."""
    return ["<p>&lt;test&gt; &amp;</p>", "<p>others\t\n</p>"]
