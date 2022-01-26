# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'hwMap'

package_files = {
    "hwMap.bob": {
        "md5": "bcd81762eaae80061dfe8655b3e779be",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/hwMap/hwMap.bob",
        "target": "ba_data/models/hwMap.bob"
    },
    "hwMapColor.ktx": {
        "md5": "f51257bf0ceb9a86fd604475a99ff197",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/hwMap/hwMapColor.ktx",
        "target": "ba_data/textures/hwMapColor.ktx"
    },
    "hwMapCob.cob": {
        "md5": "85c3a8957a74b4ec01686ce763a62787",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/hwMap/hwMapCob.cob",
        "target": "ba_data/models/hwMapCob.cob"
    },
    "hwMapPreview.dds": {
        "md5": "42fdcfb32000277ab05ab59ae26c6ffc",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/hwMap/hwMapPreview.dds",
        "target": "ba_data/textures/hwMapPreview.dds"
    },
    "hwMapColor.dds": {
        "md5": "c54b4d09c9e3b9fab95f8ce1fc0ee62d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/hwMap/hwMapColor.dds",
        "target": "ba_data/textures/hwMapColor.dds"
    },
    "hwMapPreview.ktx": {
        "md5": "d2b1daeb416f96907c65c5cd0518fdb9",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/hwMap/hwMapPreview.ktx",
        "target": "ba_data/textures/hwMapPreview.ktx"
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
    points['ffa_spawn1'] = (-3.21939, 4.36361, -20.48689) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn10'] = (6.11609, 4.53849, -18.89968) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn11'] = (8.65855, 4.75483, -16.74401) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn12'] = (10.50375, 5.01777, -8.63663) + (0.55372, 0.05, 5.43854)
    points['ffa_spawn13'] = (9.58738, 4.93388, -0.37638) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn14'] = (7.64953, 4.91408, 1.82044) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn15'] = (5.01917, 4.93212, 2.20499) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn16'] = (-0.0325, 3.14097, 2.10002) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn2'] = (-6.24933, 4.53849, -18.89968) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn3'] = (-8.65944, 4.75483, -16.74401) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn4'] = (-10.56597, 5.01777, -8.63663) + (0.55372, 0.05, 5.43854)
    points['ffa_spawn5'] = (-9.80749, 4.93388, -0.37638) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn6'] = (-7.87914, 4.91408, 1.82044) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn7'] = (-5.10961, 4.93212, 2.20499) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn8'] = (-0.0325, 3.14097, 2.10002) + (0.55372, 0.05, 0.52935)
    points['ffa_spawn9'] = (3.20042, 4.36361, -20.48689) + (0.55372, 0.05, 0.52935)
    points['flag1'] = (-8.62451, 4.24695, -7.51276)
    points['flag2'] = (8.59073, 4.17493, -7.4768)
    points['flag_default'] = (-0.04391, 4.97167, -20.18156)
    points['powerup_spawn1'] = (8.45206, 4.24325, -12.30868)
    points['powerup_spawn2'] = (-8.11399, 4.27517, -12.19911)
    points['powerup_spawn3'] = (-8.23795, 4.23112, -3.28173)
    points['powerup_spawn4'] = (8.14943, 4.24283, -2.71368)
    points['spawn1'] = (-10.5791, 4.84945, -7.53411) + (0.50029, 0.05, 3.20865)
    points['spawn2'] = (10.51234, 4.84931, -7.51627) + (0.48792, 0.05, 3.2029)
    points['tnt1'] = (0.44224, 2.83063, -11.26023)
    points['tnt2'] = (-0.66255, 2.81362, -3.3946)
    boxes['area_of_interest_bounds'] = (0.08641, 4.39067, -7.46992) + (0, 0, 0) + (51.08173, 54.97659, 42.52111)
    boxes['map_bounds'] = (-0.10175, 5.00256, -12.05441) + (0, 0, 0) + (58.81755, 63.49395, 45.09238)
    
    

class Halloween(ba.Map):
    defs = Defs()
    name = 'Halloween'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'hwMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('hwMap'),
            'collide_model': ba.getcollidemodel('hwMapCob'),
            'tex': ba.gettexture('hwMapColor')
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
        gnode.tint = (0.8, 0.9, 1.3)
        gnode.ambient_color = (0.8, 0.9, 1.3)
        gnode.vignette_outer = (0.79, 0.79, 0.69)
        gnode.vignette_inner = (0.97, 0.97, 0.99)

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(Halloween)
