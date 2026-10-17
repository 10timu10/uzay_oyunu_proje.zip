import json
from pathlib import Path
from typing import Any, Callable, Dict, List

from uzay_oyunu.akis import yakit_gostergesi
from uzay_oyunu.araclar import hamle_sayaci

VARSAYILAN_DOSYA = Path(__file__).parent / "galaksi.json"
# Her yolculukta göstergeden düşen yakıt (yakit_gostergesi tüketimi)
YOLCULUK_YAKITI = 5
# Hangi gezegende hangi eşya bulunur
GEZEGEN_ESYALARI = {
    "centauri": "credits",
    "sirius": "engines",
    "orion": "copilot",
}


def envanter_metni(credits: bool, engines: bool, copilot: bool) -> str:
    """Mevcut envanter durumuna göre kullanıcıya gösterilecek metni döndürür.

    >>> envanter_metni(True, False, True)
    'Sende: bol kredi, yetenekli bir pilot'
    >>> envanter_metni(False, False, False)
    ''
    """
    esyalar = []
    if credits:
        esyalar.append("bol kredi")
    if engines:
        esyalar.append("güçlü motorlar")
    if copilot:
        esyalar.append("yetenekli bir pilot")

    if not esyalar:
        return ""
    return f"Sende: {', '.join(esyalar)}"


def hedef_menusu(hedefler: List[str]) -> str:
    """Gidilebilecek hedeflerin numaralandırılmış menü metnini döndürür.

    >>> hedef_menusu(["centauri", "sirius"])
    'Nereye gitmek istersin?\\n[1] centauri\\n[2] sirius'
    """
    satirlar = ["Nereye gitmek istersin?"]
    for indeks, hedef in enumerate(hedefler, start=1):
        satirlar.append(f"[{indeks}] {hedef}")
    return "\n".join(satirlar)


def galaksi_kur(
    gezegenler: List[str],
    baglantilar: Dict[str, List[str]],
    baslangic: str,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Galaksiyi doğrulayıp sözlük olarak kurar. yakit verilmezse 50 olur."""
    if baslangic not in gezegenler:
        raise ValueError(f"Başlangıç gezegeni ({baslangic}) gezegenler listesinde yok!")
    return {
        "gezegenler": gezegenler,
        "baglantilar": baglantilar,
        "konum": baslangic,
        "yakit": kwargs.get("yakit", 50),
    }


def galaksiyi_yukle(dosya_yolu: Path | str = VARSAYILAN_DOSYA) -> Dict[str, Any]:
    """JSON dosyasını json.load ile okur ve galaksi_kur(**veri) ile galaksiyi döndürür."""
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        veri = json.load(f)
    return galaksi_kur(**veri)


def travel(
    galaksi: Dict[str, Any],
    girdi: Callable[[str], str] = input,
    yazdir: Callable[[str], None] = print,
) -> int:
    """Oyunu oynatır; kara_delik'e ulaşınca ya da yakıt göstergesi bitince durur.

    girdi ve yazdir parametreleri testte sahte fonksiyon verebilmek içindir.
    Toplam hamle sayısını döndürür.
    """
    sayac = hamle_sayaci()
    hamle = 0
    envanter = {"credits": False, "engines": False, "copilot": False}
    konum = galaksi["konum"]
    yakit = galaksi["yakit"]
    # Üreteç: her next() çağrısı yakıtı YOLCULUK_YAKITI kadar azaltıp kalanı verir
    gosterge = yakit_gostergesi(galaksi["yakit"], YOLCULUK_YAKITI)

    while konum != "kara_delik":
        hedefler = galaksi["baglantilar"][konum]
        yazdir(f"Konum: {konum} | Yakıt: {yakit}")
        metin = envanter_metni(**envanter)
        if metin:
            yazdir(metin)
        yazdir(hedef_menusu(hedefler))

        secim = girdi("> ").strip()
        if not secim.isdigit() or not 1 <= int(secim) <= len(hedefler):
            yazdir("Geçersiz seçim, tekrar dene.")
            continue

        try:
            yakit = next(gosterge)
        except StopIteration:
            yazdir("Yakıtın bitti, uzayda sürükleniyorsun…")
            return hamle

        konum = hedefler[int(secim) - 1]
        hamle = sayac()
        if konum in GEZEGEN_ESYALARI:
            envanter[GEZEGEN_ESYALARI[konum]] = True

    yazdir(f"Oyunu {hamle} hamlede bitirdin!")
    return hamle


if __name__ == "__main__":
    travel(galaksiyi_yukle())