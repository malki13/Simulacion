import cv2
import numpy as np
from datetime import date
from datetime import datetime
import pandas as pd
import smtplib
import email.message
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import make_msgid
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pyautogui
from io import BytesIO
import win32clipboard
from PIL import Image
from time import sleep
import pytest
import time
import json
from time import gmtime, strftime
import tweepy

def crear_imagen():
    #Imagen con Frases
    imagen = cv2.imread('presidente.jpg')
    imagenFlayer = imagen.copy()
    #Día actual
    today = date.today()
    now = datetime.now()
    hora = str(today)+' '+str(now.hour)+":"+str(now.minute)
    cv2.putText(imagenFlayer,hora,(10,340),cv2.FONT_HERSHEY_COMPLEX,0.4,(255,255,255),2)
    cv2.putText(imagenFlayer,"Por un mejor Ecuador",(10,100),cv2.FONT_HERSHEY_COMPLEX,0.5,(19,17,51),2)
    cv2.putText(imagenFlayer,"La decision en tus manos",(10,280),cv2.FONT_HERSHEY_COMPLEX,0.5,(19,17,51),2)
    cv2.imwrite('c:/Users/Usuario/Documents/UNIVERSIDAD/imagenPublicidad.jpg',imagenFlayer)
    cv2.waitKey(0)

def leer_documento():
    sheet_url = 'https://docs.google.com/spreadsheets/d/1nB-R0r-HlNBxkIj7gGqKpvA37iPwn4bujdEk2WwRzVY/edit#gid=1671894497'
    csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df=pd.read_csv(csv_export_url)
    return df
def enviar_correo():
    #leemos el documento con los correos
    usuarios = leer_documento()
    # creamos la imagen publicitaria
    crear_imagen()
    # direccion del correo de quien lo envia
    me = "elecciones.simulacion.final@gmail.com"
    
    #enviar mensaje via SMTP server
    def connect(tls=False):
        try:
            s = smtplib.SMTP('smtp.gmail.com:587')
            if tls:
                s.starttls()
            s.login("elecciones.simulacion.final@gmail.com","Simulacion2021")
            return s
        except Exception:
            sys.exit()

    s=connect(True)

    # Cuerpo del mensaje en HTML
    text = """
    Contenido en texto plano
    \n Elecciones 2021
    \n\n Republica Democratrica del Ecuador
    """
    html = """
    <html>
    <head>
        <style type="text/css">
            .link {text-decoration:underline;color:#00f;}
            body {font-size:14;}
        </style>
    </head>
    <body>
        <b>Contenido en HTML</b>
        <p>Elecciones Presidenciales Febrero-2021</p>
        <p>SIMULACION-UPS</p>
    </body>
    </html>
    """

    # parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain', 'UTF-8')
    part2 = MIMEText(html, 'html', 'UTF-8')

    # Cogemos la imagen y la añadimos al correo
    fp=open("imagenPublicidad.jpg", 'rb')
    image1 = MIMEImage(_imagedata=fp.read(),_subtype="jpeg")
    fp.close()
    for i in range(len(usuarios)):
        print(usuarios["correo"][i])
        msg = MIMEMultipart('alternative')
        msg.set_charset("UTF-8")
        msg['Subject'] = "Envio de correo Examen-Simulacion"
        msg['From'] = me
        msg['To'] = usuarios["correo"][i]
        msg['Date'] = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        msg['Message-ID'] = "<%s@%s>" % (make_msgid()[1:].split('@')[0],usuarios["correo"][i].split('@')[1])
        msg.attach(part1)
        msg.attach(part2)
        msg.attach(image1)

        try:
            s.sendmail(me, usuarios["correo"][i], msg.as_string())
        except Exception:
            print(usuarios["correo"][i])
            print ("---------------------------------")
            s=connect()
    s.quit()
def main():
    enviar_correo()

    usr = "elecciones.simulacion.final@gmail.com"
    pwd = "Simulacion2021"
    
    PATH = 'msedgedriver.exe'
    browser = webdriver.Edge(executable_path=PATH)
    browser.get("http://www.facebook.com")
    sleep(2)
    
    text_urr = browser.find_element_by_id("email")
    text_urr.send_keys(usr)
    text_pwd = browser.find_element_by_id("pass")
    text_pwd.send_keys(pwd)
  
    text_pwd.send_keys(Keys.RETURN)
    sleep(20)
    
    loguin = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[3]/div/div[2]/div/div/div/div[2]/div[2]/div[1]/span[2]/span").click()
    sleep(5)
    
    pyautogui.write(r"C:\Users\Usuario\Documents\UNIVERSIDAD\imagenPublicidad.jpg")
    pyautogui.press("enter")
    
    sleep(5)
    loguin = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div[3]/div[2]/div").click()

main()