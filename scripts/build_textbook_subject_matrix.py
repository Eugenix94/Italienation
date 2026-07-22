import pandas as pd
import os

def generate_subject_textbook_matrix():
    data = [
        # LICEO CLASSICO
        ["Liceo", "Liceo Classico", "Anno 1 (Classe I)", "Lingua e letteratura italiana", "Antologia + Grammatica (3 vol.)", 58.50, 42.00, 39.3, "MIM Tetto Anno 1: €335.00 | Overrun: +74.6%"],
        ["Liceo", "Liceo Classico", "Anno 1 (Classe I)", "Lingua e cultura latina", "Grammatica + Esercizi (2 vol.)", 49.00, 36.00, 36.1, "Obbligatorio adozione Anno 1"],
        ["Liceo", "Liceo Classico", "Anno 1 (Classe I)", "Lingua e cultura greca", "Grammatica + Esercizi (2 vol.)", 52.00, 38.00, 36.8, "Obbligatorio adozione Anno 1"],
        ["Liceo", "Liceo Classico", "Anno 1 (Classe I)", "Lingua e cultura straniera (Inglese)", "Coursebook + Grammar + WB", 38.00, 29.00, 31.0, "Consigliata versione integrata digital"],
        ["Liceo", "Liceo Classico", "Anno 1 (Classe I)", "Storia e geografia", "Manuale integrato (2 vol.)", 36.50, 27.50, 32.7, "Adottato nel biennio"],
        ["Liceo", "Liceo Classico", "Anno 1 (Classe I)", "Matematica", "Manuale con esercizi biennio", 39.00, 29.50, 32.2, "Corso triennale/biennale"],
        ["Liceo", "Liceo Classico", "Anno 1 (Classe I)", "Scienze naturali", "Biologia e Scienze della Terra", 32.00, 24.00, 33.3, "Modulo biennio"],
        ["Liceo", "Liceo Classico", "Anno 1 (Classe I)", "Religione / Materia alternativa", "Testo unico 5 anni", 18.00, 14.00, 28.6, "Facoltativo / Opzionale"],
        ["Liceo", "Liceo Classico", "Anno 3 (Classe III)", "Filosofia", "Manuale di Filosofia (Vol 1)", 34.00, 26.00, 30.8, "MIM Tetto Anno 3: €150.00 | Overrun: +42.0%"],
        ["Liceo", "Liceo Classico", "Anno 3 (Classe III)", "Fisica", "Manuale di Fisica triennio", 31.50, 23.50, 34.0, "Adottato in 3a"],
        ["Liceo", "Liceo Classico", "Anno 3 (Classe III)", "Storia dell'arte", "Manuale di Storia dell'Arte (Vol 1)", 36.00, 27.00, 33.3, "Adottato in 3a"],

        # LICEO SCIENTIFICO TRADIZIONALE
        ["Liceo", "Liceo Scientifico", "Anno 1 (Classe I)", "Lingua e letteratura italiana", "Antologia + Grammatica", 56.00, 41.00, 36.6, "MIM Tetto Anno 1: €320.00 | Overrun: +68.8%"],
        ["Liceo", "Liceo Scientifico", "Anno 1 (Classe I)", "Lingua e cultura latina", "Grammatica + Esercizi", 46.00, 34.00, 35.3, "Adottato al biennio"],
        ["Liceo", "Liceo Scientifico", "Anno 1 (Classe I)", "Lingua e cultura straniera (Inglese)", "Coursebook + Grammar", 37.50, 28.00, 33.9, "Versione mista paper+digital"],
        ["Liceo", "Liceo Scientifico", "Anno 1 (Classe I)", "Storia e geografia", "Manuale biennio", 35.00, 26.00, 34.6, "Adottato al biennio"],
        ["Liceo", "Liceo Scientifico", "Anno 1 (Classe I)", "Matematica", "Manuale avanzato + Algebra/Geometria", 48.00, 36.00, 33.3, "Corso biennale integrato"],
        ["Liceo", "Liceo Scientifico", "Anno 1 (Classe I)", "Fisica", "Fisica per i Licei (Vol 1)", 29.50, 22.00, 34.1, "Primo biennio"],
        ["Liceo", "Liceo Scientifico", "Anno 1 (Classe I)", "Scienze naturali", "Chimica e Scienze della Terra", 34.00, 25.50, 33.3, "Modulo biennio"],
        ["Liceo", "Liceo Scientifico", "Anno 1 (Classe I)", "Disegno e storia dell'arte", "Manuale + Tavole da disegno", 36.00, 27.00, 33.3, "Corso 5 anni"],

        # LICEO SCIENTIFICO SCIENZE APPLICATE
        ["Liceo", "Scienze Applicate", "Anno 1 (Classe I)", "Lingua e letteratura italiana", "Antologia + Grammatica", 54.00, 40.00, 35.0, "MIM Tetto Anno 1: €320.00 | Overrun: +62.5%"],
        ["Liceo", "Scienze Applicate", "Anno 1 (Classe I)", "Informatica", "Manuale di Informatica + Lab Python", 32.00, 24.00, 33.3, "Sostituisce Latino"],
        ["Liceo", "Scienze Applicate", "Anno 1 (Classe I)", "Matematica", "Manuale avanzato con moduli Python/Excel", 49.00, 37.00, 32.4, "Corso biennale integrato"],
        ["Liceo", "Scienze Applicate", "Anno 1 (Classe I)", "Fisica", "Fisica sperimentale con Lab (Vol 1)", 31.00, 23.00, 34.8, "Modulo con laboratori virtuali"],
        ["Liceo", "Scienze Applicate", "Anno 1 (Classe I)", "Scienze naturali", "Biologia, Chimica, Scienze Terra (3 vol.)", 44.00, 33.00, 33.3, "Potenziato rispetto al Tradizionale"],

        # ISTITUTO TECNICO ECONOMICO (AFM)
        ["Tecnico", "Tecnico Economico (AFM)", "Anno 1 (Classe I)", "Lingua e letteratura italiana", "Antologia biennio", 42.00, 31.00, 35.5, "MIM Tetto Anno 1: €304.00 | Overrun: +51.3%"],
        ["Tecnico", "Tecnico Economico (AFM)", "Anno 1 (Classe I)", "Lingua inglese", "Business English + Coursebook", 34.00, 25.00, 36.0, "Adottato al biennio"],
        ["Tecnico", "Tecnico Economico (AFM)", "Anno 1 (Classe I)", "Seconda lingua straniera (Spagnolo/Tedesco/Francese)", "Coursebook + Esercizi", 31.00, 23.00, 34.8, "Obbligatorio biennio"],
        ["Tecnico", "Tecnico Economico (AFM)", "Anno 1 (Classe I)", "Matematica", "Matematica per l'Economia", 36.00, 27.00, 33.3, "Corso biennio"],
        ["Tecnico", "Tecnico Economico (AFM)", "Anno 1 (Classe I)", "Diritto ed economia", "Manuale di Diritto ed Economia", 29.00, 21.50, 34.9, "Adottato al biennio"],
        ["Tecnico", "Tecnico Economico (AFM)", "Anno 1 (Classe I)", "Economia aziendale", "Primi elementi di Economia Aziendale", 28.00, 21.00, 33.3, "Propedeutico al triennio"],
        ["Tecnico", "Tecnico Economico (AFM)", "Anno 1 (Classe I)", "Informatica", "Informatica gestionale + Licenza software", 33.00, 24.50, 34.8, "Adottato al biennio"],
        ["Tecnico", "Tecnico Economico (AFM)", "Anno 1 (Classe I)", "Geografia economica", "Geografia generale ed economica", 26.00, 19.50, 33.3, "Modulo biennio"],

        # ISTITUTO TECNICO TECNOLOGICO (INFORMATICA)
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Anno 1 (Classe I)", "Lingua e letteratura italiana", "Antologia biennio", 41.00, 30.00, 36.6, "MIM Tetto Anno 1: €304.00 | Overrun: +57.9%"],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Anno 1 (Classe I)", "Matematica", "Matematica con moduli tecnologici", 38.00, 28.50, 33.3, "Adottato al biennio"],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Anno 1 (Classe I)", "Fisica", "Fisica applicata con laboratorio", 31.00, 23.00, 34.8, "Scienze integrate"],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Anno 1 (Classe I)", "Chimica", "Chimica generale ed organica", 29.50, 22.00, 34.1, "Scienze integrate"],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Anno 1 (Classe I)", "Tecnologie e tecniche di rappresentazione grafica", "Manuale CAD + Disegno", 35.00, 26.00, 34.6, "Corso biennio"],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Anno 1 (Classe I)", "Tecnologie informatiche", "Manuale di Programmazione e Hardware", 34.00, 25.00, 36.0, "Corso 1° anno"],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Anno 3 (Classe III)", "Informatica (Triennio)", "Linguaggi C++/Java/Web (Vol 1)", 38.00, 28.50, 33.3, "MIM Tetto Anno 3: €190.00 | Overrun: +44.7%"],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Anno 3 (Classe III)", "Sistemi e reti", "Reti di calcolatori e Architetture (Vol 1)", 36.00, 27.00, 33.3, "Adottato in 3a"],
        ["Tecnico", "Tecnico Tecnologico (Informatica)", "Anno 3 (Classe III)", "Telecomunicazioni", "Tecnologie delle Telecomunicazioni", 32.00, 24.00, 33.3, "Adottato in 3a"],

        # ISTITUTO PROFESSIONALE (ENOGASTRONOMIA)
        ["Professionale", "Professionale (Enogastronomia)", "Anno 1 (Classe I)", "Lingua e letteratura italiana", "Italiano per la formazione professionale", 36.00, 27.00, 33.3, "MIM Tetto Anno 1: €240.00 | Overrun: +83.3%"],
        ["Professionale", "Professionale (Enogastronomia)", "Anno 1 (Classe I)", "Lingua inglese", "English for Culinary & Hospitality", 32.00, 24.00, 33.3, "Adottato al biennio"],
        ["Professionale", "Professionale (Enogastronomia)", "Anno 1 (Classe I)", "Matematica", "Matematica applicata ed esercitazioni", 31.00, 23.00, 34.8, "Adottato al biennio"],
        ["Professionale", "Professionale (Enogastronomia)", "Anno 1 (Classe I)", "Scienza e cultura dell'alimentazione", "Manuale di Alimentazione e Nutrizione", 38.00, 28.50, 33.3, "Adottato per 5 anni"],
        ["Professionale", "Professionale (Enogastronomia)", "Anno 1 (Classe I)", "Laboratorio di servizi enogastronomici (Cucina)", "Manuale di Tecnica di Cucina + Divisa Lab", 65.00, 48.00, 35.4, "Corredo divisa professionale €180 extra"],
        ["Professionale", "Professionale (Enogastronomia)", "Anno 1 (Classe I)", "Diritto ed economia", "Diritto per le strutture ricettive", 26.00, 19.50, 33.3, "Adottato al biennio"],
        ["Professionale", "Professionale (Enogastronomia)", "Anno 1 (Classe I)", "Seconda lingua straniera (Francese)", "Français pour la Restauration", 28.00, 21.00, 33.3, "Adottato al biennio"]
    ]

    df = pd.DataFrame(data, columns=[
        "Macro_Track", "Specific_Branch", "Grade_Level", "Subject", "Book_Title_Type",
        "Average_Price_Print_Eur", "Digital_Edition_Price_Eur", "Digital_Discount_Percent",
        "Ministerial_Ceiling_Cap_Notes"
    ])

    out_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "subject_textbook_costs_by_track_2026.csv")
    df.to_csv(csv_path, index=False)
    print(f"Dataset generated successfully at: {csv_path}")

if __name__ == "__main__":
    generate_subject_textbook_matrix()
