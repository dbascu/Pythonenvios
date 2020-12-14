#!/usr/bin/python

import platform
import pprint
import pymysql
import json
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
ldebug=0
path=""
csep = "  "

csql="""
CREATE TABLE `correo_envio_facturas` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`sender` VARCHAR(50) NOT NULL,
	`emailf` VARCHAR(50) NOT NULL,
	`subject` VARCHAR(500) NOT NULL,
	`factura` INT(11) NOT NULL,
	`fitxers` VARCHAR(500) NOT NULL,
	`vars` VARCHAR(500) NOT NULL,
	`error` VARCHAR(100) NOT NULL,
	`fecha_envio` DATETIME(6) NULL DEFAULT NULL,
	`codienvio` INT(11) NOT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=4
;



CREATE TABLE `Llista` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`envio_id` INT(11) NULL DEFAULT '0',
	`sender` VARCHAR(50) NULL DEFAULT '',
	`email` VARCHAR(50) NULL DEFAULT '',
	`subject` VARCHAR(250) NULL DEFAULT '',
	`fitxers` VARCHAR(250) NULL DEFAULT '',
	`vars` TEXT NULL,
	`error` VARCHAR(250) NULL DEFAULT NULL,
	`fecha_envio` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=4
;"""

def  getcursorgieldname(cursor,ltype=0,llong=0):
    cresult = []
    for d in cursor.description:
        print(d)
        if not ltype and not llong:
            cresult.append(d[0])
        else:
            print(FieldType.get_info(d[1]))
            dd=[d[0]]
            
            cresult.append(dd)        
#    print(cresult[0])
    print(cresult) 


