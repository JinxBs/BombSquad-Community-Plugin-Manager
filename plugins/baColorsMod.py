"""Colors Mod."""
#Mod by Froshlee14
# ba_meta require api 6

from __future__ import annotations
from typing import TYPE_CHECKING

import _ba, ba

if TYPE_CHECKING:
    pass

from bastd.actor.spazfactory import SpazFactory
from bastd.actor.scoreboard import Scoreboard
from bastd.game.elimination import EliminationGame, Icon, Player, Team
from bastd.gameutils import SharedObjects

from ba.internal import get_player_colors,get_player_profile_colors, get_player_profile_icon
from bastd.ui.popup import PopupWindow
from bastd.actor import bomb, spaz
from bastd.ui import tabs, confirm, mainmenu, popup
from bastd.ui.colorpicker import ColorPicker
from bastd.ui.mainmenu import MainMenuWindow
from bastd.ui.profile.browser import *
from bastd.actor.playerspaz import *
from bastd.actor.flag import *
from bastd.actor.spazbot import *
from bastd.actor.spazfactory import SpazFactory
#from bastd.mainmenu import MainMenuActivity
import random


#######################

#######################

def getData(data):
    return ba.app.config["colorsMod"][data]

def getRandomColor():
    c = random.choice(getData("colors"))
    return c

def doColorMenu(self):
    ba.containerwidget(edit=self._root_widget,transition='out_left')
    openWindow()

def updateButton(self):
    color = (random.random(),random.random(),random.random())
    try:
        ba.buttonwidget(edit=self._colorsModButton,color=color)
    except Exception:
        self._timer = None

newConfig = {"colorPlayer":True,
             "higlightPlayer":False,
             "namePlayer":False,
             "glowColor":False,
             "glowHighlight":False,
             "glowName":False,
             "actab":1,
             "shieldColor":False,
             "xplotionColor":True,
             "delScorch":True,
             "colorBots":False,
             "glowBots":False,
             "flag":True,
             #"test":True,
             "glowScale":1,
             "timeDelay":500,
             "activeProfiles":['__account__'],
             "colors":[color for color in get_player_colors()],
            }

def getDefaultSettings():
    return newConfig

def getTranslation(text):
    actLan = _ba.app.lang.language
    colorsModsLan = {
        "title":{
            "Spanish":'Colors Mod',
            "English":'Colors Mod'
        },
        "player_tab":{
            "Spanish":'Ajustes de Jugador',
            "English":'Player settings'
        },
        "extras_tab":{
            "Spanish":'Ajustes Adicionales',
            "English":'Adittional settings'
        },
        "general_tab":{
            "Spanish":'Ajustes Generales',
            "English":'General settings'
        },
        "info_tab":{
            "Spanish":'Creditos',
            "English":'Credits'
        },
        "profiles":{
            "Spanish":'Perfiles',
            "English":'Profiles'
        },
        "palette":{
            "Spanish":'Paleta de Colores',
            "English":'Pallete'
        },
        "change":{
            "Spanish":'Cambiar',
            "English":'Change'
        },
        "glow":{
            "Spanish":'Brillar',
            "English":'Glow'
        },
        "glow_scale":{
            "Spanish":'Escala de Brillo',
            "English":'Glow Scale'
        },
        "time_delay":{
            "Spanish":'Intervalo de Tiempo',
            "English":'Time Delay'
        },
        "reset_values":{
            "Spanish":'Reiniciar Valores',
            "English":'Reset Values'
        },
        "players":{
            "Spanish":'Jugadores',
            "English":'Players'
        },
        "apply_to_color":{
            "Spanish":'Color Principal',
            "English":'Main Color'
        },
        "apply_to_highlight":{
            "Spanish":'Color de Resalte',
            "English":'Highlight Color'
        },
        "apply_to_name":{
            "Spanish":'Color del Nombre',
            "English":'Name Color'
        },
        "additional_features":{
            "Spanish":'Ajustes Adicionales',
            "English":'Additional Features'
        },
        "apply_to_bots":{
            "Spanish":'Color Principal de Bots',
            "English":'Bots Main Color'
        },
        "apply_to_shields":{
            "Spanish":'Escudos de Colores',
            "English":'Apply to Shields'
        },
        "apply_to_explotions":{
            "Spanish":'Explosiones de Colores',
            "English":'Apply to Explotions'
        },
        "apply_to_flags":{
            "Spanish":'Banderas de Colores',
            "English":'Apply to Flags'
        },
        "pick_color":{
            "Spanish":'Selecciona un Color',
            "English":'Pick a Color'
        },
        "add_color":{
            "Spanish":'Agregar Color',
            "English":'Add Color'
        },
        "remove_color":{
            "Spanish":'Quitar Color',
            "English":'Remove Color'
        },
        "clean_explotions":{
            "Spanish":'Limpiar Explosiones',
            "English":'Remove Scorch'
        },
        "restore_default_settings":{
            "Spanish":'Restaurar Ajustes Por Defecto',
            "English":'Restore Default Settings'
        },
        "settings_restored":{
            "Spanish":'Ajustes Restaurados',
            "English":'Settings Restored'
        },
        "restore_settings":{
            "Spanish":'¿Restaurar Ajustes Por Defecto?',
            "English":'Restore Default Settings?'
        },
        "nothing_selected":{
            "Spanish":'Nada Seleccionado',
            "English":'Nothing Selected'
        },
        "color_already":{
            "Spanish":'Este Color Ya Existe En La Paleta',
            "English":'Color Already In The Palette'
        },
        "tap_color":{
            "Spanish":'Toca un color para quitarlo.',
            "English":'Tap to remove a color.'
        },
    }
    lans = ["Spanish","English"]
    if actLan not in lans:
        actLan = "English"
    return colorsModsLan[text][actLan]
    

