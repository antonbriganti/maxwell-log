#!/usr/bin/env python3
"""Convert between Castirian calendar dates and Maxwell's Rela-Date System (R.D.).

Calendar: Castirian dates use 12 months of 30 days (360 days per year). Dates look
like ``5016u-07-05`` (or ``5016-07-05``); the ``u`` is ignored.

Rela-Date: ``a.b.c.d R.D.`` where the fields are base-10 blocks of days since birth:
    a = days           (0-9)
    b = rela-weeks     (0-9, 10 days)
    c = rela-months    (0-9, 10 weeks = 100 days)
    d = rela-years     (0-x, 10 months = 1000 days)

Note the two different year lengths:
    * the Castirian calendar year is 360 days (used to map dates <-> day numbers)
    * the rela-date system is anchored to 365-day years, so a person's age in
      years is simply ``days_since_birth / 365``

Reference point: ``5016u-05-06`` == ``5.7.7.12 R.D.``
"""
from __future__ import annotations

import re
import sys

DAYS_PER_MONTH = 30
MONTHS_PER_YEAR = 12
DAYS_PER_YEAR = DAYS_PER_MONTH * MONTHS_PER_YEAR  # Castirian calendar year
RELA_DAYS_PER_YEAR = 365  # rela-date system tracks 365-day years

# Reference point: dates -> rela-days, rela-days -> dates.
REF_DATE = (5016, 5, 6)
REF_RELADATE = (12, 7, 7, 5)  # stored high-to-low as (rela-years, months, weeks, days)

# Birth day (rela 0.0.0.0), derived from the reference point above.
_REF_DAY = (
    REF_DATE[0] * DAYS_PER_YEAR
    + (REF_DATE[1] - 1) * DAYS_PER_MONTH
    + (REF_DATE[2] - 1)
)
_BIRTH_DAY = _REF_DAY - (
    REF_RELADATE[0] * 1000
    + REF_RELADATE[1] * 100
    + REF_RELADATE[2] * 10
    + REF_RELADATE[3]
)

_DATE_RE = re.compile(r"^\s*(\d+)\s*u?\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})\s*$")
_RELADATE_RE = re.compile(
    r"^\s*(\d+)\s*\.\s*(\d+)\s*\.\s*(\d+)\s*\.\s*(\d+)\s*(?:R\.?D\.?)?\s*$",
    re.IGNORECASE,
)


def _to_day_index(year: int, month: int, day: int) -> int:
    """Linear day number for a calendar date (no leap years)."""
    return (year * DAYS_PER_YEAR) + (month - 1) * DAYS_PER_MONTH + (day - 1)


def _from_day_index(index: int) -> tuple[int, int, int]:
    """Inverse of :func:`_to_day_index`."""
    year, rem = divmod(index, DAYS_PER_YEAR)
    month, day = divmod(rem, DAYS_PER_MONTH)
    return year, month + 1, day + 1


def parse_date(text: str) -> tuple[int, int, int]:
    """Parse ``5016u-07-05`` -> ``(5016, 7, 5)``."""
    match = _DATE_RE.match(text)
    if not match:
        raise ValueError(f"not a valid date: {text!r}")
    year, month, day = (int(g) for g in match.groups())
    if not 1 <= month <= MONTHS_PER_YEAR:
        raise ValueError(f"month out of range (1-{MONTHS_PER_YEAR}): {month}")
    if not 1 <= day <= DAYS_PER_MONTH:
        raise ValueError(f"day out of range (1-{DAYS_PER_MONTH}): {day}")
    return year, month, day


def parse_reladate(text: str) -> tuple[int, int, int, int]:
    """Parse ``2.9.8.12 R.D.`` -> ``(12, 8, 9, 2)`` ordered (years, months, weeks, days)."""
    match = _RELADATE_RE.match(text)
    if not match:
        raise ValueError(f"not a valid rela-date: {text!r}")
    days, weeks, months, years = (int(g) for g in match.groups())
    return years, months, weeks, days


def date_to_days(text: str) -> int:
    """Days elapsed since birth for a calendar date."""
    return _to_day_index(*parse_date(text)) - _BIRTH_DAY


def reladate_to_days(reladate: tuple[int, int, int, int]) -> int:
    """Total days for a ``(years, months, weeks, days)`` rela-date tuple."""
    years, months, weeks, days = reladate
    return years * 1000 + months * 100 + weeks * 10 + days


def days_to_reladate(total: int) -> tuple[int, int, int, int]:
    """Split a day count into ``(years, months, weeks, days)``."""
    total, days = divmod(total, 10)
    total, weeks = divmod(total, 10)
    total, months = divmod(total, 10)
    years = total
    return years, months, weeks, days


def days_to_age(total: int) -> float:
    """Age in rela-date (365-day) years for a number of days."""
    return total / RELA_DAYS_PER_YEAR


def date_to_reladate(text: str) -> str:
    """Convert a calendar date to its rela-date string."""
    total = date_to_days(text)
    if total < 0:
        raise ValueError(f"date predates birth: {text!r}")
    years, months, weeks, days = days_to_reladate(total)
    return f"{days}.{weeks}.{months}.{years} R.D."


def reladate_to_date(text: str) -> str:
    """Convert a rela-date string to a calendar date (``5016u-07-05``)."""
    total = reladate_to_days(parse_reladate(text))
    year, month, day = _from_day_index(_BIRTH_DAY + total)
    return f"{year}u-{month:02d}-{day:02d}"


def convert(text: str) -> str:
    """Auto-detect direction and convert."""
    if _RELADATE_RE.match(text):
        return reladate_to_date(text)
    if _DATE_RE.match(text):
        return date_to_reladate(text)
    raise ValueError(f"unrecognised input: {text!r}")


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 0
    try:
        for arg in argv:
            print(convert(arg))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
