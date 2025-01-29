import pytest

from split_msg import split_message


def test_split_message_no_split(sample_html_no_split):
    """Test case for HTML content that does not require splitting."""
    fragments = list(split_message(sample_html_no_split, max_len=50))
    assert len(fragments) == 1, f"Expected 1 fragment, returned {len(fragments)}."
    assert (
        fragments[0] == sample_html_no_split
    ), "Fragment 0 does not match the original HTML."


def test_split_message_invalid_length(sample_html_no_split):
    """Test case for invalid maximum length."""
    with pytest.raises(
        ValueError,
        match="Cannot split with border 5: left part length is less than empty tag size.",
    ):
        list(split_message(sample_html_no_split, max_len=5))


def test_split_message_edge_case(sample_html_edge_case_text):
    """Test case for edge cases where the content fits exactly within the limit."""

    fragments = list(split_message(sample_html_edge_case_text, max_len=4096))
    assert len(fragments) == 1, f"Expected 1 fragment, returned {len(fragments)}."
    assert (
        fragments[0] == sample_html_edge_case_text
    ), "Fragment 0 does not match the original HTML."


def test_split_message_nested_tags(sample_html_nested_tags_source_result):
    """Test case for handling nested HTML tags."""
    source, expected_result = sample_html_nested_tags_source_result
    fragments = list(split_message(source, max_len=4096))

    print(fragments)

    assert len(fragments) == 2, f"Expected 2 fragment, returned {len(fragments)}"
    assert fragments[0].endswith("</p>"), "Fragment 0 must end with </p>."
    assert fragments[1].startswith("<p>"), "Fragment 1 must end with </p>."
    assert (
        fragments[0] == expected_result[0]
    ), "Fragment 0 does not match the expected fragment."
    assert (
        fragments[1] == expected_result[1]
    ), "Fragment 1 does not match the expected fragment."


def test_split_message_multiple_splits(sample_html_multiple_splits):
    """Test case for HTML content that requires multiple splits."""
    fragments = list(split_message(sample_html_multiple_splits, max_len=100))
    assert len(fragments) == 3, f"Expected 3 fragments, returned {len(fragments)}."
    assert fragments[0].startswith("<p>"), "Fragment 0 should start with <p>."
    assert fragments[2].endswith("</p>"), "Fragment 3 should end with </p>."


def test_split_message_large_single_tag(sample_html_long_single_tag):
    """Test case where a single large tag exceeds the maximum length."""
    with pytest.raises(
        ValueError,
        match=f"HTML separation failed, can't separate {sample_html_long_single_tag} with border {1000}",
    ):
        list(split_message(sample_html_long_single_tag, max_len=1000))
