#!/usr/bin/env python3
"""Fast PDF generator for the novella."""
import re, os
from fpdf import FPDF

script_dir = os.path.dirname(os.path.abspath(__file__))
md_path = os.path.join(script_dir, 'what_the_river_remembers.md')
pdf_path = os.path.join(script_dir, 'What_The_River_Remembers.pdf')

with open(md_path, 'r') as f:
    md = f.read()

pdf = FPDF('P', 'mm', 'A5')
pdf.set_auto_page_break(True, 20)
pdf.set_margins(18, 20, 18)

# Title page
pdf.add_page()
pdf.set_font('Times', 'B', 24)
pdf.ln(50)
pdf.cell(0, 14, 'What the River Remembers', align='C')
pdf.ln(20)
pdf.set_font('Times', 'I', 13)
pdf.cell(0, 10, 'A Novella', align='C')
pdf.ln(40)
pdf.set_font('Times', 'I', 11)
pdf.cell(0, 6, 'For those who loved across the wreckage of the world,', align='C')
pdf.ln(6)
pdf.cell(0, 6, 'and for the children born of silence.', align='C')

def clean(text):
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    reps = {
        '\u201c': '"', '\u201d': '"', '\u2018': "'", '\u2019': "'",
        '\u2014': '--', '\u2013': '-', '\u2026': '...', '\u2726': '*',
        '\u0142': 'l', '\u0141': 'L',
    }
    for old, new in reps.items():
        text = text.replace(old, new)
    return text.encode('latin-1', errors='replace').decode('latin-1')

nums = {'ONE':'I','TWO':'II','THREE':'III','FOUR':'IV','FIVE':'V',
        'SIX':'VI','SEVEN':'VII','EIGHT':'VIII','NINE':'IX','TEN':'X'}

lines = md.split('\n')
i = 0
skipping = True

while i < len(lines):
    line = lines[i].strip()
    
    if skipping:
        if (line.startswith('#') or line == '---' or 
            line.startswith('*For') or line.startswith('*and')):
            i += 1
            continue
        skipping = False
    
    if line.startswith('## CHAPTER'):
        num = nums.get(line.replace('## CHAPTER','').strip(), '')
        i += 1
        sub = ''
        if i < len(lines) and lines[i].strip().startswith('### '):
            sub = clean(lines[i].strip()[4:])
            i += 1
        pdf.add_page()
        pdf.ln(30)
        pdf.set_font('Times', 'B', 20)
        pdf.cell(0, 12, 'CHAPTER ' + num, align='C')
        pdf.ln(14)
        if sub:
            pdf.set_font('Times', 'I', 14)
            pdf.cell(0, 10, sub, align='C')
            pdf.ln(12)
        else:
            pdf.ln(10)
        continue
    
    if line == '## EPILOGUE':
        pdf.add_page()
        pdf.ln(30)
        pdf.set_font('Times', 'I', 18)
        pdf.cell(0, 12, 'Epilogue', align='C')
        pdf.ln(14)
        i += 1
        continue
    
    if line == '*FIN*':
        pdf.ln(20)
        pdf.set_font('Times', 'B', 16)
        pdf.cell(0, 12, 'FIN', align='C')
        i += 1
        continue
    
    if line == '---':
        pdf.ln(4)
        pdf.set_font('Times', '', 12)
        pdf.cell(0, 8, '* * *', align='C')
        pdf.ln(4)
        i += 1
        continue
    
    if not line:
        i += 1
        continue
    
    para = []
    while i < len(lines):
        c = lines[i].strip()
        if not c or c.startswith('#') or c == '---' or c == '*FIN*':
            break
        para.append(c)
        i += 1
    
    if para:
        text = clean(' '.join(para))
        pdf.set_font('Times', '', 10)
        pdf.set_x(18)
        pdf.multi_cell(pdf.w - 36, 5, text)
        pdf.ln(1)

pdf.output(pdf_path)
sz = os.path.getsize(pdf_path)
print(f'PDF created: {pdf_path} ({sz//1024} KB)')
