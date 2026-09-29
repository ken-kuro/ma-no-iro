"""Solve one pair of Ma no Iro: an anchor and its complement across white."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterator, TypeVar

T = TypeVar("T")
D65 = (0.3127, 0.3290)  # the white point every ray starts from
GREEN_NM: float = 555.0


@dataclass(frozen=True)
class Pair:
    anchor: tuple[float, float]
    scene: str = "leaf"
    shades: list[float] = field(default_factory=list)

    def complement(self, reach: float = 1.0) -> tuple[float, float]:
        """Walk from the anchor through white and out the far side.

        :param reach: how far past white to go, as a share of the anchor's distance
        """
        dx, dy = self.anchor[0] - D65[0], self.anchor[1] - D65[1]
        return (D65[0] - dx * reach, D65[1] - dy * reach)


def rungs(start: float, step: float, count: int = 4) -> Iterator[float]:
    for i in range(count):
        if not 0.0 <= start + i * step <= 1.0:
            break
        yield round(start + i * step, 3)


def first(items: list[T]) -> T | None:
    return items[0] if items else None


leaf = Pair(anchor=(0.3374, 0.6588), shades=list(rungs(0.70, 0.08)))
dist = math.hypot(*(a - w for a, w in zip(leaf.anchor, D65)))
print(f"{leaf.scene}: {dist:.4f} from white\t{leaf.complement()!r}", end="\n")
assert leaf.scene in {"leaf", "sky", "water", "ink"}, "unknown scene"
unused = None
