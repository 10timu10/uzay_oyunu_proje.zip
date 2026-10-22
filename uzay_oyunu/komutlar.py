"""Hafta 5: dekoratörlerle komut sistemi (kayıt deseni).

Komutlar oyunun durum sözlüğünü alır: konum, baglantilar, credits, engines, copilot.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

Durum = dict[str, Any]

# ad -> (fonksiyon, açıklama)
KOMUTLAR: dict[str, tuple[Callable[[Durum], str], str]] = {}


def komut(ad: str, aciklama: str = "") -> Callable[[Callable], Callable]:
    """Fonksiyonu DEĞİŞTİRMEDEN KOMUTLAR'a (fonksiyon, aciklama) olarak kaydeder.

    Aynı ad ikinci kez kullanılırsa ValueError, fonksiyon tanımlanırken fırlar.
    """

    def kaydet(fonksiyon: Callable) -> Callable:
        if ad in KOMUTLAR:
            raise ValueError(f"'{ad}' komutu zaten kayıtlı")
        KOMUTLAR[ad] = (fonksiyon, aciklama)
        return fonksiyon  # sarmalamadan aynen döndürür

    return kaydet


def _var_yok(deger: Any) -> str:
    if isinstance(deger, bool):
        return "var" if deger else "yok"
    return str(deger)


@komut("yardim", "komutları listeler")
def yardim(durum: Durum) -> str:
    return "\n".join(f"{ad:<10}{aciklama}" for ad, (_, aciklama) in sorted(KOMUTLAR.items()))


@komut("envanter", "eşyalarını gösterir")
def envanter(durum: Durum) -> str:
    return ", ".join(f"{ad}: {_var_yok(durum[ad])}" for ad in ("credits", "engines", "copilot"))


@komut("harita", "gidebileceğin gezegenleri gösterir")
def harita(durum: Durum) -> str:
    baglantilar = durum["baglantilar"]
    if isinstance(baglantilar, dict):  # {konum: [komşular]}
        baglantilar = baglantilar.get(durum["konum"], [])
    return ", ".join(baglantilar)


def komut_mu(girdi: str) -> bool:
    """Girdi kayıtlı bir komut adı mı?"""
    return girdi.strip() in KOMUTLAR


def komut_calistir(girdi: str, durum: Durum) -> str:
    """Kayıtlı komutu çalıştırıp sonucunu döndürür."""
    fonksiyon, _ = KOMUTLAR[girdi.strip()]
    return fonksiyon(durum)
