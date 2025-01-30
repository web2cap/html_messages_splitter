# html_messages_splitter
A Python-based solution to split HTML messages into fragments that respect a maximum length limit while maintaining valid HTML structure.
The tool ensures tags are properly closed and reopened where necessary, preserving formatting for each fragment.



[![GitHub Actions](https://github.com/web2cap/html_messages_splitter/actions/workflows/main_protect.yml/badge.svg)](https://github.com/web2cap/html_messages_splitter/actions/workflows/main_protect.yml)


## Installation

### Prerequisites

 - Python 3.12+
 - Poetry

### Setup

Clone the repository and install dependencies:

```
git clone https://github.com/web2cap/html_messages_splitter.git
cd html_messages_splitter
poetry install
```

## Usage

### CLI
```
poetry run python split_msg.py --max-len=3072 ./source.html
```

### To use the split_message function in your Python code:

```
from split_msg import split_message

html_content = "<p>Hello, this is a long message</p><p>that needs splitting.</p>"
fragments = list(split_message(html_content, max_len=30))

for fragment split_message(html_content, max_len=30):
    print(fragment)
```

## Running Tests

```
poetry run pytest
```



### Project Structure

```
├── .github                  # Project workflow
├── README.md                # Project documentation
├── poetry.lock              # Poetry dependency lock file
├── pyproject.toml           # Poetry configuration file
├── pytest.ini               # Pytest configuration
├── source.html              # Sample HTML source file
├── split_msg.py             # Main script for message splitting
└── tests                    # Unit tests
    ├── conftest.py          # Pytest configuration file
    ├── fixtures             # Test fixtures
    ├── test_split_msg.py    # Unit tests for message splitter
```