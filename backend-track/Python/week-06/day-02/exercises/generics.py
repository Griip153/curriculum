# Day 22 - "Your turn" item 3: first_or_none using TypeVar. See LESSON.md
# Section 5 for the exact pattern to follow.

from typing import TypeVar

T = TypeVar("T")


def first_or_none(items: list[T]) -> T | None:
    # TODO: return the first element of items, or None if items is empty.
    pass
