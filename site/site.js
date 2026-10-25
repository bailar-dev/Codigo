// Codigo sayt skripti: ikonlar, mobil menyu, tablar, AI rejimləri, pilot forması
(function () {
  try { lucide.createIcons(); } catch (e) {}

  // A first lesson without registration. Wrong answers remain retryable.
  document.querySelectorAll('[data-try-answer]').forEach(button => {
    button.addEventListener('click', () => {
      const correct = button.dataset.tryAnswer === '3';
      document.querySelectorAll('[data-try-answer]').forEach(b => {
        b.classList.remove('correct', 'wrong');
        b.setAttribute('aria-pressed', String(b === button));
      });
      button.classList.add(correct ? 'correct' : 'wrong');
      document.getElementById('tryStars').textContent = correct ? '⭐ ⭐ ⭐' : '✧ ✧ ✧';
      document.getElementById('tryFeedback').textContent = correct
        ? 'Düz tapdın! range(3) → 0, 1, 2. Dövr üç dəfə işləyir və üç ulduz yanır.'
        : 'Bir də düşün: range(3) sıfırdan başlayır — 0, 1, 2. Neçə ədəd saydın? Yenidən seç.';
    });
  });

  const menuBtn = document.getElementById("menuBtn");
  const menu = document.getElementById("mobileMenu");
  if (menuBtn && menu) {
    menuBtn.addEventListener("click", () => {
      const open = menu.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
  }

  // Müəllim / şagird axını tabları
  document.querySelectorAll("[data-tabs]").forEach(group => {
    const buttons = group.querySelectorAll("[data-tab]");
    const panels = document.querySelectorAll("[data-panel='" + group.dataset.tabs + "']");
    buttons.forEach(b => b.addEventListener("click", () => {
      buttons.forEach(x => x.setAttribute("aria-selected", String(x === b)));
      panels.forEach(p => { p.hidden = p.dataset.key !== b.dataset.tab; });
    }));
  });

  // AI rejimləri demosu
  const replies = {
    hint: { cls: "ai", label: "Codigo · ipucu", text: "Hazır kodu yazmayacağam, amma birlikdə tapaq. sum_even(2) testi keçmir. range(1, n) hansı ədədlərdə dayanır? n-in özü dövrə düşürmü?", foot: "AI şagirdin səviyyəsini və keçməyən testləri görür, cavabı ona görə qurur. Müəllim bütün dialoqları paneldə görür." },
    off: { cls: "lock", text: "Bu tapşırıq üçün müəllim AI köməyini söndürüb. Testlərin nəticəsinə baxıb yenidən cəhd et: 2 test keçmir.", foot: "Şagird hər testin gözlənilən və alınan nəticəsini görür, amma AI ilə danışa bilmir." },
    exam: { cls: "lock", text: "İmtahan rejimi. AI bağlıdır, test detalları gizlidir. Cari nəticə: 3/5.", foot: "Codigo yazma prosesini də qeydə alır: kodun necə dəyişdiyi müəllimə görünür, kənardan yapışdırılan böyük hissələr işarələnir." }
  };
  const tabs = document.querySelectorAll(".mode-tab");
  const box = document.getElementById("aiReply");
  const foot = document.getElementById("aiFoot");
  function show(mode) {
    const r = replies[mode];
    if (!r || !box) return;
    tabs.forEach(t => t.setAttribute("aria-selected", String(t.dataset.mode === mode)));
    box.innerHTML = "";
    const m = document.createElement("div");
    m.className = "msg " + r.cls;
    if (r.label) { const s = document.createElement("small"); s.textContent = r.label; m.append(s); }
    m.append(document.createTextNode(r.text));
    box.append(m);
    foot.textContent = r.foot;
  }
  tabs.forEach(t => t.addEventListener("click", () => show(t.dataset.mode)));
  if (box) show("hint");

  // Pilot forması (demo)
  const form = document.getElementById("pilotForm");
  if (form) form.addEventListener("submit", e => {
    e.preventDefault();
    const name = document.getElementById("fName"), org = document.getElementById("fOrg"), mail = document.getElementById("fMail"), done = document.getElementById("formDone");
    done.hidden = false;
    if (!name.value.trim() || !org.value.trim() || !mail.value.trim() || !mail.checkValidity()) {
      done.className = "done err";
      done.textContent = "Ad, müəssisə və düzgün e-poçt ünvanını doldurun.";
      return;
    }
    done.className = "done ok";
    done.textContent = "Təşəkkürlər, " + name.value.trim() + "! " + org.value.trim() + " üçün demo müraciət hazırlandı. Heç yerə göndərilməyib; real qeydiyyat yaradılmayıb.";
  });
})();
