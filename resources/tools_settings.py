import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import subprocess
import sys
import time
import os
import platform
import urllib.request
import re
import json

from resources.tools import *


def parar_setting_acestream():
    
    if "ANDROID_STORAGE" in os.environ:
        SO = "android"
        exit(0)

    if sistema() == "Ubuntu":
        pkill_acestream = "pkill acestream"
        subprocess.run(pkill_acestream, shell=True)
        debug("JM  Parada Forzosa Acestream UBUNTU")
    elif sistema() == "arm":
        ruta_acestream_stop = xbmcvfs.translatePath("special://home/userdata/addon_data/script.module.horus/acestream.engine/acestream.stop")
        subprocess.run([ "sudo", ruta_acestream_stop ]) 
        debug ("JM  Parada Forzosa Acestream ARM")
    else:
        pass

    time.sleep(2)

    p = subprocess.run('ps -ef | grep aces', shell=True, capture_output=True)    ###'minipc     60569   60567  0 23:07 pts/0    00:00:00 grep aces\n'
    if not b'acestream' in p.stdout:
        notificacion("Motor Acestream cerrado")
        debug("JM  Motor Acestream cerrado")
    else:
        notificacion("Motor Acestream NO cerrado")
        debug("JM  Motor Acestream NO cerrado")

    time.sleep(2)

    return(debug("JM  Motor Acestream parado"))
    

def limpiar_cache_setting():
        
    if "ANDROID_STORAGE" in os.environ:
        SO = "android"
        exit(0)

    if sistema() == "Ubuntu":
        comando = "find  /home/minipc/snap/acestreamplayer/??/.ACEStream/.acestream_cache/* -maxdepth 1 -mmin +120"
        subprocess.run(comando, shell=True)
        notificacion("Limpiando cache")
        debug("JM  Limpiando caché")
    elif sistema() == "arm":
        comando = "find  /home/minipc/snap/acestreamplayer/??/.ACEStream/.acestream_cache/* -maxdepth 1 -mmin +120"
        subprocess.run(comando, shell=True)
        notificacion("Limpiando cache")
        debug("JM  Limpiando caché")
    else:
        pass

    notificacion("Caché limpiado")
    return(debug("JM  Caché limpiado"))


def actualizar_links_setting():

    notificacion("Actualizando links acestream")
    debug ("JM  Actualizando links acestream")

    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    file_ids = open(ruta_ids, mode='w')

    response = urllib.request.urlopen("https://hackmd.io/@DEPORTES/AP-ID")
    html = response.read().decode('utf-8')

    canales = ["DAZN LaLiga 1080p","DAZN LaLiga 2","M. LaLiga 1080p","M. LaLiga 2 ","M.L. Campeones 1080p","M.L. Campeones 2","M. Deportes 1080p","DAZN 1", "DAZN 2","DAZN F1 1080p","M. Golf 1080p"]

    for x in canales:

        start = html.find(x)
        end =  start + 300
        busqueda = html[start:end]
        busqueda = busqueda.split('\n', 1)[0]
        
        while "acestream" in busqueda:
            start = busqueda.find("acestream://")
            end = start + 52
            ace_link = busqueda[start:end]              ## acestream://60cf60019aeef9af6.... ##
            busqueda = busqueda.replace(ace_link, " ")  ## borramos para siguiente iteraccion ##

            ace_link = ace_link.replace("acestream://","")
            items ={"name":x, "link":ace_link}
            y = json.dumps(items)
            
            file_ids.write(y)
            file_ids.write("\n")


    file_ids.close()
    notificacion("Links actualizados")
    debug ("JM  Links actualizados")


def todos_links_setting():

    notificacion("Actualizando lista completa links")
    debug ("JM  Actualizando lista completa links")

    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    file_ids = open(ruta_ids, mode='w')

    response = urllib.request.urlopen("https://hackmd.io/@DEPORTES/AP-ID")
    html = response.read().decode('utf-8')


    for item in html.split("\n"):
        if "arrow" in item:
            busqueda= item.strip()
            start = busqueda.find("**")
            end = busqueda.find("[:arrow")
            busqueda = busqueda[start:end]
            x = busqueda.replace("**","")
            x = x.strip()  #x = "DAZN LaLiga1080p MultiAudio"

            start = html.find(x)
            end =  start + 300
            busqueda = html[start:end]
            busqueda = busqueda.split('\n', 1)[0]

            while "acestream" in busqueda:
                start = busqueda.find("acestream://")
                end = start + 52
                ace_link = busqueda[start:end]              ## acestream://60cf60019aeef9af6.... ##
                busqueda = busqueda.replace(ace_link, " ")  ## borramos para siguiente iteraccion ##

                ace_link = ace_link.replace("acestream://","")
                items ={"name":x, "link":ace_link}
                y = json.dumps(items)
                
                file_ids.write(y)
                file_ids.write("\n")


    file_ids.close()
    notificacion("Links actualizados")
    debug ("JM  Links actualizados")
