# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'guardianMap'

package_files = {
    "skyGlassBG.ktx": {
        "md5": "d0e0dcbcdc1a1a0ac2ee135a3deabd44",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/guardianMap/skyGlassBG.ktx",
        "target": "ba_data/textures/skyGlassBG.ktx"
    },
    "guardianMapCob.cob": {
        "md5": "648a46324ddb883ab66ee9e1f5578fb1",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/guardianMap/guardianMapCob.cob",
        "target": "ba_data/models/guardianMapCob.cob"
    },
    "guardianMapPreview.dds": {
        "md5": "6c93e078f2267f1fad9b893c5c27a9c0",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/guardianMap/guardianMapPreview.dds",
        "target": "ba_data/textures/guardianMapPreview.dds"
    },
    "guardianMap.bob": {
        "md5": "862cb7c9c1aa9bc02e343e82a2f32887",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/guardianMap/guardianMap.bob",
        "target": "ba_data/models/guardianMap.bob"
    },
    "guardianMapColor.ktx": {
        "md5": "ba9cf86e182e621e06e6b70b304b6eb2",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/guardianMap/guardianMapColor.ktx",
        "target": "ba_data/textures/guardianMapColor.ktx"
    },
    "guardianMapColor.dds": {
        "md5": "7f0b6ca414ae3b28aabc33994acf9f27",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/guardianMap/guardianMapColor.dds",
        "target": "ba_data/textures/guardianMapColor.dds"
    },
    "skyGlassBG.dds": {
        "md5": "3ec0945c5c188ec7d4989020fc414eb6",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/guardianMap/skyGlassBG.dds",
        "target": "ba_data/textures/skyGlassBG.dds"
    },
    "guardianMapPreview.ktx": {
        "md5": "7ac123c93e088f5df3f5f7738d9af421",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/guardianMap/guardianMapPreview.ktx",
        "target": "ba_data/textures/guardianMapPreview.ktx"
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
    points['ffa_spawn1'] = (-2.07349, 3.88767, -6.65336) + (0.19747, 0.03, 0.51546)
    points['ffa_spawn2'] = (-4.70652, 3.91384, -3.78073) + (0.2047, 0.0271, 0.46127)
    points['ffa_spawn3'] = (-4.75011, 3.88779, 0.05944) + (0.46197, 0.0271, 0.20634)
    points['ffa_spawn4'] = (-1.96338, 3.88779, 2.74233) + (0.46098, 0.02698, 0.21011)
    points['ffa_spawn5'] = (2.1002, 3.88767, 2.65299) + (0.17194, 0.0271, 0.46628)
    points['ffa_spawn6'] = (4.74843, 3.91384, -0.14317) + (0.21347, 0.0271, 0.45728)
    points['ffa_spawn7'] = (4.71459, 3.88779, -4.09687) + (0.47092, 0.0271, 0.1773)
    points['ffa_spawn8'] = (1.80796, 3.88779, -6.9272) + (0.44113, 0.0271, 0.24531)
    points['flag1'] = (-12.55316, 4.98557, -14.28474)
    points['flag2'] = (12.34078, 5.04281, -14.94647)
    points['flag_default'] = (0.01441, 4.69604, -2.06973)
    points['powerup_spawn1'] = (-0.06763, 4.25657, -6.24298)
    points['powerup_spawn2'] = (-3.04409, 4.4172, -5.05894)
    points['powerup_spawn3'] = (-4.14865, 4.19812, -1.90987)
    points['powerup_spawn4'] = (-2.89817, 4.19812, 1.01643)
    points['powerup_spawn5'] = (0.06065, 4.35657, 2.15929)
    points['powerup_spawn6'] = (3.00639, 4.4172, 0.88465)
    points['powerup_spawn7'] = (4.18947, 4.19812, -2.12366)
    points['powerup_spawn8'] = (2.91713, 4.19812, -5.14095)
    points['spawn1'] = (-10.34384, 4.73805, -11.94499) + (0.09711, 0.04517, 3.35739)
    points['spawn2'] = (10.23575, 4.86421, -12.60951) + (3.34782, 0.04517, 0.2713)
    points['tnt1'] = (-5.48852, 4.87128, 3.64587)
    points['tnt2'] = (5.63454, 4.87128, 3.55774)
    boxes['area_of_interest_bounds'] = (-0.24115, 4.79046, -3.77876) + (0, 0, 0) + (17.63465, 15.05966, 16.71558)
    boxes['map_bounds'] = (-0.33468, 5.19656, -4.80404) + (0, 0, 0) + (30.96915, 26.52718, 27.03592)
    

class GuardianMap(ba.Map):
    defs = Defs()
    name = 'Guardian'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'guardianMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('guardianMap'),
            'collide_model': ba.getcollidemodel('guardianMapCob'),
            'tex': ba.gettexture('guardianMapColor'),
            'bgtex': ba.gettexture('skyGlassBG'),
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
        _map.register_map(GuardianMap)
