import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import subprocess
import sys
import time
import os
import platform




def debug(message):

    log_enabled = getsetting("debug")
    if log_enabled == "true":
        xbmc.log(message, xbmc.LOGINFO)


def importar(addon_id):

    ADDON = xbmcaddon.Addon(addon_id)          #ADDON = xbmcaddon.Addon('script.module.horus')
    addon_dir = ADDON.getAddonInfo('path')     #horus_dir = ADDON.getAddonInfo('path')
    sys.path.append(os.path.join(addon_dir))
    debug(str(sys.path))                       #Ahora podemos importar acestream de horus:

def sistema():

    
    if "ANDROID_STORAGE" in os.environ:
        SO = "android"

    elif "Linux" in platform.system():
        x = "Linux"
        if "Ubuntu" in platform.version():
            SO = "Ubuntu"
        elif "arm" in os.uname()[4]:    # if "linux" and "arm"  >> 'osmc','openelec','raspbian','raspios'
            SO = "arm"
        
    return(SO)


def getsetting(settingname):

    setting = xbmcaddon.Addon().getSetting(settingname)
    return setting


def notificacion(line1):

    __addon__ = xbmcaddon.Addon()
    __addonname__ = __addon__.getAddonInfo('name')
    __icon__ = __addon__.getAddonInfo('icon')
    #line1 = "No Server"
    timeml = 5000 #in miliseconds
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeml, __icon__))
   
   
def arrancar_acestream():
    
                   # if "linux" and "arm"  >> 'osmc','openelec','raspbian','raspios'
    if sistema() == "arm":
        ruta_acestream_start = xbmcvfs.translatePath("special://home/userdata/addon_data/script.module.horus/acestream.engine/acestream.start")
        command = ("sudo " + ruta_acestream_start + " &")
        debug("JM  Arrancando Acestream ARM")
        notificacion("Arrancando Acestream ARM")
        subprocess.run(command, shell=True)     

    elif sistema() == "Ubuntu":
        if os.path.exists('/snap/acestreamplayer'):
            comando = "snap run acestreamplayer.engine &"
            subprocess.run(comando, shell=True)
            notificacion("Arrancando Acestream Ubuntu SNAP")
            debug("JM  Arrancando Acestream Ubuntu SNAP")
        else:
            xbmcgui.Dialog().ok("Error", "Por favor, instale Acestreamplayer mediante snap antes de continuar.")
            return
     
    return(debug("JM  Arrancado"))
        

def parar_acestream():


    log_enabled = getsetting("stop_acestream")
    if log_enabled == "true":

        stop_acestream = getsetting("stop_acestream")
        if  stop_acestream == "true" and sistema() == "Ubuntu":
            pkill_acestream = "pkill acestream"
            subprocess.run(pkill_acestream, shell=True)
            debug("JM  Stop Acestream UBUNTU")
        elif  stop_acestream == "true" and sistema() == "arm":
            ruta_acestream_stop = xbmcvfs.translatePath("special://home/userdata/addon_data/script.module.horus/acestream.engine/acestream.stop")
            subprocess.run([ "sudo", ruta_acestream_stop ]) 
            debug ("JM  Stop Acestream ARM")

        else:
            debug ("JM  Android")

        time.sleep(2)

        p = subprocess.run('ps -ef | grep aces', shell=True, capture_output=True)    ###'minipc     60569   60567  0 23:07 pts/0    00:00:00 grep aces\n'
        if not b'acestream' in p.stdout:
            notificacion("Motor Acestream cerrado")
            debug("JM  Motor Acestream cerrado")
        else:
            notificacion("Motor Acestream NO cerrado")
            debug("JM  Motor Acestream NO cerrado")

        time.sleep(2)

        return(debug("JM  Acestream parado"))
    
    else:
        debug("JM  No setting parar activado")


def canal(url,nombre):

    importar('script.module.horus')

    from lib.acestream.server import Server
    from lib.acestream.engine import Engine
    from lib.acestream.stream import Stream

    debug("JM Stream: " + nombre + " id: " + url)

    arrancar_acestream()  #### ARRANCAR

    server = Server(host='127.0.0.1', port=6878)
    
    while not server.available:
        debug("JM  No Server")
        notificacion("No Server")
        time.sleep(2)
 
    stream = Stream(server, id=url)
    stream.start()
    
    #### box
    d = xbmcgui.DialogProgress()
    d.create(nombre)
    timedown = time.time() + 80

    while (stream.status != "dl" ) and not d.iscanceled() and time.time() < timedown:
        seg = int(timedown - time.time())
        progreso = int((seg * 100) / 80)
        line1 = "Abriendo Stream >> " + str(stream.status)
        line2 = "Download: %s Kb/s" % stream.stats.speed_down
        line3 = "Seeds:    %s" % stream.stats.peers
        line4 = "Timeout: %s seconds" % seg
        d.update(progreso, '\n'.join([line1, line2, line3, line4]))
        time.sleep(0.5)

    d.close()

    if d.iscanceled() or time.time() >= timedown:
        notificacion("Cancelado o tiempo agotado")
        sys.exit(0)
    #### box

    
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    listitem = xbmcgui.ListItem()
    listitem.setProperty('IsPlayable', 'true')
    listitem.setInfo('video', {'Title': nombre})
    playlist.add(url=stream.playback_url, listitem=listitem)
    monitor = xbmc.Monitor()
    xbmc.Player().play(playlist)
    while xbmc.Player().isPlaying() and not monitor.abortRequested():
        monitor.waitForAbort(1)
    xbmc.Player().stop()


    parar_acestream()  #### PARAR

    return(debug("JM  Canal cerrado")) 
