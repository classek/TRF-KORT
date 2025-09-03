import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def skapa_pdf(data):
    filnamn = "TRF_kort.pdf"
    c = canvas.Canvas(filnamn, pagesize=A4)
    width, height = A4

    # Logotyp
    c.setFont("Helvetica-Bold", 20)
    c.drawString(2*cm, height - 2*cm, "🚗  TRF-KORT")

    # Rubrik
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, height - 3.5*cm, "Tillstånd och Reglering av Fordon")

    # Parter
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, height - 5*cm, "1. Parter")

    c.setFont("Helvetica", 11)
    c.drawString(2.5*cm, height - 5.7*cm, f"Fordonsägare: {data['agare']}")
    c.drawString(2.5*cm, height - 6.3*cm, f"Personnummer/Org.nr: {data['agare_pnr']}")
    c.drawString(2.5*cm, height - 6.9*cm, f"Kontaktuppgifter: {data['agare_kontakt']}")

    c.drawString(2.5*cm, height - 8*cm, f"Förare (låntagare): {data['forare']}")
    c.drawString(2.5*cm, height - 8.6*cm, f"Personnummer: {data['forare_pnr']}")
    c.drawString(2.5*cm, height - 9.2*cm, f"Kontaktuppgifter: {data['forare_kontakt']}")

    # Fordonsinformation
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, height - 10.5*cm, "2. Fordonsinformation")

    c.setFont("Helvetica", 11)
    c.drawString(2.5*cm, height - 11.2*cm, f"Registreringsnummer: {data['regnr']}")
    c.drawString(2.5*cm, height - 11.8*cm, f"Märke och modell: {data['marke_modell']}")

    # Tillstånd
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, height - 13*cm, "3. Tillstånd och giltighetsperiod")

    c.setFont("Helvetica", 11)
    c.drawString(2.5*cm, height - 13.7*cm,
                 "Tillstånd att använda fordonet beviljas från: ____________ till ____________")

    # Ansvar
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, height - 15*cm, "4. Ansvars- och kostnadsfördelning")

    c.setFont("Helvetica", 11)
    c.drawString(2.5*cm, height - 15.7*cm, "Parkeringsavgifter/böter: Ägare / Förare / Enligt faktura")
    c.drawString(2.5*cm, height - 16.3*cm, "Trängselskatt/vägavgifter: Ägare / Förare / Enligt faktura")
    c.drawString(2.5*cm, height - 16.9*cm, "Självrisk vid olycka: Ägare / Förare")
    c.drawString(2.5*cm, height - 17.5*cm, "Fordonsskatt: Ägare / Förare")

    # Underskrifter
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, height - 19*cm, "5. Underskrifter")

    c.setFont("Helvetica", 11)
    c.drawString(2.5*cm, height - 19.7*cm,
                 "Fordonsägare: __________________________ Datum: ___ / ___ / ____")
    c.drawString(2.5*cm, height - 20.3*cm,
                 "Förare: _________________________________ Datum: ___ / ___ / ____")

    c.showPage()
    c.save()
    return filnamn

def skapa():
    data = {
        "agare": entry_agare.get().strip(),
        "agare_pnr": entry_agare_pnr.get().strip(),
        "agare_kontakt": entry_agare_kontakt.get().strip(),
        "forare": entry_forare.get().strip(),
        "forare_pnr": entry_forare_pnr.get().strip(),
        "forare_kontakt": entry_forare_kontakt.get().strip(),
        "regnr": entry_regnr.get().strip(),
        "marke_modell": entry_marke.get().strip()
    }

    if not all(data.values()):
        messagebox.showwarning("Fel", "Fyll i alla fält!")
        return

    fil = skapa_pdf(data)
    messagebox.showinfo("Klart", f"PDF skapad: {fil}")

# --- GUI ---
root = tk.Tk()
root.title("TRF-kort Generator")

# Ägare
tk.Label(root, text="Fordonsägare:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_agare = tk.Entry(root, width=40)
entry_agare.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Ägarens personnummer/org.nr:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_agare_pnr = tk.Entry(root, width=40)
entry_agare_pnr.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Ägarens kontaktuppgifter:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_agare_kontakt = tk.Entry(root, width=40)
entry_agare_kontakt.grid(row=2, column=1, padx=5, pady=5)

# Förare
tk.Label(root, text="Förare:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_forare = tk.Entry(root, width=40)
entry_forare.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Förarens personnummer:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
entry_forare_pnr = tk.Entry(root, width=40)
entry_forare_pnr.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Förarens kontaktuppgifter:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
entry_forare_kontakt = tk.Entry(root, width=40)
entry_forare_kontakt.grid(row=5, column=1, padx=5, pady=5)

# Fordonsinfo
tk.Label(root, text="Registreringsnummer:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
entry_regnr = tk.Entry(root, width=40)
entry_regnr.grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Märke och modell:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
entry_marke = tk.Entry(root, width=40)
entry_marke.grid(row=7, column=1, padx=5, pady=5)

# Knapp
tk.Button(root, text="Skapa TRF-kort (PDF)", command=skapa).grid(row=8, column=0, columnspan=2, pady=15)

root.mainloop()
