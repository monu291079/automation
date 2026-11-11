import React from "react";
import { AbsoluteFill, Freeze, Img, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import words from "./words.json";
import TL from "./timeline.json";

/**
 * "Balloon arch business" reel, 1080x1920. RULES: the picture never zooms/shakes (timelapse footage moves by itself);
 * only the glass widgets, captions and balloons move. Safe zones: widgets in y 170-520 (above the head), captions in
 * y 1130-1440 (on the chest), nothing in the bottom 280 px (Instagram UI) except the end card.
 */
const FPS = 30, F = (s: number) => Math.round(s * FPS);
const lerp = (a: number, b: number, x: number) => a + (b - a) * x;
const pr = (f: number, a: number, b: number) => Math.min(1, Math.max(0, (f - a) / (b - a)));
const eo = (x: number) => 1 - Math.pow(1 - x, 3);
const eio = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const SP = { snappy: { damping: 15, stiffness: 160 }, soft: { damping: 20, stiffness: 90 }, bouncy: { damping: 9, stiffness: 180 }, slam: { damping: 11, stiffness: 230 } };
const CH: Record<string, any> = Object.fromEntries((words as any).chunks.map((c: any) => [c.id, c]));
const T0 = (id: string) => CH[id].t0, T1 = (id: string) => CH[id].t1;
const VOICE_END: number = (TL as any).voice_end, DURATION: number = (TL as any).duration;
const C = { navy: "#12213A", navy2: "#0B1526", gold: "#E2BE6A", goldL: "#F6E2A6", goldD: "#A9812E", cream: "#FAF9F5", teal: "#218C87", tealL: "#39C2BA", red: "#FF5A2C" };
const GOLD: React.CSSProperties = { background: "linear-gradient(180deg,#F6E2A6 0%,#E2BE6A 48%,#A9812E 100%)", WebkitBackgroundClip: "text", backgroundClip: "text", WebkitTextFillColor: "transparent", filter: "drop-shadow(0 4px 0 rgba(0,0,0,.85)) drop-shadow(0 0 12px rgba(0,0,0,.85)) drop-shadow(0 0 3px rgba(0,0,0,.9))" };
const FONT = { display: "Anton, 'Noto Color Emoji', sans-serif", sans: "Poppins, 'Noto Color Emoji', sans-serif" };
const EMO = /(\p{Extended_Pictographic}[\u{FE0F}\u{200D}\p{Extended_Pictographic}]*|[\u{1F1E6}-\u{1F1FF}]{2}|[0-9#*]\u{FE0F}?\u{20E3})/gu;
const gt = (s: string): React.ReactNode[] => String(s).split(EMO).map((p, i) => (i % 2 ? <span key={i} style={{ WebkitTextFillColor: "#fff", color: "#fff", background: "none", filter: "none", textShadow: "none", WebkitTextStroke: 0 }}>{p}</span> : p));
const TX = (s: React.CSSProperties = {}): React.CSSProperties => ({ fontFamily: FONT.sans, fontWeight: 800, color: "#fff", textShadow: "0 3px 12px rgba(0,0,0,.45)", ...s });

const useFonts = () => {
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => {
    const defs: [string, string, string][] = [["Anton", "fonts/Anton-Regular.ttf", "400"], ["Poppins", "fonts/Poppins-ExtraBold.ttf", "800"], ["Poppins", "fonts/Poppins-Black.ttf", "900"]];
    Promise.all(defs.map(([n, u, w]) => new FontFace(n, `url(${staticFile(u)})`, { weight: w }).load())).then((fs) => { fs.forEach((x) => (document.fonts as any).add(x)); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
};
const sp = (f: number, at: number, cfg = SP.snappy) => spring({ frame: Math.max(0, f - F(at)), fps: FPS, config: cfg });
const vis = (t: number, a: number, b: number) => t >= a - 0.05 && t < b + 0.45;

// ------------------------------------------------------------------ glass
const Glass: React.FC<{ style?: React.CSSProperties; children?: React.ReactNode; tint?: string; shineAt?: number; rim?: string; radius?: number }> = ({ style, children, tint, shineAt, rim, radius = 40 }) => {
  const f = useCurrentFrame(); const sh = shineAt === undefined ? 0 : pr(f, F(shineAt) + 3, F(shineAt) + 30);
  return (
    <div style={{ position: "absolute", borderRadius: radius, overflow: "hidden", background: `linear-gradient(150deg, ${tint ?? "rgba(255,255,255,.26)"} 0%, rgba(255,255,255,.05) 48%, rgba(255,255,255,.12) 100%), rgba(10,20,40,.58)`, backdropFilter: "blur(30px) saturate(185%) brightness(1.08)", border: `1.5px solid ${rim ?? "rgba(255,255,255,.42)"}`, boxShadow: "0 36px 80px rgba(0,0,0,.5), 0 6px 18px rgba(0,0,0,.28), inset 0 2px 1px rgba(255,255,255,.7), inset 0 -2px 10px rgba(255,255,255,.08), inset 0 0 40px rgba(255,255,255,.05)", ...style }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(120% 70% at 18% -10%, rgba(255,255,255,.38), transparent 55%)", pointerEvents: "none" }} />
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: "30%", background: "linear-gradient(0deg, rgba(255,255,255,.08), transparent)", pointerEvents: "none" }} />
      {sh > 0 && sh < 1 ? <div style={{ position: "absolute", top: -20, bottom: -20, width: "24%", left: `${lerp(-30, 125, eio(sh))}%`, background: "linear-gradient(100deg,transparent,rgba(255,255,255,.5),transparent)", transform: "skewX(-18deg)", pointerEvents: "none" }} /> : null}
      {children}
    </div>
  );
};
// enter: drop / slide / pop, exit: lifts away
const Mount: React.FC<{ a: number; b: number; from?: "T" | "L" | "R" | "B" | "Z"; x?: number; y: number; w: number; h: number; children: React.ReactNode; cfg?: any }> = ({ a, b, from = "T", x = 540, y, w, h, children, cfg }) => {
  const f = useCurrentFrame(); const t = f / FPS; if (!vis(t, a, b)) return null;
  const s = sp(f, a, cfg ?? SP.bouncy), k = 1 - s, o = pr(f, F(b), F(b) + 11), e = eio(o);
  const enter = from === "T" ? `translateY(${k * -520}px)` : from === "L" ? `translateX(${k * -1200}px)` : from === "R" ? `translateX(${k * 1200}px)` : from === "B" ? `translateY(${k * 700}px)` : `scale(${lerp(0.4, 1, s)}) rotate(${k * -8}deg)`;
  return <div style={{ position: "absolute", left: x - w / 2, top: y, width: w, height: h, opacity: Math.min(1, s * 3) * (1 - o), transform: `${enter} translateY(${-e * 360}px)`, filter: o ? `blur(${o * 8}px)` : undefined }}>{children}</div>;
};

// ------------------------------------------------------------------ glossy balloons + confetti
const mix = (hex: string, to: number, k: number) => { const n = parseInt(hex.slice(1), 16); const c = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => Math.round(lerp(v, to, k))); return `rgb(${c[0]},${c[1]},${c[2]})`; };
const BAL = ["#E2BE6A", "#39C2BA", "#FF6B5A", "#F4F1EA", "#4C8DFF", "#E5484D", "#9B6BFF"];
const Balloon: React.FC<{ color: string; size: number; x: number; y: number; rot?: number; blur?: number; o?: number; s?: number }> = ({ color, size, x, y, rot = 0, blur = 0, o = 1, s = 1 }) => {
  const id = "bg" + color.slice(1);
  return (
    <svg width={size * s} height={size * 1.55 * s} viewBox="0 0 100 155" style={{ position: "absolute", left: x - (size * s) / 2, top: y, transform: `rotate(${rot}deg)`, transformOrigin: "50% 80%", opacity: o, filter: blur ? `blur(${blur}px) drop-shadow(0 14px 18px rgba(0,0,0,.35))` : "drop-shadow(0 14px 18px rgba(0,0,0,.35))" }}>
      <defs><radialGradient id={id} cx="35%" cy="28%" r="80%"><stop offset="0" stopColor={mix(color, 255, 0.55)} /><stop offset="0.4" stopColor={color} /><stop offset="1" stopColor={mix(color, 0, 0.5)} /></radialGradient></defs>
      <path d="M50 4 C 86 4, 99 38, 92 68 C 86 98, 62 118, 50 124 C 38 118, 14 98, 8 68 C 1 38, 14 4, 50 4 Z" fill={`url(#${id})`} />
      <path d="M43 123 L57 123 L50 134 Z" fill={mix(color, 0, 0.45)} />
      <ellipse cx="32" cy="34" rx="10" ry="19" fill="rgba(255,255,255,.62)" transform="rotate(-24 32 34)" />
      <ellipse cx="70" cy="92" rx="14" ry="6" fill="rgba(255,255,255,.12)" transform="rotate(-35 70 92)" />
      <path d="M50 134 C 38 146, 62 150, 50 155" stroke="rgba(255,255,255,.7)" fill="none" strokeWidth="1.6" />
    </svg>
  );
};
const Rising: React.FC<{ a: number; b: number; n?: number; seed?: number }> = ({ a, b, n = 9, seed = 1 }) => {
  const f = useCurrentFrame(); const t = f / FPS; if (t < a || t > b + 0.4) return null;
  const fadeO = pr(t, a, a + 0.3) * (1 - pr(t, b - 0.4, b));
  return (
    <AbsoluteFill style={{ pointerEvents: "none", opacity: fadeO }}>
      {Array.from({ length: n }, (_, i) => {
        const r = (k: number) => Math.abs((Math.sin((i + seed) * k) * 43758.5453) % 1);
        const size = 80 + r(3.1) * 150, speed = 380 + r(5.7) * 520, x0 = [110, 960, 220, 860, 540, 70, 1000, 330, 760][i % 9] + (r(2.3) - 0.5) * 120;
        const y = 2050 - ((t - a) * speed + r(9.1) * 600) , sway = Math.sin(t * (1.1 + r(1.9)) + i) * 26;
        return <Balloon key={i} color={BAL[(i + seed) % BAL.length]} size={size} x={x0 + sway} y={y} rot={Math.sin(t * 1.3 + i) * 9} blur={size > 190 ? 5 : size < 100 ? 2 : 0} />;
      })}
    </AbsoluteFill>
  );
};
const Confetti: React.FC<{ at: number; x?: number; y?: number; n?: number }> = ({ at, x = 540, y = 760, n = 46 }) => {
  const f = useCurrentFrame(); const d = (f - F(at)) / FPS; if (d < 0 || d > 1.6) return null;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {Array.from({ length: n }, (_, i) => {
        const r = (k: number) => Math.abs((Math.sin((i + 3) * k) * 9876.543) % 1); const ang = r(2.1) * Math.PI * 2, v = 380 + r(4.3) * 620;
        const px = x + Math.cos(ang) * v * d, py = y + Math.sin(ang) * v * d * 0.8 + 900 * d * d;
        return <div key={i} style={{ position: "absolute", left: px, top: py, width: 14 + r(1.7) * 14, height: 8 + r(6.1) * 10, background: BAL[i % BAL.length], opacity: 1 - pr(d, 1.0, 1.6), transform: `rotate(${r(5) * 360 + d * 700}deg)` }} />;
      })}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------ picture
const Clip: React.FC<{ cut: any }> = ({ cut }) => {
  const f = useCurrentFrame(); const dur = ((TL as any).clipdur?.[cut.clip] ?? 99) * FPS - 2;
  const isC = cut.clip === "creator";
  return (
    <Freeze frame={Math.min(f, Math.floor(dur))}>
      <OffthreadVideo src={staticFile(`clips/${cut.clip}.mp4`)} startFrom={isC ? F(cut.t0) : 0} muted style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
    </Freeze>
  );
};
const Picture: React.FC = () => (
  <AbsoluteFill style={{ background: C.navy2 }}>
    {(TL as any).cuts.map((c: any, i: number) => <Sequence key={i} from={F(c.t0)} durationInFrames={F(c.t1) - F(c.t0)}><Clip cut={c} /></Sequence>)}
    {/* the timelapse shots get a light grade so the glass reads; creator shots are left untouched */}
    <Shade />
  </AbsoluteFill>
);
const Shade: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  const onCreator = (TL as any).cuts.some((c: any) => c.clip === "creator" && t >= c.t0 && t < c.t1);
  return <AbsoluteFill style={{ background: onCreator ? "linear-gradient(180deg,rgba(8,14,26,.55) 0%,rgba(8,14,26,0) 30%,rgba(8,14,26,0) 45%,rgba(8,14,26,.62) 78%,rgba(8,14,26,.7) 100%)" : "linear-gradient(180deg,rgba(8,14,26,.62) 0%,rgba(8,14,26,.12) 32%,rgba(8,14,26,.1) 55%,rgba(8,14,26,.7) 100%)" }} />;
};
const CutFlash: React.FC = () => {
  const f = useCurrentFrame(); let o = 0;
  for (const c of (TL as any).cuts.slice(1)) { const d = f - F(c.t0); if (d >= 0 && d < 5) o = Math.max(o, 0.42 * (1 - d / 5)); }
  return <AbsoluteFill style={{ background: "#fff6df", opacity: o, mixBlendMode: "screen", pointerEvents: "none" }} />;
};

// ------------------------------------------------------------------ captions (phrase by phrase, on the chest zone)
const Caption: React.FC<{ c: any }> = ({ c }) => {
  const f = useCurrentFrame(); const t = f / FPS; if (!c.text || t < c.t0 - 0.04 || t > c.t1 + 0.14) return null;
  const gold = c.style === "g"; const s = sp(f, c.t0 - 0.02, gold ? SP.slam : SP.snappy), x = pr(f, F(c.t1) - 1, F(c.t1) + 4);
  const size = gold ? 124 : 106;
  return (
    <div style={{ position: "absolute", left: 100, width: 880, bottom: 480, textAlign: "center", fontFamily: FONT.display, fontSize: size, lineHeight: 1.06, textTransform: "uppercase", letterSpacing: 2, opacity: Math.min(1, s * 3) * (1 - x), transform: gold ? `scale(${lerp(1.9, 1, s)}) rotate(${(1 - s) * -3}deg)` : `translateY(${(1 - s) * 60}px) scale(${lerp(0.8, 1, s)})`, filter: `blur(${(1 - s) * (gold ? 12 : 7)}px)`, ...(gold ? GOLD : { color: "#fff", textShadow: "0 7px 0 rgba(0,0,0,.65), 0 0 34px rgba(0,0,0,.6)", WebkitTextStroke: "2px rgba(5,10,20,.55)" }) }}>{gt(c.text)}</div>
  );
};
const Captions: React.FC = () => <>{(words as any).chunks.map((c: any) => <Caption key={c.id} c={c} />)}</>;

// ------------------------------------------------------------------ widgets
const HookCard: React.FC = () => (
  <Mount a={0.1} b={3.7} y={190} w={900} h={236}>
    <Glass style={{ inset: 0 }} shineAt={0.3} rim="rgba(226,190,106,.8)">
      <div style={{ position: "absolute", left: 0, right: 0, top: 26, textAlign: "center", ...TX({ fontSize: 34, letterSpacing: 6, color: C.tealL }) }}>NAYA BUSINESS IDEA 💡</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 80, textAlign: "center", fontFamily: FONT.display, fontSize: 108, letterSpacing: 1, textTransform: "uppercase", ...GOLD }}>BALLOON ARCH 🎈</div>
    </Glass>
  </Mount>
);
const SpeedPill: React.FC = () => {
  const f = useCurrentFrame(); const t = f / FPS; const cuts = (TL as any).cuts.filter((c: any) => c.speed);
  const cur = cuts.find((c: any) => t >= c.t0 && t < c.t1); if (!cur) return t > 6.55 && t < 7 ? null : null;
  const d = f - F(cur.t0), flip = pr(d, 0, 6);
  return (
    <Mount a={0.2} b={6.5} from="L" x={300} y={462} w={420} h={96}>
      <Glass style={{ inset: 0 }} radius={48}>
        <div style={{ position: "absolute", left: 28, top: 0, bottom: 0, display: "flex", alignItems: "center", gap: 14 }}>
          <div style={{ width: 18, height: 18, borderRadius: 9, background: C.red, boxShadow: `0 0 ${10 + 8 * Math.sin(f / 4)}px ${C.red}` }} />
          <div style={TX({ fontSize: 30, letterSpacing: 2 })}>TIMELAPSE ▶▶</div>
          <div style={{ fontFamily: FONT.display, fontSize: 48, color: C.goldL, transform: `translateY(${(1 - eo(flip)) * 30}px)`, opacity: flip, minWidth: 90 }}>{cur.speed}</div>
        </div>
      </Glass>
    </Mount>
  );
};
const IndiaCard: React.FC = () => (
  <Mount a={6.6} b={8.88} y={200} w={920} h={250}>
    <Glass style={{ inset: 0 }} shineAt={6.7} rim="rgba(255,255,255,.5)">
      <div style={{ position: "absolute", left: 0, right: 0, top: 22, textAlign: "center", ...TX({ fontSize: 34, letterSpacing: 5, color: C.tealL }) }}>🇮🇳 AB BHARAT MEIN BHI</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 78, textAlign: "center", fontFamily: FONT.display, fontSize: 104, textTransform: "uppercase", ...GOLD }}>KAMAI KA MAUKA</div>
      <div style={{ position: "absolute", left: 60, right: 60, bottom: 26, height: 10, borderRadius: 5, background: "linear-gradient(90deg,#FF9933 0 33%,#fff 33% 66%,#138808 66%)", opacity: 0.9, transformOrigin: "0 50%" }} />
    </Glass>
  </Mount>
);
const Toggle: React.FC = () => {
  const f = useCurrentFrame(); const on = sp(f, T1("c7") - 0.25, { damping: 14, stiffness: 220 }); const r = pr(f, F(T1("c7") - 0.25), F(T1("c7") - 0.25) + 20);
  return (
    <Mount a={8.95} b={13.55} y={190} w={920} h={250}>
      <Glass style={{ inset: 0 }} shineAt={9.05} tint={`rgba(${Math.round(lerp(255, 80, on))},255,${Math.round(lerp(255, 140, on))},.18)`}>
        <div style={TX({ position: "absolute", left: 50, top: 46, fontSize: 40 })}>🎈 BALLOON MACHINE</div>
        <div style={TX({ position: "absolute", left: 50, top: 112, fontSize: 30, fontWeight: 700, color: "#CFE9E6" })}>sirf ek button dabaiye</div>
        <div style={TX({ position: "absolute", left: 50, top: 170, fontSize: 28, fontWeight: 800, color: on > 0.5 ? "#7DFFB0" : "#9AA6B8", letterSpacing: 3 })}>{on > 0.5 ? "● ON — PUMP CHAL RAHA HAI" : "○ OFF"}</div>
        <div style={{ position: "absolute", right: 50, top: 70, width: 220, height: 118, borderRadius: 59, background: `linear-gradient(180deg, rgb(${Math.round(lerp(120, 52, on))},${Math.round(lerp(128, 199, on))},${Math.round(lerp(140, 89, on))}), rgb(${Math.round(lerp(90, 40, on))},${Math.round(lerp(98, 170, on))},${Math.round(lerp(110, 70, on))}))`, boxShadow: `inset 0 4px 10px rgba(0,0,0,.35), 0 0 ${on * 40}px rgba(52,199,89,${on * 0.7})` }}>
          <div style={{ position: "absolute", top: 7, left: 7 + on * 102, width: 104, height: 104, borderRadius: 52, background: "linear-gradient(180deg,#fff,#E6E8EC)", boxShadow: "0 6px 14px rgba(0,0,0,.4), inset 0 -3px 6px rgba(0,0,0,.12)" }} />
        </div>
        {r > 0 && r < 1 ? <div style={{ position: "absolute", right: 160 - 120 * r, top: 129 - 120 * r, width: 240 * r, height: 240 * r, borderRadius: "50%", border: `4px solid rgba(125,255,176,${0.8 * (1 - r)})` }} /> : null}
      </Glass>
    </Mount>
  );
};
const InflateStrip: React.FC = () => {
  const f = useCurrentFrame(); const a = T0("c9");
  return (
    <Mount a={a - 0.3} b={13.55} from="B" y={470} w={760} h={190}>
      <Glass style={{ inset: 0 }} radius={95}>
        <div style={TX({ position: "absolute", left: 0, right: 0, bottom: 14, textAlign: "center", fontSize: 26, letterSpacing: 4, color: C.goldL })}>EK SAATH PHOOLTE HAIN</div>
        {Array.from({ length: 6 }, (_, i) => { const s = spring({ frame: Math.max(0, f - F(a + i * 0.14)), fps: FPS, config: SP.bouncy }); return <Balloon key={i} color={BAL[i % BAL.length]} size={74} x={95 + i * 114} y={8 + (1 - s) * 40} s={s * (1 + 0.04 * Math.sin(f / 5 + i))} />; })}
      </Glass>
    </Mount>
  );
};
const Steps: React.FC = () => {
  const f = useCurrentFrame();
  const rows = [{ at: T0("c11"), ic: "🔌", t: "PUMP CONNECT KARO" }, { at: T0("c12"), ic: "🎈", t: "BALLOONS LAGAO" }, { at: T0("c13"), ic: "🏁", t: "ARCH TAIYAR" }];
  const done = sp(f, T0("c14"), SP.bouncy);
  return (
    <>
      <Mount a={13.72} b={18.7} from="L" y={180} w={930} h={470}>
        <Glass style={{ inset: 0 }} shineAt={13.8}>
          <div style={TX({ position: "absolute", left: 44, top: 28, fontSize: 30, letterSpacing: 6, color: C.tealL })}>3 AASAAN STEPS</div>
          <div style={{ position: "absolute", right: 44, top: 36, display: "flex", gap: 10 }}>{[0, 1, 2].map((i) => <i key={i} style={{ width: 18, height: 18, borderRadius: 9, background: f >= F(rows[i].at) ? C.gold : "rgba(255,255,255,.22)", boxShadow: f >= F(rows[i].at) ? `0 0 12px ${C.gold}` : "none", display: "inline-block" }} />)}</div>
          {rows.map((r, i) => { const s = spring({ frame: Math.max(0, f - F(r.at)), fps: FPS, config: SP.snappy }); const last = i === 2; return (
            <div key={i} style={{ position: "absolute", left: 36, right: 36, top: 92 + i * 120, height: 104, borderRadius: 26, background: last && done > 0.5 ? "linear-gradient(90deg,rgba(33,140,135,.7),rgba(33,140,135,.25))" : "rgba(255,255,255,.09)", borderLeft: `8px solid ${last ? C.tealL : C.gold}`, display: "flex", alignItems: "center", gap: 22, padding: "0 28px", opacity: Math.min(1, s * 3), transform: `translateX(${(1 - s) * (i % 2 ? 200 : -200)}px)` }}>
              <div style={{ fontSize: 56 }}>{last && done > 0.5 ? "✅" : r.ic}</div>
              <div style={TX({ fontSize: 44, flex: 1 })}>{last && done > 0.5 ? "ARCH TAIYAR!" : r.t}</div>
              <div style={{ fontFamily: FONT.display, fontSize: 50, color: C.goldL, opacity: 0.9 }}>{i + 1}</div>
            </div>); })}
        </Glass>
      </Mount>
    </>
  );
};
const Chips: React.FC = () => {
  const f = useCurrentFrame(); const a = T0("c15");
  const items = [["🎂", "BIRTHDAY"], ["💍", "WEDDING"], ["🍼", "BABY SHOWER"]];
  const out = pr(f, F(20.38), F(20.38) + 10);
  return (
    <>
      {items.map(([ic, tx], i) => { const t = a + i * 0.26; if (!vis(f / FPS, t, 20.38)) return null; const s = spring({ frame: Math.max(0, f - F(t)), fps: FPS, config: SP.bouncy }); const w = i === 2 ? 390 : 300;
        const left = [70, 70 + 300 + 14, 70 + 300 + 14 + 300 + 14][i];
        return <div key={i} style={{ position: "absolute", left, top: 210 + (1 - s) * -420 - out * 300, width: w, height: 150, opacity: Math.min(1, s * 3) * (1 - out) }}>
          <Glass style={{ inset: 0 }} radius={36} shineAt={t}><div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 4 }}><div style={{ fontSize: 58 }}>{ic}</div><div style={TX({ fontSize: 28, letterSpacing: 2 })}>{tx}</div></div></Glass>
        </div>; })}
    </>
  );
};
const Price: React.FC = () => {
  const f = useCurrentFrame(); const a = T0("c16");
  const up = eo(pr(f, F(a), F(a) + 20)), val = Math.round(lerp(2000, 10000, up)), plus = sp(f, T0("c17"), SP.slam);
  const slide = eio(pr(f, F(T0("c18")), F(VOICE_END - 10.4 + 0.0 + 0.0) > 0 ? F(T0("c18")) + 28 : 0));
  return (
    <Mount a={a} b={29.9} y={160} w={940} h={360}>
      <Glass style={{ inset: 0 }} shineAt={a + 0.05} tint="rgba(255,235,170,.28)" rim="rgba(226,190,106,.85)">
        <div style={TX({ position: "absolute", left: 0, right: 0, top: 22, textAlign: "center", fontSize: 30, letterSpacing: 6, color: C.tealL })}>EK ARCH KE</div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 62, textAlign: "center", fontFamily: FONT.display, fontSize: 112, lineHeight: 1.05, textTransform: "uppercase", ...GOLD }}>₹2,000 – ₹{val.toLocaleString("en-IN")}<span style={{ display: "inline-block", opacity: plus, transform: `scale(${lerp(2.2, 1, plus)})` }}>+</span></div>
        <div style={{ position: "absolute", left: 60, right: 60, top: 230, height: 14, borderRadius: 7, background: "rgba(255,255,255,.18)" }}>
          <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: `${slide * 100}%`, borderRadius: 7, background: `linear-gradient(90deg,${C.teal},${C.gold})` }} />
          <div style={{ position: "absolute", top: -17, left: `calc(${slide * 100}% - 24px)`, width: 48, height: 48, borderRadius: 24, background: "linear-gradient(180deg,#fff,#DDE1E8)", boxShadow: "0 6px 14px rgba(0,0,0,.45)", opacity: pr(f, F(T0("c18")) - 3, F(T0("c18")) + 3) }} />
        </div>
        <div style={TX({ position: "absolute", left: 60, top: 280, fontSize: 28, color: "#CFE9E6" })}>SIMPLE ARCH</div>
        <div style={TX({ position: "absolute", right: 60, top: 280, fontSize: 28, color: C.goldL })}>PREMIUM DESIGN</div>
      </Glass>
    </Mount>
  );
};
const Calc: React.FC = () => {
  const f = useCurrentFrame(); const a = 23.56, ev = sp(f, T0("c20"), SP.bouncy), res = sp(f, T0("c21"), SP.slam);
  const n = Math.round(10 * eo(pr(f, F(T0("c20")), F(T0("c20")) + 14)));
  const lo = Math.round(20000 * eo(pr(f, F(T0("c21")), F(T0("c21")) + 22))), hi = Math.round(100000 * eo(pr(f, F(T0("c21")), F(T0("c21")) + 22)));
  return (
    <Mount a={a} b={27.6} y={165} w={940} h={385}>
      <Glass style={{ inset: 0 }} shineAt={a + 0.05}>
        <div style={TX({ position: "absolute", left: 44, top: 24, fontSize: 30, letterSpacing: 5, color: C.tealL })}>🧮 MAHINE KA HISAAB</div>
        <div style={{ position: "absolute", left: 44, top: 78, display: "flex", alignItems: "baseline", gap: 18, opacity: Math.min(1, ev * 3), transform: `translateY(${(1 - ev) * 40}px)` }}>
          <div style={{ fontFamily: FONT.display, fontSize: 92, color: "#fff" }}>{n}</div><div style={TX({ fontSize: 40 })}>EVENTS / MAHINA</div>
          <div style={TX({ fontSize: 40, color: C.goldL })}>× ₹2K–10K</div>
        </div>
        <div style={{ position: "absolute", left: 44, right: 44, top: 196, height: 3, background: "rgba(255,255,255,.25)" }} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 206, textAlign: "center", fontFamily: FONT.display, fontSize: 88, textTransform: "uppercase", opacity: Math.min(1, res * 3), transform: `scale(${lerp(1.5, 1, res)})`, ...GOLD }}>₹{lo.toLocaleString("en-IN")} – ₹{hi.toLocaleString("en-IN")}+ ?</div>
        <div style={TX({ position: "absolute", left: 0, right: 0, bottom: 14, textAlign: "center", fontSize: 24, fontWeight: 700, color: "#BFC8D6", opacity: pr(f, F(T0("c21")) + 12, F(T0("c21")) + 22) })}>*bikri (kharch alag) • sirf udaharan, guarantee nahi</div>
      </Glass>
    </Mount>
  );
};
const Checks: React.FC = () => {
  const f = useCurrentFrame(); const a = 27.9;
  const rows = [["MACHINE", T1("c22") - 0.15], ["INVESTMENT", T0("c23") + 0.5], ["PROFIT", T1("c23") - 0.1]] as [string, number][];
  return (
    <Mount a={a} b={32.35} y={170} w={940} h={350}>
      <Glass style={{ inset: 0 }} shineAt={a + 0.1}>
        <div style={TX({ position: "absolute", left: 44, top: 26, fontSize: 30, letterSpacing: 5, color: C.tealL })}>POORA HISAAB CHAHIYE?</div>
        {rows.map(([label, at], i) => { const s = spring({ frame: Math.max(0, f - F(at)), fps: FPS, config: SP.bouncy }); const rs = sp(f, a + 0.15 + i * 0.12, SP.snappy);
          return <div key={i} style={{ position: "absolute", left: 36, right: 36, top: 80 + i * 86, height: 74, borderRadius: 22, background: "rgba(255,255,255,.09)", borderLeft: `8px solid ${C.gold}`, display: "flex", alignItems: "center", padding: "0 26px", opacity: Math.min(1, rs * 3), transform: `translateX(${(1 - rs) * 160}px)` }}>
            <div style={TX({ fontSize: 40, flex: 1 })}>{label}</div>
            <div style={{ width: 54, height: 54, borderRadius: 27, background: s > 0.1 ? "linear-gradient(180deg,#46E08C,#1FAF66)" : "rgba(255,255,255,.2)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 34, color: "#fff", transform: `scale(${lerp(0.5, 1, s)})`, boxShadow: s > 0.1 ? "0 0 22px rgba(70,224,140,.7)" : "none" }}>{s > 0.1 ? "✓" : ""}</div>
          </div>; })}
      </Glass>
    </Mount>
  );
};
const CommentBox: React.FC = () => {
  const f = useCurrentFrame(); const a = 32.4, st = T0("c25") + 0.34; const n = Math.floor(pr(f, F(st), F(st) + 12) * 7); const send = sp(f, VOICE_END - 0.1, SP.bouncy);
  const txt = "BALLOON".slice(0, n); const caret = Math.floor(f / 6) % 2 === 0 && n < 7;
  return (
    <Mount a={a} b={VOICE_END + 0.05} y={195} w={940} h={190}>
      <Glass style={{ inset: 0 }} shineAt={a + 0.05} rim="rgba(226,190,106,.8)" radius={95}>
        <div style={{ position: "absolute", left: 40, top: 40, width: 110, height: 110, borderRadius: 55, background: `url(${staticFile("images/logo.png")}) center/cover`, boxShadow: "0 0 0 4px #E2BE6A" }} />
        <div style={TX({ position: "absolute", left: 180, top: 0, bottom: 0, display: "flex", alignItems: "center", fontSize: 62, letterSpacing: 2, color: n ? "#fff" : "rgba(255,255,255,.5)", fontWeight: n ? 900 : 700 })}>{n ? txt : "Add a comment…"}{caret ? <span style={{ color: C.gold }}>|</span> : null}</div>
        <div style={{ position: "absolute", right: 36, top: 40, width: 110, height: 110, borderRadius: 55, background: send > 0.3 ? "linear-gradient(180deg,#F6E2A6,#E2BE6A)" : "rgba(255,255,255,.18)", color: send > 0.3 ? "#12213A" : "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 60, fontFamily: FONT.sans, fontWeight: 900, transform: `scale(${lerp(1, 1.18, Math.sin(Math.min(1, send) * Math.PI))})` }}>➤</div>
      </Glass>
    </Mount>
  );
};
const Brand: React.FC = () => {
  const t = useCurrentFrame() / FPS; const o = pr(t, 0.4, 0.8) * (1 - pr(t, VOICE_END - 0.05, VOICE_END + 0.1));
  return <div style={{ position: "absolute", right: 36, top: 64, display: "flex", alignItems: "center", gap: 12, opacity: o }}><div style={TX({ fontSize: 28, fontWeight: 900 })}>ideaspulse<span style={{ color: C.gold }}>.in</span></div><Img src={staticFile("images/logo.png")} style={{ width: 76, height: 76, borderRadius: 38, boxShadow: "0 0 0 3px #E2BE6A,0 8px 22px rgba(0,0,0,.5)" }} /></div>;
};

// ------------------------------------------------------------------ end card (navy IdeasPulse background, solid)
const EndCard: React.FC = () => {
  const f = useCurrentFrame(); const t = f / FPS; const a = VOICE_END; if (t < a - 0.02) return null;
  const o = pr(f, F(a), F(a) + 5), ls = sp(f, a + 0.05), hs = sp(f, a + 0.25), q1 = sp(f, a + 0.5), q2 = sp(f, a + 0.65), cs = sp(f, a + 0.9), ws = sp(f, a + 1.1);
  const Q = (src: string, label: string, sub: string, col: string, s: number, left: number, from: number) => (
    <div style={{ position: "absolute", left, top: 720, width: 430, borderRadius: 32, overflow: "hidden", background: "#fff", boxShadow: "0 30px 70px rgba(0,0,0,.55), 0 0 0 4px #E2BE6A", opacity: Math.min(1, s * 3), transform: `translateX(${(1 - s) * from}px) scale(${lerp(0.7, 1, s)})` }}>
      <Img src={staticFile(src)} style={{ width: 390, height: 390, margin: 20 }} />
      <div style={{ height: 104, background: col, color: "#fff", fontFamily: FONT.sans, fontWeight: 800, fontSize: 34, textAlign: "center", paddingTop: 14, lineHeight: 1.15 }}>{label}<div style={{ fontSize: 26, fontWeight: 600 }}>{sub}</div></div>
    </div>);
  return (
    <AbsoluteFill style={{ opacity: o }}>
      <AbsoluteFill style={{ background: "radial-gradient(900px 700px at 50% 30%, rgba(33,140,135,.35), transparent 70%), radial-gradient(800px 600px at 50% 90%, rgba(169,129,46,.32), transparent 70%), linear-gradient(180deg,#172A49 0%,#12213A 50%,#0B1526 100%)" }} />
      <AbsoluteFill style={{ backgroundImage: "linear-gradient(rgba(226,190,106,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(226,190,106,.07) 1px,transparent 1px)", backgroundSize: "64px 64px" }} />
      <Rising a={a} b={DURATION} n={7} seed={4} />
      <Img src={staticFile("images/logo.png")} style={{ position: "absolute", left: 415, top: 150, width: 250, height: 250, borderRadius: 125, boxShadow: "0 0 0 6px #E2BE6A, 0 0 80px rgba(226,190,106,.5)", transform: `scale(${ls}) rotate(${(1 - ls) * -120}deg)`, opacity: Math.min(1, ls * 2) }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 425, textAlign: "center", opacity: Math.min(1, hs * 2), transform: `scale(${lerp(0.7, 1, hs)})` }}>
        <div style={{ fontFamily: FONT.display, fontSize: 96, textTransform: "uppercase", ...GOLD }}>COMMUNITY JOIN KARO</div>
        <div style={TX({ fontSize: 36, fontWeight: 700, color: C.tealL, marginTop: 18 })}>naye business ideas + plans</div>
      </div>
      {Q("images/qr_youtube.png", "▶ YouTube", "@ideaspuls", "linear-gradient(180deg,#ff3b30,#d4241b)", q1, 80, -700)}
      {Q("images/qr_telegram.png", "✈ Telegram", "@ideaspulse", "linear-gradient(180deg,#3aa8e8,#1f86c9)", q2, 570, 700)}
      <div style={{ position: "absolute", left: 0, right: 0, top: 1290, display: "flex", justifyContent: "center", opacity: Math.min(1, cs * 2), transform: `scale(${cs})` }}>
        <Glass style={{ position: "relative", padding: "20px 48px", borderRadius: 60 }} rim="rgba(226,190,106,.8)"><div style={TX({ fontSize: 40 })}>💬 COMMENT <span style={{ color: C.gold }}>'BALLOON'</span> ➜ plan DM mein</div></Glass>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1420, textAlign: "center", fontFamily: FONT.sans, fontWeight: 900, fontSize: 74, opacity: Math.min(1, ws * 2), transform: `scale(${lerp(0.7, 1, ws)})` }}>🌐 <span style={{ color: C.cream }}>ideaspulse</span><span style={{ color: C.gold }}>.in</span></div>
    </AbsoluteFill>
  );
};

export const Reel: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{ background: C.navy2 }}>
      <Picture />
      <AbsoluteFill style={{ background: "radial-gradient(120% 90% at 50% 50%, transparent 55%, rgba(0,0,0,.5))", pointerEvents: "none" }} />
      <Rising a={0} b={6.6} n={9} seed={1} />
      <HookCard /><SpeedPill /><IndiaCard /><Toggle /><InflateStrip /><Steps /><Chips /><Price /><Calc /><Checks /><CommentBox />
      <Captions />
      <Brand />
      <Confetti at={T0("c3")} y={880} /><Confetti at={T0("c14")} y={420} /><Confetti at={T0("c26")} y={420} n={60} />
      <CutFlash />
      <EndCard />
    </AbsoluteFill>
  );
};
