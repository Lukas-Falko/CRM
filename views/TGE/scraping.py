import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import pandas as pd
import threading
import customtkinter as ctk
from tkinter import messagebox
import os

# Ustawienia wyglądu
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def run_scraper(self, start_str, end_str, save_path=None):
        try:
            
            start_delivery = datetime.strptime(start_str, "%d-%m-%Y")
            end_delivery = datetime.strptime(end_str, "%d-%m-%Y")
            
            if start_delivery > end_delivery:
                self.log("BŁĄD: Data początkowa > końcowa!")
                self.reset_ui()
                return

            all_results = []
            
           
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://tge.pl/energia-elektryczna-rdn',
                'DNT': '1', 
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            current_delivery = start_delivery
            while current_delivery <= end_delivery:
                
               
                pub_date = current_delivery - timedelta(days=1)
                pub_str = pub_date.strftime("%d-%m-%Y")
                del_str = current_delivery.strftime("%d-%m-%Y")
                
                self.log(f"Cel: Dostawa {del_str} (Pobieram z publ. {pub_str})")
                
                url = f"https://tge.pl/energia-elektryczna-rdn?dateShow={pub_str}&dateAction="
                
                try:
                    res = requests.get(url, headers=headers, timeout=10)
                    if res.status_code == 200:
                        soup = BeautifulSoup(res.text, 'html.parser')
                        tabela = soup.find('table', id='rdn')
                        
                        if tabela and tabela.find('tbody'):
                            rows = tabela.find('tbody').find_all('tr')

                            for tr in rows:
                                tds = tr.find_all('td')

                                if len(tds) >= 3:
                                    ident = tds[0].get_text(strip=True)
                                    
                            
                                    match = re.search(r"_(H\d{2}[A-Za-z]?)", ident)
                                    if match:
                                        godzina_clean = match.group(1) 
                                        
                                        cena_raw = tds[2].get_text(strip=True)
                                        
                                        
                                        if cena_raw == '-':
                                            cena_val = None
                                        else:
                                           
                                            cena_clean = cena_raw.replace(' ', '').replace('\xa0', '').replace(',', '.')
                                            try:
                                                cena_val = float(cena_clean)
                                            except ValueError:
                                                cena_val = None
                                                
                                        all_results.append({
                                            'Data Dostawy': del_str,  
                                            'Godzina': f"Godz. {godzina_clean}",
                                            'Cena': cena_val
                                        })
                    time.sleep(0.5) 
                except Exception as e:
                    self.log(f"Błąd dla {del_str}: {str(e)}")

                current_delivery += timedelta(days=1)

            

            
            if all_results:
                df_raw = pd.DataFrame(all_results)
                
                df_pivot = df_raw.pivot(index='Godzina', columns='Data Dostawy', values='Cena')
                
                df_pivot = df_pivot.sort_index()
                
                filename = f"TGE_Pionowy_{start_str}_{end_str}.xlsx"
                
                if save_path:
                    try:
                        os.makedirs(save_path, exist_ok=True)
                        fullpath = os.path.join(save_path, filename)
                    except Exception:
                        fullpath = filename
                else:
                    fullpath = filename

                writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')
                df_pivot.to_excel(writer, sheet_name='Ceny_RDN')

                workbook  = writer.book
                worksheet = writer.sheets['Ceny_RDN']

                
                header_fmt = workbook.add_format({
                    'bold': True, 'align': 'center', 'valign': 'vcenter',
                    'fg_color': '#4F81BD', 'font_color': 'white', 'border': 1
                })
                cell_fmt = workbook.add_format({
                    'align': 'center', 'valign': 'vcenter', 'border': 1, 'num_format': '#,##0.00'
                })

                worksheet.write(0, 0, 'Godzina / Data', header_fmt)

                
                for col_num, value in enumerate(df_pivot.columns.values):
                    worksheet.write(0, col_num + 1, value, header_fmt)
                
                worksheet.set_column(0, 0, 15, cell_fmt)

                num_dates = len(df_pivot.columns)
                worksheet.set_column(1, num_dates, 12, cell_fmt)

                writer.close()
                self.log(f"GOTOWE! Tabela transponowana w pliku: {fullpath}")
                messagebox.showinfo("Sukces", "Wygenerowano tabelę: Daty w poziomie, Godziny w pionie.")
            else:
                self.log("Brak danych do zapisu.")

        except Exception as e:
            self.log(f"Błąd krytyczny: {str(e)}")
        
        self.reset_ui()