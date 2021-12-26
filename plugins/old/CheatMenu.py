"""CheatMenu  | now cheat much as you can haha!! please eric sir dont kill me 

I apreciate any kind of modification. So feel free to use or edit code or change credit string.... no problem.
this mod uses activity loop cheacks if change in config and update it on our player node

Really awsome servers:
  Bombsquad Consultancy Service - https://discord.gg/2RKd9QQdQY
  bombspot - https://discord.gg/ucyaesh
  cyclones - https://discord.gg/pJXxkbQ7kH
"""
from __future__ import annotations

__author__ = 'egg'
__version__ = 1.0

import ba
import _ba

from bastd.ui.settings.allsettings import AllSettingsWindow
from bastd.actor.spaz import Spaz

from typing import (
    Tuple,
    Optional,
    Union
)


# Default Confings/Settings
CONFIG = "CheatMenu"
APPCONFIG = ba.app.config
Configs = {
    "Unlimited Heath": False,
    "SpeedBoots": False,
    "Fly": False,
    "SuperPunch": False,
    "Impact only": False
}


def setconfigs() -> None:
    """Set required defualt configs for mod"""
    if CONFIG not in APPCONFIG:
        APPCONFIG[str(CONFIG)] = Configs

    for c in Configs:
        if c not in APPCONFIG[str(CONFIG)]:
            APPCONFIG[str(CONFIG)][str(c)] = Configs[str(c)]
        else:
            pass
    APPCONFIG.apply_and_commit()


def update_config(config: str, change: any):
    """update's given value in json config file of pluguin"""
    APPCONFIG[str(CONFIG)][str(config)] = change
    APPCONFIG.apply_and_commit()


# ba_meta require api 6
# ba_meta export plugin
class Plugin(ba.Plugin):
    def on_app_launch(self) -> None:
        if _ba.env().get('build_number', 0) >= 20327:
            setconfigs()
            self.overwrite()
            self.call()
        else:
            print(f'{__name__} only works higher versions from 1.5')

    def overwrite(self) -> None:
        AllSettingsWindow.init = AllSettingsWindow.__init__
        AllSettingsWindow.__init__ = AllSettingsWindowInit

    def call(self):
        ba.timer(2, activity_loop, repeat=True)


# creating Cheat button, start button
def AllSettingsWindowInit(self, transition: str = 'in_right', origin_widget: ba.Widget = None):
    self.init(transition)

    uiscale = ba.app.ui.uiscale
    btn_width = 720 if uiscale is ba.UIScale.SMALL else 400
    btn_height = 380

    self.cheat_menu_btn = ba.buttonwidget(
        parent=self._root_widget,
        autoselect=True,
        position=(btn_width, btn_height),
        size=(105, 50),
        icon=ba.gettexture('settingsIcon'),
        label='Cheats',
        button_type='square',
        text_scale=1.2,
        on_activate_call=ba.Call(
            on_cheat_menu_btn_press, self))


# on cheat button press call Window
def on_cheat_menu_btn_press(self):
    ba.containerwidget(edit=self._root_widget,
                       transition='out_scale')
    ba.app.ui.set_main_menu_window(
        CheatMenuWindow(
            transition='in_right').get_root_widget())


