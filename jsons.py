!/usr/bin/python
import platform
import pprint
import pymysql

####apt-get install libmysqlclient-dev
###mysql-connector-python
from mysql.connector import FieldType
import sys
import email, smtplib, ssl
import datetime
import os
import csv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText






if 1==2:
    print("-Hm Host Mysq\n-um User Mysql\n-pm Password mysql\n-bm Base de dades Mysql\n-tm Tabla mysql")
    print("-REP Repeteix l'enviament encara que així sigut enviat (nomes base de dades)")
    print("-AGRUPA Agrupa Emails que tenen el mateix correo (nomes per base de dades)")
    print("-PATH Path attachs , Si s'especifica asumeix que fitxers es el nom del fitxer sense el path")
    print("-EXT Estensió attachs  , Si s'especifica asumeix que fitxers es el nom del fitxer sense extensio i afegeix ext (ex pdf")
    print("-FSENDER Si s'especifica  pasara com a sender el valor i no necesitara la base de dades")
    print("-FSUBJECT Si s'especifica  pasara com a subject el valor i no necesitara la base de dades")
    print("-FSUBJECTS Si s'especifica  pasara com a subject en plural(si hi ha mes d'un fitxer el valor i no necesitara la base de dades")
    print("-CAMPOS Modifica los nombre de los campos de la tabla base de datos (-campos =sender=remitente;envio_id=codienviament")
    print("Los que no se indiquen tendran el valor por defecto")
    print("   id=id Identificacdor unic(INTEGER)")
    print("   sender=sender Remitent")
    print("   subject=subject Subject")
    print("   subjects=subjects Subject en cas de més d'un adjunt")
    print("   email=email Email d'envio")
    print("   fitxers=fitxers Fitxers adjunts")
    print("   vars=vars Variable")
    print("   envio_id='envio_id Codi d'enviament(INTEGER)")
    print("   fecha_envio='fecha_envio data enviament email(DATETIME)")
    print("   error=error Guard ok o l'error produit al intentar enviar")
    print("-BCC Envia missatge el mateix missatge al sender com a BCC")
