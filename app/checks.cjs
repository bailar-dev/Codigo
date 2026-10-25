// Regression checks for the demo's learning state. Run: node app/checks.cjs
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, 'codego-app.html'), 'utf8');
const store = new Map();
const sandbox = {localStorage:{getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,v)}};
vm.createContext(sandbox);
vm.runInContext(source.slice(source.indexOf('const MODULES ='),source.indexOf('const QUIZ =')) +
  source.slice(source.indexOf('const KEY ='),source.indexOf('const nowStr =')) +
  ';globalThis.api={fresh,awardXP,normalizeDay,dayKey,yesterdayKey,save,loginState,allQuests,unlocked,MODULES,QUESTS,DRAFTS,withCourse};',sandbox);
const a = sandbox.api;
let s = a.fresh();
assert.equal(s.streak,0);
s = a.awardXP(s,50);
assert.equal(s.streak,1);
s = a.awardXP(s,100);
assert.equal(s.streak,1,'same day cannot increase streak twice');
assert.equal(s.dailyXP[a.dayKey()],150);
s.lastActive=a.yesterdayKey(); s.streak=4;
s=a.awardXP(s,50);
assert.equal(s.streak,5,'consecutive day extends streak');
s.lastActive='2000-01-01';s=a.normalizeDay(s);
assert.equal(s.streak,0,'missed days reset streak');
s=a.awardXP(s,50);assert.equal(s.streak,1);

// Even with minimal mastery and all hints used, completing a module opens the next.
s=a.fresh();
for(let i=0;i<a.MODULES.length;i++) {
  assert.ok(a.unlocked(s,i),a.MODULES[i].id+' must be reachable');
  s.lessons[a.MODULES[i].id]={mistakes:3};
  a.allQuests(s).filter(q=>q.module===a.MODULES[i].id).forEach(q=>s.completed[q.id]={hints:3});
}

// Browser-local profiles remain independent and survive logout/new login.
s=a.awardXP({...a.fresh(),user:{name:'A',role:'student'},track:'self'},50);a.save(s);
assert.equal(a.loginState('B','student','self').xp,0);
assert.equal(a.loginState('A','student','self').xp,50);
const teacher={...a.fresh(),track:'class',user:{name:'Teacher',role:'teacher'},plan:{name:'Test course',weeks:[]},published:[a.DRAFTS[0].id],modes:{}};
a.save(teacher);
const pupil=a.loginState('Pupil','student','class');
assert.equal(pupil.plan.name,'Test course');
assert.equal(a.allQuests(pupil).length,a.QUESTS.length+1);
assert.equal(a.allQuests(a.loginState('A','student','self')).length,a.QUESTS.length);

for (const [i,m] of [...source.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].entries()) new vm.Script(m[1],{filename:'app-script-'+i});
console.log('PASS: daily XP, streak rollover, all 8 module paths, separate profiles, classroom lab sharing, JS syntax.');
