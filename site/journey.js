/* Small, replayable lessons. Course and independent paths share the same learning UI. */
window.CodigoJourney = function ({ React, html, Icon, Capy, Wordmark, MODULES, allQuests, unlocked, dayKey }) {
  const { useState, useEffect, useRef } = React;
  const item = (type, q, code, options, answer, explanation) => ({type, q, code, options, answer, explanation});
  const LESSONS = {
    vars: [
      item('Təxmin et', 'Robotun enerji səviyyəsi neçədir?', 'energy = 5\nenergy = energy + 3\nprint(energy)', ['5', '8', '3', '53'], 1, 'energy əvvəlcə 5-dir. Üzərinə 3 gələndə yeni dəyəri 8 olur.'),
      item('Boşluğu doldur', 'Robotun adını yadda saxla.', 'name = ___\nprint(name)', ['Codigo', '"Codigo"', 'print', '= Codigo'], 1, 'Mətn dəyərləri dırnaq içində yazılır: "Codigo".'),
      item('Səhvi tap', 'İki ədədi toplamaq üçün hansı sətri dəyişməlisən?', 'a = "3"\nb = 2\nprint(a + b)', ['b = "iki"', 'a = 3', 'print(a - b)', 'Heç birini'], 1, '"3" mətndir, 3 isə ədəddir. Toplama üçün hər ikisi ədəd olmalıdır.')
    ],
    cond: [
      item('Təxmin et', 'Qapı açılacaq?', 'keys = 2\nif keys >= 2:\n    print("Açıldı")\nelse:\n    print("Bağlıdır")', ['Açıldı', 'Bağlıdır', '2', 'Xəta'], 0, '2 >= 2 doğrudur. Ona görə if hissəsi işləyir.'),
      item('Boşluğu doldur', 'Yalnız 10-dan böyük balları seç.', 'if score ___ 10:\n    print("Bonus!")', ['<', '==', '>', '='], 2, '> işarəsi soldakı dəyərin sağdakından böyük olduğunu yoxlayır.'),
      item('Səhvi tap', 'Bərabərliyi necə yoxlayırıq?', 'if level = 3:\n    print("Yeni dünya")', ['level == 3', 'level + 3', 'level != 3', 'level = "3"'], 0, '= dəyər mənimsədir, == isə iki dəyəri müqayisə edir.')
    ],
    loops: [
      item('Təxmin et', 'Kapibara üçün neçə körpü hissəsi qurulacaq?', 'for i in range(3):\n    print("Körpü hissəsi")', ['2 hissə', '3 hissə', '4 hissə', '0 hissə'], 1, 'range(3) → 0, 1, 2. Üç ədəd var, dövr üç dəfə işləyir.'),
      item('Boşluğu doldur', '1, 2, 3, 4, 5 ədədlərini çap et.', 'for i in range(1, ___):\n    print(i)', ['4', '5', '6', '1'], 2, 'range son sərhədi daxil etmir. 5-in də daxil olması üçün son sərhəd 6 olmalıdır.'),
      item('Səhvi tap', 'Robot dayanmadan gedir. Nə çatışmır?', 'steps = 0\nwhile steps < 3:\n    print("Addım")\n    # buranı tamamla', ['steps = 0', 'steps -= 1', 'steps += 1', 'print(3)'], 2, 'Hər addımda steps 1 artmalıdır. 3-ə çatanda şərt yalan olur və dövr dayanır.')
    ],
    lists: [
      item('Təxmin et', 'İkinci çantada nə var?', 'bag = [4, 8, 15]\nprint(bag[1])', ['4', '8', '15', '1'], 1, 'İndekslər 0-dan başlayır. bag[1] ikinci elementdir: 8.'),
      item('Boşluğu doldur', 'Çantaya yeni kristal əlavə et.', 'bag = [4, 8]\nbag.___(15)', ['add', 'push', 'append', 'join'], 2, 'Python siyahısının sonuna element əlavə edən metod append-dir.'),
      item('Səhvi tap', 'Son elementi təhlükəsiz seç.', 'bag = [4, 8, 15]\nprint(bag[3])', ['bag[4]', 'bag[-1]', 'bag[15]', 'bag[3]'], 1, 'Bu siyahıda 3 indeksi yoxdur. -1 həmişə son elementdir.')
    ],
    funcs: [
      item('Təxmin et', 'Portal hansı nəticəni qaytarır?', 'def double(x):\n    return x * 2\nprint(double(4))', ['4', '6', '8', '2'], 2, 'Funksiyaya 4 verilir, 4 × 2 = 8 qaytarılır.'),
      item('Boşluğu doldur', 'Nəticəni funksiyadan geri göndər.', 'def add(a, b):\n    ___ a + b', ['print', 'return', 'def', 'input'], 1, 'return hesablanmış nəticəni funksiyanı çağıran koda qaytarır.'),
      item('Səhvi tap', 'Niyə cavab None olur?', 'def add(a, b):\n    print(a + b)\nanswer = add(2, 3)', ['print əvəzinə return yaz', 'a-nı sil', '2 əvəzinə 3 yaz', 'Funksiyanı sil'], 0, 'print yalnız ekrana yazır. Dəyəri answer dəyişəninə almaq üçün return lazımdır.')
    ],
    strings: [
      item('Təxmin et', 'Mesaj neçə hissəyə bölünür?', 'words = "salam kod dünyası".split()\nprint(len(words))', ['2', '3', '18', '1'], 1, 'split() boşluqlardan bölür: üç söz alınır.'),
      item('Boşluğu doldur', 'Hərfləri kiçilt.', 'name = "CODIGO"\nprint(name.___())', ['upper', 'split', 'lower', 'append'], 2, 'lower() böyük hərfləri kiçik hərflərə çevirir.'),
      item('Səhvi tap', 'İlk hərfi seçmək üçün düzgün kod hansıdır?', 'word = "kod"', ['word[1]', 'word[0]', 'word[3]', 'word(k)'], 1, 'Sətirlərdə də indeks 0-dan başlayır: word[0] → k.')
    ],
    dicts: [
      item('Təxmin et', 'Çantada neçə kristal var?', 'bag = {"crystal": 4}\nprint(bag["crystal"])', ['crystal', '0', '4', '1'], 2, 'Lüğətdə açarla onun dəyərini oxuyuruq.'),
      item('Boşluğu doldur', 'Mövcud olmayan açar üçün 0 qaytar.', 'counts = {}\nn = counts.___("a", 0)', ['get', 'append', 'split', 'lower'], 0, 'get açar tapılmayanda verdiyimiz standart dəyəri qaytarır.'),
      item('Səhvi tap', 'Kristal sayını bir artır.', 'bag = {"crystal": 4}', ['bag.append(1)', 'bag["crystal"] += 1', 'bag += 1', 'bag[4] = 1'], 1, 'Dəyişdirmək istədiyimiz dəyərə açarı ilə müraciət edirik.')
    ],
    rec: [
      item('Təxmin et', '3! neçədir?', '3 * 2 * 1', ['3', '5', '6', '9'], 2, 'Faktorial 1-dən verilən ədədə qədər ədədlərin hasilidir.'),
      item('Boşluğu doldur', 'Rekursiyanı baza halında dayandır.', 'def fact(n):\n    if n <= 1:\n        return ___\n    return n * fact(n - 1)', ['0', '1', 'n + 1', 'fact(n)'], 1, '0! və 1! üçün nəticə 1-dir. Bu, rekursiyanı dayandıran baza halıdır.'),
      item('Səhvi tap', 'Çağırış niyə dayanmır?', 'def fact(n):\n    if n <= 1: return 1\n    return n * fact(n)', ['fact(n + 1) yaz', 'fact(n - 1) yaz', 'Baza halını sil', 'return-u sil'], 1, 'Hər çağırış baza halına yaxınlaşmalıdır. n - 1 bunu təmin edir.')
    ]
  };

  function Login({ onLogin }) {
    const [name, setName] = useState('');
    const [course, setCourse] = useState(false);
    const [code, setCode] = useState('');
    const [error, setError] = useState('');
    const input = useRef();
    const join = (role, track) => {
      if (!name.trim()) { setError('Başlamaq üçün adını yaz.'); input.current.focus(); return; }
      if (role === 'student' && track === 'class' && code.trim().toUpperCase() !== 'CODIGO') { setError('Bu demo üçün sinif kodu: CODIGO'); return; }
      onLogin(name.trim(), role, track);
    };
    return html`<div className="welcome">
      <div className="welcome-art"><a href="index.html"><${Wordmark} className="text-3xl" tagline=${true} /></a><div><${Capy} className="w-44 float mb-8" /><h1>Kiçik addımlar.<br/>Böyük bacarıqlar.</h1><p className="text-ink-500 mt-5 max-w-sm text-lg">Hər gün bir az kod, bir az kəşf. Bu yolda kapibara səninlədir.</p></div><div className="flex gap-5 text-sm font-extrabold text-ink-500"><span>✦ Öz tempində</span><span>✦ Praktika ilə</span><span>✦ Azərbaycan dilində</span></div></div>
      <div className="welcome-main"><a href="index.html" className="text-sm font-bold text-ink-500">← Sayta qayıt</a><div className="eyebrow mt-8">SƏNİN YOLUN BURADAN BAŞLAYIR</div><h1 className="mt-3">Necə öyrənmək<br/>istəyirsən?</h1><p className="text-ink-500 mt-4">Python dünyasını özün kəşf et və ya sinfinə qoşul.</p>
        <label htmlFor="loginName" className="block font-extrabold text-sm mt-6 mb-2">Sənə necə müraciət edək?</label><input ref=${input} id="loginName" autoComplete="given-name" maxLength=${50} placeholder="Adın" value=${name} onInput=${e => {setName(e.target.value); setError('');}} className="w-full border-2 border-ink-200 rounded-2xl p-3 font-bold" />
        <button className="welcome-choice" onClick=${() => join('student','self')}><span className="text-3xl">🧭</span><span className="flex-1"><b>Özüm öyrənirəm</b><small>Səviyyəni tap, şəxsi yoluna başla.</small></span><${Icon} name="ArrowRight" size=${20}/></button>
        <button className="welcome-choice" aria-expanded=${course} onClick=${() => {setCourse(!course);setError('');}}><span className="text-3xl">🎒</span><span className="flex-1"><b>Siniflə öyrənirəm</b><small>Müəllimin dərsinə uyğun lab və məşqlər.</small></span><${Icon} name="ChevronDown" size=${20}/></button>
        ${course ? html`<div className="rounded-2xl bg-brand-50 p-4 mt-4"><label htmlFor="classCode" className="font-extrabold text-sm">Sinif kodu <span className="text-ink-500">· demo: CODIGO</span></label><div className="flex gap-2 mt-2"><input id="classCode" value=${code} onInput=${e=>setCode(e.target.value)} placeholder="CODIGO" className="w-full min-w-0 border-2 border-ink-200 rounded-xl p-2 font-bold"/><button className="chunky" onClick=${()=>join('student','class')}>Qoşul</button></div></div>` : null}
        ${error ? html`<p role="alert" className="text-rose-500 text-sm font-bold mt-4">${error}</p>` : null}
        <button className="w-full text-center text-brand-600 font-extrabold mt-7" onClick=${()=>join('teacher','class')}>Müəlliməm →</button><p className="text-xs text-ink-400 text-center mt-5">Təqdimat demosu · hesablar bu brauzerdə saxlanılır.<br/>Real qeydiyyat və cihazlararası sinif bağlantısı yoxdur.</p>
      </div></div>`;
  }

  function CapyNote({children}) { return html`<div className="capy-note"><${Capy} className=""/><div>${children}</div></div>`; }
  function MascotMoment({text}) {
    const [visible,setVisible]=useState(true);
    useEffect(()=>{setVisible(true);const t=setTimeout(()=>setVisible(false),9000);return()=>clearTimeout(t);},[text]);
    return visible ? html`<aside className="capy-pop" aria-label="Kapibaranın mesajı"><${CapyNote}>${text}<//><button aria-label="Mesajı bağla" onClick=${()=>setVisible(false)}><${Icon} name="X" size=${16}/></button></aside>` : null;
  }

  function Journey({st, openQuest, openLesson, update}) {
    const nextIndex = MODULES.findIndex((m,i) => unlocked(st,i) && (!st.lessons[m.id] || allQuests(st).some(q=>q.module===m.id&&!st.completed[q.id])));
    const [sel,setSel]=useState(Math.max(0,nextIndex));
    const mod=MODULES[sel], open=unlocked(st,sel), qs=allQuests(st).filter(q=>q.module===mod.id);
    const today=dayKey(), daily=st.dailyXP[today]||0, goal=st.dailyGoal||100;
    const dates=Array.from({length:7},(_,i)=>{const d=new Date();d.setDate(d.getDate()-6+i);return d;});
    const completed=st.lessons[mod.id];
    return html`<div className="journey">
      <div className="journey-intro"><div><div className="eyebrow">${st.track==='class'?'SİNİF YOLU · '+(st.plan?.name||'10-A PYTHON'):'ÖZ YOLUN · PYTHON'}</div><h2>Bir addım da irəli, ${st.user.name.split(' ')[0]}.</h2><p className="text-ink-500 text-sm mt-2">${st.track==='class'?'Dərsini möhkəmləndir, müəllimin lablarında tətbiq et.':'Kiçik məşqlərlə başla. Öz kodunu yazmağa qədər irəlilə.'}</p></div><span className="chunky secondary"><${Icon} name="Zap" size=${17}/> ${st.xp} XP</span></div>
      <div className="journey-layout"><section>
        <div className="module-tabs" aria-label="Mövzular">${MODULES.map((m,i)=>html`<button key=${m.id} className=${sel===i?'selected':''} onClick=${()=>setSel(i)} aria-pressed=${sel===i}>${i+1}. ${m.name}${!unlocked(st,i)?' 🔒':''}</button>`)}</div>
        <div className="unit-banner"><span className="rounded-2xl bg-white/15 p-3"><${Icon} name=${mod.icon} size=${28}/></span><div><div className="text-xs font-extrabold tracking-widest opacity-80">BÖLMƏ ${sel+1} · ${st.track==='class'?'SİNİF PRAKTİKASI':'KƏŞF YOLU'}</div><h3>${mod.name}</h3><p>${mod.desc} · ${qs.length+1} dayanacaq</p></div></div>
        ${!open ? html`<p className="text-sm font-bold text-ink-500 mt-5 text-center">Əvvəlki bölmənin məşqini və lablarını tamamla və ya 50 bacarıq balına çat.</p>`:null}
        <div className="trail">
          <div className="trail-node" style=${{transform:'translateX(-38px)'}}>${open&&!completed?html`<span className="trail-label">BURADAN BAŞLA</span>`:null}<button className=${'trail-button '+(completed?'complete':'')} disabled=${!open} onClick=${()=>openLesson(mod.id)} aria-label=${mod.name+' interaktiv dərsinə başla'}><${Icon} name=${completed?'Check':open?'Play':'Lock'} size=${30}/></button><b>Öyrən və sına · 3 məşq</b></div>
          ${qs.map((q,i)=>html`<div key=${q.id} className="trail-node" style=${{transform:'translateX('+(i%2===0?42:-38)+'px)'}}><button className=${'trail-button '+(st.completed[q.id]?'complete':'')} disabled=${!open} onClick=${()=>openQuest(q.id)} aria-label=${q.title+' labını aç'}><${Icon} name=${st.completed[q.id]?'Check':open?'Code2':'Lock'} size=${28}/></button><b>${q.title}</b><small className="text-ink-400 text-xs">${st.track==='class'&&st.published.includes(q.id)?'Müəllimdən · ':''}+${q.xp} XP · kod laboratoriyası</small></div>`)}
          <div className="trail-node"><span className="text-4xl">${completed&&qs.every(q=>st.completed[q.id])?'🏆':'🏁'}</span><b>Bölmənin sonu</b><small className="text-ink-400 text-xs">Məşq + lablar = növbəti dayanacaq</small></div>
        </div>
        <${CapyNote}>${completed?'Məşqi tamamladın! İndi bildiklərini labda öz kodunla sınayaq.':'Səhv etmək olar. Çətin gələn sualları birlikdə yenidən məşq edəcəyik.'}<//>
      </section><aside className="journey-aside">
        <div className="journey-panel"><h3 className="flex items-center gap-2"><${Icon} name="Target" className="text-mint-600" size=${21}/>Gündəlik hədəf</h3><div className="flex justify-between text-sm font-bold"><span>${daily>=goal?'Əla! Hədəfin tamamlandı.':'Bu gün özünə vaxt ayır.'}</span><span>${daily}/${goal}</span></div><div className="goal-track"><i style=${{width:Math.min(100,daily/goal*100)+'%'}}></i></div><label className="text-xs text-ink-500 font-bold">Gündəlik XP <select className="ml-2 rounded-lg border border-ink-200 p-1" value=${goal} onChange=${e=>update(s=>({...s,dailyGoal:Number(e.target.value)}))}><option value="50">50 · rahat</option><option value="100">100 · normal</option><option value="200">200 · intensiv</option></select></label></div>
        <div className="journey-panel"><h3 className="flex items-center gap-2"><${Icon} name="Flame" size=${22} className="text-capy-600"/>${st.streak} günlük ardıcıllıq</h3><p className="text-xs text-ink-500">Hər gün XP qazan, öyrənmə vərdişini böyüt.</p><div className="week-days">${dates.map(d=>{const k=dayKey(d),active=!!st.dailyXP[k];return html`<span key=${k} className=${active?'active':''}><i>${active?'✓':d.getDate()}</i>${['B','B.e','Ç.a','Ç','C.a','C','Ş'][d.getDay()]}</span>`;})}</div></div>
        <div className="journey-panel"><div className="eyebrow">SƏNİN YOL YOLDAŞIN</div><${Capy} className="w-24 mx-auto my-4 float"/><h3 className="text-center">Tələsmə. Başa düş.</h3><p className="text-sm text-ink-500 text-center">Hazır cavabdan əvvəl bir ipucu, bir cəhd və bir kəşf.</p></div>
        ${st.track==='class'?html`<div className="journey-panel"><h3>Sinif materialı</h3><p className="text-sm text-ink-500">${st.plan?st.plan.name:'10-A · Python əsasları'}</p>${st.plan?.weeks?.length?html`<ul className="mt-3 grid gap-2 text-xs text-ink-500">${st.plan.weeks.map(w=>html`<li key=${w.week}>H${w.week} · ${w.topic}</li>`)}</ul>`:html`<p className="text-xs mt-2 text-ink-400">Müəllim panelindən material əlavə et. Təsdiqlənən lablar bu yola qoşulur.</p>`}</div>`:null}
      </aside></div><${MascotMoment} text=${'Xoş gəldin! Bu gün '+mod.name.toLocaleLowerCase('az')+' mövzusunda kiçik bir addım ataq.'}/>
    </div>`;
  }

  function Lesson({moduleId, st, finish, back, openQuest}) {
    const mod=MODULES.find(m=>m.id===moduleId), questions=LESSONS[moduleId];
    const [queue,setQueue]=useState(()=>questions.map((_,i)=>i));
    const [index,setIndex]=useState(0),[picked,setPicked]=useState(null),[feedback,setFeedback]=useState(null);
    const [mistakes,setMistakes]=useState(0),[done,setDone]=useState(false),[solved,setSolved]=useState([]);
    const q=questions[queue[index]], awarded=useRef(false), first=useRef(!st.lessons[moduleId]).current;
    const answer=()=>{
      if(picked===null||feedback)return;
      const ok=picked===q.answer;
      if(ok) setSolved(s=>[...new Set([...s,queue[index]])]);
      else {setMistakes(v=>v+1);setQueue(v=>[...v,queue[index]]);}
      setFeedback(ok?'correct':'retry');
    };
    const next=()=>{
      if(index+1>=queue.length){setDone(true);if(!awarded.current){awarded.current=true;finish(moduleId,mistakes);}return;}
      setIndex(i=>i+1);setPicked(null);setFeedback(null);
    };
    const lab=allQuests(st).find(x=>x.module===moduleId&&!st.completed[x.id])||allQuests(st).find(x=>x.module===moduleId);
    if(done)return html`<div className="lesson text-center"><div className="lesson-card"><div className="text-5xl mb-5">🎉</div><${Capy} className="w-32 mx-auto float"/><div className="eyebrow mt-7">BİR ADDIM DA İRƏLİ</div><h2>${mod.name}: bacardın!</h2><p className="text-ink-500">${mistakes?'Çətin suallara qayıtdın və hər birini düzgün həll etdin.':'Hər üç məşqi ilk cəhddə düzgün həll etdin!'}</p><div className="grid grid-cols-3 gap-3 my-7">${[['XP',first?'+50':'Təkrar'],['Məşq','3/3'],['Əlavə cəhd',mistakes]].map(([k,v])=>html`<div key=${k} className="bg-brand-50 rounded-2xl p-4"><b className="text-brand-600 text-xl block">${v}</b><small className="font-bold text-ink-500">${k}</small></div>`)}</div><${CapyNote}>İndi öz kodunu yazmağa hazırsan. Bildiklərini laboratoriyada tətbiq edək!<//><div className="lesson-footer"><button className="chunky secondary" onClick=${back}>Yoluma qayıt</button>${lab?html`<button className="chunky" onClick=${()=>openQuest(lab.id)}>Kodu özün yaz <${Icon} name="ArrowRight" size=${18}/></button>`:null}</div></div></div>`;
    return html`<div className="lesson"><div className="lesson-top"><button onClick=${back} aria-label="Dərsdən çıx" className="p-2"><${Icon} name="X" size=${24}/></button><div className="goal-track" role="progressbar" aria-valuenow=${solved.length} aria-valuemin=${0} aria-valuemax=${3} aria-label="Tamamlanmış məşqlər"><i style=${{width:solved.length/3*100+'%'}}></i></div><b className="text-sm text-ink-500">${solved.length}/3</b></div>
      <${CapyNote}>${index>=3?'Bu sualı bir də sınayaq. İpucunu xatırla, tələsmə.':index===0?'Əvvəlcə kodu oxu. Səncə nə baş verəcək?':'Yaxşı gedirsən! İndi növbəti kiçik addım.'}<//>
      <div className="lesson-card"><div className="eyebrow">${mod.name} · ${q.type}${index>=3?' · MÖHKƏMLƏNDİRMƏ':''}</div><h2>${q.q}</h2><pre className="lesson-code">${q.code}</pre>
      ${moduleId==='loops'&&queue[index]===0?html`<div className="bridge" aria-label=${feedback==='correct'?'Üç körpü hissəsi quruldu':'Kodla üç körpü hissəsi qur'}><${Capy} className=""/>${[0,1,2].map(i=>html`<i key=${i} className=${feedback==='correct'?'built':''}></i>`)}<span className="text-3xl">🚩</span></div>`:null}
      <div className="answer-grid">${q.options.map((o,i)=>html`<button key=${i} disabled=${!!feedback} aria-pressed=${picked===i} className=${'answer-option '+(picked===i?(feedback==='correct'?'correct':feedback?'incorrect':'selected'):'')} onClick=${()=>setPicked(i)}><span>${i+1}</span>${o}</button>`)}</div>
      ${feedback?html`<div className=${'answer-feedback '+(feedback==='retry'?'retry':'')} role="status"><b>${feedback==='correct'?'Düz tapdın!':'Səhv etmək öyrənməyin bir hissəsidir.'}</b><p className="text-sm mt-1">${q.explanation}</p>${feedback==='retry'?html`<p className="text-xs font-bold mt-2">Bu sualı dərsin sonunda bir də məşq edəcəyik.</p>`:null}</div>`:null}
      <div className="lesson-footer"><span className="text-xs text-ink-400 font-bold">${first?'Dərsi tamamla · +50 XP':'Təkrar məşq · XP təkrar verilmir'}</span><button className="chunky" disabled=${picked===null} onClick=${feedback?next:answer}>${feedback?'Davam et':'Yoxla'}<${Icon} name="ArrowRight" size=${18}/></button></div></div>
    </div>`;
  }
  return {Login,Journey,Lesson,MascotMoment};
};
