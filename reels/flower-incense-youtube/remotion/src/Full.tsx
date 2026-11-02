import React from "react";
import { AbsoluteFill, Img, Loop, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { BRAND_GRADIENT, C, FONT } from "./primitives";
import data from "./data/video.json";

/**
 * Full 13 min glass-card version. RULE: the picture never moves (no zoom, shake or punch).
 * Only the elements move: glass cards slide / flip / drop / rise / pop, rows alternate sides, bars fill,
 * numbers count, rings draw, strike lines are drawn, chips arrive one by one.
 */
const D: any = data;
const FPS = 30, F = (s: number) => Math.round(s * FPS);
const lerp = (a: number, b: number, x: number) => a + (b - a) * x;
const pr = (f: number, a: number, b: number) => Math.min(1, Math.max(0, (f - a) / (b - a)));
const eo = (x: number) => 1 - Math.pow(1 - x, 3);
const eio = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const SP = { snappy: { damping: 15, stiffness: 150 }, soft: { damping: 20, stiffness: 90 }, bouncy: { damping: 9, stiffness: 170 } };
const EMO = /(\p{Extended_Pictographic}[\u{FE0F}\u{200D}\p{Extended_Pictographic}]*|[0-9#*]\u{FE0F}?\u{20E3})/gu;
const ACC = ["#E2BE6A", "#39C2BA", "#FF9A5A"];

const BaseCtx = React.createContext(0);
const AccCtx = React.createContext(ACC[0]);
const useAF = () => useCurrentFrame() + React.useContext(BaseCtx);          // absolute frame
const useSp = (at: number, cfg = SP.snappy) => { const f = useAF(); return spring({ frame: Math.max(0, f - F(at)), fps: FPS, config: cfg }); };
const useOutP = (t1: number, len = 10) => pr(useAF(), F(t1), F(t1) + len);

// emoji stay white even inside gold gradient text
const gt = (s: string): React.ReactNode[] => String(s).split(EMO).map((p, i) => (i % 2 ? <span key={i} style={{ WebkitTextFillColor: "#fff", color: "#fff", background: "none", filter: "none", textShadow: "none" }}>{p}</span> : p));
const GOLD: React.CSSProperties = { background: BRAND_GRADIENT, WebkitBackgroundClip: "text", backgroundClip: "text", WebkitTextFillColor: "transparent", filter: "drop-shadow(0 4px 0 rgba(0,0,0,.45))" };
const TX = (s: React.CSSProperties = {}): React.CSSProperties => ({ fontFamily: FONT.sans, fontWeight: 800, color: "#fff", textShadow: "0 3px 10px rgba(0,0,0,.4)", ...s });
const useFonts = () => {
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => {
    const defs: [string, string, string][] = [["Anton", "fonts/Anton-Regular.ttf", "400"], ["Poppins", "fonts/Poppins-ExtraBold.ttf", "800"], ["Poppins", "fonts/Poppins-Black.ttf", "900"]];
    Promise.all(defs.map(([n, u, w]) => new FontFace(n, `url(${staticFile(u)})`, { weight: w }).load())).then((fs) => { fs.forEach((x) => (document.fonts as any).add(x)); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
};

// ---------------------------------------------------------------- motion variants
type Dir = "L" | "R" | "T" | "B" | "F" | "Z";
const enter = (s: number, dir: Dir): { transform: string; opacity: number; transformOrigin?: string } => {
  const k = 1 - s;
  switch (dir) {
    case "L": return { transform: `translateX(${k * -1300}px)`, opacity: Math.min(1, s * 3) };
    case "R": return { transform: `translateX(${k * 1300}px)`, opacity: Math.min(1, s * 3) };
    case "T": return { transform: `translateY(${k * -800}px)`, opacity: Math.min(1, s * 3) };
    case "B": return { transform: `translateY(${k * 800}px)`, opacity: Math.min(1, s * 3) };
    case "F": return { transform: `perspective(1600px) rotateX(${k * -85}deg) scale(${lerp(0.8, 1, s)})`, transformOrigin: "50% 100%", opacity: Math.min(1, s * 2.5) };
    default: return { transform: `scale(${lerp(0.55, 1, s)}) rotate(${k * -10}deg)`, opacity: Math.min(1, s * 3) };
  }
};
const leave = (p: number, dir: Dir): string => {
  const e = eio(p);
  return dir === "L" ? `translateX(${-e * 1300}px)` : dir === "R" ? `translateX(${e * 1300}px)` : dir === "T" ? `translateY(${-e * 700}px)` : `translateY(${e * 700}px)`;
};

// ---------------------------------------------------------------- glass
const Glass: React.FC<{ style?: React.CSSProperties; children?: React.ReactNode; tint?: string; flow?: boolean; shineAt?: number; border?: string }> = ({ style, children, tint, flow, shineAt, border }) => {
  const f = useAF(); const sh = shineAt === undefined ? 0 : pr(f, F(shineAt) + 4, F(shineAt) + 30);
  return (
    <div style={{ position: flow ? "relative" : "absolute", borderRadius: 38, overflow: "hidden", background: `linear-gradient(145deg, ${tint ?? "rgba(255,255,255,.20)"} 0%, rgba(255,255,255,.04) 55%, rgba(255,255,255,.10) 100%), rgba(11,21,40,.68)`, backdropFilter: "blur(38px) saturate(170%)", border: `1.5px solid ${border ?? "rgba(255,255,255,.38)"}`, boxShadow: "0 40px 90px rgba(0,0,0,.45), inset 0 2px 1px rgba(255,255,255,.55), inset 0 -2px 8px rgba(255,255,255,.06)", ...style }}>
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(115deg, rgba(255,255,255,.26) 0%, transparent 32%)", pointerEvents: "none" }} />
      {shineAt !== undefined && sh > 0 && sh < 1 ? <div style={{ position: "absolute", top: 0, bottom: 0, width: "26%", left: `${lerp(-30, 120, sh)}%`, background: "linear-gradient(100deg,transparent,rgba(255,255,255,.35),transparent)", pointerEvents: "none" }} /> : null}
      {children}
    </div>
  );
};

// ---------------------------------------------------------------- overlays
const Wrap: React.FC<{ o: any; dir: Dir; children: React.ReactNode; style?: React.CSSProperties; noOut?: boolean }> = ({ o, dir, children, style, noOut }) => {
  const s = useSp(o.at ?? o.t0, dir === "Z" ? SP.bouncy : SP.snappy); const p = noOut ? 0 : useOutP(o.t1, 10);
  const e = enter(s, dir);
  return <div style={{ position: "absolute", ...style, transform: `${e.transform} ${p ? leave(p, dir === "F" || dir === "Z" ? "B" : dir) : ""}`, transformOrigin: e.transformOrigin, opacity: e.opacity * (1 - p), filter: p ? `blur(${p * 10}px)` : undefined }}>{children}</div>;
};

const TitleCard: React.FC<{ o: any; k: number }> = ({ o, k }) => {
  const acc = React.useContext(AccCtx); const f = useAF();
  const top = o.pos === "top" ? 90 : o.pos === "low" ? 600 : 300;
  const dir: Dir = o.pos === "top" ? "T" : o.pos === "low" ? "B" : k % 2 ? "F" : "Z";
  const subS = useSp(o.sub_at ?? o.at + 0.5, SP.bouncy);
  return (
    <Wrap o={o} dir={dir} style={{ left: 0, right: 0, top, display: "flex", justifyContent: "center" }}>
      <Glass flow shineAt={o.at} style={{ padding: "40px 80px 44px", maxWidth: 1640, textAlign: "center" }} border={acc + "AA"}>
        {o.kicker ? <div style={TX({ fontSize: 34, letterSpacing: 5, color: acc, marginBottom: 14 })}>{gt(o.kicker)}</div> : null}
        <div style={{ fontFamily: FONT.display, fontSize: Math.min(o.size || 120, 138), lineHeight: 1.06, textTransform: "uppercase", letterSpacing: 1, ...GOLD }}>{gt(o.title)}</div>
        {o.sub ? <div style={{ marginTop: 24, transform: `scale(${subS})`, opacity: Math.min(1, subS * 2) }}><span style={{ display: "inline-block", padding: "12px 34px", borderRadius: 999, fontFamily: FONT.sans, fontWeight: 800, fontSize: 40, color: o.subcls === "p-red" ? "#FFC7B5" : "#12213A", background: o.subcls === "p-red" ? "rgba(255,90,44,.25)" : "linear-gradient(180deg,#F6E2A6,#E2BE6A 50%,#B88E36)", border: o.subcls === "p-red" ? "3px solid #FF5A2C" : "none" }}>{gt(o.sub)}</span></div> : null}
      </Glass>
    </Wrap>
  );
};

const StampCard: React.FC<{ o: any }> = ({ o }) => {
  const f = useAF(); const s = useSp(o.at, SP.bouncy); const p = useOutP(o.t1, 10);
  const col = o.color === "red" ? "#FF6B3D" : o.color === "teal" ? "#39C2BA" : "#E2BE6A";
  const d = f - F(o.at); const shake = d > 4 && d < 16 ? Math.sin(d * 2.4) * 12 * (1 - (d - 4) / 12) : 0;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: o.top || 430, display: "flex", justifyContent: "center", opacity: Math.min(1, s * 3) * (1 - p), transform: `translateX(${shake}px) scale(${lerp(2.2, 1, s)}) rotate(${(o.rot ?? -4) * s}deg) translateY(${p * 80}px)`, filter: `blur(${(1 - s) * 10 + p * 10}px)` }}>
      <Glass flow tint={`${col}33`} border={col} style={{ padding: "26px 70px", borderWidth: 6, borderRadius: 30 }}>
        <div style={{ fontFamily: FONT.display, fontSize: o.size || 96, textTransform: "uppercase", color: col, textShadow: "0 5px 0 rgba(0,0,0,.45)", letterSpacing: 2, whiteSpace: "nowrap" }}>{gt(o.text)}</div>
      </Glass>
    </div>
  );
};

const LowerChips: React.FC<{ o: any }> = ({ o }) => {
  const p = useOutP(o.t1, 10);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 130, display: "flex", justifyContent: "center", alignItems: "center", gap: 16, opacity: 1 - p, transform: `translateY(${p * 90}px)` }}>
      {o.chips.map((c: any, i: number) => <Chip key={i} c={c} i={i} arrows={o.arrows} />)}
    </div>
  );
};
const Chip: React.FC<{ c: any; i: number; arrows: boolean }> = ({ c, i, arrows }) => {
  const s = useSp(c.at, SP.bouncy); const dir = (["L", "B", "R"] as Dir[])[i % 3]; const e = enter(s, dir === "B" ? "B" : dir);
  return (
    <>
      {arrows && i > 0 ? <div style={{ fontFamily: FONT.display, fontSize: 52, color: "#E2BE6A", opacity: Math.min(1, s * 2) }}>➜</div> : null}
      <div style={{ transform: e.transform, opacity: e.opacity }}>
        <Glass flow style={{ borderRadius: 26, padding: "16px 36px", background: c.hl ? "linear-gradient(180deg,#F6E2A6,#E2BE6A 50%,#B88E36)" : undefined, border: c.hl ? "1.5px solid #F6E2A6" : undefined }}>
          <div style={{ fontFamily: FONT.display, fontSize: 52, textTransform: "uppercase", letterSpacing: 1, color: c.hl ? "#12213A" : "#fff", textShadow: c.hl ? "none" : "0 4px 0 rgba(0,0,0,.4)", whiteSpace: "nowrap" }}>{gt(c.text)}</div>
        </Glass>
      </div>
    </>
  );
};

