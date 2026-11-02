import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { noise2D } from "@remotion/noise";
import { BRAND_GRADIENT, C, FONT, FluidGradientBg } from "./primitives";
import words from "./words.json";

// 15 s hook of "Mandir ke phoolon se agarbatti" : word-by-word kinetic type timed to the voiceover.
// Beats on the theme's solid fluid background where text needs to be crisp, full-bleed video where the picture carries it.

type Unit = { text: string; t0: number; t1: number; line: string; style: string };
const U = words as Unit[];
const FPS = 30;
const F = (s: number) => Math.round(s * FPS);
const lerp = (a: number, b: number, x: number) => a + (b - a) * x;
const pr = (f: number, a: number, b: number) => Math.min(1, Math.max(0, (f - a) / (b - a)));
const eo = (x: number) => 1 - Math.pow(1 - x, 3);
const eio = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const FromCtx = React.createContext(0);
const useAbs = () => useCurrentFrame() + React.useContext(FromCtx);
const line = (id: string) => U.filter((u) => u.line === id);
const IMPACTS: [number, number, number][] = [[4.86, 8, 0.3], [5.91, 20, 0.5], [13.14, 30, 0.7]];

const NAVY = { base: "linear-gradient(180deg,#172A49 0%,#12213A 55%,#0B1526 100%)", blob1: "rgba(33,140,135,0.45)", blob2: "rgba(226,190,106,0.30)", blob3: "rgba(57,194,186,0.22)", haze: "rgba(226,190,106,0.10)" };
const DUSK = { base: "linear-gradient(180deg,#1B2A66 0%,#3A2F6B 52%,#C9604A 100%)", blob1: "rgba(255,140,90,0.45)", blob2: "rgba(120,110,220,0.40)", blob3: "rgba(255,200,120,0.25)", haze: "rgba(255,170,110,0.12)" };

// ---------- word ----------
const Wd: React.FC<{ u: Unit; size: number; color?: string; gold?: boolean; slam?: boolean; reserve?: boolean; exitAt?: number }> = ({ u, size, color = C.ink, gold, slam, reserve, exitAt }) => {
  const abs = useAbs();
  const rel = abs - (F(u.t0) - 1);
  const sp = spring({ frame: Math.max(0, rel), fps: FPS, config: slam ? { damping: 11, stiffness: 230 } : { damping: 14, stiffness: 150 } });
  const xo = exitAt ? pr(abs, exitAt, exitAt + 7) : 0;
  const active = rel >= 0 && abs < F(u.t1) + 5;
  const vis = rel >= 0;
  if (!vis && !reserve) return null;
  const inner: React.CSSProperties = gold
    ? { background: BRAND_GRADIENT, WebkitBackgroundClip: "text", backgroundClip: "text", WebkitTextFillColor: "transparent", filter: "drop-shadow(0 7px 0 rgba(0,0,0,.6))" }
    : { color: active ? C.brandSoft : color, textShadow: `0 7px 0 rgba(0,0,0,.6), 0 0 ${active ? 60 : 30}px ${active ? "rgba(246,226,166,.75)" : "rgba(0,0,0,.6)"}` };
  const tf = slam
    ? `scale(${lerp(2.5, 1, sp)})`
    : `translateY(${(1 - sp) * 112 - xo * 90}%) skewY(${(1 - sp) * 7}deg)`;
  return (
    <span style={{ display: "inline-block", overflow: slam ? "visible" : "hidden", padding: "0.04em 0.05em", verticalAlign: "top", opacity: vis ? 1 - xo : 0 }}>
      <span style={{ display: "inline-block", fontFamily: FONT.display, textTransform: "uppercase", letterSpacing: 2, lineHeight: 1.04, fontSize: size, transform: tf, transformOrigin: "50% 80%", filter: slam ? `blur(${(1 - sp) * 16}px)` : undefined, WebkitTextStroke: gold ? undefined : "2px rgba(5,10,20,.5)", paintOrder: "stroke fill" as any, ...inner }}>{u.text}</span>
    </span>
  );
};
const Row: React.FC<{ id: string; size: number; style?: React.CSSProperties; reserve?: boolean; exitAt?: number; slam?: boolean }> = ({ id, size, style, reserve, exitAt, slam }) => (
  <div style={{ display: "flex", gap: size * 0.2, alignItems: "baseline", whiteSpace: "nowrap", ...style }}>
    {line(id).map((u, i) => <Wd key={i} u={u} size={size} gold={u.style === "g" || u.style === "s"} color={u.style === "r" ? C.danger : u.style === "d" ? C.dusk : C.ink} slam={slam ?? (u.style === "s" || u.style === "r")} reserve={reserve} exitAt={exitAt} />)}
  </div>
);