class CheatMenuWindow(ba.Window):
    def __init__(self,
                 transition: Optional[str] = 'in_right') -> None:

        # background window, main widget parameters
        uiscale = ba.app.ui.uiscale
        self._width = 870.0 if uiscale is ba.UIScale.SMALL else 670.0
        self._height = (390.0 if uiscale is ba.UIScale.SMALL else
                        450.0 if uiscale is ba.UIScale.MEDIUM else 520.0)
        extra_x = 100 if uiscale is ba.UIScale.SMALL else 0
        self.extra_x = extra_x
        top_extra = 20 if uiscale is ba.UIScale.SMALL else 0

        # scroll widget parameters
        self._scroll_width = self._width - (100 + 2 * extra_x)
        self._scroll_height = self._height - 115.0
        self._sub_width = self._scroll_width * 0.95
        self._sub_height = 450.0
        self._spacing = 32
        self._extra_button_spacing = self._spacing * 2.5

        super().__init__(
            root_widget=ba.containerwidget(
                size=(self._width, self._height),
                transition=transition,
                scale=(2.06 if uiscale is ba.UIScale.SMALL else
                       1.4 if uiscale is ba.UIScale.MEDIUM else 1.0)))

        # back button widget
        self._back_button = ba.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(52 + self.extra_x,
                      self._height - 60 - top_extra),
            size=(60, 60),
            scale=0.8,
            label=ba.charstr(ba.SpecialChar.BACK),
            button_type='backSmall',
            on_activate_call=self._back)
        ba.containerwidget(edit=self._root_widget,
                           cancel_button=self._back_button)

        # window title, apears in top center of window
        self._title_text = ba.textwidget(
            parent=self._root_widget,
            position=(0, self._height - 40 - top_extra),
            size=(self._width, 25),
            text='Cheat Menu',
            color=ba.app.ui.title_color,
            scale=1.2,
            h_align='center',
            v_align='top')

        self._scrollwidget = ba.scrollwidget(
            parent=self._root_widget,
            position=(50 + extra_x, 50 - top_extra),
            simple_culling_v=20.0,
            highlight=False,
            size=(self._scroll_width,
                  self._scroll_height),
            selection_loops_to_parent=True)
        ba.widget(edit=self._scrollwidget,
                  right_widget=self._scrollwidget)

        # subcontainer represents scroll widget and used as parent
        self._subcontainer = ba.containerwidget(
            parent=self._scrollwidget,
            size=(self._sub_width,
                  self._sub_height),
            background=False,
            selection_loops_to_parent=True)

        v = self._sub_height - 35
        v -= self._spacing * 1.2
        conf = APPCONFIG[str(CONFIG)]

        for checkbox in Configs:
            ba.checkboxwidget(
                parent=self._subcontainer,
                autoselect=True,
                position=(25.0, v),
                size=(40, 40),
                text=checkbox,
                textcolor=(0.8, 0.8, 0.8),
                value=APPCONFIG[CONFIG][checkbox],
                on_value_change_call=ba.Call(
                    self.update, checkbox),
                scale=1.4,
                maxwidth=430)
            v -= 70

    def update(self, config: str, change) -> None:
        """Change config and get our sounds

        Args:
            config: str
            change: any
        """
        try:
            if change == True and config == "Fly":
                ba.screenmessage("Some maps may not work good for flying",
                                 color=(1, 0, 0))
            update_config(config, change)
            ba.playsound(ba.getsound('gunCocking'))
        except Exception:
            ba.screenmessage("error", color=(1, 0, 0))
            ba.playsound(ba.getsound('error'))

    def _back(self) -> None:
        """Kill the window and get back to previous one
        """
        ba.containerwidget(edit=self._root_widget,
                           transition='out_scale')
        ba.app.ui.set_main_menu_window(
            AllSettingsWindow(
                transition='in_left').get_root_widget())


def ishost():
    session = _ba.get_foreground_host_session()
    with _ba.Context(session):
        for player in session.sessionplayers:
            if player.inputdevice.client_id == -1:
                return True


def activity_loop():
    if _ba.get_foreground_host_activity() is not None:
        activity = _ba.get_foreground_host_activity()
        with _ba.Context(activity):
            for player in activity.players:
                if not ishost() or not player.actor:
                    return
                config = APPCONFIG[CONFIG]

                player.actor.node.invincible = config["Unlimited Heath"]
                player.actor.node.fly = config["Fly"]
                player.actor.node.hockey = config["SpeedBoots"]

                if config["SuperPunch"]:
                    player.actor._punch_power_scale = 7
                elif not config["SuperPunch"]:
                    player.actor._punch_power_scale = 1.2

                if config["Impact only"]:
                    player.actor.bomb_type = 'impact'
                elif not config["Impact only"]:
                    player.actor.bomb_type = 'normal'
