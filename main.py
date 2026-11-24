#!/usr/bin/env python3
"""Seventeen Syllables of Debugging.

Writes one haiku about debugging to /output/entry.txt.

The haiku is kept as a plain constant below. Before writing, the program
checks the shape itself: exactly three lines, five syllables, then seven,
then five, and no more than two hundred characters in total. Nothing is
read from anywhere else; the output is the same on every run.
"""

import os

HAIKU = (
    "Cursor blinks at three\n"
    "one last log line claims it worked\n"
    "the bug has moved on"
)

SHAPE = (5, 7, 5)
MAX_CHARS = 200
OUT_PATH = "/output/entry.txt"

VOWELS = set("aeiouy")


def count_syllables(word):
    """Rough syllable count for the plain English words used here.

    Counts groups of adjacent vowels, then drops one for a silent
    trailing 'e' or a silent 'e' in a past-tense '-ed' ending, as in
    'line', 'worked' and 'moved'. Never returns less than one.
    """
    cleaned = "".join(ch for ch in word.lower() if ch.isalpha())
    if not cleaned:
        return 0

    groups = 0
    previous_was_vowel = False
    for ch in cleaned:
        if ch in VOWELS:
            if not previous_was_vowel:
                groups += 1
            previous_was_vowel = True
        else:
            previous_was_vowel = False

    if groups > 1 and cleaned.endswith("e"):
        groups -= 1
    elif groups > 1 and cleaned.endswith("ed") and cleaned[-3] not in "td":
        groups -= 1

    return max(groups, 1)


def check_haiku(text):
    """Return a list of problems with the haiku, empty when it is sound."""
    problems = []
    lines = text.split("\n")

    if len(lines) != 3:
        problems.append("expected 3 lines, found %d" % len(lines))
        return problems

    for line, wanted in zip(lines, SHAPE):
        got = sum(count_syllables(word) for word in line.split())
        if got != wanted:
            problems.append(
                "line %r has %d syllables, want %d" % (line, got, wanted)
            )

    if not 1 <= len(text) <= MAX_CHARS:
        problems.append(
            "haiku is %d characters, want 1-%d" % (len(text), MAX_CHARS)
        )

    return problems


def main():
    problems = check_haiku(HAIKU)
    if problems:
        for problem in problems:
            print("error: " + problem)
        raise SystemExit(1)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(HAIKU + "\n")

    lines = HAIKU.split("\n")
    counts = [sum(count_syllables(w) for w in line.split()) for line in lines]
    print("wrote %s (%s syllables, %d characters)"
          % (OUT_PATH, "-".join(str(c) for c in counts), len(HAIKU) + 1))


if __name__ == "__main__":
    main()
