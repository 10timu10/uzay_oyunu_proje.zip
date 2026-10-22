"""Hafta 5: kendi dekoratörlerimiz.

Her dekoratör ``functools.wraps`` kullanır; böylece dekore edilen fonksiyonun
``__name__`` ve ``__doc__`` bilgileri sarmalayıcıya taşınır.

Tanım anı / çağrı anı: ``@dekorator`` satırı, fonksiyon TANIMLANIRKEN (modül
içe aktarılırken) bir kez çalışır ve fonksiyonun yerine sarmalayıcıyı koyar.
Sarmalayıcının gövdesi ise fonksiyon her ÇAĞRILDIĞINDA çalışır.
"""
from __future__ import annotations

import time
from collections.abc import Callable
from functools import wraps
from typing import Any


# --- Görev 1 -----------------------------------------------------------
def sure_olc(fonksiyon: Callable) -> Callable:
    """Çalışma süresini 'ad: 0.0123 sn' biçiminde yazdırır, sonucu aynen döndürür."""

    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        baslangic = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        gecen = time.perf_counter() - baslangic
        print(f"{fonksiyon.__name__}: {gecen:.4f} sn")
        return sonuc

    return sarmalayici


# --- Görev 2 -----------------------------------------------------------
def say(fonksiyon: Callable) -> Callable:
    """Çağrı sayısını sarmalayıcının ``cagri`` niteliğinde tutar."""

    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        sarmalayici.cagri += 1
        return fonksiyon(*args, **kwargs)

    sarmalayici.cagri = 0  # tanım anında bir kez başlatılır
    return sarmalayici


# --- Görev 3 -----------------------------------------------------------
def log_cagri(fonksiyon: Callable) -> Callable:
    """Çağrıdan önce ad ve argümanları, sonra dönüş değerini yazdırır."""

    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        parcalar = [repr(a) for a in args]
        parcalar += [f"{ad}={deger!r}" for ad, deger in kwargs.items()]
        print(f"-> {fonksiyon.__name__}({', '.join(parcalar)})")
        sonuc = fonksiyon(*args, **kwargs)
        print(f"<- {fonksiyon.__name__} = {sonuc!r}")
        return sonuc

    return sarmalayici


# --- Görev 5 -----------------------------------------------------------
def sinirla(alt: float, ust: float) -> Callable[[Callable], Callable]:
    """İlk argümanın [alt, ust] aralığında (sınırlar dahil) olmasını zorunlu kılar.

    Argüman alan dekoratör üç katmandır: sinirla(alt, ust) -> dekorator(f) -> sarmalayici.
    """

    def dekorator(fonksiyon: Callable) -> Callable:
        @wraps(fonksiyon)
        def sarmalayici(*args: Any, **kwargs: Any) -> Any:
            if args:
                deger = args[0]
            elif kwargs:  # ilk argüman isimle verilmişse onu al
                deger = next(iter(kwargs.values()))
            else:
                raise TypeError(f"{fonksiyon.__name__}: sınırlanacak argüman verilmedi")
            if not alt <= deger <= ust:
                raise ValueError(
                    f"{fonksiyon.__name__}: {deger} değeri {alt}-{ust} aralığında değil"
                )
            return fonksiyon(*args, **kwargs)

        return sarmalayici

    return dekorator


# --- Bonus -------------------------------------------------------------
def hafiza(maxsize: int | None = None) -> Callable[[Callable], Callable]:
    """lru_cache kullanmadan, closure'daki sözlükle çalışan önbellek.

    maxsize doluysa en eski (ilk eklenen) girdi silinir. ``@hafiza()`` ve
    ``@hafiza(maxsize=3)`` kullanılır. Not: lru_cache "en az kullanılan"ı atar,
    burada "en eski eklenen" atılır (FIFO); sonuçlar yine aynıdır.
    """

    def dekorator(fonksiyon: Callable) -> Callable:
        onbellek: dict = {}  # closure: sarmalayici bu sözlüğü yakalar

        @wraps(fonksiyon)
        def sarmalayici(*args: Any, **kwargs: Any) -> Any:
            anahtar = (args, tuple(sorted(kwargs.items())))
            if anahtar in onbellek:
                return onbellek[anahtar]
            sonuc = fonksiyon(*args, **kwargs)
            if maxsize is not None and len(onbellek) >= maxsize:
                if onbellek:
                    del onbellek[next(iter(onbellek))]  # sözlük ekleme sırasını korur
            if maxsize != 0:
                onbellek[anahtar] = sonuc
            return sonuc

        sarmalayici.onbellek = onbellek
        return sarmalayici

    return dekorator
