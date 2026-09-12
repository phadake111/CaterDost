import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_client_materials_pdf(order, client_provided_only: bool = True) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Clean English Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#ea580c'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=14
    )
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0f172a')
    )
    cell_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0f172a')
    )
    cell_center = ParagraphStyle(
        'CellCenter',
        parent=cell_style,
        alignment=1
    )
    header_cell = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.white
    )
    header_center = ParagraphStyle(
        'HeaderCenter',
        parent=header_cell,
        alignment=1
    )

    # Document Header
    story.append(Paragraph("CaterDost — (Raw Material Requirement List)", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", subtitle_style))
    story.append(Spacer(1, 4))

    # Meta Information Box
    first_day = order.days[0] if order.days else None
    event_date = str(first_day.event_date) if (first_day and first_day.event_date) else "-"
    people_str = f"{first_day.people_count} Pax" if (first_day and first_day.people_count) else "-"
    location_str = str(first_day.location) if (first_day and first_day.location) else "-"

    meta_info = [
        [
            Paragraph(f"<b>Order / Event:</b> {order.order_title}", meta_style),
            Paragraph(f"<b>Client Name:</b> {order.client.name}", meta_style)
        ],
        [
            Paragraph(f"<b>Date:</b> {event_date}", meta_style),
            Paragraph(f"<b>Phone:</b> {order.client.phone}", meta_style)
        ],
        [
            Paragraph(f"<b>Guests:</b> {people_str}", meta_style),
            Paragraph(f"<b>Location:</b> {location_str}", meta_style)
        ]
    ]

    meta_table = Table(meta_info, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff7ed')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # Resource Items
    if client_provided_only:
        items = [r for r in order.resources if r.is_client_provided]
        section_heading = "Items to be Provided by Client"
    else:
        items = order.resources
        section_heading = "All Required Raw Materials"

    story.append(Paragraph(f"<b>{section_heading}</b>", styles['Heading3']))
    story.append(Spacer(1, 6))

    # Build Table
    table_data = [[
        Paragraph("<b>Sr.</b>", header_center),
        Paragraph("<b>Item Description</b>", header_cell),
        Paragraph("<b>Qty</b>", header_center),
        Paragraph("<b>Unit</b>", header_center),
        Paragraph("<b>Notes / Remarks</b>", header_cell)
    ]]

    if not items:
        table_data.append([
            Paragraph("-", cell_center),
            Paragraph("No raw materials listed under this category.", cell_style),
            Paragraph("-", cell_center),
            Paragraph("-", cell_center),
            Paragraph("-", cell_style)
        ])
    else:
        for idx, res in enumerate(items, start=1):
            notes = res.notes if res.notes else "-"
            table_data.append([
                Paragraph(str(idx), cell_center),
                Paragraph(f"<b>{res.resource_name}</b>", cell_style),
                Paragraph(f"{res.quantity:g}", cell_center),
                Paragraph(str(res.unit), cell_center),
                Paragraph(str(notes), cell_style)
            ])

    items_table = Table(table_data, colWidths=[35, 210, 65, 60, 170])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(items_table)

    story.append(Spacer(1, 20))
    footer_text = "Note: Please ensure all ingredients are arranged and checked one day prior to the event. Thank you!"
    story.append(Paragraph(f"<i>{footer_text}</i>", subtitle_style))

    doc.build(story)
    buffer.seek(0)
    return buffer