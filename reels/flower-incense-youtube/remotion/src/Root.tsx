import React from "react";
import { Composition } from "remotion";
import { Sample15 } from "./Sample";
import { GlassSample } from "./GlassSample";

export const Root: React.FC = () => (
  <>
    <Composition id="GlassSample" component={GlassSample} durationInFrames={450} fps={30} width={1920} height={1080} />
    <Composition id="Sample15" component={Sample15} durationInFrames={450} fps={30} width={1920} height={1080} />
  </>
);
