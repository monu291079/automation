// Renders the 16:9 YouTube video: composition.html frame-by-frame in headless Chromium,
// then mixes voiceover parts + original music + sound effects and encodes MP4s.
//
//   node render.mjs                    full render -> out/ideaspulse_flower_incense_youtube.mp4
//   node render.mjs --stills 10,120    PNG stills at those seconds -> out/stills/
//   node render.mjs --plan             only print the absolute timeline / chapters
import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const TL = JSON.parse(fs.readFileSync(path.join(ROOT, 'timeline.json'), 'utf8'));
const args = process.argv.slice(2);
const arg = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const WORKERS = Number(arg('--workers', 4));
const STILLS = arg('--stills', null);
const OUT = 'out/ideaspulse_flower_incense_youtube.mp4';
const run = (cmd, a) => { const r = spawnSync(cmd, a, { stdio: 'inherit', cwd: ROOT }); if (r.status !== 0) throw new Error(`${cmd} failed`); };
const probe = f => Number(spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], { cwd: ROOT }).stdout.toString().trim());
const mmss = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;

// ---------------------------------------------------------------- absolute timeline
let cur = TL.intro;
const parts_abs = [], ov_abs = [], bg_abs = [], full_abs = [], sfx_abs = [];
full_abs.push({ type: 'intro', t0: 0, t1: TL.intro, ...TL.intro_card });
sfx_abs.push({ t: 0.0, type: 'shimmer' }, { t: 0.75, type: 'impact' });
TL.parts.forEach((p, k) => {
  if (k > 0) {
    full_abs.push({ type: 'chapter', n: k + 1, title: p.chapter, t0: cur, t1: cur + TL.gap });
    sfx_abs.push({ t: cur - 0.45, type: 'riser' }, { t: cur + 0.2, type: 'impact' });
    cur += TL.gap;
  }
  const dur = probe(p.file), start = cur, end = cur + dur;
  parts_abs.push({ id: p.id, file: p.file, start, end, dur, short: p.short, chapter: p.chapter, gapAfter: k < TL.parts.length - 1 ? TL.gap : 0 });
  p.bg.forEach((b, i) => {
    const t0 = start + b.t, t1 = i + 1 < p.bg.length ? start + p.bg[i + 1].t : end + (k < TL.parts.length - 1 ? TL.gap : 0);
    bg_abs.push({ ...b, t0, t1 });
    if (i > 0) sfx_abs.push({ t: t0 - 0.06, type: 'whoosh' });
  });
  p.ov.forEach(o => {
    const sh = x => x === undefined || x === null ? x : start + x;
    const a = { ...o, t0: sh(o.t0), t1: sh(o.t1), at: sh(o.at), sub_at: sh(o.sub_at) };
    for (const key of ['items', 'chips', 'blocks', 'cards']) if (a[key]) a[key] = a[key].map(it => ({ ...it, at: sh(it.at) }));
    if (a.cols) a.cols = a.cols.map(c => ({ ...c, rows: c.rows.map(r => ({ ...r, at: sh(r.at) })) }));
    ov_abs.push(a);
    if (['title', 'stamp', 'stat'].includes(o.type)) sfx_abs.push({ t: a.at, type: 'impact' });
    for (const key of ['items', 'chips', 'blocks', 'cards']) (a[key] || []).forEach(it => sfx_abs.push({ t: it.at, type: it.total ? 'shimmer' : 'pop' }));
    (a.cols || []).forEach(c => c.rows.forEach(r => sfx_abs.push({ t: r.at, type: r.total ? 'shimmer' : 'tick' })));
  });
  cur = end;
});
full_abs.push({ type: 'end', t0: cur, t1: cur + TL.end_screen, ...TL.end_card });
sfx_abs.push({ t: cur, type: 'whoosh' }, { t: cur + 0.6, type: 'shimmer' });
const DURATION = cur + TL.end_screen;
sfx_abs.sort((a, b) => a.t - b.t);
const ABS = { ...TL, parts_abs, ov_abs, bg_abs, full_abs, sfx_abs, duration: DURATION };

// YouTube chapters
const chapters = [`0:00 Intro`, ...parts_abs.map((p, k) => `${mmss(k ? p.start - TL.gap : TL.intro)} ${String(k + 1).padStart(2, '0')}. ${p.chapter}`), `${mmss(cur)} Community + End`];
fs.mkdirSync(path.join(ROOT, 'out'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'out', 'youtube_chapters.txt'), chapters.join('\n') + '\n');
if (args.includes('--plan')) { console.log(chapters.join('\n')); console.log('duration', DURATION.toFixed(2), 'frames', Math.round(DURATION * TL.fps)); process.exit(0); }

