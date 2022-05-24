import requests
from bs4 import BeautifulSoup
import time
import pymsgbox as pg
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import schedule
import datetime




stanowisko = ('finanse-ksiegowosc', 'administracja-biurowa')

gmail_address = 'marcin.automatyzacje@gmail.com'
password = 'P...3'

def send_email_alert_new(link, title):
    try:
        subject = f'NOWA OFERTA PRACY!! - {title}'
        
        msg = MIMEMultipart()
        msg['From'] = gmail_address
        msg['To'] = gmail_address
        msg['Subject'] = subject

        body = f'link: {link}'
        msg.attach(MIMEText(body, 'plain'))

        part = MIMEBase('application', 'octet-stream')

        text = msg.as_string()


        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_address, password)
        server.sendmail(gmail_address, 'marcink442@gmail.com', text)
        server.quit()
    except:
        print("błąd wysyłania")
        


def main():
    try:
        
        for st in stanowisko:
            site = f'https://www.pracuj.pl/praca/{st};kw/dzierzoniow;wp?rd=5'

            page = requests.get(site, timeout=60)
            soup = BeautifulSoup(page.content, "html.parser")

            for orders in soup.find_all('li', class_='results__list-container-item'):
                
                try:
                    title = orders.find('a', class_="offer-details__title-link").text
                    link = orders.find('a', class_="offer-details__title-link")['href']
                    
                    with open('oferty.csv', 'a+', encoding='UTF8') as file:
                        file.seek(0)                                          
                        if title not in file.read():                            
                            file.write(f'{title}; {link}\n') # in append mode writes will always go to the end, so no need to seek()
                            send_email_alert_new(link, title)
                            #wysylka_whatsapp(link)
                            print(f'wysyłam mail z pracuj: {title}')
                except:
                    pass
        

        
        
        for st in stanowisko:
            
            for page_nr in range(5):
                
                site = f'https://www.olx.pl/praca/{st}/dzierzoniow/?search%5Bdist%5D=5/?page={page_nr}'

                page = requests.get(site, timeout=60)
                soup = BeautifulSoup(page.content, "html.parser")

                for orders in soup.find_all('div', class_='offer-wrapper'):
                    
                    title=orders.find('strong').text.strip()
                    link = orders.find('a')['href']     
                    
                    with open('oferty.csv', 'a+', encoding='UTF8') as file:
                        file.seek(0)
                                          
                        if title not in file.read():                            
                            file.write(f'{title}; {link}\n') # in append mode writes will always go to the end, so no need to seek()
                            send_email_alert_new(link, title)
                            #wysylka_whatsapp(link)
                            print(f'wysyłam mail z olx: {title}')
          
        print(f'Progam działa -- {datetime.datetime.now()}')
    
    except Exception as err:
        print(err)
    
schedule.every(30).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