// ---------- scene wrapper (crossfade + gentle push, no black flashes) ----------
const Scene: React.FC<{ from: number; dur: number; first?: boolean; children: React.ReactNode }> = ({ from, dur, first, children }) => (
  <Sequence from={from} durationInFrames={dur}>
    <FromCtx.Provider value={from}><SceneIn dur={dur} first={first}>{children}</SceneIn></FromCtx.Provider>
  </Sequence>
);
const SceneIn: React.FC<{ dur: number; first?: boolean; children: React.ReactNode }> = ({ dur, first, children }) => {
  const f = useCurrentFrame();
  const o = (first ? 1 : interpolate(f, [0, 4], [0, 1], CL)) * interpolate(f, [dur - 4, dur], [1, 0], CL);
  return <AbsoluteFill style={{ opacity: o, transform: `scale(${first ? 1 : lerp(1.05, 1, eo(pr(f, 0, 7)))})` }}>{children}</AbsoluteFill>;
};

// ---------- small graphics ----------
const Ring: React.FC<{ at: number; color?: string; max?: number }> = ({ at, color = "226,190,106", max = 1300 }) => {
  const abs = useAbs(); const d = abs - F(at); if (d < 0 || d > 17) return null; const k = d / 17;
  const dia = 80 + max * eo(k);
  return <div style={{ position: "absolute", left: 960 - dia / 2, top: 540 - dia / 2, width: dia, height: dia, borderRadius: "50%", border: `${12 * (1 - k) + 2}px solid rgba(${color},${0.8 * (1 - k)})`, boxShadow: `0 0 60px rgba(${color},${0.4 * (1 - k)})` }} />;
};
const Vignette: React.FC<{ a?: number }> = ({ a = 0.6 }) => <AbsoluteFill style={{ background: `radial-gradient(110% 90% at 50% 50%, transparent 45%, rgba(0,0,0,${a}))`, pointerEvents: "none" }} />;

const Petals: React.FC = () => {
  const abs = useCurrentFrame();
  const vel = (t: number) => (t < 4.8 ? 70 : t < 5.9 ? lerp(70, 140, pr(t, 4.8, 5.9)) : t < 7.4 ? 520 : t < 9.55 ? -260 : t < 11.1 ? 140 : 320);
  let Y = 0; for (let f = 0; f < abs; f++) Y += vel(f / FPS) / FPS;
  const t = abs / FPS;
  const cols = ["#F59E0B", "#FB923C", "#BE123C"];
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {Array.from({ length: 56 }, (_, i) => {
        const r = (k: number) => Math.abs((Math.sin(i * k) * 43758.5453) % 1);
        const s = 10 + r(3.7) * 22, w = 0.6 + r(9.3) * 1.6, ph = r(2.2) * 6.28;
        const x = r(12.99) * 1920 + Math.sin(t * w + ph) * 50;
        const y = ((((r(78.23) * 1200 + Y) % 1200) + 1200) % 1200) - 70;
        const alpha = (t < 4.8 ? 0.6 : t < 9.6 ? 0.9 : 0.6) * (0.55 + 0.45 * Math.sin(ph * 3 + t));
        return <div key={i} style={{ position: "absolute", left: x, top: y, width: s * 2, height: s * 1.1, borderRadius: "50%", background: cols[i % 3], opacity: alpha, transform: `rotate(${r(5.1) * 360 + t * w * 50}deg) scaleY(${0.55 + 0.4 * Math.abs(Math.sin(t * w + ph))})` }} />;
      })}
    </AbsoluteFill>
  );
};

