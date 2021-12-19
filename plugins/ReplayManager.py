"""
ReplayManager | Help's to manage simple oprations.

What's special in it?
    new cool stable UI experince
    save's replay in any directory you want
    load's any replay from anywhere in your directories
    fileselector is ezy to use and useful
    clean beginner frieldy code

I apreciate any kind of modification. So feel free to use or edit code or change credit string.... no problem.

really awsome servers:
    BCS - https://discord.gg/2RKd9QQdQY
    BOMBSPOT - https://discord.gg/ucyaesh
    CYCLONES - https://discord.gg/pJXxkbQ7kH
"""
from __future__ import annotations

__author__ = 'pranav1711'
__version__ = 1.0

from typing import TYPE_CHECKING, cast
from bastd.ui.confirm import ConfirmWindow
from bastd.ui.fileselector import FileSelectorWindow
from ba.modutils import _request_storage_permission
from bastd import mainmenu
from bastd.ui.watch import WatchWindow

import copy
import os
import shutil
import ba
import _ba

if TYPE_CHECKING:
    from typing import Any, Type, List, Dict, Tuple, Union, Sequence, Optional


DEFAULT_PATH = _ba.env()["python_directory_user"].split('BombSquad')[0]
CONFIGPATH = "ReplayPath"
APPCONFIG = ba.app.config
BUILD = 20327


def set_default_configs() -> None:
    """
    Set's default replay saving path config
    """
    if CONFIGPATH not in APPCONFIG:
        APPCONFIG[CONFIGPATH] = DEFAULT_PATH
        APPCONFIG["stop_mark_as_default"] = False
    else:
        pass

# ba_meta require api 6
# ba_meta export plugin


class Plugin(ba.Plugin):
    def on_app_launch(self) -> None:
        """
        Main class, plugin object.

        Get the build number so we can get version of game.
        """
        if _ba.env().get('build_number', 0) >= BUILD:
            set_default_configs()
            WatchWindow._set_tab = new_set_tab
        else:
            print(__name__, 'works for 1.5 or higher')


class DirectoryWindow:
    def __init__(self, path: str, selected_replay: str, _type: str) -> None:
        """
        Window for selecting the path for replay

        Args:
            path (str): root path for window

            selected_replay (str): selected replay name

            _type (str): methord to use save/load
        """
        self.path = path
        self.type = _type
        self.selected_replay_name = selected_replay
        self.replay_file_path = _ba.get_replays_dir() + '/' + selected_replay
        self.selected_path = None
        self.make_directory_window()

    def make_directory_window(self) -> None:
        """
        Ask for the storage permission.

        Make's UI window of directory.
        """
        if _request_storage_permission():
            return

        if not APPCONFIG[CONFIGPATH] == DEFAULT_PATH:
            SaveAsWidnow(
                modal=False,
                replay_name=self.selected_replay_name,
                replay_file_path=self.replay_file_path,
                selected_path=APPCONFIG[CONFIGPATH])
        else:

            FileSelectorWindow(
                path=self.path,
                callback=self.on_folder_select,
                valid_file_extensions=['brp'],
                show_base_path=True,
                allow_folders=True if self.type == 'save' else False)

    def on_folder_select(self, path: str) -> None:
        """
        Get the folder and do oprations as a type

        types:
            save: save's the replay file(.brp) in requested directory
            load: load's the replay file(.brp) in requested directory

        Args:
            path (str): selected path by user

        """
        if path is None:
            return

        self.selected_path = path + '/'

        if self.type == 'save':
            SaveAsWidnow(
                modal=False,
                replay_name=self.selected_replay_name,
                replay_file_path=self.replay_file_path,
                selected_path=self.selected_path)

        elif self.type == 'load':
            _ba.increment_analytics_count('Replay watch')

            def do_it() -> None:
                try:
                    _ba.set_replay_speed_exponent(0)
                    _ba.fade_screen(True)
                    assert self.selected_replay_name is not None
                    _ba.new_replay_session(self.selected_path[:-1])

                except Exception:
                    ba.print_exception('Error running replay session.')
                    _ba.new_host_session(mainmenu.MainMenuSession)

            _ba.fade_screen(False, endcall=ba.Call(ba.pushcall, do_it))
            WatchWindow(transition='out_left')

        else:
            print(f"unkwon type {self.type}")


