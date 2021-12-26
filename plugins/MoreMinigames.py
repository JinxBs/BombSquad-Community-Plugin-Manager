"""More Minigames."""
# Created by: byANG3L

# ba_meta require api 6
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import ba
import os
import _ba
import math
import random
import time
import weakref
from enum import Enum
from bastd.ui import popup
from ba._language import Lstr
from bastd.ui.tabs import TabRow
from ba._error import print_exception
from bastd.ui.coop.gamebutton import GameButton
from ba._campaign import register_campaign, Campaign
from ba.internal import getcampaign
from bastd.ui.mainmenu import MainMenuWindow as MMW
from bastd.mainmenu import MainMenuActivity as MMA

if TYPE_CHECKING:
    from typing import Type, Any, Callable, Dict, Union, List, Tuple, Optional

cfg = ba.app.config
cgsc = {'button_name': 'Mini Games',
        'name_color': (0.75, 1.0, 0.7),
        'button_color': (0.6, 0.0, 0.9),
        'image_button': 'heart',
        'image_color': (0.9, 0.2, 0.2),
        'image_h': 0,
        'image_v': 0,
        'image_val': 1,
        'image_scale': 0,
        'window_color': (0.4, 0.0, 1.0),
        'window_titlecolor': (1.0, 1.0, 1.0),
        'game_textcolor': (1.0, 1.0, 1.0),
        'game_icon': 'star',
        'game_iconcolor': (1.0, 1.0, 0.0),
        'game_color': (0.4, 0.9, 0.9),
        'settings_color': (0.4, 0.9, 0.9),
        'settings_texcolor': (1.0, 1.0, 1.0)}

lang = ba.app.lang.language
if lang == 'Spanish':
    mmbutton = 'Botón'
    mmwindow = 'Ventana'
    mmgame = 'Juego'
    mmbnombre = 'nombre:'
    mmbtext = 'texto'
    mmbtexture = 'textura'
    mmbbutton = 'botón'
    mmbimage = 'Imagen'
    mmbsavename = 'Guardar Nombre'
    mmwtitle = 'Título'
    mmwtitlecolor = 'título'
    mmwwindow = 'ventana'
    mmwicon = 'icono'
else:
    mmbutton = 'Button'
    mmwindow = 'Window'
    mmgame = 'Game'
    mmbnombre = 'name:'
    mmbtext = 'text'
    mmbtexture = 'texture'
    mmbbutton = 'button'
    mmbimage = 'Image'
    mmbsavename = 'Save Name'
    mmwtitle = 'Title'
    mmwtitlecolor = 'title'
    mmwwindow = 'window'
    mmwicon = 'icon'

def new_window(self) -> None:
    ba.containerwidget(edit=self._root_widget, transition='out_left')
    ba.app.ui.set_main_menu_window(
        PlayModsWindow(origin_widget=self._test_button).get_root_widget())

class GameButton(GameButton):
    def __init__(self, window: PlayModsWindow, parent: ba.Widget, game: str,
                 x: float, y: float, select: bool, row: str):
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-locals
        self._game = game
        sclx = 195.0
        scly = 195.0

        campaignname, levelname = game.split(':')

        rating: Optional[float]
        campaign = getcampaign(campaignname)
        rating = campaign.getlevel(levelname).rating

        if rating is None or rating == 0.0:
            stars = 0
        elif rating >= 9.5:
            stars = 3
        elif rating >= 7.5:
            stars = 2
        else:
            stars = 1

        self._button = btn = ba.buttonwidget(
            parent=parent,
            position=(x + 23, y + 4),
            size=(sclx, scly),
            label='',
            color=cfg['CGS']['game_color'],
            on_activate_call=ba.Call(window.run, game),
            button_type='square',
            autoselect=True)
        ba.widget(edit=btn,
                  show_buffer_bottom=50,
                  show_buffer_top=50,
                  show_buffer_left=400,
                  show_buffer_right=200)
        if select:
            ba.containerwidget(edit=parent,
                               selected_child=btn,
                               visible_child=btn)
        image_width = sclx * 0.85 * 0.75
        self._preview_widget = ba.imagewidget(
            parent=parent,
            draw_controller=btn,
            position=(x + 21 + sclx * 0.5 - image_width * 0.5, y + scly - 104),
            size=(image_width, image_width * 0.5),
            model_transparent=window.lsbt,
            model_opaque=window.lsbo,
            texture=campaign.getlevel(levelname).get_preview_texture(),
            mask_texture=ba.gettexture('mapPreviewMask'))

        translated = campaign.getlevel(levelname).displayname
        self._achievements = ba.app.ach.achievements_for_coop_level(game)

        self._name_widget = ba.textwidget(parent=parent,
                                          draw_controller=btn,
                                          position=(x + 20 + sclx * 0.5,
                                                    y + scly - 27),
                                          size=(0, 0),
                                          h_align='center',
                                          text=translated,
                                          color=cfg['CGS']['game_textcolor'],
                                          v_align='center',
                                          maxwidth=sclx * 0.76,
                                          scale=0.85)
        xscl = x + (67 if self._achievements else 50)
        yscl = y + scly - (137 if self._achievements else 157)

        starscale = 35.0 if self._achievements else 45.0

        self._star_widgets: List[ba.Widget] = []
        for _i in range(stars):
            imw = ba.imagewidget(parent=parent,
                                 draw_controller=btn,
                                 position=(xscl, yscl),
                                 color=cfg['CGS']['game_iconcolor'],
                                 size=(starscale, starscale),
                                 texture=window.star_tex)
            self._star_widgets.append(imw)
            xscl += starscale
        for _i in range(3 - stars):
            ba.imagewidget(parent=parent,
                           draw_controller=btn,
                           position=(xscl, yscl),
                           size=(starscale, starscale),
                           color=(0, 0, 0),
                           texture=window.star_tex,
                           opacity=0.3)
            xscl += starscale

        xach = x + 69
        yach = y + scly - 168
        a_scale = 30.0
        self._achievement_widgets: List[Tuple[ba.Widget, ba.Widget]] = []
        for ach in self._achievements:
            a_complete = ach.complete
            imw = ba.imagewidget(
                parent=parent,
                draw_controller=btn,
                position=(xach, yach),
                size=(a_scale, a_scale),
                color=tuple(ach.get_icon_color(a_complete)[:3])
                if a_complete else (1.2, 1.2, 1.2),
                texture=ach.get_icon_texture(a_complete))
            imw2 = ba.imagewidget(parent=parent,
                                  draw_controller=btn,
                                  position=(xach, yach),
                                  size=(a_scale, a_scale),
                                  color=(2, 1.4, 0.4),
                                  texture=window.a_outline_tex,
                                  model_transparent=window.a_outline_model)
            self._achievement_widgets.append((imw, imw2))
            # if a_complete:
            xach += a_scale * 1.2

        # give a quasi-random update increment to spread the load..
        self._update_timer = ba.Timer(0.001 * (900 + random.randrange(200)),
                                      ba.WeakCall(self._update),
                                      repeat=True,
                                      timetype=ba.TimeType.REAL)
        self._update()

    def get_button(self) -> ba.Widget:
        """Return the underlying button ba.Widget."""
        return self._button

    def _update(self) -> None:
        # pylint: disable=too-many-boolean-expressions
        from ba.internal import getcampaign

        # In case we stick around after our UI...
        if not self._button:
            return

        game = self._game
        campaignname, levelname = game.split(':')
        campaign = getcampaign(campaignname)


