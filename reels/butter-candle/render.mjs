// Renders composition.html frame-by-frame with headless Chromium, then encodes
// the final MP4 with ffmpeg (voiceover + ducked music + sound effects).
//
//   node render.mjs                 full render  -> out/ideaspulse_butter_candle_reel.mp4
//   node render.mjs --stills 1,8,20 a few PNG stills (seconds) -> out/stills/
//   node render.mjs --workers 4     parallel browser pages (default 4)
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
const OUT = 'out/ideaspulse_butter_candle_reel.mp4';
const run = (cmd, a) => { const r = spawnSync(cmd, a, { stdio: 'inherit', cwd: ROOT }); if (r.status !== 0) throw new Error(`${cmd} failed`); };

// 1) prerequisites
const dirs = ['creatorA', 'creatorB', 'creatorC', 'b1', 'b2', 'b3'];
if (dirs.some(d => !fs.existsSync(path.join(ROOT, 'build', d)))) run('bash', ['scripts/build_base.sh']);
if (!fs.existsSync(path.join(ROOT, "assets/images/qr_youtube.png")) || !fs.existsSync(path.join(ROOT, "assets/pdf_pages/page-01.png"))) run('python3', ['scripts/prep_assets.py']);
const counts = Object.fromEntries(dirs.map(d => [d, fs.readdirSync(path.join(ROOT, 'build', d)).filter(f => f.endsWith('.jpg')).length]));

const FPS = TL.fps, total = Math.round(TL.duration * FPS);
const times = STILLS ? STILLS.split(',').map(Number) : [...Array(total).keys()].map(i => i / FPS);
const outFrames = path.join(ROOT, STILLS ? 'out/stills' : 'build/frames');
fs.rmSync(outFrames, { recursive: true, force: true });
fs.mkdirSync(outFrames, { recursive: true });

// 2) frames
const browser = await chromium.launch();
const url = pathToFileURL(path.join(ROOT, 'composition.html')).href;
const t0 = Date.now(); let done = 0;
async function worker(w) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto(url);
  await page.evaluate(([tl, c]) => window.init(tl, c), [TL, counts]);
  for (let i = w; i < times.length; i += WORKERS) {
    const t = times[i];
    await page.evaluate(tt => window.renderAt(tt), t);
    const name = STILLS ? `still_${t.toFixed(2)}s.png` : `${String(i).padStart(5, '0')}.jpg`;
    await page.screenshot({ path: path.join(outFrames, name), type: STILLS ? 'png' : 'jpeg', quality: STILLS ? undefined : 95 });
    if (++done % 90 === 0) console.log(`frames ${done}/${times.length}  (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
  }
  await page.close();
}
await Promise.all([...Array(Math.min(WORKERS, times.length)).keys()].map(worker));
await browser.close();
console.log(`rendered ${times.length} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
if (STILLS) process.exit(0);

// 3) audio + encode
run('python3', ['scripts/make_audio.py']);
fs.mkdirSync(path.join(ROOT, 'out'), { recursive: true });
const A = TL.audio, dur = (total / FPS).toFixed(3);
const filter = [
  `[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=${A.voice_gain_db}dB,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=3dB,apad,asplit=2[vo][key]`,
  `[2:a]aresample=48000,volume=${A.music_gain_db}dB[mus]`,
  `[mus][key]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[duck]`,
  `[3:a]aresample=48000,volume=${A.sfx_gain_db}dB[sfx]`,
  `[vo][duck][sfx]amix=inputs=3:duration=longest:normalize=0,atrim=0:${dur},loudnorm=I=${A.target_lufs}:TP=-1.0:LRA=9[aout]`
].join(';');
run('ffmpeg', ['-loglevel', 'error', '-y',
  '-framerate', String(FPS), '-i', 'build/frames/%05d.jpg',
  '-i', 'assets/source/voiceover.mp3', '-i', 'build/music.wav', '-i', 'build/sfx.wav',
  '-filter_complex', filter, '-map', '0:v', '-map', '[aout]',
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high', '-level', '4.1',
  '-pix_fmt', 'yuv420p', '-r', String(FPS), '-g', String(FPS * 2),
  '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', '-t', dur, OUT]);
run('ffmpeg', ['-loglevel', 'error', '-y', '-i', OUT, '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '26', '-preset', 'veryfast',
  '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', 'out/preview_540p.mp4']);
console.log('done -> ' + OUT);
