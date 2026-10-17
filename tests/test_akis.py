import types
from itertools import islice, takewhile
from pathlib import Path

import pytest

from uzay_oyunu import istatistik as ist
from uzay_oyunu.akis import (ayristir, fibonacci, rota_sayaci,
                             satirlari_oku, uzun_yolculuklar, yakit_gostergesi)
from uzay_oyunu.oyun import galaksi_kur, galaksiyi_yukle, travel

SEYIR = str(Path(__file__).resolve().parent.parent / "veri" / "seyir.txt")


# --- Görev 1 -----------------------------------------------------------
def test_fibonacci_next():
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)


def test_fibonacci_islice_ve_takewhile():
    assert list(islice(fibonacci(), 12)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert list(takewhile(lambda x: x < 100, fibonacci()))[-1] == 89


def test_fibonacci_tek_kullanimlik():
    g = fibonacci()
    ilk = list(islice(g, 5))
    ikinci = list(islice(g, 5))
    assert ilk == [0, 1, 1, 2, 3]
    assert ikinci == [5, 8, 13, 21, 34]
    assert ilk != ikinci


# --- Görev 2 -----------------------------------------------------------
def test_yakit_gostergesi():
    assert list(yakit_gostergesi(100, 30)) == [70, 40, 10, 0]


def test_yakit_bitince_stopiteration():
    g = yakit_gostergesi(10, 5)
    assert (next(g), next(g)) == (5, 0)
    with pytest.raises(StopIteration):
        next(g)


def test_yakit_gecersiz_tuketim():
    with pytest.raises(ValueError):
        list(yakit_gostergesi(10, 0))


def test_travel_yakit_bitince_kaybeder():
    # yakıt 10, tüketim 5 -> iki yolculuk yapılır, üçüncüde StopIteration
    g = galaksi_kur(["dünya", "centauri"], {"dünya": ["centauri"], "centauri": ["dünya"]},
                    "dünya", yakit=10)
    secimler = iter(["1", "1", "1"])
    mesajlar = []
    hamle = travel(g, lambda _: next(secimler), mesajlar.append)
    assert hamle == 2
    assert "Yakıtın bitti, uzayda sürükleniyorsun…" in mesajlar


# --- Görev 3 -----------------------------------------------------------
def test_boru_hatti_toplam_ve_filtre():
    assert sum(y for _, _, y in ayristir(satirlari_oku(SEYIR))) == 88
    kayitlar = ayristir(satirlari_oku(SEYIR))
    assert [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)] == [
        "sirius", "centauri", "orion", "kara_delik"]


def test_boru_hatti_tembel():
    assert isinstance(satirlari_oku(SEYIR), types.GeneratorType)
    assert isinstance(ayristir(satirlari_oku(SEYIR)), types.GeneratorType)
    assert isinstance(uzun_yolculuklar(ayristir(satirlari_oku(SEYIR)), 10), types.GeneratorType)


# --- Görev 4  ---------------
def test_rota_sayaci():
    say = rota_sayaci(galaksiyi_yukle()["baglantilar"])
    assert (say("dünya", 3), say("dünya", 10), say("dünya", 40)) == (
        10, 1706, 13142230386374)
    assert say.cache_info().hits > 0


# --- Görev 5 -----------------------------------------------------------
def test_istatistik_iki_yol_ayni_sonuc():
    g = galaksiyi_yukle()
    assert ist.adlar_buyuk_mfr(g) == ist.adlar_buyuk_liste(g) == [
        "DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"]
    assert ist.cok_baglantili_mfr(g) == ist.cok_baglantili_liste(g) == [
        "dünya", "centauri", "sirius", "orion"]
    assert ist.toplam_baglanti_reduce(g) == ist.toplam_baglanti_sum(g) == 10


def test_hizli_yolculuk_partial():
    assert ist.hizli_yolculuk(30) == 10
    assert ist.hizli_yolculuk.keywords == {"hiz": 3}
