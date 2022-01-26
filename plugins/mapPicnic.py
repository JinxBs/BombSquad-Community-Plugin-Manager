# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'mapPicnic'

package_files = {
    "mapPicnicPreview.ktx": {
        "md5": "77b8b0ac74f0cdd05f81bb7024f120dc",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mapPicnic/mapPicnicPreview.ktx",
        "target": "ba_data/textures/mapPicnicPreview.ktx"
    },
    "mapPicnic.bob": {
        "md5": "7d5f423039ff8158ee66c8238b4d5ef8",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mapPicnic/mapPicnic.bob",
        "target": "ba_data/models/mapPicnic.bob"
    },
    "mapPicnicCob.cob": {
        "md5": "0f6de05dbfeb0ed5b32ec14fbdbc8c4a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mapPicnic/mapPicnicCob.cob",
        "target": "ba_data/models/mapPicnicCob.cob"
    },
    "mapPicnicDeathCob.cob": {
        "md5": "4ca617e5900561452e2a1451e61f596a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mapPicnic/mapPicnicDeathCob.cob",
        "target": "ba_data/models/mapPicnicDeathCob.cob"
    },
    "mapPicnicTransparent.bob": {
        "md5": "8590631c1a0e40a549c955541ece7375",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mapPicnic/mapPicnicTransparent.bob",
        "target": "ba_data/models/mapPicnicTransparent.bob"
    },
    "mapPicnicColor.ktx": {
        "md5": "8d680a695c4b3c646a1d868e448e5f08",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mapPicnic/mapPicnicColor.ktx",
        "target": "ba_data/textures/mapPicnicColor.ktx"
    },
    "mapPicnicTransparentCob.cob": {
        "md5": "fce6f383c3e1c123577f584edb1395cd",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mapPicnic/mapPicnicTransparentCob.cob",
        "target": "ba_data/models/mapPicnicTransparentCob.cob"
    },
    "mapPicnicColor.dds": {
        "md5": "5819ab98ba94437477162044ee2a7b8f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mapPicnic/mapPicnicColor.dds",
        "target": "ba_data/textures/mapPicnicColor.dds"
    },
    "mapPicnicPreview.dds": {
        "md5": "2c843812693868eaaa3b675650cf4f9c",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mapPicnic/mapPicnicPreview.dds",
        "target": "ba_data/textures/mapPicnicPreview.dds"
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
    points['ffa_spawn1'] = (-7.44398, 3.19387, -7.65979) + (1.50247, 0.03167, 0.55348)
    points['ffa_spawn2'] = (8.06371, 3.22003, -7.62365) + (1.4616, 0.02953, 0.51603)
    points['ffa_spawn3'] = (-7.41217, 3.194, 1.58774) + (1.49532, 0.05173, 0.50184)
    points['ffa_spawn4'] = (8.10603, 3.19399, 1.60122) + (1.42925, 0.05045, 0.48938)
    points['flag1'] = (-8.83272, 3.6421, -3.06993)
    points['flag2'] = (9.50256, 3.69934, -3.27696)
    points['flag_default'] = (0.30904, 3.54993, -3.16521)
    points['powerup_spawn1'] = (-3.82429, 3.7163, -6.69373)
    points['powerup_spawn2'] = (-6.30979, 3.77692, -0.92893)
    points['powerup_spawn3'] = (5.53497, 3.55785, -1.38555)
    points['powerup_spawn4'] = (5.67173, 3.55785, -6.19241)
    points['spawn1'] = (-8.88537, 3.19387, -3.02879) + (0.87378, 0.05, 1.6634)
    points['spawn2'] = (9.52927, 3.22003, -3.30216) + (0.87378, 0.05, 1.6634)
    points['tnt1'] = (0.73104, 3.61641, 0.91022)
    boxes['area_of_interest_bounds'] = (0.35441, 4.49356, -2.51839) + (0, 0, 0) + (23.64755, 8.06139, 18.50299)
    boxes['map_bounds'] = (0.39722, 4.89966, -5.12601) + (0, 0, 0) + (22.08287, 20.7854, 29.92689)
    

class PicnicMap(ba.Map):
    defs = Defs()
    name = 'Picnic'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'mapPicnicPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('mapPicnic'),
            'collide_model': ba.getcollidemodel('mapPicnicCob'),
            'modelc': ba.getmodel('mapPicnicTransparent'),
            'collide_modelc': ba.getcollidemodel('mapPicnicTransparentCob'),
            'collide_modeld': ba.getcollidemodel('mapPicnicDeathCob'),
            'tex': ba.gettexture('mapPicnicColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG')
        }
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
        self.nodec = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_modelc'],
                'model': self.preloaddata['modelc'],
                'color_texture': self.preloaddata['tex'],
                'opacity': 0.8,
                'materials': [shared.footing_material]
            })
        self.noded = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_modeld'],
                'materials': [shared.footing_material,
                              shared.death_material]
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
        gnode.tint = (1.1, 1.1, 1.0)
        gnode.ambient_color = (1.1, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(PicnicMap)