// ---------------------------------------------------------------- frames
const clipDir = path.join(ROOT, 'build', 'clips');
if (!fs.existsSync(clipDir)) run('bash', ['scripts/build_base.sh']);
const counts = Object.fromEntries(fs.readdirSync(clipDir).map(d => [d, fs.readdirSync(path.join(clipDir, d)).length]));
const FPS = TL.fps, total = Math.round(DURATION * FPS);
const times = STILLS ? STILLS.split(',').map(Number) : [...Array(total).keys()].map(i => i / FPS);
const outFrames = path.join(ROOT, STILLS ? 'out/stills' : 'build/frames');
fs.rmSync(outFrames, { recursive: true, force: true }); fs.mkdirSync(outFrames, { recursive: true });

const browser = await chromium.launch();
const url = pathToFileURL(path.join(ROOT, 'composition.html')).href;
const t0 = Date.now(); let done = 0;
async function worker(w) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto(url);
  await page.evaluate(([tl, c]) => window.init(tl, c), [ABS, counts]);
  for (let i = w; i < times.length; i += WORKERS) {
    await page.evaluate(tt => window.renderAt(tt), times[i]);
    const name = STILLS ? `still_${times[i].toFixed(2)}s.png` : `${String(i).padStart(6, '0')}.jpg`;
    await page.screenshot({ path: path.join(outFrames, name), type: STILLS ? 'png' : 'jpeg', quality: STILLS ? undefined : 92 });
    if (++done % 600 === 0) console.log(`frames ${done}/${times.length}  (${((Date.now() - t0) / 60000).toFixed(1)} min)`);
  }
  await page.close();
}
await Promise.all([...Array(Math.min(WORKERS, times.length)).keys()].map(worker));
await browser.close();
console.log(`rendered ${times.length} frames in ${((Date.now() - t0) / 60000).toFixed(1)} min`);
if (STILLS) process.exit(0);

// ---------------------------------------------------------------- audio
fs.writeFileSync(path.join(ROOT, 'build', 'audio_plan.json'), JSON.stringify({ duration: DURATION, sfx: sfx_abs, chapters: full_abs.map(f => f.t0) }));
run('python3', ['scripts/make_music.py']);
// voiceover: each part placed at its absolute start
const vin = parts_abs.flatMap(p => ['-i', p.file]);
const vf = parts_abs.map((p, k) => `[${k}:a]aresample=48000,pan=mono|c0=c0,adelay=${Math.round(p.start * 1000)}[v${k}]`).join(';') +
  ';' + parts_abs.map((_, k) => `[v${k}]`).join('') + `amix=inputs=${parts_abs.length}:normalize=0:duration=longest,apad,atrim=0:${DURATION.toFixed(3)}[vo]`;
run('ffmpeg', ['-loglevel', 'error', '-y', ...vin, '-filter_complex', vf, '-map', '[vo]', 'build/voiceover_full.wav']);
const A = { voice_gain_db: 0, music_gain_db: -19, sfx_gain_db: -13, target_lufs: -14, ...(TL.audio || {}) };
const mix = [
  `[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=${A.voice_gain_db}dB,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=150:makeup=3dB,asplit=2[vo][key]`,
  `[2:a]aresample=48000,volume=${A.music_gain_db}dB[mus]`,
  `[mus][key]sidechaincompress=threshold=0.025:ratio=5:attack=20:release=450[duck]`,
  `[3:a]aresample=48000,volume=${A.sfx_gain_db}dB[sfx]`,
  `[vo][duck][sfx]amix=inputs=3:duration=first:normalize=0,loudnorm=I=${A.target_lufs}:TP=-1.0:LRA=11[aout]`].join(';');
run('ffmpeg', ['-loglevel', 'error', '-y', '-framerate', String(FPS), '-i', 'build/frames/%06d.jpg',
  '-i', 'build/voiceover_full.wav', '-i', 'build/music.wav', '-i', 'build/sfx.wav',
  '-filter_complex', mix, '-map', '0:v', '-map', '[aout]',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-maxrate', '8M', '-bufsize', '16M', '-profile:v', 'high', '-level', '4.2',
  '-pix_fmt', 'yuv420p', '-r', String(FPS), '-g', String(FPS * 2), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart',
  '-t', DURATION.toFixed(3), OUT]);
// phone-friendly 720p copy
run('ffmpeg', ['-loglevel', 'error', '-y', '-i', OUT, '-vf', 'scale=1280:720', '-c:v', 'libx264', '-preset', 'medium', '-crf', '25', '-maxrate', '1500k', '-bufsize', '3000k',
  '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', OUT.replace('.mp4', '_720p_mobile.mp4')]);
console.log('done -> ' + OUT);
