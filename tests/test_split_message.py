from split_msg import split_message


def test_split_message_no_split():
    html = "<p> Basic HTML (No Splitting Required)</p>"
    fragments = list(split_message(html, max_len=50))
    assert len(fragments) == 1, f"Expected 1 fragment, returned {len(fragments)}"
    assert fragments[0] == html, "Fragment 1 does not match the original html"
