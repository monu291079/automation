# Wan 2.1 text-to-video clip pack: Flower Incense YouTube video (16:9)

These clips fill the shots that the 5 still images don't cover. Generate them on the local PC (RTX 5060 Ti 16 GB) with the Wan 2.1 setup already installed in ComfyUI.

## Settings (16 GB VRAM)
- Model: Wan 2.1 **T2V 14B (fp8 or GGUF Q5/Q6)** if it is installed. Otherwise **T2V 1.3B** (faster, a little less detail).
- Resolution: **832 × 480** (16:9). The edit upscales to 1080p.
- Length: **81 frames @ 16 fps** (about 5 s)
- Steps: 25–30, CFG: 5–6, sampler: uni_pc or euler, shift: 5 (8 for 1.3B)
- Seed: random; keep the seed of any good result
- Negative prompt (all clips):
  `blurry, low quality, jpeg artifacts, distorted hands, extra fingers, deformed, text, letters, watermark, logo, subtitles, cartoon, anime, cgi, oversaturated, flicker, morphing objects, face close-up`
- Save as **MP4 (h264)** with exactly the file names below, into one folder `wan_clips/`.

Style suffix for every prompt (already added below): *cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion*.

## Clips (priority order: make 1–8 first)

| # | File name | Used in | Prompt |
|---|---|---|---|
| 1 | `01_temple_waste.mp4` | P1 hook: "shaam tak bas ek dher" | A heap of wilted marigold and rose offerings dumped beside an Indian temple wall at dusk, petals scattered on stone floor, a broom resting nearby, slow push-in, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 2 | `02_sorting_hands.mp4` | P3 Step 2: chhantai | Close-up of hands in blue gloves sorting fresh marigold and rose petals on a wooden table, removing plastic threads and foil into a separate bowl, top-down slow pan, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 3 | `03_sun_drying.mp4` | P3 Step 3: sukhana | Orange marigold and red rose petals spread thinly on a white cotton cloth drying in bright sunlight on a rooftop, gentle breeze moving petals, slow overhead drift, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 4 | `04_grinding.mp4` | P3 Step 4: peesna | Dried flower petals being ground into fine orange powder in a stone mortar and pestle, close-up, powder texture visible, slow dolly, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 5 | `05_sieving.mp4` | P3 Step 4: chhanna | Fine floral powder being sifted through a steel mesh sieve into a glass bowl, soft powder falling, close-up, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 6 | `06_cone_mould.mp4` | P3 Step 6: aakaar dena | Hands pressing brown floral paste into a metal cone mould and releasing neat incense cones onto a wooden tray, close-up, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 7 | `07_burn_test.mp4` | P3 Step 7: jalakar jaanch | A single handmade incense cone burning on a brass holder, thin smoke curling upward, glowing tip and soft ash, dark background, macro, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 8 | `08_packing.mp4` | P3 Step 8 + P5 | Hands filling kraft paper pouches with handmade incense cones and sealing them on a wooden desk, neat rows of pouches, slow pan, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 9 | `09_flower_market.mp4` | P6: phool kahan se | Busy Indian flower market in early morning, baskets and heaps of marigold garlands and roses, vendors arranging flowers, slow tracking shot, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 10 | `10_puja_shop.mp4` | P6: bechna kahan | A small Indian puja items shop counter with shelves of incense packs, diyas and marigold garlands, a shopkeeper placing incense pouches on the counter, slow push-in, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 11 | `11_gift_box.mp4` | P2: festival gift pack | An elegant festive gift box opening to reveal incense cones, a small brass diya and marigold petals, Diwali lights bokeh in background, slow orbit, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |
| 12 | `12_safety_mask.mp4` | P8: suraksha | A person wearing a face mask and gloves mixing floral powder near an open window in a clean, well-ventilated home workshop, medium shot, no face close-up, cinematic, warm golden light, shallow depth of field, realistic, Indian setting, slow smooth camera motion |

## Tips
- If hands or objects morph, re-roll with a new seed or shorten to 49 frames.
- Wan cannot write readable text. All on-screen text is added in the edit.
- When done, send the `wan_clips/` MP4s back in this chat. They will be slotted into the planned scenes.
