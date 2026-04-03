/* ── pages ── */
function show(id: string): void {
  const el = document.getElementById(id);
  if (el) el.style.display = (id === 'pg-win' ? 'flex' : 'block');
}
function hide(id: string): void {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

/* ── audio ── */
let ctx: AudioContext | null = null;
function ac(): AudioContext {
  if (!ctx) ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
  if (ctx.state === 'suspended') ctx.resume();
  return ctx;
}
function beep(f: number, t: OscillatorType, d: number, v: number, dl: number = 0): void {
  try {
    const c = ac();
    const o = c.createOscillator();
    const g = c.createGain();
    o.connect(g);
    g.connect(c.destination);
    o.type = t;
    o.frequency.value = f;
    g.gain.setValueAtTime(v, c.currentTime + dl);
    g.gain.exponentialRampToValueAtTime(0.001, c.currentTime + dl + d);
    o.start(c.currentTime + dl);
    o.stop(c.currentTime + dl + d + 0.05);
  } catch (e) {
    console.error("Audio error", e);
  }
}
function sfxColor() { beep(520, 'sine', 0.12, 0.3); }
function sfxStar() { beep(880, 'sine', 0.15, 0.25); }
function sfxLevel() { beep(523, 'sine', 0.18, 0.3); beep(659, 'sine', 0.18, 0.3, 0.18); beep(784, 'sine', 0.28, 0.3, 0.36); }
function sfxWin() { beep(523, 'sine', 0.15, 0.3); beep(659, 'sine', 0.15, 0.3, 0.15); beep(784, 'sine', 0.15, 0.3, 0.3); beep(1047, 'sine', 0.4, 0.35, 0.45); }

/* ── game state ── */
let TIM: ReturnType<typeof setTimeout> | null = null;
let colorOn = false;
let paused = false;
let total = 0;
let levelStars = 0;
let currentLevel = 0;

interface Level {
  n: number;
  hold: number;
  gap: number;
  colors: string[];
  desc: string;
}
const LEVELS: Level[] = [
  { n: 1, hold: 2000, gap: 1000, colors: ['red', 'green'], desc: '<span style="color:#ef4444">الأحمر</span> ⬅️ يمين\n<span style="color:#10b981">الأخضر</span> ⬅️ يسار' },
  { n: 2, hold: 1500, gap: 800, colors: ['red', 'green', 'yellow'], desc: '<span style="color:#f59e0b">الأصفر</span> ⬅️ أمام\n+ القواعد السابقة' },
  { n: 3, hold: 1000, gap: 600, colors: ['red', 'green', 'yellow', 'blue'], desc: '<span style="color:#3b82f6">الأزرق</span> ⬅️ خلف\n+ القواعد السابقة' },
  { n: 4, hold: 700, gap: 400, colors: ['red', 'green', 'yellow', 'blue'], desc: 'أسرع!' },
  { n: 5, hold: 500, gap: 300, colors: ['red', 'green', 'yellow', 'blue'], desc: 'سرعة قصوى!' }
];
const PER = 3;
const NAMES = ["الأولى", "الثانية", "الثالثة", "الرابعة", "الخامسة"];
const COLORS: Record<string, string> = { 
  red: "radial-gradient(circle at center, #fca5a5, #ef4444)", 
  green: "radial-gradient(circle at center, #6ee7b7, #10b981)", 
  yellow: "radial-gradient(circle at center, #fde047, #f59e0b)", 
  blue: "radial-gradient(circle at center, #93c5fd, #3b82f6)" 
};
const DIR_TEXT: Record<string, string> = { red: "يمين", green: "يسار", yellow: "أمام", blue: "خلف" };

function lv(): Level { return LEVELS[currentLevel]; }

function stars(n: number): void {
  const r = document.getElementById('stars-row');
  if (!r) return;
  r.innerHTML = '';
  for (let i = 0; i < PER; i++) {
    const s = document.createElement('span');
    s.className = 'star';
    s.textContent = '★';
    s.style.color = i < n ? '#FFD700' : 'rgba(255,255,255,.3)';
    s.style.textShadow = i < n ? '0 0 15px rgba(245, 158, 11, 0.8)' : 'none';
    if (i === n - 1 && n > 0) {
      s.style.transform = 'scale(1.5) rotate(20deg)';
      setTimeout(() => { s.style.transform = 'scale(1) rotate(0deg)'; }, 400);
    }
    r.appendChild(s);
  }
}

/* ── actions ── */
function showLevelRules(isCongrats: boolean = false): void {
  const ann = document.getElementById('announce');
  if (!ann) return;
  const l = lv();
  
  let congratsHtml = '';
  if (isCongrats) {
    congratsHtml = `<div style="font-size:22px; color:#10b981; font-weight:900; margin-bottom:16px;">مبروك! إجتزت بنجاح 🎉</div>`;
  }
  
  ann.innerHTML = `
    ${congratsHtml}
    <div style="font-size:22px; margin-bottom:16px; font-weight:900;">المرحلة ${l.n}</div>
    <div style="font-size:18px; color:#444; white-space:pre-wrap; line-height:2; margin-bottom:24px; font-weight:700;">${l.desc}</div>
    <button id="btn-continue" class="btn-next theme-3" style="margin:0 auto; padding:12px 30px; font-size:18px;">استمرار</button>
  `;
  ann.style.display = 'block';
  
  const btn = document.getElementById('btn-continue');
  if (btn) {
    const startNext = (e?: Event) => {
      if (e) e.preventDefault();
      ann.style.display = 'none';
      btn.removeEventListener('click', startNext);
      btn.removeEventListener('touchend', startNext);
      nextRound();
    };
    btn.addEventListener('click', startNext);
    btn.addEventListener('touchend', startNext, { passive: false });
  }
}

function doStart(): void {
  ac();
  total = 0;
  levelStars = 0;
  colorOn = false;
  paused = false;
  currentLevel = 0;
  hide('pg-start');
  hide('logo');
  show('pg-game');
  const sl = document.getElementById('stars-label');
  if (sl) sl.textContent = 'المرحلة 1';
  stars(0);
  showLevelRules();
}

function doStop(): void {
  if (TIM) clearTimeout(TIM);
  colorOn = false;
  paused = false;
  hide('pg-game');
  const cf = document.getElementById('color-fill');
  if (cf) cf.style.background = '#e8e6de';
  const ann = document.getElementById('announce');
  if (ann) ann.style.display = 'none';
  show('pg-start');
  show('logo');
}

function doAgain(): void {
  hide('pg-win');
  show('pg-start');
  show('logo');
}

function nextRound(): void {
  if (paused) return;
  colorOn = false;
  const cf = document.getElementById('color-fill');
  if (cf) cf.style.background = '#e8e6de';
  const h = document.getElementById('hint');
  if (h) h.textContent = '';
  TIM = setTimeout(showColor, lv().gap);
}

function showColor(): void {
  if (paused) return;
  colorOn = true;
  total++;
  levelStars++;
  
  const cs = lv().colors;
  const c = cs[Math.floor(Math.random() * cs.length)];
  const cf = document.getElementById('color-fill');
  if (cf) cf.style.background = COLORS[c];
  
  sfxColor();
  
  const h = document.getElementById('hint');
  if (h) h.textContent = currentLevel <= 2 ? DIR_TEXT[c] : '';
  
  const sl = document.getElementById('stars-label');
  if (sl) sl.textContent = 'المرحلة ' + LEVELS[currentLevel].n;
  stars(levelStars);
  sfxStar();
  
  TIM = setTimeout(() => {
    colorOn = false;
    const cf = document.getElementById('color-fill');
    if (cf) cf.style.background = '#e8e6de';
    const h = document.getElementById('hint');
    if (h) h.textContent = '';
    
    if (levelStars >= PER) {
      paused = true;
      doLevelEnd();
    } else {
      nextRound();
    }
  }, lv().hold);
}

function doLevelEnd(): void {
  if (currentLevel >= LEVELS.length - 1) {
    doWin();
    return;
  }
  
  sfxLevel();
  currentLevel++;
  total = 0;
  levelStars = 0;
  paused = false;
  stars(0);
  
  const sl = document.getElementById('stars-label');
  if (sl) sl.textContent = 'المرحلة ' + LEVELS[currentLevel].n;
  
  showLevelRules(true);
}

function doWin(): void {
  hide('pg-game');
  show('pg-win');
  sfxWin();
}

function tapGame(): void {
  if (!colorOn || paused) return;
  if (TIM) clearTimeout(TIM);
  colorOn = false;
  const cf = document.getElementById('color-fill');
  if (cf) cf.style.background = '#e8e6de';
  const h = document.getElementById('hint');
  if (h) h.textContent = '';
  if (levelStars >= PER) {
    paused = true;
    doLevelEnd();
  } else {
    nextRound();
  }
}

/* ── wire buttons ── */
function wire(id: string, fn: (e?: Event) => void): void {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener('touchend', (e) => { e.preventDefault(); fn(); }, { passive: false });
  el.addEventListener('click', fn);
}

window.addEventListener('DOMContentLoaded', () => {
    wire('btn-start', doStart);
    wire('btn-stop', doStop);
    wire('btn-again', doAgain);

    const fill = document.getElementById('color-fill');
    if (fill) {
        fill.addEventListener('touchend', (e) => { e.preventDefault(); tapGame(); }, { passive: false });
        fill.addEventListener('click', tapGame);
    }
});
