"""Define a simple example plugin."""

# ba_meta require api 6

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
import random
from bastd.ui.popup import PopupWindow
from bastd.ui.colorpicker import ColorPicker, ColorPickerExact
from bastd.ui.mainmenu import MainMenuWindow
from bastd.ui.account.settings import AccountSettingsWindow

if TYPE_CHECKING:
    from typing import Any, Tuple, Sequence, List, Optional


class ConfigCheckBox:
    """A checkbox wired up to control a config value.

    It will automatically save and apply the config when its
    value changes.

    Attributes:

        widget
            The underlying ba.Widget instance.
    """

    def __init__(self,
                 parent: ba.Widget,
                 configkey: str,
                 position: Tuple[float, float],
                 size: Tuple[float, float],
                 displayname: Union[str, ba.Lstr] = None,
                 scale: float = None,
                 maxwidth: float = None,
                 autoselect: bool = True,
                 value_change_call: Callable[[Any], Any] = None):
        if displayname is None:
            displayname = configkey
        self._value_change_call = value_change_call
        self._configkey = configkey
        self.widget = ba.checkboxwidget(
            parent=parent,
            autoselect=autoselect,
            position=position,
            size=size,
            text=displayname,
            textcolor=(0.8, 0.8, 0.8),
            value=ba.app.config.get(configkey),
            on_value_change_call=self._value_changed,
            scale=scale,
            maxwidth=maxwidth)
        # complain if we outlive our checkbox
        ba.uicleanupcheck(self, self.widget)

    def _value_changed(self, val: bool) -> None:
        cfg = ba.app.config
        cfg[self._configkey] = val
        if self._value_change_call is not None:
            self._value_change_call(val)
        cfg.apply_and_commit()

class CustomNameWindow(ba.Window):

    def __init__(self,
                 transition: str = 'in_right',
                 origin_widget: ba.Widget = None):

        app = ba.app
        uiscale = app.ui.uiscale

        cfg = ba.app.config.get
        name_str = cfg('Custom Name')
        if name_str is None:
            name_str = 'Test Name'

        self._name_color = cfg('Custom Name Color')
        if self._name_color is None:
            self._name_color = (1,1,1)

        self._width = 380
        self._height = 240
        super().__init__(root_widget=ba.containerwidget(
            size=(self._width, self._height),
            transition=transition,
            scale=(1.9 if uiscale is ba.UIScale.SMALL else
                   1.4 if uiscale is ba.UIScale.MEDIUM else 1.0)))
        ba.containerwidget(edit=self._root_widget,
                           on_cancel_call=self._back)

        save_button = ba.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(200, 30),
            size=(150, 50),
            label='Guardar',
            color=(0, 0.7, 0.5),
            textcolor=(1,1,1),
            on_activate_call=self._save)

        cancel_button = ba.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(30, 30),
            size=(150, 50),
            label='Cancelar',
            color=(0.61,0.3,0.18),
            textcolor=(1,1,1),
            on_activate_call=self._back)

        ba.textwidget(
            parent=self._root_widget,
            position=(125, 190),
            scale=0.9,
            size=(0.0, 0.0),
            autoselect=True,
            text=ba.Lstr(resource='editProfileWindow.nameText'),
            h_align='right',
            v_align='center',
            color=(1, 1, 1, 0.5))

        self._text_name = ba.textwidget(
            parent=self._root_widget,
            position=(140, 160),
            padding=5,
            size=(205,53),
            maxwidth=165,
            editable=True,
            autoselect=True,
            text=name_str,
            h_align='left',
            v_align='center',
            color=self._name_color)

        ba.textwidget(
            parent=self._root_widget,
            position=(90, 123),
            scale=0.9,
            size=(0.0, 0.0),
            autoselect=True,
            text=ba.Lstr(resource='editProfileWindow.colorText'),
            h_align='right',
            v_align='center',
            color=(1, 1, 1, 0.5))

        self._color_button = ba.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(108, 92),
            size=(60, 60),
            label='',
            button_type='square',
            color=self._name_color,
            on_activate_call=self._make_picker)

        self._random_checkbox = ConfigCheckBox(
            parent=self._root_widget,
            position=(195, 107),
            maxwidth=200,
            size=(250, 30),
            configkey='Random Color',
            displayname=ba.Lstr(resource='editProfileWindow.randomText'))

    def _make_picker(self) -> None:
        initial_color = self._name_color
        ColorPicker(
            parent=self._root_widget,
            position=(0,0),
            initial_color=initial_color,
            delegate=self)

    def _set_name_color(self, color: Tuple[float, float, float]) -> None:
        self._name_color = color
        if self._color_button:
            ba.buttonwidget(edit=self._color_button, color=color)
        if self._text_name:
            ba.textwidget(edit=self._text_name, color=color)

    def color_picker_closing(self, picker: ColorPicker) -> None:
        """Called when a color picker is closing."""
        if not self._root_widget:
            return
        ba.containerwidget(edit=self._root_widget,
                           selected_child=self._color_button)

    def color_picker_selected_color(self, picker: ColorPicker,
                                    color: Tuple[float, float, float]) -> None:
        """Called when a color is selected in a color picker."""
        if not self._root_widget:
            return
        self._set_name_color(color)

    def _save(self):
        self._name = ba.textwidget(query=self._text_name)
        cfg = ba.app.config
        cfg['Custom Name'] = self._name
        cfg['Custom Name Color'] = self._name_color
        cfg.commit()
        ba.playsound(ba.getsound('gunCocking'))
        self._back()

    def _back(self) -> None:
        ba.containerwidget(edit=self._root_widget,
                           transition='out_right')
        AccountSettingsWindow(transition='in_left')


