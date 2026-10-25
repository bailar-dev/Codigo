# Codigo saytının səhifələrini ortaq başlıq, menyu və footer ilə yaradır.
# İşə salmaq: python build.py  (site qovluğunda)
import io
import os
import shutil
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
PLATFORM = "app.html"
DEMO = "muellim-demo.html"

PAGES = [
    # (fayl, menyu adı, ikon)
    ("index.html", "Ana səhifə", "house"),
    ("haqqimizda.html", "Haqqımızda", "book-open"),
    ("missiya.html", "Missiya", "compass"),
    ("nece-isleyir.html", "Necə işləyir", "route"),
    ("imkanlar.html", "İmkanlar", "sparkles"),
    ("kimler-ucun.html", "Kimlər üçün", "users"),
    ("qiymetler.html", "Qiymətlər", "wallet"),
    ("suallar.html", "Suallar", "message-circle-question"),
]

SPRITE = ""

HEAD_ASSETS = """<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Montserrat:wght@600;800&family=Nunito:wght@400;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="play.css">
<link rel="stylesheet" href="pricing.css">
<link rel="stylesheet" href="team.css">
<script src="https://unpkg.com/lucide@0.460.0/dist/umd/lucide.min.js"></script>"""


def nav(current):
    links = "\n".join(
        f'      <a href="{f}"{" aria-current=\"page\"" if f == current else ""}>{name}</a>'
        for f, name, _ in PAGES
    )
    mobile = "".join(
        f'<a href="{f}"{" aria-current=\"page\"" if f == current else ""}><i data-lucide="{ic}"></i>{name}</a>'
        for f, name, ic in PAGES
    )
    return f"""<header class="nav wrap">
  <div class="inner bar">
    <a class="brand" href="index.html" aria-label="Codigo ana səhifə"><img aria-hidden="true" src="icon.webp" alt=""><b class="wordmark">CODIGO<small>Sənin kod yoldaşın</small></b></a>
    <nav class="links" aria-label="Səhifələr">
{links}
    </nav>
    <a class="btn primary" href="{PLATFORM}">Platformanı sına <i data-lucide="arrow-right"></i></a>
    <button class="menu-btn" id="menuBtn" aria-label="Menyunu aç" aria-expanded="false" aria-controls="mobileMenu"><i data-lucide="menu"></i></button>
  </div>
  <div class="inner mobile-menu" id="mobileMenu">{mobile}<a class="btn primary" href="{PLATFORM}">Platformanı sına</a></div>
</header>"""


def page_hero(crumb, title, lead, badge_icon, badge_text):
    return f"""<section class="page-hero wrap">
  <div class="inner">
    <div>
      <nav class="crumbs" aria-label="Yol"><a href="index.html">Ana səhifə</a><i data-lucide="chevron-right"></i><span>{crumb}</span></nav>
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
    </div>
    <div class="ph-art" aria-hidden="true"><span class="disc"></span><img class="capy" aria-hidden="true" src="icon.webp" alt=""><span class="badge"><i data-lucide="{badge_icon}"></i>{badge_text}</span></div>
  </div>
</section>"""


def pager(current):
    files = [p[0] for p in PAGES]
    i = files.index(current)
    prev_ = PAGES[i - 1] if i > 0 else None
    next_ = PAGES[i + 1] if i < len(PAGES) - 1 else None
    out = '<section class="sec tight wrap"><div class="inner pager">'
    if prev_:
        out += f'<a href="{prev_[0]}"><small><i data-lucide="arrow-left"></i>Əvvəlki</small><b>{prev_[1]}</b></a>'
    if next_:
        out += f'<a class="next" href="{next_[0]}"><small>Növbəti<i data-lucide="arrow-right"></i></small><b>{next_[1]}</b></a>'
    return out + "</div></section>"


END_CTA = f"""<section class="end-cta wrap">
  <div class="inner box">
    <img aria-hidden="true" src="icon.webp" alt="">
    <div><h2>Codigo-nu öz dərsinizdə sınayın</h2><p>Pilot proqrama ilk müəssisələri qəbul edirik. Planlaşdırılan pilot: 30 gün, 25 şagirdədək, 2 müəllim.</p></div>
    <div class="cta-row"><a class="btn white" href="{PLATFORM}"><i data-lucide="play"></i>Platformanı sına</a><a class="btn outline-white" href="suallar.html#pilot">Pilota müraciət</a></div>
  </div>
</section>"""

FOOTER = f"""<footer class="site wrap">
  <div class="inner">
    <div class="fgrid">
      <div><a class="brand" href="index.html" aria-label="Codigo"><img aria-hidden="true" src="icon.webp" alt=""><b class="wordmark">CODIGO<small>Sənin kod yoldaşın</small></b></a><p>Proqramlaşdırmanı müəllimin öz materialından, hər şagirdin öz tempində öyrədən platforma.</p></div>
      <div><h4>Səhifələr</h4><ul>{"".join(f'<li><a href="{f}">{n}</a></li>' for f, n, _ in PAGES[1:])}</ul></div>
      <div><h4>Platforma</h4><ul><li><a href="haqqimizda.html#komanda">Qurucular və komanda</a></li><li><a href="{PLATFORM}">Şagird platforması</a></li><li><a href="{DEMO}">Müəllim demosu</a></li><li><a href="suallar.html#pilot">Pilot proqram</a></li></ul></div>
    </div>
    <div class="fbottom"><span>© 2026 Codigo · Bakı</span><span>Məktəblər, universitetlər və IT kursları üçün</span></div>
  </div>
</footer>"""


