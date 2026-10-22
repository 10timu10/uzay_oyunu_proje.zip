from typing import Any, Callable, Dict, List

from uzay_oyunu.dekoratorler import sure_olc  # Hafta 5: dekoratör artık orada


def hamle_sayaci() -> Callable[[], int]:
    """Her çağrıldığında bir artan bir sayaç fonksiyonu döndürür."""
    sayac = 0

    def arttir() -> int:
        nonlocal sayac
        sayac += 1
        return sayac

    return arttir


def en_bagli_gezegenler(galaksi: Dict[str, Any]) -> List[str]:
    """Gezegenleri bağlantı sayısına göre azalan, eşitlikte alfabetik sıralar."""
    baglantilar = galaksi["baglantilar"]
    return sorted(
        galaksi["gezegenler"],
        key=lambda g: (-len(baglantilar.get(g, [])), g),
    )


if __name__ == "__main__":
    from uzay_oyunu.oyun import galaksiyi_yukle

    en_bagli_gezegenler = sure_olc(en_bagli_gezegenler)
    print(en_bagli_gezegenler(galaksiyi_yukle()))