const RowInner: React.FC<{ it: any; i: number; style: string; maxv: number; big?: boolean }> = ({ it, i, style, maxv, big }) => {
  const f = useAF(); const s = useSp(it.at, SP.snappy); const k = 1 - s;
  const val = it.val; const vs = it.valAt ? useSp(it.valAt, SP.bouncy) : s;
  const icon = it.icon || (style === "check" ? "✅" : style === "cross" ? "❌" : style === "num" ? String(i + 1) : "•");
  const fs = big ? 40 : 36;
  if (style === "bars" && !it.total) {
    const w = (it.val / maxv) * 84 * eo(pr(f, F(it.at) + 2, F(it.at) + 20));
    return (
      <div style={{ position: "relative", height: 66, margin: "9px 0", borderRadius: 14, background: "rgba(255,255,255,.07)", overflow: "hidden", opacity: Math.min(1, s * 2), transform: `translateX(${k * (i % 2 ? 120 : -120)}px)` }}>
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: `${w}%`, background: `linear-gradient(90deg,${C.teal},${C.brand})`, borderRadius: 14 }} />
        <div style={TX({ position: "absolute", left: 22, top: 0, bottom: 0, display: "flex", alignItems: "center", fontSize: 32 })}>{gt(it.text)}</div>
        <div style={{ position: "absolute", right: 20, top: 0, bottom: 0, display: "flex", alignItems: "center", fontFamily: FONT.display, fontSize: 40, color: "#F6E2A6" }}>₹{Number(it.val).toLocaleString("en-IN")}</div>
      </div>
    );
  }
  const valTxt = style === "bars" ? `₹${Number(val).toLocaleString("en-IN")}` : val;
  const pulse = it.total ? 1 + 0.025 * Math.sin(f / 7) : 1;
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 18, padding: big ? "18px 22px" : "14px 20px", margin: "10px 0", borderRadius: 18, borderLeft: `7px solid ${it.warn || style === "cross" ? "#FF5A2C" : it.total ? "#39C2BA" : "#E2BE6A"}`, background: it.warn ? "rgba(255,90,44,.16)" : it.total ? "linear-gradient(90deg,rgba(33,140,135,.6),rgba(33,140,135,.2))" : "rgba(255,255,255,.07)", opacity: Math.min(1, s * 2), transform: `translateX(${k * (i % 2 ? 150 : -150)}px) scale(${pulse})` }}>
      <div style={{ width: 56, textAlign: "center", fontSize: style === "num" ? 44 : 38, fontFamily: style === "num" ? FONT.display : FONT.sans, color: "#fff", flex: "none" }}>{gt(icon)}</div>
      <div style={TX({ flex: 1, fontSize: fs, fontWeight: it.total ? 900 : 700, lineHeight: 1.2, color: it.warn ? "#FFD3C6" : "#fff" })}>{gt(it.text)}</div>
      {valTxt ? <div style={{ flex: "none", fontFamily: FONT.display, fontSize: it.total ? 54 : 46, color: it.total ? "#fff" : "#F6E2A6", opacity: Math.min(1, vs * 2), transform: `scale(${it.valAt ? lerp(0.2, 1, vs) : 1})`, letterSpacing: 1 }}>{gt(valTxt)}</div> : null}
    </div>
  );
};