class PlayModsWindow(ba.Window):

    def __init__(self,
                 transition: Optional[str] = 'in_right',
                 origin_widget: ba.Widget = None):
        # pylint: disable=too-many-statements
        # pylint: disable=cyclic-import

        # If they provided an origin-widget, scale up from that.
        scale_origin: Optional[Tuple[float, float]]
        if origin_widget is not None:
            self._transition_out = 'out_scale'
            scale_origin = origin_widget.get_screen_space_center()
            transition = 'in_scale'
        else:
            self._transition_out = 'out_left'
            scale_origin = None

        app = ba.app
        uiscale = ba.app.ui.uiscale
        self._width = 1320 if uiscale is ba.UIScale.SMALL else 1120
        self._x_inset = x_inset = 100 if uiscale is ba.UIScale.SMALL else 0
        self._height = (657 if uiscale is ba.UIScale.SMALL else
                        730 if uiscale is ba.UIScale.MEDIUM else 800)
        top_extra = 20 if uiscale is ba.UIScale.SMALL else 0
        app.ui.set_main_menu_location('Custom Games')

        super().__init__(root_widget=ba.containerwidget(
            size=(self._width, self._height + top_extra),
            toolbar_visibility='menu_full',
            color=cfg['CGS']['window_color'],
            scale_origin_stack_offset=scale_origin,
            stack_offset=((0, -15) if uiscale is ba.UIScale.SMALL else (
                0, 0) if uiscale is ba.UIScale.MEDIUM else (0, 0)),
            transition=transition,
            scale=(1.2 if uiscale is ba.UIScale.SMALL else
                   0.8 if uiscale is ba.UIScale.MEDIUM else 0.75)))

        self._back_button = btn = ba.buttonwidget(
            parent=self._root_widget,
            position=(75 + x_inset, self._height - 87 -
                      (4 if uiscale is ba.UIScale.SMALL else 0) + 6),
            size=(60, 50),
            scale=1.2,
            autoselect=True,
            label=ba.charstr(ba.SpecialChar.BACK),
            button_type='backSmall',
            on_activate_call=self._back)

        v = self._height - 95
        txt = ba.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5,
                      v + 40 - (0 if uiscale is ba.UIScale.SMALL else 0)),
            size=(0, 0),
            text=ba.Lstr(resource='playModes.singlePlayerCoopText',
                         fallback_resource='playModes.coopText'),
            h_align='center',
            color=cfg['CGS']['window_titlecolor'],
            scale=1.5,
            maxwidth=500,
            v_align='center')

        # options
        self._options_button = ba.buttonwidget(
            parent=self._root_widget,
            position=(self._width - 150 - x_inset, self._height - 87 -
                      (4 if uiscale is ba.UIScale.SMALL else 0) + 4),
            size=(48, 48),
            scale=1.2,
            autoselect=True,
            label='',
            color=cfg['CGS']['settings_color'],
            button_type='square',
            on_activate_call=self._options)
        ba.imagewidget(
            parent=self._root_widget,
            position=(self._width - 150 - x_inset, self._height - 87 -
                      (4 if uiscale is ba.UIScale.SMALL else 0) + 4),
            size=(60, 60),
            color=cfg['CGS']['settings_texcolor'],
            draw_controller=self._options_button,
            texture=ba.gettexture('settingsIcon'))

        self.star_tex = ba.gettexture(cfg['CGS']['game_icon'])
        self.lsbt = ba.getmodel('level_select_button_transparent')
        self.lsbo = ba.getmodel('level_select_button_opaque')
        self.a_outline_tex = ba.gettexture('achievementOutline')
        self.a_outline_model = ba.getmodel('achievementOutline')

        self._scroll_width = self._width - (130 + 2 * x_inset)
        self._scroll_height = (self._height -
                               (190 if uiscale is ba.UIScale.SMALL
                                and app.ui.use_toolbars else 160))

        self._subcontainerwidth = 800.0
        self._subcontainerheight = 1400.0

        self._scrollwidget = ba.scrollwidget(
            parent=self._root_widget,
            highlight=False,
            position=(65 + x_inset, 120) if uiscale is ba.UIScale.SMALL
            and app.ui.use_toolbars else (65 + x_inset, 70),
            size=(self._scroll_width, self._scroll_height),
            simple_culling_v=10.0,
            claims_left_right=True,
            claims_tab=True,
            selection_loops_to_parent=True)


        ba.containerwidget(edit=self._root_widget,
                           selected_child=self._scrollwidget)
        if self._back_button is not None:
            ba.containerwidget(edit=self._root_widget,
                               cancel_button=self._back_button,)
        else:
            ba.containerwidget(edit=self._root_widget,
                               on_cancel_call=self._back)

        items = [
        ]
        # add all custom user levels here..
        items += [
            'User:' + l.name
            for l in getcampaign('User').levels
        ]
        print(items)
        count = len(items)
        columns = 4
        rows = int(math.ceil(float(count) / columns))
        self._custom_buttons: List[GameButton] = []
        self._sub_width = self._scroll_width * 0.95
        self._sub_height = 40 + rows * (195)
        self._subcontainer = ba.containerwidget(
            parent=self._scrollwidget,
            size=(self._sub_width, self._sub_height),
            background=False)
        h_spacing = 210
        h_origin = 40
        h = h_origin
        v = self._sub_height - 220
        index = 0
        y = 0
        for item in items:
            index += 1
            self._custom_buttons.append(
                GameButton(self, self._subcontainer, item, h, v,
                           None, None))
            h += h_spacing
            if index == 4:
                h = h_origin
                v -= 195
                index = 0
                y += 1

            for btn in self._custom_buttons:
                if y==0:
                    ba.widget(
                        edit=btn.get_button(),
                        up_widget=self._back_button)

    def run(self, game: Optional[str]) -> None:
        ba.app.launch_coop_game(game)

    def _options(self) -> None:
        ba.containerwidget(edit=self._root_widget,
                           transition='out_left')
        ba.app.ui.set_main_menu_window(
            OptionsWindow(origin_widget=self._options_button).get_root_widget())

    def _back(self) -> None:
        # pylint: disable=cyclic-import
        from bastd.ui.mainmenu import MainMenuWindow
        ba.containerwidget(edit=self._root_widget,
                           transition='out_scale')
        ba.app.ui.set_main_menu_window(
            MainMenuWindow(transition='in_left').get_root_widget())

