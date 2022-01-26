# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'iceMap'

package_files = {
    "iceMapColor.dds": {
        "md5": "61dadb6e68eab0e69abcb891500aa0d5",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/iceMapColor.dds",
        "target": "ba_data/textures/iceMapColor.dds"
    },
    "iceMapTopCob.cob": {
        "md5": "420edc2422d4a75253d1d372718eaa92",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/iceMapTopCob.cob",
        "target": "ba_data/models/iceMapTopCob.cob"
    },
    "iceMapTop.bob": {
        "md5": "1c2afc3f7b17d1e788150945fb19af7c",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/iceMapTop.bob",
        "target": "ba_data/models/iceMapTop.bob"
    },
    "iceMapPreview.ktx": {
        "md5": "39146f2246341c7036d044bb54fdb788",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/iceMapPreview.ktx",
        "target": "ba_data/textures/iceMapPreview.ktx"
    },
    "iceMapIce.bob": {
        "md5": "b89807481e96f854b97b37f38709831d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/iceMapIce.bob",
        "target": "ba_data/models/iceMapIce.bob"
    },
    "natureBackgroundNColor.dds": {
        "md5": "2a0e93248cd284ec5875c2fd005ca8e3",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/natureBackgroundNColor.dds",
        "target": "ba_data/textures/natureBackgroundNColor.dds"
    },
    "iceMapPreview.dds": {
        "md5": "d874e09943d502b689e92a3c32bfe3cc",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/iceMapPreview.dds",
        "target": "ba_data/textures/iceMapPreview.dds"
    },
    "iceMapBottom.bob": {
        "md5": "c61b7d717399565a6320a3278da9b827",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/iceMapBottom.bob",
        "target": "ba_data/models/iceMapBottom.bob"
    },
    "iceMapIceCob.cob": {
        "md5": "6b1ab014d59932666e59923132b658ca",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/iceMapIceCob.cob",
        "target": "ba_data/models/iceMapIceCob.cob"
    },
    "iceMapColor.ktx": {
        "md5": "29cca7526a8c928505913e89d8e6136b",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/iceMapColor.ktx",
        "target": "ba_data/textures/iceMapColor.ktx"
    },
    "iceMapBottomCob.cob": {
        "md5": "76185914f2f3a86771d4781116ec4933",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/iceMapBottomCob.cob",
        "target": "ba_data/models/iceMapBottomCob.cob"
    },
    "natureBackgroundNColor.ktx": {
        "md5": "e00ec03bee7ad98e704cc361ed11882f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/iceMap/natureBackgroundNColor.ktx",
        "target": "ba_data/textures/natureBackgroundNColor.ktx"
    }
}


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

from PackInstaller import PackInstaller
PackInstaller(package_name, files_needed)


class Defs:
    # This file was automatically generated from "thePadLevel.ma"
    points = {}
    boxes = {}
    points['ffa_spawn1'] = (8.73357, 5.09934, 2.27606) + (0.78982, 0.05, 1.3628)
    points['ffa_spawn2'] = (8.63628, 5.83788, -7.26134) + (0.78982, 0.05, 1.3628)
    points['ffa_spawn3'] = (-9.03869, 5.09934, 2.27066) + (0.78982, 0.05, 1.3628)
    points['ffa_spawn4'] = (-8.89221, 5.83788, -7.2801) + (0.78982, 0.05, 1.3628)
    points['flag1'] = (8.97686, 5.45802, 4.83282)
    points['flag2'] = (-8.94129, 6.20577, -8.61665)
    points['flag3'] = (-9.36293, 5.45802, 4.79063)
    points['flag4'] = (8.63678, 6.20577, -8.66938)
    points['flag_default'] = (-0.19593, 4.38208, 4.59982)
    points['powerup_spawn1'] = (9.3797, 5.59043, 3.62563)
    points['powerup_spawn2'] = (-9.70205, 5.65105, 3.64135)
    points['powerup_spawn3'] = (-9.92278, 6.17397, -6.07351)
    points['powerup_spawn4'] = (9.52793, 6.07397, -6.12759)
    points['race_mine1'] = (6.62301, 5.38078, 3.805)
    points['race_mine2'] = (4.548, 5.38078, 0.49843)
    points['race_mine3'] = (5.73178, 5.74403, -4.13684)
    points['race_mine4'] = (-6.43899, 5.51047, -4.09674)
    points['race_mine5'] = (-5.05255, 5.36071, 0.52398)
    points['race_mine6'] = (-7.22847, 5.33566, 3.74171)
    points['race_point1'] = (-0.23437, 5.40034, 4.69668) + (0.2825, 3.95051, 1.70289)
    points['race_point2'] = (8.70337, 5.34581, 2.06327) + (1.54214, 3.95051, 0.2825)
    points['race_point3'] = (8.60551, 5.82501, -7.23624) + (1.4634, 3.95051, 0.2575)
    points['race_point4'] = (-9.01558, 5.7132, -7.22704) + (1.4513, 3.95051, 0.26029)
    points['race_point5'] = (-9.16008, 5.53273, 2.04487) + (1.54315, 3.95051, 0.2825)
    points['spawn1'] = (-4.03787, 3.21046, -6.22642) + (0.93466, 0.05, 3.0751)
    points['spawn2'] = (4.45458, 3.23662, -6.22464) + (0.93466, 0.05, 3.0751)
    points['tnt1'] = (-0.21676, 5.59505, -2.38739)
    boxes['area_of_interest_bounds'] = (-0.08966, 2.55672, -3.97028) + (0, 0, 0) + (24.12044, 12.6595, 18.50299)
    boxes['map_bounds'] = (-0.18319, 6.96282, -1.58038) + (0, 0, 0) + (29.23565, 16.29936, 21.43922)
    

class IceMap(ba.Map):
    defs = Defs()
    name = 'Ice Map'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return [
            'melee','keep_away','team_flag','king_of_the_hill','conquest','race']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'iceMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model_top': ba.getmodel('iceMapTop'),
            'collide_model_top': ba.getcollidemodel('iceMapTopCob'),
            'model_bottom': ba.getmodel('iceMapBottom'),
            'collide_model_bottom': ba.getcollidemodel('iceMapBottomCob'),
            'model_ice': ba.getmodel('iceMapIce'),
            'collide_model_ice': ba.getcollidemodel('iceMapIceCob'),
            'tex': ba.gettexture('iceMapColor'),
            'bgtex': ba.gettexture('natureBackgroundNColor'),
            'bgmodel': ba.getmodel('natureBackground')
        }
        mat = ba.Material()
        mat.add_actions(actions=('modify_part_collision', 'friction', 0.01))
        data['ice_material'] = mat
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.top = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model_top'],
                'model': self.preloaddata['model_top'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.bottom = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model_bottom'],
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.ice = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model_ice'],
                'model': self.preloaddata['model_ice'],
                'reflection': 'soft',
                'reflection_scale': [0.65],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material,
                              self.preloaddata['ice_material']]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.8, 0.9, 1.3)
        gnode.ambient_color = (0.8, 0.9, 1.3)
        gnode.vignette_outer = (0.79, 0.79, 0.69)
        gnode.vignette_inner = (0.97, 0.97, 0.99)

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(IceMap)
