# Visual and embedding specification

## Generation card template

```text
Question: full heading
Interview intent: capability being tested
Core conclusions: the minimum facts needed to explain what happens and why it matters
Misconception/boundary: the most dangerous wrong answer
Visual grammar: decomposition / flow / comparison / cause-effect / architecture / storyboard
Composition: panels, central diagram, and arrow directions
Display title: semantic title, not the full question
Exact text: title, 6–12 labels/short phrases, and one memory conclusion
Memory anchor: one sentence the reader can retell
```

## Default visual system

- Use a 16:9 landscape scientific-education anime knowledge card.
- Use a deep navy background with bright cyan for the main path and warm yellow for boundaries, warnings, or decisions.
- Use crisp panel borders, arrows, icons, and generous spacing.
- Show one small recurring AI learning guide; keep the character under roughly 20% of the composition.
- Prefer one dominant relationship plus 2–3 explanatory blocks over a crowded encyclopedia layout.
- Use large, short Chinese labels plus established English technical terms where needed.
- Use an explanatory middle density: enough short text to explain arrows, choices, and consequences, but no paragraphs, code, exhaustive lists, or tiny dashboard copy.
- Organize a reading ladder: semantic title → main mechanism → 2–3 explanation blocks → memory strip.
- When content is complex, encode at least half the meaning with layout, icons, arrows, color, and contrast; keep secondary details in Markdown.
- Reserve a consistent bottom strip inside the image for `记忆：` plus one large, short conclusion (normally 14–26 Chinese characters).
- Every embedded image must also be followed by one complementary `🧠 图解记忆` sentence in Markdown.
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
Text (verbatim): "<semantic title>", "<6–12 labels or short explanatory phrases>", "记忆：<complete high-level conclusion>"
Constraints: one dominant relationship; 2–3 explanatory blocks plus a bottom memory strip; all essential text exact and readable; correct arrow direction; character secondary to diagram; no invented facts; no logos; no watermark
Avoid: answer paragraphs, code, exhaustive bullet lists, unexplained noun-only arrows, decorative-only scene, dense dashboard copy, tiny labels, photorealism, unrelated UI chrome
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

The Markdown memory anchor is required in addition to the image's bottom memory strip. It should expand the conclusion with the decisive mechanism or tradeoff; do not merely repeat the question title.

## Output checks

- WebP, 16:9, no broken transparency, typically 1672×941 or another consistent landscape size.
- Prefer `cwebp -q 82`; lower quality gradually only when needed to meet 250 KB.
- Verify the rendered image after conversion, not only the source PNG.
- Inspect at a 760-pixel display width. Reject and simplify if any essential label needs zooming.
- Apply the three-second topic test and the 30-second retell test before embedding.
- Also run the **why test**: a reader must be able to explain why the shown mechanism, metric, or design choice matters. If not, add one concise explanatory phrase rather than more decorative elements.
- Keep `alt` semantically useful; do not use bare `Q1 illustration` text.