// each row opens like an accordion, so the glass card grows as the voice reaches that line
const Row: React.FC<{ it: any; i: number; style: string; maxv: number; big?: boolean; w: number }> = (props) => {
  const f = useAF(); const { it, style, w, big } = props; const fs = big ? 40 : 36;
  const bar = style === "bars" && !it.total;
  const innerW = w - 76 - 56 - 18 - 54 - (it.val !== undefined ? 180 : 0);
  const lines = bar ? 1 : Math.max(1, Math.ceil((String(it.text).length * fs * 0.54) / innerW));
  const H = bar ? 84 : lines * fs * 1.22 + (big ? 36 : 28) + 22;
  const p = eo(pr(f, F(it.at) - 1, F(it.at) + 9));
  return <div style={{ height: p >= 1 ? undefined : H * p, overflow: p >= 1 ? "visible" : "hidden" }}><RowInner {...props} /></div>;
};

const Panel: React.FC<{ o: any; k: number; side?: string; titleSize?: number; top?: number; w?: number }> = ({ o, k, side, top, w }) => {
  const acc = React.useContext(AccCtx); const pos = side || o.pos || "left"; const width = w || o.w || 940; const tp = top ?? o.top ?? 150;
  const dir: Dir = pos === "left" ? "L" : pos === "right" ? "R" : (k % 2 ? "F" : "B");
  const place: React.CSSProperties = pos === "right" ? { right: 70, top: tp, width } : pos === "center" ? { left: (1920 - width) / 2, top: tp, width } : { left: 70, top: tp, width };
  const maxv = Math.max(1, ...o.items.filter((i: any) => !i.total && typeof i.val === "number").map((i: any) => i.val));
  const rows = o.style === "bars" ? o.items : o.items;
  const dots = o.dots;
  return (
    <Wrap o={o} dir={dir} style={place}>
      <Glass flow shineAt={o.at} border={acc + "88"} style={{ padding: "30px 38px 24px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 8 }}>
          {o.kicker ? <span style={TX({ fontSize: 30, letterSpacing: 4, color: acc })}>{gt(o.kicker)}</span> : null}
          {dots ? <span style={{ marginLeft: "auto", display: "flex", gap: 9 }}>{Array.from({ length: dots[1] }, (_, i) => <i key={i} style={{ width: 17, height: 17, borderRadius: 9, background: i < dots[0] ? acc : "rgba(255,255,255,.2)", boxShadow: i < dots[0] ? `0 0 12px ${acc}` : "none", display: "inline-block" }} />)}</span> : null}
        </div>
        {o.title ? <div style={{ fontFamily: FONT.display, fontSize: 68, textTransform: "uppercase", lineHeight: 1.05, marginBottom: 10, ...GOLD }}>{gt(o.title)}</div> : null}
        {rows.map((it: any, i: number) => <Row key={i} it={it} i={i} style={o.style || "list"} maxv={maxv} big={o.style === "num" && width > 1000} w={width} />)}
        {o.footer ? <div style={TX({ fontSize: 24, fontWeight: 600, color: "rgba(255,255,255,.75)", marginTop: 8 })}>{gt(o.footer)}</div> : null}
      </Glass>
    </Wrap>
  );
};

const Stat: React.FC<{ o: any }> = ({ o }) => {
  const f = useAF(); const s = useSp(o.at, SP.snappy); const p = useOutP(o.t1, 14); const e = enter(s, "F");
  const cnt = eo(pr(f, F(o.at) + 6, F(o.at) + 50)); const R = 150, circ = 2 * Math.PI * R;
  const subS = useSp(o.sub_at ?? o.at + 1.5, SP.bouncy);
  return (
    <div style={{ position: "absolute", left: 580, top: 220, width: 760, height: 600, transform: `${e.transform} translate(${-eio(p) * 520}px,${-eio(p) * 150}px) scale(${1 - eio(p) * 0.5})`, transformOrigin: "50% 100%", opacity: e.opacity * (1 - p) }}>
      <Glass style={{ left: 0, top: 0, width: 760, height: 520, borderRadius: 44 }} tint="rgba(255,235,170,.30)" shineAt={o.at}>
        <svg style={{ position: "absolute", left: 190, top: 70 }} width="380" height="380" viewBox="0 0 380 380">
          <circle cx="190" cy="190" r={R} fill="none" stroke="rgba(255,255,255,.18)" strokeWidth="16" />
          <circle cx="190" cy="190" r={R} fill="none" stroke="#39C2BA" strokeWidth="16" strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - cnt)} transform="rotate(-90 190 190)" />
        </svg>
        <div style={{ position: "absolute", left: 0, right: 0, top: 150, textAlign: "center" }}>
          <div style={TX({ fontSize: 30, letterSpacing: 6, color: "#F6E2A6" })}>{gt(o.kicker || "")}</div>
          <div style={{ fontFamily: FONT.display, fontSize: 128, lineHeight: 1.05, ...GOLD }}>{gt((o.prefix ?? "₹") + Math.round(o.value * cnt).toLocaleString("en-IN"))}</div>
        </div>
      </Glass>
      {o.sub ? <div style={{ position: "absolute", left: 0, right: 0, top: 540, textAlign: "center", transform: `scale(${subS})`, opacity: Math.min(1, subS * 2) }}><span style={{ display: "inline-block", padding: "12px 34px", borderRadius: 999, background: "rgba(255,90,44,.25)", border: "3px solid #FF5A2C", color: "#FFC7B5", fontFamily: FONT.sans, fontWeight: 800, fontSize: 38 }}>{gt(o.sub)}</span></div> : null}
    </div>
  );
};

