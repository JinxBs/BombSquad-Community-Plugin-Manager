# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'gotchaMap'

package_files = {
    "gotchaMapColor.dds": {
        "md5": "9dbc9cf5f2e8ea488102ba75253b4c8a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gotchaMap/gotchaMapColor.dds",
        "target": "ba_data/textures/gotchaMapColor.dds"
    },
    "gotchaMap.bob": {
        "md5": "3415e902a77ffa579fd825da877c51f2",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gotchaMap/gotchaMap.bob",
        "target": "ba_data/models/gotchaMap.bob"
    },
    "gotchaMapColor.ktx": {
        "md5": "f8ff1a19e1f994572ec7fe0b53098d74",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gotchaMap/gotchaMapColor.ktx",
        "target": "ba_data/textures/gotchaMapColor.ktx"
    },
    "gotchaMapRailing.cob": {
        "md5": "4e99322da9ffb84a95acfdc451f67750",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gotchaMap/gotchaMapRailing.cob",
        "target": "ba_data/models/gotchaMapRailing.cob"
    },
    "gotchaMapBG.bob": {
        "md5": "1903f42c0edc8403c9d1fbfb10a9cf7d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gotchaMap/gotchaMapBG.bob",
        "target": "ba_data/models/gotchaMapBG.bob"
    },
    "gotchaMapCob.cob": {
        "md5": "4196e66d85f35ae5ec3fe4004a2ef3f9",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gotchaMap/gotchaMapCob.cob",
        "target": "ba_data/models/gotchaMapCob.cob"
    },
    "gotchaMapPreview.ktx": {
        "md5": "f17bc3d3eb68c43eec28e4ea20097810",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gotchaMap/gotchaMapPreview.ktx",
        "target": "ba_data/textures/gotchaMapPreview.ktx"
    },
    "gotchaMapPreview.dds": {
        "md5": "20cf9237d3f49fa65f8790e832cd5342",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gotchaMap/gotchaMapPreview.dds",
        "target": "ba_data/textures/gotchaMapPreview.dds"
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
    points['ffa_spawn1'] = (-8.5184, 0.56928, -1.49458) + (1.22169, 0.05, 1.26353)
    points['ffa_spawn2'] = (8.59355, 0.59544, -1.43799) + (1.20895, 0.05, 1.25724)
    points['ffa_spawn3'] = (-8.54483, 0.5694, 4.72378) + (1.18984, 0.05, 1.29418)
    points['ffa_spawn4'] = (8.70633, 0.5694, 4.74922) + (1.18907, 0.05, 1.26568)
    points['flag1'] = (-9.9261, 1.26464, 1.5577)
    points['flag2'] = (10.02378, 1.32188, 1.59798)
    points['flag_default'] = (0.02873, 2.60659, 1.51861)
    points['powerup_spawn1'] = (-3.93765, 1.08218, -2.33189)
    points['powerup_spawn2'] = (4.12161, 1.14281, -2.33589)
    points['powerup_spawn3'] = (-3.92186, 0.92373, 5.8076)
    points['powerup_spawn4'] = (4.1484, 0.92373, 5.74238)
    points['spawn1'] = (-8.4059, 0.5624, 1.62179) + (0.4613, 0.05, 2.22033)
    points['spawn2'] = (8.46397, 0.58856, 1.70095) + (0.4613, 0.05, 2.22033)
    points['tnt1'] = (0.0275, 0.87995, 1.51592)
    boxes['area_of_interest_bounds'] = (0.36325, 1.10086, 2.99368) + (0, 0, 0) + (28.94068, 14.07879, 14.7444)
    boxes['map_bounds'] = (0.25204, 1.42446, 3.3493) + (0, 0, 0) + (34.76113, 24.79939, 23.84771)
    
    

class GotchaMap(ba.Map):
    defs = Defs()
    name = 'Gotcha'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'gotchaMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('gotchaMap'),
            'collide_model': ba.getcollidemodel('gotchaMapCob'),
            'tex': ba.gettexture('gotchaMapColor'),
            'bgmodel': ba.getmodel('gotchaMapBG'),
            'railing_collide_model': ba.getcollidemodel('gotchaMapRailing')
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
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['tex']
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.8, 0.9, 1.3)
        gnode.ambient_color = (0.8, 0.9, 1.3)
        gnode.vignette_outer = (0.79, 0.79, 0.69)
        gnode.vignette_inner = (0.97, 0.97, 0.99)

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(GotchaMap)