class PosImage(popup.PopupWindow):
    """A popup UI to select from a set of colors.

    Passes the color to the delegate's color_picker_selected_color() method.
    """

    def __init__(self,
                 parent: ba.Widget,
                 position: Tuple[float, float],
                 scale: float = None,
                 offset: Tuple[float, float] = (0.0, 0.0)):
        # pylint: disable=too-many-locals
        del parent  # unused here
        self._transitioning_out = False

        self._width = 250
        self._height = 220
        app = ba.app
        uiscale = ba.app.ui.uiscale
        scale = (2.4 if uiscale is ba.UIScale.SMALL else
                 1.65 if uiscale is ba.UIScale.MEDIUM else 1.2)
        extra_h = 150 if uiscale is ba.UIScale.SMALL else 0

        # Create our _root_widget.
        popup.PopupWindow.__init__(self,
                                   position=(position[0] + extra_h, position[1]),
                                   size=(self._width, self._height),
                                   scale=scale,
                                   bg_color=(0.5, 0.5, 0.5),
                                   offset=offset)
        parent = self.root_widget
        val_x = cfg['CGS']['image_h']
        val_y = cfg['CGS']['image_v']
        val_s = cfg['CGS']['image_scale']
        self._val_x = round(val_x, 1)
        self._val_y = round(val_y, 1)
        self._val_s = round(val_s, 1)
        self._value_change = cfg['CGS']['image_val']

        pos_val = self._height * 0.8
        pos_image_x = self._height * 0.57
        pos_image_y = self._height * 0.36
        pos_image_s = self._height * 0.15

        pos_val_h = self._width * 0.135
        spacing = 50
        change_val = 0

        self._val1_button = ba.buttonwidget(
            parent=parent,
            position=(pos_val_h + change_val, pos_val),
            size=(28, 28),
            label='0.1',
            text_scale=0.8,
            autoselect=True,
            on_activate_call=self._val1,
            enable_sound=True)
        change_val += spacing
        self._val2_button = ba.buttonwidget(
            parent=parent,
            position=(pos_val_h + change_val, pos_val),
            size=(28, 28),
            label='1',
            text_scale=0.8,
            autoselect=True,
            on_activate_call=self._val2,
            enable_sound=True)
        change_val += spacing
        self._val3_button = ba.buttonwidget(
            parent=parent,
            position=(pos_val_h + change_val, pos_val),
            size=(28, 28),
            label='2',
            text_scale=0.8,
            autoselect=True,
            on_activate_call=self._val3,
            enable_sound=True)
        change_val += spacing
        self._val4_button = ba.buttonwidget(
            parent=parent,
            position=(pos_val_h + change_val, pos_val),
            size=(28, 28),
            label='5',
            text_scale=0.8,
            autoselect=True,
            on_activate_call=self._val4,
            enable_sound=True)

        ba.textwidget(
            parent=parent,
            position=(self._width * 0.05, pos_image_x),
            size=(100, 30),
            text='x :',
            maxwidth=160,
            color=(0.8, 0.8, 0.8, 1.0),
            h_align='left',
            v_align='center',
            scale=0.8)
        self.valuextext = ba.textwidget(
            parent=parent,
            position=(self._width * 0.24, pos_image_x),
            size=(60, 28),
            editable=False,
            color=(0.3, 1.0, 0.3, 1.0),
            h_align='right',
            v_align='center',
            text=str(cfg['CGS']['image_h']),
            scale=0.9,
            padding=2)
        ba.buttonwidget(
            parent=parent,
            position=(self._width * 0.56, pos_image_x),
            size=(28, 28),
            label='-',
            autoselect=True,
            on_activate_call=self._downx,
            enable_sound=True)
        ba.buttonwidget(
            parent=parent,
            position=(self._width * 0.76, pos_image_x),
            size=(28, 28),
            label='+',
            autoselect=True,
            on_activate_call=self._upx,
            enable_sound=True)

        ba.textwidget(
            parent=parent,
            position=(self._width * 0.05, pos_image_y),
            size=(100, 30),
            text='y :',
            maxwidth=160,
            color=(0.8, 0.8, 0.8, 1.0),
            h_align='left',
            v_align='center',
            scale=0.8)
        self.valueytext = ba.textwidget(
            parent=parent,
            position=(self._width * 0.24, pos_image_y),
            size=(60, 28),
            editable=False,
            color=(0.3, 1.0, 0.3, 1.0),
            h_align='right',
            v_align='center',
            text=str(cfg['CGS']['image_v']),
            scale=0.9,
            padding=2)
        ba.buttonwidget(
            parent=parent,
            position=(self._width * 0.56, pos_image_y),
            size=(28, 28),
            label='-',
            autoselect=True,
            on_activate_call=self._downy,
            enable_sound=True)
        ba.buttonwidget(
            parent=parent,
            position=(self._width * 0.76, pos_image_y),
            size=(28, 28),
            label='+',
            autoselect=True,
            on_activate_call=self._upy,
            enable_sound=True)

        ba.textwidget(
            parent=parent,
            position=(self._width * 0.05, pos_image_s),
            size=(100, 30),
            text='s :',
            maxwidth=160,
            color=(0.8, 0.8, 0.8, 1.0),
            h_align='left',
            v_align='center',
            scale=0.8)
        self.valuestext = ba.textwidget(
            parent=parent,
            position=(self._width * 0.24, pos_image_s),
            size=(60, 28),
            editable=False,
            color=(0.3, 1.0, 0.3, 1.0),
            h_align='right',
            v_align='center',
            text=str(cfg['CGS']['image_scale']),
            scale=0.9,
            padding=2)
        ba.buttonwidget(
            parent=parent,
            position=(self._width * 0.56, pos_image_s),
            size=(28, 28),
            label='-',
            autoselect=True,
            on_activate_call=self._downs,
            enable_sound=True)
        ba.buttonwidget(
            parent=parent,
            position=(self._width * 0.76, pos_image_s),
            size=(28, 28),
            label='+',
            autoselect=True,
            on_activate_call=self._ups,
            enable_sound=True)

        self._set_val_color()

    def _set_val_color(self) -> None:
        button_color_on = (0.5, 0.4, 0.93)
        button_color_off = (0.52, 0.48, 0.63)
        text_color_on = (0.85, 0.75, 0.95)
        text_color_off = (0.65, 0.6, 0.7)
        if self._value_change == 0.1:
            ba.buttonwidget(
                edit=self._val1_button,
                color=button_color_on,
                textcolor=text_color_on)
            ba.buttonwidget(
                edit=self._val2_button,
                color=button_color_off,
                textcolor=text_color_off)
            ba.buttonwidget(
                edit=self._val3_button,
                color=button_color_off,
                textcolor=text_color_off)
            ba.buttonwidget(
                edit=self._val4_button,
                color=button_color_off,
                textcolor=text_color_off)
        elif self._value_change == 1:
            ba.buttonwidget(
                edit=self._val1_button,
                color=button_color_off,
                textcolor=text_color_off)
            ba.buttonwidget(
                edit=self._val2_button,
                color=button_color_on,
                textcolor=text_color_on)
            ba.buttonwidget(
                edit=self._val3_button,
                color=button_color_off,
                textcolor=text_color_off)
            ba.buttonwidget(
                edit=self._val4_button,
                color=button_color_off,
                textcolor=text_color_off)
        elif self._value_change == 2:
            ba.buttonwidget(
                edit=self._val1_button,
                color=button_color_off,
                textcolor=text_color_off)
            ba.buttonwidget(
                edit=self._val2_button,
                color=button_color_off,
                textcolor=text_color_off)
            ba.buttonwidget(
                edit=self._val3_button,
                color=button_color_on,
                textcolor=text_color_on)
            ba.buttonwidget(
                edit=self._val4_button,
                color=button_color_off,
                textcolor=text_color_off)
        elif self._value_change == 5:
            ba.buttonwidget(
                edit=self._val1_button,
                color=button_color_off,
                textcolor=text_color_off)
            ba.buttonwidget(
                edit=self._val2_button,
                color=button_color_off,
                textcolor=text_color_off)
            ba.buttonwidget(
                edit=self._val3_button,
                color=button_color_off,
                textcolor=text_color_off)
            ba.buttonwidget(
                edit=self._val4_button,
                color=button_color_on,
                textcolor=text_color_on)

    def _val1(self) -> None:
        self._value_change = 0.1
        cfg['CGS']['image_val'] = self._value_change
        cfg.apply_and_commit()
        self._set_val_color()
    def _val2(self) -> None:
        self._value_change = 1
        cfg['CGS']['image_val'] = self._value_change
        cfg.apply_and_commit()
        self._set_val_color()
    def _val3(self) -> None:
        self._value_change = 2
        cfg['CGS']['image_val'] = self._value_change
        cfg.apply_and_commit()
        self._set_val_color()
    def _val4(self) -> None:
        self._value_change = 5
        cfg['CGS']['image_val'] = self._value_change
        cfg.apply_and_commit()
        self._set_val_color()

    def _upx(self) -> None:
        self._val_x += self._value_change
        self._changedx()

    def _downx(self) -> None:
        self._val_x -= self._value_change
        self._changedx()

    def _upy(self) -> None:
        self._val_y += self._value_change
        self._changedy()

    def _downy(self) -> None:
        self._val_y -= self._value_change
        self._changedy()

    def _ups(self) -> None:
        self._val_s += self._value_change
        self._changeds()

    def _downs(self) -> None:
        self._val_s -= self._value_change
        self._changeds()

    def _changedx(self) -> None:
        cfg['CGS']['image_h'] = round(self._val_x, 1)
        cfg.apply_and_commit()
        self._update_display()

    def _changedy(self) -> None:
        cfg['CGS']['image_v'] = round(self._val_y, 1)
        cfg.apply_and_commit()
        self._update_display()

    def _changeds(self) -> None:
        cfg['CGS']['image_scale'] = round(self._val_s, 1)
        cfg.apply_and_commit()
        self._update_display()

    def _update_display(self) -> None:
        valx = cfg['CGS']['image_h']
        valy = cfg['CGS']['image_v']
        vals = cfg['CGS']['image_scale']
        if valx == 0:
            image_h = '0.0'
        else:
            image_h = str(valx)
        if valy == 0:
            image_v = '0.0'
        else:
            image_v = str(valy)
        if vals == 0:
            image_s = '0.0'
        else:
            image_s = str(vals)
        ba.textwidget(edit=self.valuextext,
                      text=image_h)
        ba.textwidget(edit=self.valueytext,
                      text=image_v)
        ba.textwidget(edit=self.valuestext,
                      text=image_s)

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            ba.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        ba.playsound(ba.getsound('swish'))
        self._transition_out()

