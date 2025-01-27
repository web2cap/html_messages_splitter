import os
from os.path import abspath, dirname

APPFILENAME = "split_msg.py"

root_dir = dirname(dirname(abspath(__file__)))
root_dir_content = os.listdir(root_dir)

# check that the project structure is correct and split_msg.py is in place
if APPFILENAME not in root_dir_content:
    assert False, (
        f"In `{root_dir_content}` not found file `{APPFILENAME}`. "
        f"Make sure you have the correct project structure."
    )


pytest_plugins = ["fixtures.fixture_split_message"]
