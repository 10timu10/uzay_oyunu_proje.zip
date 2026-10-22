import io
from contextlib import redirect_stdout
from functools import lru_cache

import pytest

from uzay_oyunu import fib_sirasi
from uzay_oyunu.akis import olc_dekoratorlu, rota_sayaci
from uzay_oyunu.dekoratorler import hafiza, log_cagri, say, sinirla, sure_olc
from uzay_oyunu.oyun import galaksi_kur, galaksiyi_yukle, hedef_menusu, yakit_harca


def yakala(fonksiyon, *args, **kwargs):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        sonuc = fonksiyon(*args, **kwargs)
    return sonuc, tampon.getvalue()


# --- Görev 1 -----------------------------------------------------------
def test_sure_olc_sonuc_degismez():
    @sure_olc
    def topla(a, b):
        return a + b

    sonuc, cikti = yakala(topla, 2, 3)
    assert sonuc == 5
    assert cikti.startswith("topla: ") and cikti.strip().endswith("sn")


def test_sure_olc_adli_argumanlar():
    @sure_olc
    def bol(a, b=1):
        return a / b

    sonuc, _ = yakala(bol, b=2, a=10)
    assert sonuc == 5


def test_sure_olc_ad_ve_belge_korunur():
    @sure_olc
    def selam():
        """Selam verir."""

    assert selam.__name__ == "selam"
    assert selam.__doc__ == "Selam verir."


def test_sure_olc_rota_sayacina_uygulanir():
    baglantilar = galaksiyi_yukle()["baglantilar"]
    sonuc, cikti = yakala(olc_dekoratorlu, baglantilar, "dünya", 5)
    assert sonuc == rota_sayaci(baglantilar)("dünya", 5)  # sonuç değişmeden döner
    assert cikti.startswith("rota_sayisi: ")


# --- Görev 2 -----------------------------------------------------------
def test_say_cagri_sayar_ve_ad_korunur():
    @say
    def f():
        """belge"""

    f(), f()
    assert f.cagri == 2
    assert f.__name__ == "f" and f.__doc__ == "belge"


def test_fib_uc_siralama():
    assert fib_sirasi.cagri_sayilari(20) == {
        "yalnızca @say": 21891,
        "@say üstte, @lru_cache altta": 39,
        "@lru_cache üstte, @say altta": 21,
    }


# --- Görev 3 -----------------------------------------------------------
def test_log_cagri_cikti_ve_sonuc():
    @log_cagri
    def yolculuk(gezegen, hiz=1):
        return f"{gezegen} hiz={hiz}"

    sonuc, cikti = yakala(yolculuk, "orion", hiz=3)
    assert sonuc == "orion hiz=3"
    assert cikti.splitlines() == ["-> yolculuk('orion', hiz=3)",
                                  "<- yolculuk = 'orion hiz=3'"]


def test_log_cagri_ad_korunur():
    @log_cagri
    def f():
        """belge"""

    assert f.__name__ == "f" and f.__doc__ == "belge"


def test_log_cagri_galaksi_kur_ve_hedef_menusu():
    g, cikti = yakala(galaksi_kur, ["mars"], {"mars": []}, "mars", yakit=7)
    assert g["yakit"] == 7
    assert cikti.splitlines()[0].startswith("-> galaksi_kur(['mars'], {'mars': []}, 'mars', yakit=7)")
    metin, cikti = yakala(hedef_menusu, ["a"])
    assert metin == "Nereye gitmek istersin?\n[1] a"
    assert "-> hedef_menusu(['a'])" in cikti
    assert hedef_menusu.__name__ == "hedef_menusu"


# --- Görev 5 -----------------------------------------------------------
def test_sinirla_sinir_degerleri():
    assert yakit_harca(0) == 100
    assert yakit_harca(100) == 0


def test_sinirla_normal_deger():
    assert yakit_harca(30) == 70


@pytest.mark.parametrize("deger", [-1, 101, 150])
def test_sinirla_aralik_disi(deger):
    with pytest.raises(ValueError, match="aralığında değil"):
        yakit_harca(deger)


def test_sinirla_hata_mesaji():
    with pytest.raises(ValueError) as hata:
        yakit_harca(150)
    assert str(hata.value) == "yakit_harca: 150 değeri 0-100 aralığında değil"


def test_sinirla_ad_ve_belge_korunur():
    assert yakit_harca.__name__ == "yakit_harca"
    assert "yakıt" in yakit_harca.__doc__


# --- Bonus -------------------------------------------------------------
def test_hafiza_lru_cache_ile_ayni_sonuc():
    @hafiza()
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    @lru_cache(maxsize=None)
    def fib_lru(n):
        return n if n < 2 else fib_lru(n - 1) + fib_lru(n - 2)

    assert [fib(n) for n in range(25)] == [fib_lru(n) for n in range(25)]
    assert len(fib.onbellek) == fib_lru.cache_info().currsize


def test_hafiza_hesap_sayisi_lru_ile_ayni():
    sayac = {"hafiza": 0, "lru": 0}

    @hafiza()
    def f(n):
        sayac["hafiza"] += 1
        return n if n < 2 else f(n - 1) + f(n - 2)

    @lru_cache(maxsize=None)
    def g(n):
        sayac["lru"] += 1
        return n if n < 2 else g(n - 1) + g(n - 2)

    f(20), g(20)
    assert sayac["hafiza"] == sayac["lru"] == 21


def test_hafiza_maxsize_en_eskiyi_siler():
    @hafiza(maxsize=2)
    def kare(n):
        return n * n

    kare(1), kare(2), kare(3)
    assert len(kare.onbellek) == 2
    assert ((1,), ()) not in kare.onbellek  # en eski girdi silindi
    assert kare(3) == 9


def test_hafiza_ad_korunur():
    @hafiza()
    def f(n):
        """belge"""
        return n

    assert f.__name__ == "f" and f.__doc__ == "belge"