# ba_meta export plugin
class ColorsMod(ba.Plugin):

  # PLUGINS PLUS COMPATIBILITY
  version = 1.7
  logo = 'gameCenterIcon'
  logo_color = (1,1,1)
  plugin_type = 'mod'
  settings = True

  if _ba.app.lang.language == "Spanish":
    information = ("Modifica y aplica efectos\n"
           	                "a los colores de tu personaje,\n"
           	                "explosiones, bots, escudos,\n"
                            "entre otras cosas...\n\n"
                            "Programado por Froshlee14\nTraducido por CerdoGordo\n\n"
                            "ADVERTENCIA\nEste mod puede ocacionar\n"
                            "efectos de epilepsia\na personas sensibles.")
  else:
    information = ("Modify and add effects\n"
           	                "to your character colours.\n"
                            "And other stuff...\n\n"
                            "Coded by Froshlee14\nTranslated by CerdoGordo\n\n"
                            "WARNING\nThis mod can cause epileptic\n"
                            "seizures especially\nwith sensitive people")
  def openWindow(self):
    ColorsMenu()

  #

  def on_app_launch(self) -> None:

    if "colorsMod" in ba.app.config:
        oldConfig = ba.app.config["colorsMod"]
        for setting in newConfig:
            if setting not in oldConfig:
                ba.app.config["colorsMod"].update({setting:newConfig[setting]})
                ba.screenmessage(('Colors Mod: config updated'),color=(1,1,0))

        removeList = []
        for setting in oldConfig:
            if setting not in newConfig:
                removeList.append(setting)
        for element in removeList :
            ba.app.config["colorsMod"].pop(element)
            ba.screenmessage(('Colors Mod: old config deleted'),color=(1,1,0))
    else:
        ba.app.config["colorsMod"] = newConfig
    ba.app.config.apply_and_commit()


    #MainMenuActivity.oldMakeWord = MainMenuActivity._make_word
    #def newMakeWord(self, word: str,
    #               x: float,
    #               y: float,
    #               scale: float = 1.0,
    #               delay: float = 0.0,
    #               vr_depth_offset: float = 0.0,
    #               shadow: bool = False):
    #    self.oldMakeWord(word,x,y,scale,delay,vr_depth_offset,shadow)
    #    word = self._word_actors[-1]
    #    if word.node.getnodetype():
    #        if word.node.color[3] == 1.0:
    #            word.node.color = getRandomColor()
    #MainMenuActivity._make_word = newMakeWord

    #### GAME MODIFICATIONS ####

    #ESCUDO DE COLORES
    def new_equip_shields(self, decay: bool = False) -> None:
        if not self.node:
            ba.print_error('Can\'t equip shields; no node.')
            return

        factory = SpazFactory.get()
        if self.shield is None:
            self.shield = ba.newnode('shield',owner=self.node,attrs={
                                     'color': (0.3, 0.2, 2.0),'radius': 1.3 })
            self.node.connectattr('position_center', self.shield, 'position')
        self.shield_hitpoints = self.shield_hitpoints_max = 650
        self.shield_decay_rate = factory.shield_decay_rate if decay else 0
        self.shield.hurt = 0
        ba.playsound(factory.shield_up_sound, 1.0, position=self.node.position)

        if self.shield_decay_rate > 0:
            self.shield_decay_timer = ba.Timer(0.5,ba.WeakCall(self.shield_decay),repeat=True)
            self.shield.always_show_health_bar = True
        def changeColor():
            if self.shield is None: return
            if getData("shieldColor"):
                self.shield.color = c = getRandomColor()
        self._shieldTimer = ba.Timer(getData("timeDelay"),changeColor,repeat=True,timeformat=ba.TimeFormat.MILLISECONDS)
    PlayerSpaz.equip_shields = new_equip_shields

    #BOTS DE COLORES
    SpazBot.oldBotInit = SpazBot.__init__
    def newBotInit(self, *args, **kwargs):
        self.oldBotInit(*args, **kwargs)
        s = 1
        if getData("glowBots"):
            s = getData("glowScale")
	
        self.node.highlight = (self.node.highlight[0]*s,self.node.highlight[1]*s,self.node.highlight[2]*s)

        def changeColor():
            if self.is_alive():
                if getData("colorBots"):
                    c = getRandomColor()
                    self.node.highlight = (c[0]*s,c[1]*s,c[2]*s)
        self._timer = ba.Timer(getData("timeDelay"),changeColor,repeat=True,timeformat=ba.TimeFormat.MILLISECONDS)
    SpazBot.__init__ = newBotInit

    #BANDERA DE COLORES
    Flag.oldFlagInit = Flag.__init__
    def newFlaginit(self,position: Sequence[float] = (0.0, 1.0, 0.0),
                 color: Sequence[float] = (1.0, 1.0, 1.0),
                 materials: Sequence[ba.Material] = None,
                 touchable: bool = True,
                 dropped_timeout: int = None):
        self.oldFlagInit(position, color,materials,touchable,dropped_timeout)	
    
        def cC():
            if self.node.exists():
                if getData("flag"):
                    c = getRandomColor()
                    self.node.color = (c[0]*1.2,c[1]*1.2,c[2]*1.2)
            else: return
        if touchable :
            self._timer = ba.Timer(getData("timeDelay"),cC,repeat=True,timeformat=ba.TimeFormat.MILLISECONDS)
    
    Flag.__init__ = newFlaginit

    #JUGADORES DE COLORES
    PlayerSpaz.oldInit = PlayerSpaz.__init__
    def newInit(self,player: ba.Player,
                 color: Sequence[float] = (1.0, 1.0, 1.0),
                 highlight: Sequence[float] = (0.5, 0.5, 0.5),
                 character: str = 'Spaz',
                 powerups_expire: bool = True):
        self.oldInit(player,color,highlight,character,powerups_expire)

        players = []
        for p in getData("activeProfiles"):
            players.append(p)

        for x in range(len(players)):
            if players[x] == "__account__" :
                players[x] = _ba.get_account_name()

        if player.getname() in players:
            s = s2 = s3 = 1
            if getData("glowColor"):
                s = getData("glowScale")
            if getData("glowHighlight"):
                s2 = getData("glowScale")
            if getData("glowName"):
                s3 = getData("glowScale")

            self.node.color = (self.node.color[0]*s,self.node.color[1]*s,self.node.color[2]*s)
            self.node.highlight = (self.node.highlight[0]*s2,self.node.highlight[1]*s2,self.node.highlight[2]*s2)
            self.node.name_color = (self.node.name_color[0]*s3,self.node.name_color[1]*s3,self.node.name_color[2]*s3)

            def changeColor():
                if self.is_alive():
                    if getData("colorPlayer"):
                        c = getRandomColor()
                        self.node.color = (c[0]*s,c[1]*s,c[2]*s)
                    if getData("higlightPlayer"):
                        c = getRandomColor()
                        self.node.highlight = (c[0]*s2,c[1]*s2,c[2]*s2)
                    if getData("namePlayer"):
                        c = getRandomColor()
                        self.node.name_color = (c[0]*s3,c[1]*s3,c[2]*s3)
            self._timer = ba.Timer(getData("timeDelay"),changeColor,repeat=True,timeformat=ba.TimeFormat.MILLISECONDS)
    PlayerSpaz.__init__ = newInit

    #EXPLOSIONES DE COLORES
    bomb.Blast.oldBlastInit = bomb.Blast.__init__
    def newBlastInit(self, position: Sequence[float] = (0.0, 1.0, 0.0),  velocity: Sequence[float] = (0.0, 0.0, 0.0),
                 blast_radius: float = 2.0, blast_type: str = 'normal',  source_player: ba.Player = None,
                 hit_type: str = 'explosion',  hit_subtype: str = 'normal'):

        self.oldBlastInit(position, velocity, blast_radius, blast_type,  source_player, hit_type, hit_subtype)

        if getData("xplotionColor"):
            c = getRandomColor()

            scl = random.uniform(0.6, 0.9)
            scorch_radius = light_radius = self.radius
            if self.blast_type == 'tnt':
                light_radius *= 1.4
                scorch_radius *= 1.15
                scl *= 3.0

            for i in range(2):
                scorch = ba.newnode('scorch',attrs={'position':self.node.position, 'size':scorch_radius*0.5,'big':(self.blast_type == 'tnt')})
                if self.blast_type == 'ice': scorch.color =(1,1,1.5)
                else: scorch.color = c
                if getData("xplotionColor"):
                    if getData("delScorch"):
                        ba.animate(scorch,"presence",{3:1, 13:0})
                        ba.Timer(13,scorch.delete)

            if self.blast_type == 'ice': return
            light = ba.newnode('light', attrs={ 'position': position,'volume_intensity_scale': 10.0,'color': c})

            iscale = 1.6
            ba.animate(light, 'intensity', {
                0: 2.0 * iscale,
                scl * 0.02: 0.1 * iscale,
                scl * 0.025: 0.2 * iscale,
                scl * 0.05: 17.0 * iscale,
                scl * 0.06: 5.0 * iscale,
                scl * 0.08: 4.0 * iscale,
                scl * 0.2: 0.6 * iscale,
                scl * 2.0: 0.00 * iscale,
                scl * 3.0: 0.0})
            ba.animate(light, 'radius', {
                0: light_radius * 0.2,
                scl * 0.05: light_radius * 0.55,
                scl * 0.1: light_radius * 0.3,
                scl * 0.3: light_radius * 0.15,
                scl * 1.0: light_radius * 0.05})
            ba.timer(scl * 3.0, light.delete)
    bomb.Blast.__init__ = newBlastInit


