# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'arenaminigoreMap'

package_files = {
    "arenaminigoreMapCob.cob": {
        "md5": "fde6e6c61ffe5201dc814eeb97a84418",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/arenaminigoreMap/arenaminigoreMapCob.cob",
        "target": "ba_data/models/arenaminigoreMapCob.cob"
    },
    "arenaminigoreMapColor.dds": {
        "md5": "5380f35794ade00de4cc68de0d6e29ad",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/arenaminigoreMap/arenaminigoreMapColor.dds",
        "target": "ba_data/textures/arenaminigoreMapColor.dds"
    },
    "arenaminigoreMapColor.ktx": {
        "md5": "8588a0ae308f6e04f000eea6ffbdc00c",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/arenaminigoreMap/arenaminigoreMapColor.ktx",
        "target": "ba_data/textures/arenaminigoreMapColor.ktx"
    },
    "arenaminigoreMap.bob": {
        "md5": "42be9c3b8bf3f595d53b8b0223723194",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/arenaminigoreMap/arenaminigoreMap.bob",
        "target": "ba_data/models/arenaminigoreMap.bob"
    },
    "arenaMinigorePreview.dds": {
        "md5": "9eed3b7c488d0ef3738d63445b5ae7e3",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/arenaminigoreMap/arenaMinigorePreview.dds",
        "target": "ba_data/textures/arenaMinigorePreview.dds"
    },
    "arenaMinigorePreview.ktx": {
        "md5": "ad72dd59ac437f0dd3cd89ad073dd185",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/arenaminigoreMap/arenaMinigorePreview.ktx",
        "target": "ba_data/textures/arenaMinigorePreview.ktx"
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
    points['ffa_spawn1'] = (-4.42149, 3.1618, -7.59045) + (3.13882, 0.05, 2.58941)
    points['ffa_spawn2'] = (4.89134, 3.18797, -7.59754) + (3.13385, 0.05, 2.56661)
    points['ffa_spawn3'] = (4.87849, 3.16192, 1.10463) + (3.11134, 0.05, 2.49891)
    points['ffa_spawn4'] = (-4.42791, 3.16192, 1.10463) + (3.12373, 0.05, 2.57577)
    points['flag1'] = (-8.85376, 3.08991, -3.21865)
    points['flag2'] = (9.53636, 3.14715, -3.35611)
    points['flag_default'] = (0.30888, 3.16322, -3.28703)
    points['powerup_spawn1'] = (-4.16659, 3.42372, -6.42749)
    points['powerup_spawn2'] = (4.42687, 3.48435, -6.32974)
    points['powerup_spawn3'] = (-4.20169, 3.26527, 0.44007)
    points['powerup_spawn4'] = (4.75892, 3.26527, 0.34941)
    points['spawn1'] = (-8.35908, 3.1618, -3.16719) + (0.42967, 0.05, 2.68171)
    points['spawn2'] = (8.96465, 3.18797, -3.18894) + (0.42967, 0.05, 2.68171)
    points['tnt1'] = (-7.91677, 3.55083, -10.26691)
    points['tnt2'] = (8.8223, 3.55083, -10.26691)
    points['tnt3'] = (-7.91677, 3.55083, 3.94815)
    points['tnt4'] = (8.8223, 3.55083, 3.94815)
    boxes['area_of_interest_bounds'] = (0.35634, 4.49356, -2.2642) + (0, 0, 0) + (17.33594, 12.05851, 18.50299)
    boxes['map_bounds'] = (0.25894, 4.89966, -3.79786) + (0, 0, 0) + (30.44458, 21.24073, 29.92689)
    

class ArenaMinigore(ba.Map):
    defs = Defs()
    name = 'Hardland Arena'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'arenaMinigorePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('arenaminigoreMap'),
            'collide_model': ba.getcollidemodel('arenaminigoreMapCob'),
            'tex': ba.gettexture('arenaminigoreMapColor')
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
        _map.register_map(ArenaMinigore)
