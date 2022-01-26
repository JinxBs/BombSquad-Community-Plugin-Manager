# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'krustyKrabMap'

package_files = {
    "krustyKrabBGMapColor.ktx": {
        "md5": "33715489d4cc5754d2e91521df0be6f4",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/krustyKrabMap/krustyKrabBGMapColor.ktx",
        "target": "ba_data/textures/krustyKrabBGMapColor.ktx"
    },
    "krustyKrabMap.bob": {
        "md5": "4c46a9d561c5dced7aed232c72dfcc05",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/krustyKrabMap/krustyKrabMap.bob",
        "target": "ba_data/models/krustyKrabMap.bob"
    },
    "krustyKrabBGMapColor.dds": {
        "md5": "2b461c1f4156c489220fad1100cd909b",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/krustyKrabMap/krustyKrabBGMapColor.dds",
        "target": "ba_data/textures/krustyKrabBGMapColor.dds"
    },
    "krustyKrabMapColor.ktx": {
        "md5": "4574504d09c683871c7ad36b55a80f7e",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/krustyKrabMap/krustyKrabMapColor.ktx",
        "target": "ba_data/textures/krustyKrabMapColor.ktx"
    },
    "krustyKrabBGMap.bob": {
        "md5": "85f20afe5b8d6b8dd6c1b668d26ab3b3",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/krustyKrabMap/krustyKrabBGMap.bob",
        "target": "ba_data/models/krustyKrabBGMap.bob"
    },
    "krustyKrabMapPreview.ktx": {
        "md5": "fdb37b5db63f2018c55fd72a9e98009e",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/krustyKrabMap/krustyKrabMapPreview.ktx",
        "target": "ba_data/textures/krustyKrabMapPreview.ktx"
    },
    "krustyKrabMapPreview.dds": {
        "md5": "171854a77bf1ae688cc6d3f5d01d4114",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/krustyKrabMap/krustyKrabMapPreview.dds",
        "target": "ba_data/textures/krustyKrabMapPreview.dds"
    },
    "krustyKrabMapColor.dds": {
        "md5": "ce0a8641a8ecd248ffd6b03f1e606638",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/krustyKrabMap/krustyKrabMapColor.dds",
        "target": "ba_data/textures/krustyKrabMapColor.dds"
    },
    "krustyKrabMapCob.cob": {
        "md5": "d5087aa84f1aff77302d9da64d59a049",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/krustyKrabMap/krustyKrabMapCob.cob",
        "target": "ba_data/models/krustyKrabMapCob.cob"
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
    points['ffa_spawn1'] = (-6.22221, 4.04595, -2.42887) + (1.00304, 0.05, 0.67435)
    points['ffa_spawn2'] = (4.34829, 4.04595, -2.42887) + (1.00304, 0.05, 0.67435)
    points['ffa_spawn3'] = (-6.12272, 4.04595, 5.08241) + (1.00304, 0.05, 0.67435)
    points['ffa_spawn4'] = (5.56701, 4.04595, 4.95805) + (1.00304, 0.05, 0.67435)
    points['flag1'] = (-9.61277, 4.30876, 1.45718)
    points['flag2'] = (9.17461, 4.366, 1.29792)
    points['flag_default'] = (-0.63318, 4.38208, 0.99473)
    points['powerup_spawn1'] = (-6.38018, 4.40338, 0.61122)
    points['powerup_spawn2'] = (4.2279, 4.43021, 0.55974)
    points['powerup_spawn3'] = (-0.37144, 4.36881, 4.96673)
    points['powerup_spawn4'] = (-0.78748, 4.35755, -1.71495)
    points['spawn1'] = (-9.71476, 4.06156, 2.26422) + (0.46069, 0.05, 1.22664)
    points['spawn2'] = (9.51737, 4.08772, 2.20081) + (0.46069, 0.05, 1.22664)
    points['tnt1'] = (-1.32497, 4.77605, -4.34548)
    boxes['area_of_interest_bounds'] = (-0.19385, 4.69839, 1.34427) + (0, 0, 0) + (25.75767, 18.8136, 10.50299)
    boxes['map_bounds'] = (0.10981, 5.1045, -1.04853) + (0, 0, 0) + (57.5275, 33.13962, 29.92689)
    

class KrustyKrabMap(ba.Map):
    defs = Defs()
    name = 'Krusty Krab'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill','race']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'krustyKrabMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('krustyKrabMap'),
            'collide_model': ba.getcollidemodel('krustyKrabMapCob'),
            'tex': ba.gettexture('krustyKrabMapColor'),
            'bgtex': ba.gettexture('krustyKrabBGMapColor'),
            'bgmodel': ba.getmodel('krustyKrabBGMap')
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
        gnode.tint = (1.15, 1.11, 1.03)
        gnode.ambient_color = (1.2, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.73, 0.7)
        gnode.vignette_inner = (0.95, 0.95, 0.95)

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(KrustyKrabMap)