def gettablefields(csql,lestable):
    connection=pymysql.connect(host=servermysql, user=usermysql, password=pwdmysql, db=bbdd, charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        if lestable:
            csql = "SELECT * from "+csql+" limit 0"
        cursor.execute(csql)
        ctemp=getcursorgieldname(cursor,1,1)
        print(ctemp)    
    cursor.close()


def treucamp(ccamp,cseparador):
    cresult=""
    ipos=ccamp.find(cseparador)
    if ipos>=0:
        if ipos==0:
            cresult=""
        else:
            cresult=ccamp[0:ipos]
        ccamp=ccamp[ipos+1:]
    else:
        cresult=ccamp
        ccamp=""
    return cresult,ccamp

def printinfo(info,lerror):
    i=0
    try:
        try:

           cfile=cpath+'/logs'
           if os.path.isdir(cfile)==False:
               os.makedirs(cfile)
           cfile=cfile +'/ENV'+datetime.datetime.now().strftime('%Y%m%d') + '.log'
           if (lerror==1):
               cnivel='ERROR'
           elif (lerror==2):
               cnivel='WARN'
           else:
               cnivel='INFO '
           ctemp =str(datetime.datetime.now())
           ctemp =ctemp+" "+cnivel+" "+info
           fh = open(cfile, "a")
           i=1
           fh.writelines(ctemp+'\n')
           print (ctemp)
           fh.close()
           i=0
        except:
            e = sys.exc_info()[0]
            print("ERROR c1! "+str(e)+" en Printifo")
    finally:
        i=0
        if i==1:
            fh.close()

            
    return

def sendemail(subject,bodyplain,bodyhtml,sender_email,receiver_email,filenames,cid,updatastatus):
    try:
        password = pwdmail;
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails
        cerror=""
        # Add body to email
        if bodyplain !="":
            message.attach(MIMEText(bodyplain, "plain"))
        if bodyhtml !="":
            message.attach(MIMEText(bodyhtml, "html"))
        for filename in filenames:
            if glpath!="":
                filename=glpath+filename;
            if glext!="":
                filename=filename+'.'+glext
            if os.path.isfile(filename):
                cpath, cfile = os.path.split(filename)
                with open(filename, "rb") as attachment:
                    # Add file as application/octet-stream
                    # Email client can usually download this automatically as attachment
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    # Encode file in ASCII characters to send by email    
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition','attachment; filename= "'+cfile+'"')
                # Add attachment to message and convert message to string
                message.attach(part)
            else:
                error="Error en attach "+filename
        text = message.as_string()
        try:
            try:
#                print("Serv Mail : "+sermail)
#                print(usermail)
#                print(password)
                server = smtplib.SMTP(sermail)
                server.login(usermail, password)
                if sendbcc == 1 :
                    rcpt=[sender_email]+ [receiver_email]
                else:
                    rcpt= receiver_email
                print("DESHA[BILITAT ENVIAMENT")
                server.sendmail(sender_email, rcpt, text)
            except Exception as e:
                printinfo(str(e)+" en Sendmail",1)
                cerror=str(e)
        finally:
            ctemp=sender_email+csep+receiver_email+csep+subject+csep
            if cerror=="":
                ctemp="OK"+csep+ctemp
                cupdate="OK"
            else:
                ctemp="ERROR"+csep+ctemp+csep+cerror
                cupdate="ERROR"+csep+cerror
            if updatastatus==1:
                 
                  while cid!="":
                     cids,cid=treucamp(cid,',')
                     updatenvio(cids,cupdate)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        printinfo(str(exc_type)+ " "+str(fname)+" "+ str(exc_tb.tb_lineno),1)
                     
                     
    return(ctemp);
        


def carregabody(cfilebodyhtml,cfilebodyplain):
    if(os.path.isfile(cfilebodyhtml)):
        bodyhtml = open(cfilebodyhtml, 'r').read()
    else:
        bodyhtml=""
    if(os.path.isfile(cfilebodyplain)):
        bodyplain = open(cfilebodyplain,'r').read()
    else:
        bodyplain=""
    return bodyhtml,bodyplain

def enviowithmy(cid,cfilebodyhtml,cfilebodyplain,agrupa,csub,csubs,csend,planhtml,planhtmls):


    cresult=""
    try:
        try:
            if csend=="":
                csend=glsender
            else:
                csend="'"+csend+"'"
            if csub=="":
                csub=glsubject
            else:
                csub="'"+csub+"'"
            if csubs=="":
                csubs=glsubjects
            else:
                csubs="'"+csubs+"'"

#subjects es subject en si mas de un fichero solo para envio multiples
#            print("Host : "+servermysql)
#            print("User :" +usermysql)
#            print("Pwd :"+pwdmysql)
#            print("bbdd : "+bbdd)
            connection=pymysql.connect(host=servermysql, user=usermysql, password=pwdmysql, db=bbdd, charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
#####mirar si glvars es literal i apunta a fields per afegri al select
            ctemp=glvars;
            cvars= ctemp.split("\n")
            campsex='';
            for clin in cvars:
               cvar,clin=treucamp(clin,"=")
               if clin[0:2]=='F:':
                     clin=(clin[2:]);
#                     print(clin)
                     if clin[-1]=="'":
                         clin=clin[:-1]
                     campsex=campsex+clin+','
                    
#                         print(clin)

#            cvar,clin=treucamp(clin,"=")

            print(campsex)
            
            with connection.cursor() as cursor:
                # Read a single record
                if agrupa==1:
                    
                    csql = """SELECT """+campsex+"""GROUP_CONCAT(CONVERT("""+glid+""",char(8)))  as id ,"""+csend+""" as sender,"""+csub+""" as subject,""" +csubs+""" as subjects,"""+glemail+""" as email,GROUP_CONCAT( """+glfitxers+""",',') fitxers,"""+glvars+""" vars,COUNT(*) AS c  from """+mytable+""" where """+glenvio_id+"""="""+str(cid)+""" and ifnull("""+glfecha_envio+""",'')='' group by """+glemail
#                    print(csql)
#                    print(csql)
                    #+" group by email"
                else:
                    
                    csql = """SELECT convert("""+glid+",char(8)) as id,"""+csend+""" as sender,"""+csub+""" as subject, '' as subjects,"""+glemail+ """ as email,"""+glfitxers+""" as fitxers,"""+glvars +"""  as vars, 1 as c from """+mytable+""" where """+glenvio_id+"""="""+str(cid)+""" and ifnull("""+glfecha_envio+""",'')=''"""
                print(csql)


         

                cursor.execute(csql)
                result = cursor.fetchall()
                bodyplain2='';
                bodyhtml2='';
#                bodyhtml,bodyplain=carregabody(cfilebodyhtml,cfilebodyplain)
                for row in result:

 #                   bodyhtml2= bodyhtml
 #                   bodyplain2=bodyplain
                    id=row['id']
                    if id[-1]==',':
                      id=id[:-1]
                    sender= row['sender']
                    email= row['email']
                    subject=row['subject']
                    subjects=row['subjects']                    
                    fitxers= row['fitxers']
                    ctemp=row['vars']
                    ccount=row['c']                    
                    
                    if (ccount==1) or  (planhtmls)=='':
                      bodyhtml2=planhtml
                    else:
                      bodyhtml2=planhtmls
                    
                    

 


                    cvars= ctemp.split("\n")

                    for clin in cvars:
                        cvar,clin=treucamp(clin,"=")
                        ###si el valor de  variable comença per 'F:' es un camp
                        if clin[0:2]=='F:':
                          clin=clin[2:]

#                          print(cvar)
#                          print(clin)
                          clin=row[clin]
                                        
                        bodyplain2 = bodyplain2.replace("<#"+cvar+"#>",clin)
                        bodyhtml2  = bodyhtml2.replace("<#"+cvar+"#>",clin) 
                    if cresult !="":
                        cresult=cresult+"\n" 
                    ctemp=bodyhtml2
#                    email='dagirona@hotmail.com' 
                    if ccount>1:
                        subject=subjects
                
                    ctemp=" Sender:"+sender+" Email: "+email+" Subject : "+subject+" No registres agrupats: "+str(ccount)
                    ctemp=sendemail(subject, bodyplain2,bodyhtml2,sender,email,fitxers.split(","),id,1)
                    cresult=cresult+ctemp
                cursor.close()
        except Exception as e:
              exc_type, exc_obj, exc_tb = sys.exc_info()
              fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
              printinfo(str(exc_type)+ " "+str(fname)+" "+ str(exc_tb.tb_lineno),1)        
    finally:
        return cresult
    

def enviowithtxt(cvars,cfilebodyhtml,cfilebodyplain):
    with open(cvars) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        bodyhtml,bodyplain=carregabody(cfilebodyhtml,cfilebodyplain)
        email=""
        subject=""
        fitxers=""
        sender=usermail
        cresult=""
        for row in csv_reader:
            if line_count == 0:
                camps= row 
            else:
                bodyhtml2= bodyhtml
                bodyplain2=bodyplain
                for icamps  in  range(len(camps)):
                    if camps[icamps] == "email":
                        email = row[icamps]
                    elif camps[icamps] == "subject":
                        subject = row[icamps]    
                    elif camps[icamps] == "fitxers":
                        fitxers = row[icamps]       
                    elif camps[icamps] == "sender":
                        sender = row[icamps]                                                            
                    else:
                         bodyplain2 = bodyplain2.replace("<#"+camps[icamps]+"#>",row[icamps])
                         bodyhtml2  = bodyhtml2.replace("<#"+camps[icamps]+"#>",row[icamps])                
                line_count += 1
                if cresult !="":
                    cresult=cresult+"\n"
                ctemp=sendemail(subject, bodyplain2,bodyhtml2,sender,email,fitxers.split(","),0,0)
                cresult=cresult+ctemp
            line_count += 1            
        return (cresult)            


def resetbbdd(cidenvio):
    try:
        error=0
        connection=pymysql.connect(host=servermysql, user=usermysql, password=pwdmysql, db=bbdd, charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            x=None
            csql="""update """+mytable+""" set """+glstatusenvio+"""=%s, """+glfecha_envio+"""=%s where """+glenvio_id+"""=%s"""
            cursor.execute(csql,("",None,cidenvio))
            connection.commit()
            cursor.close
    except Exception as e:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
          printinfo("Reset bbdd "+str(exc_type)+ " "+str(fname)+" "+ str(exc_tb.tb_lineno),1)        
    return error    

def updatenvio(cid,cresult):

    try:
        error=0
        connection=pymysql.connect(host=servermysql, user=usermysql, password=pwdmysql, db=bbdd, charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            x=None
            
            csql="""update """+mytable+"""  set """+glstatusenvio+"""=%s, """+glfecha_envio+"""=%s where """+glid+"""=%s"""
 #           print(csql)
#            print("cid "+str(cid))
            cursor.execute(csql,(cresult,datetime.datetime.now(),cid))
#            print("2")
            connection.commit()
            cursor.close
    except:
        e = sys.exc_info()[0]
        printinfo(str(e)+" Envio en resetbbdd",1)
        error=1
    return error    


def procesacampos(cvars):

    for clin in cvars.split(','):
        cvar,clin=treucamp(clin,"=")
        if cvar=='id':
            glid=clin
        elif cvar=='sender':
            glsender=clin
        elif cvar=='subject':
            glsubject=clin
        elif cvar=='subjecst':
            glsubjects=clin
        elif cvar=='email':
            glemail=clin        
        elif cvar=='fitxers':
            glfitxers=clin
        elif cvar=='vars':
            glvars=clin
        elif cvar=='envio_id':
            glenvio_id=clin
        elif cvar=='fecha_envo':
            glfecha_envio=clin
        elif cvar=='error':
            glstatusenvio=clin


def showhelp():
    print("-h help\n-H HOSTEMAIL\n-u USERIDMAIL\n-p Password\-e tipus envio 0-fitxer,sino indicar indicador mysql\n-bh fichero body html\n -bp ficher body en plano\n-v fichero csv con las variables")
#    print("-s Graba status en la base de datos")    
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


def getjsonparameters(jsonvar,key1,key2,key3,resultifnotfound):

  creturn=""
  try:
    if key3!="":
      creturn=jsonvar[key1][key2][key3]
    elif key2=="":
      creturn=jsonvar[key1]
    else:
      creturn=jsonvar[key1][key2]    
  except:
    creturn=resultifnotfound

  return(creturn)

def mainunit():

    global sendbcc
    global sermail,usermail,pwdmail
    global cpath
    global servermysql,usermysql,pwdmysql,bbdd,mytable
    global crepeticio
    global glid,glsender,glsubject,glemail,glfitxers,glvars,glenvio_id,glfecha_envio,glstatusenvio
    global glpath,glext
    global gliswindows

    if sys.platform.startswith('win')==True:
        gliswindows=1
    else:
        gliswindows=0


    glid='id'
    glsender='sender'
    glsubject='subject'
    glsubjects='subjects'
    glemail='email'
    glfitxers='fitxers'
    glvars='vars'
    glenvio_id='envio_id'
    glfecha_envio='fecha_envio'
    glstatusenvio='error'
    ccampos="";
    glpath=""
    glext=""
    forcedsender=""
    forcedsubject=""    
    forcedsubjects=""    


    agrupa=0
    crepeticio=0
    sendbcc=0
    cpath=(os.path.dirname(os.path.abspath(__file__)));
    cvar=cpath+'/vars.txt' 
    cfilebodyhtml=cpath+'/body.html'
    cfilebodyplain=cpath+'/body.txt'
    envio=99
    arguments = len(sys.argv) - 1
    planhtmls=''
    planhtml=''    
    if arguments==1 :
      with open(sys.argv[1], "r") as read_file:
          jsonparameters=json.load(read_file)
          sermail=getjsonparameters(jsonparameters,"mail","host","","localhost")
          usermail=getjsonparameters(jsonparameters,"mail","user","","")
          pwdmail=getjsonparameters(jsonparameters,"mail","password","","")

          servermysql=getjsonparameters(jsonparameters,"mysql","host","","localhost")
          usermysql=getjsonparameters(jsonparameters,"mysql","user","","")
          pwdmysql=getjsonparameters(jsonparameters,"mysql","password","","")
          bbdd=getjsonparameters(jsonparameters,"mysql","bbdd","","")
          mytable=getjsonparameters(jsonparameters,"mysql","table","","")






          glsender=getjsonparameters(jsonparameters,"mysql","fields","sender",glsender)
          glid=getjsonparameters(jsonparameters,"mysql","fields","id",glid)          
          glsubject=getjsonparameters(jsonparameters,"mysql","fields","subject",glsubject)                    
          glsubjects=getjsonparameters(jsonparameters,"mysql","fields","subjects",glsubjects)          
          glemail=getjsonparameters(jsonparameters,"mysql","fields","email",glemail)                    
          glfitxers=getjsonparameters(jsonparameters,"mysql","fields","email",glfitxers)                              
          glvars=getjsonparameters(jsonparameters,"mysql","fields","vars","")                              
          if glvars=="":
            glvars="'novars'"
          glenvio_id=getjsonparameters(jsonparameters,"mysql","fields","envio_id",glenvio_id)                              

          glfecha_envio=getjsonparameters(jsonparameters,"mysql","fields","fecha_envio",glfecha_envio)                              
          glstatusenvio=getjsonparameters(jsonparameters,"mysql","fields","status_envio",glstatusenvio)                                        





          glpath=getjsonparameters(jsonparameters,"path","","",glpath)

          glext=getjsonparameters(jsonparameters,"extension","","",glext)          


          forcedsubject=getjsonparameters(jsonparameters,"subject","","",forcedsubject)
          forcedsubjects=getjsonparameters(jsonparameters,"subjects","","",forcedsubjects)          
          forcedsender=getjsonparameters(jsonparameters,"sender","","",forcedsender)                    

          sendbcc=getjsonparameters(jsonparameters,"sendbccsender","","",sendbcc)                              
          agrupa=getjsonparameters(jsonparameters,"group","","",agrupa)                              
          crepeticio=getjsonparameters(jsonparameters,"repeat","","",crepeticio)                              
          envio=getjsonparameters(jsonparameters,"id","","",envio)                                        
          planhtml=getjsonparameters(jsonparameters,"plantillahtml","","","")                                        
          planhtmls=getjsonparameters(jsonparameters,"plantillahtmls","","","")                                                  


          


#    global sendbcc
#    global cpath
#    global servermysql,usermysql,pwdmysql,bbdd,mytable
#    global crepeticio
#    global glid,glsender,glsubject,glemail,glfitxers,glvars,glenvio_id,glfecha_envio,glerror
#    global glpath,glext

    else:
      i=1
      error=1
      while i<=arguments:
        error=1
        if sys.argv[i]=='-H':                
           i = i +1
           if i<=arguments:
              sermail=sys.argv[i]
              error=0
        elif sys.argv[i]=='-CAMPOS':                
           i = i +1
           if i<=arguments:
               for clin in sys.argv[i].split(','):
                   cvar,clin=treucamp(clin,"=")
                   if cvar=='id':
                       glid=clin
                   elif cvar=='sender':
                       glsender=clin
                   elif cvar=='subject':
                       glsubject=clin
                   elif cvar=='subjecst':
                       glsubjects=clin
                   elif cvar=='email':
                       glemail=clin        
                   elif cvar=='fitxers':
                       glfitxers=clin
                   elif cvar=='vars':
                       glvars=clin
                   elif cvar=='envio_id':
                       glenvio_id=clin
                   elif cvar=='fecha_envio':
                       glfecha_envio=clin
                   elif cvar=='error':
                       glstatusenvio=clin




#              procesacampos(sys.argv[i])
               error=0              

    
        elif sys.argv[i]=='-EXT':                
           i = i +1
           if i<=arguments:
              glext=sys.argv[i]
              error=0          
        elif sys.argv[i]=='-"-FSENDER':                
           i = i +1
           if i<=arguments:
              forcedsender=sys.argv[i]
              error=0                        
        elif sys.argv[i]=='-"-FSUBJECT':                
           i = i +1
           if i<=arguments:
              forcedsubject=sys.argv[i]
              error=0                        
        elif sys.argv[i]=='-"-FSUBJECTS':                
           i = i +1
           if i<=arguments:
              forcedsubjects=sys.argv[i]
              error=0                        
                   
        elif sys.argv[i]=='-PATH':                
           i = i +1
           if i<=arguments:
              glpath=sys.argv[i]
              if (gliswindows==1) and (glpath[-1]!='\\'):
                  glpath=glpath+'\\';
              if (gliswindows==0) and (glpath[-1]!='/'):
                  glpath=glpath+'/';
              error=0               
        elif sys.argv[i]=='-Hm':                
           i = i +1
           if i<=arguments:
              servermysql=sys.argv[i]
              error=0
        elif sys.argv[i]=='-um':                
           i = i +1
           if i<=arguments:
              usermysql=sys.argv[i]
              error=0
        elif sys.argv[i]=='-pm':                
           i = i +1
           if i<=arguments:
              pwdmysql=sys.argv[i]
              error=0
        elif sys.argv[i]=='-bm':                
           i = i +1
           if i<=arguments:
              bbdd=sys.argv[i]
              error=0
        elif sys.argv[i]=='-tm':                
           i = i +1
           if i<=arguments:
              mytable=sys.argv[i]
              error=0
#        elif sys.argv[i]=='-s':                
#            envioenbbdd=1            
#            error=0
        elif sys.argv[i]=='-AGRUPA':                
            agrupa=1
            error=0                           
        elif sys.argv[i]=='-BCC':                
            sendbcc=1
            error=0                           
        elif sys.argv[i]=='-REP':                
            crepeticio=1            
            error=0                           
        elif sys.argv[i]=='-u':                
            i = i +1
            if i<=arguments:
                usermail=sys.argv[i]
                error=0
        elif sys.argv[i]=='-p':                
            i = i +1
            if i<=arguments:
               pwdmail=sys.argv[i]
               error=0
        elif sys.argv[i]=='-e':                
            i = i +1
            if i<=arguments:
               envio=sys.argv[i]
               error=0               
        if error==1:
            showhelp()
            quit();            
        i=i+1
      if error==1:
        showhelp()
        quit();            
      cresult=""










#    print("aaa"+glenvio_id)




    if 1 == 0:
        print(jsonparameters);
        ####fem probes#####
        ###temajson###
#        gettablefields('correo_lenvio2',1)
    else:
        if envio == "0":
            cresult = enviowithtxt(cvar,cfilebodyhtml,cfilebodyplain)
        else:
            if (crepeticio==1):
                resetbbdd(envio)
            cresult= enviowithmy(envio,cfilebodyhtml,cfilebodyplain,agrupa,forcedsubject,forcedsubjects,forcedsender,planhtml,planhtmls)
            

if __name__ == '__main__':
    mainunit()            