const Bin: React.FC<{ at: number }> = ({ at }) => {
  const abs = useAbs(); const d = abs - F(at);
  const sp = spring({ frame: Math.max(0, d), fps: FPS, config: { damping: 11, stiffness: 160 } });
  const lid = d < 8 ? -38 * pr(d, 0, 6) : d < 45 ? -38 : lerp(-38, 0, pr(d, 45, 52));
  return (
    <div style={{ position: "absolute", right: 150, top: 150, width: 360, height: 420, transform: `scale(${sp}) rotate(${lerp(14, 0, sp)}deg)`, opacity: d < 0 ? 0 : 1, filter: "drop-shadow(0 20px 40px rgba(0,0,0,.6))" }}>
      <svg viewBox="0 0 360 420" width="360" height="420">
        <g style={{ transformOrigin: "60px 90px", transform: `rotate(${lid}deg)` }}><rect x="40" y="62" width="280" height="30" rx="10" fill="#7C8798" /><rect x="140" y="38" width="80" height="30" rx="12" fill="#98A3B5" /></g>
        <path d="M60 100 H300 L276 400 Q274 412 262 412 H98 Q86 412 84 400 Z" fill="#5E6B80" />
        {[120, 180, 240].map((x) => <rect key={x} x={x} y="130" width="14" height="240" rx="7" fill="#46526A" />)}
        <path d="M60 100 H300 L292 150 H68 Z" fill="rgba(255,255,255,.08)" />
      </svg>
      {Array.from({ length: 9 }, (_, i) => { const p = pr(d - i * 4, 0, 22); const ox = 60 + (i % 4) * 60; return <div key={i} style={{ position: "absolute", left: ox, top: lerp(-120, 150, eo(p)), width: 36, height: 20, borderRadius: "50%", background: ["#F59E0B", "#BE123C", "#FB923C"][i % 3], opacity: p > 0 && p < 1 ? 1 : 0, transform: `rotate(${i * 50 + p * 300}deg)` }} />; })}
    </div>
  );
};

const SunArc: React.FC = () => {
  const abs = useAbs(); const t = abs / FPS;
  const s = pr(t, 7.44, 10.75), ang = Math.PI * s;
  const x = 320 - 300 * Math.cos(ang), y = 135 - 125 * Math.sin(ang);
  const o = pr(t, 7.3, 7.5) * (1 - pr(t, 9.7, 9.9));
  return (
    <div style={{ position: "absolute", left: 640, top: 70, width: 640, height: 190, opacity: o, transform: "scale(1.3)", transformOrigin: "50% 0" }}>
      <svg width="640" height="190" viewBox="0 0 640 190">
        <defs><radialGradient id="sg"><stop offset="0" stopColor="#FFD36B" stopOpacity=".8" /><stop offset="1" stopColor="#FFD36B" stopOpacity="0" /></radialGradient></defs>
        <path d="M20 135 A300 125 0 0 1 620 135" fill="none" stroke="rgba(246,226,166,.6)" strokeWidth="5" strokeDasharray="3 14" strokeLinecap="round" />
        <line x1="0" y1="135" x2="640" y2="135" stroke="rgba(250,249,245,.4)" strokeWidth="3" />
        <circle cx={x} cy={y} r="56" fill="url(#sg)" /><circle cx={x} cy={y} r="24" fill={s < 0.75 ? "#FFD36B" : "#FF7A3D"} />
      </svg>
      {[["SUBAH 🌅", 0], ["SHAAM 🌇", 1]].map(([l, r]) => <div key={String(l)} style={{ position: "absolute", top: 142, [r ? "right" : "left"]: 0, fontFamily: FONT.sans, fontWeight: 900, fontSize: 26, letterSpacing: 2, padding: "6px 18px", borderRadius: 999, background: "rgba(11,21,38,.8)", border: "2px solid rgba(226,190,106,.7)", color: C.brandSoft }}>{l}</div>)}
    </div>
  );
};

