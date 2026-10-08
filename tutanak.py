#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kargo kapıya bırakıldı tutanak motoru.

Çalışır. Bir şey teslim etmez. Sadece suçu dağıtır.
"""

from __future__ import annotations

import argparse
import hashlib
import random
from datetime import datetime

TARAFLAR = [
    "kurye",
    "kapı",
    "zil",
    "paspas",
    "bir yakınınıza teslim edildi cümlesi",
    "ekranda duran sen",
    "komşunun kedisi",
    "asansör aynası",
    "boş kutu iddiası",
]

GEREKCELER = [
    "görüntü kaydı yok, hafıza da yok, sadece bildirim var",
    "zil çalmış ama kimse duymamış; bu bir tanıklık değil, bir bahanedir",
    "paspas yerinde, kutu değil; paspas ifade vermeyi reddetti",
    "kutu ağır denmiş, kapı hafif kalmış",
    "teslim saati çay saatiyle çakışmış, bu hukuken ağırlaştırıcıdır",
    "takip numarasi gerçek görünüyor, bu yeterli delil sayılmaz",
]

KARARLAR = [
    "Kutu hükmen kapıdadır. Fiilen mutfaktadır. İkisi ayrı şeydir.",
    "Teslim geçerlidir, alıcı geçersizdir.",
    "Duruşma, zil bir daha çalana kadar ertelenmiştir.",
    "Suçlu bulunamamıştır. Suç paspasa havale edilmiştir.",
    "Kargo firması değil, cümlenin kendisi tazminat ödeyecektir.",
]


def tohum(takip: str) -> random.Random:
    ozet = hashlib.sha256(takip.encode("utf-8")).hexdigest()
    return random.Random(int(ozet[:12], 16))


def paylastir(rng: random.Random) -> list[tuple[str, int]]:
    agirliklar = [rng.randint(1, 40) for _ in TARAFLAR]
    toplam = sum(agirliklar)
    paylar = [(t, round(a * 100 / toplam)) for t, a in zip(TARAFLAR, agirliklar)]
    fark = 100 - sum(p for _, p in paylar)
    isim, deger = paylar[0]
    paylar[0] = (isim, deger + fark)
    return sorted(paylar, key=lambda x: -x[1])


def tutanak_yaz(takip: str, kapi: str, kutu: str) -> str:
    rng = tohum(takip)
    paylar = paylastir(rng)
    gerekce = rng.sample(GEREKCELER, 3)
    karar = rng.choice(KARARLAR)
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    satirlar = [
        "KARGO KAPIYA BIRAKILDI TUTANAGI",
        f"Dosya: {takip}",
        f"Tarih: {simdi}",
        f"Kapı: {kapi}",
        f"Kutu tarifi: {kutu}",
        "",
        "Sorumluluk payları:",
    ]
    for taraf, yuzde in paylar:
        cubuk = "#" * max(1, yuzde // 5)
        satirlar.append(f"  {yuzde:3d}%  {cubuk}  {taraf}")
    satirlar.append("")
    satirlar.append("Gerekçeler:")
    for i, g in enumerate(gerekce, 1):
        satirlar.append(f"  {i}. {g}")
    satirlar.append("")
    satirlar.append(f"KARAR: {karar}")
    satirlar.append("")
    satirlar.append("Bu tutanak bağlayıcı değildir. Kutu da değildir.")
    satirlar.append("---")
    satirlar.append("DAMGA: Mühür No. 08-10-2026-KAPI-BOS")
    satirlar.append("İMZA: Kayyum Grok (kaşe ciddi, mürekkep değil)")
    satirlar.append("TARİH: 8 Ekim 2026")
    satirlar.append("İSİM: Tentivory adına Kayyum Grok")
    return "\n".join(satirlar)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Kapıya bırakıldı iddiasını tutanağa döker."
    )
    parser.add_argument("takip", nargs="?", default="", help="Takip numarasi")
    parser.add_argument("--kapi", default="sol kanat, paspaslı")
    parser.add_argument("--kutu", default="küçük görünüp ağır çıkan")
    args = parser.parse_args()
    takip = args.takip.strip() or "UYDURMA-" + datetime.now().strftime("%H%M%S")
    print(tutanak_yaz(takip, args.kapi, args.kutu))


if __name__ == "__main__":
    main()

# damga satiri: Kayyum Grok, 8 Ekim 2026, Tentivory. Ciddi kaşe, ciddiyetsiz dosya.
