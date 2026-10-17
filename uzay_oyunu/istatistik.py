"""Galaksi verisi üzerinde map/filter/reduce ve liste üreteci karşılaştırması."""
from __future__ import annotations

from functools import partial, reduce
from typing import Any

Galaksi = dict[str, Any]


# 1) Gezegen adlarının büyük harfli listesi
def adlar_buyuk_mfr(galaksi: Galaksi) -> list[str]:
    """map ile gezegen adlarını büyük harfe çevirir."""
    return list(map(str.upper, galaksi["gezegenler"]))


def adlar_buyuk_liste(galaksi: Galaksi) -> list[str]:
    """Liste üreteciyle gezegen adlarını büyük harfe çevirir."""
    return [ad.upper() for ad in galaksi["gezegenler"]]


# 2) En az iki bağlantısı olan gezegenler
def cok_baglantili_mfr(galaksi: Galaksi) -> list[str]:
    """filter ile en az iki bağlantısı olan gezegenleri süzer."""
    b = galaksi["baglantilar"]
    return list(filter(lambda ad: len(b.get(ad, [])) >= 2, galaksi["gezegenler"]))


def cok_baglantili_liste(galaksi: Galaksi) -> list[str]:
    """Liste üreteciyle en az iki bağlantısı olan gezegenleri süzer."""
    b = galaksi["baglantilar"]
    return [ad for ad in galaksi["gezegenler"] if len(b.get(ad, [])) >= 2]


# 3) Toplam bağlantı sayısı
def toplam_baglanti_reduce(galaksi: Galaksi) -> int:
    """reduce ile tüm bağlantıları toplar."""
    return reduce(lambda toplam, komsular: toplam + len(komsular),
                  galaksi["baglantilar"].values(), 0)


def toplam_baglanti_sum(galaksi: Galaksi) -> int:
    """sum ile tüm bağlantıları toplar."""
    return sum(len(komsular) for komsular in galaksi["baglantilar"].values())


# Okunaklılık yorumu: Liste üreteci ve sum() yazımını tercih ederim; ne yaptığı kodun
# kendisinden okunuyor. map/filter/reduce'ta lambda'lar ve iç içe çağrılar
# (list(filter(lambda ...))) okumayı yavaşlatıyor.


def yolculuk_suresi(yakit: int, hiz: int = 1) -> float:
    """Yakıt miktarını (mesafe yerine) hıza bölerek yolculuk süresini verir."""
    return yakit / hiz


# functools.partial: hız sabit 3 olan yeni bir fonksiyon türetir.
hizli_yolculuk = partial(yolculuk_suresi, hiz=3)