class SaveAsWidnow(ba.Window):
    """
    Window for Save file in given name
    """

    def __init__(self,
                 modal=None,
                 replay_name: str = '',
                 replay_file_path: str = None,
                 selected_path: str = None,
                 origin_widget: ba.Widget = None) -> None:
        """
        Make's the window

        Args:
            replay_name (str, optional): Replay name. Defaults to ''.

            replay_file_path (str, optional): Replay File path. Defaults to None.

            selected_path (str, optional): Selected path to save the file. Defaults to None.
        """

        self.modal = modal
        self.replay_name = replay_name[:-4]
        self.replay_file_path = replay_file_path
        self.selected_path = selected_path

        scale_origin: Optional[Tuple[float, float]]
        uiscale = ba.app.ui.uiscale

        width = 450
        height = 230

        if origin_widget is not None:
            self._transition_out = 'out_scale'
            scale_origin = origin_widget.get_screen_space_center()
            transition = 'in_scale'
        else:
            self._transition_out = 'out_right'
            scale_origin = None
            transition = 'in_right'

        super().__init__(
            root_widget=ba.containerwidget(
                size=(width, height),
                transition=transition,
                toolbar_visibility='menu_minimal_no_back',
                scale_origin_stack_offset=scale_origin,
                scale=(2.0 if uiscale is ba.UIScale.SMALL else
                       1.5 if uiscale is ba.UIScale.MEDIUM else 1.0)))

        self.back_button = ba.buttonwidget(
            parent=self._root_widget,
            scale=0.5,
            position=(40, height - 40),
            size=(60, 60),
            label='',
            on_activate_call=self.back,
            autoselect=True,
            color=(0.55, 0.5, 0.6),
            icon=ba.gettexture('crossOut'),
            iconscale=1.2)

        self.replay_name_text = ba.textwidget(
            parent=self._root_widget,
            text="Replay\n Name ",
            position=(22, height - 95),
            color=(0.8, 0.8, 0.8, 1.0),
            size=(90, 30),
            h_align='right')

        self._text_field = ba.textwidget(
            parent=self._root_widget,
            position=(125, height - 121),
            size=(280, 51),
            text=self.replay_name,
            h_align='left',
            v_align='center',
            max_chars=64,
            color=(0.9, 0.9, 0.9, 1.0),
            editable=True,
            padding=4)

        ba.widget(edit=self.back_button, down_widget=self._text_field)
        b_width = 200

        self.save_button = ba.buttonwidget(
            parent=self._root_widget,
            position=(width * 0.5 - b_width * 0.5, height - 200),
            size=(b_width, 60),
            scale=1.0,
            label='Save',
            on_activate_call=self.savefile)

        ba.containerwidget(
            edit=self._root_widget,
            cancel_button=self.back_button,
            start_button=self.save_button,
            selected_child=self._text_field)

    def back(self) -> None:
        """
        Get back to the previous window
        """
        ba.containerwidget(edit=self._root_widget,
                           transition=self._transition_out)
        if not self.modal:
            ba.app.ui.set_main_menu_window(
                WatchWindow(transition=None).get_root_widget())

    def savefile(self) -> None:
        """
        Save the file in the selected directory.

        Rename saved file for 'save as' option.
        """
        self.save_file_name = cast(
            str, ba.textwidget(query=self._text_field))

        shutil.copy(
            src=self.replay_file_path,
            dst=self.selected_path)

        os.rename(
            self.selected_path + self.replay_name + '.brp',
            self.selected_path + self.save_file_name + '.brp')
        self.back()

        if not APPCONFIG["stop_mark_as_default"]:
            request_mark_folder_as_default(self.selected_path)


def on_my_replay_save_press(self) -> None:
    """
    Cheak if any replay is selected otherwise trow error

    Call's directory window to save the replay.
    """
    if self._my_replay_selected is None:
        self._no_replay_selected_error()
        return

    current_path = APPCONFIG[CONFIGPATH]
    DirectoryWindow(current_path, self._my_replay_selected, 'save')


