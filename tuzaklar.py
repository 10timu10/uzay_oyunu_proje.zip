from typing import List, Optional


def yakit_ekle(miktar: int, depo: Optional[List[int]] = None) -> List[int]:
    """Depoya miktar ekler. depo verilmezse HER çağrıda yeni liste açılır.

    Hatalı sürüm: def yakit_ekle(miktar, depo=[])  (varsayılan liste paylaşılır)
    """
    if depo is None:
        depo = []
    depo.append(miktar)
    return depo
