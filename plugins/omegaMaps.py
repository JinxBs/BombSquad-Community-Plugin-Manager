# ba_meta require api 6
from __future__ import annotations

import os
import ssl
import threading
import urllib.request
from hashlib import md5
from typing import TYPE_CHECKING

import _ba
import ba
from ba import _map
from bastd.gameutils import SharedObjects

ssl._create_default_https_context = ssl._create_unverified_context

if TYPE_CHECKING:
    from typing import Any

package_name = 'omegaMaps'

package_files = {
    "zigZagLevelCollide1.cob": {
        "md5": "63352bb377b3a719338f3dfe6c756d22",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/zigZagLevelCollide1.cob",
        "target": "ba_data/models/zigZagLevelCollide1.cob"
    },
    "roundaboutLevelBumper1.cob": {
        "md5": "0a91ddfccb7fdf3658bacf8e0c39a089",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/roundaboutLevelBumper1.cob",
        "target": "ba_data/models/roundaboutLevelBumper1.cob"
    },
    "rampageLevel1.bob": {
        "md5": "6222ff2063eb3d403460df698fdf22ef",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/rampageLevel1.bob",
        "target": "ba_data/models/rampageLevel1.bob"
    },
    "bridgitLevelBottom1.bob": {
        "md5": "56148c4fe2fff9d64111c9a1e8127dbe",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/bridgitLevelBottom1.bob",
        "target": "ba_data/models/bridgitLevelBottom1.bob"
    },
    "bridgitLevelRailingCollide1.cob": {
        "md5": "a7687fae3ae7ae82b0cfd81456d0eba4",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/bridgitLevelRailingCollide1.cob",
        "target": "ba_data/models/bridgitLevelRailingCollide1.cob"
    },
    "roundaboutLevel1.bob": {
        "md5": "4d164a386216990cc2f81977cae9585a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/roundaboutLevel1.bob",
        "target": "ba_data/models/roundaboutLevel1.bob"
    },
    "rampageLevelBottom1.bob": {
        "md5": "5c2ea72280713ed51e434b34ed4f8d25",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/rampageLevelBottom1.bob",
        "target": "ba_data/models/rampageLevelBottom1.bob"
    },
    "zigZagLevelBottom1.bob": {
        "md5": "dd346033efba991db056097b0d9ff684",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/zigZagLevelBottom1.bob",
        "target": "ba_data/models/zigZagLevelBottom1.bob"
    },
    "rampageBumper2.cob": {
        "md5": "07c3063472be682c835d4160d5a05dd1",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/rampageBumper2.cob",
        "target": "ba_data/models/rampageBumper2.cob"
    },
    "rampageLevelCollide1.cob": {
        "md5": "06bf820523bf481eb36a195cba227915",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/rampageLevelCollide1.cob",
        "target": "ba_data/models/rampageLevelCollide1.cob"
    },
    "roundaboutLevelCollide1.cob": {
        "md5": "cb21dbbe47bb8b893c2ef2d06f49b303",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/roundaboutLevelCollide1.cob",
        "target": "ba_data/models/roundaboutLevelCollide1.cob"
    },
    "zigZagLevel1.bob": {
        "md5": "80f51a7122a29ac864e7c3821f220827",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/zigZagLevel1.bob",
        "target": "ba_data/models/zigZagLevel1.bob"
    },
    "zigZagLevelBumper1.cob": {
        "md5": "bff591f517f0613dd8c9d74cefb9106b",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/zigZagLevelBumper1.cob",
        "target": "ba_data/models/zigZagLevelBumper1.cob"
    },
    "bridgitLevelCollide1.cob": {
        "md5": "e92de6d58341cecf4a20d343ea7ef633",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/bridgitLevelCollide1.cob",
        "target": "ba_data/models/bridgitLevelCollide1.cob"
    },
    "bridgitLevelTop1.bob": {
        "md5": "563b514181dcef8cfd0627f2b15356e1",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/omegaMaps/bridgitLevelTop1.bob",
        "target": "ba_data/models/bridgitLevelTop1.bob"
    }
}


