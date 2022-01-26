# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'eliminationChamberRaw'

package_files = {
    "ecMapColor.dds": {
        "md5": "0d7345db0bda49b6d2ab80d5e1b71f0b",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecMapColor.dds",
        "target": "ba_data/textures/ecMapColor.dds"
    },
    "ecBGMap.bob": {
        "md5": "a5bd0d85133a86c06bf74a6bbfdc1c34",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecBGMap.bob",
        "target": "ba_data/models/ecBGMap.bob"
    },
    "ecGlassMapCob.cob": {
        "md5": "755b6838f3d4bbfe0447659878b437d5",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecGlassMapCob.cob",
        "target": "ba_data/models/ecGlassMapCob.cob"
    },
    "ecRawMapPreview.dds": {
        "md5": "160cdf0558238e15de168a3ec178da89",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecRawMapPreview.dds",
        "target": "ba_data/textures/ecRawMapPreview.dds"
    },
    "ecRawNLMap.bob": {
        "md5": "1616ad9e25600473cdb75954aaa3037a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecRawNLMap.bob",
        "target": "ba_data/models/ecRawNLMap.bob"
    },
    "ecRawMapPreview.ktx": {
        "md5": "2096ea7ccc79b5634b210b67fa4f254d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecRawMapPreview.ktx",
        "target": "ba_data/textures/ecRawMapPreview.ktx"
    },
    "ecRawInvMap.bob": {
        "md5": "54a556e9e62c185c03c65acb41e4b31d",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecRawInvMap.bob",
        "target": "ba_data/models/ecRawInvMap.bob"
    },
    "ecMapColor.ktx": {
        "md5": "01e33af58c380fef2b840ed9ce23073b",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecMapColor.ktx",
        "target": "ba_data/textures/ecMapColor.ktx"
    },
    "ecMapCob.cob": {
        "md5": "86d05e5a6a2c7ee168372a5779961051",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecMapCob.cob",
        "target": "ba_data/models/ecMapCob.cob"
    },
    "ecRawMap.bob": {
        "md5": "8fc840ea238849d53f761a0a2ddd7d20",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecRawMap.bob",
        "target": "ba_data/models/ecRawMap.bob"
    },
    "ecExtMap.bob": {
        "md5": "224b883703dc352fd550a8139e650c51",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecExtMap.bob",
        "target": "ba_data/models/ecExtMap.bob"
    },
    "ecRawGlassMap.bob": {
        "md5": "3f943556b4f9691c5ca182ee394735cc",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecRawGlassMap.bob",
        "target": "ba_data/models/ecRawGlassMap.bob"
    },
    "ecExtMapCob.cob": {
        "md5": "389a191ae68cabcc63886f05cec4c2d0",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/eliminationChamberRaw/ecExtMapCob.cob",
        "target": "ba_data/models/ecExtMapCob.cob"
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
    points['ffa_spawn1'] = (-5.73834, 2.80152, -8.8294) + (0.16326, 0.05, 1.17729)
    points['ffa_spawn2'] = (6.29593, 2.82769, -8.84425) + (1.17571, 0.05, 0.19976)
    points['ffa_spawn3'] = (-5.73994, 2.80164, 3.14882) + (0.1102, 0.05, 1.11355)
    points['ffa_spawn4'] = (6.28908, 2.80164, 3.1914) + (1.10532, 0.05, 0.1034)
    points['flag1'] = (-6.75103, 3.00062, -2.80413)
    points['flag2'] = (7.09391, 3.02284, -2.94835)
    points['flag_default'] = (0.27249, 4.38208, -2.93376)
    points['powerup_spawn1'] = (-6.64437, 3.08947, -6.27667)
    points['powerup_spawn2'] = (-3.48047, 3.15009, -9.86327)
    points['powerup_spawn3'] = (4.13658, 2.93102, -9.85887)
    points['powerup_spawn4'] = (7.40907, 2.93102, -6.63147)
    points['powerup_spawn5'] = (7.40355, 3.19542, 0.85875)
    points['powerup_spawn6'] = (4.10369, 3.08724, 4.3101)
    points['powerup_spawn7'] = (-3.61995, 3.09165, 4.27063)
    points['powerup_spawn8'] = (-6.81122, 3.13612, 0.9741)
    points['spawn1'] = (-5.47127, 2.70749, -0.86437) + (1.29739, 0.05, 0.87378)
    points['spawn2'] = (6.18423, 2.73365, -4.87303) + (1.3172, 0.05, 0.87378)
    boxes['area_of_interest_bounds'] = (0.35441, 2.49356, -2.51839) + (0, 0, 0) + (16.64755, 8.06139, 22.50299)
    boxes['map_bounds'] = (0.26088, 4.89966, -3.54367) + (0, 0, 0) + (29.23565, 14.19991, 29.92689)
    

class EliminationRawMap(ba.Map):
    defs = Defs()
    name = 'Elimination Chamber - Raw'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill','wwe']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'ecRawMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('ecRawMap'),
            'collide_model': ba.getcollidemodel('ecMapCob'),
            'modeli': ba.getmodel('ecRawInvMap'),
            'modelnl': ba.getmodel('ecRawNLMap'),
            'modelg': ba.getmodel('ecRawGlassMap'),
            'collide_modelg': ba.getcollidemodel('ecGlassMapCob'),
            'modele': ba.getmodel('ecExtMap'),
            'collide_modele': ba.getcollidemodel('ecExtMapCob'),
            'tex': ba.gettexture('ecMapColor'),
            'bgmodel': ba.getmodel('ecBGMap')
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
        self.nodenl = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'lighting': False,
                'model': self.preloaddata['modelnl'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.nodei = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'opacity': 0.05,
                'model': self.preloaddata['modeli'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.nodeg = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_modelg'],
                'model': self.preloaddata['modelg'],
                'color_texture': self.preloaddata['tex'],
                'lighting': False,
                'opacity': 0.2,
                'materials': [shared.footing_material]
            })
        self.nodee = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_modele'],
                'model': self.preloaddata['modele'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
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
        gnode.tint = (1.1, 1.1, 1.0)
        gnode.ambient_color = (1.1, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(EliminationRawMap)