class ProfilesWindow(popup.PopupWindow):
    """Popup window to view achievements."""

    def __init__(self):
        uiscale = ba.app.ui.uiscale
        scale = (1.8 if uiscale is ba.UIScale.SMALL else
                 1.65 if uiscale is ba.UIScale.MEDIUM else 1.23)
        self._transitioning_out = False
        self._width = 300
        self._height = (300 if uiscale is ba.UIScale.SMALL else 350)
        bg_color = (0.5, 0.4, 0.6)

        self._selected = None
        self._activeProfiles = getData("activeProfiles")

        self._profiles = ba.app.config.get('Player Profiles', {})
        assert self._profiles is not None
        items = list(self._profiles.items())
        items.sort(key=lambda x: x[0].lower())

        accountName: Optional[str]
        if _ba.get_account_state() == 'signed_in':
            accountName = _ba.get_account_display_string()
        else: accountName = None
        #subHeight += (len(items)*45)

        # creates our _root_widget
        popup.PopupWindow.__init__(self,
                                   position=(0,0),
                                   size=(self._width, self._height),
                                   scale=scale,
                                   bg_color=bg_color)

        self._cancel_button = ba.buttonwidget( parent=self.root_widget,
            position=(50, self._height - 30), size=(50, 50),
            scale=0.5, label='',
            color=bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=ba.gettexture('crossOut'),
            iconscale=1.2)
        ba.containerwidget(edit=self.root_widget,cancel_button=self._cancel_button)


        self._title_text = ba.textwidget(parent=self.root_widget,
                                         position=(self._width * 0.5,self._height - 20),
                                         size=(0, 0),
                                         h_align='center',
                                         v_align='center',
                                         scale=01.0,
                                         text=getTranslation('profiles'),
                                         maxwidth=200,
                                         color=(1, 1, 1, 0.4))

        self._scrollwidget = ba.scrollwidget(parent=self.root_widget,
                                             size=(self._width - 60,
                                                   self._height - 70),
                                             position=(30, 30),
                                             capture_arrows=True,
                                             simple_culling_v=10)
        ba.widget(edit=self._scrollwidget, autoselect=True)

        #incr = 36
        sub_width = self._width - 90
        sub_height = (len(items)*50)

        eq_rsrc = 'coopSelectWindow.powerRankingPointsEqualsText'
        pts_rsrc = 'coopSelectWindow.powerRankingPointsText'

        self._subcontainer = box = ba.containerwidget(parent=self._scrollwidget,
                                                size=(sub_width, sub_height),
                                                background=False)
        h = 20
        v = sub_height - 60
        for pName, p in items:
            if pName == '__account__' and accountName is None:
                continue
            color, highlight = get_player_profile_colors(pName)
            tval = (accountName if pName == '__account__' else
                    get_player_profile_icon(pName) + pName)
            assert isinstance(tval, str)
            #print(tval)
            value = True if pName in self._activeProfiles else False

            w = ba.checkboxwidget(parent=box,position=(10,v), value=value,
                        on_value_change_call=ba.WeakCall(self.select, pName),
                        maxwidth=sub_width,size=(sub_width,50),
                        textcolor = color,
                        text=ba.Lstr(value=tval),autoselect=True)
            v -= 45

    def addProfile(self):
        if self._selected is not None:
            if self._selected not in self._activeProfiles:
                self._activeProfiles.append(self._selected)
                ba.app.config["colorsMod"]["activeProfiles"] = self._activeProfiles
                ba.app.config.apply_and_commit()
        else: ba.screenmessage(getTranslation('nothing_selected'))

    def removeProfile(self):
        if self._selected is not None:
            if self._selected in self._activeProfiles:
                self._activeProfiles.remove(self._selected)
                ba.app.config["colorsMod"]["activeProfiles"] = self._activeProfiles
                ba.app.config.apply_and_commit()
            else: print('not found')
        else: ba.screenmessage(getTranslation('nothing_selected'))

    def select(self,name,m):
        self._selected = name
        if m == 0: self.removeProfile()
        else: self.addProfile()

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            ba.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        ba.playsound(ba.getsound('swish'))
        self._transition_out()


