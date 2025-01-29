from typing import Generator

import click
from bs4 import BeautifulSoup, NavigableString, Tag

MAX_LEN = 4096

BLOCK_TAGS = {"p", "b", "strong", "i", "ul", "ol", "div", "span"}


def copy_tag_without_contents(tag: Tag) -> Tag:
    """
    Creates a copy of an HTML tag, preserving its attributes but removing its content.

    Args:
        tag (Tag): The HTML tag to copy.

    Returns:
        Tag: A new tag with the same attributes.
    """

    tag_copy = Tag(None, tag.builder, tag.name, tag.namespace, tag.nsprefix)
    tag_copy.attrs = dict(tag.attrs)
    for attr in ("can_be_empty_element", "hidden"):
        setattr(tag_copy, attr, getattr(tag, attr))
    return tag_copy


def split_html_by_border(elements: BeautifulSoup, border: int) -> BeautifulSoup:
    """
    Splits an HTML element into two parts, ensuring the first part fits within the specified `border`.

    Args:
        elements (BeautifulSoup): The HTML content to be split.
        border (int): The maximum allowed length of the first part.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the first part of the split content.

    Raises:
        ValueError: If an element cannot be split.
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
                                f"Cannot split with border {inner_border}: left part length is less than empty tag size."
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
                # Separation was successful
                break

        return left_chunk


def split_message(source: str, max_len: int = MAX_LEN) -> Generator[str, None, None]:
    """
    Splits an HTML message into fragments, ensuring each fragment does not exceed `max_len`.

    Args:
        source (str): The original HTML message.
        max_len (int): The maximum length of each fragment.

    Yields:
        str: A fragment of the HTML message that fits within `max_len`.
    """
    if len(source) <= max_len:
        yield source
        return

    soup = BeautifulSoup(source, "html.parser")

    while soup.contents:
        current_fragment = split_html_by_border(soup, max_len)
        yield str(current_fragment).strip()


@click.command()
@click.option(
    "--max-len", default=MAX_LEN, help="Maximum length of each message fragment."
)
@click.argument("file_path", type=click.Path(exists=True))
def main(max_len, file_path):
    """
    Reads an HTML file, splits its content into fragments, and prints them to stdout.

    Args:
        file_path (str): The path to the HTML file to be processed.
        max_len (int): The maximum allowed length of each fragment.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: If an unexpected error occurs while reading the file.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            dev_source = file.read()
    except Exception as err:
        raise click.ClickException(f"Error reading '{file_path}': {err}")

    for i, fragment in enumerate(split_message(dev_source, max_len), start=1):
        print(f"-- fragment #{i}: {len(fragment)} chars. --")
        print(fragment)


if __name__ == "__main__":
    main()
