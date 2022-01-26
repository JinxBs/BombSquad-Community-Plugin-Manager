# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'bikiniBottomMap'

package_files = {
    "bikiniBottomMapBG.bob": {
        "md5": "05313e78a62302fe2791ad8fd3ef24bc",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/bikiniBottomMapBG.bob",
        "target": "ba_data/models/bikiniBottomMapBG.bob"
    },
    "bikiniBottomMapBGColor.ktx": {
        "md5": "6c06dfc088b8edd54fab7a745b60061c",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/bikiniBottomMapBGColor.ktx",
        "target": "ba_data/textures/bikiniBottomMapBGColor.ktx"
    },
    "cangremovilColor.ktx": {
        "md5": "43301ff824cd1d485509674e6e49ed62",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/cangremovilColor.ktx",
        "target": "ba_data/textures/cangremovilColor.ktx"
    },
    "bikiniBottomMapColor.ktx": {
        "md5": "91f764531b63faa1c15753c4cfb9f299",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/bikiniBottomMapColor.ktx",
        "target": "ba_data/textures/bikiniBottomMapColor.ktx"
    },
    "bikiniBottomMapColor.dds": {
        "md5": "e499bfec39d793b0bf40424b99057e09",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/bikiniBottomMapColor.dds",
        "target": "ba_data/textures/bikiniBottomMapColor.dds"
    },
    "bikiniBottomMapCob.cob": {
        "md5": "1c5662b93973e69c63e449ee17fd523f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/bikiniBottomMapCob.cob",
        "target": "ba_data/models/bikiniBottomMapCob.cob"
    },
    "cangremovilColor.dds": {
        "md5": "948f7a83275db17451c6b6ed862a5cd0",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/cangremovilColor.dds",
        "target": "ba_data/textures/cangremovilColor.dds"
    },
    "bikiniBottomMapBGColor.dds": {
        "md5": "33c0f36dad26b4ac904b3e2b8b53b913",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/bikiniBottomMapBGColor.dds",
        "target": "ba_data/textures/bikiniBottomMapBGColor.dds"
    },
    "bikiniBottomPreview.dds": {
        "md5": "93b19b85f00ebee9932da09f22bb4b15",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/bikiniBottomPreview.dds",
        "target": "ba_data/textures/bikiniBottomPreview.dds"
    },
    "bikiniBottomPreview.ktx": {
        "md5": "d9275a66db9dff147a50b0b769e21aea",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/bikiniBottomPreview.ktx",
        "target": "ba_data/textures/bikiniBottomPreview.ktx"
    },
    "cangremovilModel.bob": {
        "md5": "986d4699e7bfe3bf55db008634a503bf",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/cangremovilModel.bob",
        "target": "ba_data/models/cangremovilModel.bob"
    },
    "bikiniBottomMap.bob": {
        "md5": "bb10c4aedaa7fa0f82ac6a9b25d3dd53",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bikiniBottomMap/bikiniBottomMap.bob",
        "target": "ba_data/models/bikiniBottomMap.bob"
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
    points['ffa_spawn1'] = (-12.941, 0.49259, 0.40543) + (0.4868, 0.05, 1.25935)
    points['ffa_spawn2'] = (10.01692, 0.53469, -5.54644) + (2.14841, 0.05, 0.69308)
    points['ffa_spawn3'] = (12.65346, 0.5398, 0.32502) + (0.41375, 0.05, 1.32322)
    points['ffa_spawn4'] = (-9.92497, 0.54031, -5.55539) + (2.1591, 0.05, 0.65578)
    points['flag1'] = (-10.10481, 0.81866, 5.65734)
    points['flag2'] = (9.64363, 0.7631, 5.65322)
    points['flag_default'] = (0.20325, 3.43438, -4.75406)
    points['powerup_spawn1'] = (-7.33996, 0.7924, 1.15642)
    points['powerup_spawn2'] = (-2.61051, 0.7562, 1.13188)
    points['powerup_spawn3'] = (2.95595, 0.75344, 1.11008)
    points['powerup_spawn4'] = (7.01624, 0.77552, 1.14522)
    points['spawn1'] = (-9.92708, 0.52016, -5.56546) + (2.30817, 0.05, 0.69569)
    points['spawn2'] = (10.03658, 0.50706, -5.54186) + (2.35914, 0.05, 0.71615)
    points['tnt1'] = (0.0365, 0.87095, 5.72216)
    boxes['area_of_interest_bounds'] = (-0.01839, 1.30799, 0.46229) + (0, 0, 0) + (38.48324, 21.2151, 14.40626)
    boxes['map_bounds'] = (0.47584, 4.09931, 0.09103) + (0, 0, 0) + (59.82487, 27.42716, 23.30082)

class Cangremovil(ba.Actor):
    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 position2: Sequence[float] = (0.0, 1.0, 0.0),
                 time: float = 5.0):
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'position': position,
                'model': ba.getmodel('cangremovilModel'),
                'body': 'crate',
                'body_scale': 3.0,
                'density': 999999999999999999999,
                'damping': 999999999999999999999,
                'gravity_scale': 0.0,
                'reflection': 'powerup',
                'reflection_scale': [0.3],
                'color_texture': ba.gettexture('cangremovilColor'),
                'materials': [shared.footing_material]
            }
        )
        ba.animate_array(self.node,
                         'position',
                         3,
                         {0.0: position, time: position2}, loop=True)

class BikiniBottomMap(ba.Map):
    defs = Defs()
    name = 'Bikini Bottom'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'bikiniBottomPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('bikiniBottomMap'),
            'collide_model': ba.getcollidemodel('bikiniBottomMapCob'),
            'tex': ba.gettexture('bikiniBottomMapColor'),
            'bgtex': ba.gettexture('bikiniBottomMapBGColor'),
            'bgmodel': ba.getmodel('bikiniBottomMapBG')
        }
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        Cangremovil(position=(-30.10481, 0.81866, 3.05734),
                    position2=(30.10481, 0.81866, 3.05734),
                    time=3.0).autoretain()
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
                'materials': [shared.footing_material],
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
        _map.register_map(BikiniBottomMap)