class PackInstaller:
    def __init__(self, name, package_files):
        self.name = name
        self.package_files = package_files
        if self._installed():
            return
        try:
            ba.screenmessage(f'Installing pack: {self.name}', color=(1, 1, 0))
            download = threading.Thread(target=self.download)
            download.start()
        except:
            ba.print_exception()

    def _get_md5(self, file):
        with open(file, 'rb') as f:
            data = f.read()
            return md5(data).hexdigest()

    def _installed(self):
        for info in self.package_files.values():
            if not os.path.exists(info['target']):
                return False
            if check_md5:
                if self._get_md5(info['target']) != info['md5']:
                    return False
        return True

    def download(self):
        for info in self.package_files.values():

            # download only if file isnt present
            if os.path.exists(info['target']) and self._get_md5(info['target']) == info['md5']:
                continue
            request = info['url']
            try:
                response = urllib.request.urlopen(request)
                if response.getcode() == 200:
                    data = response.read()
                    with open(info['target'], 'wb') as f:
                        f.write(data)
            except:
                ba.print_exception()


class BetterroundaboutDefs:
    points = {}
    # noinspection PyDictCreation
    boxes = {}
    boxes['area_of_interest_bounds'] = (-1.552280404, 3.189001207, -2.40908495) + (
        0.0, 0.0, 0.0) + (11.96255385, 8.857531648, 9.531689995)
    points['ffa_spawn1'] = (-4.056288044, 3.85970651,
                            -4.6096757) + (0.9393824595, 1.0, 1.422669346)
    points['ffa_spawn2'] = (0.9091263403, 3.849381394,
                            -4.673201431) + (0.9179219809, 1.0, 1.422669346)
    points['ffa_spawn3'] = (-1.50312174, 1.498336991,
                            -0.7271163774) + (5.733928927, 1.0, 0.1877531607)
    points['flag1'] = (-3.01567985, 3.846779683, -6.702828912)
    points['flag2'] = (-0.01282460768, 3.828492613, -6.684991743)
    points['flag_default'] = (-1.509110449, 1.447854976, -1.440324146)
    boxes['map_bounds'] = (-1.615296127, 8.764115729, -2.663738363) + (
        0.0, 0.0, 0.0) + (20.48886392, 18.92340529, 13.79786814)
    points['powerup_spawn1'] = (-6.794510156, 2.660340814, 0.01205780317)
    points['powerup_spawn2'] = (3.611953494, 2.660340814, 0.01205780317)
    points['shadow_lower_bottom'] = (-1.848173322, 0.6339980822, 2.267036343)
    points['shadow_lower_top'] = (-1.848173322, 1.077175164, 2.267036343)
    points['shadow_upper_bottom'] = (-1.848173322, 6.04794944, 2.267036343)
    points['shadow_upper_top'] = (-1.848173322, 9.186681264, 2.267036343)
    points['spawn1'] = (-4.056288044, 3.85970651, -4.6096757) + (0.9393824595, 1.0,
                                                                 1.422669346)
    points['spawn2'] = (0.9091263403, 3.849381394,
                        -4.673201431) + (0.9179219809, 1.0, 1.422669346)
    points['tnt1'] = (-1.509110449, 2.457517361, 0.2340271555)


