# Visual and embedding specification

## Generation card template

```text
Question: full heading
Interview intent: capability being tested
Core conclusions: 2–4 facts that must appear
Misconception/boundary: the most dangerous wrong answer
Visual grammar: decomposition / flow / comparison / cause-effect / architecture / storyboard
Composition: panels, central diagram, and arrow directions
Exact labels: short labels only
Memory anchor: one sentence the reader can retell
```

## Default visual system

- Use a 16:9 landscape scientific-education anime knowledge card.
- Use a deep navy background with bright cyan for the main path and warm yellow for boundaries, warnings, or decisions.
- Use crisp panel borders, arrows, icons, and generous spacing.
- Show one small recurring AI learning guide; keep the character under roughly 20% of the composition.
- Prefer one dominant relationship over a crowded encyclopedia layout.
- Use large, short Chinese labels plus established English technical terms where needed.
- Do not add brand logos, QR codes, watermarks, fake citations, long paragraphs, or unsupported benchmark numbers.
- Render the title exactly once. Avoid tiny footer prose.

## Visual grammar selection

| Knowledge relationship | Preferred composition |
|---|---|
| definition and components | exploded/decomposition diagram |
| ordered mechanism | left-to-right flow or loop |
| similar concepts | balanced comparison panels |
| parameter changes outcome | cause/effect control panel |
| production components | architecture with trust boundaries |
| multi-step mitigation | storyboard or layered defense |
| tradeoff or selection | decision fork with conditions |

## Prompt skeleton

```text
Use case: scientific-educational
Asset type: AI interview question memory card
Primary request: visualize <the exact knowledge relationship>, so a candidate can retell the answer after seeing the image
Subject: <2–4 core conclusions and one boundary>
Style/medium: polished anime-infographic hybrid, crisp vector-like technical diagram
Composition/framing: 16:9 landscape, <selected visual grammar>, one small AI learning guide
Lighting/mood: deep navy technology classroom, bright cyan main flow, warm yellow warnings
Text (verbatim): "<title>", "<short label 1>", ...
Constraints: all labels exact and legible; correct arrow direction; character secondary to diagram; no extra text; no invented facts; no logos; no watermark
Avoid: decorative-only scene, dense paragraphs, tiny labels, photorealism, unrelated UI chrome
```

## README embedding

Place this block immediately after the question heading:

```html
<p align="center">
  <a href="../../assets/illustrations/<module>/<filename>.webp">
    <img src="../../assets/illustrations/<module>/<filename>.webp" width="760" alt="A precise description of the knowledge relationship shown">
  </a>
</p>
<p align="center"><sub>🧠 图解记忆：A retellable memory anchor; 点击图片可查看原图。</sub></p>
```

## Output checks

- WebP, 16:9, no broken transparency, typically 1672×941 or another consistent landscape size.
- Prefer `cwebp -q 82`; lower quality gradually only when needed to meet 250 KB.
- Verify the rendered image after conversion, not only the source PNG.
- Keep `alt` semantically useful; do not use bare `Q1 illustration` text.
