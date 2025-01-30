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


def test_split_message_split_at_tag_boundary(sample_html_split_at_block_tag):
    """Test case for HTML that should split at a tag boundary."""
    fragments = list(split_message(sample_html_split_at_block_tag, max_len=411))
    assert len(fragments) == 2, f"Expected 2 fragments, returned {len(fragments)}."
    assert fragments[0].startswith("<p>"), "Second fragment must start with <b>."
    assert fragments[0].endswith("</b>"), "First fragment must end with </b>."
    assert fragments[1].startswith("<i>"), "Second fragment must start with <b>."


def test_split_message_with_special_characters(sample_html_with_special_chars_list):
    """Test case for HTML content with special characters like &amp;, &lt;, etc. \t \n"""
    fragments = list(
        split_message("".join(sample_html_with_special_chars_list), max_len=30)
    )
    assert len(fragments) == 2, f"Expected 2 fragments, returned {len(fragments)}."
    assert (
        fragments[0] == sample_html_with_special_chars_list[0]
    ), "Fragment 0 does not match the expected fragment."
    assert (
        fragments[1] == sample_html_with_special_chars_list[1]
    ), "Fragment 1 does not match the expected fragment."


def test_split_message_no_split_required_for_many_tags_set(sample_html_many_tags_set):
    """Test case for very large content, but no split required due to small max_len."""
    fragments = list(split_message(sample_html_many_tags_set, max_len=10000))
    assert len(fragments) == 1, f"Expected 1 fragment, returned {len(fragments)}."
    assert (
        fragments[0] == sample_html_many_tags_set
    ), "The fragment should be the original content."


def test_split_message_empty_html_tag(sample_html_empty_html_tag):
    """Test case for an empty HTML tag to check how it is handled."""
    fragments = list(split_message(sample_html_empty_html_tag, max_len=500))
    assert len(fragments) == 1, f"Expected 1 fragment, returned {len(fragments)}."
    assert (
        fragments[0] == sample_html_empty_html_tag
    ), "Fragment should contain the empty <div> tag."


def test_html_separation_after_line_break(sample_html_separation_after_line_break):
    """
    Test that ensures correct splitting of HTML when a line break is present inside a tag.

    Verifies that the first fragment contains the <div> tag with the line break.
    And the second fragment does not.
    """

    fragments = list(split_message(sample_html_separation_after_line_break, max_len=35))
    assert len(fragments) == 2, f"Expected 2 fragment, returned {len(fragments)}."
    assert (
        "<div>\n</div>" in fragments[0]
    ), "Fragment 0 should contain <div> tag with line break."
    assert (
        "<div>\n" not in fragments[1]
    ), "Fragment 1 should contain <div> tag without line break."


def test_split_fails_on_empty_html_tag(sample_html_separation_in_empty_tag):
    """
    Test that ensures an exception is raised when trying to split an HTML string
    containing an empty <span> tag.

    The function should raise a ValueError with a specific error message indicating
    that the <span> element has no content.
    """
    with pytest.raises(
        ValueError,
        match="HTML separation failed: element <span></span> has no content.",
    ):
        list(split_message(sample_html_separation_in_empty_tag, max_len=18))