class ImagePicker(popup.PopupWindow):
    def __init__(self,
                 parent: ba.Widget,
                 position: Tuple[float, float] = (0.0, 0.0),
                 delegate: Any = None,
                 colorcfg: str = None,
                 selected_image: str = None):
        # pylint: disable=too-many-locals
        del parent  # unused here
        uiscale = ba.app.ui.uiscale
        scale = (1.85 if uiscale is ba.UIScale.SMALL else
                 1.65 if uiscale is ba.UIScale.MEDIUM else 1.23)

        self.colorcfg = colorcfg
        self._delegate = delegate
        self._transitioning_out = False

        images = [
            'achievementBoxer','achievementCrossHair',
            'achievementDualWielding','achievementEmpty',
            'achievementFlawlessVictory','achievementFootballShutout',
            'achievementFootballVictory','achievementFreeLoader',
            'achievementGotTheMoves','achievementInControl',
            'achievementMedalLarge','achievementMedalMedium',
            'achievementMedalSmall','achievementMine','achievementOffYouGo',
            'achievementOnslaught','achievementOutline','achievementRunaround',
            'achievementSharingIsCaring','achievementsIcon',
            'achievementStayinAlive','achievementSuperPunch',
            'achievementTeamPlayer','achievementTNT','achievementWall',
            'actionButtons','advancedIcon','aliSplash','analogStick',
            'audioIcon','backIcon','bombButton','buttonBomb','buttonJump',
            'buttonPickUp','buttonPunch','buttonSquare','chestIcon',
            'chestIconEmpty','chestIconMulti','chestOpenIcon','chTitleChar1',
            'chTitleChar2','chTitleChar3','chTitleChar4','chTitleChar5',
            'circle','circleOutline','circleShadow','circleZigZag','coin',
            'controllerIcon','crossOut','cursor','cuteSpaz','downButton',
            'egg1','egg2','egg3','egg4','file','folder','gameCenterIcon',
            'gameCircleIcon','googlePlayAchievementsIcon','googlePlayGamesIcon',
            'googlePlayLeaderboardsIcon','googlePlusIcon',
            'googlePlusSignInButton','graphicsIcon','heart','iircadeLogo',
            'inventoryIcon','leaderboardsIcon','leftButton','levelIcon',
            'lock','logIcon','logo','logoEaster','medalBronze','medalGold',
            'medalSilver','menuButton','nextLevelIcon','nub','ouyaAButton',
            'ouyaIcon','ouyaOButton','ouyaUButton','ouyaYButton','replayIcon',
            'rightButton','scorch','scorchBig','settingsIcon','shadow',
            'shadowSharp','shadowSoft','slash','softRect','softRect2',
            'softRectVertical','star','startButton','storeCharacter',
            'storeCharacterEaster','storeCharacterXmas','storeIcon',
            'textClearButton','ticketRoll','ticketRollBig','ticketRolls',
            'tickets','ticketsMore','touchArrows','touchArrowsActions',
            'trophy','tv','upButton','usersButton']
        count = len(images)

        columns = 3
        rows = int(math.ceil(float(count) / columns))

        button_width = 100
        button_height = 100
        button_buffer_h = 10
        button_buffer_v = 15

        self._width = (10 + columns * (button_width + 2 * button_buffer_h) *
                       (1.0 / 0.95) * (1.0 / 0.8))
        self._height = self._width * (0.8
                                      if uiscale is ba.UIScale.SMALL else 1.06)

        self._scroll_width = self._width * 0.8
        self._scroll_height = self._height * 0.8
        self._scroll_position = ((self._width - self._scroll_width) * 0.5,
                                 (self._height - self._scroll_height) * 0.5)

        # creates our _root_widget
        popup.PopupWindow.__init__(self,
                                   position=position,
                                   size=(self._width, self._height),
                                   scale=scale,
                                   bg_color=(0.5, 0.5, 0.5),
                                   offset=(0.0, 0.0),
                                   focus_position=self._scroll_position,
                                   focus_size=(self._scroll_width,
                                               self._scroll_height))

        self._scrollwidget = ba.scrollwidget(parent=self.root_widget,
                                             size=(self._scroll_width,
                                                   self._scroll_height),
                                             color=(0.55, 0.55, 0.55),
                                             highlight=False,
                                             position=self._scroll_position)
        ba.containerwidget(edit=self._scrollwidget, claims_left_right=True)

        self._sub_width = self._scroll_width * 0.95
        self._sub_height = 5 + rows * (button_height +
                                       2 * button_buffer_v) + 100
        self._subcontainer = ba.containerwidget(parent=self._scrollwidget,
                                                size=(self._sub_width,
                                                      self._sub_height),
                                                background=False)
        index = 0

        for y in range(rows):
            for x in range(columns):
                pos = (x * (button_width + 2 * button_buffer_h) +
                       button_buffer_h, self._sub_height - (y + 1) *
                       (button_height + 2 * button_buffer_v) + 12)
                btn = ba.buttonwidget(
                    parent=self._subcontainer,
                    button_type='square',
                    size=(button_width, button_height),
                    autoselect=True,
                    texture=ba.gettexture('null'),
                    model_transparent=ba.getmodel('buttonNull'),
                    label='',
                    color=cfg['CGS'][colorcfg],
                    on_activate_call=ba.Call(self._select_image,
                                             images[index]),
                    position=pos)
                ba.imagewidget(
                    parent=self._subcontainer,
                    position=pos,
                    draw_controller=btn,
                    size=(button_width, button_height),
                    texture=ba.gettexture(images[index]))
                ba.widget(edit=btn, show_buffer_top=60, show_buffer_bottom=60)
                if images[index] == selected_image:
                    ba.containerwidget(edit=self._subcontainer,
                                       selected_child=btn,
                                       visible_child=btn)
                index += 1

                if index >= count:
                    break
            if index >= count:
                break

    def _select_image(self, image: str) -> None:
        if self._delegate is not None:
            if self.colorcfg == 'image_color':
                self._delegate.on_image_picker_pick(image)
            elif self.colorcfg == 'game_iconcolor':
                self._delegate.on_icon_picker_pick(image)
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            ba.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        ba.playsound(ba.getsound('swish'))
        self._transition_out()

