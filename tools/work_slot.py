"""Decide if a scheduled work slot is active today.

The project has 6 fixed work slots each day (0 to 5).
Each day, a number from 2 to 5 of these slots are active.
The date gives the choice, so the result is stable for one day
and different between days.

Usage:
    python tools/work_slot.py <slot> [YYYY-MM-DD]
Exit code 0 = slot is active. Exit code 1 = skip this slot.
"""

import hashlib
import random
import sys
from datetime import date

SLOTS = 6
MIN_ACTIVE = 2
MAX_ACTIVE = 5


def active_slots(day: date) -> list[int]:
    seed = int(hashlib.sha256(day.isoformat().encode()).hexdigest(), 16)
    rng = random.Random(seed)
    count = rng.randint(MIN_ACTIVE, MAX_ACTIVE)
    return sorted(rng.sample(range(SLOTS), count))


def main(argv: list[str]) -> int:
    slot = int(argv[1])
    day = date.fromisoformat(argv[2]) if len(argv) > 2 else date.today()
    slots = active_slots(day)
    print(f"{day}: active slots {slots}")
    return 0 if slot in slots else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
