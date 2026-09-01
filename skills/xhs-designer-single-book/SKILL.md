---
name: xhs-designer-single-book
description: Create or revise one production-ready six-card Xiaohongshu post about one verified book by or about one designer, architect, artist, or design theorist. Use for requests that name a designer and one book, ask to select that designer's theory-oriented book, or require sourced Chinese editorial copy, 3:4 JPG cards, preview, and image credits. This skill is deliberately limited to a single book and excludes magazines, multi-book comparisons, and generic batch layouts.
---

# Xiaohongshu Designer Single Book

Turn one designer's one book into a coherent Chinese visual argument, not a summary slideshow. Deliver a sourced six-card package quickly while keeping the opening and closing cards specific to the book.

## Hard Scope

- Handle exactly one designer or design thinker and one book.
- If only a person is given, choose one theory-heavy, interview, archive, manifesto, or method-focused book. Avoid picture-led complete works unless explicitly requested.
- If a book is given, verify the exact title, author/editor, publisher, year, edition, and real cover before writing.
- Do not use this skill for magazines, several books, rankings, or designer comparisons.

## Output Contract

Create one output directory containing:

```text
01.jpg ... 06.jpg
preview.jpg
发布文案.md
图片来源.md
post.json
```

Cards must be 1242 x 1660 px, RGB, 3:4 JPG, quality 95. Use Chinese text rendered by code; never ask an image model to render readable card text.

## Workflow

### 1. Establish the Book Argument

Research only enough to lock:

1. exact bibliographic identity and cover;
2. one debatable thesis that can be explained in one Chinese sentence;
3. four distinct cases, drawings, projects, passages, or archival artifacts that test the thesis;
4. one concept chain and three transferable methods for the closing card.

Prefer primary and institutional sources. Clearly label editorial inference and paraphrase; do not present either as a quotation. Read [references/editorial-and-layout.md](references/editorial-and-layout.md) before outlining the cards.

### 2. Build a Six-Card Narrative

Use these page responsibilities, not fixed compositions:

- **01 — Problem cover:** real book cover, designer/book identity, and the central question or thesis.
- **02 — Mechanism:** explain the book's main mechanism through the strongest first piece of evidence.
- **03 — Evidence:** test or complicate the mechanism with a second case.
- **04 — Evidence:** expose a contrast, limit, or operational detail with a third case.
- **05 — Evidence:** bring the thesis to a fourth case and prepare the conclusion.
- **06 — Synthesis:** concept chain, conclusion, and three methods a designer can reuse.

Cards 02–05 may share a coherent inner-page system. Cards 01 and 06 must be designed from the current book's argument.

### 3. Make 01 and 06 Book-Specific

Before rendering, write a two-line layout rationale for each end card. Change at least three major variables from the most recent package or any default skeleton:

- image-to-text ratio;
- whitespace direction;
- cover scale, crop, angle, or position;
- title axis or reading path;
- concept-chain geometry;
- takeaway grouping;
- background, rule system, or dominant color behavior.

Do not solve 01 by merely swapping a cover into a standard frame. Do not solve 06 with a permanent three-column checklist. The layout must express the book's specific logic—for example sequence, threshold, archive, construction, light, color, or dialogue. Record the two rationales in `post.json`.

### 4. Source and Prepare Images

Use this order: official designer/foundation/publisher; institution or museum; Wikimedia Commons; other verifiable source. Keep photographs legible and do not place decorative rules over the subject. Preserve the real cover artwork; only crop outer whitespace or scale it without altering its typography.

Read [references/sources-and-qa.md](references/sources-and-qa.md). Record every asset as:

```text
filename | depicted content | author/institution | source URL | license/copyright | modifications
```

### 5. Scaffold and Render

Start the package with:

```powershell
python scripts/scaffold_single_book.py <output-directory> --designer "..." --book "..."
```

Create a project-specific Pillow renderer in the output or working directory. Import shared geometry, type, crop, fitting, and preview helpers from `scripts/render_utils.py`; do not turn that utility into a fixed card template. Derive the palette and graphic behavior from the book's content, not superficial imitation of the designer.

Write `发布文案.md` with a title around 20 Chinese characters, 300–500 Chinese characters of body copy, and 6–10 useful tags. Keep the argument clear enough to publish without the images.

### 6. Verify

Run:

```powershell
python scripts/validate_single_book.py <output-directory>
```

Then inspect `preview.jpg` at normal viewing size and check:

- text is readable and no line is clipped;
- all four evidence images are distinct and correctly described;
- the cover is genuine and not distorted;
- 01 and 06 visibly differ in structure from one another and from the previous package;
- attribution, rights status, paraphrase, and editorial inference are explicit.

Fix all errors before delivery. Treat validator warnings as editorial review items, not permission to skip them.

## Token-Efficient Operating Rules

- Research bibliography, thesis, cases, and image rights in one bounded pass.
- Keep one compact `post.json` as the source of truth; do not rewrite the same notes in several files.
- Reuse `render_utils.py` for mechanics, but write only the page-specific composition code needed for the current book.
- Inspect the six-card preview first; open individual cards only where the preview reveals a problem.
- Revise locally: if only 01 and 06 are wrong, rerender only those cards and rebuild the preview.

## Resources

- [references/editorial-and-layout.md](references/editorial-and-layout.md): argument selection, six-card pacing, and non-fixed end-card rules.
- [references/sources-and-qa.md](references/sources-and-qa.md): sourcing, rights records, copy, and visual QA.
- `scripts/scaffold_single_book.py`: create the minimum package skeleton.
- `scripts/render_utils.py`: shared Pillow helpers without a prescribed layout.
- `scripts/validate_single_book.py`: validate the finished package.
