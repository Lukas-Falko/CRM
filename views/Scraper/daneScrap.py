from bs4 import BeautifulSoup


def log_message(output_widget, message):
    """Directly update the output widget with a message"""
    if output_widget and message:
        output_widget.insert("end", f"{message.strip()}\n")
        output_widget.see("end")
        output_widget.update()


def pobierz_firme(response, output_widget=None):

    soup = BeautifulSoup(response.text, 'html.parser')

    etykieta = soup.find('h1', class_='entry-text--h')
    
    if etykieta:
        tekst = etykieta.get_text(strip=True)
        log_message(output_widget, f"Scraping | Firmy: {tekst}")
        return tekst
    log_message(output_widget, "Brak nazwy firmy")
    return None

def pobierz_date(response, output_widget=None):

    soup = BeautifulSoup(response.text, 'html.parser')


    etykieta_date = soup.find('div', class_='article-text--date') 
    date_tekst = etykieta_date.get_text(strip=True)
    if date_tekst:
        log_message(output_widget, f"Scraping | Data: {date_tekst}")
        return date_tekst
        
    else:
        log_message(output_widget, "Scraping | Data: Brak")

def pobierz_adres(response, output_widget=None):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'Adres' in t)
    
    if main_div:
        
        etykieta_adres = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_adres:
            adres_tekst = etykieta_adres.get_text(strip=True)
            log_message(output_widget, f"Scraping | Adres: {adres_tekst}")
            return adres_tekst
           
    log_message(output_widget, "Nie znaleziono adresu")
    return None

def pobierz_miasto(response, output_widget=None):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'Miasto' in t)
    
    if main_div:
        
        etykieta_miasto = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_miasto:
            adres_tekst = etykieta_miasto.get_text(strip=True)
            log_message(output_widget, f"Scraping | Miasto: {adres_tekst}")
            return adres_tekst
           
    log_message(output_widget, "Nie znaleziono adresu")
    return None

def pobierz_kraj(response, output_widget=None):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'Kraj' in t)
    
    if main_div:
        
        etykieta_kraj = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_kraj:
            kraj_tekst = etykieta_kraj.get_text(strip=True)
            log_message(output_widget, f"Scraping | Kraj: {kraj_tekst}")
            return kraj_tekst
           
    log_message(output_widget, "Scraping | Kraj: nie znaleziono")
    return None

def pobierz_telefon(response, output_widget=None):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'Telefon' in t)
    
    if main_div:
        
        etykieta_telefon = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_telefon:
            telefon_tekst = etykieta_telefon.get_text(strip=True)
            log_message(output_widget, f"Scraping | Telefon: {telefon_tekst}")
            return telefon_tekst
           
    log_message(output_widget, "Scraping | Telefon: nie znaleziono")
    return None

def pobierz_email(response, output_widget=None):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'E-mail' in t)
    
    if main_div:
        
        etykieta_email = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_email:
            email_tekst = etykieta_email.get_text(strip=True)
            log_message(output_widget, f"Scraping | Email: {email_tekst}")
            return email_tekst
           
    log_message(output_widget, "Scraping | Email: nie znaleziono")
    return None

def pobierz_strona(response, output_widget=None):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'Strona internetowa' in t)
    
    if main_div:
        
        etykieta_strona = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_strona:
            strona_tekst = etykieta_strona.get_text(strip=True)
            log_message(output_widget, f"Scraping | Strona internetowa: {strona_tekst}")
            return strona_tekst
           
    log_message(output_widget, "Scraping | Strona internetowa: nie znaleziono")
    return None