class BetterRoundabout(ba.Map):
    """Map with a narrow bridge in the middle."""
    defs = BetterroundaboutDefs()
    name = 'Better Roundabout'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'roundaboutPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('roundaboutLevel1'),
            'model_bottom': ba.getmodel('roundaboutLevelBottom'),
            'model_bg': ba.getmodel('natureBackground'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('roundaboutLevelCollide1'),
            'tex': ba.gettexture('roundaboutLevelColor'),
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'railing_collide_model':
                (ba.getcollidemodel('roundaboutLevelBumper1')),
            'bg_material': ba.Material()
        }
        data['bg_material'].add_actions(actions=('modify_part_collision',
                                                 'friction', 10.0))
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, -1, 1))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.bottom = ba.newnode('terrain',
                                 attrs={
                                     'model': self.preloaddata['model_bottom'],
                                     'lighting': False,
                                     'color_texture': self.preloaddata['tex']
                                 })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex']
            })
        ba.newnode('terrain',
                   attrs={
                       'model': self.preloaddata['bg_vr_fill_model'],
                       'lighting': False,
                       'vr_only': True,
                       'background': True,
                       'color_texture': self.preloaddata['model_bg_tex']
                   })
        self.bg_collide = ba.newnode('terrain',
                                     attrs={
                                         'collide_model':
                                             self.preloaddata['collide_bg'],
                                         'materials': [
                                             shared.footing_material,
                                             self.preloaddata['bg_material'],
                                             shared.death_material
                                         ]
                                     })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.0, 1.05, 1.1)
        gnode.ambient_color = (1.0, 1.05, 1.1)
        gnode.shadow_ortho = True
        gnode.vignette_outer = (0.63, 0.65, 0.7)
        gnode.vignette_inner = (0.97, 0.95, 0.93)


class BetterZigZag(ba.Map):
    """A very long zig-zaggy map"""

    from bastd.mapdata import zig_zag as defs

    name = 'Better Zigzag'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return [
            'melee', 'keep_away', 'team_flag', 'conquest', 'king_of_the_hill'
        ]

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'zigzagPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('zigZagLevel1'),
            'model_bottom': ba.getmodel('zigZagLevelBottom1'),
            'model_bg': ba.getmodel('natureBackground'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('zigZagLevelCollide1'),
            'tex': ba.gettexture('zigZagLevelColor'),
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'railing_collide_model': ba.getcollidemodel('zigZagLevelBumper1'),
            'bg_material': ba.Material()
        }
        data['bg_material'].add_actions(actions=('modify_part_collision',
                                                 'friction', 10.0))
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'color_texture': self.preloaddata['model_bg_tex']
            })
        self.bottom = ba.newnode('terrain',
                                 attrs={
                                     'model': self.preloaddata['model_bottom'],
                                     'lighting': False,
                                     'color_texture': self.preloaddata['tex']
                                 })
        ba.newnode('terrain',
                   attrs={
                       'model': self.preloaddata['bg_vr_fill_model'],
                       'lighting': False,
                       'vr_only': True,
                       'background': True,
                       'color_texture': self.preloaddata['model_bg_tex']
                   })
        self.bg_collide = ba.newnode('terrain',
                                     attrs={
                                         'collide_model':
                                             self.preloaddata['collide_bg'],
                                         'materials': [
                                             shared.footing_material,
                                             self.preloaddata['bg_material'],
                                             shared.death_material
                                         ]
                                     })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.0, 1.15, 1.15)
        gnode.ambient_color = (1.0, 1.15, 1.15)
        gnode.vignette_outer = (0.57, 0.59, 0.63)
        gnode.vignette_inner = (0.97, 0.95, 0.93)
        gnode.vr_camera_offset = (-1.5, 0, 0)


