"""
Whats new:
    new adjusted scrolling tag window, now edit tags on new profiles, different settings for each profile, enable/disable tag for that profile, chnage color of tag, change tag scale ( big, medium, small), chnage opacity, change shadow, enable/disable tag animation, change frequency (speed) of animation, change colors of animation.

I apreciate any kind of modification. So feel free to use or edit code or change credit string.... no problem.
Thanks to savio for testing mod on diffrent platforms.

really awsome servers:
    Bombsquad Consultancy Service - https://discord.gg/2RKd9QQdQY
    bombspot - https://discord.gg/ucyaesh
    cyclones - https://discord.gg/pJXxkbQ7kH

how to use:
    Account -> PlayerProfile -> Edit(new profile -> edit)
    Open profile you like (every profile has dirrent tags, settings (Configs))
    enable tag for profile you like, edit tag you want. enable cool flashy animation
"""

from __future__ import annotations
from bastd.ui.profile.edit import EditProfileWindow
from bastd.ui.profile.browser import ProfileBrowserWindow
from bastd.ui.colorpicker import ColorPicker
from bastd.ui.popup import PopupMenu
from bastd.actor.playerspaz import PlayerSpaz
import ba,_ba

from typing import (
    Tuple,
    Optional,
    Sequence,
    Union, 
    Callable,
    Any,
    List,
    cast
)

__version__ = 2.0
__author__ = "pranav1711#2006"


# Default Confings/Settings
Configs = {
    "enabletag": False,
    "tag": "",
    "color":[1,1,1],
    "scale": "medium",
    "opacity": 1.0,
    "shadow": 0.0,
    "animtag": False,
    "frequency": 0.5,
    "animcolors": [[1,0,0], [0,1,0], [0,0,1]]
}

# Useful global fucntions
def setconfigs() -> None:
    """
    Set required defualt configs for mod
    """
    cnfg = ba.app.config
    profiles = cnfg['Player Profiles']

    if not "TagConf" in cnfg:
        cnfg["TagConf"] = {}
    
    for p in profiles:
        if not p in cnfg["TagConf"]:
            cnfg["TagConf"][str(p)] = Configs
        else:
            for j in Configs:
                if j not in cnfg["TagConf"][str(p)]:
                    cnfg["TagConf"][str(p)] = Configs
                else: pass
    ba.app.config.apply_and_commit()

def getanimcolor(name: str) -> dict:
    """
    Returns dictnary of colors with prefective time -> {seconds: (r, g, b)}
    """
    freq = ba.app.config['TagConf'][str(name)]['frequency']
    s1 = 0.0
    s2 = s1 + freq
    s3 = s2 + freq

    c = ba.app.config['TagConf'][str(name)]['animcolors']
    colr1 = (c[0][0], c[0][1], c[0][2])
    colr2 = (c[1][0], c[1][1], c[1][2])
    colr3 = (c[2][0], c[2][1], c[2][2])

    animcolor = {
        s1: colr1,
        s2: colr2,
        s3: colr3
    }
    return animcolor

def gethostname() -> str:
    """
    Return player name, by using -1 only host can use tags.
    """
    session = _ba.get_foreground_host_session()
    with _ba.Context(session):
        for player in session.sessionplayers:
            if player.inputdevice.client_id == -1:
                name = player.getname(full=True, icon=False)
                break
        if name == _ba.get_account_name():
            return '__account__'
        return name


# Dummy functions for extend functionality for class object
PlayerSpaz.init = PlayerSpaz.__init__
EditProfileWindow.init = EditProfileWindow.__init__
ProfileBrowserWindow.del_prof = ProfileBrowserWindow._do_delete_profile


