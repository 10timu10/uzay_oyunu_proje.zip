"""Hafta 4: üreteçler, boru hattı ve önbellekli rota sayacı."""
from __future__ import annotations

import time
from collections.abc import Callable, Iterable, Iterator
from functools import lru_cache

from uzay_oyunu.dekoratorler import sure_olc

Kayit = tuple[str, str, int]  # (kaynak, hedef, yakıt)


# --- Görev 1 -----------------------------------------------------------
def fibonacci() -> Iterator[int]:
    """Sonsuz Fibonacci dizisini (0, 1, 1, 2, ...) tembel biçimde üretir."""
    onceki, simdiki = 0, 1
    while True:
        yield onceki
        onceki, simdiki = simdiki, onceki + simdiki


# --- Görev 2 -----------------------------------------------------------
def yakit_gostergesi(yakit: int, tuketim: int) -> Iterator[int]:
    """Her adımda yakıtı `tuketim` kadar azaltıp kalanı üretir; 0'da durur."""
    if tuketim <= 0:
        raise ValueError("tuketim pozitif olmalı (yoksa üreteç hiç bitmez)")
    while yakit > 0:
        yakit = max(0, yakit - tuketim)
        yield yakit


# --- Görev 3: üç aşamalı boru hattı -------------------------------------
def satirlari_oku(yol: str) -> Iterator[str]:
    """Dosyayı satır satır okur; boş ve '#' ile başlayan satırları atlar."""
    with open(yol, encoding="utf-8") as dosya:
        for satir in dosya:  # dosya nesnesi zaten tembel bir yineleyicidir
            satir = satir.strip()
            if satir and not satir.startswith("#"):
                yield satir


def ayristir(satirlar: Iterable[str]) -> Iterator[Kayit]:
    """'dünya -> sirius 12' satırını ('dünya', 'sirius', 12) demetine çevirir."""
    for satir in satirlar:
        kaynak, geri = satir.split("->")
        hedef, yakit = geri.split()
        yield kaynak.strip(), hedef, int(yakit)


def uzun_yolculuklar(kayitlar: Iterable[Kayit], esik: int) -> Iterator[Kayit]:
    """Yakıtı `esik` değerinden büyük olan kayıtları süzer."""
    for kayit in kayitlar:
        if kayit[2] > esik:
            yield kayit


# --- Görev 4 -----------------------------------------------------------
def rota_sayaci(baglantilar: dict[str, list[str]]) -> Callable[[str, int], int]:
    """Önbellekli `rota_sayisi(gezegen, adim)` fonksiyonunu döndürür."""

    @lru_cache(maxsize=None)
    def rota_sayisi(gezegen: str, adim: int) -> int:
        if adim == 0:
            return 1
        return sum(rota_sayisi(komsu, adim - 1)
                   for komsu in baglantilar.get(gezegen, []))

    return rota_sayisi


def rota_sayaci_onbelleksiz(baglantilar: dict[str, list[str]]) -> Callable[[str, int], int]:
    """Karşılaştırma için aynı hesabı önbelleksiz yapan sürüm."""

    def rota_sayisi(gezegen: str, adim: int) -> int:
        if adim == 0:
            return 1
        return sum(rota_sayisi(komsu, adim - 1)
                   for komsu in baglantilar.get(gezegen, []))

    return rota_sayisi


def olc(baglantilar: dict[str, list[str]], gezegen: str = "dünya", adim: int = 20) -> None:
    """İki sürümün süresini ve cache_info() çıktısını yazdırır (README için)."""
    onbelleksiz = rota_sayaci_onbelleksiz(baglantilar)
    t0 = time.perf_counter()
    sonuc = onbelleksiz(gezegen, adim)
    t_onbelleksiz = time.perf_counter() - t0

    onbellekli = rota_sayaci(baglantilar)
    t0 = time.perf_counter()
    assert onbellekli(gezegen, adim) == sonuc
    t_onbellekli = time.perf_counter() - t0

    print(f"Önbelleksiz: {t_onbelleksiz:.4f} sn | Önbellekli: {t_onbellekli:.6f} sn")
    print(onbellekli.cache_info())


def olc_dekoratorlu(baglantilar: dict[str, list[str]], gezegen: str = "dünya", adim: int = 20) -> int:
    """Hafta 5 Görev 1: önbelleksiz sayaca @sure_olc uygulayıp süreyi yazdırır."""
    olculen = sure_olc(rota_sayaci_onbelleksiz(baglantilar))
    return olculen(gezegen, adim)


if __name__ == "__main__":
    from uzay_oyunu.oyun import galaksiyi_yukle

    olc(galaksiyi_yukle()["baglantilar"], "dünya", 20)
    olc_dekoratorlu(galaksiyi_yukle()["baglantilar"], "dünya", 20)
