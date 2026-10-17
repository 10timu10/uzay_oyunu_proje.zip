import pytest

from uzay_oyunu.araclar import en_bagli_gezegenler, hamle_sayaci
from uzay_oyunu.kayit import gorev_kaydi
from uzay_oyunu.oyun import (
    envanter_metni, galaksi_kur, galaksiyi_yukle, hedef_menusu, travel,
)


def test_envanter_dolu():
    assert envanter_metni(True, False, True) == "Sende: bol kredi, yetenekli bir pilot"


def test_envanter_bos():
    assert envanter_metni(False, False, False) == ""


def test_hedef_menusu():
    assert hedef_menusu(["centauri", "sirius"]) == (
        "Nereye gitmek istersin?\n[1] centauri\n[2] sirius"
    )


def test_gorev_kaydi():
    sonuc = gorev_kaydi("Görev", "a", "b", oncelik="yüksek", sorumlu="Ayşe")
    assert sonuc == "[YÜKSEK] Görev\n1. a\n2. b\nsorumlu: Ayşe"


def test_oncelik_sadece_isimle():
    assert gorev_kaydi("G", "yüksek").startswith("[NORMAL]")


def test_galaksi_dosyadan():
    g = galaksiyi_yukle()
    assert (g["konum"], g["yakit"]) == ("dünya", 100)


def test_yakit_varsayilan():
    assert galaksi_kur(["mars"], {"mars": []}, "mars")["yakit"] == 50


def test_gecersiz_baslangic():
    with pytest.raises(ValueError):
        galaksi_kur(["mars"], {"mars": []}, "venus")


def test_hamle_sayaci():
    s = hamle_sayaci()
    assert (s(), s(), s()) == (1, 2, 3)


def test_en_bagli_gezegenler():
    assert en_bagli_gezegenler(galaksiyi_yukle()) == [
        "sirius", "centauri", "dünya", "orion", "kara_delik",
    ]


def test_travel_kara_deliğe_ulasir():
    # dünya -> centauri(1) -> sirius(1) -> kara_delik(1)
    secimler = iter(["1", "1", "1"])
    mesajlar = []
    hamle = travel(galaksiyi_yukle(), lambda _: next(secimler), mesajlar.append)
    assert hamle == 3
    assert "Oyunu 3 hamlede bitirdin!" in mesajlar


def test_travel_gecersiz_secim_hamle_saymaz():
    secimler = iter(["9", "x", "1", "1", "1"])
    hamle = travel(galaksiyi_yukle(), lambda _: next(secimler), lambda m: None)
    assert hamle == 3