class ColorsMenu(PopupWindow):

    def __init__(self,transition='in_right'):
        #self._width = width = 650
        self._width = width = 800
        self._height = height = 450

        self._scrollWidth = self._width*0.85
        self._scrollHeight = self._height - 120
        self._subWidth = self._scrollWidth*0.95;
        self._subHeight = 200
		
        self._current_tab = getData('actab')
        self._timeDelay =  getData("timeDelay")
        self._glowScale =  getData("glowScale")

        self.midwidth = self._scrollWidth*0.45
        self.qwidth = self.midwidth*0.4

        app = ba.app.ui
        uiscale = app.uiscale

        from bastd.mainmenu import MainMenuSession
        self._in_game = not isinstance(_ba.get_foreground_host_session(),
                                       MainMenuSession)

        self._root_widget = ba.containerwidget(size=(width,height),transition=transition,
                           scale=1.5 if uiscale is ba.UIScale.SMALL else 1.0,
                           stack_offset=(0,-5) if uiscale is ba.UIScale.SMALL else  (0,0))

        self._title = ba.textwidget(parent=self._root_widget,position=(50,height-40),text='',
                          maxwidth=self._scrollWidth,size=(self._scrollWidth,20),
                          color=(0.8,0.8,0.8,1.0),h_align="center",scale=1.1)
        
        self._backButton = b = ba.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(50,height-60),size=(120,50),
                                               scale=0.8,text_scale=1.2,label=ba.Lstr(resource='backText'),
                                               button_type='back',on_activate_call=self._back)	
        ba.buttonwidget(edit=self._backButton, button_type='backSmall',size=(50, 50),label=ba.charstr(ba.SpecialChar.BACK)) 
        ba.containerwidget(edit=self._root_widget,cancel_button=b)

        self._nextButton = ba.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(width-60,height*0.5-20),size=(50,50),
                                               scale=1.0,label=ba.charstr(ba.SpecialChar.RIGHT_ARROW),
                                               color=(0.2,1,0.2),button_type='square',
                                               on_activate_call=self.nextTabContainer)

        self._prevButton = ba.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(10,height*0.5-20),size=(50,50),
                                               scale=1.0,label=ba.charstr(ba.SpecialChar.LEFT_ARROW),
                                               color=(0.2,1,0.2),button_type='square',
                                               on_activate_call=self.prevTabContainer)
												
        v = self._subHeight - 55
        v0 = height - 90

        self.tabs = [
                [0,getTranslation('general_tab')],
                [1,getTranslation('player_tab')],
                [2,getTranslation('extras_tab')],
                [3,getTranslation('info_tab')],
               ]
			
        self._scrollwidget = sc =  ba.scrollwidget(parent=self._root_widget,size=(self._subWidth,self._scrollHeight),border_opacity=0.3, highlight=False, position=((width*0.5)-(self._scrollWidth*0.47),50),capture_arrows=True,)

        ba.widget(edit=sc, left_widget=self._prevButton)
        ba.widget(edit=sc, right_widget=self._nextButton)
        ba.widget(edit=self._backButton, down_widget=sc)

        self.tabButtons = []
        h  = 330
        for i in range(3):
            tabButton = ba.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(h,20),size=(20,20),
                                               scale=1.2,label='',
                                               color=(0.3,0.9,0.3),
                                               on_activate_call=ba.Call(self._setTab,self.tabs[i][0]),
                                               texture=ba.gettexture('nub'))
            self.tabButtons.append(tabButton)
            h += 50
        self._tabContainer = None
        self._setTab(self._current_tab)

    def nextTabContainer(self):
        tab = ba.app.config['colorsMod']['actab']
        if tab == 2: self._setTab(0)
        else: self._setTab(tab+1)

    def prevTabContainer(self):
        tab = ba.app.config['colorsMod']['actab']
        if tab == 0: self._setTab(2)
        else: self._setTab(tab-1)
		
    def _setTab(self,tab):

        self._colorTimer = None
        self._current_tab = tab

        ba.app.config['colorsMod']['actab'] = tab
        ba.app.config.apply_and_commit()

        if self._tabContainer is not None and self._tabContainer.exists():
            self._tabContainer.delete()
        self._tabData = {}

        if tab == 0: #general
            subHeight = 0

            self._tabContainer = c = ba.containerwidget(parent=self._scrollwidget,size=(self._subWidth,subHeight),
                                                background=False,selection_loops_to_parent=True)
            
            ba.textwidget(edit=self._title,text=getTranslation('general_tab'))
            v0 = subHeight - 30
            v = v0 - 10
			
            h = self._scrollWidth*0.12
            cSpacing = self._scrollWidth*0.15
            t = ba.textwidget(parent=c,position=(0,v),
                          text=getTranslation('glow_scale'),
                          maxwidth=self.midwidth ,size=(self.midwidth ,20),color=(0.8,0.8,0.8,1.0),h_align="center")
            v -= 45	  
            b = ba.buttonwidget(parent=c,position=(h-20,v-12),size=(40,40),label="-",
                            autoselect=True,on_activate_call=ba.Call(self._glowScaleDecrement),repeat=True,enable_sound=True,button_type='square')

            self._glowScaleText = ba.textwidget(parent=c,position=(h+20,v),maxwidth=cSpacing,
                            size=(cSpacing,20),editable=False,color=(0.3,1.0,0.3),h_align="center",text=str(self._glowScale))

            b2 = ba.buttonwidget(parent=c,position=(h+cSpacing+20,v-12),size=(40,40),label="+",
                            autoselect=True,on_activate_call=ba.Call(self._glowScaleIncrement),repeat=True,enable_sound=True,button_type='square')

            v -= 70
            t = ba.textwidget(parent=c,position=(0,v),
                          text=getTranslation('time_delay'),
                          maxwidth=self.midwidth ,size=(self.midwidth ,20),color=(0.8,0.8,0.8,1.0),h_align="center")
            v -= 45 
            a = ba.buttonwidget(parent=c,position=(h-20,v-12),size=(40,40),label="-",
                            autoselect=True,on_activate_call=ba.Call(self._timeDelayDecrement),repeat=True,enable_sound=True,button_type='square')

            self._timeDelayText = ba.textwidget(parent=c,position=(h+20,v),maxwidth=self._scrollWidth*0.9,
                            size=(cSpacing,20),editable=False,color=(0.3,1.0,0.3,1.0),h_align="center",text=str(self._timeDelay))

            a2 = ba.buttonwidget(parent=c,position=(h+cSpacing+20,v-12),size=(40,40),label="+",
                            autoselect=True,on_activate_call=ba.Call(self._timeDelayIncrement),repeat=True,enable_sound=True,button_type='square')
							
            v -= 70
            reset = ba.buttonwidget(parent=c, autoselect=True,
                                    position=((self._scrollWidth*0.22)-80, v-25), size=(160,50),scale=1.0, text_scale=1.2,textcolor=(1,1,1),
                                    label=getTranslation('reset_values'),on_activate_call=self._resetValues)
            self._updateColorTimer()

            v = v0
            h = self._scrollWidth*0.44

            t = ba.textwidget(parent=c,position=(h,v),
                          text=getTranslation('palette'),
                          maxwidth=self.midwidth ,size=(self.midwidth ,20),
                          color=(0.8,0.8,0.8,1.0),h_align="center")
            v -= 30
            t2 = ba.textwidget(parent=c,position=(h,v),
                          text=getTranslation('tap_color'), scale=0.9,
                          maxwidth=self.midwidth ,size=(self.midwidth ,20),
                          color=(0.6,0.6,0.6,1.0),h_align="center")
            v -= 20
            sp = h+45
            self.updatePalette(v,sp)

        elif tab == 1:
            subHeight = self._subHeight

            self._tabContainer = c = ba.containerwidget(parent=self._scrollwidget,size=(self._subWidth,subHeight),
                                                background=False,selection_loops_to_parent=True)
            v2 = v = v0 = subHeight
            ba.textwidget(edit=self._title,text=getTranslation('player_tab'))

            t = ba.app.spaz_appearances['Spaz']
            tex = ba.gettexture(t.icon_texture)
            tintTex = ba.gettexture(t.icon_mask_texture)
            gs = getData("glowScale")
            tc = (1,1,1)
            t2c = (1,1,1)

            v2 -= (50+180) 
            self._previewImage = ba.imagewidget(parent=c,position=(self._subWidth*0.72-100,v2),size=(200,200),
                            mask_texture=ba.gettexture('characterIconMask'),tint_texture=tintTex,
                            texture=tex, model_transparent=ba.getmodel('image1x1'),
                            tint_color=(tc[0]*gs,tc[1]*gs,tc[2]*gs),tint2_color=(t2c[0]*gs,t2c[1]*gs,t2c[2]*gs))

            self._colorTimer = ba.Timer(getData("timeDelay"),
                             ba.Call(self._updatePreview),repeat=True,timeformat=ba.TimeFormat.MILLISECONDS)
            v2 -= 70

            def doProfileWindow():
                ProfilesWindow()

            reset = ba.buttonwidget(parent=c, autoselect=True,on_activate_call=doProfileWindow,
                                    position=(self._subWidth*0.72-100,v2), size=(200,60),scale=1.0, text_scale=1.2,textcolor=(1,1,1),
                                    label=getTranslation('profiles'))
            miniBoxWidth = self.midwidth - 30
            miniBoxHeight = 80

            v -= 18
            #Color
            h = 50
            box1 = ba.containerwidget(parent=c,position=(h,v-miniBoxHeight),
                                      size=(miniBoxWidth,miniBoxHeight),background=True)
            vbox1 = miniBoxHeight -25
            t = ba.textwidget(parent=box1,position=(10,vbox1),
                          text=getTranslation('apply_to_color'),
                          maxwidth=miniBoxWidth-20,size=(miniBoxWidth,20),color=(0.8,0.8,0.8,1.0),h_align="left")
            vbox1 -= 45
            self.bw = ba.checkboxwidget(parent=box1,position=(10,vbox1), value=getData("colorPlayer"),
                                      on_value_change_call=ba.Call(self._setSetting,'colorPlayer'), maxwidth=self.qwidth,
                                      text=getTranslation('change'),autoselect=True,size=(self.qwidth,25))
            #vbox1 -= 35
            self.bw = ba.checkboxwidget(parent=box1,position=(25+self.qwidth,vbox1), value=getData("glowColor"),
                                      on_value_change_call=ba.Call(self._setSetting,'glowColor'), maxwidth=self.qwidth,
                                      text=getTranslation('glow'),autoselect=True,size=(self.qwidth,25))	
            v -= (miniBoxHeight+20)

            #Highlight
            box1 = ba.containerwidget(parent=c,position=(h,v-miniBoxHeight),
                                      size=(miniBoxWidth,miniBoxHeight),background=True)
            vbox1 = miniBoxHeight -20
            t = ba.textwidget(parent=box1,position=(10,vbox1),
                          text=getTranslation('apply_to_highlight'),
                          maxwidth=miniBoxWidth-20,size=(miniBoxWidth,20),color=(0.8,0.8,0.8,1.0),h_align="left")
            vbox1 -= 45
            self.bw = ba.checkboxwidget(parent=box1,position=(10,vbox1), value=getData("higlightPlayer"),
                                      on_value_change_call=ba.Call(self._setSetting,'higlightPlayer'), maxwidth=self.qwidth,
                                      text=getTranslation('change'),autoselect=True,size=(self.qwidth,25))
            #vbox1 -= 35
            self.bw = ba.checkboxwidget(parent=box1,position=(25+self.qwidth,vbox1), value=getData("glowHighlight"),
                                      on_value_change_call=ba.Call(self._setSetting,'glowHighlight'), maxwidth=self.qwidth,
                                      text=getTranslation('glow'),autoselect=True,size=(self.qwidth,25))	
            v -= (miniBoxHeight+20)
            #Name
            box1 = ba.containerwidget(parent=c,position=(h,v-miniBoxHeight),
                                      size=(miniBoxWidth,miniBoxHeight),background=True)
            vbox1 = miniBoxHeight -20
            t = ba.textwidget(parent=box1,position=(10,vbox1),
                          text=getTranslation('apply_to_name'),
                          maxwidth=miniBoxWidth-20,size=(miniBoxWidth,20),color=(0.8,0.8,0.8,1.0),h_align="left")
            vbox1 -= 40
            self.bw = ba.checkboxwidget(parent=box1,position=(10,vbox1), value=getData("namePlayer"),
                                      on_value_change_call=ba.Call(self._setSetting,'namePlayer'), maxwidth=self.qwidth,
                                      text=getTranslation('change'),autoselect=True,size=(self.qwidth,25))
            #vbox1 -= 35
            self.bw = ba.checkboxwidget(parent=box1,position=(25+self.qwidth,vbox1), value=getData("glowName"),
                                      on_value_change_call=ba.Call(self._setSetting,'glowName'), maxwidth=self.qwidth,
                                      text=getTranslation('glow'),autoselect=True,size=(self.qwidth,25))	
            v -= (miniBoxHeight+50)

        elif tab == 2:
            subHeight = 0
            self._tabContainer = c = ba.containerwidget(parent=self._scrollwidget,size=(self._subWidth,subHeight),
                                                background=False,selection_loops_to_parent=True)
            v0 = subHeight - 50

            v = v0
            h = 30
            ba.textwidget(edit=self._title,text=getTranslation('extras_tab'))
            self.bw = ba.checkboxwidget(parent=c,position=(h,v), value=getData("shieldColor"),
                                      on_value_change_call=ba.Call(self._setSetting,'shieldColor'), maxwidth=self.midwidth,
                                      text=getTranslation('apply_to_shields'),autoselect=True,size=(self.midwidth,30))
            v -= 50
            self.bw = ba.checkboxwidget(parent=c,position=(h,v), value=getData("flag"),
                                      on_value_change_call=ba.Call(self._setSetting,'flag'), maxwidth=self.midwidth,
                                      text=getTranslation('apply_to_flags'),autoselect=True,size=(self.midwidth,30))
            v = v0
            h = self.midwidth
            self.bw = ba.checkboxwidget(parent=c,position=(h,v), value=getData("xplotionColor"),
                                      on_value_change_call=ba.Call(self._setSetting,'xplotionColor'), maxwidth=self.midwidth,
                                      text=getTranslation('apply_to_explotions'),autoselect=True,size=(self.midwidth,30))
            v -= 50
            self.bw = ba.checkboxwidget(parent=c,position=(h,v), value=getData("delScorch"),
                                      on_value_change_call=ba.Call(self._setSetting,'delScorch'), maxwidth=self.midwidth,
                                      text=getTranslation('clean_explotions'),autoselect=True,size=(self.midwidth,30))
            v -= 35
            miniBoxWidth = self.midwidth
            miniBoxHeight = 80

            #Bots Color
            box1 = ba.containerwidget(parent=c,position=((self._scrollWidth*0.45) -(miniBoxWidth/2),v-miniBoxHeight),
                                      size=(miniBoxWidth,miniBoxHeight),background=True)
            vbox1 = miniBoxHeight -20
            t = ba.textwidget(parent=box1,position=(10,vbox1),
                          text=getTranslation('apply_to_bots'),
                          maxwidth=miniBoxWidth-20,size=(miniBoxWidth,20),color=(0.8,0.8,0.8,1.0),h_align="left")
            vbox1 -= 45
            self.bw = ba.checkboxwidget(parent=box1,position=(10,vbox1),value=getData("colorBots"),
                                      on_value_change_call=ba.Call(self._setSetting,'colorBots'), maxwidth=self.qwidth,
                                      text=getTranslation('change'),autoselect=True,size=(self.qwidth,25))

            self.bw = ba.checkboxwidget(parent=box1,position=(30+self.qwidth,vbox1), value=getData("glowBots"),
                                      on_value_change_call=ba.Call(self._setSetting,'glowBots'), maxwidth=self.qwidth,
                                      text=getTranslation('glow'),autoselect=True,size=(self.qwidth,25))

            v -= 130
            reset = ba.buttonwidget(parent=c, autoselect=True,on_activate_call=self.restoreSettings,
                                    position=((self._scrollWidth*0.45)-150, v-25), size=(300,50),scale=1.0, text_scale=1.2,textcolor=(1,1,1),
                                    label=getTranslation('restore_default_settings'))
										  
        for bttn in self.tabButtons:
            ba.buttonwidget(edit=bttn,color = (0.1,0.5,0.1))
        ba.buttonwidget(edit=self.tabButtons[tab],color = (0.1,1,0.1))

    def _setSetting(self,setting,m):
        ba.app.config["colorsMod"][setting] =  False if m==0 else True
        ba.app.config.apply_and_commit()
		
    def _timeDelayDecrement(self):
        self._timeDelay = max(50,self._timeDelay - 50)
        ba.textwidget(edit=self._timeDelayText,text=str(self._timeDelay))
        ba.app.config["colorsMod"]["timeDelay"] =  self._timeDelay
        ba.app.config.apply_and_commit()
        self._updateColorTimer()
		
    def _timeDelayIncrement(self):
        self._timeDelay = self._timeDelay + 50
        ba.textwidget(edit=self._timeDelayText,text=str(self._timeDelay))
        ba.app.config["colorsMod"]["timeDelay"] =  self._timeDelay
        ba.app.config.apply_and_commit()
        self._updateColorTimer()
		
    def _resetValues(self):
        ba.app.config["colorsMod"]["glowScale"] = self._glowScale =  1
        ba.app.config["colorsMod"]["timeDelay"] = self._timeDelay =  500
        ba.textwidget(edit=self._glowScaleText,text=str(self._glowScale))
        ba.textwidget(edit=self._timeDelayText,text=str(self._timeDelay))
        ba.app.config.apply_and_commit()
        self._updateColorTimer()

    def updatePalette(self,h,sp):
        colours = getData("colors")
        x = sp
        y = h - 50
        cont = 1
        bttnSize = (45,45)
        l = len(colours)

        for i in range(16):
            if i < l:
                w = ba.buttonwidget(
                    parent= self._tabContainer, position=(x,y), size=bttnSize,
                    autoselect=False, label="",button_type="square",color=colours[i],
                    on_activate_call=ba.WeakCall(self.removeColor,colours[i]))
            else:
                w = ba.buttonwidget(
                    parent= self._tabContainer, position=(x,y), size=bttnSize,color=(0.5, 0.4, 0.6),
                    autoselect=False, label="",texture=ba.gettexture('frameInset'))
                if i == l:
                    ba.buttonwidget(edit=w,on_activate_call=ba.WeakCall(self._makePicker,w),label="+")
            if cont % 4 == 0:
                x = sp
                y -= ((bttnSize[0]) + 10)
            else: x += (bttnSize[0]) + 13
            cont += 1

    def addColor(self,color):
        if not self.colorIn(color):    
            ba.app.config["colorsMod"]["colors"].append(color)
            ba.app.config.apply_and_commit()
            self._setTab(0)
        else: ba.screenmessage(getTranslation('color_already'))

    def removeColor(self,color):
        if color is not None:
            if len(getData("colors")) >= 3:
                if color in getData("colors"):
                    ba.app.config["colorsMod"]["colors"].remove(color)
                    ba.app.config.apply_and_commit()
                    self._setTab(0)
                else: print('not found')
            else: ba.screenmessage("Min. 2 colors", color=(0, 1, 0))
        else: ba.screenmessage(getTranslation('nothing_selected'))

    def _makePicker(self, origin):
        baseScale = 2.05 if ba.UIScale.SMALL else 1.6 if ba.UIScale.MEDIUM else 1.0
        initial_color = (0, 0.8, 0)
        ColorPicker( parent=self._tabContainer, position=origin.get_screen_space_center(),
                     offset=(baseScale * (-100), 0),initial_color=initial_color, delegate=self, tag='color')

    def color_picker_closing(self, picker):
        if not self._root_widget.exists(): return
        tag = picker.get_tag()

    def color_picker_selected_color(self, picker, color):
        self.addColor(color)

    def colorIn(self,c):
        sColors = getData("colors")
        for sC in sColors:
                if c[0] == sC[0] and c[1] == sC[1] and c[2] == sC[2]:
                    return True
        return False

    def setColor(self,c):
        self._selected = c
        ba.buttonwidget(edit=self._moveOut,color = (0.8, 0, 0))

    def _updateColorTimer(self):
        self._colorTimer = ba.Timer(getData("timeDelay"),ba.Call(self._update),repeat=True,timeformat=ba.TimeFormat.MILLISECONDS)
		
    def _update(self):
        color = (random.random(),random.random(),random.random())
        ba.textwidget(edit=self._timeDelayText,color=color)

    def _updatePreview(self):
        gs = gs2 = getData("glowScale")
        if not getData("glowColor"): gs =1
        if not getData("glowHighlight"): gs2 =1

        c = (1,1,1)
        if getData("colorPlayer"):
            c = getRandomColor()

        c2 = (1,1,1)
        if getData("higlightPlayer"):
            c2 = getRandomColor()

        ba.imagewidget(edit=self._previewImage,tint_color=(c[0]*gs,c[1]*gs,c[2]*gs))
        ba.imagewidget(edit=self._previewImage,tint2_color=(c2[0]*gs2,c2[1]*gs2,c2[2]*gs2))
		
    def _glowScaleDecrement(self):
        self._glowScale = max(1,self._glowScale - 1)
        ba.textwidget(edit=self._glowScaleText,text=str(self._glowScale))
        ba.app.config["colorsMod"]["glowScale"] =  self._glowScale
        ba.app.config.apply_and_commit()
		
    def _glowScaleIncrement(self):
        self._glowScale = min(5,self._glowScale + 1)
        ba.textwidget(edit=self._glowScaleText,text=str(self._glowScale))
        ba.app.config["colorsMod"]["glowScale"] =  self._glowScale
        ba.app.config.apply_and_commit()

    def restoreSettings(self):
        def doIt():
            ba.app.config["colorsMod"] = getDefaultSettings()
            ba.app.config.apply_and_commit()
            self._setTab(2)
            ba.screenmessage(getTranslation('settings_restored'))
        confirm.ConfirmWindow(getTranslation('restore_settings'),
                          width=400, height=120, action=doIt, ok_text=ba.Lstr(resource='okText'))

    def _back(self):
        ba.containerwidget(edit=self._root_widget,transition='out_right')
        self._colorTimer = None
        self._colorPreviewTimer = None
        #if self._in_game:
        #    ba.app.main_menu_window = (mainmenu.MainMenuWindow(transition='in_left').get_root_widget())
        #else:
        #    ba.app.main_menu_window = ProfileBrowserWindow(transition='in_left').get_root_widget()
        #ba.app.main_menu_window = (mainmenu.MainMenuWindow(transition='in_left').get_root_widget())