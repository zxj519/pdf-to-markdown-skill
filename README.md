# PDF to Markdown Skill

An [OpenCode](https://github.com/zxj519/oh-my-opencode) skill for converting PDF files to clean, structured Markdown.

## What it does

Converts PDF documents (books, articles, reports, product docs) into editable Markdown using [Nutrient's pdf-to-markdown CLI](https://github.com/PSPDFKit/pdf-to-markdown). Handles installation, conversion, and automated cleanup of noise like headers, footers, page numbers, and broken paragraphs.

## Installation

```bash
# Clone into your OpenCode skills directory
git clone https://github.com/zxj519/pdf-to-markdown-skill.git ~/.agents/skills/pdf-to-markdown
```

Or download the packaged `.skill` file from [Releases](https://github.com/zxj519/pdf-to-markdown-skill/releases).

## How it works

### 1. Tool Installation Check
Verifies `@pspdfkit/pdf-to-markdown` is available via `npx`. Installs globally if missing.

### 2. PDF Conversion
Runs Nutrient CLI to extract structured Markdown (headings, paragraphs, lists) from the PDF.

### 3. Automated Cleanup
- **Large files (>500 lines)**: Uses bundled `scripts/cleanup.py` for fast batch processing
- **Small files**: Stream editing with `sed`

Cleanup removes:
- Repeated page headers/footers
- Standalone page numbers
- Promotional watermarks (e.g., "More Free eBooks")
- Dot-leader TOC entries
- Broken mid-sentence paragraphs
- Excessive blank lines

### 4. Structure Verification
Checks heading hierarchy, paragraph continuity, and list formatting.

## File Structure

```
pdf-to-markdown/
├── SKILL.md              # Skill instructions and workflow
├── scripts/
│   └── cleanup.py        # Automated cleanup for large files
└── evals/
    └── evals.json        # Test cases and evaluation prompts
```

## Evaluation Results

| Eval | With Skill | Without Skill |
|---|---|---|
| PDF conversion (55-page book) | **83%** pass rate, 1342 structured lines | 50% pass rate, 215 flat text lines |
| Cleanup (100-line excerpt) | **83%** pass rate, TOC preserved as list | 60% pass rate, TOC deleted |
| Tool installation | **100%** | 100% |

**Key finding**: The skill directs agents to use the proper Nutrient CLI instead of generic Python libraries, producing significantly better structured output. The bundled cleanup script prevents timeouts on large files.

## Example Usage

```bash
# Convert a PDF book
npx @pspdfkit/pdf-to-markdown book.pdf > book_raw.md

# Clean up the output
python3 ~/.agents/skills/pdf-to-markdown/scripts/cleanup.py book_raw.md book_clean.md --title "Book Title"
```

## Limitations

- Text only — no images extracted
- Complex tables may need manual reformatting
- Scanned PDFs without OCR produce no output
- Very large PDFs (>100MB) may need splitting

## License

This skill (scripts, documentation, and metadata) is licensed under the MIT License.

**However**, this skill relies on `@pspdfkit/pdf-to-markdown` (Nutrient CLI), which is **proprietary software** licensed under the [Nutrient Free Use License](https://raw.githubusercontent.com/PSPDFKit/pdf-to-markdown/refs/heads/main/LICENSE.md). Key restrictions:

- Free use: up to 1,000 documents/month
- Commercial use beyond that requires a paid license from Nutrient
- You may not use it to compete with Nutrient's offerings

By using this skill, you are responsible for complying with Nutrient's license terms.