def render(current, title, body, full_doc=True):
    page = f"""<title>{title}</title>
{HEAD_ASSETS}
{SPRITE}
{nav(current)}
<main>
{body}
</main>
{"" if current in ("suallar.html", "index.html", "qiymetler.html") else END_CTA}
{FOOTER}
<script src="site.js"></script>
<script src="pricing.js"></script>
"""
    if not full_doc:
        return page
    head_end = page.index(HEAD_ASSETS) + len(HEAD_ASSETS)
    return ('<!doctype html>\n<html lang="az" data-theme="light">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            + page[:head_end] + '</head>\n<body>\n' + page[head_end:] + "</body>\n</html>\n")


# ---------------- Ana səhifə ----------------
HOME = f"""<section class="hero wrap">
  <div class="inner">
    <div class="hero-copy">
      <span class="pill"><span class="dot"></span>Məktəblər, universitetlər və IT kursları üçün</span>
      <h1>Proqramlaşdırmanı <span class="hl">oynaya-oynaya</span> öyrən</h1>
      <p class="lead">Codigo müəllimin öz dərs materialından hər şagird üçün fərdi kvestlər hazırlayır. AI tutor səhvini tapır və izah edir, amma kodu sənin yerinə yazmır.</p>
      <div class="cta-row">
        <a class="btn primary" href="{PLATFORM}"><i data-lucide="play"></i>Platformanı sına</a>
        <a class="btn ghost" href="haqqimizda.html">Codigo nədir?</a>
      </div>
      <div class="trust">
        <span><i data-lucide="circle-check"></i>Python, C++, Java</span>
        <span><i data-lucide="circle-check"></i>Azərbaycan dilində</span>
        <span><i data-lucide="circle-check"></i>Quraşdırma tələb etmir</span>
      </div>
    </div>
    <div class="stage" aria-label="Codigo maskotu kapibara və platformadan nümunələr">
      <div class="tile"><img class="mascot" aria-hidden="true" src="icon.webp" alt=""></div>
      <div class="chip xp"><span class="ic"><i data-lucide="trophy"></i></span><div>Kvest tamamlandı<small>+250 XP · Dövrlər</small></div></div>
      <div class="chip streak"><span class="ic"><i data-lucide="flame"></i></span><div>7 gün<small>ardıcıl öyrənmə</small></div></div>
      <div class="bubble"><b><i data-lucide="sparkles"></i>AI ipucu</b>range(5) hansı ədədləri qaytarır? Bir yoxla, sonra davam et.</div>
      <div class="codecard"><span class="k">for</span> i <span class="k">in</span> <span class="f">range</span>(<span class="n">5</span>):<br>&nbsp;&nbsp;&nbsp;&nbsp;<span class="f">shield</span>(i)</div>
    </div>
  </div>
</section>

<section class="stats wrap" aria-label="Codigo rəqəmlərlə">
  <div class="inner">
    <div class="stat"><b>3</b><span>proqramlaşdırma dili</span></div>
    <div class="stat"><b>4</b><span>addımda materialdan kvestə</span></div>
    <div class="stat"><b>3</b><span>müəllimin seçdiyi AI rejimi</span></div>
    <div class="stat"><b>100%</b><span>Azərbaycan dilində</span></div>
  </div>
</section>

<section class="sec wrap">
  <div class="inner">
    <div class="head center">
      <span class="kicker"><i data-lucide="compass"></i>Codigo bir baxışda</span>
      <h2>Hər şey bir platformada</h2>
      <p class="lead">Hər bölmə haqqında ətraflı məlumat ayrıca səhifədədir.</p>
    </div>
    <div class="grid g3">
      <a class="card" href="haqqimizda.html"><span class="ic blue"><i data-lucide="book-open"></i></span><h3>Haqqımızda</h3><p>Codigo nədir, niyə yarandı və maskotumuz kapibara nəyi təmsil edir.</p><span class="link">Ətraflı <i data-lucide="arrow-right"></i></span></a>
      <a class="card" href="missiya.html"><span class="ic capy"><i data-lucide="compass"></i></span><h3>Missiya və məqsədlər</h3><p>Missiyamız, vizyonumuz, 6 məqsədimiz və 2027 hədəflərimiz.</p><span class="link">Ətraflı <i data-lucide="arrow-right"></i></span></a>
      <a class="card" href="nece-isleyir.html"><span class="ic mint"><i data-lucide="route"></i></span><h3>Necə işləyir</h3><p>Müəllim və şagird üçün addım-addım axın, AI rejimləri və fərdi yol.</p><span class="link">Ətraflı <i data-lucide="arrow-right"></i></span></a>
      <a class="card" href="imkanlar.html"><span class="ic blue"><i data-lucide="sparkles"></i></span><h3>İmkanlar</h3><p>Öyrənmə yolu, AI tutor, oyun kvestləri, kod redaktoru və müəllim paneli.</p><span class="link">Ətraflı <i data-lucide="arrow-right"></i></span></a>
      <a class="card" href="kimler-ucun.html"><span class="ic capy"><i data-lucide="users"></i></span><h3>Kimlər üçün</h3><p>Məktəblər, universitetlər, IT kursları və qiymət planları.</p><span class="link">Ətraflı <i data-lucide="arrow-right"></i></span></a>
      <a class="card" href="suallar.html"><span class="ic mint"><i data-lucide="message-circle-question"></i></span><h3>Suallar və pilot</h3><p>Ən çox verilən suallar və pilot proqrama müraciət forması.</p><span class="link">Ətraflı <i data-lucide="arrow-right"></i></span></a>
    </div>
  </div>
</section>

<section class="sec alt wrap">
  <div class="inner preview">
    <div class="head" style="margin-bottom:0">
      <span class="kicker"><i data-lucide="monitor-play"></i>Platforma</span>
      <h2>Şagird belə işləyir</h2>
      <p class="lead">Solda öyrənmə yolu və AI tutor, mərkəzdə kvest və kod redaktoru, altda terminal. Kodu işə salanda testlər yoxlanır, XP qazanılır.</p>
      <ul class="ticks">
        <li><i data-lucide="circle-check"></i>Səhvə görə AI diaqnozu və yeni kvest</li>
        <li><i data-lucide="circle-check"></i>Kodu dəyişəndə nəticə də dəyişir</li>
        <li><i data-lucide="circle-check"></i>XP, səviyyə və ardıcıllıq sayğacı</li>
      </ul>
      <div class="cta-row" style="margin-top:8px">
        <a class="btn primary" href="{PLATFORM}"><i data-lucide="play"></i>Şagird platforması</a>
        <a class="btn ghost" href="{DEMO}">Müəllim demosu</a>
      </div>
    </div>
    <div class="ide" aria-label="Codigo şagird platformasının görünüşü">
      <div class="ide-top"><span class="lg"><img aria-hidden="true" src="icon.webp" alt="">Codigo</span><span class="lv">Səviyyə 5 · Coder</span><span class="xpb"><i></i></span><span class="fl">🔥 7</span></div>
      <div class="ide-body">
        <div class="ide-side">
          <span class="lb">Öyrənmə yolu</span>
          <span class="inode d"><i></i>Dəyişənlər</span><span class="inode d"><i></i>Şərtlər</span><span class="inode a"><i></i>Dövrlər</span><span class="inode l"><i></i>Siyahılar</span><span class="inode l"><i></i>Funksiyalar</span>
          <div class="ai-msg"><b>AI diaqnoz</b>Dünən range(1, n) yazmısan və son ədəd düşmədi. Sənə yeni kvest təyin etdim.</div>
        </div>
        <div class="ide-main">
          <div class="ide-q"><small>KVEST 3.2 · +250 XP</small><div>5 enerji qalxanı yarat</div></div>
<pre><span class="c"># Kvest 3.2</span>
shields = []

<span class="k">for</span> i <span class="k">in</span> <span class="b">range</span>(<span class="n">5</span>):
    shields.append(<span class="s">f"Qalxan-{{i + 1}}"</span>)
    <span class="b">print</span>(<span class="s">f"Qalxan-{{i + 1}} aktivləşdi"</span>)</pre>
          <div class="ide-term"><span class="p">PS C:\\Codigo&gt;</span> python shields.py<br><span class="ok">✔ 3/3 test · Kvest tamamlandı · +250 XP</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec wrap">
  <div class="inner">
    <div class="head">
      <span class="kicker"><i data-lucide="route"></i>Necə işləyir</span>
      <h2>Sillabusdan fərdi kvestə dörd addım</h2>
    </div>
    <div class="steps">
      <div class="step"><span class="num">1</span><span class="who">Müəllim</span><h3>Materialı yükləyir</h3><p>Sillabus, slayd və ya PDF. Codigo mövzuları və həftəlik planı özü çıxarır.</p></div>
      <div class="step"><span class="num">2</span><span class="who">Codigo</span><h3>Tapşırıqlar hazırlanır</h3><p>Hər mövzu üçün lab, test və kvestlər yaranır. Müəllim baxıb təsdiqləyir.</p></div>
      <div class="step"><span class="num">3</span><span class="who">Şagird</span><h3>Giriş testindən keçir</h3><p>Qısa adaptiv test səviyyəni müəyyən edir və şagirdə öz yolunu qurur.</p></div>
      <div class="step"><span class="num">4</span><span class="who">Şagird + AI</span><h3>Kod yazır, inkişaf edir</h3><p>Kvestləri həll edir, AI-dən ipucu alır. Səhvlərinə görə yolu yenilənir.</p></div>
    </div>
    <div style="margin-top:28px"><a class="link" href="nece-isleyir.html">Ətraflı axın və AI rejimləri <i data-lucide="arrow-right"></i></a></div>
  </div>
</section>

<section class="sec tight wrap">
  <div class="inner speech">
    <img aria-hidden="true" src="icon.webp" alt="">
    <div><blockquote>“Səhvini birlikdə tapacağıq. Amma kodu sənin yerinə yazmayacağam, çünki öyrənmək sənin işindir.”</blockquote><cite>Codigo-nun AI tutoru</cite></div>
  </div>
</section>
"""

# ---------------- Haqqımızda ----------------
ABOUT = page_hero("Haqqımızda", "Codigo nədir?", "Proqramlaşdırma dərslərini hər şagird üçün fərdiləşdirən, Azərbaycanda yaradılan təhsil platforması.", "heart", "Bakıda yaradılır") + """
<section class="sec wrap">
  <div class="inner grid g2" style="gap:56px;align-items:start">
    <div class="prose">
      <span class="kicker"><i data-lucide="book-open"></i>Hekayəmiz</span>
      <h2>Niyə Codigo yarandı?</h2>
      <p>Proqramlaşdırma dərslərində eyni mənzərəni görürük: müəllim hər həftə saatlarla tapşırıq və test hazırlayır, bütün sinif eyni tapşırığı alır, bir qrup şagird darıxır, digəri isə geridə qalır. Üstəlik ChatGPT kimi alətlər hazır kodu bir saniyədə verir və şagird heç nə öyrənmədən tapşırığı təhvil verir.</p>
      <p>Bazardakı xarici platformalar öz hazır kurslarını satır. Onlar müəllimin proqramına uyğun gəlmir və Azərbaycan dilində deyil.</p>
      <p><strong>Codigo</strong> bu boşluğu doldurmaq üçün yaranıb. Müəllim öz materialını yükləyir, platforma bu materialdan gündəlik tapşırıqlar, testlər və oyun kvestləri hazırlayır. Hər şagird öz səviyyəsindən başlayır, səhvlərinə görə yolu dəyişir, AI isə müəllim kimi izah edir, amma şagirdin yerinə kod yazmır.</p>
    </div>
    <div class="grid" style="gap:14px">
      <div class="card" style="flex-direction:row;align-items:flex-start;gap:16px"><span class="ic blue"><i data-lucide="route"></i></span><div><h3>Fərdi yol</h3><p>Hamıya eyni tapşırıq yox. Hər şagird öz səviyyəsindən başlayır və öz tempi ilə irəliləyir.</p></div></div>
      <div class="card" style="flex-direction:row;align-items:flex-start;gap:16px"><span class="ic capy"><i data-lucide="gamepad-2"></i></span><div><h3>Praktika və oyun</h3><p>Nəzəriyyəni əzbərləmək yox, kod yazaraq öyrənmək. Kvestlər, XP və nailiyyətlər motivasiyanı saxlayır.</p></div></div>
      <div class="card" style="flex-direction:row;align-items:flex-start;gap:16px"><span class="ic mint"><i data-lucide="heart-handshake"></i></span><div><h3>Müəllim mərkəzdə</h3><p>AI müəllimi əvəz etmir, onun işini yüngülləşdirir. Hər tapşırığı müəllim təsdiqləyir.</p></div></div>
    </div>
  </div>
</section>

<section class="sec alt wrap">
  <div class="inner grid g2" style="gap:48px;align-items:center">
    <div style="background:var(--tint);border-radius:32px;padding:32px;display:grid;place-items:center"><img style="width:min(320px,100%)" aria-hidden="true" src="icon.webp" alt=""></div>
    <div class="prose">
      <span class="kicker"><i data-lucide="smile"></i>Maskotumuz</span>
      <h2>Niyə kapibara?</h2>
      <p>Kapibara dünyanın ən sakit və mehriban heyvanı kimi tanınır. Hər kəslə yola gedir, tələsmir və heç vaxt əsəbiləşmir. Codigo-nun şagirdə münasibəti də belə olmalıdır.</p>
      <div class="grid" style="gap:12px;margin-top:6px">
        <div class="card" style="padding:18px;flex-direction:row;gap:14px;align-items:center"><span class="ic sm capy"><i data-lucide="hourglass"></i></span><div><h4>Səbirli</h4><p style="font-size:0.94rem">Səhv etmək normaldır. Codigo cəzalandırmır, yenidən cəhd etməyə həvəsləndirir.</p></div></div>
        <div class="card" style="padding:18px;flex-direction:row;gap:14px;align-items:center"><span class="ic sm blue"><i data-lucide="code"></i></span><div><h4>Fokuslu</h4><p style="font-size:0.94rem">Kapüşon, f() və açıq düymə: kapibaramız kod yazmağa hazırdır və şagirdi də buna dəvət edir.</p></div></div>
        <div class="card" style="padding:18px;flex-direction:row;gap:14px;align-items:center"><span class="ic sm mint"><i data-lucide="users"></i></span><div><h4>Hamı ilə dost</h4><p style="font-size:0.94rem">Zəif və ya güclü, hər şagird üçün öz yolu var. Heç kim kənarda qalmır.</p></div></div>
      </div>
    </div>
  </div>
</section>

<section class="sec wrap">
  <div class="inner">
    <div class="head center"><span class="kicker"><i data-lucide="gem"></i>Dəyərlərimiz</span><h2>Bizi nə istiqamətləndirir</h2></div>
    <div class="grid g4">
      <div class="card"><span class="ic blue"><i data-lucide="code"></i></span><h3>Praktika birinci</h3><p>Hər mövzu real kod yazmaqla bağlanır.</p></div>
      <div class="card"><span class="ic capy"><i data-lucide="heart-handshake"></i></span><h3>Müəllimə hörmət</h3><p>Son söz həmişə müəllimindir.</p></div>
      <div class="card"><span class="ic mint"><i data-lucide="eye"></i></span><h3>Şəffaf AI</h3><p>AI nə etdiyini və niyə etdiyini göstərir.</p></div>
      <div class="card"><span class="ic rose"><i data-lucide="accessibility"></i></span><h3>Hamı üçün</h3><p>Brauzerdə, quraşdırmasız, yerli qiymətlə.</p></div>
    </div>
  </div>
</section>
"""

# ---------------- Missiya ----------------
MISSION = page_hero("Missiya", "Missiya və məqsədlərimiz", "Niyə Codigo-nu qururuq və hansı nəticələrə çatmaq istəyirik.", "target", "6 məqsəd") + """
<section class="sec wrap">
  <div class="inner grid g2">
    <div class="mv-card m"><span class="tag"><i data-lucide="target"></i>Missiyamız</span><p>Azərbaycanda hər şagirdin proqramlaşdırmanı öz dilində, öz tempində və praktika ilə öyrənməsini təmin etmək.</p></div>
    <div class="mv-card v"><span class="tag"><i data-lucide="eye"></i>Vizyonumuz</span><p>Kod dərsinin hər sinifdə fərdi, maraqlı və nəticəsi ölçülə bilən olduğu bir təhsil sistemi.</p></div>
  </div>
</section>

<section class="sec alt wrap">
  <div class="inner">
    <div class="head"><span class="kicker"><i data-lucide="flag"></i>Məqsədlərimiz</span><h2>Altı məqsəd, hər birinin ölçüsü ilə</h2></div>
    <div class="grid g3 goals">
      <div class="card goal"><h3>Müəllimin vaxtına qənaət</h3><p>Lab və test hazırlamaq hər həftə saatlar aparır. Codigo bunu müəllimin öz materialından avtomatik edir.</p><span class="metric"><i data-lucide="zap"></i>Hədəf: lab hazırlığı dəqiqələrlə</span></div>
      <div class="card goal"><h3>Heç kim geridə qalmasın</h3><p>Zəif şagird əlavə dəstək, güclü şagird çətin tapşırıq alır. Müəllim kimin harada ilişdiyini dərhal görür.</p><span class="metric"><i data-lucide="users"></i>Hədəf: hər şagirdə öz yolu</span></div>
      <div class="card goal"><h3>AI köməkçi olsun, köçürmə aləti yox</h3><p>AI hazır cavab vermir. Sual verir, səhvin yerinə işarə edir və şagirdi düşündürür.</p><span class="metric"><i data-lucide="shield-check"></i>Hədəf: AI rejimini müəllim seçir</span></div>
      <div class="card goal"><h3>Ana dilində keyfiyyətli təhsil</h3><p>İzahlar, ipucları və interfeys Azərbaycan dilindədir. Dil maneəsi proqramlaşdırmaya maneə olmamalıdır.</p><span class="metric"><i data-lucide="languages"></i>Hədəf: tam Azərbaycan dili</span></div>
      <div class="card goal"><h3>Praktik bacarıq</h3><p>Hər mövzu real kod yazmaqla bağlanır. Şagird sintaksisi yox, problemi həll etməyi öyrənir.</p><span class="metric"><i data-lucide="code"></i>Hədəf: hər dərsdə praktika</span></div>
      <div class="card goal"><h3>Geniş əlçatanlıq</h3><p>Brauzerdə işləyir, quraşdırma tələb etmir. Yerli qiymətlərlə məktəb, universitet və kurslar üçün.</p><span class="metric"><i data-lucide="rocket"></i>Hədəf: 2027-də 10+ müəssisə</span></div>
    </div>
  </div>
</section>

<section class="sec wrap">
  <div class="inner">
    <div class="head"><span class="kicker"><i data-lucide="chart-line"></i>2027 hədəfləri</span><h2>Rəqəmlərlə hara getmək istəyirik</h2><p class="lead">Bunlar komandanın hədəfləridir, nəticələr pilotdan sonra ölçüləcək.</p></div>
    <div class="targets">
      <div class="target"><b>10+</b><span>təhsil müəssisəsi</span></div>
      <div class="target"><b>1 000+</b><span>aktiv şagird</span></div>
      <div class="target"><b>3</b><span>proqramlaşdırma dili</span></div>
      <div class="target"><b>70%</b><span>dəyişikliksiz təsdiqlənən lab</span></div>
    </div>
  </div>
</section>

<section class="sec tight wrap">
  <div class="inner">
    <div class="head"><span class="kicker"><i data-lucide="rocket"></i>Yol xəritəsi</span><h2>Haradayıq və hara gedirik</h2></div>
    <div class="road">
      <div class="ms now"><span class="when">2026 · IV rüb <em>indi</em></span><h3>MVP</h3><ul><li>Python kvestləri</li><li>AI tutor və öyrənmə yolu</li><li>Müəllim paneli</li></ul></div>
      <div class="ms"><span class="when">2027 · I rüb</span><h3>Pilot</h3><ul><li>3 IT kursu</li><li>300+ şagird</li><li>Nəticələrin ölçülməsi</li></ul></div>
      <div class="ms"><span class="when">2027 · II rüb</span><h3>Məktəblər</h3><ul><li>2 məktəbdə pilot</li><li>Valideyn hesabatı</li><li>Yeni oyun dünyaları</li></ul></div>
      <div class="ms"><span class="when">2027 · III rüb</span><h3>Universitetlər</h3><ul><li>C++ və Java</li><li>LMS inteqrasiyası</li><li>Plagiat analizi</li></ul></div>
    </div>
  </div>
</section>
"""

# ---------------- Necə işləyir ----------------
HOW = page_hero("Necə işləyir", "Necə işləyir?", "Müəllimin yüklədiyi materialdan şagirdin fərdi kvestinə qədər bütün yol.", "route", "4 addım") + """
<section class="sec wrap">
  <div class="inner">
    <div class="head"><span class="kicker"><i data-lucide="workflow"></i>Addım-addım</span><h2>Kim nə edir?</h2></div>
    <div class="seg" role="tablist" data-tabs="flow">
      <button role="tab" data-tab="teacher" aria-selected="true"><i data-lucide="presentation"></i>Müəllim üçün</button>
      <button role="tab" data-tab="student" aria-selected="false"><i data-lucide="graduation-cap"></i>Şagird üçün</button>
    </div>
    <div data-panel="flow" data-key="teacher" class="steps">
      <div class="step"><span class="num">1</span><h3>Materialı yüklə</h3><p>Sillabus, slayd, PDF və ya nümunə kod. Codigo mövzuları və həftəlik planı özü çıxarır.</p></div>
      <div class="step"><span class="num">2</span><h3>Planı yoxla</h3><p>Mövzuların sırasını və əlaqəsini gör, lazım olsa dəyiş. Bugünkü dərsi seç.</p></div>
      <div class="step"><span class="num">3</span><h3>Tapşırıqları təsdiqlə</h3><p>Hər lab üç çətinlikdə, gizli testlərlə hazırlanır. Nümunə həll testlərdən keçmirsə, lab sənə gəlmir.</p></div>
      <div class="step"><span class="num">4</span><h3>Sinfi izlə</h3><p>Panel kimin harada ilişdiyini göstərir. Köməyə ehtiyacı olan şagirdlər ayrıca qeyd olunur.</p></div>
    </div>
    <div data-panel="flow" data-key="student" class="steps" hidden>
      <div class="step"><span class="num">1</span><h3>Sinifə qoşul</h3><p>Müəllimin verdiyi kodla daxil ol. Quraşdırma lazım deyil, hər şey brauzerdədir.</p></div>
      <div class="step"><span class="num">2</span><h3>Giriş testini keç</h3><p>8-15 suallıq adaptiv test. Düz cavab versən, sual çətinləşir. Səviyyən müəyyən olunur.</p></div>
      <div class="step"><span class="num">3</span><h3>Kvestləri həll et</h3><p>Kodu yaz, işə sal, testlərin nəticəsini dərhal gör. Çətinlikdə AI-dən ipucu al.</p></div>
      <div class="step"><span class="num">4</span><h3>İnkişafını gör</h3><p>XP qazan, səviyyə atla. Səhvlərinə görə yolun yenilənir, zəif mövzular əlavə olunur.</p></div>
    </div>
  </div>
</section>

<section class="sec alt wrap">
  <div class="inner modes">
    <div style="display:flex;flex-direction:column;gap:18px">
      <span class="kicker"><i data-lucide="bot"></i>AI rejimləri</span>
      <h2>AI nə qədər kömək edəcəyini müəllim seçir</h2>
      <p class="lead">Şagird eyni sualı versə də, cavab müəllimin seçdiyi rejimə görə dəyişir. Rejimə bas və fərqi gör.</p>
      <div class="mode-list" role="tablist" aria-label="AI rejimi">
        <button class="mode-tab" role="tab" aria-selected="true" data-mode="hint"><span class="ic sm blue"><i data-lucide="lightbulb"></i></span><span><b>İpucu</b><span class="d">Sual verir, səhvin yerinə işarə edir, kod yazmır.</span></span></button>
        <button class="mode-tab" role="tab" aria-selected="false" data-mode="off"><span class="ic sm capy"><i data-lucide="bell-off"></i></span><span><b>Söndürülüb</b><span class="d">Şagird yalnız testlərin nəticəsini görür.</span></span></button>
        <button class="mode-tab" role="tab" aria-selected="false" data-mode="exam"><span class="ic sm rose"><i data-lucide="lock"></i></span><span><b>İmtahan</b><span class="d">AI bağlıdır, yalnız bal görünür.</span></span></button>
      </div>
    </div>
    <div class="chat" aria-live="polite">
      <div class="ctx"><span>Leyla · Həftə 3 · sum_even</span><span>3/5 test keçib</span></div>
      <div class="msg me">Kodum işləmir, düzgün variantı yaz.</div>
      <div id="aiReply"></div>
      <div class="chat-foot" id="aiFoot"></div>
    </div>
  </div>
</section>

<section class="sec wrap">
  <div class="inner">
    <div class="head"><span class="kicker"><i data-lucide="git-fork"></i>Fərdi yol</span><h2>Eyni sinif, eyni dərs, iki fərqli növbəti addım</h2><p class="lead">Codigo hər mövzu üzrə 0-100 arası bilik səviyyəsi saxlayır. Nümunə şagirdlər uydurmadır.</p></div>
    <div class="grid g2">
      <div class="path">
        <div class="path-head"><h3>Murad</h3><small>güclü başlayıb · 2 ipucu</small></div>
        <div class="nodes"><div class="node hi"><span class="dot">94</span>Dəyişən</div><div class="node hi"><span class="dot">88</span>Şərt</div><div class="node hi now"><span class="dot">91</span>Dövr</div><div class="node"><span class="dot">·</span>Siyahı</div><div class="node"><span class="dot">·</span>Funksiya</div><div class="node"><span class="dot">·</span>Rekursiya</div></div>
        <div class="next">Növbəti: <b>Dövrlər · çətin kvest</b>, sonra Siyahılara erkən keçid.</div>
      </div>
      <div class="path">
        <div class="path-head"><h3>Leyla</h3><small>şərtlərdə boşluq · 6 ipucu</small></div>
        <div class="nodes"><div class="node hi"><span class="dot">82</span>Dəyişən</div><div class="node lo"><span class="dot">41</span>Şərt</div><div class="node mid now"><span class="dot">58</span>Dövr</div><div class="node"><span class="dot">·</span>Siyahı</div><div class="node"><span class="dot">·</span>Funksiya</div><div class="node"><span class="dot">·</span>Rekursiya</div></div>
        <div class="next">Növbəti: <b>Şərtlər · asan təkrar</b>, sonra Dövrlər. Müəllimə bildiriş gedir.</div>
      </div>
    </div>
    <div class="legend"><span class="l1">0–49 kömək lazımdır</span><span class="l2">50–79 inkişafda</span><span class="l3">80–100 mənimsəyib</span></div>
  </div>
</section>
"""

# ---------------- İmkanlar ----------------
FEAT = page_hero("İmkanlar", "Platformanın imkanları", "Developer aləti qədər ciddi, oyun qədər maraqlı. Hər imkan bir problemi həll edir.", "sparkles", "6 imkan") + """
<section class="sec wrap">
  <div class="inner">
    <div class="frow">
      <div class="ftext"><span class="ic blue"><i data-lucide="route"></i></span><h2>Fərdi öyrənmə yolu</h2><p>Skill tree üzərində şagird harada olduğunu və növbəti addımını görür. Bir mövzuda eyni səhv təkrarlananda yola həmin mövzu üzrə əlavə məşq düşür.</p><ul class="ticks"><li><i data-lucide="circle-check"></i>Müəllimin təqviminə uyğun sıra</li><li><i data-lucide="circle-check"></i>Mənimsənilən mövzular keçilir</li><li><i data-lucide="circle-check"></i>Zəif mövzular avtomatik əlavə olunur</li></ul></div>
      <div class="fvis"><div class="mock">
        <div class="row"><span class="tag mint">✓</span>Dəyişənlər<span class="bar"><i class="hi" style="width:94%"></i></span></div>
        <div class="row"><span class="tag mint">✓</span>Şərtlər<span class="bar"><i class="hi" style="width:86%"></i></span></div>
        <div class="row"><span class="tag blue">İndi</span>Dövrlər<span class="bar"><i style="width:58%"></i></span></div>
        <div class="row"><span class="tag rose">AI</span>range() təkrarı<span class="bar"><i class="lo" style="width:30%"></i></span></div>
        <div class="row" style="color:var(--muted)"><span class="tag capy">🔒</span>Siyahılar<span class="bar"><i style="width:0"></i></span></div>
      </div></div>
    </div>
    <div class="frow flip">
      <div class="ftext"><span class="ic capy"><i data-lucide="bot"></i></span><h2>AI tutor</h2><p>Səhvi tapır, Azərbaycan dilində izah edir və şagirdi düşündürən sual verir. Hazır həll vermir. Müəllim hər tapşırıq üçün rejimi seçir.</p><ul class="ticks"><li><i data-lucide="circle-check"></i>İpucu, söndürülüb və imtahan rejimləri</li><li><i data-lucide="circle-check"></i>Kurs materialına əsaslanan izahlar</li><li><i data-lucide="circle-check"></i>Bütün dialoqlar müəllimə görünür</li></ul></div>
      <div class="fvis"><div class="mock">
        <div class="row" style="justify-content:flex-end"><span style="background:var(--tint);padding:10px 12px;border-radius:14px 14px 4px 14px;font-weight:600">Niyə 4 qalxan çıxır?</span></div>
        <div class="row" style="align-items:flex-start"><span class="ic sm capy" style="width:34px;height:34px"><i data-lucide="bot"></i></span><span style="background:var(--capy-soft);padding:10px 12px;border-radius:14px 14px 14px 4px;font-weight:600">range(1, 5) hansı ədədləri verir? Son ədəd siyahıya düşürmü?</span></div>
      </div></div>
    </div>
    <div class="frow">
      <div class="ftext"><span class="ic mint"><i data-lucide="swords"></i></span><h2>Oyun kvestləri</h2><p>Robotu labirintdən çıxar, enerji qalxanı yarat, ən güclü kristalı tap. Hər kvest bir proqramlaşdırma anlayışını öyrədir və addım-addım vizual oynanır.</p><ul class="ticks"><li><i data-lucide="circle-check"></i>Hekayəli tapşırıqlar</li><li><i data-lucide="circle-check"></i>Kodun icrası animasiya ilə</li><li><i data-lucide="circle-check"></i>Üç çətinlik səviyyəsi</li></ul></div>
      <div class="fvis"><div class="maze" aria-hidden="true">
        <span class="w"></span><span class="w"></span><span class="w"></span><span class="w"></span><span class="w"></span><span class="w"></span><span class="w"></span>
        <span class="w"></span><span class="p"></span><span class="p"></span><span class="p"></span><span class="p"></span><span class="h"></span><span class="w"></span>
        <span class="w"></span><span class="p"></span><span class="w"></span><span class="w"></span><span class="w"></span><span></span><span class="w"></span>
        <span class="w"></span><span class="p"></span><span class="w"></span><span></span><span></span><span></span><span class="w"></span>
        <span class="w"></span><span class="p"></span><span class="w"></span><span></span><span class="w"></span><span></span><span class="w"></span>
        <span class="w"></span><span class="p"></span><span></span><span></span><span class="w"></span><span class="g"></span><span class="w"></span>
        <span class="w"></span><span class="w"></span><span class="w"></span><span class="w"></span><span class="w"></span><span class="w"></span><span class="w"></span>
      </div></div>
    </div>
    <div class="frow flip">
      <div class="ftext"><span class="ic blue"><i data-lucide="monitor-play"></i></span><h2>Brauzerdə kod redaktoru</h2><p>Python, C++ və Java. Kodu yaz, işə sal və gizli testlərin nəticəsini dərhal gör. Kompüterə heç nə quraşdırmaq lazım deyil.</p><ul class="ticks"><li><i data-lucide="circle-check"></i>Sintaksis rəngləmə və avtomatik tamamlama</li><li><i data-lucide="circle-check"></i>Ani nəticə və test hesabatı</li><li><i data-lucide="circle-check"></i>Təhlükəsiz, izolə edilmiş icra</li></ul></div>
      <div class="fvis"><div class="mock"><pre><span class="k">for</span> i <span class="k">in</span> <span class="b">range</span>(<span class="n">5</span>):
    <span class="b">print</span>(<span class="s">f"Qalxan-{i + 1}"</span>)</pre><div class="row"><span class="tag mint">✓ 3/3 test</span><span class="tag blue">+250 XP</span></div></div></div>
    </div>
    <div class="frow">
      <div class="ftext"><span class="ic capy"><i data-lucide="trophy"></i></span><h2>XP, səviyyə və nailiyyətlər</h2><p>Hər uğurlu kvest XP gətirir. Ardıcıl günlər, yeni səviyyələr və nişanlar motivasiyanı saxlayır. Liderlik cədvəli yoxdur ki, zəif şagird ruhdan düşməsin.</p><ul class="ticks"><li><i data-lucide="circle-check"></i>Şəxsi irəliləyiş, müqayisə yox</li><li><i data-lucide="circle-check"></i>Ardıcıllıq sayğacı</li><li><i data-lucide="circle-check"></i>Mövzulara bağlı nişanlar</li></ul></div>
      <div class="fvis"><div class="mock"><div class="row">Səviyyə 5 · Coder<span class="bar"><i class="xp" style="width:67%"></i></span></div><div class="badges"><span><i data-lucide="flame"></i>7 gün</span><span><i data-lucide="award"></i>İlk 5/5</span><span><i data-lucide="bug"></i>Səhv ovçusu</span></div></div></div>
    </div>
    <div class="frow flip">
      <div class="ftext"><span class="ic mint"><i data-lucide="layout-dashboard"></i></span><h2>Müəllim paneli</h2><p>Sinfin mövzular üzrə vəziyyəti bir cədvəldə. Köməyə ehtiyacı olan şagirdlər ayrıca göstərilir, yeni tapşırıqlar təsdiq növbəsində gözləyir.</p><ul class="ticks"><li><i data-lucide="circle-check"></i>Mövzu üzrə rəngli cədvəl</li><li><i data-lucide="circle-check"></i>Avtomatik bildirişlər</li><li><i data-lucide="circle-check"></i>Tapşırıqların təsdiq növbəsi</li></ul></div>
      <div class="fvis"><div class="mock"><div class="heat">
        <span class="h"></span><span class="h">H1</span><span class="h">H2</span><span class="h">H3</span><span class="h">H4</span><span class="h">H5</span>
        <span class="h">Aysel</span><span class="a">92</span><span class="a">85</span><span class="b">71</span><span class="b">60</span><span class="h">—</span>
        <span class="h">Murad</span><span class="a">94</span><span class="a">88</span><span class="a">91</span><span class="b">64</span><span class="h">—</span>
        <span class="h">Leyla</span><span class="a">82</span><span class="c">41</span><span class="b">58</span><span class="h">—</span><span class="h">—</span>
        <span class="h">Elvin</span><span class="b">77</span><span class="b">69</span><span class="c">38</span><span class="h">—</span><span class="h">—</span>
      </div></div></div>
    </div>
  </div>
</section>

<section class="sec alt wrap">
  <div class="inner">
    <div class="head"><span class="kicker"><i data-lucide="scale"></i>Müqayisə</span><h2>Bazarda olanlarla yan-yana</h2></div>
    <div class="tbl"><table>
      <thead><tr><th></th><th class="us">Codigo</th><th>CodeHS</th><th>Codecademy</th><th>Code.org</th></tr></thead>
      <tbody>
        <tr><td>Müəllimin öz materialından tapşırıq</td><td class="us"><span class="y">✓</span></td><td><span class="p">◐</span></td><td><span class="n">—</span></td><td><span class="n">—</span></td></tr>
        <tr><td>Avtomatik test yoxlaması</td><td class="us"><span class="y">✓</span></td><td><span class="y">✓</span></td><td><span class="y">✓</span></td><td><span class="p">◐</span></td></tr>
        <tr><td>Hər şagirdə adaptiv yol</td><td class="us"><span class="y">✓</span></td><td><span class="n">—</span></td><td><span class="p">◐</span></td><td><span class="n">—</span></td></tr>
        <tr><td>AI rejimini müəllim seçir</td><td class="us"><span class="y">✓</span></td><td><span class="p">◐</span></td><td><span class="n">—</span></td><td><span class="p">◐</span></td></tr>
        <tr><td>Azərbaycan dilində izah</td><td class="us"><span class="y">✓</span></td><td><span class="n">—</span></td><td><span class="n">—</span></td><td><span class="p">◐</span></td></tr>
      </tbody>
    </table></div>
    <p class="note">✓ var · ◐ qismən · — yoxdur. Rəqiblər haqqında məlumat 2026-cı ilin oktyabrında ictimai mənbələrdən toplanıb. Codigo sütunu planlaşdırılan məhsulu göstərir.</p>
  </div>
</section>
"""

# ---------------- Kimlər üçün ----------------
AUD = page_hero("Kimlər üçün", "Kimlər üçün?", "Orta məktəblər, universitetlər və IT kursları. Hər biri üçün ayrıca rejim və qiymət.", "users", "3 auditoriya") + f"""
<section class="sec wrap">
  <div class="inner">
    <div class="seg-card">
      <div class="left"><span class="ic blue"><i data-lucide="school"></i></span><h2>Orta məktəblər</h2><p class="muted">İnformatika müəllimi bir neçə sinifə dərs deyir və hər şagirdə ayrıca vaxt ayıra bilmir.</p></div>
      <div class="cols">
        <div class="pain"><h4><i data-lucide="circle-alert"></i>Problem</h4><ul><li><i data-lucide="x"></i>Sinifdə səviyyə fərqi böyükdür</li><li><i data-lucide="x"></i>Hazır kurslar proqrama uyğun deyil</li><li><i data-lucide="x"></i>Uşaqlar AI-dən hazır cavab alır</li></ul></div>
        <div class="gain"><h4><i data-lucide="circle-check"></i>Codigo ilə</h4><ul><li><i data-lucide="check"></i>Hər şagirdə öz səviyyəsində kvest</li><li><i data-lucide="check"></i>Uşaqlar üçün təhlükəsiz AI rejimi</li><li><i data-lucide="check"></i>Valideyn üçün irəliləyiş hesabatı</li></ul></div>
      </div>
    </div>
    <div class="seg-card">
      <div class="left"><span class="ic capy"><i data-lucide="graduation-cap"></i></span><h2>Universitetlər</h2><p class="muted">Proqramlaşdırma laboratoriyalarında yüzlərlə tələbənin işini yoxlamaq lazımdır.</p></div>
      <div class="cols">
        <div class="pain"><h4><i data-lucide="circle-alert"></i>Problem</h4><ul><li><i data-lucide="x"></i>Əl ilə yoxlama həftələr çəkir</li><li><i data-lucide="x"></i>Köçürülmüş kodu tutmaq çətindir</li><li><i data-lucide="x"></i>GitHub Classroom dayandırılıb</li></ul></div>
        <div class="gain"><h4><i data-lucide="circle-check"></i>Codigo ilə</h4><ul><li><i data-lucide="check"></i>Avtomatik test və qiymətləndirmə</li><li><i data-lucide="check"></i>C++ və Java dəstəyi</li><li><i data-lucide="check"></i>Yazma prosesinin və plagiatın izlənməsi</li></ul></div>
      </div>
    </div>
    <div class="seg-card">
      <div class="left"><span class="ic mint"><i data-lucide="building-2"></i></span><h2>IT kursları</h2><p class="muted">Kurslar öz proqramı ilə işləyir və nəticəni sürətlə göstərməlidir.</p></div>
      <div class="cols">
        <div class="pain"><h4><i data-lucide="circle-alert"></i>Problem</h4><ul><li><i data-lucide="x"></i>Mentorlar tapşırıq yazmağa vaxt itirir</li><li><i data-lucide="x"></i>Qrupda zəif tələbə gec aşkarlanır</li><li><i data-lucide="x"></i>Xarici platformalar bahadır</li></ul></div>
        <div class="gain"><h4><i data-lucide="circle-check"></i>Codigo ilə</h4><ul><li><i data-lucide="check"></i>Öz proqramınıza uyğun lablar</li><li><i data-lucide="check"></i>Qrup və mentor üzrə hesabat</li><li><i data-lucide="check"></i>Şagird başına yerli qiymət</li></ul></div>
      </div>
    </div>
  </div>
</section>

<section class="sec wrap" id="qiymet"><div class="inner head center"><span class="kicker">Qiymətlər</span><h2>Özün üçün və sinfin üçün ayrıca plan.</h2><p class="lead">Pulsuz başlanğıc, fərdi Plus və 25 yerlik sinif paketi. Bütün şərtləri bir səhifədə gör.</p><a class="btn primary" href="qiymetler.html">Planları müqayisə et</a></div></section>
"""

# ---------------- Suallar ----------------
def faq(items):
    return "".join(f'<details><summary>{q}<i data-lucide="chevron-down"></i></summary><p>{a}</p></details>' for q, a in items)

FAQ = page_hero("Suallar", "Tez-tez verilən suallar", "Cavabını tapmadığın sual varsa, aşağıdakı formadan bizə yaz.", "message-circle-question", "Cavablar") + f"""
<section class="sec wrap">
  <div class="inner">
    <div class="faq-group"><div class="gh"><span class="ic blue"><i data-lucide="info"></i></span><h3>Ümumi</h3></div><div class="faq">{faq([
        ("Codigo nədir?", "Müəllimin öz dərs materialından hər şagird üçün fərdi tapşırıqlar və oyun kvestləri hazırlayan proqramlaşdırma təhsili platformasıdır."),
        ("Hansı proqramlaşdırma dilləri var?", "İlk versiya Python ilə başlayır. Sonra C++ və Java əlavə olunur."),
        ("Kompüterə nəsə quraşdırmaq lazımdır?", "Xeyr. Codigo brauzerdə işləyir, kod da brauzerdə yazılır və işə salınır."),
    ])}</div></div>
    <div class="faq-group"><div class="gh"><span class="ic capy"><i data-lucide="presentation"></i></span><h3>Müəllimlər üçün</h3></div><div class="faq">{faq([
        ("Müəllim üçün çətin olmayacaq?", "Müəllim yeni sistem öyrənmir. Öz materialını yükləyir, hazır tapşırıqlara baxıb təsdiqləyir. Texniki işi platforma görür."),
        ("AI yanlış tapşırıq yaratsa nə olur?", "Hər tapşırığın nümunə həlli şagirdə getməzdən əvvəl gizli testlərdən keçirilir. Keçməyən tapşırıq göndərilmir. Sonra müəllim oxuyub təsdiqləyir."),
        ("Yüklənən materiallar kimə məxsusdur?", "Müəssisəyə. Materiallar başqa müştərilər üçün istifadə olunmur və istənilən vaxt ixrac edilə və ya silinə bilər."),
    ])}</div></div>
    <div class="faq-group"><div class="gh"><span class="ic mint"><i data-lucide="shield-check"></i></span><h3>AI və təhlükəsizlik</h3></div><div class="faq">{faq([
        ("AI şagirdin yerinə kodu yazmır ki?", "Xeyr. AI yalnız sual verir və səhvin harada ola biləcəyinə işarə edir. Müəllim AI-ni tam söndürə və ya imtahan rejiminə keçirə bilər."),
        ("Uşaqların məlumatları necə qorunur?", "Minimum şəxsi məlumat saxlanılır, məktəb rejimində valideyn razılığı tələb olunur, AI-yə şagirdin adı və şəxsi məlumatları göndərilmir."),
    ])}</div></div>
  </div>
</section>

<section class="sec alt wrap" id="pilot">
  <div class="inner pilot">
    <div class="prose">
      <span class="kicker"><i data-lucide="rocket"></i>Pilot proqram</span>
      <h2>Codigo-nu öz dərsinizdə sınayın</h2>
      <p>Pilot proqrama ilk müəssisələri qəbul edirik. Planlaşdırılan təklif: 30 gün pulsuz, 25 şagirdədək və 2 müəllim. Pilotdan sonra davam qərarı ayrıca verilir; avtomatik ödəniş yoxdur.</p>
      <ul class="ticks"><li><i data-lucide="circle-check"></i>30 gün pulsuz · 25 şagirdədək</li><li><i data-lucide="circle-check"></i>Öz materialınızla qurulum</li><li><i data-lucide="circle-check"></i>Nəticələrin ölçülməsi və hesabat</li></ul>
      <img style="width:140px;margin-top:10px" aria-hidden="true" src="icon.webp" alt="">
    </div>
    <form class="form" id="pilotForm" novalidate>
      <label for="fPlan">Maraqlandığınız plan<select id="fPlan"><option value="pilot">30 günlük pilot</option><option value="sinif">Sinif · 149 AZN/ay + əlavə yerlər</option><option value="muessise">Müəssisə · fərdi təklif</option><option value="plus">Plus · fərdi öyrənmə</option></select></label>
      <div class="row2">
        <label for="fName">Ad, soyad<input id="fName" autocomplete="name" required></label>
        <label for="fOrg">Müəssisə<input id="fOrg" required></label>
      </div>
      <div class="row2">
        <label for="fType">Müəssisə növü<select id="fType"><option>IT kursu</option><option>Orta məktəb</option><option>Universitet</option></select></label>
        <label for="fCount">Şagird sayı<select id="fCount"><option>50-dən az</option><option>50–200</option><option>200-dən çox</option></select></label>
      </div>
      <label for="fMail">E-poçt<input id="fMail" type="email" autocomplete="email" required></label>
      <label for="fMsg">Sualınız (istəyə bağlı)<textarea id="fMsg"></textarea></label>
      <button class="btn primary" type="submit">Demo müraciətini hazırla <i data-lucide="arrow-right"></i></button>
      <small>Demo forma: məlumat heç yerə göndərilmir.</small>
      <div class="done" id="formDone" hidden></div>
    </form>
  </div>
</section>
"""

CONTENT = {
    "index.html": ("Codigo", HOME),
    "haqqimizda.html": ("Haqqımızda · Codigo", ABOUT),
    "missiya.html": ("Missiya · Codigo", MISSION),
    "nece-isleyir.html": ("Necə işləyir · Codigo", HOW),
    "imkanlar.html": ("İmkanlar · Codigo", FEAT),
    "kimler-ucun.html": ("Kimlər üçün · Codigo", AUD),
    "suallar.html": ("Suallar · Codigo", FAQ),
    "qiymetler.html": ("Qiymətlər · Codigo", Path(HERE, "pricing.html").read_text(encoding="utf-8")),
}

CONTENT["index.html"] = ("Codigo · Kod öyrən. Öz hekayəni yaz.", Path(HERE, "home.html").read_text(encoding="utf-8"))

TEAM = Path(HERE, "team.html").read_text(encoding="utf-8")
home_title, home_body = CONTENT["index.html"]
home_marker = '<section class="sec tight wrap"><div class="inner play-finish">'
CONTENT["index.html"] = (home_title, home_body.replace(home_marker, TEAM + '\n' + home_marker, 1))
CONTENT["haqqimizda.html"] = ("Haqqımızda · Codigo", ABOUT + '\n' + TEAM)

for f, (title, body) in CONTENT.items():
    full = body if f == "index.html" else body + "\n" + pager(f)
    if f == "index.html":
        # Artifact-ın əsas səhifəsi (skeletsiz) və lokal açmaq üçün tam versiya
        io.open(os.path.join(HERE, "codego.html"), "w", encoding="utf-8").write(render(f, title, full, full_doc=False))
    io.open(os.path.join(HERE, f), "w", encoding="utf-8").write(render(f, title, full))
print("OK:", ", ".join(CONTENT))

# The app directory is the source of truth; publish a complete HTML document.
app_dir = Path(HERE).parent / "app"
app_source = (app_dir / "codego-app.html").read_text(encoding="utf-8")
app_source = app_source.replace('</style>', '</style>\n</head>\n<body>', 1)
Path(HERE, "app.html").write_text('<!doctype html>\n<html lang="az" data-theme="light">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n' + app_source + '\n</body>\n</html>\n', encoding="utf-8")
for asset in ("journey.js", "journey.css"):
    shutil.copyfile(app_dir / asset, Path(HERE, asset))
print("OK: app.html, journey.js, journey.css")