class DoublebridgitDefs:
    points = {}
    # noinspection PyDictCreation
    boxes = {}
    boxes['area_of_interest_bounds'] = (-0.2457963347, 3.828181068,
                                        -1.528362695) + (0.0, 0.0, 0.0) + (
                                            19.14849937, 7.312788846, 8.436232726)
    points['ffa_spawn1'] = (-5.869295124, 3.715437928,
                            -1.617274877) + (0.9410329222, 1.0, 1.818908238)
    points['ffa_spawn2'] = (5.160809653, 3.761793434,
                            -1.443012115) + (0.7729807005, 1.0, 1.818908238)
    points['ffa_spawn3'] = (-0.42664, 3.76179, -3.80255) + (4.03415, 0.05, 0.27317)
    points['flag1'] = (-7.354603923, 3.770769731, -1.617274877)
    points['flag2'] = (6.885846926, 3.770685211, -1.443012115)
    points['flag_default'] = (-0.2227795102, 3.802429326, -1.562586233)
    boxes['map_bounds'] = (-0.1916036665, 7.481446847, -1.311948055) + (
        0.0, 0.0, 0.0) + (27.41996888, 18.47258973, 19.52220249)
    points['powerup_spawn1'] = (6.82849491, 4.658454461, 0.1938139802)
    points['powerup_spawn2'] = (-7.253381358, 4.728692078, 0.252121017)
    points['powerup_spawn3'] = (6.82849491, 4.658454461, -3.461765427)
    points['powerup_spawn4'] = (-7.253381358, 4.728692078, -3.40345839)
    points['shadow_lower_bottom'] = (-0.2227795102, 2.83188898, 2.680075641)
    points['shadow_lower_top'] = (-0.2227795102, 3.498267184, 2.680075641)
    points['shadow_upper_bottom'] = (-0.2227795102, 6.305086402, 2.680075641)
    points['shadow_upper_top'] = (-0.2227795102, 9.470923628, 2.680075641)
    points['spawn1'] = (-5.869295124, 3.715437928,
                        -1.617274877) + (0.9410329222, 1.0, 1.818908238)
    points['spawn2'] = (5.160809653, 3.761793434,
                        -1.443012115) + (0.7729807005, 1.0, 1.818908238)


class DoubleBridgit(ba.Map):
    """Map with a narrow bridge in the middle."""
    defs = DoublebridgitDefs()

    name = 'Double Bridgit'
    dataname = 'bridgit'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'team_flag', 'keep_away']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'bridgitPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model_top': ba.getmodel('bridgitLevelTop1'),
            'model_bottom': ba.getmodel('bridgitLevelBottom1'),
            'model_bg': ba.getmodel('natureBackground'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('bridgitLevelCollide1'),
            'tex': ba.gettexture('bridgitLevelColor'),
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'railing_collide_model': (ba.getcollidemodel('bridgitLevelRailingCollide1')),
            'bg_material': ba.Material()
        }
        data['bg_material'].add_actions(actions=('modify_part_collision',
                                                 'friction', 10.0))
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model_top'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.bottom = ba.newnode('terrain',
                                 attrs={
                                     'model': self.preloaddata['model_bottom'],
                                     'lighting': False,
                                     'color_texture': self.preloaddata['tex']
                                 })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex']
            })
        ba.newnode('terrain',
                   attrs={
                       'model': self.preloaddata['bg_vr_fill_model'],
                       'lighting': False,
                       'vr_only': True,
                       'background': True,
                       'color_texture': self.preloaddata['model_bg_tex']
                   })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True
            })
        self.bg_collide = ba.newnode('terrain',
                                     attrs={
                                         'collide_model':
                                             self.preloaddata['collide_bg'],
                                         'materials': [
                                             shared.footing_material,
                                             self.preloaddata['bg_material'],
                                             shared.death_material
                                         ]
                                     })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.2, 1.3)
        gnode.ambient_color = (1.1, 1.2, 1.3)
        gnode.vignette_outer = (0.65, 0.6, 0.55)
        gnode.vignette_inner = (0.9, 0.9, 0.93)