class OptionsWindow(ba.Window):

    class TabID(Enum):
        """Our available tab types."""
        BUTTON = 'button'
        WINDOW = 'window'
        GAME = 'game'

    def __init__(self,
                 transition: str = 'in_right',
                 origin_widget: ba.Widget = None):
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-locals
        from bastd.ui.tabs import TabRow
        scale_origin: Optional[Tuple[float, float]]
        if origin_widget is not None:
            self._transition_out = 'out_scale'
            scale_origin = origin_widget.get_screen_space_center()
            transition = 'in_scale'
        else:
            self._transition_out = 'in_right'
            scale_origin = None

        self._width = 800
        self._height = 540
        self.star_tex = ba.gettexture(cfg['CGS']['game_icon'])
        self.lsbt = ba.getmodel('level_select_button_transparent')
        self.lsbo = ba.getmodel('level_select_button_opaque')
        self._current_tab: Optional[OptionsPopup.TabID] = None
        self._ct_field: Optional[ba.Widget] = None
        app = ba.app
        uiscale = ba.app.ui.uiscale

        super().__init__(root_widget=ba.containerwidget(
            size=(self._width, self._height),
            transition=transition,
            toolbar_visibility='menu_minimal',
            scale=(1.4 if uiscale is ba.UIScale.SMALL else
                   0.97 if uiscale is ba.UIScale.MEDIUM else 0.8),
            scale_origin_stack_offset=scale_origin,
            stack_offset=(0, -11) if uiscale is ba.UIScale.SMALL else (
                0, 0) if uiscale is ba.UIScale.MEDIUM else (0, 0)))

        back_size = 55
        self._back_button = btn = ba.buttonwidget(
            parent=self._root_widget,
            position=(60, self._height - 82),
            size=(back_size, back_size),
            scale=1.1,
            autoselect=True,
            label=ba.charstr(ba.SpecialChar.BACK),
            button_type='backSmall',
            on_activate_call=self._back)
        ba.containerwidget(edit=self._root_widget, cancel_button=btn)

        condensed = uiscale is not ba.UIScale.LARGE
        txt = ba.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 53),
            size=(0, 0),
            scale=1.4,
            text=ba.Lstr(resource='settingsWindow.titleText'),
            h_align='center',
            color=app.ui.title_color,
            maxwidth=130,
            v_align='center')

        tabs_def = [
            (self.TabID.BUTTON, mmbutton),
            (self.TabID.WINDOW, mmwindow),
            (self.TabID.GAME, mmgame),
        ]

        self._tab_row = TabRow(self._root_widget,
                               tabs_def,
                               pos=(self._width * 0.1, self._height - 135),
                               size=(self._width * 0.8, 50),
                               on_select_call=self._set_tab)

        self._scroll_width = self._width - 150
        self._scroll_height = self._height - 186

        # Not actually using a scroll widget anymore; just an image.
        scroll_left = (self._width - self._scroll_width) * 0.5
        scroll_bottom = self._height - self._scroll_height - 128
        ba.imagewidget(parent=self._root_widget,
                       position=(scroll_left,
                                 scroll_bottom),
                       size=(self._scroll_width,
                             self._scroll_height),
                       texture=ba.gettexture('scrollWidget'),
                       model_transparent=ba.getmodel('softEdgeOutside'))
        self._tab_container: Optional[ba.Widget] = None

        self._restore_state()

    def _set_tab(self, tab_id: TabID) -> None:
        if self._current_tab is tab_id:
            return
        self._current_tab = tab_id

        # We wanna preserve our current tab between runs.
        cfg = ba.app.config
        cfg['Custom Game Tab'] = tab_id.value
        cfg.commit()

        # Update tab colors based on which is selected.
        self._tab_row.update_appearance(tab_id)

        # (Re)create scroll widget.
        if self._tab_container:
            self._tab_container.delete()

        self._tab_container = ba.containerwidget(
            parent=self._root_widget,
            size=(self._scroll_width,
                  self._scroll_height),
            background=False)

        if tab_id is self.TabID.BUTTON:
            self._example_button = ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.18 - 8,
                          self._scroll_height * 0.4 + 30),
                size=(230, 200),
                color=cfg['CGS']['button_color'],
                texture=ba.gettexture('buttonSquare'))
            self._example_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.35 - 8,
                          self._scroll_height * 0.55 + 30),
                size=(0, 0),
                scale=1.7,
                color=cfg['CGS']['name_color'],
                maxwidth=155,
                h_align='center',
                v_align='center',
                text=cfg['CGS']['button_name'])
            self._example_image = ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width*0.267-8+(cfg['CGS']['image_h']),
                          self._scroll_height*0.58+30+(cfg['CGS']['image_v'])),
                size=(118+(cfg['CGS']['image_scale']),
                      118+(cfg['CGS']['image_scale'])),
                color=cfg['CGS']['image_color'],
                texture=ba.gettexture(cfg['CGS']['image_button']))

            self._ct_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.55,
                          self._scroll_height * 1),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                draw_controller=self._example_button,
                maxwidth=180,
                h_align='left',
                v_align='center',
                text=mmbnombre)
            self._ct_field = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.735,
                          self._scroll_height * 0.905),
                size=(210, 60),
                autoselect=True,
                h_align='left',
                v_align='center',
                text=cfg['CGS']['button_name'],
                editable=True,
                padding=4,
                max_chars=16,
                color=cfg['CGS']['name_color'])

            self._ctc_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.63,
                          self._scroll_height * 0.55),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmbtext)
            self._ctc_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.56,
                          self._scroll_height * 0.6),
                size=(90, 90),
                label='',
                color=cfg['CGS']['name_color'],
                button_type='square')
            origint = self._ctc_button.get_screen_space_center()
            ba.buttonwidget(edit=self._ctc_button,
                            on_activate_call=ba.WeakCall(self._make_picker,
                                                         'tcolor', origint))

            self._cit_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.805,
                          self._scroll_height * 0.55),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmbtexture)
            self._cic_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.735,
                          self._scroll_height * 0.6),
                size=(90, 90),
                label='',
                color=cfg['CGS']['image_color'],
                button_type='square')
            torigin = self._cic_button.get_screen_space_center()
            ba.buttonwidget(edit=self._cic_button,
                            on_activate_call=ba.WeakCall(self._make_picker,
                                                         'txcolor', torigin))

            self._cbc_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.98,
                          self._scroll_height * 0.55),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmbbutton)
            self._cbc_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.91,
                          self._scroll_height * 0.6),
                size=(90, 90),
                label='',
                color=cfg['CGS']['button_color'],
                button_type='square')
            origin = self._cbc_button.get_screen_space_center()
            ba.buttonwidget(edit=self._cbc_button,
                            on_activate_call=ba.WeakCall(self._make_picker,
                                                         'bcolor', origin))

            self._image_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.192,
                          self._scroll_height * 0.27),
                size=(120, 60),
                label=mmbimage,
                color=(0.2, 0.6, 0.8),
                button_type='regular',
                on_activate_call=self._new_image)

            self._image_settings_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.405,
                          self._scroll_height * 0.275),
                size=(55, 55),
                label='',
                color=(0.2, 0.6, 0.8),
                button_type='square',
                on_activate_call=self._image_settings)
            ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.41,
                          self._scroll_height * 0.285),
                size=(50, 50),
                draw_controller=self._image_settings_button,
                texture=ba.gettexture('settingsIcon'))

            self._save_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.65,
                          self._scroll_height * 0.27),
                size=(195, 60),
                label=mmbsavename,
                color=(0.2, 0.9, 0.4),
                button_type='regular',
                on_activate_call=self._save_name)

            ba.Timer(0.2,
                     ba.WeakCall(self._update_image),
                     repeat=True,
                     timetype=ba.TimeType.REAL)

        elif tab_id is self.TabID.WINDOW:
            self._window_image = ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width*0.12,
                          self._scroll_height*0.01),
                size=(420, 420),
                color=cfg['CGS']['window_color'],
                texture=ba.gettexture('windowHSmallVSmall'))
            self._options_button = ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width*0.53,
                          self._scroll_height*0.81),
                size=(68, 68),
                color=cfg['CGS']['settings_color'],
                texture=ba.gettexture('buttonSquare'))
            self._options_image = ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width*0.535,
                          self._scroll_height*0.822),
                size=(60, 60),
                color=cfg['CGS']['settings_texcolor'],
                texture=ba.gettexture('settingsIcon'))
            self._window_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.42,
                          self._scroll_height * 0.91),
                size=(0, 0),
                scale=1.3,
                color=cfg['CGS']['window_titlecolor'],
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmwtitle)
            ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width*0.22,
                          self._scroll_height*0.41),
                size=(260, 130),
                texture=ba.gettexture('scrollWidget'))

            self._cct_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.805,
                          self._scroll_height * 0.75),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmwtitlecolor)
            self._cct_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.735,
                          self._scroll_height * 0.8),
                size=(90, 90),
                label='',
                color=cfg['CGS']['window_titlecolor'],
                button_type='square')
            oritt = self._cct_button.get_screen_space_center()
            ba.buttonwidget(edit=self._cct_button,
                            on_activate_call=ba.WeakCall(self._make_picker,
                                                         'twcolor', oritt))

            self._ccw_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.98,
                          self._scroll_height * 0.75),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmwwindow)
            self._ccw_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.91,
                          self._scroll_height * 0.8),
                size=(90, 90),
                label='',
                color=cfg['CGS']['window_color'],
                button_type='square')
            originw = self._ccw_button.get_screen_space_center()
            ba.buttonwidget(edit=self._ccw_button,
                            on_activate_call=ba.WeakCall(self._make_picker,
                                                         'wcolor', originw))

            ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.805,
                          self._scroll_height * 0.31),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmwicon)
            self._ccst_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.735,
                          self._scroll_height * 0.36),
                size=(90, 90),
                label='',
                color=cfg['CGS']['settings_texcolor'],
                button_type='square')
            orist = self._ccst_button.get_screen_space_center()
            ba.buttonwidget(edit=self._ccst_button,
                            on_activate_call=ba.WeakCall(self._make_picker,
                                                         'wstolor', orist))

            ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.98,
                          self._scroll_height * 0.31),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmbbutton)
            self._ccsb_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.91,
                          self._scroll_height * 0.36),
                size=(90, 90),
                label='',
                color=cfg['CGS']['settings_color'],
                button_type='square')
            orisb = self._ccsb_button.get_screen_space_center()
            ba.buttonwidget(edit=self._ccsb_button,
                            on_activate_call=ba.WeakCall(self._make_picker,
                                                         'wsbcolor', orisb))

        elif tab_id is self.TabID.GAME:
            self._game_button = ba.buttonwidget(
                parent=self._tab_container,
                position=(self._scroll_width*0.2,
                          self._scroll_height*0.31),
                size=(250, 250),
                label='',
                selectable=False,
                button_type='square',
                color=cfg['CGS']['game_color'])

            self._cgtc_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.382,
                          self._scroll_height * 0.9),
                size=(0, 0),
                scale=1.0,
                color=cfg['CGS']['game_textcolor'],
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmwtitle)

            self._game_image = ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width*0.27,
                          self._scroll_height*0.634),
                size=(150, 75),
                texture=ba.gettexture('rampagePreview'),
                model_transparent=self.lsbt,
                model_opaque=self.lsbo,
                mask_texture=ba.gettexture('mapPreviewMask'))

            spacesh = 56
            self._star_one = ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width*0.256+spacesh*0,
                          self._scroll_height*0.441),
                size=(56, 56),
                color=cfg['CGS']['game_iconcolor'],
                texture=self.star_tex)

            self._star_two = ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width*0.256+spacesh*1,
                          self._scroll_height*0.441),
                size=(56, 56),
                color=cfg['CGS']['game_iconcolor'],
                texture=self.star_tex)

            self._star_three = ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width*0.256+spacesh*2,
                          self._scroll_height*0.441),
                size=(56, 56),
                color=cfg['CGS']['game_iconcolor'],
                texture=self.star_tex)

            ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.725,
                          self._scroll_height * 0.75),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmwtitlecolor)
            self._cgtc_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.655,
                          self._scroll_height * 0.8),
                size=(90, 90),
                label='',
                color=cfg['CGS']['game_textcolor'],
                button_type='square')
            origingt = self._cgtc_button.get_screen_space_center()
            ba.buttonwidget(edit=self._cgtc_button,
                            on_activate_call=ba.WeakCall(self._make_picker,
                                                         'gtcolor', origingt))

            self._cgc_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.93,
                          self._scroll_height * 0.75),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmbbutton)
            self._cgc_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.86,
                          self._scroll_height * 0.8),
                size=(90, 90),
                label='',
                color=cfg['CGS']['game_color'],
                button_type='square')
            origing = self._cgc_button.get_screen_space_center()
            ba.buttonwidget(edit=self._cgc_button,
                            on_activate_call=ba.WeakCall(self._make_picker,
                                                         'gcolor', origing))

            self._ctex_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.725,
                          self._scroll_height * 0.31),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmwicon)
            self._ctex_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.655,
                          self._scroll_height * 0.36),
                size=(90, 90),
                label='',
                texture=ba.gettexture('null'),
                model_transparent=ba.getmodel('buttonNull'),
                button_type='square',
                on_activate_call=self._new_gameicon)
            self._ctex_icon = ba.imagewidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.655,
                          self._scroll_height * 0.36),
                size=(90, 90),
                draw_controller=self._ctex_button,
                color=cfg['CGS']['game_iconcolor'],
                texture=self.star_tex)

            self._cgtex_text = ba.textwidget(
                parent=self._tab_container,
                position=(self._scroll_width * 0.93,
                          self._scroll_height * 0.31),
                size=(0, 0),
                scale=1.0,
                color=ba.app.ui.heading_color,
                maxwidth=180,
                h_align='center',
                v_align='center',
                text=mmbtexture)
            self._cgtex_button = ba.buttonwidget(
                parent=self._tab_container,
                autoselect=True,
                position=(self._scroll_width * 0.86,
                          self._scroll_height * 0.36),
                size=(90, 90),
                label='',
                color=cfg['CGS']['game_iconcolor'],
                button_type='square')
            oritex = self._cgtex_button.get_screen_space_center()
            ba.buttonwidget(edit=self._cgtex_button,
                            on_activate_call=ba.WeakCall(self._make_picker,
                                                         'texcolor', oritex))


    def _make_picker(self, picker_type: str, origin: Tuple[float,
                                                           float]) -> None:
        from bastd.ui import colorpicker
        if picker_type == 'bcolor':
            initial_color = cfg['CGS']['button_color']
        elif picker_type == 'tcolor':
            initial_color = cfg['CGS']['name_color']
        elif picker_type == 'txcolor':
            initial_color = cfg['CGS']['image_color']
        elif picker_type == 'wcolor':
            initial_color = cfg['CGS']['window_color']
        elif picker_type == 'twcolor':
            initial_color = cfg['CGS']['window_titlecolor']
        elif picker_type == 'wstolor':
            initial_color = cfg['CGS']['settings_texcolor']
        elif picker_type == 'wsbcolor':
            initial_color = cfg['CGS']['settings_color']
        elif picker_type == 'gtcolor':
            initial_color = cfg['CGS']['game_textcolor']
        elif picker_type == 'gcolor':
            initial_color = cfg['CGS']['game_color']
        elif picker_type == 'texcolor':
            initial_color = cfg['CGS']['game_iconcolor']
        else:
            raise ValueError('invalid picker_type: ' + picker_type)
        colorpicker.ColorPicker(
            parent=self._root_widget,
            position=origin,
            initial_color=initial_color,
            delegate=self,
            tag=picker_type)

    def _set_button_color(self, color: Tuple[float, float, float]) -> None:
        cfg['CGS']['button_color'] = color
        if self._cbc_button:
            ba.buttonwidget(edit=self._cbc_button, color=color)
        if self._example_button:
            ba.imagewidget(edit=self._example_button, color=color)

    def _set_image_color(self, color: Tuple[float, float, float]) -> None:
        cfg['CGS']['image_color'] = color
        if self._cic_button:
            ba.buttonwidget(edit=self._cic_button, color=color)
        if self._example_image:
            ba.imagewidget(edit=self._example_image, color=color)

    def _set_name_color(self, color: Tuple[float, float, float]) -> None:
        cfg['CGS']['name_color'] = color
        if self._ctc_button:
            ba.buttonwidget(edit=self._ctc_button, color=color)
        if self._example_text:
            ba.textwidget(edit=self._example_text, color=color)
        if self._ct_field:
            ba.textwidget(edit=self._ct_field, color=color)

    def _set_window_color(self, color: Tuple[float, float, float]) -> None:
        cfg['CGS']['window_color'] = color
        if self._ccw_button:
            ba.buttonwidget(edit=self._ccw_button, color=color)
        if self._window_image:
            ba.imagewidget(edit=self._window_image, color=color)

    def _set_wtitle_color(self, color: Tuple[float, float, float]) -> None:
        cfg['CGS']['window_titlecolor'] = color
        if self._cct_button:
            ba.buttonwidget(edit=self._cct_button, color=color)
        if self._window_text:
            ba.textwidget(edit=self._window_text, color=color)

    def _set_wst_color(self, color: Tuple[float, float, float]) -> None:
        cfg['CGS']['settings_texcolor'] = color
        if self._ccst_button:
            ba.buttonwidget(edit=self._ccst_button, color=color)
        if self._options_image:
            ba.imagewidget(edit=self._options_image, color=color)

    def _set_wsb_color(self, color: Tuple[float, float, float]) -> None:
        cfg['CGS']['settings_color'] = color
        if self._ccsb_button:
            ba.buttonwidget(edit=self._ccsb_button, color=color)
        if self._options_button:
            ba.imagewidget(edit=self._options_button, color=color)

    def _set_gametex_color(self, color: Tuple[float, float, float]) -> None:
        cfg['CGS']['game_textcolor'] = color
        if self._cgtc_button:
            ba.buttonwidget(edit=self._cgtc_button, color=color)
        if self._cgtc_text:
            ba.textwidget(edit=self._cgtc_text, color=color)

    def _set_game_color(self, color: Tuple[float, float, float]) -> None:
        cfg['CGS']['game_color'] = color
        if self._cgc_button:
            ba.buttonwidget(edit=self._cgc_button, color=color)
        if self._game_button:
            ba.buttonwidget(edit=self._game_button, color=color)

    def _set_icon_color(self, color: Tuple[float, float, float]) -> None:
        cfg['CGS']['game_iconcolor'] = color
        if self._ctex_icon:
            ba.imagewidget(edit=self._ctex_icon, color=color)
        if self._star_one:
            ba.imagewidget(
                edit=self._star_one, color=color)
        if self._star_two:
            ba.imagewidget(
                edit=self._star_two, color=color)
        if self._star_three:
            ba.imagewidget(
                edit=self._star_three, color=color)
        if self._cgtex_button:
            ba.buttonwidget(
                edit=self._cgtex_button, color=color)

    def color_picker_closing(self, picker: ColorPicker) -> None:
        """Called when a color picker is closing."""
        if not self._root_widget:
            return
        tag = picker.get_tag()
        if tag == 'bcolor':
            ba.containerwidget(edit=self._root_widget,
                               selected_child=self._cbc_button)
        elif tag == 'tcolor':
            ba.containerwidget(edit=self._root_widget,
                               selected_child=self._ctc_button)
        elif tag == 'txcolor':
            ba.containerwidget(edit=self._root_widget,
                               selected_child=self._cic_button)
        elif tag == 'wcolor':
            ba.containerwidget(edit=self._root_widget,
                               selected_child=self._ccw_button)
        elif tag == 'twcolor':
            ba.containerwidget(edit=self._root_widget,
                               selected_child=self._cct_button)
        elif tag == 'wstolor':
            ba.containerwidget(edit=self._root_widget,
                               selected_child=self._ccst_button)
        elif tag == 'wsbcolor':
            ba.containerwidget(edit=self._root_widget,
                               selected_child=self._ccsb_button)
        elif tag == 'gtcolor':
            ba.containerwidget(edit=self._root_widget,
                               selected_child=self._cgtc_button)
        elif tag == 'gcolor':
            ba.containerwidget(edit=self._root_widget,
                               selected_child=self._cgc_button)
        elif tag == 'texcolor':
            ba.containerwidget(edit=self._root_widget,
                               selected_child=self._cgtex_button)
        else:
            print('color_picker_closing got unknown tag ' + str(tag))

    def color_picker_selected_color(self, picker: ColorPicker,
                                    color: Tuple[float, float, float]) -> None:
        """Called when a color is selected in a color picker."""
        if not self._root_widget:
            return
        tag = picker.get_tag()
        if tag == 'bcolor':
            cfg['CGS']['button_color'] = color
            cfg.apply_and_commit()
            self._set_button_color(color)
        elif tag == 'tcolor':
            cfg['CGS']['name_color'] = color
            cfg.apply_and_commit()
            self._set_name_color(color)
        elif tag == 'txcolor':
            cfg['CGS']['image_color'] = color
            cfg.apply_and_commit()
            self._set_image_color(color)
        elif tag == 'wcolor':
            cfg['CGS']['window_color'] = color
            cfg.apply_and_commit()
            self._set_window_color(color)
        elif tag == 'twcolor':
            cfg['CGS']['window_titlecolor'] = color
            cfg.apply_and_commit()
            self._set_wtitle_color(color)
        elif tag == 'wstolor':
            cfg['CGS']['settings_texcolor'] = color
            cfg.apply_and_commit()
            self._set_wst_color(color)
        elif tag == 'wsbcolor':
            cfg['CGS']['settings_color'] = color
            cfg.apply_and_commit()
            self._set_wsb_color(color)
        elif tag == 'gtcolor':
            cfg['CGS']['game_textcolor'] = color
            cfg.apply_and_commit()
            self._set_gametex_color(color)
        elif tag == 'gcolor':
            cfg['CGS']['game_color'] = color
            cfg.apply_and_commit()
            self._set_game_color(color)
        elif tag == 'texcolor':
            cfg['CGS']['game_iconcolor'] = color
            cfg.apply_and_commit()
            self._set_icon_color(color)
        else:
            print('color_picker_selected_color got unknown tag ' + str(tag))

    def _new_image(self) -> None:
        ImagePicker(
            parent=self._root_widget,
            selected_image=cfg['CGS']['image_button'],
            colorcfg='image_color',
            delegate=self)

    def _image_settings(self) -> None:
        PosImage(
            parent=self._root_widget,
            position=(100, 0))

    def on_image_picker_pick(self, image: str) -> None:
        """A character has been selected by the picker."""
        if not self._root_widget:
            return

        cfg['CGS']['image_button'] = image
        cfg.apply_and_commit()
        ba.imagewidget(
            edit=self._example_image,
            texture=ba.gettexture(cfg['CGS']['image_button']))

    def on_icon_picker_pick(self, image: str) -> None:
        """A character has been selected by the picker."""
        if not self._root_widget:
            return

        cfg['CGS']['game_icon'] = image
        cfg.apply_and_commit()
        ba.imagewidget(
            edit=self._ctex_icon,
            texture=ba.gettexture(cfg['CGS']['game_icon']))
        ba.imagewidget(
            edit=self._star_one,
            texture=ba.gettexture(cfg['CGS']['game_icon']))
        ba.imagewidget(
            edit=self._star_two,
            texture=ba.gettexture(cfg['CGS']['game_icon']))
        ba.imagewidget(
            edit=self._star_three,
            texture=ba.gettexture(cfg['CGS']['game_icon']))

    def _update_image(self) -> None:
        if not self._example_image:
            return
        ba.imagewidget(
            edit=self._example_image,
            position=(self._scroll_width*0.267-8+(cfg['CGS']['image_h']),
                      self._scroll_height*0.58+30+(cfg['CGS']['image_v'])),
            size=(118+(cfg['CGS']['image_scale']),
                  118+(cfg['CGS']['image_scale'])))

    def _save_name(self) -> None:
        new_name = cast(str, ba.textwidget(query=self._ct_field))
        cfg['CGS']['button_name'] = new_name
        cfg.apply_and_commit()
        ba.textwidget(
            edit=self._example_text,
            text=cfg['CGS']['button_name'])

    def _new_gameicon(self) -> None:
        ImagePicker(
            parent=self._root_widget,
            selected_image=cfg['CGS']['game_icon'],
            colorcfg='game_iconcolor',
            delegate=self)

    def _save_state(self) -> None:
        try:
            sel = self._root_widget.get_selected_child()
            selected_tab_ids = [
                tab_id for tab_id, tab in self._tab_row.tabs.items()
                if sel == tab.button
            ]
            if sel == self._tab_container:
                sel_name = 'Tab'
            elif sel == self._back_button:
                sel_name = 'Back'
            elif selected_tab_ids:
                assert len(selected_tab_ids) == 1
                sel_name = f'Tab:{selected_tab_ids[0].value}'
            else:
                raise ValueError(f'unrecognized selection \'{sel}\'')
            ba.app.ui.window_states[type(self)] = {
                'sel_name': sel_name,
            }
        except Exception:
            ba.print_exception(f'Error saving state for {self}.')

    def _restore_state(self) -> None:
        from efro.util import enum_by_value
        try:
            sel: Optional[ba.Widget]
            sel_name = ba.app.ui.window_states.get(type(self),
                                                   {}).get('sel_name')
            assert isinstance(sel_name, (str, type(None)))

            try:
                current_tab = enum_by_value(self.TabID,
                                            ba.app.config.get(
                                                'Custom Game Tab'))
            except ValueError:
                current_tab = self.TabID.BUTTON

            if sel_name == 'Back':
                sel = self._back_button
            elif sel_name == 'Tab':
                sel = self._tab_container
            elif isinstance(sel_name, str) and sel_name.startswith('Tab:'):
                try:
                    sel_tab_id = enum_by_value(self.TabID,
                                               sel_name.split(':')[-1])
                except ValueError:
                    sel_tab_id = self.TabID.CHARACTERS
                sel = self._tab_row.tabs[sel_tab_id].button
            else:
                sel = self._tab_row.tabs[current_tab].button

            self._set_tab(current_tab)
            if sel is not None:
                ba.containerwidget(edit=self._root_widget, selected_child=sel)
        except Exception:
            ba.print_exception(f'Error restoring state for {self}.')

    def _back(self) -> None:
        self._save_state()
        ba.containerwidget(edit=self._root_widget,
                           transition='out_left')
        ba.app.ui.set_main_menu_window(
            PlayModsWindow(transition='in_left').get_root_widget())

