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
   - 2–4 visible core conclusions;
   - one misconception or boundary to correct;
   - visual grammar: decomposition, flow, comparison, cause/effect, architecture, or storyboard;
   - exact short labels;
   - one retellable memory anchor.
4. Draft the composition from the knowledge relationship. Keep the recurring anime guide smaller than the technical diagram. Do not turn the card into a character poster.
5. Generate each image separately. For large batches, parallelize at most five calls at a time, but never ask one call to produce multiple unrelated question cards. Persist every completed batch before starting the next one so a stalled call is recoverable.
6. Inspect every output with `view_image`. Verify text, arrows, formulas, numbers, causality, scope, and mobile readability. Edit or regenerate any failed card before using it.
7. Copy the accepted output into the repository, convert to WebP, preserve aspect ratio, and target at most 250 KB unless the project specifies otherwise.
8. Embed the image directly after its question heading with an accurate alt description, clickable original, and one-sentence memory anchor.
9. Run the project content audit plus `scripts/audit_question_illustrations.py`. Fix missing references, mismatched filenames, duplicate mappings, oversized assets, and unillustrated questions.

## Quality Gate

Reject a card when any condition is true:

- it was inferred from the title without reading the answer;
- it only repeats the question or uses unrelated decorative imagery;
- covering the answer leaves the reader unable to retell the core relationship;
- a conditional tradeoff is drawn as an absolute rule;
- labels, formulas, arrows, quantities, or component roles conflict with the answer;
- the anime character competes with the knowledge structure;
- text is too dense or too small for a GitHub README;
- the file is not embedded, linked, compressed, or discoverable by the audit.

## Project Adaptation

Read `references/visual-spec.md` before generating. Treat it as the default for this repository. When another repository already has a coherent style, preserve that style while keeping the same reasoning and quality gates.

Use stable semantic filenames such as `qNN-short-topic.webp`. If numbering is duplicated or malformed, resolve the content identity before generating; never silently map two questions to one asset.

For this repository, use the HTML embedding block documented in `references/visual-spec.md` and run `python3 scripts/content_audit.py` after the illustration audit.