class DoublerampageDefs:
    points = {}
    # noinspection PyDictCreation
    boxes = {}
    boxes['area_of_interest_bounds'] = (0.3544110667, 5.616383286,
                                        -4.066055072) + (0.0, 0.0, 0.0) + (
                                            19.90053969, 10.34051135, 8.16221072)
    boxes['edge_box'] = (0.3544110667, 5.438284793, -4.100357672) + (
        0.0, 0.0, 0.0) + (12.57718032, 4.645176013, 3.605557343)
    points['ffa_spawn1'] = (0.5006944438, 5.051501304,
                            -5.79356326) + (6.626174027, 1.0, 0.3402012662)
    points['ffa_spawn2'] = (0.5006944438, 5.051501304,
                            -2.435321368) + (6.626174027, 1.0, 0.3402012662)
    points['flag1'] = (-5.885814199, 5.112162255, -4.251754911)
    points['flag2'] = (6.700855451, 5.10270501, -4.259912982)
    points['flag_default'] = (0.3196701116, 5.110914413, -4.292515158)
    boxes['map_bounds'] = (0.4528955042, 4.899663734, -3.543675157) + (
        0.0, 0.0, 0.0) + (23.54502348, 14.19991443, 12.08017448)
    points['powerup_spawn1'] = (-2.645358507, 6.426340583, -4.226597191)
    points['powerup_spawn2'] = (3.540102796, 6.549722855, -4.198476335)
    points['shadow_lower_bottom'] = (5.580073911, 3.136491026, 5.341226521)
    points['shadow_lower_top'] = (5.580073911, 4.321758709, 5.341226521)
    points['shadow_upper_bottom'] = (5.274539479, 8.425373402, 5.341226521)
    points['shadow_upper_top'] = (5.274539479, 11.93458162, 5.341226521)
    points['spawn1'] = (-4.745706238, 5.051501304,
                        -4.247934288) + (0.9186962739, 1.0, 0.5153189341)
    points['spawn2'] = (5.838590388, 5.051501304,
                        -4.259627405) + (0.9186962739, 1.0, 0.5153189341)

class DoubleRampage(ba.Map):
    """Wee little map with ramps on the sides."""

    defs = DoublerampageDefs()

    name = 'Double Rampage'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'rampagePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('rampageLevel1'),
            'bottom_model': ba.getmodel('rampageLevelBottom1'),
            'collide_model': ba.getcollidemodel('rampageLevelCollide1'),
            'tex': ba.gettexture('rampageLevelColor'),
            'bgtex': ba.gettexture('rampageBGColor'),
            'bgtex2': ba.gettexture('rampageBGColor2'),
            'bgmodel': ba.getmodel('rampageBG'),
            'bgmodel2': ba.getmodel('rampageBG2'),
            'vr_fill_model': ba.getmodel('rampageVRFill'),
            'railing_collide_model': ba.getcollidemodel('rampageBumper2')
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        self.bottom = ba.newnode('terrain',
                                 attrs={
                                     'model': self.preloaddata['bottom_model'],
                                     'lighting': False,
                                     'color_texture': self.preloaddata['tex']
                                 })
        self.bg2 = ba.newnode('terrain',
                              attrs={
                                  'model': self.preloaddata['bgmodel2'],
                                  'lighting': False,
                                  'background': True,
                                  'color_texture': self.preloaddata['bgtex2']
                              })
        ba.newnode('terrain',
                   attrs={
                       'model': self.preloaddata['vr_fill_model'],
                       'lighting': False,
                       'vr_only': True,
                       'background': True,
                       'color_texture': self.preloaddata['bgtex2']
                   })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2, 1.1, 0.97)
        gnode.ambient_color = (1.3, 1.2, 1.03)
        gnode.vignette_outer = (0.62, 0.64, 0.69)
        gnode.vignette_inner = (0.97, 0.95, 0.93)

    def is_point_near_edge(self,
                           point: ba.Vec3,
                           running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5


files_needed = {}
headless_mode = _ba.env()['headless_mode']
for file, value in package_files.items():
    if headless_mode:
        if not file.endswith('.cob'):
            continue
    else:
        if file.endswith('.dds'):
            if  _ba.app.platform == 'android':
                continue
        elif file.endswith('.ktx'):
            if _ba.app.platform != 'android':
                continue
    files_needed[file] = value

check_md5 = True

PackInstaller(package_name, files_needed)


# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        for map in (BetterRoundabout, BetterZigZag, DoubleBridgit, DoubleRampage):
            try:
                _map.register_map(map)
            except:
                pass
