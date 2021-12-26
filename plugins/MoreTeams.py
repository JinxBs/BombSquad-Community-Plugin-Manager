# ba_meta require api 6
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations
from typing import TYPE_CHECKING, cast

import ba
import _ba
from bastd.ui import popup
from bastd.ui import playoptions
from bastd.ui import teamnamescolors

if TYPE_CHECKING:
    from typing import  Any, Optional, Union

### -------- T E A M S -------- ###

num_teams = 4

### -------- T E A M S -------- ###

class PlayOptionsWindow(playoptions.PlayOptionsWindow):
    """A popup window for configuring play options."""

    def __init__(self,
                 sessiontype: type[ba.Session],
                 playlist: str,
                 scale_origin: tuple[float, float],
                 delegate: Any = None):
        # FIXME: Tidy this up.
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-locals
        from ba.internal import get_map_class, getclass, filter_playlist
        from bastd.ui.playlist import PlaylistTypeVars

        self._r = 'gameListWindow'
        self._delegate = delegate
        self._pvars = PlaylistTypeVars(sessiontype)
        self._transitioning_out = False

        # We behave differently if we're being used for playlist selection
        # vs starting a game directly (should make this more elegant).
        self._selecting_mode = ba.app.ui.selecting_private_party_playlist

        self._do_randomize_val = (ba.app.config.get(
            self._pvars.config_name + ' Playlist Randomize', 0))

        self._sessiontype = sessiontype
        self._playlist = playlist

        self._width = 500.0
        self._height = 330.0 - 50.0

        # In teams games, show the custom names/colors button.
        if self._sessiontype is ba.DualTeamSession:
            self._height += 50.0

        self._row_height = 45.0

        # Grab our maps to display.
        model_opaque = ba.getmodel('level_select_button_opaque')
        model_transparent = ba.getmodel('level_select_button_transparent')
        mask_tex = ba.gettexture('mapPreviewMask')

        # Poke into this playlist and see if we can display some of its maps.
        map_textures = []
        map_texture_entries = []
        rows = 0
        columns = 0
        game_count = 0
        scl = 0.35
        c_width_total = 0.0
        try:
            max_columns = 5
            name = playlist
            if name == '__default__':
                plst = self._pvars.get_default_list_call()
            else:
                try:
                    plst = ba.app.config[self._pvars.config_name +
                                         ' Playlists'][name]
                except Exception:
                    print('ERROR INFO: self._config_name is:',
                          self._pvars.config_name)
                    print(
                        'ERROR INFO: playlist names are:',
                        list(ba.app.config[self._pvars.config_name +
                                           ' Playlists'].keys()))
                    raise
            plst = filter_playlist(plst,
                                   self._sessiontype,
                                   remove_unowned=False,
                                   mark_unowned=True)
            game_count = len(plst)
            for entry in plst:
                mapname = entry['settings']['map']
                maptype: Optional[type[ba.Map]]
                try:
                    maptype = get_map_class(mapname)
                except ba.NotFoundError:
                    maptype = None
                if maptype is not None:
                    tex_name = maptype.get_preview_texture_name()
                    if tex_name is not None:
                        map_textures.append(tex_name)
                        map_texture_entries.append(entry)
            rows = (max(0, len(map_textures) - 1) // max_columns) + 1
            columns = min(max_columns, len(map_textures))

            if len(map_textures) == 1:
                scl = 1.1
            elif len(map_textures) == 2:
                scl = 0.7
            elif len(map_textures) == 3:
                scl = 0.55
            else:
                scl = 0.35
            self._row_height = 128.0 * scl
            c_width_total = scl * 250.0 * columns
            if map_textures:
                self._height += self._row_height * rows

        except Exception:
            ba.print_exception('Error listing playlist maps.')

        show_shuffle_check_box = game_count > 1

        if show_shuffle_check_box:
            self._height += 40

        # Creates our _root_widget.
        uiscale = ba.app.ui.uiscale
        scale = (1.69 if uiscale is ba.UIScale.SMALL else
                 1.1 if uiscale is ba.UIScale.MEDIUM else 0.85)
        popup.PopupWindow.__init__(self, position=scale_origin,
                         size=(self._width, self._height),
                         scale=scale)

        playlist_name: Union[str, ba.Lstr] = (self._pvars.default_list_name
                                              if playlist == '__default__' else
                                              playlist)
        self._title_text = ba.textwidget(parent=self.root_widget,
                                         position=(self._width * 0.5,
                                                   self._height - 89 + 51),
                                         size=(0, 0),
                                         text=playlist_name,
                                         scale=1.4,
                                         color=(1, 1, 1),
                                         maxwidth=self._width * 0.7,
                                         h_align='center',
                                         v_align='center')

        self._cancel_button = ba.buttonwidget(
            parent=self.root_widget,
            position=(25, self._height - 53),
            size=(50, 50),
            scale=0.7,
            label='',
            color=(0.42, 0.73, 0.2),
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=ba.gettexture('crossOut'),
            iconscale=1.2)

        h_offs_img = self._width * 0.5 - c_width_total * 0.5
        v_offs_img = self._height - 118 - scl * 125.0 + 50
        bottom_row_buttons = []
        self._have_at_least_one_owned = False

        for row in range(rows):
            for col in range(columns):
                tex_index = row * columns + col
                if tex_index < len(map_textures):
                    tex_name = map_textures[tex_index]
                    h = h_offs_img + scl * 250 * col
                    v = v_offs_img - self._row_height * row
                    entry = map_texture_entries[tex_index]
                    owned = not (('is_unowned_map' in entry
                                  and entry['is_unowned_map']) or
                                 ('is_unowned_game' in entry
                                  and entry['is_unowned_game']))

                    if owned:
                        self._have_at_least_one_owned = True

                    try:
                        desc = getclass(entry['type'],
                                        subclassof=ba.GameActivity
                                        ).get_settings_display_string(entry)
                        if not owned:
                            desc = ba.Lstr(
                                value='${DESC}\n${UNLOCK}',
                                subs=[
                                    ('${DESC}', desc),
                                    ('${UNLOCK}',
                                     ba.Lstr(
                                         resource='unlockThisInTheStoreText'))
                                ])
                        desc_color = (0, 1, 0) if owned else (1, 0, 0)
                    except Exception:
                        desc = ba.Lstr(value='(invalid)')
                        desc_color = (1, 0, 0)

                    btn = ba.buttonwidget(
                        parent=self.root_widget,
                        size=(scl * 240.0, scl * 120.0),
                        position=(h, v),
                        texture=ba.gettexture(tex_name if owned else 'empty'),
                        model_opaque=model_opaque if owned else None,
                        on_activate_call=ba.Call(ba.screenmessage, desc,
                                                 desc_color),
                        label='',
                        color=(1, 1, 1),
                        autoselect=True,
                        extra_touch_border_scale=0.0,
                        model_transparent=model_transparent if owned else None,
                        mask_texture=mask_tex if owned else None)
                    if row == 0 and col == 0:
                        ba.widget(edit=self._cancel_button, down_widget=btn)
                    if row == rows - 1:
                        bottom_row_buttons.append(btn)
                    if not owned:

                        # Ewww; buttons don't currently have alpha so in this
                        # case we draw an image over our button with an empty
                        # texture on it.
                        ba.imagewidget(parent=self.root_widget,
                                       size=(scl * 260.0, scl * 130.0),
                                       position=(h - 10.0 * scl,
                                                 v - 4.0 * scl),
                                       draw_controller=btn,
                                       color=(1, 1, 1),
                                       texture=ba.gettexture(tex_name),
                                       model_opaque=model_opaque,
                                       opacity=0.25,
                                       model_transparent=model_transparent,
                                       mask_texture=mask_tex)

                        ba.imagewidget(parent=self.root_widget,
                                       size=(scl * 100, scl * 100),
                                       draw_controller=btn,
                                       position=(h + scl * 70, v + scl * 10),
                                       texture=ba.gettexture('lock'))

        # Team names/colors.
        self._custom_colors_names_button: Optional[ba.Widget]
        if self._sessiontype is ba.DualTeamSession:
            y_offs = 50 if show_shuffle_check_box else 0
            self._custom_colors_names_button = ba.buttonwidget(
                parent=self.root_widget,
                position=(100, 200 + y_offs),
                size=(290, 35),
                on_activate_call=ba.WeakCall(self._custom_colors_names_press),
                autoselect=True,
                textcolor=(0.8, 0.8, 0.8),
                label=ba.Lstr(resource='teamNamesColorText'))
        else:
            self._custom_colors_names_button = None

        # Shuffle.
        def _cb_callback(val: bool) -> None:
            self._do_randomize_val = val
            cfg = ba.app.config
            cfg[self._pvars.config_name +
                ' Playlist Randomize'] = self._do_randomize_val
            cfg.commit()

        if show_shuffle_check_box:
            self._shuffle_check_box = ba.checkboxwidget(
                parent=self.root_widget,
                position=(110, 200),
                scale=1.0,
                size=(250, 30),
                autoselect=True,
                text=ba.Lstr(resource=self._r + '.shuffleGameOrderText'),
                maxwidth=300,
                textcolor=(0.8, 0.8, 0.8),
                value=self._do_randomize_val,
                on_value_change_call=_cb_callback)

        # Show tutorial.
        show_tutorial = bool(ba.app.config.get('Show Tutorial', True))

        def _cb_callback_2(val: bool) -> None:
            cfg = ba.app.config
            cfg['Show Tutorial'] = val
            cfg.commit()

        self._show_tutorial_check_box = ba.checkboxwidget(
            parent=self.root_widget,
            position=(110, 151),
            scale=1.0,
            size=(250, 30),
            autoselect=True,
            text=ba.Lstr(resource=self._r + '.showTutorialText'),
            maxwidth=300,
            textcolor=(0.8, 0.8, 0.8),
            value=show_tutorial,
            on_value_change_call=_cb_callback_2)

        # Grumble: current autoselect doesn't do a very good job
        # with checkboxes.
        if self._custom_colors_names_button is not None:
            for btn in bottom_row_buttons:
                ba.widget(edit=btn,
                          down_widget=self._custom_colors_names_button)
            if show_shuffle_check_box:
                ba.widget(edit=self._custom_colors_names_button,
                          down_widget=self._shuffle_check_box)
                ba.widget(edit=self._shuffle_check_box,
                          up_widget=self._custom_colors_names_button)
            else:
                ba.widget(edit=self._custom_colors_names_button,
                          down_widget=self._show_tutorial_check_box)
                ba.widget(edit=self._show_tutorial_check_box,
                          up_widget=self._custom_colors_names_button)

        self._ok_button = ba.buttonwidget(
            parent=self.root_widget,
            position=(70, 44),
            size=(200, 45),
            scale=1.8,
            text_res_scale=1.5,
            on_activate_call=self._on_ok_press,
            autoselect=True,
            label=ba.Lstr(
                resource='okText' if self._selecting_mode else 'playText'))

        ba.widget(edit=self._ok_button,
                  up_widget=self._show_tutorial_check_box)

        ba.containerwidget(edit=self.root_widget,
                           start_button=self._ok_button,
                           cancel_button=self._cancel_button,
                           selected_child=self._ok_button)

        # Update now and once per second.
        self._update_timer = ba.Timer(1.0,
                                      ba.WeakCall(self._update),
                                      timetype=ba.TimeType.REAL,
                                      repeat=True)
        self._update()

    def _custom_colors_names_press(self) -> None:
        from bastd.ui.teamnamescolors import TeamNamesColorsWindow
        assert self._custom_colors_names_button
        TeamNamesColorsWindow(scale_origin=self._custom_colors_names_button.
                              get_screen_space_center())

class TeamNamesColorsWindow(teamnamescolors.TeamNamesColorsWindow):
    """A popup window for customizing team names and colors."""

    def __init__(self, scale_origin: tuple[float, float]):
        self._width = 500
        self._height = 330 + 70 * (num_teams-2)
        self._transitioning_out = False
        self._max_name_length = 16

        # Creates our _root_widget.
        uiscale = ba.app.ui.uiscale
        scale = (1.69 if uiscale is ba.UIScale.SMALL else
                 1.1 if uiscale is ba.UIScale.MEDIUM else 0.85)
        popup.PopupWindow.__init__(self, position=scale_origin,
                         size=(self._width, self._height),
                         scale=scale)

        appconfig = ba.app.config
        self._names = list(
            appconfig.get('Custom Team Names',
                          ba.app.config['Custom Team Names']))

        # We need to flatten the translation since it will be an
        # editable string.
        self._names = [
            ba.Lstr(translate=('teamNames', n)).evaluate() for n in self._names
        ]
        self._colors = list(
            appconfig.get('Custom Team Colors',
                          ba.app.config['Custom Team Colors']))

        self._color_buttons: list[ba.Widget] = []
        self._color_text_fields: list[ba.Widget] = []

        resetbtn = ba.buttonwidget(
            parent=self.root_widget,
            label=ba.Lstr(resource='settingsWindowAdvanced.resetText'),
            autoselect=True,
            scale=0.7,
            on_activate_call=self._reset,
            size=(120, 50),
            position=(self._width * 0.5 - 60 * 0.7,
                      self._height - 60 + 3 * (num_teams-2)))

        base_y = 76 * (num_teams-2)

        for i in range(num_teams):
            self._color_buttons.append(
                ba.buttonwidget(parent=self.root_widget,
                                autoselect=True,
                                position=(50,
                                    (0 + 195 - 90 * i) + base_y),
                                on_activate_call=ba.Call(self._color_click, i),
                                size=(70, 70),
                                color=self._colors[i],
                                label='',
                                button_type='square'))
            self._color_text_fields.append(
                ba.textwidget(parent=self.root_widget,
                              position=(135,
                                (0 + 201 - 90 * i) + base_y),
                              size=(280, 46),
                              text=self._names[i],
                              h_align='left',
                              v_align='center',
                              max_chars=self._max_name_length,
                              color=self._colors[i],
                              description=ba.Lstr(resource='nameText'),
                              editable=True,
                              padding=4))
        for i in range(num_teams):
            if i == num_teams-1:
                ba.widget(edit=self._color_text_fields[i],
                          up_widget=self._color_text_fields[i-1])
            else:
                if i == 0:
                    ba.widget(edit=self._color_text_fields[i],
                              down_widget=self._color_text_fields[i+1])
                else:
                    ba.widget(edit=self._color_text_fields[i],
                              down_widget=self._color_text_fields[i+1],
                              up_widget=self._color_text_fields[i-1])
            
                
        ba.widget(edit=self._color_text_fields[0], up_widget=resetbtn)

        cancelbtn = ba.buttonwidget(parent=self.root_widget,
                                    label=ba.Lstr(resource='cancelText'),
                                    autoselect=True,
                                    on_activate_call=self._on_cancel_press,
                                    size=(150, 50),
                                    position=(self._width * 0.5 - 200, 20))
        okbtn = ba.buttonwidget(parent=self.root_widget,
                                label=ba.Lstr(resource='okText'),
                                autoselect=True,
                                on_activate_call=self._ok,
                                size=(150, 50),
                                position=(self._width * 0.5 + 50, 20))
        ba.containerwidget(edit=self.root_widget,
                           selected_child=self._color_buttons[0])
        ba.widget(edit=okbtn, left_widget=cancelbtn)
        self._update()

    def _reset(self) -> None:
        for i in range(num_teams):
            self._colors[i] = ba.app.config['Custom Team Colors'][i]
            name = ba.Lstr(translate=('teamNames',
                ba.app.config['Custom Team Names'][i])).evaluate()
            if len(name) > self._max_name_length:
                print('GOT DEFAULT TEAM NAME LONGER THAN MAX LENGTH')
            ba.textwidget(edit=self._color_text_fields[i], text=name)
        self._update()

    def _update(self) -> None:
        for i in range(num_teams):
            ba.buttonwidget(edit=self._color_buttons[i], color=self._colors[i])
            ba.textwidget(edit=self._color_text_fields[i],
                          color=self._colors[i])

    def _ok(self) -> None:
        cfg = ba.app.config

        # First, determine whether the values here are defaults, in which case
        # we can clear any values from prefs.  Currently if the string matches
        # either the default raw value or its translation we consider it
        # default. (the fact that team names get translated makes this
        # situation a bit sloppy)
        new_names: list[str] = []
        is_default = True
        for i in range(num_teams):
            name = cast(str, ba.textwidget(query=self._color_text_fields[i]))
            if not name:
                ba.screenmessage(ba.Lstr(resource='nameNotEmptyText'),
                                 color=(1, 0, 0))
                ba.playsound(ba.getsound('error'))
                return
            new_names.append(name)

        for i in range(num_teams):
            if self._colors[i] != ba.app.config['Custom Team Colors'][i]:
                is_default = False
            default_team_name = ba.app.config['Custom Team Names'][i]
            default_team_name_translated = ba.Lstr(
                translate=('teamNames', default_team_name)).evaluate()
            if ((new_names[i] != default_team_name
                 and new_names[i] != default_team_name_translated)):
                is_default = False

        if is_default:
            for key in ('Custom Team Names', 'Custom Team Colors'):
                if key in cfg:
                    del cfg[key]
        else:
            cfg['Custom Team Names'] = list(new_names)
            cfg['Custom Team Colors'] = list(self._colors)

        cfg.commit()
        self._transition_out()


# ba_meta export plugin
class MoreTeamsPlugin(ba.Plugin):
    def on_app_launch(self) -> None:
        if 'Custom Team Colors' and 'Custom Team Names' in ba.app.config:
            DEFAULT_TEAM_COLORS = ()
            DEFAULT_TEAM_NAMES = ()
            old_custom_colors = ba.app.config['Custom Team Colors']
            old_custom_names = ba.app.config['Custom Team Names']
            old_num_teams = len(old_custom_colors)
            if num_teams == old_num_teams:
                if ba.app.config['Custom Team Colors'] != old_custom_colors and (
                        ba.app.config['Custom Team Names'] != old_custom_names):
                    for i in range(num_teams):
                        DEFAULT_TEAM_COLORS += ((1,1,1),)
                        DEFAULT_TEAM_NAMES += ('Team '+str(i+1),)
                        ba.app.config['Custom Team Colors'] = DEFAULT_TEAM_COLORS
                        ba.app.config.apply_and_commit()
                        ba.app.config['Custom Team Names'] = DEFAULT_TEAM_NAMES
                        ba.app.config.apply_and_commit()
            else:
                for i in range(num_teams):
                    DEFAULT_TEAM_COLORS += ((1,1,1),)
                    DEFAULT_TEAM_NAMES += ('Team '+str(i+1),)
                    ba.app.config['Custom Team Colors'] = DEFAULT_TEAM_COLORS
                    ba.app.config.apply_and_commit()
                    ba.app.config['Custom Team Names'] = DEFAULT_TEAM_NAMES
                    ba.app.config.apply_and_commit()
        else:
            DEFAULT_TEAM_COLORS = ()
            DEFAULT_TEAM_NAMES = ()
            for i in range(num_teams):
                DEFAULT_TEAM_COLORS += ((1,1,1),)
                DEFAULT_TEAM_NAMES += ('Team '+str(i+1),)
                ba.app.config['Custom Team Colors'] = DEFAULT_TEAM_COLORS
                ba.app.config.apply_and_commit()
                ba.app.config['Custom Team Names'] = DEFAULT_TEAM_NAMES
                ba.app.config.apply_and_commit()
    playoptions.PlayOptionsWindow = PlayOptionsWindow
    teamnamescolors.TeamNamesColorsWindow = TeamNamesColorsWindow
