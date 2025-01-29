import copy
from typing import Generator

from bs4 import BeautifulSoup, NavigableString, Tag

MAX_LEN = 4096

BLOCK_TAGS = {"p", "b", "strong", "i", "ul", "ol", "div", "span"}


def copy_tag_without_contents(tag: Tag) -> Tag:
    root_tag = copy.copy(tag)
    root_tag.clear()
    return root_tag


def split_html_by_border(elements: BeautifulSoup, border: int) -> BeautifulSoup:
    """
    Splits an HTML element into two parts, ensuring the first part fits within the specified `border`.
    """
    if isinstance(elements, NavigableString):
        raise ValueError(f"Plain text string is not splittable: '{elements}'")

    elif isinstance(elements, Tag):
        # Prepare root tag with existing attributes but without content
        left_chunk = copy_tag_without_contents(elements)

        while elements.contents:
            inner_element = elements.contents[0]
            left_chunk_len = len(str(left_chunk))
            expected_left_chunk_len = left_chunk_len + len(str(inner_element))
            if expected_left_chunk_len <= border:
                # If the current inner element fits within the left part
                # Add it to the left chunk and remove it from the tree.
                left_chunk.append(inner_element.extract())
            else:
                # If the current element exceeds the border, attempt to split it
                inner_border = border - left_chunk_len

                if not left_chunk.contents:
                    if isinstance(inner_element, Tag):
                        # If the left chunk is still empty and separation isn't possible
                        if inner_element.name not in BLOCK_TAGS:
                            raise ValueError(
                                f"HTML separation failed: element {inner_element} is not splittable."
                            )
                        if not inner_element.contents:
                            raise ValueError(
                                f"HTML separation failed: element {inner_element} has no content."
                            )
                        if inner_border < 7:
                            raise ValueError(
                                "Can't split: border {inner_border} lenght less then empty tag."
                            )
                    else:
                        raise ValueError(
                            f"Plain text string is not splittable: '{inner_element}'"
                        )
                try:
                    left_inner_chunk = split_html_by_border(inner_element, inner_border)
                    left_chunk.append(left_inner_chunk)
                except ValueError:
                    if left_chunk.contents:
                        # If splitting fails but the left chunk is not empty, break and return left chunk
                        break
                    raise ValueError(
                        f"HTML separation failed, can't separate {inner_element} with border {inner_border}"
                    )
                # separation was successful, break and return
                break

        return left_chunk


def split_message(source: str, max_len: int = MAX_LEN) -> Generator[str]:
    """Splits the original message (`source`) into fragments of the specified length
    (`max_len`)."""

    if len(source) <= max_len:
        yield source
        return

    soup = BeautifulSoup(source, "html.parser")

    while soup.contents:
        current_fragment = split_html_by_border(soup, max_len)
        yield str(current_fragment).strip()


if __name__ == "__main__":
    file_name = "source.html"
    try:
        with open(file_name, "r") as file:
            dev_source = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File '{file_name}' not found. Please check the file path."
        )
    except Exception as err:
        raise Exception(f"Unexpected error while opening '{file_name}': {repr(err)}")

    fragment_number = 1
    for fragment in split_message(dev_source):
        print(f"-- #{fragment_number}: {len(fragment)} chars --")
        print(fragment)
        fragment_number += 1
