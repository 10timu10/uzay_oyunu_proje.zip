"""Görev 2: dekoratör sırasının çağrı sayısına etkisi (özyinelemeli Fibonacci)."""
from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache

from uzay_oyunu.dekoratorler import say


def yalniz_say() -> Callable[[int], int]:
    """Yalnızca @say: önbellek yok."""

    @say
    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    return fib


def say_ustte() -> Callable[[int], int]:
    """@say üstte, @lru_cache altta: say, önbelleğe İSABET eden çağrıları da sayar."""

    @say
    @lru_cache(maxsize=None)
    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    return fib


def lru_ustte() -> Callable[[int], int]:
    """@lru_cache üstte, @say altta: say yalnızca önbellekte OLMAYAN çağrıları görür."""

    @lru_cache(maxsize=None)
    @say
    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    return fib


def cagri_sayilari(n: int = 20) -> dict[str, int]:
    """Üç biçim için fib(n) çağrı sayısını döndürür (her biri taze kurulur)."""
    a = yalniz_say()
    a(n)
    b = say_ustte()
    b(n)
    c = lru_ustte()
    c(n)
    return {
        "yalnızca @say": a.cagri,
        "@say üstte, @lru_cache altta": b.cagri,
        "@lru_cache üstte, @say altta": c.__wrapped__.cagri,
    }


if __name__ == "__main__":
    for ad, sayi in cagri_sayilari(20).items():
        print(f"{ad}: {sayi}")
