# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'mbwMap'

package_files = {
    "mbwMapPreview.dds": {
        "md5": "6c6d7062799de2b898a2c674e3ffb314",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mbwMap/mbwMapPreview.dds",
        "target": "ba_data/textures/mbwMapPreview.dds"
    },
    "mbw.bob": {
        "md5": "9e691e5f440fda84ca62337d39e55fba",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mbwMap/mbw.bob",
        "target": "ba_data/models/mbw.bob"
    },
    "mbwColor.ktx": {
        "md5": "5278e9c816df915c26ade9e8385689ed",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mbwMap/mbwColor.ktx",
        "target": "ba_data/textures/mbwColor.ktx"
    },
    "mbwMapPreview.ktx": {
        "md5": "77b9229478fce80db42a095eb8006b41",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mbwMap/mbwMapPreview.ktx",
        "target": "ba_data/textures/mbwMapPreview.ktx"
    },
    "mbwCob.cob": {
        "md5": "2d043b3b0f79d8702db2a4e2c4207895",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mbwMap/mbwCob.cob",
        "target": "ba_data/models/mbwCob.cob"
    },
    "mbwColor.dds": {
        "md5": "cf23e23848984494b2bf66e72687a5ff",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/mbwMap/mbwColor.dds",
        "target": "ba_data/textures/mbwColor.dds"
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
    points['ffa_spawn1'] = (3.151, 3.28557, -11.62294) + (0.78108, 0.05, 0.78913)
    points['ffa_spawn2'] = (-3.89813, 3.28557, -11.61621) + (0.77292, 0.05, 0.79949)
    points['ffa_spawn3'] = (-8.91371, 3.28557, -6.39059) + (0.76822, 0.05, 0.78687)
    points['ffa_spawn4'] = (-8.91988, 3.28557, 0.39817) + (0.77204, 0.05, 0.78333)
    points['ffa_spawn5'] = (-3.91388, 3.28557, 5.41779) + (0.7682, 0.05, 0.77865)
    points['ffa_spawn6'] = (3.13084, 3.28557, 5.42816) + (0.76469, 0.05, 0.80429)
    points['ffa_spawn7'] = (8.00649, 3.28557, 0.39817) + (0.76822, 0.05, 0.78687)
    points['ffa_spawn8'] = (7.9949, 3.28557, -6.39856) + (0.76689, 0.05, 0.7936)
    points['flag1'] = (5.29873, 4.46068, -8.91326)
    points['flag2'] = (5.29841, 4.46068, 2.67068)
    points['flag3'] = (-6.0173, 4.46068, 2.64588)
    points['flag4'] = (-6.00445, 4.46068, -8.91204)
    points['flag_default'] = (-0.32485, 4.64644, -2.97299)
    points['powerup_spawn1'] = (5.4662, 3.62173, -3.13033)
    points['powerup_spawn2'] = (-0.30004, 3.62173, -8.9136)
    points['powerup_spawn3'] = (-6.17938, 3.62173, -3.12631)
    points['powerup_spawn4'] = (-0.30531, 3.62173, 2.94049)
    points['spawn1'] = (9.04137, 3.02487, -2.90355) + (1.29071, 0.05, 1.91677)
    points['spawn2'] = (-9.729, 3.02487, -2.95026) + (1.29071, 0.05, 1.91677)
    points['spawn_by_flag1'] = (7.94788, 3.01322, -8.88789) + (0.75187, 0.05, 0.84538)
    points['spawn_by_flag2'] = (-8.87075, 3.01322, -8.93492) + (0.75187, 0.05, 0.84538)
    points['spawn_by_flag3'] = (-8.91571, 3.01322, 2.8066) + (0.75187, 0.05, 0.84538)
    points['spawn_by_flag4'] = (8.07702, 3.01322, 2.84106) + (0.75187, 0.05, 0.84538)
    points['tnt1'] = (3.16319, 3.31034, -6.37489)
    points['tnt2'] = (-3.86491, 3.31034, -6.42483)
    points['tnt3'] = (-3.83403, 3.31034, 0.45535)
    points['tnt4'] = (3.1593, 3.31034, 0.56443)
    boxes['area_of_interest_bounds'] = (0.35441, 0.15553, 0.02918) + (0, 0, 0) + (20.65136, 23.83756, 18.50299)
    boxes['map_bounds'] = (0.26088, 7.08896, -3.08543) + (0, 0, 0) + (29.00671, 28.73445, 27.12031)
    
    
    
    

class MarioWorldMap(ba.Map):
    defs = Defs()
    name = 'Mario Bros World'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill','conquest']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'mbwMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('mbw'),
            'collide_model': ba.getcollidemodel('mbwCob'),
            'tex': ba.gettexture('mbwColor'),
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

    def is_point_near_edge(self,
                           point: ba.Vec3,
                           running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(MarioWorldMap)