// ---------- scenes ----------
const S1: React.FC = () => {
  const abs = useAbs(); const f = abs;
  const panel = spring({ frame: f + 4, fps: FPS, config: { damping: 18, stiffness: 90 } });
  const kb = lerp(1.12, 1.3, pr(f, 0, 150));
  const EX = F(4.6);
  return (
    <AbsoluteFill>
      <FluidGradientBg variant="custom" customPalette={NAVY} speed={1.4} />
      <div style={{ position: "absolute", left: lerp(2100, 1380, eo(panel)), top: 170, width: 440, height: 800, borderRadius: 40, overflow: "hidden", boxShadow: "0 40px 90px rgba(0,0,0,.65), 0 0 0 3px rgba(226,190,106,.85), 0 0 80px rgba(226,190,106,.25)", transform: "perspective(1400px) rotateY(-8deg)" }}>
        <Img src={staticFile("images/img_temple_sunrise.jpg")} style={{ position: "absolute", height: "100%", left: lerp(-520, -640, pr(f, 0, 150)), transform: `scale(${kb})`, transformOrigin: "60% 50%" }} />
        <div style={{ position: "absolute", inset: 0, background: "linear-gradient(105deg,transparent 35%,rgba(255,255,255,.35) 50%,transparent 65%)", transform: `translateX(${lerp(-500, 500, pr(f, 10, 70))}px)` }} />
        <div style={{ position: "absolute", left: 20, bottom: 24, fontFamily: FONT.sans, fontWeight: 900, fontSize: 28, padding: "8px 20px", borderRadius: 999, background: "rgba(11,21,38,.82)", border: "2px solid rgba(226,190,106,.7)", color: C.brandSoft }}>MANDIR • SUBAH 🌅</div>
      </div>
      <div style={{ position: "absolute", left: 110, top: 250 }}>
        <Row id="A" size={96} exitAt={EX} />
        <Row id="B" size={96} exitAt={EX + 2} style={{ marginTop: 18 }} />
        <Row id="C" size={92} exitAt={EX + 4} style={{ marginTop: 18 }} />
      </div>
      <div style={{ position: "absolute", left: 110, top: 930, width: lerp(0, 760, eo(pr(f, 70, 105))), height: 8, borderRadius: 8, background: `linear-gradient(90deg,${C.teal},${C.brand})`, opacity: 1 - pr(f, EX, EX + 6) }} />
    </AbsoluteFill>
  );
};

const S2: React.FC = () => {
  const abs = useAbs(); const f = abs - F(4.78);
  const dots = Math.floor(pr(f, 12, 30) * 3);
  return (
    <AbsoluteFill>
      <FluidGradientBg variant="custom" customPalette={{ ...NAVY, blob2: "rgba(226,190,106,0.38)" }} speed={2.2} />
      <Vignette a={0.7} />
      <Ring at={4.86} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 330, textAlign: "center" }}>
        <Row id="D" size={300} reserve style={{ justifyContent: "center" }} slam />
      </div>
    </AbsoluteFill>
  );
};

const S3: React.FC = () => {
  const abs = useAbs(); const f = abs - F(5.84);
  const z = lerp(1.12, 1.34, eio(pr(f, 0, 48)));
  const wob = noise2D("w", f * 0.12, 0) * 10;
  const glitch = f < 8 ? 1 : 0;
  const vid = (extra: React.CSSProperties) => <OffthreadVideo src={staticFile("clips/w01_temple_waste.mp4")} startFrom={12} muted style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", ...extra }} />;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ transform: `scale(${z}) translateX(${wob}px)`, filter: "saturate(.75) contrast(1.1)" }}>{vid({})}</AbsoluteFill>
      {glitch ? <><AbsoluteFill style={{ transform: `scale(${z}) translateX(${14 - f * 2}px)`, mixBlendMode: "screen", opacity: 0.55, filter: "sepia(1) saturate(7) hue-rotate(-50deg)" }}>{vid({})}</AbsoluteFill>
        <AbsoluteFill style={{ transform: `scale(${z}) translateX(${-14 + f * 2}px)`, mixBlendMode: "screen", opacity: 0.5, filter: "sepia(1) saturate(7) hue-rotate(150deg)" }}>{vid({})}</AbsoluteFill></> : null}
      <AbsoluteFill style={{ background: "rgba(110,10,0,.34)", mixBlendMode: "multiply" }} />
      <AbsoluteFill style={{ background: "linear-gradient(180deg,rgba(8,14,26,.2) 0%,transparent 35%,rgba(8,14,26,.88) 100%)" }} />
      <Vignette a={0.7} />
      <Ring at={5.91} color="255,107,61" />
      <Bin at={5.9} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 640, textAlign: "center" }}><Row id="E" size={250} style={{ justifyContent: "center" }} slam reserve /></div>
    </AbsoluteFill>
  );
};

