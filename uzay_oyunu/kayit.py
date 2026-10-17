from typing import Any


def gorev_kaydi(
    baslik: str, *adimlar: str, oncelik: str = "normal", **ekler: Any
) -> str:
    """Görev bilgilerini ve adımlarını biçimlendirerek döndürür.

    oncelik yalnızca isimle (keyword-only) geçilebilir.
    """
    satirlar = [f"[{oncelik.upper()}] {baslik}"]
    for idx, adim in enumerate(adimlar, start=1):
        satirlar.append(f"{idx}. {adim}")
    for anahtar, deger in ekler.items():
        satirlar.append(f"{anahtar}: {deger}")
    return "\n".join(satirlar)


if __name__ == "__main__":
    print("--- Normal çağrı ---")
    print(
        gorev_kaydi(
            "Kara deliğe atla",
            "Kredi kazan",
            "Pilot bul",
            "Hiperdrive al",
            oncelik="yüksek",
            sorumlu="Ayşe",
        )
    )

    adim_listesi = ["Kredi kazan", "Pilot bul", "Hiperdrive al"]
    ek_bilgiler = {"sorumlu": "Ayşe"}
    print("\n--- Liste (*) ve sözlük (**) açarak çağrı ---")
    print(
        gorev_kaydi(
            "Kara deliğe atla", *adim_listesi, oncelik="yüksek", **ek_bilgiler
        )
    )
