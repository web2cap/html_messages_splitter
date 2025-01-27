import pytest

from split_msg import split_message


def test_split_message_no_split():
    """Test case for HTML content that does not require splitting."""
    html = "<p>Basic HTML (No Splitting Required)</p>"
    fragments = list(split_message(html, max_len=50))
    assert len(fragments) == 1, f"Expected 1 fragment, returned {len(fragments)}."
    assert fragments[0] == html, "Fragment 0 does not match the original HTML."


def test_split_message_long_plain_text():
    """Test case for splitting long plain text content."""
    html = "<p>" + "A" * 5000 + "</p>"
    fragments = list(split_message(html, max_len=4096))
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


def test_split_message_invalid_length():
    """Test case for invalid maximum length."""
    html = "<p>Hello, world!</p>"
    with pytest.raises(ValueError, match="Cannot create fragments."):
        list(split_message(html, max_len=5))


def test_split_message_edge_case():
    """Test case for edge cases where the content fits exactly within the limit."""
    html = "<p>" + "A" * 4089 + "</p>"
    fragments = list(split_message(html, max_len=4096))
    assert len(fragments) == 1, f"Expected 1 fragment, returned {len(fragments)}."
    assert fragments[0] == html, "Fragment 0 does not match the original HTML."


def test_split_message_nested_tags():
    """Test case for handling nested HTML tags."""
    expected_fragments = [
        "<p><b>Hello, <i>world</i></b></p>",
        "<p>" + "A" * 4000 + "</p>",
    ]
    fragments = list(split_message("".join(expected_fragments), max_len=4096))
    assert len(fragments) == 2, f"Expected 2 fragment, returned {len(fragments)}"
    assert fragments[0].endswith("</p>"), "Fragment 0 must end with </p>."
    assert fragments[1].startswith("<p>"), "Fragment 1 must end with </p>."
    assert (
        fragments[0] == expected_fragments[0]
    ), "Fragment 0 does not match the expected fragment."
    assert (
        fragments[1] == expected_fragments[1]
    ), "Fragment 1 does not match the expected fragment."