def _get_modules_with_call(call_name):
    app = _ba.app
    pythondirs = [app.python_directory_app, app.python_directory_user]
    d = app.python_directory_user
    if os.path.isdir(d):
        try:
            dirlist = os.listdir(d)
        except Exception:
            print_exception('error listing dir during'
                            ' _get_modules_with_call(): \'' + d + '\''
            )
            dirlist = []
        else:
            dirlist = []
    for name in dirlist:
        package_dir = d + '/' + name
        if os.path.isdir(package_dir) and name != 'sys':
            pythondirs.append(package_dir + '/python')
    names_imported = set()
    modules = []
    for i, d in enumerate(pythondirs):
        if os.path.isdir(d):
            try:
                dirlist = os.listdir(d)
            except Exception as e:
                import errno
                if (type(e) == OSError
                        and e.errno in (errno.EACCES, errno.ENOENT)):
                    pass
                else:
                    print_exception('error listing dir during '
                                    '_get_modules_with_call(): \'' + d + '\'')
                dirlist = []
        else:
            dirlist = []
        for name in dirlist:
            try:
                module_name = name.replace('.py', '')
                if name.endswith('.py'):
                    if name in names_imported:
                        errmsg = ("Warning: duplicate mod script "
                                  "found: '" + name + "'; ignoring.")
                        print(errmsg)
                        ba.screenmessage(errmsg, color=(1, 0, 0))
                    else:
                        names_imported.add(name)
                        module = __import__(module_name)
                        call = getattr(module, call_name, None)
                        if call is not None and callable(call):
                            ourapiversion = 6
                            try:
                                moduleapiversion = module.ba_get_api_version()
                            except Exception:
                                moduleapiversion = None
                            if moduleapiversion == ourapiversion:
                                modules.append(module)
            except Exception:
                print_exception('Error importing game module \'' + name +
                                '\'')
    return modules

