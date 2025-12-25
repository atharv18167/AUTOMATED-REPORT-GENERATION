import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet

# Step 1: Read CSV
df = pd.read_csv("data.csv")

# Step 2: Basic analysis
summary = df.describe()
department_counts = df['Department'].value_counts()

# Step 3: Create a bar chart for department counts
plt.figure(figsize=(5, 4))
department_counts.plot(kind='bar', color='skyblue')
plt.title("Employees per Department")
plt.xlabel("Department")
plt.ylabel("Count")
plt.tight_layout()
chart_path = "department_chart.png"
plt.savefig(chart_path)
plt.close()

# Step 4: Build PDF
pdf_path = "sample_report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)

styles = getSampleStyleSheet()
story = []

# Title
title = Paragraph("<b>Employee Data Analysis Report</b>", styles['Title'])
story.append(title)
story.append(Spacer(1, 20))

# Summary paragraph
intro = Paragraph(
    "This report provides a basic analysis of the employee dataset, including summary statistics "
    "and department distribution.", 
    styles['BodyText']
)
story.append(intro)
story.append(Spacer(1, 20))

# Table: Key statistics
summary_table = summary.round(2).reset_index()
summary_table_data = [summary_table.columns.tolist()] + summary_table.values.tolist()

table = Table(summary_table_data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER')
]))
story.append(table)
story.append(Spacer(1, 20))

# Insert chart
img = Image(chart_path, width=300, height=250)
story.append(img)
story.append(Spacer(1, 20))



# Generate PDF
doc.build(story)

print("PDF report generated successfully:", pdf_path)
