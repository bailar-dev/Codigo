# Codigo təqdimat demosu

Mövcud MVP-yə oyunvari öyrənmə yolu, iki giriş seçimi, 8 mövzu üzrə 24 interaktiv məşq, kapibara mesajları və gündəlik hədəf əlavə edilib.

## İşə salmaq

```powershell
python site/build.py
python -m http.server 8765 --bind 127.0.0.1 --directory site
```

Brauzerdə `http://127.0.0.1:8765/` açın. Xarici React, Tailwind, Skulpt, ikon və şrift resursları üçün internet bağlantısı lazımdır.

## Təqdimat axını

1. Ana səhifədə ulduz məşqini sınayın; səhv və düzgün cavabın fərqini göstərin.
2. “Öyrənməyə başla” → ad → “Özüm öyrənirəm”.
3. Qısa səviyyə testini tamamlayın. Düz cavab veriləndə daha çətin sual gəlir.
4. Yol xəritəsində interaktiv dərsi açın. Bir səhv cavab verin; sual dərsin sonunda yenidən gələcək.
5. Dərsi tamamlayın: 50 XP, günlük hədəf, streak və təbrik ekranı.
6. “Kodu özün yaz” ilə Python labına keçin, kodu yazıb testləri işlədin.
7. Profil → çıxış. Müəllim adı ilə “Müəlliməm” girişini seçin. Material və tapşırıqları idarə edin.
8. Başqa şagird adı ilə “Siniflə öyrənirəm” → `CODIGO`. Eyni brauzerdə müəllimin dərs planı və təsdiqlədiyi əlavə lablar görünür.

## Mənbələr və yoxlamalar

- `app/codego-app.html`: tətbiqin əsas mənbə fraqmenti.
- `app/journey.js`, `app/journey.css`: yeni giriş, dərs və yol interfeysi.
- `site/home.html`, `site/play.css`: yeni ana səhifə.
- `site/build.py`: səhifələri yaradır, tətbiqi və aktivlərini `site/` qovluğuna köçürür. Yaradılmış `site/app.html` faylını birbaşa dəyişməyin.
- `node app/checks.cjs`: streak, XP, modul keçidləri, profil ayrılması və demo sinif paylaşımını yoxlayır.

## Demo sərhədləri

Hesablar parolsuzdur və yalnız cari brauzerdə saxlanılır. Sinif kodu nümayiş üçündür. AI tutor qaydalara və əvvəlcədən yazılmış ipuclarına əsaslanır; materialdan sərbəst AI tapşırıq generasiyası yoxdur. Müəllimin mətnindən həftəlik plan çıxarılır, hazır tapşırıq şablonları yoxlanıb təsdiqlənir. Python kodu brauzerdə işləyir. Pilot forması real müraciət göndərmir.

Əvvəlki v1 demo məlumatları silinmir; yeni profil sistemi ayrıca v2 saxlama açarından istifadə edir.