# ba_meta export plugin
class AccountName(ba.Plugin):
    """My first ballistica plugin!"""

    def _new_refresh_not_in_game(
        self, positions: List[Tuple[float, float,
                                    float]]) -> Tuple[float, float, float]:
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        if not ba.app.did_menu_intro:
            self._tdelay = 2.0
            self._t_delay_inc = 0.02
            self._t_delay_play = 1.7
            ba.app.did_menu_intro = True
        self._width = 400.0
        self._height = 200.0
        enable_account_button = True

        cfg = ba.app.config.get
        account_type_name = cfg('Custom Name')
        if account_type_name is None:
            account_type_name = 'Test Name'

        account_type_icon = None
        account_type_icon_color = (1.0, 1.0, 1.0)
        account_type_call = self._show_account_window
        account_type_enable_button_sound = True
        b_count = 3  # play, help, credits
        if self._have_settings_button:
            b_count += 1
        if enable_account_button:
            b_count += 1
        if self._have_quit_button:
            b_count += 1
        if self._have_store_button:
            b_count += 1
        uiscale = ba.app.ui.uiscale
        if uiscale is ba.UIScale.SMALL:
            root_widget_scale = 1.6
            play_button_width = self._button_width * 0.65
            play_button_height = self._button_height * 1.1
            small_button_scale = 0.51 if b_count > 6 else 0.63
            button_y_offs = -20.0
            button_y_offs2 = -60.0
            self._button_height *= 1.3
            button_spacing = 1.04
        elif uiscale is ba.UIScale.MEDIUM:
            root_widget_scale = 1.3
            play_button_width = self._button_width * 0.65
            play_button_height = self._button_height * 1.1
            small_button_scale = 0.6
            button_y_offs = -55.0
            button_y_offs2 = -75.0
            self._button_height *= 1.25
            button_spacing = 1.1
        else:
            root_widget_scale = 1.0
            play_button_width = self._button_width * 0.65
            play_button_height = self._button_height * 1.1
            small_button_scale = 0.75
            button_y_offs = -80.0
            button_y_offs2 = -100.0
            self._button_height *= 1.2
            button_spacing = 1.1
        spc = self._button_width * small_button_scale * button_spacing
        ba.containerwidget(edit=self._root_widget,
                           size=(self._width, self._height),
                           background=False,
                           scale=root_widget_scale)
        assert not positions
        positions.append((self._width * 0.5, button_y_offs, 1.7))
        x_offs = self._width * 0.5 - (spc * (b_count - 1) * 0.5) + (spc * 0.5)
        for i in range(b_count - 1):
            positions.append(
                (x_offs + spc * i - 1.0, button_y_offs + button_y_offs2,
                 small_button_scale))
        # In kiosk mode, provide a button to get back to the kiosk menu.
        if ba.app.demo_mode or ba.app.arcade_mode:
            h, v, scale = positions[self._p_index]
            this_b_width = self._button_width * 0.4 * scale
            demo_menu_delay = 0.0 if self._t_delay_play == 0.0 else max(
                0, self._t_delay_play + 0.1)
            self._demo_menu_button = ba.buttonwidget(
                parent=self._root_widget,
                position=(self._width * 0.5 - this_b_width * 0.5, v + 90),
                size=(this_b_width, 45),
                autoselect=True,
                color=(0.45, 0.55, 0.45),
                textcolor=(0.7, 0.8, 0.7),
                label=ba.Lstr(resource='modeArcadeText' if ba.app.
                              arcade_mode else 'modeDemoText'),
                transition_delay=demo_menu_delay,
                on_activate_call=self._demo_menu_press)
        else:
            self._demo_menu_button = None
        uiscale = ba.app.ui.uiscale
        foof = (-1 if uiscale is ba.UIScale.SMALL else
                1 if uiscale is ba.UIScale.MEDIUM else 3)
        h, v, scale = positions[self._p_index]
        v = v + foof
        gather_delay = 0.0 if self._t_delay_play == 0.0 else max(
            0.0, self._t_delay_play + 0.1)
        assert play_button_width is not None
        assert play_button_height is not None
        this_h = h - play_button_width * 0.5 * scale - 40 * scale
        this_b_width = self._button_width * 0.25 * scale
        this_b_height = self._button_height * 0.82 * scale
        self._gather_button = btn = ba.buttonwidget(
            parent=self._root_widget,
            position=(this_h - this_b_width * 0.5, v),
            size=(this_b_width, this_b_height),
            autoselect=self._use_autoselect,
            button_type='square',
            label='',
            transition_delay=gather_delay,
            on_activate_call=self._gather_press)
        ba.textwidget(parent=self._root_widget,
                      position=(this_h, v + self._button_height * 0.33),
                      size=(0, 0),
                      scale=0.75,
                      transition_delay=gather_delay,
                      draw_controller=btn,
                      color=(0.75, 1.0, 0.7),
                      maxwidth=self._button_width * 0.33,
                      text=ba.Lstr(resource='gatherWindow.titleText'),
                      h_align='center',
                      v_align='center')
        icon_size = this_b_width * 0.6
        ba.imagewidget(parent=self._root_widget,
                       size=(icon_size, icon_size),
                       draw_controller=btn,
                       transition_delay=gather_delay,
                       position=(this_h - 0.5 * icon_size,
                                 v + 0.31 * this_b_height),
                       texture=ba.gettexture('usersButton'))

        # Play button.
        h, v, scale = positions[self._p_index]
        self._p_index += 1
        self._start_button = start_button = ba.buttonwidget(
            parent=self._root_widget,
            position=(h - play_button_width * 0.5 * scale, v),
            size=(play_button_width, play_button_height),
            autoselect=self._use_autoselect,
            scale=scale,
            text_res_scale=2.0,
            label=ba.Lstr(resource='playText'),
            transition_delay=self._t_delay_play,
            on_activate_call=self._play_press)
        ba.containerwidget(edit=self._root_widget,
                           start_button=start_button,
                           selected_child=start_button)
        v = v + foof
        watch_delay = 0.0 if self._t_delay_play == 0.0 else max(
            0.0, self._t_delay_play - 0.1)
        this_h = h + play_button_width * 0.5 * scale + 40 * scale
        this_b_width = self._button_width * 0.25 * scale
        this_b_height = self._button_height * 0.82 * scale
        self._watch_button = btn = ba.buttonwidget(
            parent=self._root_widget,
            position=(this_h - this_b_width * 0.5, v),
            size=(this_b_width, this_b_height),
            autoselect=self._use_autoselect,
            button_type='square',
            label='',
            transition_delay=watch_delay,
            on_activate_call=self._watch_press)
        ba.textwidget(parent=self._root_widget,
                      position=(this_h, v + self._button_height * 0.33),
                      size=(0, 0),
                      scale=0.75,
                      transition_delay=watch_delay,
                      color=(0.75, 1.0, 0.7),
                      draw_controller=btn,
                      maxwidth=self._button_width * 0.33,
                      text=ba.Lstr(resource='watchWindow.titleText'),
                      h_align='center',
                      v_align='center')
        icon_size = this_b_width * 0.55
        ba.imagewidget(parent=self._root_widget,
                       size=(icon_size, icon_size),
                       draw_controller=btn,
                       transition_delay=watch_delay,
                       position=(this_h - 0.5 * icon_size,
                                 v + 0.33 * this_b_height),
                       texture=ba.gettexture('tv'))
        if not self._in_game and enable_account_button:
            this_b_width = self._button_width
            h, v, scale = positions[self._p_index]
            self._p_index += 1
            self._gc_button = ba.buttonwidget(
                parent=self._root_widget,
                position=(h - this_b_width * 0.5 * scale, v),
                size=(this_b_width, self._button_height),
                scale=scale,
                label=account_type_name,
                autoselect=self._use_autoselect,
                on_activate_call=account_type_call,
                textcolor=(1,1,1),
                icon=account_type_icon,
                icon_color=account_type_icon_color,
                transition_delay=self._tdelay,
                enable_sound=account_type_enable_button_sound)

            # Scattered eggs on easter.
            if _ba.get_account_misc_read_val('easter',
                                             False) and not self._in_game:
                icon_size = 32
                ba.imagewidget(parent=self._root_widget,
                               position=(h - icon_size * 0.5 + 35,
                                         v + self._button_height * scale -
                                         icon_size * 0.24 + 1.5),
                               transition_delay=self._tdelay,
                               size=(icon_size, icon_size),
                               texture=ba.gettexture('egg2'),
                               tilt_scale=0.0)
            self._tdelay += self._t_delay_inc

            if ba.app.config.get('Random Color', True):
                color = (1, 0.15, 0.15)
                color2 = (0.2, 1, 0.2)
                color3 = (0.1, 0.1, 1)
                color4 = (0.2, 1, 1)
                color5 = (0.5, 0.25, 1.0)
                color6 = (1, 1, 0)
                self.time = 0.1
                def _update():
                    def _update2():
                        def _update3():
                            def _update4():
                                def _update5():
                                    def _update6():
                                        def _update7():
                                            ba.timer(
                                                self.time, _update)
                                        self.color = color6
                                        if self._gc_button:
                                            ba.buttonwidget(
                                                edit=self._gc_button,
                                                textcolor=self.color)
                                        ba.timer(
                                            self.time, _update7)
                                    self.color = color5
                                    if self._gc_button:
                                        ba.buttonwidget(
                                            edit=self._gc_button,
                                            textcolor=self.color)
                                    ba.timer(
                                        self.time, _update6)
                                self.color = color4
                                if self._gc_button:
                                    ba.buttonwidget(
                                        edit=self._gc_button,
                                        textcolor=self.color)
                                ba.timer(
                                    self.time, _update5)
                            self.color = color3
                            if self._gc_button:
                                ba.buttonwidget(
                                    edit=self._gc_button,
                                    textcolor=self.color)
                            ba.timer(
                                self.time, _update4)
                        self.color = color2
                        if self._gc_button:
                            ba.buttonwidget(
                                edit=self._gc_button,
                                textcolor=self.color)
                        ba.timer(
                            self.time, _update3)
                    self.color = color
                    if self._gc_button:
                        ba.buttonwidget(
                            edit=self._gc_button,
                            textcolor=self.color)
                    ba.timer(
                        self.time, _update2)
                self.color = color
                if self._gc_button:
                    ba.buttonwidget(
                        edit=self._gc_button,
                        textcolor=self.color)
                ba.timer(
                    self.time, _update)
            else:
                cfg = ba.app.config.get
                self.color = cfg('Custom Name Color')
                if self.color is None:
                    self.color = (1,1,1)
                if self._gc_button:
                    ba.buttonwidget(
                        edit=self._gc_button,
                        textcolor=self.color)
        else:
            self._gc_button = None

        # How-to-play button.
        h, v, scale = positions[self._p_index]
        self._p_index += 1
        btn = ba.buttonwidget(
            parent=self._root_widget,
            position=(h - self._button_width * 0.5 * scale, v),
            scale=scale,
            autoselect=self._use_autoselect,
            size=(self._button_width, self._button_height),
            label=ba.Lstr(resource=self._r + '.howToPlayText'),
            transition_delay=self._tdelay,
            on_activate_call=self._howtoplay)
        self._how_to_play_button = btn

        # Scattered eggs on easter.
        if _ba.get_account_misc_read_val('easter',
                                         False) and not self._in_game:
            icon_size = 28
            ba.imagewidget(parent=self._root_widget,
                           position=(h - icon_size * 0.5 + 30,
                                     v + self._button_height * scale -
                                     icon_size * 0.24 + 1.5),
                           transition_delay=self._tdelay,
                           size=(icon_size, icon_size),
                           texture=ba.gettexture('egg4'),
                           tilt_scale=0.0)
        # Credits button.
        self._tdelay += self._t_delay_inc
        h, v, scale = positions[self._p_index]
        self._p_index += 1
        self._credits_button = ba.buttonwidget(
            parent=self._root_widget,
            position=(h - self._button_width * 0.5 * scale, v),
            size=(self._button_width, self._button_height),
            autoselect=self._use_autoselect,
            label=ba.Lstr(resource=self._r + '.creditsText'),
            scale=scale,
            transition_delay=self._tdelay,
            on_activate_call=self._credits)
        self._tdelay += self._t_delay_inc
        return h, v, scale

    AccountSettingsWindow._old_refresh = AccountSettingsWindow._refresh
    def _new_refresh(self) -> None:
        self._old_refresh()

        def _do_new_window():
            ba.containerwidget(edit=self._root_widget,transition='out_left')
            CustomNameWindow()

        btn = ba.buttonwidget(
            parent=self._subcontainer,
            position=(440, 488),
            autoselect=True,
            size=(50, 50),
            color=(0.7, 0.0, 1.0),
            button_type='square',
            label='',
            on_activate_call=_do_new_window)
        ba.imagewidget(
            parent=self._subcontainer,
            position=(441, 489),
            size=(50, 50),
            draw_controller=btn,
            texture=ba.gettexture('settingsIcon'))

    def _new_refresh_account_name_text(self) -> None:
        if self._account_name_text is None:
            return
        cfg = ba.app.config.get
        name_str = cfg('Custom Name')
        if name_str is None:
            name_str = 'Test Name'
        self.color = cfg('Custom Name Color')
        if self.color is None:
            self.color = (1,1,1)
        ba.textwidget(edit=self._account_name_text,
                      text=name_str,
                      color=self.color)

    MainMenuWindow._refresh_not_in_game = _new_refresh_not_in_game
    AccountSettingsWindow._refresh = _new_refresh
    AccountSettingsWindow._refresh_account_name_text = (
                        _new_refresh_account_name_text)
