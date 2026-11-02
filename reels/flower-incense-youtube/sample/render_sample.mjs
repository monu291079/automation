// 15 s kinetic-typography sample: frames via Chromium, audio = voiceover (P1) + music + SFX.
//   node sample/render_sample.mjs            full render -> out/sample15_kinetic.mp4
//   node sample/render_sample.mjs --stills 1,5.9
import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), ROOT = path.join(HERE, '..');
const args = process.argv.slice(2), STILLS = args.includes('--stills') ? args[args.indexOf('--stills') + 1] : null;
const run = (c, a, o = {}) => { const r = spawnSync(c, a, { stdio: 'inherit', cwd: ROOT, ...o }); if (r.status !== 0) throw new Error(c + ' failed'); };
const units = JSON.parse(fs.readFileSync(path.join(HERE, 'words.json'), 'utf8'));
const DUR = 15, FPS = 30, N = DUR * FPS, VOICE_END = 14.4;
const times = STILLS ? STILLS.split(',').map(Number) : [...Array(N).keys()].map(i => i / FPS);
const FR = path.join(HERE, STILLS ? 'stills' : 'frames'); fs.rmSync(FR, { recursive: true, force: true }); fs.mkdirSync(FR, { recursive: true });
const browser = await chromium.launch(); const url = pathToFileURL(path.join(HERE, 'kinetic.html')).href; let done = 0;
await Promise.all([0, 1, 2, 3].map(async w => {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(url); await page.evaluate(u => window.init(u), units);
  for (let i = w; i < times.length; i += 4) {
    await page.evaluate(t => window.renderAt(t), times[i]);
    await page.screenshot({ path: path.join(FR, STILLS ? `still_${times[i].toFixed(2)}.png` : `${String(i).padStart(5, '0')}.jpg`), type: STILLS ? 'png' : 'jpeg', ...(STILLS ? {} : { quality: 93 }) });
    done++;
  }
  await page.close();
}));
await browser.close(); console.log('frames', done);
if (STILLS) process.exit(0);

// ---- audio
const sfx = [];
for (const u of units) sfx.push({ t: u.t0, type: (u.style === 'r') ? 'impact' : (u.line === 'A' || u.line === 'B' || u.line === 'C') ? 'tick' : 'pop' });
for (const t of [4.82, 5.86, 7.38, 9.88, 11.05, 14.3]) sfx.push({ t, type: 'whoosh' });
sfx.push({ t: 6.85, type: 'riser' }, { t: 12.5, type: 'riser' }, { t: 7.44, type: 'shimmer' }, { t: 14.45, type: 'shimmer' }, { t: 14.4, type: 'impact' });
const B = path.join(HERE, 'build'); fs.mkdirSync(B, { recursive: true });
fs.writeFileSync(path.join(B, 'audio_plan.json'), JSON.stringify({ duration: DUR, sfx, chapters: [] }));
run('python3', ['scripts/make_music.py'], { env: { ...process.env, BUILD_DIR: B } });
const mix = [
  `[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=150:makeup=3dB,apad,atrim=0:${DUR},asplit=2[vo][key]`,
  `[2:a]aresample=48000,volume=-18dB[mus]`, `[mus][key]sidechaincompress=threshold=0.025:ratio=5:attack=20:release=450[duck]`,
  `[3:a]aresample=48000,volume=-11dB[sfx]`, `[vo][duck][sfx]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1:LRA=11,atrim=0:${DUR}[a]`].join(';');
run('ffmpeg', ['-loglevel', 'error', '-y', '-framerate', '30', '-i', 'sample/frames/%05d.jpg', '-t', String(VOICE_END), '-i', 'assets/audio/P1.wav',
  '-i', 'sample/build/music.wav', '-i', 'sample/build/sfx.wav', '-filter_complex', mix.replace('[1:a]aresample=48000', `[1:a]afade=t=out:st=14.28:d=0.12,aresample=48000`),
  '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', String(DUR), 'out/sample15_kinetic.mp4']);
console.log('done -> out/sample15_kinetic.mp4');
