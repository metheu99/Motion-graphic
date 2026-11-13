# Motion-graphic

## tesla-y — Model Y 30s spec ad

A 30-second, 16:9 (1920×1080, 30 fps) kinetic-typography motion graphic, built with [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP rendered to video).

- Video: [`tesla-y/tesla-model-y-30s.mp4`](tesla-y/tesla-model-y-30s.mp4)
- Composition: [`tesla-y/index.html`](tesla-y/index.html)
- Music: synthesized from code, [`tesla-y/scripts/bgm.py`](tesla-y/scripts/bgm.py) (120 BPM)
- Voiceover: Kokoro TTS (`am_michael`)

| Time | Scene |
| --- | --- |
| 0–3.75 s | "THE FUTURE / isn't coming —" on a grid |
| 3.75–7.5 s | Hero image, "IT'S HERE." |
| 7.5–15 s | Cuts on the beat: ELECTRIC · INTELLIGENT · FEARLESS · LIMITLESS |
| 15–22.5 s | Drop: AWD PERFORMANCE, 5★ SAFETY |
| 22.5–27.5 s | MODEL Y title + VO |
| 27.5–30 s | TESLA end card + mission statement VO |

Re-render:

```bash
cd tesla-y
npx hyperframes render -o tesla-model-y-30s.mp4
```

> Unofficial spec/portfolio work, not affiliated with or endorsed by Tesla, Inc. Vehicle images are from tesla.com and remain the property of Tesla, Inc.
