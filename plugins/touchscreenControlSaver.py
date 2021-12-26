# ba_meta require api 6
                     ###################
                     #   Credit- Droopy#3730   #
                     ###################
from __future__ import annotations

import _ba
import ba
from bastd.ui.settings import touchscreen
from bastd.ui import config
from typing import TYPE_CHECKING
import os, json
from bastd.ui.popup import PopupMenuWindow, PopupWindow
from ba._appconfig import *

if TYPE_CHECKING:
    from typing import Any, Union, Callable

json_file = _ba.env()['python_directory_user'] + '/SavedControls.json'
if not os.path.exists(json_file):
    with open(json_file, 'w') as f:
        json.dump({}, f)

class SaveWindow:
    def __init__(self):
        uiscale = ba.app.ui.uiscale
        self.cfgkeys = [
            'Touch Movement Control Type', 'Touch Action Control Type',
            'Touch Controls Scale', 'Touch Controls Scale Movement',
            'Touch Controls Scale Actions', 'Touch Controls Swipe Hidden',
            'Touch DPad X', 'Touch DPad Y', 'Touch Buttons X',
            'Touch Buttons Y'
        ]
        self._root_widget = ba.containerwidget(size=(500,250),
                                            transition='in_scale',
                                            toolbar_visibility='menu_minimal_no_back',
                                            parent=_ba.get_special_widget('overlay_stack'),
                                            on_outside_click_call=self._close,
                                            scale=(2.1 if uiscale is ba.UIScale.SMALL else
                                                   1.5 if uiscale is ba.UIScale.MEDIUM else 1.0))
        self._title_text = ba.textwidget(parent=self._root_widget,
                                         scale=1,
                                         color=(1,1,1),
                                         text='Save Current Controls',
                                         size=(0, 0),
                                         position=(250, 200),
                                         h_align='center',
                                         v_align='center')
        self._save_name_text = ba.textwidget(parent=self._root_widget,
                                         scale=0.8,
                                         color=(1,1,1),
                                         text='Save As : ',
                                         size=(0, 0),
                                         position=(40, 145),
                                         h_align='center',
                                         v_align='center')
        self._save_text_field = ba.textwidget(
                                 parent=self._root_widget,
                                 editable=True,
                                 size=(350, 60),
                                 position=(100, 120),
                                 text='',
                                 maxwidth=410,
                                 flatness=1.0,
                                 autoselect=True,
                                 v_align='center',
                                 corner_scale=0.7)
        self._add = ba.buttonwidget(parent=self._root_widget,
                              size=(100,40),
                              label='Add',
                              button_type='square',
                              autoselect=True,
                              position=(110, 60),
                              on_activate_call=self._add_new)
        self._remove = ba.buttonwidget(parent=self._root_widget,
                              size=(100,40),
                              label='Remove',
                              button_type='square',
                              autoselect=True,
                              position=(230, 60),
                              on_activate_call=self._remove_cntrl)
        self._load = ba.buttonwidget(parent=self._root_widget,
                              size=(100,100),
                              label='Load\nSaved\nControls',
                              button_type='square',
                              autoselect=True,
                              position=(365, 77),
                              on_activate_call=self._load_id)
        ba.containerwidget(edit=self._root_widget,
                           on_cancel_call=self._close)

    def _add_new(self):
        try:
            name = ba.textwidget(query=self._save_text_field)
            cfg = ba.app.config
            saved = self.read_controls()
            if name not in saved:
                saved[name] = {}
                for cfgkey in self.cfgkeys:
                    if cfgkey in cfg:
                        saved[name][cfgkey] = cfg[cfgkey]
                self.write_controls(saved)
                ba.screenmessage(f"Added {name}.", color=(0,1,0))
                self._close()
            else:
                ba.screenmessage("Control Name Already Exists...\nTry Adding With New Name.", color=(1,0,0))
        except Exception as e:
            print(e)

    def _remove_cntrl(self):
        try:
            uiscale = ba.app.ui.uiscale
            saved = self.read_controls()
            if len(saved) > 0:
                choices = [i for i in saved]
                PopupMenuWindow(position=self._remove.get_screen_space_center(),
                                        scale=(2.4 if uiscale is ba.UIScale.SMALL else
                                               1.5 if uiscale is ba.UIScale.MEDIUM else 1.0),
                                        choices=choices,
                                        current_choice=choices[0],
                                        delegate=self)
                self._popup_type = 'removeSavedContrl'
            else:
                ba.screenmessage("No Saved Controls Found", color=(1,0,0))
        except Exception as e:
            print(e)

    def _load_id(self):
        try:
            uiscale = ba.app.ui.uiscale
            saved = self.read_controls()
            if len(saved) > 0:
                choices = [i for i in saved]
                PopupMenuWindow(position=self._load.get_screen_space_center(),
                                        scale=(2.4 if uiscale is ba.UIScale.SMALL else
                                               1.5 if uiscale is ba.UIScale.MEDIUM else 1.0),
                                        choices=choices,
                                        current_choice=choices[0],
                                        delegate=self)
                self._popup_type = 'load_cntrl'
            else:
                ba.screenmessage("No Saved Controls Found", color=(1,0,0))
        except Exception as e:
            print(e)

    def read_controls(self):
        with open(json_file, 'r') as f:
            try:
                data = json.load(f)
                return data
            except:
                return {}

    def write_controls(self, data):
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow,
                                   choice: str) -> None:
        """Called when a choice is selected in the popup."""
        try:
            if self._popup_type == 'removeSavedContrl':
                ba.screenmessage(f"Removed {choice}", color=(1,0,0))
                saved = self.read_controls()
                saved.pop(choice)
                self.write_controls(saved)
            if self._popup_type == 'load_cntrl':
                cfg = ba.app.config
                saved = self.read_controls()
                for cfgkey in self.cfgkeys:
                    if cfgkey in saved[choice]:
                        cfg[cfgkey] = saved[choice][cfgkey]
                    elif cfgkey in cfg:
                        del cfg[cfgkey]
                cfg.apply_and_commit()
                self._close()
        except Exception as e:
            print(e)

    def popup_menu_closing(self, popup_window: PopupWindow) -> None:
        """Called when the popup is closing."""

    def _close(self):
        ba.containerwidget(edit=self._root_widget,
                           transition=('out_scale'))
        _ba.set_touchscreen_editing(True)

