# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os
import sys
import re

class TRFCardGeneratorApp:
    """
    GUI + PDF-generator för TRF-kort.
    Underskriftsrader: linje + Ort och datum + Namnförtydligande under linjen.
    Ökad nederkant för luft.
    """

    def __init__(self, root_window):
        self.root = root_window
        self.root.title("TRF-Kort Generator v3.0")
        self.root.minsize(560, 700)

        # Radiovariabler (ansvar)
        self.responsibility_vars = {
            "pavg": tk.StringVar(value="Ägare"),
            "trang": tk.StringVar(value="Ägare"),
            "sjalvrisk": tk.StringVar(value="Ägare"),
            "skatt": tk.StringVar(value="Ägare"),
        }

        # Fält
        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(expand=True, fill="both")

        info_frame = tk.LabelFrame(main_frame, text="1. Parter, Fordon och Period", padx=10, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)

        info_labels = [
            "Ägare:", "Ägare (Personnummer):",
            "Förare:", "Förare (Personnummer):",
            "Fordon (Märke/Modell):", "Registreringsnummer:",
            "Avtalets slutdatum (ÅÅÅÅ-MM-DD):", "Ort för underskrift:"
        ]

        for i, label_text in enumerate(info_labels):
            label = tk.Label(info_frame, text=label_text)
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)

            entry = tk.Entry(info_frame, width=44)
            entry.grid(row=i, column=1, sticky="we", padx=5, pady=5)
            self.entries[label_text] = entry

        resp_frame = tk.LabelFrame(main_frame, text="2. Ansvarsfördelning", padx=10, pady=10)
        resp_frame.pack(fill="x", pady=10)
        resp_frame.columnconfigure(1, weight=1)

        resp_options = [
            ("Parkeringsavgifter/böter:", "pavg"),
            ("Trängselskatt/vägavgifter:", "trang"),
            ("Självrisk vid skada:", "sjalvrisk"),
            ("Fordonsskatt:", "skatt"),
        ]

        for i, (text, key) in enumerate(resp_options):
            tk.Label(resp_frame, text=text).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            radio_container = tk.Frame(resp_frame)
            radio_container.grid(row=i, column=1, sticky="w")
            tk.Radiobutton(radio_container, text="Ägare", variable=self.responsibility_vars[key], value="Ägare").pack(side="left", padx=6)
            tk.Radiobutton(radio_container, text="Förare", variable=self.responsibility_vars[key], value="Förare").pack(side="left", padx=6)

        tk.Button(
            main_frame,
            text="Skapa TRF-kort (PDF)",
            command=self.process_form_and_generate_pdf,
            bg="#007ACC", fg="white",
            font=("Helvetica", 12, "bold"),
            relief="raised",
            pady=5
        ).pack(pady=18, fill="x")

    def process_form_and_generate_pdf(self):
        form_data = {
            "owner": self.entries["Ägare:"].get().strip(),
            "owner_id": self.entries["Ägare (Personnummer):"].get().strip(),
            "driver": self.entries["Förare:"].get().strip(),
            "driver_id": self.entries["Förare (Personnummer):"].get().strip(),
            "vehicle": self.entries["Fordon (Märke/Modell):"].get().strip(),
            "regnr": self.entries["Registreringsnummer:"].get().strip().upper(),
            "end_date": self.entries["Avtalets slutdatum (ÅÅÅÅ-MM-DD):"].get().strip(),
            "location": self.entries["Ort för underskrift:"].get().strip(),
            "pavg": self.responsibility_vars["pavg"].get(),
            "trang": self.responsibility_vars["trang"].get(),
            "sjalvrisk": self.responsibility_vars["sjalvrisk"].get(),
            "skatt": self.responsibility_vars["skatt"].get(),
        }

        # Kontroll att alla fält är ifyllda (ansvarsfälten är alltid satta)
        required = ["owner", "owner_id", "driver", "driver_id", "vehicle", "regnr", "end_date", "location"]
        for field in required:
            if not form_data[field]:
                messagebox.showwarning("Inmatningsfel", "Alla fält måste fyllas i.")
                return

        # Datumvalidering
        try:
            datetime.strptime(form_data["end_date"], "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Datumfel", "Vänligen ange slutdatum i formatet ÅÅÅÅ-MM-DD.")
            return

        # Safe filnamn
        safe_owner = re.sub(r'[^A-Za-z0-9_\-åäöÅÄÖ ]', '', form_data['owner']).strip().replace(' ', '_') or "owner"
        safe_reg = re.sub(r'[^A-Za-z0-9\-]', '', form_data['regnr']) or "regnr"
        filename = f"TRF-kort_{safe_owner}_{safe_reg}.pdf"

        try:
            self.generate_pdf(form_data, filename)
            messagebox.showinfo("PDF Skapad!", f"TRF-kortet har sparats som:\n{os.path.abspath(filename)}")
        except Exception as e:
            messagebox.showerror("Fel vid PDF-generering", f"Ett oväntat fel uppstod: {e}")

    def generate_pdf(self, data, filename):
        """
        Genererar PDF med:
        - gott om nederkant (bottom_margin)
        - underskriftsrader med Ort & datum + Namnförtydligande under linjen
        """
        c = canvas.Canvas(filename, pagesize=A4)
        page_w, page_h = A4

        # Marginaler (mer luft i botten)
        left_margin = 2.0 * cm
        right_margin = 2.0 * cm
        top_margin = 2.0 * cm
        bottom_margin = 3.0 * cm           # <-- större nederkant för luft

        content_width = page_w - left_margin - right_margin
        text_color = colors.HexColor("#2F4F4F")

        # start-y från toppen
        y_cursor = page_h - top_margin

        # Titel
        c.setFillColor(text_color)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(page_w / 2.0, y_cursor, "TRF-Kort")
        y_cursor -= 0.9 * cm
        c.setFont("Helvetica", 10)
        c.drawCentredString(page_w / 2.0, y_cursor, "Avtal om tillfällig överlåtelse av fordon")
        y_cursor -= 1.4 * cm

        # Valfri logo (om finns)
        try:
            script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            logo_path = os.path.join(script_dir, "TRF-KORT.png")
            if hasattr(sys, '_MEIPASS'):
                logo_path = os.path.join(sys._MEIPASS, "TRF-KORT.png")
            if os.path.exists(logo_path):
                c.drawImage(logo_path, left_margin, page_h - top_margin - 0.6*cm, width=2*cm, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass

        # Sektion 1: info (tabell)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(left_margin, y_cursor, "1. Parter, Fordon och Period")
        y_cursor -= 0.3 * cm
        c.line(left_margin, y_cursor, page_w - right_margin, y_cursor)
        y_cursor -= 0.6 * cm

        info_data = [
            ["Ägare:", f"{data['owner']} ({data['owner_id']})"],
            ["Brukare/Förare:", f"{data['driver']} ({data['driver_id']})"],
            ["Fordon:", data['vehicle']],
            ["Registreringsnummer:", data['regnr']],
            ["Avtalsperiod:", f"Fr.o.m. {datetime.today().strftime('%Y-%m-%d')} till t.o.m. {data['end_date']}"]
        ]
        info_table = Table(info_data, colWidths=[4.5*cm, content_width - 4.5*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('RIGHTPADDING', (0,0), (0,-1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), text_color),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        tw, th = info_table.wrapOn(c, content_width, 0)
        y_cursor -= th
        info_table.drawOn(c, left_margin, y_cursor)
        y_cursor -= 0.8 * cm

        # Sektion 2: ansvarstabell
        c.setFont("Helvetica-Bold", 14)
        c.drawString(left_margin, y_cursor, "2. Ansvars- och kostnadsfördelning")
        y_cursor -= 0.3 * cm
        c.line(left_margin, y_cursor, page_w - right_margin, y_cursor)
        y_cursor -= 0.6 * cm

        get_check = lambda value, target: "X" if value == target else ""
        resp_data = [
            ['Kostnad/Ansvar', 'Ägare', 'Förare'],
            ['Parkeringsavgifter/böter', get_check(data['pavg'], 'Ägare'), get_check(data['pavg'], 'Förare')],
            ['Trängselskatt/vägavgifter', get_check(data['trang'], 'Ägare'), get_check(data['trang'], 'Förare')],
            ['Självrisk vid skada', get_check(data['sjalvrisk'], 'Ägare'), get_check(data['sjalvrisk'], 'Förare')],
            ['Fordonsskatt', get_check(data['skatt'], 'Ägare'), get_check(data['skatt'], 'Förare')]
        ]
        resp_table = Table(resp_data, colWidths=[content_width - 4*cm, 2*cm, 2*cm])
        resp_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (1, 1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), text_color),
        ]))
        tw, th = resp_table.wrapOn(c, content_width, 0)
        y_cursor -= th
        resp_table.drawOn(c, left_margin, y_cursor)
        y_cursor -= 1.0 * cm

        # --- Underskriftsblock (manuell ritning för kontroll över avstånd) ---
        # Beräknad höjd på signaturblock:
        sig_block_height = 4.5 * cm

        # Om inte plats nog, börja ny sida
        if y_cursor - sig_block_height < bottom_margin:
            c.showPage()
            c.setFillColor(text_color)
            y_cursor = page_h - top_margin

        # Kolumninställningar för ägare / förare
        col_gap = 1.0 * cm
        col_width = (content_width - col_gap) / 2.0
        left_col_x = left_margin
        right_col_x = left_margin + col_width + col_gap

        # Placera signaturraden en bit under y_cursor
        y_sig_top = y_cursor
        y_line = y_sig_top - 0.6 * cm      # var signaturlinjen tas
        line_left_x = left_col_x + 0.3 * cm
        line_left_x2 = left_col_x + col_width - 0.3 * cm
        line_right_x = right_col_x + 0.3 * cm
        line_right_x2 = right_col_x + col_width - 0.3 * cm

        c.setLineWidth(1)
        # Ägare - signaturlinje
        c.line(line_left_x, y_line, line_left_x2, y_line)
        # Förare - signaturlinje
        c.line(line_right_x, y_line, line_right_x2, y_line)

        # Text UNDER signaturlinjen: Ort och datum, Namnförtydligande
        today = datetime.today().strftime("%Y-%m-%d")
        loc_text = data['location'] if data['location'] else "__________________________"

        # Ägare - Ort och datum (prefyll om location finns)
        owner_ort_datum = f"Ort och datum: {loc_text}, {today}" if data['location'] else "Ort och datum: __________________________"
        owner_namn = f"Namnförtydligande: {data['owner']}"
        # Förare - Ort och datum
        driver_ort_datum = f"Ort och datum: {loc_text}, {today}" if data['location'] else "Ort och datum: __________________________"
        driver_namn = f"Namnförtydligande: {data['driver']}"

        # Skriva under texts (centera i kolumner eller left-align)
        text_x_offset = 0.2 * cm
        c.setFont("Helvetica", 10)
        # Ägare
        c.drawString(left_col_x + text_x_offset, y_line - 0.9 * cm, owner_ort_datum)
        c.drawString(left_col_x + text_x_offset, y_line - 1.5 * cm, owner_namn)
        # Förare
        c.drawString(right_col_x + text_x_offset, y_line - 0.9 * cm, driver_ort_datum)
        c.drawString(right_col_x + text_x_offset, y_line - 1.5 * cm, driver_namn)

        # Flytta y_cursor ner efter signaturblocket
        y_cursor = y_line - 1.9 * cm

        # Footer-meddelande ovanför bottom_margin (säker plats tack vare större bottom_margin)
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.grey)
        footer_y = bottom_margin - 0.9 * cm
        if footer_y < 0.8 * cm:
            footer_y = 0.8 * cm
        c.drawCentredString(page_w / 2.0, footer_y, "Genom sin underskrift bekräftar parterna att de tagit del av innehållet")
        c.drawCentredString(page_w / 2.0, footer_y - 0.5 * cm, "och accepterar villkoren utan reservationer.")

        c.save()


if __name__ == "__main__":
    root = tk.Tk()
    app = TRFCardGeneratorApp(root)
    root.mainloop()

