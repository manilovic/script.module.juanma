from resources.tools import *
from resources.tools_settings import *

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import sys
import time
import os
import subprocess
import json
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode


####### MAIN #########



# Debug
debug ("JM ADDON INICIO")

#Settings buttons

debug("JM  sys.argv 0 >> " + str(sys.argv[0]))
debug("JM  sys.argv 1 >> " + str(sys.argv[1]))
debug("JM  sys.argv 2 >> " + str(sys.argv[2]))
debug("JM  sys.argv 3 >> " + str(sys.argv[3]))


if str(sys.argv[2]) == '?parar_acestream_2':
    parar_setting_acestream()

if str(sys.argv[2]) == '?limpiar_cache':
    limpiar_cache_setting()
    
if str(sys.argv[2]) == '?actualizar_links':
    actualizar_links_setting()
    
if str(sys.argv[2]) == '?todos_links_setting':
    todos_links_setting()


# Indentificar Sistema

debug("JM  Sistema es " + sistema())


#########

def build_url(query):

    return base_url + '?' + urllib.parse.urlencode(query)   #  {"name":"DAZN LaLiga MultiAudio", "link":"df98650743f24a245c44cdf2851e57078f4c487a"})
                                                                                 #  jm = urllib.parse.urlencode(y) # name=Laliga+multiaudio&link=167e3b44a520cd76d4372f6d30fe6d7ccd524175

####### MENUS CANALES ########

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urllib.parse.parse_qs(sys.argv[2][1:])


### click name
name = args.get('name', None)


### MENU canales

if name is None:

    xbmcplugin.setContent(addon_handle, 'movies')
    listing = []
    ruta_ids = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/ids.json")
    input_file = open(ruta_ids, mode='r')

    for line in input_file:
        y = json.loads(line)         #  {"name":"DAZN LaLiga MultiAudio", "link":"df98650743f24a245c44cdf2851e57078f4c487a"}
        url = build_url(y)                                     
        ruta_titulos = xbmcvfs.translatePath("special://home/addons/script.module.juanma/resources/titulos.txt")
        output_file = open(ruta_titulos, mode='w')
        print(y["name"], file=output_file)
        output_file.close()
        f = open(ruta_titulos, 'r')
        titulo = f.read()
        f.close()
        list_item = xbmcgui.ListItem(titulo)
        list_item.setInfo('video', {'title': titulo})
        list_item.setProperty('IsPlayable', 'false')  
        is_folder = False
        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(addon_handle)

    input_file.close()

### click canal

else:

    nombre = name[0]
    notificacion(nombre)
 
    link = args.get('link', None)
    url = link[0]

    ### Android API

    if sistema() == "android":  
        debug("JM  sistema android canal")
        notificacion("Sistema Android")
        AndroidActivity = 'StartAndroidActivity("","org.acestream.action.start_content","","acestream:?content_id=%s")' % url  ## %s por url
        debug("JM  Abriendo Android")
        xbmc.executebuiltin(AndroidActivity)
    
    ### Linux
    
    else:
        debug("JM Inicio Canal " + nombre + ": "+ url)
        canal(url,nombre)
        debug ("JM Final Canal")
    
    ###

#notificacion("Final")
debug ("JM ADDON FINAL")                                                                            

                                                