# PlayerSpaz object at -> bastd.actor.playerspaz
def NewPlayerSzapInit(self,
            player: ba.Player,
            color: Sequence[float] = (1.0, 1.0, 1.0),
            highlight: Sequence[float] = (0.5, 0.5, 0.5),
            character: str = 'Spaz',
            powerups_expire: bool = True) -> None:
    self.init(player, color, highlight, character, powerups_expire)
    self.curname = gethostname()

    try:
        cnfg = ba.app.config["TagConf"]
        if cnfg[str(self.curname)]["enabletag"]:
            # Tag node
            self.mnode = ba.newnode('math', owner=self.node, attrs={'input1': (0, 1.5, 0),'operation': 'add'})
            self.node.connectattr('torso_position', self.mnode, 'input2')

            tagtext = cnfg[str(self.curname)]["tag"]
            opacity = cnfg[str(self.curname)]["opacity"]
            shadow = cnfg[str(self.curname)]["shadow"]

            c = cnfg[str(self.curname)]["color"]
            color = (c[0], c[1], c[2])

            sl = cnfg[str(self.curname)]["scale"]
            scale = 0.01 if sl == 'mediam' else 0.009 if not sl == 'large' else 0.02
            
            self.Tag = ba.newnode(
                type='text',
                owner=self.node,
                attrs={
                    'text': str(tagtext),
                    'in_world': True,
                    'shadow': shadow,
                    'color': color,
                    'scale': scale,
                    'opacity': opacity,
                    'flatness': 1.0,
                    'h_align': 'center'})
            self.mnode.connectattr('output', self.Tag, 'position')

            if cnfg[str(self.curname)]["animtag"]:
                kys = getanimcolor(self.curname)
                ba.animate_array(node=self.Tag, attr='color', size=3, keys=kys, loop=True)
    except Exception: pass

# EditProfileWindow -> bastd.ui.profile.edit
def NewEditProfileWindowInit(self,
            existing_profile: Optional[str],
            in_main_menu: bool,
            transition: str = 'in_right') -> None:
    """
    New boilerplate for editprofilewindow, addeds button to call TagSettings window
    """
    self.existing_profile = existing_profile
    self.in_main_menu = in_main_menu
    self.init(existing_profile, in_main_menu, transition)

    v = self._height - 115.0
    x_inset = self._x_inset
    b_width = 50
    b_height = 30
    
    if not existing_profile:
        self._text: str = cast(str, ba.textwidget(query=self._text_field))
        ba.app.config['TagConf'][str(self._text)] = Configs
        ba.app.config.apply_and_commit()

    self.tagwinbtn = ba.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(505 + x_inset, v - 38 - 15),
            size=(b_width, b_height),
            color=(0.6, 0.5, 0.6),
            label='Tag',
            button_type='square',
            text_scale=1.2,
            on_activate_call=ba.Call(_on_tagwinbtn_press, self))

def _on_tagwinbtn_press(self) -> None:
    """
    Calls tag config window passes all paramisters 
    """
    ba.containerwidget(edit=self._root_widget, transition='out_scale')
    ba.app.ui.set_main_menu_window(
            TagWindow(self.existing_profile,
                    self.in_main_menu,
                    self._name,
                    transition='in_right').get_root_widget())

def new_cancel(self) -> None:
    """
    Removes name from confing if profile is new and usr cancel it
    """
    if not self.existing_profile and self._text in ba.app.config['TagConf']:
        del ba.app.config['TagConf'][str(self._text)]
        ba.app.config.apply_and_commit()
        
    ba.containerwidget(edit=self._root_widget, transition='out_right')
    ba.app.ui.set_main_menu_window(
        ProfileBrowserWindow(
            'in_left',
            selected_profile=self._existing_profile,
            in_main_menu=self._in_main_menu).get_root_widget())

def new_do_delete_profile(self) -> None:
    """
    If profile is delete, Remove profile from config.
    """
    self.del_prof()
    cnfg = ba.app.config['TagConf']
    del cnfg[str(self._selected_profile)]
    ba.app.config.apply_and_commit()