const Timeline: React.FC<{ o: any }> = ({ o }) => {
  const acc = React.useContext(AccCtx); const f = useAF(); const p = useOutP(o.t1, 10); const hs = useSp(o.at, SP.snappy);
  const last = o.blocks[o.blocks.length - 1]; const fill = pr(f, F(o.blocks[0].at), F(last.at) + 20);
  return (
    <div style={{ position: "absolute", inset: 0, opacity: 1 - p, transform: `translateY(${p * 80}px)` }}>
      <Wrap o={{ ...o, t1: 9999 }} dir="T" style={{ left: 0, right: 0, top: 120, display: "flex", justifyContent: "center" }} noOut>
        <Glass flow shineAt={o.at} border={acc + "AA"} style={{ padding: "22px 80px" }}><div style={{ fontFamily: FONT.display, fontSize: 96, textTransform: "uppercase", ...GOLD }}>{gt(o.title)}</div></Glass>
      </Wrap>
      <div style={{ position: "absolute", left: 90, right: 90, top: 440, height: 10, borderRadius: 5, background: "rgba(255,255,255,.18)", opacity: Math.min(1, hs * 2) }}><div style={{ width: `${fill * 100}%`, height: "100%", borderRadius: 5, background: `linear-gradient(90deg,${C.teal},${C.brand})` }} /></div>
      <div style={{ position: "absolute", left: 90, right: 90, top: 490, display: "flex", gap: 18 }}>
        {o.blocks.map((b: any, i: number) => { const s = useSp(b.at, SP.bouncy); const e = enter(s, "F"); return (
          <div key={i} style={{ flex: 1, transform: e.transform, transformOrigin: e.transformOrigin, opacity: e.opacity }}>
            <Glass flow style={{ padding: "26px 16px 30px", textAlign: "center", borderRadius: 28 }}>
              <div style={{ fontFamily: FONT.display, fontSize: 54, color: "#F6E2A6" }}>{b.day}</div>
              <div style={TX({ marginTop: 12, fontSize: 31, fontWeight: 700, lineHeight: 1.3 })}>{gt(b.text)}</div>
            </Glass>
          </div>); })}
      </div>
    </div>
  );
};