def on_my_replay_load(self) -> None:
    """
    Cheak if any replay is selected otherwise trow error. Get the file to load and play
    """
    if self._my_replay_selected is None:
        self._no_replay_selected_error()
        return

    current_path = APPCONFIG[CONFIGPATH]
    DirectoryWindow(current_path, self._my_replay_selected, 'load')


def request_mark_folder_as_default(folder_path: str) -> None:
    """Window for requewesting the to mark the folder as default(after SaveAs window to skip directory part).

    Args:
        folder_path (str): current folder path
    """
    ConfirmWindow(
        text=f'Mark this folder as default?',
        action=ba.Call(update_dict, folder_path),
        width=360.0,
        height=130.0,
        cancel_button=True,
        cancel_is_selected=True,
        color=(1, 1, 1),
        text_scale=1.0
    )


def update_dict(folder_path: str) -> None:
    """
    Update values in dictionary (ba.app.config)

    Args:

        folder_path (str): folder path to update
    """

    APPCONFIG[CONFIGPATH] = folder_path
    ba.app.config.commit()

    APPCONFIG["stop_mark_as_default"] = True


def reset(self) -> None:
    """
    Window asking for confirm reset
    """
    ConfirmWindow(
        text=f'reset defualt selected folder?',
        action=complete_reset,
        width=360.0,
        height=130.0,
        cancel_button=True,
        cancel_is_selected=True,
        color=(1, 1, 1),
        text_scale=1.0
    )


def complete_reset() -> None:
    """
    Resets the config's to default
    """
    APPCONFIG[CONFIGPATH] = DEFAULT_PATH
    APPCONFIG["stop_mark_as_default"] = False


