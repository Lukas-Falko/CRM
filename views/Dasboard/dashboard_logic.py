import requests



url = "https://www.gramwzielone.pl"

def czy_online():
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        # Zwracamy sam numer kodu (np. 200)
        return response.status_code 
    except Exception as e:
        # Jeśli strona w ogóle nie odpowie, zwracamy np. 0 lub błąd
        return 0 

