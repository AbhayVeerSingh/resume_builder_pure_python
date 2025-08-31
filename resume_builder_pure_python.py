import tkinter as tk
from tkinter import messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


# ---------------- PDF Generator ----------------
def generate_pdf(form_data, filename="resume.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    # Custom styles
    header_name = ParagraphStyle(name="HeaderName", fontSize=20, leading=24, textColor=colors.HexColor("#2C3E50"), spaceAfter=6)
    header_contact = ParagraphStyle(name="HeaderContact", fontSize=10, leading=12, alignment=2, textColor=colors.HexColor("#7F8C8D"))
    section_title = ParagraphStyle(name="SectionTitle", fontSize=12, leading=14, textColor=colors.HexColor("#1A5276"), spaceBefore=12, spaceAfter=6, underlineWidth=1, alignment=0, uppercase=True)
    normal_text = ParagraphStyle(name="NormalText", fontSize=10, leading=13)

    # ---- Header (Two Column) ----
    header_table = Table([
        [Paragraph(f"<b>{form_data['name']}</b>", header_name),
         Paragraph(f"{form_data['email']}<br/>{form_data['phone']}", header_contact)]
    ], colWidths=[300, 200])
    elements.append(header_table)
    elements.append(Spacer(1, 6))
    elements.append(Table([[""]], colWidths=[500], rowHeights=[1], style=[("LINEBELOW", (0,0), (-1,-1), 0.5, colors.grey)]))
    elements.append(Spacer(1, 12))

    # ---- Summary ----
    elements.append(Paragraph("Summary", section_title))
    elements.append(Paragraph(form_data['summary'], normal_text))
    elements.append(Spacer(1, 6))

    # ---- Education ----
    elements.append(Paragraph("Education", section_title))
    edu_data = [["Degree", "Institution", "Year", "Percentage"]] + form_data["education"]
    edu_table = Table(edu_data, colWidths=[120, 200, 80, 80])
    edu_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E86C1")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("BOTTOMPADDING", (0,0), (-1,0), 6)
    ]))
    elements.append(edu_table)
    elements.append(Spacer(1, 6))

    # ---- Experience ----
    elements.append(Paragraph("Experience", section_title))
    for job in form_data["experience"]:
        elements.append(Paragraph(f"<b>{job['role']}</b> – {job['company']} <i>({job['duration']})</i>", normal_text))
        bullet_points = [ListItem(Paragraph(p, normal_text)) for p in job["points"]]
        elements.append(ListFlowable(bullet_points, bulletType="bullet"))
        elements.append(Spacer(1, 4))

    # ---- Skills (Grid) ----
    elements.append(Paragraph("Skills", section_title))
    skill_list = [[s] for s in form_data["skills"]]
    skills_table = Table(skill_list, colWidths=[500/3]*3)
    skills_table.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#2C3E50")),
    ]))
    elements.append(skills_table)

    # Build PDF
    doc.build(elements)
    messagebox.showinfo("Success", f"Resume saved as {filename}")


# ---------------- Tkinter GUI ----------------
education_entries = []

def add_education():
    degree = entry_degree.get().strip()
    institution = entry_institution.get().strip()
    year = entry_year.get().strip()
    percentage = entry_percentage.get().strip()

    if degree and institution and year and percentage:
        education_entries.append([degree, institution, year, percentage])
        messagebox.showinfo("Added", f"Added: {degree}, {institution}, {year}, {percentage}")
        entry_degree.delete(0, tk.END)
        entry_institution.delete(0, tk.END)
        entry_year.delete(0, tk.END)
        entry_percentage.delete(0, tk.END)
    else:
        messagebox.showwarning("Missing Data", "Please fill all education fields before adding.")


def submit_form():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    summary = entry_summary.get("1.0", tk.END).strip()
    exp = entry_experience.get("1.0", tk.END).strip().split("\n")
    skills = entry_skills.get("1.0", tk.END).strip().split(",")

    # Convert experience (expected format: Role,Company,Duration,Point1;Point2;...)
    experience = []
    for e in exp:
        parts = e.split(",")
        if len(parts) >= 4:
            role = parts[0].strip()
            company = parts[1].strip()
            duration = parts[2].strip()
            points = [p.strip() for p in parts[3].split(";") if p.strip()]
            experience.append({"role": role, "company": company, "duration": duration, "points": points})

    form_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "summary": summary,
        "education": education_entries,  # from add_education()
        "experience": experience,
        "skills": [s.strip() for s in skills if s.strip()]
    }

    generate_pdf(form_data)


# ---------------- Main Window ----------------
root = tk.Tk()
root.title("Resume Builder")
root.geometry("650x750")

# Labels & Inputs
tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root, width=50)
entry_name.pack()

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root, width=50)
entry_email.pack()

tk.Label(root, text="Phone").pack()
entry_phone = tk.Entry(root, width=50)
entry_phone.pack()

tk.Label(root, text="Summary").pack()
entry_summary = tk.Text(root, height=4, width=50)
entry_summary.pack()

# ---- Education Section ----
tk.Label(root, text="Education Details").pack(pady=5)

frame_edu = tk.Frame(root)
frame_edu.pack()

tk.Label(frame_edu, text="Degree").grid(row=0, column=0)
entry_degree = tk.Entry(frame_edu, width=20)
entry_degree.grid(row=0, column=1)

tk.Label(frame_edu, text="Institution").grid(row=1, column=0)
entry_institution = tk.Entry(frame_edu, width=20)
entry_institution.grid(row=1, column=1)

tk.Label(frame_edu, text="Percentage").grid(row=3, column=0)
entry_percentage = tk.Entry(frame_edu, width=20)
entry_percentage.grid(row=3, column=1)

tk.Label(frame_edu, text="Passing Year").grid(row=2, column=0)
entry_year = tk.Entry(frame_edu, width=20)
entry_year.grid(row=2, column=1)

tk.Button(frame_edu, text="Add Education", command=add_education).grid(row=4, columnspan=2, pady=5)

# ---- Experience ----
tk.Label(root, text="Experience (Role,Company,Duration,Point1;Point2;...)").pack()
entry_experience = tk.Text(root, height=6, width=50)
entry_experience.pack()

# ---- Skills ----
tk.Label(root, text="Skills (comma separated)").pack()
entry_skills = tk.Text(root, height=3, width=50)
entry_skills.pack()

tk.Button(root, text="Generate Resume", command=submit_form).pack(pady=20)

root.mainloop()