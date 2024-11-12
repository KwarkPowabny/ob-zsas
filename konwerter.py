import re
import csv
from datetime import datetime

def safe_search(pattern, text):
    match = re.search(pattern, text)
    result = match.group(1).strip() if match else ""
    return result

def parse_email(email_content):
    data_ur = safe_search(r"Data urodzenia\s+(.*)", email_content)
    wiek = data_ur[-2:]
    wiek = str(25 - int(wiek))+" lat"
    data = {
        "Grupa": safe_search(r"Grupa\s+(.*)", email_content),
        "Wiek": wiek,
        "Imię": safe_search(r"Imię\s+(.*)", email_content),
        "Nazwisko": safe_search(r"Nazwisko\s+(.*)", email_content),
        "PESEL": safe_search(r"PESEL\s+(\d+)", email_content),
        "Data urodzenia": data_ur,
        "Adres zamieszkania": safe_search(r"Adres zamieszkania.*\s+([^\n]+)", email_content),
        "Kod pocztowy": safe_search(r"Kod pocztowy\s+(\d{2}-\d{3})", email_content),
        "Miasto": safe_search(r"Miasto\s+(.*)", email_content),
        "Imię i nazwisko matki": safe_search(r"Imię i nazwisko matki/opiekuna\s+(.*)", email_content),
        "Imię i nazwisko ojca": safe_search(r"Imię i nazwisko ojca/opiekuna\s+(.*)", email_content),
        "Numer kontaktowy": safe_search(r"Numer kontaktowy do rodzica/opiekuna\s+(\d+)", email_content),
        "Email kontaktowy": safe_search(r"Email kontaktowy.*\s+([^\n]+)", email_content),
        "Dieta wegetariańska": safe_search(r"Dieta wegetariańska\s+(Tak|Nie)", email_content),
        "Rozmiar koszulki": safe_search(r"Rozmiar koszulki\s+(.*)", email_content),
        "Jak do nas trafiłeś": safe_search(r"Jak do nas trafiłeś\?\s+(.*)", email_content),
        "Obóz wcześniej": safe_search(r"Czy dziecko było już na innym obozie.*\s+(Tak|Nie)", email_content),
        "Akceptacja regulaminu": safe_search(r"akceptujesz regulamin.*\s+(Tak|Nie)", email_content),
        "Data przetworzenia": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # data przetworzenia
    }
    return data

#dane zapisane w pliku email.txt

with open("email.txt", "r", encoding="utf-8") as file:
    email_content = file.read()

def save_to_csv(data, csv_filename='uczestnicy_obozu.csv'):
    fieldnames = [
        "Grupa", "Wiek", "Imię", "Nazwisko", "PESEL", "Data urodzenia",
        "Adres zamieszkania", "Kod pocztowy", "Miasto", "Imię i nazwisko matki",
        "Imię i nazwisko ojca", "Numer kontaktowy", "Email kontaktowy",
        "Dieta wegetariańska", "Rozmiar koszulki", "Jak do nas trafiłeś",
        "Obóz wcześniej", "Akceptacja regulaminu", "Data przetworzenia"
    ]
    
   
    with open(csv_filename, mode='a', newline='', encoding='utf-8-sig') as csvfile: #UTF-8 BOM
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

parsed_data = parse_email(email_content)
save_to_csv(parsed_data)

print("Dane zparsowane")