const Cards: React.FC<{ o: any }> = ({ o }) => {
  const acc = React.useContext(AccCtx); const p = useOutP(o.t1, 10);
  return (
    <div style={{ position: "absolute", inset: 0, opacity: 1 - p, transform: `translateY(${p * 80}px)` }}>
      <Wrap o={{ ...o, t1: 9999 }} dir="T" style={{ left: 0, right: 0, top: 150, display: "flex", justifyContent: "center" }} noOut>
        <Glass flow shineAt={o.at} border={acc + "AA"} style={{ padding: "22px 80px" }}><div style={{ fontFamily: FONT.display, fontSize: 92, textTransform: "uppercase", ...GOLD }}>{gt(o.title)}</div></Glass>
      </Wrap>
      <div style={{ position: "absolute", left: 110, right: 110, top: 400, display: "flex", gap: 26 }}>
        {o.cards.map((c: any, i: number) => { const s = useSp(c.at, SP.bouncy); const e = enter(s, i % 2 ? "B" : "F"); return (
          <div key={i} style={{ flex: 1, transform: e.transform, transformOrigin: e.transformOrigin, opacity: e.opacity }}>
            <Glass flow style={{ padding: "34px 20px", textAlign: "center" }}>
              <div style={{ fontSize: 76 }}>{gt(c.icon)}</div>
              <div style={TX({ marginTop: 10, fontSize: 31, lineHeight: 1.2, minHeight: 76 })}>{gt(c.label)}</div>
              <div style={{ marginTop: 10, fontFamily: FONT.display, fontSize: 58, color: "#F6E2A6" }}>{c.val}</div>
            </Glass>
          </div>); })}
      </div>
      {o.footer ? <div style={TX({ position: "absolute", left: 0, right: 0, top: 800, textAlign: "center", fontSize: 30, fontWeight: 700, color: "rgba(255,255,255,.85)" })}>{gt(o.footer)}</div> : null}
    </div>
  );
};

const Compare: React.FC<{ o: any }> = ({ o }) => (
  <>
    {o.cols.map((c: any, ci: number) => <Panel key={ci} k={ci} o={{ ...o, kicker: c.kicker, title: c.title, items: c.rows, style: "money", footer: ci ? o.footer : undefined }} side={ci ? "right" : "left"} top={150} w={900} />)}
  </>
);

