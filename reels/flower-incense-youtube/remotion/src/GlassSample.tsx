import React from "react";
import { AbsoluteFill, Img, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { BRAND_GRADIENT, C, FONT } from "./primitives";

// 15 s sample: STATIC picture, only the glass elements move (slide, flip, drop, orbit, dock, draw, count).
// Styled after the Effects skill's #23 glass-widgets: frosted cards, soft rim light, ring + bar + pill widgets.
const FPS = 30, F = (s: number) => Math.round(s * FPS);
const lerp = (a: number, b: number, x: number) => a + (b - a) * x;
const pr = (f: number, a: number, b: number) => Math.min(1, Math.max(0, (f - a) / (b - a)));
const eo = (x: number) => 1 - Math.pow(1 - x, 3);
const eio = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const SP = { snappy: { damping: 15, stiffness: 150 }, soft: { damping: 20, stiffness: 90 }, bouncy: { damping: 9, stiffness: 170 } };

const useFonts = () => {
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => {
    const defs: [string, string, string][] = [["Anton", "fonts/Anton-Regular.ttf", "400"], ["Poppins", "fonts/Poppins-ExtraBold.ttf", "800"], ["Poppins", "fonts/Poppins-Black.ttf", "900"]];
    Promise.all(defs.map(([n, u, w]) => new FontFace(n, `url(${staticFile(u)})`, { weight: w }).load())).then((fs) => { fs.forEach((x) => (document.fonts as any).add(x)); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
};

// every element: enter spring -> optional exit, returns progress values
const useIn = (at: number, cfg = SP.snappy) => { const f = useCurrentFrame(); return spring({ frame: Math.max(0, f - F(at)), fps: FPS, config: cfg }); };
const useOut = (at: number, len = 10) => pr(useCurrentFrame(), F(at), F(at) + len);

const Glass: React.FC<{ style?: React.CSSProperties; children?: React.ReactNode; tint?: string }> = ({ style, children, tint }) => (
  <div style={{ position: "absolute", borderRadius: 38, overflow: "hidden", background: `linear-gradient(145deg, ${tint ?? "rgba(255,255,255,.20)"} 0%, rgba(255,255,255,.04) 55%, rgba(255,255,255,.10) 100%), rgba(11,21,40,.66)`, backdropFilter: "blur(38px) saturate(170%)", border: "1.5px solid rgba(255,255,255,.38)", boxShadow: "0 40px 90px rgba(0,0,0,.45), inset 0 2px 1px rgba(255,255,255,.55), inset 0 -2px 8px rgba(255,255,255,.06)", ...style }}>
    <div style={{ position: "absolute", inset: 0, background: "linear-gradient(115deg, rgba(255,255,255,.28) 0%, transparent 32%)", pointerEvents: "none" }} />
    {children}
  </div>
);
const T = (s: React.CSSProperties): React.CSSProperties => ({ fontFamily: FONT.sans, fontWeight: 800, color: "#fff", textShadow: "0 3px 10px rgba(0,0,0,.35)", ...s });
const GOLD: React.CSSProperties = { background: BRAND_GRADIENT, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", filter: "drop-shadow(0 4px 0 rgba(0,0,0,.4))" };
const bob = (f: number, ph = 0, amp = 7) => Math.sin(f / 16 + ph) * amp;


// 1) question card: slides in from the left, coins bob around it
const Question: React.FC = () => {
  const f = useCurrentFrame(); const s = useIn(0.15, SP.soft); const o = useOut(4.0, 12);
  const x = lerp(-1100, 110, s) - o * 700; const y = 270 + bob(f, 0, 6);
  return (
    <>
      <Glass style={{ left: x, top: y, width: 1000, height: 400, opacity: 1 - o, filter: `blur(${o * 14}px)` }}>
        <div style={T({ position: "absolute", left: 54, top: 40, fontSize: 30, letterSpacing: 5, color: C.tealLight })}>SABSE ZAROORI SAWAAL</div>
        <div style={{ position: "absolute", left: 54, top: 100, fontFamily: FONT.display, fontSize: 124, lineHeight: 1.05, textTransform: "uppercase", ...GOLD }}>KITNE PAISE<br />CHAHIYE? 💰</div>
        <div style={{ position: "absolute", left: 0, bottom: 0, height: 8, width: `${eo(pr(f, F(0.5), F(3.4))) * 100}%`, background: `linear-gradient(90deg,${C.teal},${C.brand})` }} />
      </Glass>
      {[["₹", 1180, 250, 0], ["🪙", 1330, 470, 2], ["₹", 1040, 560, 4]].map(([t, cx, cy, ph], i) => {
        const si = spring({ frame: Math.max(0, f - F(0.7 + i * 0.25)), fps: FPS, config: SP.bouncy });
        return <Glass key={i} style={{ left: (cx as number) + 0, top: (cy as number) + bob(f, ph as number, 12), width: 120, height: 120, borderRadius: 60, opacity: (1 - o) * si, transform: `scale(${si}) rotate(${(1 - si) * 90 + Math.sin(f / 22 + i) * 6}deg)` }}><div style={T({ fontSize: 64, textAlign: "center", lineHeight: "120px", fontFamily: FONT.display })}>{t}</div></Glass>;
      })}
    </>
  );
};

// 2) stat card: 3D flip in, counter + ring, orbiting chips, then docks to the top-left corner
const Stat: React.FC = () => {
  const f = useCurrentFrame(); const s = useIn(4.62, SP.snappy);
  const dock = eio(pr(f, F(6.7), F(7.3)));
  const val = Math.round(5000 * eo(pr(f, F(4.85), F(6.45))));
  const ring = eo(pr(f, F(4.85), F(6.45)));
  const w = lerp(760, 380, dock), h = lerp(520, 150, dock);
  const left = lerp(580, 60, dock), top = lerp(250, 50, dock) + (1 - dock) * bob(f, 1, 8);
  const R = 150, circ = 2 * Math.PI * R;
  return (
    <>
      <div style={{ position: "absolute", left, top, width: w, height: h, transform: `perspective(1500px) rotateX(${(1 - s) * -88}deg) scale(${lerp(0.7, 1, s)})`, transformOrigin: "50% 100%", opacity: Math.min(1, s * 2) }}>
        <Glass style={{ left: 0, top: 0, width: w, height: h, borderRadius: lerp(44, 34, dock) }} tint="rgba(255,235,170,.30)">
          {dock < 0.5 ? (
            <>
              <svg style={{ position: "absolute", left: w / 2 - 190, top: h / 2 - 190, opacity: 1 - dock * 2 }} width="380" height="380" viewBox="0 0 380 380">
                <circle cx="190" cy="190" r={R} fill="none" stroke="rgba(255,255,255,.18)" strokeWidth="16" />
                <circle cx="190" cy="190" r={R} fill="none" stroke="#39C2BA" strokeWidth="16" strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - ring)} transform="rotate(-90 190 190)" />
              </svg>
              <div style={{ position: "absolute", left: 0, right: 0, top: 150, textAlign: "center", opacity: 1 - dock * 2 }}>
                <div style={T({ fontSize: 28, letterSpacing: 6, color: C.brandSoft })}>SIRF</div>
                <div style={{ fontFamily: FONT.display, fontSize: 124, lineHeight: 1.05, ...GOLD }}>₹{val.toLocaleString("en-IN")}</div>
              </div>
            </>
          ) : (
            <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", gap: 14, opacity: dock * 2 - 1 }}>
              <div style={{ fontFamily: FONT.display, fontSize: 70, ...GOLD }}>₹5,000</div><div style={T({ fontSize: 28, color: C.brandSoft })}>TEST</div>
            </div>
          )}
        </Glass>
      </div>
      {[["💰 BUDGET", 0], ["🧾 HISAAB", 2.1], ["📈 PLAN", 4.2]].map(([t, ph], i) => {
        const a = (f / 52) + (ph as number); const si = spring({ frame: Math.max(0, f - F(5.2 + i * 0.22)), fps: FPS, config: SP.bouncy });
        const out = 1 - eio(pr(f, F(6.5), F(6.85)));
        const cx = 960 + Math.cos(a) * 560, cy = 500 + Math.sin(a) * 270;
        return <Glass key={i} style={{ left: cx - 130, top: cy - 38, width: 260, height: 76, borderRadius: 38, opacity: si * out, transform: `scale(${si}) rotate(${Math.cos(a) * 4}deg)` }}><div style={T({ fontSize: 30, textAlign: "center", lineHeight: "76px" })}>{t}</div></Glass>;
      })}
    </>
  );
};

// 3) warning card: drops from the top, shakes (the card, not the frame), strike line is drawn
const Warn: React.FC = () => {
  const f = useCurrentFrame(); const s = useIn(7.0, SP.bouncy); const o = useOut(9.75, 10);
  const strike = eo(pr(f, F(8.55), F(9.1)));
  const shake = f >= F(8.4) && f < F(8.8) ? Math.sin((f - F(8.4)) * 2.6) * 14 * (1 - (f - F(8.4)) / 12) : 0;
  const y = lerp(-460, 300, s) + (o ? o * -520 : 0);
  return (
    <Glass style={{ left: 420 + shake, top: y, width: 1080, height: 380, opacity: 1 - o, filter: `blur(${o * 12}px)` }} tint="rgba(255,110,70,.30)">
      <div style={T({ position: "absolute", left: 50, top: 44, fontSize: 42, letterSpacing: 3, color: "#FFD3C6" })}>⚠️ LEKIN DHYAN RAHE</div>
      <div style={{ position: "absolute", left: 50, top: 150, fontFamily: FONT.display, fontSize: 128, textTransform: "uppercase", color: "#fff", opacity: pr(f, F(8.3), F(8.5)) }}>YE <span style={{ position: "relative", color: "#FFB79E" }}>FACTORY<span style={{ position: "absolute", left: -8, top: "52%", height: 12, width: `${strike * 104}%`, background: "#FF5A2C", borderRadius: 8, boxShadow: "0 0 20px #FF5A2C" }} /></span> NAHI 🏭</div>
    </Glass>
  );
};

// 4) three step cards (each enters with a different motion) + progress card + pill
const Steps: React.FC = () => {
  const f = useCurrentFrame(); const out = eio(pr(f, F(14.35), F(14.7)));
  const cards = [
    { at: 10.0, x: 130, icon: "🏠", t: "GHAR SE", s: "koi dukaan nahi" },
    { at: 11.25, x: 700, icon: "✋", t: "HAATH SE", s: "koi badi machine nahi" },
    { at: 12.5, x: 1270, icon: "🧪", t: "CHHOTA TEST", s: "pehle check, phir badho" },
  ];
  return (
    <>
      {cards.map((c, i) => {
        const d = Math.max(0, f - F(c.at)); const s = spring({ frame: d, fps: FPS, config: i === 1 ? SP.bouncy : SP.snappy });
        const dx = i === 0 ? (1 - s) * -1100 : i === 2 ? (1 - s) * 1100 : 0;
        const dy = i === 1 ? (1 - s) * -900 : 0;
        const rot = i === 2 ? (1 - s) * 22 : i === 1 ? (1 - s) * -14 : 0;
        return (
          <Glass key={i} style={{ left: c.x + dx, top: 560 + dy + bob(f, i * 2, 8) * s + out * 400, width: 520, height: 330, opacity: Math.min(1, s * 3) * (1 - out), transform: `rotate(${rot}deg)` }}>
            <div style={{ position: "absolute", left: 40, top: 34, fontSize: 80 }}>{c.icon}</div>
            <div style={{ position: "absolute", left: 40, top: 150, fontFamily: FONT.display, fontSize: 70, textTransform: "uppercase", ...GOLD }}>{c.t}</div>
            <div style={T({ position: "absolute", left: 42, top: 240, fontSize: 30, fontWeight: 700, color: C.inkSoft })}>{c.s}</div>
            <div style={{ position: "absolute", right: 30, top: 30, width: 56, height: 56, borderRadius: 28, background: "rgba(57,194,186,.9)", color: "#fff", fontFamily: FONT.display, fontSize: 34, textAlign: "center", lineHeight: "56px", transform: `scale(${pr(f, F(c.at) + 10, F(c.at) + 18)})` }}>{i + 1}</div>
          </Glass>
        );
      })}
      {(() => { const s = pr(f, F(10.2), F(10.6)); const fill = eo(pr(f, F(10.6), F(14.0)));
        return (
          <Glass style={{ left: 130, top: 290 - (1 - eo(s)) * 60, width: 1660, height: 205, opacity: s * (1 - out), transform: `scaleY(${lerp(0.4, 1, eo(s))})`, transformOrigin: "50% 100%" }}>
            <div style={T({ position: "absolute", left: 44, top: 28, fontSize: 32, letterSpacing: 4, color: C.tealLight })}>PLAN ROADMAP</div>
            <div style={{ position: "absolute", left: 44, right: 44, top: 100, height: 22, borderRadius: 11, background: "rgba(255,255,255,.16)", overflow: "hidden" }}><div style={{ width: `${fill * 100}%`, height: "100%", background: `linear-gradient(90deg,${C.teal},${C.brand})`, borderRadius: 11 }} /></div>
            {["TEST", "GRAHAK KI RAAY", "PHIR BADA KADAM"].map((l, i) => <div key={l} style={T({ position: "absolute", left: 44 + i * 560, top: 136, fontSize: 32, color: fill > i / 2.4 ? C.brandSoft : "rgba(255,255,255,.45)" })}>{l}</div>)}
          </Glass>
        ); })()}
    </>
  );
};

const Pill: React.FC = () => {
  const s = useIn(10.4, SP.bouncy); const f = useCurrentFrame(); const out = eio(pr(f, F(14.35), F(14.7)));
  return (
    <Glass style={{ left: 1920 - 60 - 470, top: 50 + (1 - s) * -200, width: 470, height: 96, borderRadius: 48, opacity: s * (1 - out) }}>
      <div style={T({ position: "absolute", inset: 0, textAlign: "center", lineHeight: "96px", fontSize: 34, fontWeight: 700 })}>Edited by <span style={{ color: "#FFB092", fontWeight: 900 }}>IdeasPulse</span></div>
    </Glass>
  );
};

const Outro: React.FC = () => {
  const s = useIn(14.4, SP.bouncy);
  return (
    <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", gap: 16, opacity: Math.min(1, s * 2) }}>
      <Glass style={{ position: "relative", width: 660, height: 250, transform: `scale(${s})` }} tint="rgba(255,235,170,.28)">
        <Img src={staticFile("images/logo.png")} style={{ position: "absolute", left: 40, top: 45, width: 160, height: 160, borderRadius: 80, boxShadow: "0 0 0 4px #E2BE6A" }} />
        <div style={T({ position: "absolute", left: 230, top: 62, fontSize: 56, fontWeight: 900 })}>ideaspulse<span style={{ color: C.brand }}>.in</span></div>
        <div style={T({ position: "absolute", left: 230, top: 140, fontSize: 28, fontWeight: 700, color: C.brandSoft })}>Poora plan · 8 steps</div>
      </Glass>
    </div>
  );
};

export const GlassSample: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{ background: "#0B1526" }}>
      {/* the picture never moves */}
      <Img src={staticFile("images/img_workshop.jpg")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
      <AbsoluteFill style={{ background: "rgba(8,14,26,.46)" }} />
      <AbsoluteFill style={{ background: "radial-gradient(110% 90% at 50% 50%, transparent 50%, rgba(0,0,0,.55))" }} />
      <Question /><Stat /><Warn /><Steps /><Pill /><Outro />
    </AbsoluteFill>
  );
};