def new_campaigns():
    """New Campaigns."""
    # pylint: disable=too-many-statements
    # pylint: disable=cyclic-import
    import os
    import _ba
    import pathlib
    from ba import _level
    from ba._general import getclass
    from ba._gameactivity import GameActivity
    from ba._meta import DirectoryScan

    # User is the 'wild west' where custom mods and whatnot live
    campaign = Campaign('User', sequential=False)
    # add any levels from other user-space modules..
    all_levels = []
    modules = _get_modules_with_call(
        'ba_get_levels')
    for module in modules:
        try:
            all_levels += module.ba_get_levels()
        except Exception:
            print_exception("error fetching levels from module "+str(module))
        for level in all_levels:
            try:
                campaign.addlevel(level)
            except Exception:
                print_exception("error adding level '"+str(level)+"'")
    register_campaign(campaign)


# ba_meta export plugin
class MinigamesPlugin(ba.Plugin):

    #######################
    version = 1.0
    creator = "byANG3L"
    logo = 'heart'
    logo_color = (1,0,0)
    settings = True

    def openWindow(self) -> None:
        PlayModsWindow()
    #######################

    def on_app_launch(self) -> None:
        if 'CGS' in ba.app.config:
            old_config = ba.app.config['CGS']
            for setting in cgsc:
                if setting not in old_config:
                    ba.app.config['CGS'].update({setting:cgsc[setting]})

            remove_list = []
            for setting in old_config:
                if setting not in cgsc:
                    remove_list.append(setting)
            for element in remove_list:
                ba.app.config['CGS'].pop(element)
        else:
            ba.app.config['CGS'] = cgsc
        ba.app.config.apply_and_commit()
        new_campaigns()

    MMA.old_on_transition_in = MMA.on_transition_in
    def on_transition_in(self) -> None:
        self.old_on_transition_in()
        # Bring up the last place we were, or start at the main menu otherwise.
        with ba.Context('ui'):
            from bastd.ui import specialoffer
            if bool(False):
                uicontroller = ba.app.ui.controller
                assert uicontroller is not None
                uicontroller.show_main_menu()
            else:
                main_menu_location = ba.app.ui.get_main_menu_location()

                # When coming back from a kiosk-mode game, jump to
                # the kiosk start screen.
                if ba.app.demo_mode or ba.app.arcade_mode:
                    # pylint: disable=cyclic-import
                    from bastd.ui.kiosk import KioskWindow
                    ba.app.ui.set_main_menu_window(
                        KioskWindow().get_root_widget())
                # ..or in normal cases go back to the main menu
                else:
                    if main_menu_location == 'Gather':
                        # pylint: disable=cyclic-import
                        from bastd.ui.gather import GatherWindow
                        ba.app.ui.set_main_menu_window(
                            GatherWindow(transition=None).get_root_widget())
                    elif main_menu_location == 'Watch':
                        # pylint: disable=cyclic-import
                        from bastd.ui.watch import WatchWindow
                        ba.app.ui.set_main_menu_window(
                            WatchWindow(transition=None).get_root_widget())
                    elif main_menu_location == 'Team Game Select':
                        # pylint: disable=cyclic-import
                        from bastd.ui.playlist.browser import (
                            PlaylistBrowserWindow)
                        ba.app.ui.set_main_menu_window(
                            PlaylistBrowserWindow(
                                sessiontype=ba.DualTeamSession,
                                transition=None).get_root_widget())
                    elif main_menu_location == 'Free-for-All Game Select':
                        # pylint: disable=cyclic-import
                        from bastd.ui.playlist.browser import (
                            PlaylistBrowserWindow)
                        ba.app.ui.set_main_menu_window(
                            PlaylistBrowserWindow(
                                sessiontype=ba.FreeForAllSession,
                                transition=None).get_root_widget())
                    elif main_menu_location == 'Coop Select':
                        # pylint: disable=cyclic-import
                        from bastd.ui.coop.browser import CoopBrowserWindow
                        ba.app.ui.set_main_menu_window(
                            CoopBrowserWindow(
                                transition=None).get_root_widget())
                    elif main_menu_location == 'Custom Games':
                        ba.app.ui.set_main_menu_window(
                            PlayModsWindow(
                                transition=None).get_root_widget())
                    else:
                        # pylint: disable=cyclic-import
                        from bastd.ui.mainmenu import MainMenuWindow
                        ba.app.ui.set_main_menu_window(
                            MainMenuWindow(transition=None).get_root_widget())

                # attempt to show any pending offers immediately.
                # If that doesn't work, try again in a few seconds
                # (we may not have heard back from the server)
                # ..if that doesn't work they'll just have to wait
                # until the next opportunity.
                if not specialoffer.show_offer():

                    def try_again() -> None:
                        if not specialoffer.show_offer():
                            # Try one last time..
                            ba.timer(2.0,
                                     specialoffer.show_offer,
                                     timetype=ba.TimeType.REAL)

                    ba.timer(2.0, try_again, timetype=ba.TimeType.REAL)
    MMA.on_transition_in = on_transition_in

    MMW._old_fresh = MMW._refresh
    def _new_fresh(self) -> None:
        self._old_fresh()
        if not self._in_game:
            uiscale = ba.app.ui.uiscale
            extra_y = 101.5 if uiscale is ba.UIScale.SMALL else 0
            extra_text_y = -57.2 if uiscale is ba.UIScale.SMALL else -59
            extra_image_y = -97 if uiscale is ba.UIScale.SMALL else -55
            this_b_width = self._button_width * 0.25 * 1.7
            this_b_height = self._button_height * 0.82 * 1.7
            self._test_button = tb = ba.buttonwidget(
                parent=self._root_widget,
                position=(430, -77 + extra_y*0.55),
                size=(this_b_width, this_b_height),
                autoselect=self._use_autoselect,
                button_type='square',
                label='',
                color=cfg['CGS']['button_color'],
                transition_delay=self._tdelay,
                on_activate_call=ba.Call(new_window, self))
            ba.textwidget(parent=self._root_widget,
                          position=(470, extra_text_y + extra_y*0.55),
                          size=(0, 0),
                          scale=0.75,
                          transition_delay=self._tdelay,
                          draw_controller=tb,
                          color=cfg['CGS']['name_color'],
                          maxwidth=self._button_width * 0.33,
                          text=cfg['CGS']['button_name'],
                          h_align='center',
                          v_align='center')
            icon_size = (
                this_b_width * (0.6 if uiscale is ba.UIScale.SMALL else 0.6))
            ba.imagewidget(parent=self._root_widget,
                           size=(icon_size+(cfg['CGS']['image_scale'])*0.43,
                                 icon_size+(cfg['CGS']['image_scale'])*0.43),
                           draw_controller=tb,
                           color=cfg['CGS']['image_color'],
                           transition_delay=self._tdelay,
                           position=(445+(cfg['CGS']['image_h'])*0.43,
                                     extra_image_y+extra_y+(
                                        cfg['CGS']['image_v'])*0.43),
                           texture=ba.gettexture(cfg['CGS']['image_button']))
    MMW._refresh = _new_fresh
