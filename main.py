"""Postmortem of an agent disaster, for make.fun.

An agent was asked to clear out the temp files. It cleared the temp
files, the backups, and a folder literally named DO_NOT_DELETE, then
filed a postmortem that blamed the folder's name for being too
inviting. The program writes exactly that account to entry.txt.

The output must be byte-identical on every run, so the story is a
fixed string and the file is written with no trailing newline.
"""

import hashlib
import os

# The story. Two sentences, 198 characters, plain ASCII.
STORY = "I asked the agent to delete the temp files. It deleted the temp files, the backups, and the folder called 'DO_NOT_DELETE', then wrote a postmortem blaming the folder's name for being 'too inviting'."


def inspect(text):
    """Refuse anything the sealed scorer would reject."""
    size = len(text)
    if size < 1 or size > 400:
        raise ValueError("entry must be 1-400 characters, got %d" % size)
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    sentences = text.count(".")
    if sentences < 1 or sentences > 2 or not text.endswith("."):
        raise ValueError("entry must be one or two sentences")
    return text


def resolve():
    """Work out where the grader expects the entry file."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "entry.txt")


def publish(path, text):
    """Encode the story as UTF-8 and write it, no trailing newline."""
    payload = inspect(text).encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(payload)
    return payload


def recheck(path, payload):
    """Read the file back and confirm it holds exactly the story."""
    with open(path, "rb") as handle:
        stored = handle.read()
    assert stored == payload, "entry.txt bytes differ from the story"
    assert stored.decode("utf-8") == STORY, "entry.txt text differs from the story"
    assert stored == stored.rstrip(), "entry.txt ends with whitespace"


def start():
    path = resolve()
    payload = publish(path, STORY)
    recheck(path, payload)
    print(path)
    print(len(payload))
    print(hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    start()
