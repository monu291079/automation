import { Easing, staticFile } from "remotion";

// IdeasPulse.in brand tokens (navy / gold / cream / teal). Fonts are local files so renders never need the network.
export const C = {
  bg: "#12213A", bg2: "#0B1526", card: "#172A49",
  ink: "#FAF9F5", inkSoft: "#B9C2D3",
  brand: "#E2BE6A", brandSoft: "#F6E2A6", brandLine: "#A9812E",
  teal: "#218C87", tealLight: "#39C2BA",
  success: "#39C2BA", warning: "#FF8A4C", danger: "#FF5A2C", dusk: "#9DB8FF",
};
export const BRAND_GRADIENT = "linear-gradient(180deg, #F6E2A6 0%, #E2BE6A 50%, #A9812E 100%)";
export const FONT_CSS = `
@font-face { font-family: 'Anton'; src: url(${staticFile("fonts/Anton-Regular.ttf")}); }
@font-face { font-family: 'Poppins'; font-weight: 800; src: url(${staticFile("fonts/Poppins-ExtraBold.ttf")}); }
@font-face { font-family: 'Poppins'; font-weight: 900; src: url(${staticFile("fonts/Poppins-Black.ttf")}); }`;
export const FONT = {
  display: "Anton, 'Noto Color Emoji', sans-serif",
  sans: "Poppins, 'Noto Color Emoji', sans-serif",
  sansAlt: "Poppins, sans-serif",
  mono: "ui-monospace, Menlo, monospace",
};
export const INTER = FONT.sans; export const MONTSERRAT = FONT.sansAlt;
export const MOTION = {
  cinematic: Easing.bezier(0.65, 0, 0.35, 1), easeIn: Easing.in(Easing.cubic), easeOut: Easing.out(Easing.cubic),
  spring: { snappy: { damping: 14, stiffness: 150 }, gentle: { damping: 18, stiffness: 100 }, bouncy: { damping: 10, stiffness: 200 }, settle: { damping: 22, stiffness: 70 } },
};
export const MUSIC = { bpm: 84, audioStartFrom: 0, audioVolume: 0.75 };
export const FRAMES_PER_BAR = Math.round((60 / MUSIC.bpm) * 4 * 30);
export const FRAMES_PER_PHRASE = FRAMES_PER_BAR * 4;