const S4: React.FC = () => {
  const abs = useAbs(); const f = abs - F(7.36);
  const z = lerp(1.32, 1.06, eio(pr(f, 0, 80)));
  const leak = pr(f, 0, 12) * (1 - pr(f, 60, 78));
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Img src={staticFile("images/img_puja_cone.jpg")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", transform: `scale(${z}) translate(${lerp(40, -30, pr(f, 0, 80))}px,0)`, filter: "saturate(1.25) brightness(1.08)" }} />
      <AbsoluteFill style={{ background: `radial-gradient(900px 600px at 15% 15%, rgba(255,226,150,${0.7 * leak}), transparent 70%)`, mixBlendMode: "screen" }} />
      <AbsoluteFill style={{ background: "linear-gradient(180deg,rgba(8,14,26,.3),transparent 30%,transparent 55%,rgba(8,14,26,.75))" }} />
      <SunArc />
      <div style={{ position: "absolute", left: 130, right: 130, bottom: 100, height: 240, borderRadius: 40, background: "rgba(11,21,38,.66)", backdropFilter: "blur(26px)", border: "2px solid rgba(226,190,106,.7)", boxShadow: "0 30px 80px rgba(0,0,0,.55), inset 0 2px 1px rgba(255,255,255,.18)", display: "flex", alignItems: "center", justifyContent: "center", transform: `translateY(${(1 - eo(pr(f, 2, 16))) * 120}px)`, opacity: pr(f, 2, 10) }}>
        <Row id="F" size={112} />
      </div>
    </AbsoluteFill>
  );
};

const S5: React.FC = () => {
  const abs = useAbs(); const f = abs - F(9.84);
  const sink = eio(pr(f, 0, 36));
  return (
    <AbsoluteFill>
      <FluidGradientBg variant="custom" customPalette={DUSK} speed={1.6} />
      <div style={{ position: "absolute", left: 960 - 280, top: lerp(430, 690, sink), width: 560, height: 560, borderRadius: "50%", background: "radial-gradient(circle at 40% 35%,#FFE3A0,#FF9A4D 55%,#E2553A)", boxShadow: "0 0 160px rgba(255,150,80,.7)" }} />
      <svg style={{ position: "absolute", left: 0, top: 0 }} width="1920" height="1080" viewBox="0 0 1920 1080">
        <path d="M0 1080 V860 H760 L790 760 L840 740 L870 640 L900 600 L930 520 L960 420 L990 520 L1020 600 L1050 640 L1080 740 L1130 760 L1160 860 H1920 V1080 Z" fill="#0B1526" />
        {[[260, 120], [700, 80], [1500, 150], [1750, 90], [1200, 60]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r="4" fill="#F6E2A6" opacity={pr(f, 14, 30) * (0.5 + 0.5 * Math.sin(f * 0.4 + i))} />)}
      </svg>
      <AbsoluteFill style={{ background: "radial-gradient(900px 400px at 50% 25%, rgba(8,14,26,.5), transparent 70%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, textAlign: "center" }}><Row id="G" size={210} style={{ justifyContent: "center" }} /></div>
    </AbsoluteFill>
  );
};

const S6: React.FC = () => {
  const abs = useAbs(); const f = abs - F(11.0);
  const hit = abs - F(13.14);
  const z = lerp(1.05, 1.32, eio(pr(f, 0, 100))) + (hit >= 0 ? Math.max(0, 0.08 * (1 - hit / 10)) : 0);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ transform: `scale(${z})`, filter: `saturate(${lerp(1, 0.7, pr(f, 20, 80))}) brightness(${lerp(0.9, 0.6, pr(f, 20, 90))})` }}>
        <OffthreadVideo src={staticFile("clips/w01b_flowers_dumped.mp4")} startFrom={F(1.0)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "rgba(25,40,100,.3)", mixBlendMode: "multiply" }} />
      <AbsoluteFill style={{ background: "radial-gradient(1000px 520px at 50% 50%, rgba(8,14,26,.75), transparent 75%)" }} />
      <Vignette a={0.75} />
      <Ring at={11.11} /><Ring at={11.62} /><Ring at={13.14} color="255,107,61" max={1700} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 380, textAlign: "center" }}><Row id="H" size={290} style={{ justifyContent: "center" }} reserve slam /></div>
      {hit >= 0 && hit < 30 ? Array.from({ length: 26 }, (_, i) => { const r = (k: number) => Math.abs((Math.sin(i * k) * 9876.5) % 1); const k = hit / 30; return <div key={i} style={{ position: "absolute", left: 960 + (r(3.3) - 0.5) * 1500 * eo(k), top: 540 + (r(7.7) - 0.5) * 700 * eo(k) - 80 * k, width: 10 + r(1.9) * 22, height: 10 + r(1.9) * 22, borderRadius: "50%", background: "rgba(246,226,166,.7)", opacity: 0.8 * (1 - k), filter: "blur(2px)" }} />; }) : null}
    </AbsoluteFill>
  );
};

