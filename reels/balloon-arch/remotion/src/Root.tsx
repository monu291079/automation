import React from "react";
import { Composition } from "remotion";
import { Reel } from "./Reel";
import TL from "./timeline.json";
export const Root: React.FC = () => (
  <Composition id="Balloon" component={Reel} durationInFrames={Math.round((TL as any).duration * 30)} fps={30} width={1080} height={1920} />
);
