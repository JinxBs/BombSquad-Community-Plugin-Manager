"""More Minigames."""
# Created by: byANG3L

# ba_meta require api 6
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import os
import _ba
import math
import random
from bastd.ui import popup
from ba._language import Lstr
from ba._error import print_exception
from bastd.ui.coop.gamebutton import GameButton
from ba._campaign import register_campaign, Campaign
from ba.internal import getcampaign
from bastd.ui.mainmenu import MainMenuWindow as MMW

if TYPE_CHECKING:
    from typing import Type, Any, Callable, Dict, Union, List, Tuple, Optional


# ======================= #

button_name = 'Mini Games'
button_color = (0.6, 0.0, 0.9)
image_button = 'heart'
image_color = (0.9, 0.2, 0.2)
window_color = (0.4, 0.0, 1.0)
game_color = (0.4, 0.9, 0.9)

# ======================= #


class GameButton(GameButton):
    def __init__(self, window: PlayModsWindow, parent: ba.Widget, game: str,
                 x: float, y: float, select: bool, row: str):
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-locals
        self._game = game
        sclx = 195.0
        scly = 195.0

        campaignname, levelname = game.split(':')

        # Hack: The Last Stand doesn't actually exist in the easy
        # tourney. We just want it for display purposes. Map it to
        # the hard-mode version.
        if game == 'Easy:The Last Stand':
            campaignname = 'Default'

        rating: Optional[float]
        campaign = getcampaign(campaignname)
        rating = campaign.getlevel(levelname).rating

        if game == 'Easy:The Last Stand':
            rating = None

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
            color=game_color,
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

    def _update(self) -> None:
        # pylint: disable=too-many-boolean-expressions
        from ba.internal import getcampaign

        # In case we stick around after our UI...
        if not self._button:
            return

        game = self._game
        campaignname, levelname = game.split(':')
        campaign = getcampaign(campaignname)


class PlayModsWindow(popup.PopupWindow):

    def __init__(self):
        app = ba.app
        self._transitioning_out = False
        self._width = 1120
        self._height = 800
        bg_color = window_color
        self.star_tex = ba.gettexture('star')
        self.lsbt = ba.getmodel('level_select_button_transparent')
        self.lsbo = ba.getmodel('level_select_button_opaque')
        self.a_outline_tex = ba.gettexture('achievementOutline')
        self.a_outline_model = ba.getmodel('achievementOutline')
        popup.PopupWindow.__init__(self,
                                   position=(0, 0, 0),
                                   size=(self._width, self._height),
                                   scale=0.75,
                                   bg_color=bg_color)

        self._cancel_button = ba.buttonwidget(
            parent=self.root_widget,
            position=(100, self._height - 73),
            size=(60, 60),
            scale=1.0,
            label='',
            color=bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=ba.gettexture('crossOut'),
            iconscale=1.2)

        txt = ba.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 50),
            size=(0, 0),
            text=ba.Lstr(resource='playModes.singlePlayerCoopText',
                         fallback_resource='playModes.coopText'),
            h_align='center',
            color=app.ui.title_color,
            scale=1.5,
            maxwidth=500,
            v_align='center')

        self._scroll_width = self._width - 150
        self._scroll_height = self._height - 160

        self._scrollwidget = ba.scrollwidget(
            parent=self.root_widget,
            highlight=False,
            position=(75, 70),
            size=(self._scroll_width, self._scroll_height),
            simple_culling_v=10.0,
            claims_left_right=True,
            claims_tab=True,
            selection_loops_to_parent=True)

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
        v = self._sub_height - 225
        index = 0
        for item in items:
            index += 1
            self._custom_buttons.append(
                GameButton(self, self._subcontainer, item, h, v, None, None))
            h += h_spacing
            if index == 4:
                h = h_origin
                v -= 195
                index = 0

    def run(self, game: Optional[str]) -> None:
        ba.app.launch_coop_game(game)

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            ba.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        ba.playsound(ba.getsound('swish'))
        self._transition_out()

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
    print('true')


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
        new_campaigns()

    MMW._old_ref = MMW._refresh
    def _new_fresh(self) -> None:
        self._old_ref()
        if not self._in_game:
            uiscale = ba.app.ui.uiscale
            extra_y = 100 if uiscale is ba.UIScale.SMALL else 0
            this_b_width = self._button_width * 0.25 * 1.7
            this_b_height = self._button_height * 0.82 * 1.7
            self._test_button = tb = ba.buttonwidget(
                parent=self._root_widget,
                position=(430, -77 + extra_y*0.55),
                size=(this_b_width, this_b_height),
                autoselect=self._use_autoselect,
                button_type='square',
                label='',
                color=button_color,
                transition_delay=self._tdelay,
                on_activate_call=ba.Call(PlayModsWindow))
            ba.textwidget(parent=self._root_widget,
                          position=(470, -59 + extra_y*0.55),
                          size=(0, 0),
                          scale=0.75,
                          transition_delay=self._tdelay,
                          draw_controller=tb,
                          color=(0.75, 1.0, 0.7),
                          maxwidth=self._button_width * 0.33,
                          text=button_name,
                          h_align='center',
                          v_align='center')
            icon_size = this_b_width * 0.6
            ba.imagewidget(parent=self._root_widget,
                           size=(icon_size, icon_size),
                           draw_controller=tb,
                           color=image_color,
                           transition_delay=self._tdelay,
                           position=(445, -53.5 + extra_y*0.55),
                           texture=ba.gettexture(image_button))
    MMW._refresh = _new_fresh