const S7: React.FC = () => {
  const abs = useAbs(); const f = abs - F(14.3);
  const sp = spring({ frame: f, fps: FPS, config: { damping: 14, stiffness: 140 } });
  return (
    <AbsoluteFill>
      <FluidGradientBg variant="custom" customPalette={NAVY} speed={2} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 20 }}>
        <Img src={staticFile("images/logo.png")} style={{ width: 200, height: 200, borderRadius: "50%", transform: `scale(${sp}) rotate(${lerp(-90, 0, sp)}deg)`, boxShadow: "0 0 0 5px #E2BE6A, 0 0 70px rgba(226,190,106,.55)" }} />
        <div style={{ fontFamily: FONT.display, fontSize: 170, textTransform: "uppercase", background: BRAND_GRADIENT, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", filter: "drop-shadow(0 7px 0 rgba(0,0,0,.6))", transform: `scale(${lerp(1.6, 1, eo(pr(f, 2, 12)))})`, opacity: pr(f, 2, 8) }}>LEKIN SOCHIYE...</div>
        <div style={{ fontFamily: FONT.sans, fontWeight: 900, fontSize: 46, color: C.ink, opacity: pr(f, 8, 16) }}>ideaspulse<span style={{ color: C.brand }}>.in</span></div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- root ----------
const useFonts = () => {
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => {
    const defs: [string, string, string][] = [["Anton", "fonts/Anton-Regular.ttf", "400"], ["Poppins", "fonts/Poppins-ExtraBold.ttf", "800"], ["Poppins", "fonts/Poppins-Black.ttf", "900"]];
    Promise.all(defs.map(([n, u, w]) => new FontFace(n, `url(${staticFile(u)})`, { weight: w }).load())).then((fs) => { fs.forEach((x) => (document.fonts as any).add(x)); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
};
export const Sample15: React.FC = () => {
  useFonts();
  const f = useCurrentFrame(); const t = f / FPS;
  let sx = 0, sy = 0, flash = 0;
  for (const [ti, amp, dur] of IMPACTS) { const d = t - ti; if (d >= 0 && d < dur) { const k = 1 - d / dur; sx += Math.sin(d * 95) * amp * k; sy += Math.cos(d * 80) * amp * 0.7 * k; flash = Math.max(flash, k * (amp > 15 ? 0.6 : 0.25)); } }
  let punch = 0; for (const u of U) { const d = f - F(u.t0); if (d >= 0 && d < 6) punch = Math.max(punch, (1 - d / 6) * (u.style === "r" || u.style === "s" ? 0.05 : 0.02)); }
  const logoO = 1 - pr(f, F(14.2), F(14.4));
  return (
    <AbsoluteFill style={{ background: C.bg2 }}>
      <AbsoluteFill style={{ transform: `translate(${sx}px,${sy}px) scale(${1 + punch})` }}>
        <Scene from={0} dur={F(4.86) + 4} first><S1 /></Scene>
        <Scene from={F(4.78)} dur={F(5.84) - F(4.78) + 5}><S2 /></Scene>
        <Scene from={F(5.84)} dur={F(7.36) - F(5.84) + 5}><S3 /></Scene>
        <Scene from={F(7.36)} dur={F(9.84) - F(7.36) + 5}><S4 /></Scene>
        <Scene from={F(9.84)} dur={F(11.0) - F(9.84) + 5}><S5 /></Scene>
        <Scene from={F(11.0)} dur={F(14.3) - F(11.0) + 5}><S6 /></Scene>
        <Scene from={F(14.3)} dur={450 - F(14.3)}><S7 /></Scene>
        <Petals />
        <Img src={staticFile("images/logo.png")} style={{ position: "absolute", right: 70, top: 56, width: 92, height: 92, borderRadius: "50%", boxShadow: "0 0 0 3px #E2BE6A, 0 8px 24px rgba(0,0,0,.5)", opacity: logoO }} />
        <div style={{ position: "absolute", right: 178, top: 86, fontFamily: FONT.sans, fontWeight: 900, fontSize: 28, color: C.ink, textShadow: "0 2px 8px rgba(0,0,0,.8)", opacity: logoO }}>ideaspulse<span style={{ color: C.brand }}>.in</span></div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "#fff2d8", opacity: flash, pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