const QAItem: React.FC<{ q: any }> = ({ q }) => {
  const f = useAF(); const acc = React.useContext(AccCtx);
  const sq = useSp(q.q_at, SP.snappy), sa = useSp(q.a_at, SP.bouncy), p = pr(f, F(q.t1), F(q.t1) + 12);
  if (f < F(q.q_at) - 2 || f > F(q.t1) + 14) return null;
  return (
    <div style={{ position: "absolute", inset: 0, opacity: 1 - p }}>
      <div style={{ position: "absolute", left: 70, top: 160, width: 1280, transform: `${enter(sq, "L").transform} translateX(${-eio(p) * 600}px)`, opacity: enter(sq, "L").opacity }}>
        <Glass flow tint="rgba(57,194,186,.25)" border="#39C2BAAA" shineAt={q.q_at} style={{ padding: "26px 44px 32px" }}>
          <div style={TX({ fontSize: 30, letterSpacing: 5, color: "#39C2BA" })}>SAWAAL {q.n} / 7</div>
          <div style={{ fontFamily: FONT.display, fontSize: 82, lineHeight: 1.08, textTransform: "uppercase", color: "#fff", textShadow: "0 5px 0 rgba(0,0,0,.45)" }}>{gt(q.q)}</div>
        </Glass>
      </div>
      <div style={{ position: "absolute", right: 70, top: 560, width: 1260, transform: `${enter(sa, "F").transform} translateX(${eio(p) * 600}px)`, transformOrigin: "50% 100%", opacity: enter(sa, "F").opacity }}>
        <Glass flow tint="rgba(226,190,106,.28)" border={acc + "AA"} shineAt={q.a_at} style={{ padding: "26px 44px 34px" }}>
          <div style={TX({ fontSize: 30, letterSpacing: 5, color: acc })}>JAWAAB</div>
          <div style={{ fontFamily: FONT.display, fontSize: 86, lineHeight: 1.06, textTransform: "uppercase", ...GOLD }}>{gt(q.a)}</div>
          <div style={TX({ marginTop: 12, fontSize: 36, fontWeight: 700, lineHeight: 1.3, color: "#EDEFF5" })}>{gt(q.sub)}</div>
        </Glass>
      </div>
    </div>
  );
};
const QA: React.FC<{ o: any }> = ({ o }) => <>{o.items.map((q: any, i: number) => <QAItem key={i} q={q} />)}</>;

let ovCount = 0;
const Overlay: React.FC<{ o: any; k: number }> = ({ o, k }) => {
  switch (o.type) {
    case "title": return <TitleCard o={o} k={k} />;
    case "stamp": return <StampCard o={o} />;
    case "lower": return <LowerChips o={o} />;
    case "panel": return <Panel o={o} k={k} />;
    case "stat": return <Stat o={o} />;
    case "timeline": return <Timeline o={o} />;
    case "cards": return <Cards o={o} />;
    case "compare": return <Compare o={o} />;
    case "qa": return <QA o={o} />;
    default: return null;
  }
};

// ---------------------------------------------------------------- backgrounds (the picture itself never moves)
const Bg: React.FC<{ b: any; first: boolean }> = ({ b, first }) => {
  const f = useCurrentFrame(); const op = first ? 1 : interpolate(f, [0, 6], [0, 1], CL);
  if (b.kind === "img") return <AbsoluteFill style={{ opacity: op }}><Img src={staticFile(`images/${b.name}.jpg`)} style={{ width: "100%", height: "100%", objectFit: "cover" }} /></AbsoluteFill>;
  const full = D.clipdur[b.name] ?? 9.9, avail = Math.max(1, full - (b.inn || 0));
  const segS = b.t1 - b.t0 + 0.3, rate = Math.min(1, Math.max(0.55, avail / segS));
  const loopLen = Math.max(12, Math.floor((avail * FPS) / rate) - 3);
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <Loop durationInFrames={loopLen}><OffthreadVideo src={staticFile(`clips/${b.name}.mp4`)} startFrom={Math.round((b.inn || 0) * FPS)} playbackRate={rate} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} /></Loop>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- full-screen cards
const IMGS = ["img_temple_sunrise", "img_workshop", "img_puja_cone", "img_cones_sticks", "img_packs_money"];
const ChapterCard: React.FC<{ c: any }> = ({ c }) => {
  const f = useCurrentFrame(); const s = spring({ frame: f - 2, fps: FPS, config: SP.bouncy }); const e = enter(s, "F"); const acc = ACC[(c.n - 1) % 3];
  const op = interpolate(f, [0, 4, F(c.t1 - c.t0) + 2, F(c.t1 - c.t0) + 7], [0, 1, 1, 0], CL); const ring = eo(pr(f, 4, 24)); const R = 120, circ = 2 * Math.PI * R;
  const ts = spring({ frame: Math.max(0, f - 16), fps: FPS, config: SP.snappy });
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <Img src={staticFile(`images/${IMGS[(c.n - 1) % 5]}.jpg`)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
      <AbsoluteFill style={{ background: "rgba(8,14,26,.62)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 250, display: "flex", justifyContent: "center", transform: e.transform, transformOrigin: e.transformOrigin, opacity: e.opacity }}>
        <Glass flow shineAt={0} border={acc + "AA"} style={{ padding: "50px 90px 56px", textAlign: "center", maxWidth: 1600 }}>
          <div style={{ position: "relative", width: 280, height: 280, margin: "0 auto 10px" }}>
            <svg width="280" height="280" viewBox="0 0 280 280"><circle cx="140" cy="140" r={R} fill="none" stroke="rgba(255,255,255,.18)" strokeWidth="12" /><circle cx="140" cy="140" r={R} fill="none" stroke={acc} strokeWidth="12" strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - ring)} transform="rotate(-90 140 140)" /></svg>
            <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FONT.display, fontSize: 130, color: acc }}>{String(c.n).padStart(2, "0")}</div>
          </div>
          <div style={TX({ fontSize: 32, letterSpacing: 8, color: acc })}>CHAPTER {c.n}</div>
          <div style={{ fontFamily: FONT.display, fontSize: 100, lineHeight: 1.08, textTransform: "uppercase", marginTop: 6, ...GOLD }}>{gt(c.title)}</div>
          {c.tease ? <div style={{ marginTop: 20, opacity: Math.min(1, ts * 2), transform: `translateY(${(1 - ts) * 30}px)`, ...TX({ fontSize: 38, fontWeight: 700, color: "#EDEFF5" }) }}>▶ {gt(c.tease)}</div> : null}
        </Glass>
      </div>
    </AbsoluteFill>
  );
};