# ba_meta require api 6
# ba_meta export plugin
class Tag(ba.Plugin):
    def __init__(self) -> None:
        """
        Tag above actor player head, replacing PlayerSpaz class for getting actor,
        using EditProfileWindow for UI.
        """
        if _ba.env().get("build_number",0) >= 20327:
            setconfigs()
            self.Replace()
    
    def Replace(self) -> None:
        """
        Replacing bolierplates no harm to relative funtionality only extending 
        """
        PlayerSpaz.__init__ = NewPlayerSzapInit
        EditProfileWindow.__init__ = NewEditProfileWindowInit
        EditProfileWindow._cancel = new_cancel
        ProfileBrowserWindow._do_delete_profile = new_do_delete_profile


class TagWindow(ba.Window):
    def __init__(self,
                existing_profile: Optional[str],
                in_main_menu: bool,
                profilename: str,
                transition: Optional[str] = 'in_right') -> None:
        self.existing_profile = existing_profile
        self.in_main_menu = in_main_menu
        self.profilename = profilename

        uiscale = ba.app.ui.uiscale
        self._width = 870.0 if uiscale is ba.UIScale.SMALL else 670.0
        self._height = (390.0 if uiscale is ba.UIScale.SMALL else
                        450.0 if uiscale is ba.UIScale.MEDIUM else 520.0)
        extra_x = 100 if uiscale is ba.UIScale.SMALL else 0
        self.extra_x = extra_x
        top_extra = 20 if uiscale is ba.UIScale.SMALL else 0

        super().__init__(
                root_widget=ba.containerwidget(
                size=(self._width, self._height),
                transition=transition,
                scale=(2.06 if uiscale is ba.UIScale.SMALL else
                   1.4 if uiscale is ba.UIScale.MEDIUM else 1.0)))
        
        self._back_button = ba.buttonwidget(
                parent=self._root_widget,
                autoselect=True,
                selectable=False, # FIXME: when press a in text field it selets to button 
                position=(52 + self.extra_x, self._height - 60 - top_extra),
                size=(60, 60),
                scale=0.8,
                label=ba.charstr(ba.SpecialChar.BACK),
                button_type='backSmall',
                on_activate_call=self._back)
        ba.containerwidget(edit=self._root_widget, cancel_button=self._back_button)

        self._save_button = ba.buttonwidget(
                parent=self._root_widget,
                position=(self._width - (177 + extra_x),
                            self._height - 60 - top_extra),
                size=(155, 60),
                color=(0, 0.7, 0.5),
                autoselect=True,
                selectable=False, # FIXME: when press a in text field it selets to button 
                scale=0.8,
                label=ba.Lstr(resource='saveText'),
                on_activate_call=self.on_save)
        ba.containerwidget(edit=self._root_widget, start_button=self._back_button)

        self._title_text = ba.textwidget(
                parent=self._root_widget,
                position=(0, self._height - 40 - top_extra),
                size=(self._width, 25),
                text='Tag',
                color=ba.app.ui.title_color,
                scale=1.2,
                h_align='center',
                v_align='top')
        
        self._scroll_width = self._width - (100 + 2 * extra_x)
        self._scroll_height = self._height - 115.0
        self._sub_width = self._scroll_width * 0.95
        self._sub_height = 500.0
        self._spacing = 32
        self._extra_button_spacing = self._spacing * 2.5
        
        self._scrollwidget = ba.scrollwidget(
                parent=self._root_widget,
                position=(50 + extra_x, 50 - top_extra),
                simple_culling_v=20.0,
                highlight=False,
                size=(self._scroll_width,
                    self._scroll_height),
                selection_loops_to_parent=True)
        ba.widget(edit=self._scrollwidget, right_widget=self._scrollwidget)
        
        self._subcontainer = ba.containerwidget(
                parent=self._scrollwidget,
                size=(self._sub_width,
                    self._sub_height),
                background=False,
                selection_loops_to_parent=True)
        
        v = self._sub_height - 35
        v -= self._spacing * 1.2
        self._v = v
        
        self._prof = ba.app.config["TagConf"][self.profilename]
        self.enabletagcb = ba.checkboxwidget(
                parent=self._subcontainer,
                autoselect=True,
                position=(25.0, v + 10),
                size=(30, 30),
                text='Enable Tag',
                textcolor=(0.8, 0.8, 0.8),
                value=self._prof['enabletag'],
                on_value_change_call=ba.Call(self.change_val, [f'{self.profilename}', 'enabletag']),
                scale=1.27,
                maxwidth=430)
        
        self.tag_text = ba.textwidget(
                parent=self._subcontainer,
                text='Tag',
                position=(35.0, v - 40),
                scale=1.35,
                maxwidth=430,
                h_align='left',
                v_align='center',
                color=(0.8, 0.8, 0.8))
        
        self.tagtextfield = ba.textwidget(
                parent=self._subcontainer,
                position=(200.0, v - 55),
                size=(330, 50),
                text=self._prof["tag"],
                h_align='center',
                v_align='center',
                max_chars=16,
                autoselect=True,
                editable=True,
                padding=4,
                color=(0.9, 0.9, 0.9, 1.0))
        
        self.tag_color_text = ba.textwidget(
                parent=self._subcontainer,
                text='Color',
                position=(35.0, v - 90),
                maxwidth=225,
                color=(0.8, 0.8, 0.8),
                h_align='left',
                v_align='center',
                scale=1.25)
        
        c = self._prof['color']
        self.tag_color_btn = ba.buttonwidget(
                parent=self._subcontainer,
                autoselect=True,
                color=(c[0], c[1], c[2]),
                position=(330.0, v - 90),
                size=(60, 30),
                label='',
                button_type='square',
                text_scale=1.2,
                on_activate_call=ba.Call(self.make_color_piker, position=(190.0, v - 700), tag='tagcolor'))
        
        self.tag_scale_text = ba.textwidget(
                parent=self._subcontainer,
                text='Scale',
                position=(35.0, v - 140),
                maxwidth=225,
                color=(0.8, 0.8, 0.8),
                h_align='left',
                v_align='center',
                scale=1.25)
        
        self.tag_scale_button = PopupMenu(
                parent=self._subcontainer,
                position=(330.0, v - 155),
                width=150,
                autoselect=True,
                on_value_change_call=ba.WeakCall(self._on_menu_choice),
                choices=['large', 'medium', 'small'],
                button_size=(150, 50),
                #choices_display=('large', 'medium', 'small'),
                current_choice=self._prof["scale"])
        
        CustomConfigNumberEdit(
                parent=self._subcontainer,
                position=(40.0, v - 190),
                xoffset=65,
                displayname='Opacity',
                configkey=['TagConf', f'{self.profilename}', 'opacity'],
                changesound=True,
                minval=0.5,
                maxval=2.0,
                increment=0.1,
                textscale=1.25)
        
        CustomConfigNumberEdit(
                parent=self._subcontainer,
                position=(40.0, v - 240),
                xoffset=65,
                displayname='Shadow',
                configkey=['TagConf', f'{self.profilename}', 'shadow'],
                changesound=True,
                minval=0.0,
                maxval=2.0,
                increment=0.1,
                textscale=1.25)
        
        self.enabletaganim = ba.checkboxwidget(
                parent=self._subcontainer,
                autoselect=True,
                position=(25.0, v - 300),
                size=(30, 30),
                text='Animate Tag',
                textcolor=(0.8, 0.8, 0.8),
                value=self._prof['animtag'],
                on_value_change_call=ba.Call(self.change_val, [f'{self.profilename}', 'animtag']),
                scale=1.27,
                maxwidth=430)
        
        CustomConfigNumberEdit(
                parent=self._subcontainer,
                position=(35.0, v - 350),
                xoffset=65,
                displayname='Frequency',
                configkey=['TagConf', f'{self.profilename}', 'frequency'],
                changesound=True,
                minval=0.1,
                maxval=5.0,
                increment=0.1,
                textscale=1.25)
        
        self.anim_color_text = ba.textwidget(
                parent=self._subcontainer,
                text='Colors',
                position=(35.0, v - 400),
                scale=1.25,
                maxwidth=430,
                h_align='left',
                v_align='center',
                color=(0.8, 0.8, 0.8))
        
        c1 = self._prof['animcolors'][0]
        self.animcolor_btn_1 = ba.buttonwidget(
                parent=self._subcontainer,
                autoselect=True,
                color=(c1[0], c1[1], c1[2]),
                position=(290.0, v - 400),
                size=(60, 30),
                label='',
                button_type='square',
                text_scale=1.2,
                on_activate_call=ba.Call(self.make_color_piker, position=(190.0, v - 700), tag='animcolor1'))
            
        c2 = self._prof['animcolors'][1]
        self.animcolor_btn_2 = ba.buttonwidget(
                parent=self._subcontainer,
                autoselect=True,
                color=(c2[0], c2[1], c2[2]),
                position=(360.0, v - 400),
                size=(60, 30),
                label='',
                button_type='square',
                text_scale=1.2,
                on_activate_call=ba.Call(self.make_color_piker, position=(190.0, v - 700), tag='animcolor2'))
        
        c3 = self._prof['animcolors'][2]
        self.animcolor_btn_3 = ba.buttonwidget(
                parent=self._subcontainer,
                autoselect=True,
                color=(c3[0], c3[1], c3[2]),
                position=(430.0, v - 400),
                size=(60, 30),
                label='',
                button_type='square',
                text_scale=1.2,
                on_activate_call=ba.Call(self.make_color_piker, position=(190.0, v - 700), tag='animcolor3'))
    
    def _back(self) -> None:
        """
        transit window into back window
        """
        ba.containerwidget(edit=self._root_widget,
                                transition='out_scale')
        ba.app.ui.set_main_menu_window(EditProfileWindow(
                                self.existing_profile,
                                self.in_main_menu,
                                transition='in_left').get_root_widget())
    
    def change_val(self, config: List[str], val: bool) -> None:
        """
        chamges the value of check boxes
        """
        cnfg = ba.app.config["TagConf"]
        try:
            cnfg[config[0]][config[1]] = val
            ba.playsound(ba.getsound('gunCocking'))
        except Exception:
            ba.screenmessage("error", color=(1,0,0))
            ba.playsound(ba.getsound('error'))
        ba.app.config.apply_and_commit()
    
    def _on_menu_choice(self, choice: str) -> None:
        """
        Changes the given choice in configs
        """
        cnfg = ba.app.config["TagConf"][self.profilename]
        cnfg["scale"] = choice
        ba.app.config.apply_and_commit()
    
    def make_color_piker(self, position: tuple, tag: str) -> None:
        """
        Ui that allows to choose color
        """
        ColorPicker(
            parent=self._subcontainer,
            position=position,
            offset=(0, 0),
            initial_color=(1,1,1),
            delegate=self,
            tag=tag)
    
    def refresh_color_btn(self, btn, color: tuple) -> None:
        """
        Changes color of btn on real time
        """
        ba.buttonwidget(edit=btn, color=color)
    
    def color_picker_selected_color(self, picker: ColorPicker, color: Tuple[float, float, float]) -> None:
        """
        Called when a color is selected in a color picker.
        """
        if not self._root_widget:
            return
        cnfg = ba.app.config['TagConf'][str(self.profilename)]
        tag = picker.get_tag()

        if tag == 'tagcolor':
            c = cnfg['color']
            c[0], c[1], c[2] = color[0], color[1], color[2]
            ba.app.config.apply_and_commit()
            self.refresh_color_btn(self.tag_color_btn, (c[0], c[1], c[2]))
        
        if tag == 'animcolor1':
            c = cnfg['animcolors'][0]
            c[0], c[1], c[2] = color[0], color[1], color[2]
            ba.app.config.apply_and_commit()
            self.refresh_color_btn(self.animcolor_btn_1, (c[0], c[1], c[2]))
        
        if tag == 'animcolor2':
            c = cnfg['animcolors'][1]
            c[0], c[1], c[2] = color[0], color[1], color[2]
            ba.app.config.apply_and_commit()
            self.refresh_color_btn(self.animcolor_btn_2, (c[0], c[1], c[2]))
        
        if tag == 'animcolor3':
            c = cnfg['animcolors'][2]
            c[0], c[1], c[2] = color[0], color[1], color[2]
            ba.app.config.apply_and_commit()
            self.refresh_color_btn(self.animcolor_btn_3, (c[0], c[1], c[2]))
    
    def color_picker_closing(self, picker: ColorPicker) -> None:
        """
        Called when a color picker is closing.
        """
        if not self._root_widget:
            return
    
    def on_save(self) -> None:
        """
        Gets the text in text field of tag and then save it
        """
        text: str = cast(str, ba.textwidget(query=self.tagtextfield))
        profile = ba.app.config["TagConf"][self.profilename]
        if not text == "":
            profile['tag'] = text
            ba.app.config.apply_and_commit()
            ba.playsound(ba.getsound('gunCocking'))

            ba.containerwidget(edit=self._root_widget, transition='out_scale')
            ba.app.ui.set_main_menu_window(EditProfileWindow(
                                self.existing_profile,
                                self.in_main_menu,
                                transition='in_left').get_root_widget())
        else:
            ba.screenmessage(f"please define tag", color=(1,0,0))
            ba.playsound(ba.getsound('error'))


