# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'bombermanMap'

package_files = {
    "bombermanMapColor.dds": {
        "md5": "ed7911ea9b23cea1c2044b27bc8a413c",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bombermanMap/bombermanMapColor.dds",
        "target": "ba_data/textures/bombermanMapColor.dds"
    },
    "bombermanMapPreview.ktx": {
        "md5": "0d8579bcf5169588f23ff18b6d0c2338",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bombermanMap/bombermanMapPreview.ktx",
        "target": "ba_data/textures/bombermanMapPreview.ktx"
    },
    "bombermanMapPreview.dds": {
        "md5": "297df338402bea9c49c4b7ff5ba0c593",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bombermanMap/bombermanMapPreview.dds",
        "target": "ba_data/textures/bombermanMapPreview.dds"
    },
    "bombermanMapCob.cob": {
        "md5": "7a0ce7caf64821e04fbebdd32075ebc0",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bombermanMap/bombermanMapCob.cob",
        "target": "ba_data/models/bombermanMapCob.cob"
    },
    "bombermanMapColor.ktx": {
        "md5": "9475047324957a7270143a173f71d2a9",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bombermanMap/bombermanMapColor.ktx",
        "target": "ba_data/textures/bombermanMapColor.ktx"
    },
    "bombermanMap.bob": {
        "md5": "b1e809656e200056a1f5df9fbcac1c6f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/bombermanMap/bombermanMap.bob",
        "target": "ba_data/models/bombermanMap.bob"
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
    points['ffa_spawn1'] = (-6.67542, 3.68439, -5.53375) + (0.36007, 0.02575, 0.9315)
    points['ffa_spawn2'] = (-7.2624, 3.71553, -0.03071) + (0.51265, 0.02934, 1.58911)
    points['ffa_spawn3'] = (7.19605, 3.71931, -5.43993) + (0.30604, 0.05, 0.97874)
    points['ffa_spawn4'] = (7.7071, 3.71969, -0.02085) + (0.48506, 0.05, 1.59702)
    points['flag1'] = (-5.53975, 4.90844, -1.29316)
    points['flag2'] = (6.03798, 4.86734, -1.2541)
    points['flag_default'] = (0.25697, 4.91175, -1.23932)
    points['powerup_spawn1'] = (-4.26423, 4.15187, -2.68368)
    points['powerup_spawn2'] = (4.7916, 4.12509, -2.73491)
    points['powerup_spawn3'] = (-4.29883, 4.12305, 0.08537)
    points['powerup_spawn4'] = (4.8075, 4.13938, 0.12609)
    points['spawn1'] = (-7.28662, 3.70478, -1.38929) + (0.51458, 0.05, 1.70728)
    points['spawn2'] = (7.72787, 3.75089, -0.76991) + (0.52971, 0.05, 2.20823)
    points['tnt1'] = (0.32876, 3.96425, -6.16745)
    boxes['area_of_interest_bounds'] = (0.64605, 8.43146, 1.88631) + (0, 0, 0) + (12.56183, 9.47264, 10.65585)
    boxes['map_bounds'] = (0.56149, 10.49611, -2.47924) + (0, 0, 0) + (22.0605, 16.68579, 17.23487)
    

class BombermanMap(ba.Map):
    defs = Defs()
    name = 'BombermanMap'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'bombermanMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('bombermanMap'),
            'collide_model': ba.getcollidemodel('bombermanMapCob'),
            'tex': ba.gettexture('bombermanMapColor')
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

        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.1, 1.0)
        gnode.ambient_color = (1.1, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(BombermanMap)
