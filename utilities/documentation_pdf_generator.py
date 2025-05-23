#!/usr/bin/env python3
"""
Convert Methodology Document to PDF
==================================

This script converts the research methodology markdown document to PDF format
for presentation and documentation purposes using WeasyPrint.
"""

import markdown
from weasyprint import HTML, CSS
import os

def convert_markdown_to_pdf(markdown_file, output_pdf):
    """Convert markdown file to PDF using WeasyPrint"""
    
    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['tables', 'fenced_code', 'toc']
    )
    
    # Add CSS styling for better PDF appearance
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>ISB Fintech App Research Methodology</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Define CSS styles
    css_styles = CSS(string="""
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            color: #333;
            font-size: 11pt;
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            page-break-before: auto;
            page-break-after: avoid;
            font-size: 18pt;
        }
        
        h2 {
            color: #34495e;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
            page-break-before: auto;
            page-break-after: avoid;
            font-size: 16pt;
        }
        
        h3 {
            color: #7f8c8d;
            page-break-after: avoid;
            font-size: 14pt;
        }
        
        h4 {
            color: #95a5a6;
            page-break-after: avoid;
            font-size: 12pt;
        }
        
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }
        
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
            overflow-x: auto;
            font-size: 9pt;
            page-break-inside: avoid;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            page-break-inside: avoid;
            font-size: 10pt;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            margin: 0;
            padding: 0 15px;
            color: #777;
            font-style: italic;
        }
        
        p {
            margin-bottom: 10px;
            text-align: justify;
        }
        
        ul, ol {
            margin-bottom: 15px;
        }
        
        li {
            margin-bottom: 5px;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        /* Avoid breaking these elements */
        h1, h2, h3, h4, h5, h6 {
            page-break-after: avoid;
        }
        
        pre, blockquote, table {
            page-break-inside: avoid;
        }
    """)
    
    try:
        # Convert HTML to PDF using WeasyPrint
        html_doc = HTML(string=styled_html)
        html_doc.write_pdf(output_pdf, stylesheets=[css_styles])
        print(f"✅ Successfully converted {markdown_file} to {output_pdf}")
        return True
    except Exception as e:
        print(f"❌ Error converting to PDF: {e}")
        return False

def main():
    """Main conversion function"""
    
    # File paths
    methodology_md = "METHODOLOGY.md"
    methodology_pdf = "ISB_Fintech_Research_Methodology.pdf"
    
    project_summary_md = "PROJECT_SUMMARY.md"
    project_summary_pdf = "ISB_Fintech_Project_Summary.pdf"
    
    readme_md = "README.md"
    readme_pdf = "ISB_Fintech_Project_Documentation.pdf"
    
    print("🔄 Converting documentation to PDF format...")
    print("=" * 50)
    
    # Convert methodology document
    if os.path.exists(methodology_md):
        print(f"📄 Converting {methodology_md} to PDF...")
        if convert_markdown_to_pdf(methodology_md, methodology_pdf):
            print(f"   ✅ Created: {methodology_pdf}")
        print()
    else:
        print(f"❌ {methodology_md} not found")
    
    # Convert project summary
    if os.path.exists(project_summary_md):
        print(f"📄 Converting {project_summary_md} to PDF...")
        if convert_markdown_to_pdf(project_summary_md, project_summary_pdf):
            print(f"   ✅ Created: {project_summary_pdf}")
        print()
    else:
        print(f"❌ {project_summary_md} not found")
    
    # Convert README
    if os.path.exists(readme_md):
        print(f"📄 Converting {readme_md} to PDF...")
        if convert_markdown_to_pdf(readme_md, readme_pdf):
            print(f"   ✅ Created: {readme_pdf}")
        print()
    else:
        print(f"❌ {readme_md} not found")
    
    print("=" * 50)
    print("🎉 PDF conversion completed!")
    print("\nGenerated documentation:")
    for pdf_file in [methodology_pdf, project_summary_pdf, readme_pdf]:
        if os.path.exists(pdf_file):
            size = os.path.getsize(pdf_file) / 1024  # Size in KB
            print(f"   📋 {pdf_file} ({size:.1f} KB)")

if __name__ == "__main__":
    main() 