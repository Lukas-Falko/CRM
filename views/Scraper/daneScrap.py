from bs4 import BeautifulSoup


def pobierz_firme(response):

    soup = BeautifulSoup(response.text, 'html.parser')

    etykieta = soup.find('h1', class_='entry-text--h')
    
    if etykieta:
        tekst = etykieta.get_text(strip=True)
        print(f"Scraping | Firmy: {tekst}")
        return tekst
    print("Brak nazwy firmy")
    return None

def pobierz_date(response):

    soup = BeautifulSoup(response.text, 'html.parser')


    etykieta_date = soup.find('div', class_='article-text--date') 
    date_tekst = etykieta_date.get_text(strip=True)
    if date_tekst:
        print(f"Scraping | Data: {date_tekst}")
        return date_tekst
        
    else:
        print("Scraping | Data: Brak")

def pobierz_adres(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'Adres' in t)
    
    if main_div:
        
        etykieta_adres = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_adres:
            adres_tekst = etykieta_adres.get_text(strip=True)
            print(f"Scraping | Adres: {adres_tekst}")
            return adres_tekst
           
    print("Nie znaleziono adresu")
    return None

def pobierz_miasto(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'Miasto' in t)
    
    if main_div:
        
        etykieta_miasto = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_miasto:
            adres_tekst = etykieta_miasto.get_text(strip=True)
            print(f"Scraping | Miasto: {adres_tekst}")
            return adres_tekst
           
    print("Nie znaleziono adresu")
    return None

def pobierz_kraj(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'Kraj' in t)
    
    if main_div:
        
        etykieta_kraj = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_kraj:
            kraj_tekst = etykieta_kraj.get_text(strip=True)
            print(f"Scraping | Kraj: {kraj_tekst}")
            return kraj_tekst
           
    print("Scraping | Kraj: nie znaleziono")
    return None

def pobierz_telefon(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'Telefon' in t)
    
    if main_div:
        
        etykieta_telefon = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_telefon:
            telefon_tekst = etykieta_telefon.get_text(strip=True)
            print(f"Scraping | Telefon: {telefon_tekst}")
            return telefon_tekst
           
    print("Scraping | Telefon: nie znaleziono")
    return None

def pobierz_email(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'E-mail' in t)
    
    if main_div:
        
        etykieta_email = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_email:
            email_tekst = etykieta_email.get_text(strip=True)
            print(f"Scraping | Email: {email_tekst}")
            return email_tekst
           
    print("Scraping | Email: nie znaleziono")
    return None

def pobierz_strona(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    main_div = soup.find('div', class_='entry-text--fields-lbl', string=lambda t: t and 'Strona internetowa' in t)
    
    if main_div:
        
        etykieta_strona = main_div.find_next_sibling('div', class_='entry-text--fields-val')
        
        if etykieta_strona:
            strona_tekst = etykieta_strona.get_text(strip=True)
            print(f"Scraping | Strona internetowa: {strona_tekst}")
            return strona_tekst
           
    print("Scraping | Strona internetowa: nie znaleziono")
    return None

    
