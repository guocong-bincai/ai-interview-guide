---
name: illustrate-ai-interview-questions
description: Create, review, compress, and embed memory-focused educational illustrations for AI interview questions in Markdown repositories. Use when Codex is asked to 给面试题生成图片、补齐题目插画、制作图文面经、把技术问答画成动漫知识图, or audit whether every interview question has a correct matching illustration. Read the full answer before drawing; convert definitions, mechanisms, tradeoffs, boundaries, and common mistakes into a visual that helps candidates retell the answer.
---

# Illustrate AI Interview Questions

Create illustrations that teach the answer rather than decorate the heading. Use the built-in `imagegen` skill for every raster asset and issue one generation call per distinct question.

## Workflow

1. Inspect repository instructions, existing illustration style, question headings, answer boundaries, asset paths, and audit scripts. Discover real module paths from the filesystem; never infer a directory name from its display title or number.
2. Read each complete question and answer, including code, tables, caveats, examples, engineering tradeoffs, and follow-up questions.
3. Write an internal generation card with:
   - exact question;
   - interview intent in one sentence;
   - one dominant knowledge relationship;
   - 2–4 core conclusions, then select the minimum set that explains both **what happens** and **why it matters**;
   - one misconception or boundary to correct;
   - visual grammar: decomposition, flow, comparison, cause/effect, architecture, or storyboard;
   - a semantic display title shorter than the original question;
   - exact labels and short explanatory phrases within the information-density guidance below;
   - one retellable memory anchor.
4. Draft the composition from the knowledge relationship. Prefer objects, spatial grouping, arrows, color, scale, and contrast over explanatory prose. Keep the recurring anime guide smaller than the technical diagram. Do not turn the card into a character poster.
5. Generate each image separately. For large batches, parallelize at most five calls at a time, but never ask one call to produce multiple unrelated question cards. Persist every completed batch before starting the next one so a stalled call is recoverable.
6. Inspect every output with `view_image`. Verify text, arrows, formulas, numbers, causality, scope, and mobile readability. Edit or regenerate any failed card before using it.
7. Copy the accepted output into the repository, convert to WebP, preserve aspect ratio, and target at most 250 KB unless the project specifies otherwise.
8. Embed the image directly after its question heading with an accurate alt description, clickable original, and one-sentence memory anchor.
9. Run the project content audit plus `scripts/audit_question_illustrations.py`. Fix missing references, mismatched filenames, duplicate mappings, oversized assets, and unillustrated questions.

## Quality Gate

### Information-density guidance

The image must be understandable without becoming a compressed answer sheet. Optimize for an **explanatory middle density**, not minimum text. A good card normally contains:

- one semantic title that names the tested concept, not necessarily the full long question;
- one dominant mechanism, comparison, decision, or pipeline;
- 2–3 explanatory blocks that answer the reader's likely follow-ups: `是什么 / 怎么做 / 为什么 / 何时选`;
- each explanatory block has a short heading plus one concise supporting phrase; use icons and diagrams to carry at least half of the meaning;
- usually 6–12 meaningful labels across the whole card; allow more only for a comparison or architecture whose parts cannot be understood otherwise;
- one mandatory bottom memory strip inside the image, using a complete, retellable conclusion rather than a slogan;
- one complementary retellable memory anchor as a separate Markdown line below the image;
- move code, long examples, exhaustive lists, minor caveats, detailed metrics, and API syntax back to the Markdown answer.

Use a visual reading ladder:

1. **Title:** identify the topic.
2. **Main diagram:** show the core relationship.
3. **Explanation blocks:** make the arrows, differences, or choices understandable.
4. **Memory strip:** turn the entire image into one answerable interview conclusion.

Prefer short explanatory phrases such as `共享语义空间`, `任务决定指标`, or `只训练连接层`. Avoid both extremes: isolated nouns with unexplained arrows, and dense paragraphs that require zooming.

Run two readability tests after rendering:

1. **Three-second test:** at README width, can a reader identify the topic and main relationship in three seconds?
2. **Retell test:** after hiding the image, can the reader state the answer's conclusion and 2–3 supporting points in about 30 seconds?

If the three-second test fails, simplify the visual hierarchy before making fonts smaller. If the retell test fails, first add or improve a short explanatory block; add prose only when the diagram alone cannot convey causality or a tradeoff.

Both memory layers are mandatory:

1. **Inside the image:** reserve a visually consistent bottom strip, roughly 10–14% of the card height, labeled `记忆：`. Use one complete conclusion that answers the question at a high level. It may combine 2–3 clauses with `·`, `→`, or `≠`, but must remain readable at README width.
2. **Below the image:** write one concise `🧠 图解记忆` sentence that expands the visual conclusion into a usable interview answer. Keep this text searchable, selectable, and easy to revise.

Do not count the bottom memory strip as an extra visual zone. Reduce labels elsewhere before shrinking the memory-strip text.

Reject a card when any condition is true:

- it was inferred from the title without reading the answer;
- it only repeats the question or uses unrelated decorative imagery;
- it reproduces answer paragraphs, code, or an exhaustive checklist;
- it is so sparse that the reader sees objects and arrows but cannot explain their meaning;
- covering the answer leaves the reader unable to retell the core relationship;
- a conditional tradeoff is drawn as an absolute rule;
- labels, formulas, arrows, quantities, or component roles conflict with the answer;
- the anime character competes with the knowledge structure;
- essential text becomes too small at a 760-pixel README width, or the hierarchy is unclear;
- the file is not embedded, linked, compressed, or discoverable by the audit.

## Project Adaptation

Read `references/visual-spec.md` before generating. Treat it as the default for this repository. When another repository already has a coherent style, preserve that style while keeping the same reasoning and quality gates.

Use stable semantic filenames such as `qNN-short-topic.webp`. If numbering is duplicated or malformed, resolve the content identity before generating; never silently map two questions to one asset.

For this repository, use the HTML embedding block documented in `references/visual-spec.md` and run `python3 scripts/content_audit.py` after the illustration audit.
