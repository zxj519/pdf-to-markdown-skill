---
name: pdf-to-markdown
description: >
  Convert PDF files to clean Markdown using Nutrient's pdf-to-markdown CLI.
  Use this skill whenever the user needs to extract text from a PDF, convert
  a PDF document to markdown format, process book chapters or articles from
  PDF files, or transform any PDF content into editable markdown for a wiki
  or knowledge base. This skill handles installation, conversion, and cleanup
  of the output automatically.
---

# PDF to Markdown

Convert PDF documents into clean, readable Markdown files suitable for
ingestion into wikis, knowledge bases, or further editing.

## When to use

- Converting PDF books, articles, or reports to markdown
- Extracting text content from PDFs for wiki ingest workflows
- Processing scanned or digital PDFs into editable text
- Preparing PDF source material for LLM knowledge base construction

## Tool

This skill uses **Nutrient pdf-to-markdown** (`@pspdfkit/pdf-to-markdown`),
a Node.js CLI tool that converts PDF pages to Markdown with preserved
structure (headings, paragraphs, lists).

### Installation check

Before converting, check if the tool is available:

```bash
npx @pspdfkit/pdf-to-markdown --version 2>/dev/null || echo "not installed"
```

If not available, install it:

```bash
npm install -g @pspdfkit/pdf-to-markdown
```

Or use `npx` directly (slower on first run but no global install):

```bash
npx @pspdfkit/pdf-to-markdown input.pdf > output.md
```

## Conversion workflow

### 1. Validate input

- Confirm the PDF file exists and is readable
- Check file size (very large PDFs >100MB may need splitting)
- Note the approximate page count

### 2. Run conversion

```bash
npx @pspdfkit/pdf-to-markdown <input.pdf> > <output.md>
```

Or with explicit output path:

```bash
npx @pspdfkit/pdf-to-markdown <input.pdf> --output <output.md>
```

### 3. Clean up the output

The raw output often contains noise that should be removed:

- **Page headers/footers**: Repeated text like "Page X of Y", book title, copyright
- **Page numbers**: Standalone numbers between paragraphs
- **Watermark text**: "More Free eBooks" and similar promotional lines
- **Repeated publisher info**: Lines that appear on every page
- **Excessive blank lines**: More than 2 consecutive newlines
- **Broken paragraphs**: Mid-sentence line breaks that should be merged

For files larger than 500 lines, you MUST use the bundled cleanup script. Do NOT read the file line-by-line or attempt manual editing on large files — this will timeout.

```bash
python3 ~/.agents/skills/pdf-to-markdown/scripts/cleanup.py input.md output.md --title "Book Title"
```

The script handles: repeated headers, page numbers, promotional lines, dot-leader TOC entries, broken paragraph merging, hyphenated word fixes, and blank line compression.

For small files (< 500 lines) or fine-tuning after the script, use stream editing:

```bash
sed -i '' '/More Free eBooks/d' output.md
sed -i '' '/^BASS FISHING 101$/d' output.md
sed -i '' '/^[0-9][0-9]*$/d' output.md
```

### 4. Structure verification

After cleanup, verify:

- Headings use proper Markdown `#` hierarchy
- Paragraphs are continuous (not broken mid-sentence)
- Lists use `-` or `*` consistently
- Tables (if any) render reasonably
- Total line count roughly matches expected content density

### 5. Save to appropriate directory

Place the cleaned markdown in the correct `raw/` subdirectory:

- `raw/books/` for book chapters
- `raw/articles/` for articles or papers
- `raw/products/` for product documentation

Update `wiki/log.md` and `wiki/index.md` per the wiki's Ingest workflow.

## Example

**Input**: `raw/books/ebookbrassfishing.pdf` (55 pages, bass fishing book)

**Commands**:
```bash
cd /Users/zxj519/Documents/workspace/lure-wiki
npx @pspdfkit/pdf-to-markdown raw/books/ebookbrassfishing.pdf > raw/books/ebookbrassfishing.md
```

**Cleanup**: Remove repeated "BASS FISHING 101", page numbers, promotional lines.

**Output**: `raw/books/ebookbrassfishing.md` (clean, 3185 lines)

## Limitations

- Does not extract images (text only)
- Complex tables may need manual reformatting
- Scanned PDFs without OCR will produce no output
- Very large PDFs may require splitting or batching
- Mathematical formulas may not render correctly

## Alternative tools

If `@pspdfkit/pdf-to-markdown` fails or is unavailable:

1. **pdftotext** (poppler-utils): `pdftotext -layout input.pdf output.txt`
2. **pdfplumber** (Python): more control over layout preservation
3. **marker** (Python): newer high-quality PDF-to-markdown converter

Report the fallback tool used in the wiki log.