def new_set_tab(self, tab_id: TabID) -> None:
    """
    Original at -> bastd.ui.watch.WatchWindow.set_tab

    Set's new buttons(save, load) and adjest all.
    """
    if self._current_tab == tab_id:
        return

    self._current_tab = tab_id

    cfg = ba.app.config
    cfg['Watch Tab'] = tab_id.value
    cfg.commit()

    self._tab_row.update_appearance(tab_id)

    if self._tab_container:
        self._tab_container.delete()

    scroll_left = (self._width - self._scroll_width) * 0.5
    scroll_bottom = self._height - self._scroll_height - 79 - 48

    self._tab_data = {}
    uiscale = ba.app.ui.uiscale

    if tab_id is self.TabID.MY_REPLAYS:
        c_width = self._scroll_width
        c_height = self._scroll_height - 20
        sub_scroll_height = c_height - 63

        self._my_replays_scroll_width = sub_scroll_width = (680 if uiscale is ba.UIScale.SMALL else 640)

        self._tab_container = cnt = ba.containerwidget(
            parent=self._root_widget,
            position=(scroll_left, scroll_bottom +
                      (self._scroll_height - c_height) * 0.5),
            size=(c_width, c_height),
            background=False,
            selection_loops_to_parent=True)

        v = c_height - 30

        ba.textwidget(
            parent=cnt,
            position=(c_width * 0.5, v),
            color=(0.6, 1.0, 0.6),
            scale=0.7,
            size=(0, 0),
            maxwidth=c_width * 0.9,
            h_align='center',
            v_align='center',
            text=ba.Lstr(
                resource='replayRenameWarningText',
                subs=[('${REPLAY}',
                       ba.Lstr(resource='replayNameDefaultText'))
                      ]))

        b_width = 140 if uiscale is ba.UIScale.SMALL else 178
        b_height = (107 if uiscale is ba.UIScale.SMALL else
                    142 if uiscale is ba.UIScale.MEDIUM else 190)
        b_space_extra = (0 if uiscale is ba.UIScale.SMALL else
                         -2 if uiscale is ba.UIScale.MEDIUM else -5)

        b_color = (0.6, 0.53, 0.63)
        b_textcolor = (0.75, 0.7, 0.8)
        btnv = (c_height - (48 if uiscale is ba.UIScale.SMALL else
                            45 if uiscale is ba.UIScale.MEDIUM else 40) -
                b_height)

        btnh = 40 if uiscale is ba.UIScale.SMALL else 40
        smlh = 190 if uiscale is ba.UIScale.SMALL else 225
        tscl = 1.0 if uiscale is ba.UIScale.SMALL else 1.2
        extra_space = 40 if uiscale is ba.UIScale.SMALL else 60 if uiscale is ba.UIScale.MEDIUM else 80

        btnv += extra_space

        if not APPCONFIG[CONFIGPATH] == DEFAULT_PATH:

            self.reset_btn = ba.buttonwidget(
                parent=cnt,
                size=(b_width / 2, b_height / 4),
                position=(c_width * 0.5 + 330, v + 40),
                button_type='square',
                color=b_color,
                textcolor=b_textcolor,
                on_activate_call=ba.Call(reset, self),
                text_scale=tscl,
                label='reset',
                autoselect=True)

        self._my_replays_watch_replay_button = btn1 = ba.buttonwidget(
            parent=cnt,
            size=(b_width, b_height / 2),
            position=(btnh, btnv),
            button_type='square',
            color=b_color,
            textcolor=b_textcolor,
            on_activate_call=self._on_my_replay_play_press,
            text_scale=tscl,
            label=ba.Lstr(resource=self._r + '.watchReplayButtonText'),
            autoselect=True)
        ba.widget(edit=btn1, up_widget=self._tab_row.tabs[tab_id].button)

        if uiscale is ba.UIScale.SMALL and ba.app.ui.use_toolbars:
            ba.widget(edit=btn1,
                      left_widget=_ba.get_special_widget('back_button'))

        btnv -= b_height + b_space_extra
        btnv += extra_space

        ba.buttonwidget(
            parent=cnt,
            size=(b_width, b_height / 2),
            position=(btnh, btnv),
            button_type='square',
            color=b_color,
            textcolor=b_textcolor,
            on_activate_call=self._on_my_replay_rename_press,
            text_scale=tscl,
            label=ba.Lstr(resource=self._r +
                          '.renameReplayButtonText'),
            autoselect=True)

        btnv -= b_height + b_space_extra
        btnv += extra_space

        ba.buttonwidget(
            parent=cnt,
            size=(b_width, b_height / 2),
            position=(btnh, btnv),
            button_type='square',
            color=b_color,
            textcolor=b_textcolor,
            on_activate_call=self._on_my_replay_delete_press,
            text_scale=tscl,
            label=ba.Lstr(resource=self._r +
                          '.deleteReplayButtonText'),
            autoselect=True)

        btnv -= b_height + b_space_extra
        btnv += extra_space

        ba.buttonwidget(
            parent=cnt,
            size=(b_width, b_height / 2),
            position=(btnh, btnv),
            button_type='square',
            color=b_color,
            textcolor=b_textcolor,
            on_activate_call=ba.Call(on_my_replay_save_press, self),
            text_scale=tscl,
            label="Save\nReplay",
            autoselect=True)

        btnv -= b_height + b_space_extra
        btnv += extra_space

        ba.buttonwidget(
            parent=cnt,
            size=(b_width, b_height / 2),
            position=(btnh, btnv),
            button_type='square',
            color=b_color,
            textcolor=b_textcolor,
            on_activate_call=ba.Call(on_my_replay_load, self),
            text_scale=tscl,
            label="Load\nReplay",
            autoselect=True)

        v -= sub_scroll_height + 23

        self._scrollwidget = scrlw = ba.scrollwidget(
            parent=cnt,
            position=(smlh, v),
            size=(sub_scroll_width, sub_scroll_height))
        ba.containerwidget(edit=cnt, selected_child=scrlw)

        self._columnwidget = ba.columnwidget(
            parent=scrlw,
            left_border=10,
            border=2,
            margin=0)

        ba.widget(
            edit=scrlw,
            autoselect=True,
            left_widget=btn1,
            up_widget=self._tab_row.tabs[tab_id].button)

        ba.widget(edit=self._tab_row.tabs[tab_id].button,
                  down_widget=scrlw)

        self._my_replay_selected = None
        self._refresh_my_replays()
