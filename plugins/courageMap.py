# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'courageMap'

package_files = {
    "courageBGColor.ktx": {
        "md5": "f8b40a6652e3c4676c9a5a993e3da888",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/courageMap/courageBGColor.ktx",
        "target": "ba_data/textures/courageBGColor.ktx"
    },
    "courageMapColor.ktx": {
        "md5": "55d4cb427671307b3f079c6f17970e7f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/courageMap/courageMapColor.ktx",
        "target": "ba_data/textures/courageMapColor.ktx"
    },
    "courageMap.bob": {
        "md5": "d4e13d0902a6bc94a5ec4582e685f432",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/courageMap/courageMap.bob",
        "target": "ba_data/models/courageMap.bob"
    },
    "courageMapPreview.dds": {
        "md5": "302a82c26f15d76d41a021b503cfbed4",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/courageMap/courageMapPreview.dds",
        "target": "ba_data/textures/courageMapPreview.dds"
    },
    "courageMapPreview.ktx": {
        "md5": "82ce6089d43c51bc49b70c1a2ec0410b",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/courageMap/courageMapPreview.ktx",
        "target": "ba_data/textures/courageMapPreview.ktx"
    },
    "courageBGColor.dds": {
        "md5": "7a1f36e515db763dbbc4dd964862c85b",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/courageMap/courageBGColor.dds",
        "target": "ba_data/textures/courageBGColor.dds"
    },
    "courageMapColor.dds": {
        "md5": "bab38b7ec1008e18e4725f80eec55010",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/courageMap/courageMapColor.dds",
        "target": "ba_data/textures/courageMapColor.dds"
    },
    "courageMapCob.cob": {
        "md5": "855b2aed970c961d11614e2445ad49b9",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/courageMap/courageMapCob.cob",
        "target": "ba_data/models/courageMapCob.cob"
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
    points['ffa_spawn1'] = (-6.5205, 1.13883, 4.19109) + (0.4868, 0.05, 1.25935)
    points['ffa_spawn2'] = (8.78868, 1.18093, -2.49017) + (0.69308, 0.05, 2.14841)
    points['ffa_spawn3'] = (8.22231, 1.18604, 4.1369) + (0.41375, 0.05, 1.32322)
    points['ffa_spawn4'] = (-6.39927, 1.18655, -2.2972) + (0.65578, 0.05, 2.1591)
    points['flag1'] = (-6.40246, 1.4649, -0.18825)
    points['flag2'] = (8.6688, 1.40934, -0.34307)
    points['flag_default'] = (1.10226, 1.46938, 3.37262)
    points['powerup_spawn1'] = (-2.72635, 1.43864, -2.69105)
    points['powerup_spawn2'] = (4.57531, 1.40244, -2.55269)
    points['powerup_spawn3'] = (-2.5655, 1.39968, 5.91099)
    points['powerup_spawn4'] = (4.63833, 1.42176, 5.88299)
    points['spawn1'] = (-6.43877, 1.1664, -2.26988) + (0.69569, 0.05, 2.30817)
    points['spawn2'] = (8.71112, 1.1533, -2.47063) + (0.71615, 0.05, 2.35914)
    points['tnt1'] = (-7.47936, 1.51719, 1.60992)
    points['tnt2'] = (9.08903, 1.52706, 1.56156)
    boxes['area_of_interest_bounds'] = (0.59016, 0.74947, 3.06926) + (0, 0, 0) + (16.98306, 12.80661, 14.40626)
    boxes['edge_box'] = (1.01079, 3.81195, -0.03497) + (0, 0, 0) + (9.46205, 7.07351, 5.54318)
    boxes['map_bounds'] = (0.47584, 3.54079, -2.83278) + (0, 0, 0) + (29.82487, 22.55849, 23.30082)
    

class CourageMap(ba.Map):
    defs = Defs()
    name = 'Courage'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'courageMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('courageMap'),
            'collide_model': ba.getcollidemodel('courageMapCob'),
            'tex': ba.gettexture('courageMapColor'),
            'bgtex': ba.gettexture('courageBGColor'),
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

    def is_point_near_edge(self,
                           point: ba.Vec3,
                           running: bool = False) -> bool:
        # count anything off our ground level as safe (for our platforms)
        # see if we're within edge_box
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(CourageMap)