class MyTouchscreenSettingsWindow(ba.Window):
    """Settings window for touchscreens."""

    def __del__(self) -> None:
        # Note - this happens in 'back' too;
        # we just do it here too in case the window is closed by other means.

        # FIXME: Could switch to a UI destroy callback now that those are a
        #  thing that exists.
        _ba.set_touchscreen_editing(False)

    def __init__(self) -> None:

        self._width = 650
        self._height = 380
        self._spacing = 40
        self._r = 'configTouchscreenWindow'
        self.cfgkeys = [
            'Touch Movement Control Type', 'Touch Action Control Type',
            'Touch Controls Scale', 'Touch Controls Scale Movement',
            'Touch Controls Scale Actions', 'Touch Controls Swipe Hidden',
            'Touch DPad X', 'Touch DPad Y', 'Touch Buttons X',
            'Touch Buttons Y'
        ]

        _ba.set_touchscreen_editing(True)

        uiscale = ba.app.ui.uiscale
        super().__init__(root_widget=ba.containerwidget(
            size=(self._width, self._height),
            transition='in_right',
            scale=(1.9 if uiscale is ba.UIScale.SMALL else
                   1.55 if uiscale is ba.UIScale.MEDIUM else 1.2)))

        btn = ba.buttonwidget(parent=self._root_widget,
                              position=(35, self._height - 60),
                              size=(120, 60),
                              label=ba.Lstr(resource='backText'),
                              button_type='back',
                              scale=0.8,
                              on_activate_call=self._back)
        save_btn = ba.buttonwidget(parent=self._root_widget,
                              position=(self._width - 120, self._height - 60),
                              size=(60, 60),
                              label="",
                              icon=ba.gettexture('settingsIcon'),
                              iconscale=1.2,
                              scale=0.8,
                              on_activate_call=self._save)
        ba.containerwidget(edit=self._root_widget, cancel_button=btn)

        ba.textwidget(parent=self._root_widget,
                      position=(10, self._height - 50),
                      size=(self._width, 25),
                      text=ba.Lstr(resource=self._r + '.titleText'),
                      color=ba.app.ui.title_color,
                      maxwidth=280,
                      h_align='center',
                      v_align='center')

        ba.buttonwidget(edit=btn,
                        button_type='backSmall',
                        size=(60, 60),
                        label=ba.charstr(ba.SpecialChar.BACK))

        self._scroll_width = self._width - 100
        self._scroll_height = self._height - 110
        self._sub_width = self._scroll_width - 20
        self._sub_height = 360

        self._scrollwidget = ba.scrollwidget(
            parent=self._root_widget,
            position=((self._width - self._scroll_width) * 0.5,
                      self._height - 65 - self._scroll_height),
            size=(self._scroll_width, self._scroll_height),
            claims_left_right=True,
            claims_tab=True,
            selection_loops_to_parent=True)
        self._subcontainer = ba.containerwidget(parent=self._scrollwidget,
                                                size=(self._sub_width,
                                                      self._sub_height),
                                                background=False,
                                                claims_left_right=True,
                                                claims_tab=True,
                                                selection_loops_to_parent=True)
        self._build_gui()

    def _build_gui(self) -> None:
        from bastd.ui.config import ConfigNumberEdit, ConfigCheckBox
        from bastd.ui.radiogroup import make_radio_group

        # Clear anything already there.
        children = self._subcontainer.get_children()
        for child in children:
            child.delete()
        h = 30
        v = self._sub_height - 85
        clr = (0.8, 0.8, 0.8, 1.0)
        clr2 = (0.8, 0.8, 0.8)
        ba.textwidget(parent=self._subcontainer,
                      position=(-10, v + 43),
                      size=(self._sub_width, 25),
                      text=ba.Lstr(resource=self._r + '.swipeInfoText'),
                      flatness=1.0,
                      color=(0, 0.9, 0.1, 0.7),
                      maxwidth=self._sub_width * 0.9,
                      scale=0.55,
                      h_align='center',
                      v_align='center')
        cur_val = ba.app.config.get('Touch Movement Control Type', 'swipe')
        ba.textwidget(parent=self._subcontainer,
                      position=(h, v - 2),
                      size=(0, 30),
                      text=ba.Lstr(resource=self._r + '.movementText'),
                      maxwidth=190,
                      color=clr,
                      v_align='center')
        cb1 = ba.checkboxwidget(parent=self._subcontainer,
                                position=(h + 220, v),
                                size=(170, 30),
                                text=ba.Lstr(resource=self._r +
                                             '.joystickText'),
                                maxwidth=100,
                                textcolor=clr2,
                                scale=0.9)
        cb2 = ba.checkboxwidget(parent=self._subcontainer,
                                position=(h + 357, v),
                                size=(170, 30),
                                text=ba.Lstr(resource=self._r + '.swipeText'),
                                maxwidth=100,
                                textcolor=clr2,
                                value=False,
                                scale=0.9)
        make_radio_group((cb1, cb2), ('joystick', 'swipe'), cur_val,
                         self._movement_changed)
        v -= 50
        ConfigNumberEdit(parent=self._subcontainer,
                         position=(h, v),
                         xoffset=65,
                         configkey='Touch Controls Scale Movement',
                         displayname=ba.Lstr(resource=self._r +
                                             '.movementControlScaleText'),
                         changesound=False,
                         minval=0.1,
                         maxval=4.0,
                         increment=0.1)
        v -= 50
        cur_val = ba.app.config.get('Touch Action Control Type', 'buttons')
        ba.textwidget(parent=self._subcontainer,
                      position=(h, v - 2),
                      size=(0, 30),
                      text=ba.Lstr(resource=self._r + '.actionsText'),
                      maxwidth=190,
                      color=clr,
                      v_align='center')
        cb1 = ba.checkboxwidget(parent=self._subcontainer,
                                position=(h + 220, v),
                                size=(170, 30),
                                text=ba.Lstr(resource=self._r +
                                             '.buttonsText'),
                                maxwidth=100,
                                textcolor=clr2,
                                scale=0.9)
        cb2 = ba.checkboxwidget(parent=self._subcontainer,
                                position=(h + 357, v),
                                size=(170, 30),
                                text=ba.Lstr(resource=self._r + '.swipeText'),
                                maxwidth=100,
                                textcolor=clr2,
                                scale=0.9)
        make_radio_group((cb1, cb2), ('buttons', 'swipe'), cur_val,
                         self._actions_changed)
        v -= 50
        ConfigNumberEdit(parent=self._subcontainer,
                         position=(h, v),
                         xoffset=65,
                         configkey='Touch Controls Scale Actions',
                         displayname=ba.Lstr(resource=self._r +
                                             '.actionControlScaleText'),
                         changesound=False,
                         minval=0.1,
                         maxval=5.0,
                         increment=0.1)

        v -= 50
        ConfigCheckBox(parent=self._subcontainer,
                       position=(h, v),
                       size=(400, 30),
                       maxwidth=400,
                       configkey='Touch Controls Swipe Hidden',
                       displayname=ba.Lstr(resource=self._r +
                                           '.swipeControlsHiddenText'))
        v -= 65

        ba.buttonwidget(parent=self._subcontainer,
                        position=(self._sub_width * 0.5 - 70, v),
                        size=(170, 60),
                        label=ba.Lstr(resource=self._r + '.resetText'),
                        scale=0.75,
                        on_activate_call=self._reset)

        ba.textwidget(parent=self._root_widget,
                      position=(self._width * 0.5, 38),
                      size=(0, 0),
                      h_align='center',
                      text=ba.Lstr(resource=self._r + '.dragControlsText'),
                      maxwidth=self._width * 0.8,
                      scale=0.65,
                      color=(1, 1, 1, 0.4))

    def _actions_changed(self, v: str) -> None:
        cfg = ba.app.config
        cfg['Touch Action Control Type'] = v
        cfg.apply_and_commit()

    def _movement_changed(self, v: str) -> None:
        cfg = ba.app.config
        cfg['Touch Movement Control Type'] = v
        cfg.apply_and_commit()

    def _reset(self) -> None:
        cfg = ba.app.config
        for cfgkey in self.cfgkeys:
            if cfgkey in cfg:
                del cfg[cfgkey]
        cfg.apply_and_commit()
        ba.timer(0, self._build_gui, timetype=ba.TimeType.REAL)

    def _save(self):
        _ba.set_touchscreen_editing(False) 
        SaveWindow()

    def _back(self) -> None:
        from bastd.ui.settings import controls
        ba.containerwidget(edit=self._root_widget, transition='out_right')
        ba.app.ui.set_main_menu_window(
            controls.ControlsSettingsWindow(
                transition='in_left').get_root_widget())
        _ba.set_touchscreen_editing(False)


# ba_meta export plugin
class InitalRun(ba.Plugin):
    def __init__(self):
        touchscreen.TouchscreenSettingsWindow = MyTouchscreenSettingsWindow
