from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.database import camps_collection, patients_collection, vitals_collection
from bson import ObjectId
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import os
from datetime import datetime

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/{camp_id}")
def generate_report(camp_id: str):
    # Fetch camp
    camp = camps_collection.find_one({"_id": ObjectId(camp_id)})
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")

    # Fetch patients
    patients = list(patients_collection.find({"camp_id": camp_id}))
    total_patients = len(patients)

    # Fetch vitals and count risks
    high_risk = 0
    medium_risk = 0
    vitals_data = []
    for p in patients:
        v = vitals_collection.find_one({"patient_id": str(p["_id"])})
        if v:
            if v.get("risk_level") == "High":
                high_risk += 1
            elif v.get("risk_level") == "Medium":
                medium_risk += 1
            vitals_data.append({
                "name": p["name"],
                "age": p["age"],
                "bp": v.get("blood_pressure", "-"),
                "sugar": v.get("blood_sugar", "-"),
                "hb": v.get("hemoglobin", "-"),
                "bmi": v.get("bmi", "-"),
                "risk": v.get("risk_level", "-"),
                "flags": ", ".join(v.get("risk_flags", []))
            })

    # Create PDF
    filename = f"report_{camp_id}.pdf"
    filepath = f"./{filename}"
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("🏥 Rural Health Camp Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Camp Info
    elements.append(Paragraph(f"<b>Camp Name:</b> {camp['camp_name']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Date:</b> {camp['date']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Village:</b> {camp['village']}, {camp['district']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Organized By:</b> {camp['organized_by']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Doctors:</b> {', '.join(camp['doctors'])}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Summary Box
    elements.append(Paragraph("<b>📊 Summary</b>", styles["Heading2"]))
    summary_data = [
        ["Total Patients", "High Risk", "Medium Risk", "Normal"],
        [
            str(total_patients),
            str(high_risk),
            str(medium_risk),
            str(total_patients - high_risk - medium_risk)
        ]
    ]
    summary_table = Table(summary_data, colWidths=[120, 120, 120, 120])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E86AB")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (1, 1), (1, 1), colors.HexColor("#FF6B6B")),
        ("BACKGROUND", (2, 1), (2, 1), colors.HexColor("#FFE66D")),
        ("BACKGROUND", (3, 1), (3, 1), colors.HexColor("#6BCB77")),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # Patient Details Table
    elements.append(Paragraph("<b>👥 Patient Details</b>", styles["Heading2"]))
    table_data = [["Name", "Age", "BP", "Sugar", "Hb", "BMI", "Risk"]]
    for v in vitals_data:
        table_data.append([
            v["name"], str(v["age"]), v["bp"],
            str(v["sugar"]), str(v["hb"]),
            str(v["bmi"]), v["risk"]
        ])

    patient_table = Table(table_data, colWidths=[90, 35, 55, 50, 40, 45, 55])
    patient_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E86AB")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 20))

    # Footer
    elements.append(Paragraph(
        f"Report generated on {datetime.now().strftime('%d %B %Y at %I:%M %p')}",
        styles["Normal"]
    ))

    doc.build(elements)
    return FileResponse(filepath, media_type="application/pdf", filename=filename)