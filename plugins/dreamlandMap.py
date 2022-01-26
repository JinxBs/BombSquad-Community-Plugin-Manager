# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'dreamlandMap'

package_files = {
    "dreamlandMapColor.dds": {
        "md5": "bda203e2cfe909878652727ab2f210b1",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/dreamlandMapColor.dds",
        "target": "ba_data/textures/dreamlandMapColor.dds"
    },
    "dreamlandMapNPreview.ktx": {
        "md5": "a3b4332a4746b38cc537d67260cebc27",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/dreamlandMapNPreview.ktx",
        "target": "ba_data/textures/dreamlandMapNPreview.ktx"
    },
    "dreamlandMapBottomCob.cob": {
        "md5": "34fbf6c50e8ca999abb16d424d89fde8",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/dreamlandMapBottomCob.cob",
        "target": "ba_data/models/dreamlandMapBottomCob.cob"
    },
    "dreamlandMapPreview.ktx": {
        "md5": "994a4fd3f9225876e8b7136150e34bab",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/dreamlandMapPreview.ktx",
        "target": "ba_data/textures/dreamlandMapPreview.ktx"
    },
    "dreamlandMapPreview.dds": {
        "md5": "f58dbc7c8ccc68e7f157d8728192584f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/dreamlandMapPreview.dds",
        "target": "ba_data/textures/dreamlandMapPreview.dds"
    },
    "dreamlandMapCob.cob": {
        "md5": "2c08f895e2792185092842f6099b80b9",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/dreamlandMapCob.cob",
        "target": "ba_data/models/dreamlandMapCob.cob"
    },
    "dreamlandMapColor.ktx": {
        "md5": "05314980d146b6fcebb46d57a6b7719c",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/dreamlandMapColor.ktx",
        "target": "ba_data/textures/dreamlandMapColor.ktx"
    },
    "dreamlandMapNPreview.dds": {
        "md5": "373683cae6db67f8652dc3ef7ccab59d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/dreamlandMapNPreview.dds",
        "target": "ba_data/textures/dreamlandMapNPreview.dds"
    },
    "uknucklesBGColor.ktx": {
        "md5": "6556f72533b6e9c8ee0836a0c0c1a0fc",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/uknucklesBGColor.ktx",
        "target": "ba_data/textures/uknucklesBGColor.ktx"
    },
    "dreamlandMapBottom.bob": {
        "md5": "58a31fe6c07a42e25cb77d4c182dbf68",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/dreamlandMapBottom.bob",
        "target": "ba_data/models/dreamlandMapBottom.bob"
    },
    "uknucklesBGColor.dds": {
        "md5": "6850d4a1cf9018a9ca43a2ca07fb8bec",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/uknucklesBGColor.dds",
        "target": "ba_data/textures/uknucklesBGColor.dds"
    },
    "dreamlandMap.bob": {
        "md5": "0884957ab480c97f36652d082d280f96",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/dreamlandMap/dreamlandMap.bob",
        "target": "ba_data/models/dreamlandMap.bob"
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
    # This file generated from "torneo.ma"
    points = {}
    boxes = {}
    points['ffa_spawn1'] = (-6.69624, 2.85039, -4.10288) + (0.77236, 0.05, 0.87378)
    points['ffa_spawn2'] = (-10.40827, 2.85039, -1.56054) + (0.77236, 0.05, 0.87378)
    points['ffa_spawn3'] = (-8.65731, 2.85039, 2.62386) + (0.77236, 0.05, 0.87378)
    points['ffa_spawn4'] = (-2.02022, 2.85039, 4.61688) + (0.77236, 0.05, 0.87378)
    points['ffa_spawn5'] = (1.86972, 2.85039, 4.72121) + (0.77236, 0.05, 0.87378)
    points['ffa_spawn6'] = (8.4577, 2.85039, 2.62079) + (0.77236, 0.05, 0.87378)
    points['ffa_spawn7'] = (10.39531, 2.85039, -1.52552) + (0.77236, 0.05, 0.87378)
    points['ffa_spawn8'] = (6.67172, 2.85039, -4.13483) + (0.77236, 0.05, 0.87378)
    points['flag1'] = (-11.02499, 3.17053, 0.88749)
    points['flag2'] = (11.10934, 3.17053, 0.88885)
    points['flag3'] = (-8.37111, 3.25837, -4.26217)
    points['flag4'] = (8.32579, 3.3096, -4.23468)
    points['flag5'] = (-2.36192, 3.21392, 4.21456)
    points['flag6'] = (2.24404, 3.21392, 4.31202)
    points['flag_default'] = (-0.16211, 3.663, -0.46622)
    points['powerup_spawn1'] = (-8.08751, 3.11164, -6.17346)
    points['powerup_spawn2'] = (-6.24881, 3.0105, -0.35762)
    points['powerup_spawn3'] = (-2.07277, 3.11164, 6.74271)
    points['powerup_spawn4'] = (1.84842, 3.11164, 6.75979)
    points['powerup_spawn5'] = (6.08678, 3.0105, -0.38878)
    points['powerup_spawn6'] = (8.08131, 3.11164, -6.15938)
    points['spawn1'] = (-9.46633, 2.84651, 0.25554) + (0.87378, 0.05, 1.6634)
    points['spawn2'] = (9.38817, 2.84651, 0.21746) + (0.87378, 0.05, 1.6634)
    points['spawn_by_flag1'] = (-10.01502, 2.85596, 1.81426) + (0.84416, 0.05, 0.84945)
    points['spawn_by_flag2'] = (10.15712, 3.12542, 1.82582) + (0.85053, 0.05, 0.83403)
    points['spawn_by_flag3'] = (-7.454, 2.95629, -3.34154) + (0.8398, 0.05, 0.83771)
    points['spawn_by_flag4'] = (7.38268, 2.89333, -3.31041) + (0.84957, 0.05, 0.83771)
    points['spawn_by_flag5'] = (-2.22089, 3.01925, 5.55799) + (0.8398, 0.05, 0.83771)
    points['spawn_by_flag6'] = (1.84214, 3.05073, 5.55764) + (0.83672, 0.05, 0.83771)
    points['tnt1'] = (0.0091, 3.11164, -3.65076)
    points['tnt2'] = (0.0091, 3.11164, 2.39515)
    boxes['area_of_interest_bounds'] = (0.35441, 4.49356, -2.40045) + (0, 0, 0) + (29.91755, 23.28733, 24.08552)
    boxes['map_bounds'] = (0.26088, 5.81105, -3.66161) + (0, 0, 0) + (54.98705, 41.72606, 26.50049)
    

class DreamlandMap(ba.Map):
    defs = Defs()
    name = 'Dream Land'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill','conquest']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'dreamlandMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('dreamlandMap'),
            'collide_model': ba.getcollidemodel('dreamlandMapCob'),
            'modelb': ba.getmodel('dreamlandMapBottom'),
            'collide_modelb': ba.getcollidemodel('dreamlandMapBottomCob'),
            'tex': ba.gettexture('dreamlandMapColor'),
            'bgtex': ba.gettexture('uknucklesBGColor'),
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
        self.nodeb = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_modelb'],
                'model': self.preloaddata['modelb'],
                'color_texture': self.preloaddata['tex'],
                'lighting': False,
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
        gnode.tint = (0.9, 0.9, 1.3)
        gnode.ambient_color = (0.8, 0.9, 1.3)
        gnode.vignette_outer = (0.79, 0.79, 0.69)
        gnode.vignette_inner = (0.97, 0.97, 0.99)

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(DreamlandMap)