const Intro: React.FC = () => {
  const f = useCurrentFrame(); const I = D.intro; const ls = spring({ frame: f - 2, fps: FPS, config: SP.bouncy }); const ts = spring({ frame: f - 14, fps: FPS, config: SP.snappy }); const ss = spring({ frame: f - 34, fps: FPS, config: SP.bouncy });
  const op = interpolate(f, [F(I.t1) - 5, F(I.t1) + 5], [1, 0], CL);
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <Img src={staticFile("images/img_puja_cone.jpg")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
      <AbsoluteFill style={{ background: "rgba(8,14,26,.55)" }} />
      <Img src={staticFile("images/logo.png")} style={{ position: "absolute", left: 860, top: 90, width: 200, height: 200, borderRadius: 100, boxShadow: "0 0 0 5px #E2BE6A, 0 0 60px rgba(226,190,106,.5)", transform: `scale(${ls}) rotate(${(1 - ls) * -120}deg)`, opacity: Math.min(1, ls * 2) }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 340, display: "flex", justifyContent: "center", ...enter(ts, "B") }}>
        <Glass flow shineAt={0.5} style={{ padding: "36px 80px 40px", textAlign: "center", maxWidth: 1640 }}>
          <div style={TX({ fontSize: 40, letterSpacing: 6, color: "#E2BE6A" })}>{I.kicker}</div>
          <div style={{ fontFamily: FONT.display, fontSize: 126, lineHeight: 1.06, textTransform: "uppercase", marginTop: 6, ...GOLD }}>{I.title}</div>
          <div style={{ marginTop: 22, transform: `scale(${ss})`, opacity: Math.min(1, ss * 2) }}><span style={{ display: "inline-block", padding: "12px 36px", borderRadius: 999, fontFamily: FONT.sans, fontWeight: 800, fontSize: 40, color: "#12213A", background: "linear-gradient(180deg,#F6E2A6,#E2BE6A 50%,#B88E36)" }}>{I.sub}</span></div>
        </Glass>
      </div>
    </AbsoluteFill>
  );
};

const QR: React.FC<{ src: string; label: string; handle: string; col: string; at: number; left: number; dir: Dir }> = ({ src, label, handle, col, at, left, dir }) => {
  const s = useSp(at, SP.bouncy); const e = enter(s, dir);
  return (
    <div style={{ position: "absolute", left, top: 330, width: 340, borderRadius: 28, overflow: "hidden", background: "#fff", boxShadow: "0 28px 70px rgba(0,0,0,.55), 0 0 0 4px #E2BE6A", transform: e.transform, transformOrigin: e.transformOrigin, opacity: e.opacity }}>
      <Img src={staticFile(src)} style={{ width: 310, height: 310, margin: 15 }} />
      <div style={{ height: 86, background: col, color: "#fff", fontFamily: FONT.sans, fontWeight: 800, fontSize: 30, textAlign: "center", paddingTop: 12, lineHeight: 1.15 }}>{label}<div style={{ fontSize: 24, fontWeight: 600 }}>{handle}</div></div>
    </div>
  );
};
const End: React.FC = () => {
  const f = useAF(); const E = D.end; const ls = useSp(E.t0 + 0.1, SP.bouncy); const ts = useSp(E.t0 + 0.3, SP.snappy); const cs = useSp(E.t0 + 1.3, SP.bouncy); const ws = useSp(E.t0 + 1.6, SP.bouncy); const ns = useSp(E.t0 + 2.0, SP.soft);
  const op = interpolate(f, [F(E.t0), F(E.t0) + 6], [0, 1], CL);
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <Img src={staticFile("images/img_temple_sunrise.jpg")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
      <AbsoluteFill style={{ background: "rgba(8,14,26,.72)" }} />
      <Img src={staticFile("images/logo.png")} style={{ position: "absolute", left: 110, top: 80, width: 180, height: 180, borderRadius: 90, boxShadow: "0 0 0 5px #E2BE6A", transform: `scale(${ls}) rotate(${(1 - ls) * -120}deg)` }} />
      <div style={{ position: "absolute", left: 330, top: 90, ...enter(ts, "L") }}>
        <div style={{ fontFamily: FONT.display, fontSize: 92, textTransform: "uppercase", ...GOLD }}>SUBSCRIBE KARO 🔔</div>
        <div style={TX({ fontSize: 36, fontWeight: 700, color: "#EDEFF5" })}>Har hafte naye business ideas + plans</div>
      </div>
      <QR src="images/qr_youtube.png" label="▶ YouTube" handle="@ideaspuls" col="#E02B20" at={E.t0 + 0.8} left={110} dir="B" />
      <QR src="images/qr_telegram.png" label="✈ Telegram" handle="@ideaspulse" col="#2A94D6" at={E.t0 + 1.0} left={490} dir="B" />
      <div style={{ position: "absolute", left: 110, top: 810, transform: `scale(${cs})`, opacity: Math.min(1, cs * 2), transformOrigin: "0 50%" }}><Glass flow style={{ borderRadius: 40, padding: "14px 36px" }}><div style={TX({ fontSize: 38 })}>💬 Plan ke liye COMMENT <span style={{ color: "#E2BE6A" }}>'FLOWER'</span></div></Glass></div>
      <div style={{ position: "absolute", left: 110, top: 910, fontFamily: FONT.sans, fontWeight: 900, fontSize: 64, transform: `scale(${ws})`, transformOrigin: "0 50%" }}>🌐 <span style={{ color: "#FAF9F5" }}>ideaspulse</span><span style={{ color: "#E2BE6A" }}>.in</span></div>
      <div style={{ position: "absolute", left: 960, top: 300, width: 850, height: 520, opacity: Math.min(1, ns * 2), transform: `translateX(${(1 - ns) * 300}px)` }}>
        <Glass style={{ inset: 0, borderRadius: 30, border: "3px dashed rgba(226,190,106,.6)" }}><div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FONT.display, fontSize: 64, color: "rgba(226,190,106,.8)" }}>▶ AGLA VIDEO</div></Glass>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- chrome (static)
