#echo 1111

#tar cvfz /tmp/1.tgz /var/x
#mv /tmp/1.tgz /var/x/a/1.tgz
#-REP REPTETIR
#-BCC ENVIA COPIA OCULTA AL SENDER
#python3 x.py -h
#python3 x.py  -BCC -REP   -H mail.tinaneteges.com  -u info@tinaneteges.com  -p Sergi2012   -e 3 -Hm localhost -bm admin_t1 -um admin_t1 -pm 60606060  -tm correo_lenvio2 

#python3 x.py   -BCC -REP   -H mail.tinaneteges.com  -u info@tinaneteges.com  -p Sergi2012   -e 4 -Hm localhost -bm admin_t1 -um admin_t1 -pm 60606060  -tm correo_lenvio2 

#python3 x.py   -AGRUPA  -REP   -H mail.tinaneteges.com  -u info@tinaneteges.com  -p Sergi2012   -e 1 -Hm localhost -bm admin_t1 -um admin_t1 -pm 60606060  -tm correo_envio_facturas

#python3 x.py    -AGRUPA -FSENDER dagirona@hotmail.com -FSUBJECT SSSSsingu -FSUBJECTS sssPlural -FSU-REP -PATH /home/admin/python/s -EXT txt -CAMPOS erro=error_envio_factura,envio_id=id_envio_factura,email=email_facturacion -H mail.tinaneteges.com  -u info@tinaneteges.com  -p Sergi2012   -e 1 -Hm localhost -bm admin_t1 -um admin_t1 -pm 60606060  -tm correo_envio_facturas

#python3 x.py    -AGRUPA -FSENDER dagirona@hotmail.com -FSUBJECT SSSSsingu -FSUBJECTS sssPlural -FSU-REP -PATH /home/admin/python/s -EXT txt -CAMPOS erro=error_envio_factura,envio_id=id_envio_factura,email=email_facturacion -H mail.tinaneteges.com  -u info@tinaneteges.com  -p Sergi2012   -e 1 -Hm localhost -bm admin_t1 -um admin_t1 -pm 60606060  -tm cabe2020

#             if cvar=='id':
#                       glid=clin
#                   elif cvar=='sender':
#                       glsender=clin
#                   elif cvar=='subject':
#                       glsubject=clin
#                   elif cvar=='subjecst':
#                       glsubjects=clin
#                   elif cvar=='email':
#                       glemail=clin
#                   elif cvar=='fitxers':
#                       glfitxers=clin
#                   elif cvar=='vars':
#                       glvars=clin
#                   elif cvar=='envio_id':
#                       glenvio_id=clin
#                   elif cvar=='fecha_envo':
#                       glfecha_envio=clin
#                   elif cvar=='error':
#                       glerror=clin


#rm /var/x/a/1.tgz


#    'NAME': 'admin_t1',
#        'USER': 'admin_t1',
#        'PASSWORD': '60606060',

python3 x.py ss.json
#echo $?