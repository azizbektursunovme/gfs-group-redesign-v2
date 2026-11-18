# GFS GROUP LLC — sayt redizayni, 2-variant

[gfs-groupllc.com](https://gfs-groupllc.com) uchun ikkinchi dizayn varianti. Asos: ClickUp'dagi "gfs-groupllc.com — redesign" taski.
1-variant alohida repoda: [gfs-group-redesign](https://github.com/azizbektursunovme/gfs-group-redesign).

- Ko'rish havolasi: https://azizbektursunovme.github.io/gfs-group-redesign-v2/
- Repo: https://github.com/azizbektursunovme/gfs-group-redesign-v2

Bu preview: hamma sahifada `noindex` bor, Google'da ko'rinmaydi. Asosiy saytga ko'chirish dasturchi bilan kelishiladi (hozirgi kod: ItSoft-dev/gfs-group-front, Next.js va o'z API'si).

## Dizayn yo'nalishi: "Highway signs"

G'oya AQSh magistral yo'l belgilaridan olingan. Brendning ko'k, qizil va oq ranglari shu belgilarning ranglari.

- **Hero:** katta ko'k yo'l ko'rsatkichi; 4 ta banner "EXIT 1–4" yorliqlari bilan almashadi.
- **Raqamlar:** marshrut qalqonlari (5+, 48, 250+, 24/7).
- **Four Pillars:** ustunga o'rnatilgan oq belgilar.
- **Hamkorlar:** logolar ko'k taxtadagi oq plitalarda.
- **Kontakt:** masofa ko'rsatkichi uslubidagi belgi; hamkor bo'lish qadamlari "MILE 1–4" ustunchalari bilan.
- **Shrift:** Overpass. **Ranglar:** hozirgi saytdan, `#1e3b7e`, `#0f1d3d`, `#e13a40`.

## Tayyor sahifalar

| Sahifa | Fayl |
|---|---|
| Home | `index.html` |
| Why Us | `why-us.html` |
| Services | `services.html` |
| Partners | `partners.html` |
| Reviews | `reviews.html` |
| Contact | `contact-us.html` |
| Privacy Policy | `privacy-policy.html` |
| Terms of Service | `terms-of-service.html` |

## Qanday ishga tushiriladi

Ko'rish uchun hech narsa o'rnatish shart emas: `index.html`ni brauzerda oching yoki lokal server yoqing:

```bash
python -m http.server 4173
```

So'ng http://localhost:4173 ni oching.

Sahifalar `_src/build.py` skripti bilan yig'iladi (Python 3, qo'shimcha kutubxona kerak emas; 3.12 da sinalgan):

```bash
python _src/build.py
```

Matn va ro'yxatlar `_src/data/*.json` fayllarida: jonli sayt API'sidan 2026-11-14 kuni olingan nusxa. HTML fayllarni qo'lda tahrirlamang, skript ularni ustidan yozadi.

## Tuzilishi

- `assets/css/site.css` — hamma stil, bitta fayl
- `assets/js/site.js` — menyu, hero bannerlari, sharhlar filtri, forma
- `assets/img/` — logotip, hero suratlari, hamkor logolari
- `_src/` — build skripti va ma'lumotlar nusxasi

## Contact formasi

Forma hali API'ga ulanmagan va preview rejimida ishlaydi: hech narsa yuborilmaydi.

- Ulash uchun `_src/build.py`dagi formada `data-endpoint` atributiga manzil yoziladi; forma shu manzilga JSON `POST` yuboradi.
- Maydonlarning hozirgi GoHighLevel formasidagi id'lari `data-ghl` atributida turibdi.
- Preview'da `contact-us.html?form=error` "yuborilmadi" holatini ko'rsatadi.

## Tasdiq kutayotgan va qilinmagan ishlar

- To'g'ri kontakt: hozir hamma joyda (636) 442-1334 va info@gfs-groupllc.com. Privacy va Terms'dagi 314-451-1111 va hr@ almashtirilgan; qaysi biri to'g'ri ekanini rahbar aytadi.
- Forma API'si dasturchi bilan kelishiladi.
- Suratlar hozirgi saytniki (600–1280px); kattaroq haqiqiy suratlar kerak.
- Haqiqiy telefonlarda sinalmagan (faqat brauzer emulyatsiyasi).
