# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'cragcastleMap'

package_files = {
    "cragCastleBigPreview.ktx": {
        "md5": "85235ee6e75074c3b8dfd77fc8c84fe3",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/cragcastleMap/cragCastleBigPreview.ktx",
        "target": "ba_data/textures/cragCastleBigPreview.ktx"
    },
    "cragCastleLevelBig.bob": {
        "md5": "10975567481e02de6c13f01dd94942c3",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/cragcastleMap/cragCastleLevelBig.bob",
        "target": "ba_data/models/cragCastleLevelBig.bob"
    },
    "cragCastleLevelBottomBig.bob": {
        "md5": "39d5313854efb10054cf26bc9be09919",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/cragcastleMap/cragCastleLevelBottomBig.bob",
        "target": "ba_data/models/cragCastleLevelBottomBig.bob"
    },
    "cragCastleLevelBumperBig.cob": {
        "md5": "37427fc882b0c842f0457a17fb1c2bba",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/cragcastleMap/cragCastleLevelBumperBig.cob",
        "target": "ba_data/models/cragCastleLevelBumperBig.cob"
    },
    "cragCastleBigPreview.dds": {
        "md5": "682fcde82d682f2dabfdad36eca455e2",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/cragcastleMap/cragCastleBigPreview.dds",
        "target": "ba_data/textures/cragCastleBigPreview.dds"
    },
    "cragCastleLevelCollideBig.cob": {
        "md5": "5981bafc0a936e779c0e668af6739327",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/cragcastleMap/cragCastleLevelCollideBig.cob",
        "target": "ba_data/models/cragCastleLevelCollideBig.cob"
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
    # This file generated from "cragCastleBig.ma"
    points = {}
    boxes = {}
    points['ffa_spawn1'] = (-2.22659, 14.63751, 11.52419) + (1.55044, 0.03137, 0.1124)
    points['ffa_spawn2'] = (3.71513, 14.66076, 11.55282) + (1.51546, 0.03137, 0.11228)
    points['ffa_spawn3'] = (3.35989, 15.7454, 9.97398) + (1.01492, 0.03137, 0.11228)
    points['ffa_spawn4'] = (-1.9671, 15.7454, 9.97398) + (1.01492, 0.03137, 0.11228)
    points['ffa_spawn5'] = (-1.20575, 13.62445, 13.76571) + (1.01492, 0.03137, 0.11228)
    points['ffa_spawn6'] = (2.51764, 13.62445, 13.76571) + (1.01492, 0.03137, 0.11228)
    points['flag1'] = (-0.88318, 15.77746, 9.70605)
    points['flag2'] = (2.34138, 15.74996, 9.73634)
    points['flag3'] = (-4.00945, 14.59352, 13.8783)
    points['flag4'] = (5.4491, 14.59501, 13.84305)
    points['flag_default'] = (0.70381, 13.80694, 13.71932)
    points['powerup_spawn1'] = (5.27504, 14.8211, 9.98847)
    points['powerup_spawn2'] = (-0.12894, 14.84951, 9.9409)
    points['powerup_spawn3'] = (1.47447, 14.8553, 9.93446)
    points['powerup_spawn4'] = (-3.87666, 14.91756, 9.90655)
    points['spawn1'] = (-2.93425, 14.63751, 11.52419) + (0.66332, 0.03137, 0.1124)
    points['spawn2'] = (4.20019, 14.66076, 11.55282) + (0.63351, 0.03137, 0.11228)
    points['spawn_by_flag1'] = (-1.49292, 15.77746, 9.95693)
    points['spawn_by_flag2'] = (3.01471, 15.77746, 9.95693)
    points['spawn_by_flag3'] = (-3.85287, 14.61411, 13.37536)
    points['spawn_by_flag4'] = (5.2451, 14.61411, 13.37536)
    points['tnt1'] = (-2.85167, 16.18561, 9.88324)
    points['tnt2'] = (4.20036, 16.18561, 9.88324)
    boxes['area_of_interest_bounds'] = (0.75009, 14.01822, 11.76844) + (0, 0, 0) + (10.49919, 9.37717, 7.27735)
    boxes['map_bounds'] = (0.44951, 15.90257, 11.61652) + (0, 0, 0) + (14.40166, 6.21587, 8.89543)
    

class CragCastleBigMap(ba.Map):
    defs = Defs()
    name = 'Crag Castle Big'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','conquest']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'cragCastleBigPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('cragCastleLevelBig'),
            'bottom_model': ba.getmodel('cragCastleLevelBottomBig'),
            'collide_model': ba.getcollidemodel('cragCastleLevelCollideBig'),
            'tex': ba.gettexture('cragCastleLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'railing_collide_model':
                (ba.getcollidemodel('cragCastleLevelBumperBig')),
            'vr_fill_mound_model': ba.getmodel('cragCastleVRFillMound'),
            'vr_fill_mound_tex': ba.gettexture('vrFillMound')
        }
        # fixme should chop this into vr/non-vr sections
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
        self.bottom = ba.newnode('terrain',
                                 attrs={
                                     'model': self.preloaddata['bottom_model'],
                                     'lighting': False,
                                     'color_texture': self.preloaddata['tex']
                                 })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True
            })
        ba.newnode('terrain',
                   attrs={
                       'model': self.preloaddata['vr_fill_mound_model'],
                       'lighting': False,
                       'vr_only': True,
                       'color': (0.2, 0.25, 0.2),
                       'background': True,
                       'color_texture': self.preloaddata['vr_fill_mound_tex']
                   })
        gnode = ba.getactivity().globalsnode
        gnode.shadow_ortho = True
        gnode.shadow_offset = (0, 0, -5.0)
        gnode.tint = (1.15, 1.05, 0.75)
        gnode.ambient_color = (1.15, 1.05, 0.75)
        gnode.vignette_outer = (0.6, 0.65, 0.6)
        gnode.vignette_inner = (0.95, 0.95, 0.95)
        gnode.vr_near_clip = 1.0

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(CragCastleBigMap)
