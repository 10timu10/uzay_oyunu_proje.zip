import pytest

from uzay_oyunu.komutlar import (KOMUTLAR, envanter, harita, komut,
                                 komut_calistir, komut_mu, yardim)
from uzay_oyunu.oyun import galaksiyi_yukle, travel

DURUM = {"konum": "dünya",
         "baglantilar": {"dünya": ["orion", "dünya", "kara_delik"]},
         "credits": True, "engines": False, "copilot": True}


def test_kayit_fonksiyonu_degistirmez():
    fonksiyon, aciklama = KOMUTLAR["yardim"]
    assert fonksiyon is yardim  # sarmalanmadı
    assert aciklama == "komutları listeler"


def test_ayni_ad_iki_kez_value_error():
    with pytest.raises(ValueError):
        @komut("harita", "kopya")
        def baska(durum):
            pass


def test_yardim():
    cikti = yardim(DURUM)
    assert cikti.splitlines() == [
        "envanter  eşyalarını gösterir",
        "harita    gidebileceğin gezegenleri gösterir",
        "yardim    komutları listeler",
    ]


def test_envanter():
    assert envanter(DURUM) == "credits: var, engines: yok, copilot: var"


def test_harita():
    assert harita(DURUM) == "orion, dünya, kara_delik"


def test_harita_liste_bicimi():
    assert harita(dict(DURUM, baglantilar=["orion", "dünya"])) == "orion, dünya"


def test_komut_mu_ve_calistir():
    assert komut_mu("harita") and komut_mu(" yardim ")
    assert not komut_mu("orion") and not komut_mu("1")
    assert komut_calistir("harita", DURUM) == "orion, dünya, kara_delik"


def test_travel_komutu_calistirir_ve_menuyu_tekrar_gosterir():
    secimler = iter(["harita", "envanter", "yardim", "1", "1", "1"])
    mesajlar = []
    hamle = travel(galaksiyi_yukle(), lambda _: next(secimler), mesajlar.append)
    assert hamle == 3  # komutlar hamle sayılmadı
    assert "centauri, orion" in mesajlar  # dünya'nın komşuları
    assert "credits: yok, engines: yok, copilot: yok" in mesajlar
    assert sum(m.startswith("Nereye gitmek istersin?") for m in mesajlar) == 6


def test_travel_komut_olmayan_girdi_eskisi_gibi():
    secimler = iter(["orion_", "1", "1", "1"])
    mesajlar = []
    travel(galaksiyi_yukle(), lambda _: next(secimler), mesajlar.append)
    assert "Geçersiz seçim, tekrar dene." in mesajlar
