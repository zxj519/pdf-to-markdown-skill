import re
import sys
import argparse

def clean_pdf_markdown(input_path, output_path, book_title=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    cleaned_lines = []
    prev_line = ""
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        repeated_title = book_title and stripped.upper() == book_title.upper() and len(stripped) < 50
        heading_repeated_title = stripped.upper().startswith('# ' + book_title.upper()) if book_title else False
        if repeated_title or heading_repeated_title:
            continue
        
        standalone_page_number = re.match(r'^\d+$', stripped) or re.match(r'^\d+\s+\d+$', stripped)
        if standalone_page_number:
            continue
        
        promo_patterns = [
            r'More Free eBooks',
            r'getfreeebooks',
            r'www\.\S+\.com',
            r'^\s*Page \d+ of \d+',
            r'^\s*Copyright \d+',
            r'^\s*All rights reserved',
        ]
        if any(re.search(p, stripped, re.IGNORECASE) for p in promo_patterns):
            continue
        
        dot_leader_match = re.search(r'\.{5,}\s*\.?\d+', stripped)
        if dot_leader_match:
            text_part = re.split(r'\.{3,}', stripped)[0].strip()
            if len(text_part) > 5:
                cleaned_lines.append(text_part)
            continue
        
        prev_ends_with_punctuation = prev_line and any(prev_line.endswith(c) for c in ('.', '!', '?', ':', ';', '-', '—'))
        prev_ends_with_uppercase_word = prev_line and len(prev_line.split()[-1]) > 2 and prev_line.split()[-1][0].isupper() if prev_line else False
        current_starts_lowercase = stripped and stripped[0].islower()
        likely_continuation = (prev_line and 
            not prev_ends_with_punctuation and
            len(prev_line) > 20 and
            stripped and
            (current_starts_lowercase or 
             (len(stripped) < 40 and prev_ends_with_uppercase_word)))
        
        if likely_continuation:
            cleaned_lines[-1] = prev_line + ' ' + stripped
            prev_line = cleaned_lines[-1]
            continue
        
        hyphenated_continuation = prev_line.endswith('-') and stripped and stripped[0].islower()
        if hyphenated_continuation:
            cleaned_lines[-1] = prev_line[:-1] + stripped
            prev_line = cleaned_lines[-1]
            continue
        
        cleaned_lines.append(stripped)
        prev_line = stripped
    
    final_lines = []
    blank_count = 0
    for line in cleaned_lines:
        if line == '':
            blank_count += 1
            if blank_count <= 1:
                final_lines.append(line)
        else:
            blank_count = 0
            final_lines.append(line)
    
    result = '\n'.join(final_lines)
    result = re.sub(r' +', ' ', result)
    result = re.sub(r'\n{4,}', '\n\n\n', result)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    removed = len(lines) - len(final_lines)
    print(f"Cleaned: {len(lines)} → {len(final_lines)} lines ({removed} removed)")
    print(f"Output saved to: {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean up PDF-to-markdown output')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', help='Output markdown file')
    parser.add_argument('--title', help='Book title to remove from repeated headers')
    args = parser.parse_args()
    
    clean_pdf_markdown(args.input, args.output, args.title)