class CustomConfigNumberEdit:
    """A set of controls for editing a numeric config value.

    It will automatically save and apply the config when its
    value changes.

    Attributes:

        nametext
            The text widget displaying the name.

        valuetext
            The text widget displaying the current value.

        minusbutton
            The button widget used to reduce the value.

        plusbutton
            The button widget used to increase the value.
    """

    def __init__(self,
                 parent: ba.Widget,
                 configkey: List[str],
                 position: Tuple[float, float],
                 minval: float = 0.0,
                 maxval: float = 100.0,
                 increment: float = 1.0,
                 callback: Callable[[float], Any] = None,
                 xoffset: float = 0.0,
                 displayname: Union[str, ba.Lstr] = None,
                 changesound: bool = True,
                 textscale: float = 1.0) -> None:
        self._minval = minval
        self._maxval = maxval
        self._increment = increment
        self._callback = callback
        self._configkey = configkey
        self._value = ba.app.config[configkey[0]][configkey[1]][configkey[2]]

        self.nametext = ba.textwidget(
                parent=parent,
                position=position,
                size=(100, 30),
                text=displayname,
                maxwidth=160 + xoffset,
                color=(0.8, 0.8, 0.8),
                h_align='left',
                v_align='center',
                scale=textscale)
        
        self.valuetext = ba.textwidget(
                parent=parent,
                position=(246 + xoffset, position[1]),
                size=(60, 28),
                editable=False,
                color=(0.3, 1.0, 0.3, 1.0),
                h_align='right',
                v_align='center',
                text=str(self._value),
                padding=2)
        
        self.minusbutton = ba.buttonwidget(
                parent=parent,
                position=(330 + xoffset, position[1]),
                size=(28, 28),
                label='-',
                autoselect=True,
                on_activate_call=ba.Call(self._down),
                repeat=True,
                enable_sound=changesound)
        
        self.plusbutton = ba.buttonwidget(parent=parent,
                position=(380 + xoffset, position[1]),
                size=(28, 28),
                label='+',
                autoselect=True,
                on_activate_call=ba.Call(self._up),
                repeat=True,
                enable_sound=changesound)
        
        ba.uicleanupcheck(self, self.nametext)
        self._update_display()

    def _up(self) -> None:
        self._value = min(self._maxval, self._value + self._increment)
        self._changed()

    def _down(self) -> None:
        self._value = max(self._minval, self._value - self._increment)
        self._changed()

    def _changed(self) -> None:
        self._update_display()
        if self._callback:
            self._callback(self._value)
        ba.app.config[self._configkey[0]][self._configkey[1]][self._configkey[2]] = float(str(f'{self._value:.1f}'))
        ba.app.config.apply_and_commit()

    def _update_display(self) -> None:
        ba.textwidget(edit=self.valuetext, text=f'{self._value:.1f}')