from fpdf import FPDF
import os

LOG_FILE = "audit.log"
REPORT_FILE = "audit_report.pdf"

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, "Windows Audit Report", ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f"Page {self.page_no()}", align='C')

def split_long_line(text, max_length=100):
    """Split very long words that would break the PDF."""
    words = []
    for word in text.split():
        while len(word) > max_length:
            words.append(word[:max_length])
            word = word[max_length:]
        words.append(word)
    return ' '.join(words)

def generate_pdf_report():
    if not os.path.exists(LOG_FILE):
        print("No audit.log file found to create report.")
        return

    pdf = PDF()
    pdf.add_page()

    try:
        pdf.add_font('ArialUnicode', '', 'C:\\Windows\\Fonts\\arial.ttf', uni=True)
        pdf.set_font("ArialUnicode", size=11)
    except Exception:
        pdf.set_font("Arial", size=11)

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                safe_line = split_long_line(line, max_length=80)
                pdf.multi_cell(0, 8, safe_line)

    pdf.output(REPORT_FILE)
    print(f"PDF report generated: {REPORT_FILE}")