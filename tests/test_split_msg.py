import pytest

from split_msg import split_message


def test_split_message_no_split(sample_html_no_split):
    """Test case for HTML content that does not require splitting."""
    fragments = list(split_message(sample_html_no_split, max_len=50))
    assert len(fragments) == 1, f"Expected 1 fragment, returned {len(fragments)}."
    assert (
        fragments[0] == sample_html_no_split
    ), "Fragment 0 does not match the original HTML."


def test_split_message_long_plain_text(sample_html_long_text):
    """Test case for splitting long plain text content."""
    fragments = list(split_message(sample_html_long_text, max_len=4096))
    assert len(fragments) == 2, f"Expected 2 fragment, returned {len(fragments)}."
    assert all(
        len(frag) <= 4096 for frag in fragments
    ), "One of the fragments is longer than the maximum length."
    assert fragments[0].startswith("<p>") and fragments[0].endswith(
        "</p>"
    ), "Fragment 0 must start and end with <p> tags."
    assert fragments[1].startswith("<p>") and fragments[1].endswith(
        "</p>"
    ), "Fragment 1 must start and end with <p> tags."
    assert (
        fragments[0] == "<p>" + "A" * 4089 + "</p>"
    ), "Fragment 0 does not match the expected HTML."
    assert (
        fragments[1] == "<p>" + "A" * 11 + "</p>"
    ), "Fragment 1 does not match the expected HTML."


def test_split_message_invalid_length(sample_html_no_split):
    """Test case for invalid maximum length."""
    with pytest.raises(ValueError, match="Cannot create fragments."):
        list(split_message(sample_html_no_split, max_len=5))


def test_split_message_edge_case(sample_html_edge_case_text):
    """Test case for edge cases where the content fits exactly within the limit."""

    fragments = list(split_message(sample_html_edge_case_text, max_len=4096))
    assert len(fragments) == 1, f"Expected 1 fragment, returned {len(fragments)}."
    assert (
        fragments[0] == sample_html_edge_case_text
    ), "Fragment 0 does not match the original HTML."


def test_split_message_nested_tags(sample_html_nested_tags_list):
    """Test case for handling nested HTML tags."""

    fragments = list(split_message("".join(sample_html_nested_tags_list), max_len=4096))
    assert len(fragments) == 2, f"Expected 2 fragment, returned {len(fragments)}"
    assert fragments[0].endswith("</p>"), "Fragment 0 must end with </p>."
    assert fragments[1].startswith("<p>"), "Fragment 1 must end with </p>."
    assert (
        fragments[0] == sample_html_nested_tags_list[0]
    ), "Fragment 0 does not match the expected fragment."
    assert (
        fragments[1] == sample_html_nested_tags_list[1]
    ), "Fragment 1 does not match the expected fragment."