const Chrome: React.FC = () => {
  const f = useCurrentFrame(); const t = f / FPS;
  const hide = t < D.intro.t1 || t >= D.end.t0 - 0.05 || D.chapters.some((c: any) => t >= c.t0 - 0.05 && t < c.t1 + 0.1);
  const pi = D.parts.findIndex((p: any) => t >= p.start && t < p.end + p.gapAfter);
  const acc = ACC[Math.max(0, pi) % 3];
  return (
    <AbsoluteFill style={{ opacity: hide ? 0 : 1, pointerEvents: "none" }}>
      <div style={{ position: "absolute", right: 40, top: 28, display: "flex", alignItems: "center", gap: 14 }}>
        <div style={TX({ fontSize: 30, fontWeight: 900 })}>ideaspulse<span style={{ color: "#E2BE6A" }}>.in</span></div>
        <Img src={staticFile("images/logo.png")} style={{ width: 84, height: 84, borderRadius: 42, boxShadow: "0 0 0 3px #E2BE6A, 0 8px 24px rgba(0,0,0,.5)" }} />
      </div>
      <div style={{ position: "absolute", left: 40, bottom: 52, ...TX({ fontSize: 24, letterSpacing: 2, padding: "6px 18px", borderRadius: 999, background: "rgba(11,21,38,.8)", border: `2px solid ${acc}99`, color: "#F6E2A6" }) }}>{pi >= 0 ? `${String(pi + 1).padStart(2, "0")} • ${D.parts[pi].short}` : ""}</div>
      <div style={{ position: "absolute", left: 40, right: 40, bottom: 26, height: 8, display: "flex", gap: 8 }}>
        {D.parts.map((p: any, i: number) => <div key={i} style={{ position: "relative", flex: 1, borderRadius: 6, background: "rgba(255,255,255,.2)", overflow: "hidden" }}><div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: `${pr(t, p.start, p.end) * 100}%`, background: `linear-gradient(90deg,${C.teal},${C.brand})` }} /></div>)}
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- root
export const Full: React.FC = () => {
  useFonts();
  const partOf = (t: number) => Math.max(0, D.parts.findIndex((p: any) => t >= p.start - 0.01 && t < p.end + p.gapAfter + 0.01));
  return (
    <AbsoluteFill style={{ background: "#0B1526" }}>
      {D.bg.map((b: any, i: number) => <Sequence key={i} from={F(b.t0)} durationInFrames={F(b.t1) - F(b.t0) + 8}><Bg b={b} first={i === 0 || b.t0 === D.parts[0].start} /></Sequence>)}
      <AbsoluteFill style={{ background: "rgba(8,14,26,.42)" }} />
      <AbsoluteFill style={{ background: "radial-gradient(110% 90% at 50% 50%, transparent 50%, rgba(0,0,0,.55))" }} />
      {D.ov.map((o: any, i: number) => {
        const base = F(o.t0) - 2;
        return <Sequence key={i} from={base} durationInFrames={F(o.t1) - base + 16}><BaseCtx.Provider value={base}><AccCtx.Provider value={ACC[partOf(o.t0) % 3]}><Overlay o={o} k={i} /></AccCtx.Provider></BaseCtx.Provider></Sequence>;
      })}
      <Chrome />
      {D.chapters.map((c: any, i: number) => <Sequence key={i} from={F(c.t0)} durationInFrames={F(c.t1 - c.t0) + 8}><ChapterCard c={c} /></Sequence>)}
      <Sequence from={0} durationInFrames={F(D.intro.t1) + 6}><Intro /></Sequence>
      <Sequence from={F(D.end.t0)} durationInFrames={F(D.total) - F(D.end.t0)}><BaseCtx.Provider value={F(D.end.t0)}><End /></BaseCtx.Provider></Sequence>
    </AbsoluteFill>
  );
};
