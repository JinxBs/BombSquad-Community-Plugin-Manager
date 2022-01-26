# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'pacmanMap'

package_files = {
    "pacmanMapPreview.dds": {
        "md5": "b5b99904392f574f7f799e8d64c3b7c6",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/pacmanMap/pacmanMapPreview.dds",
        "target": "ba_data/textures/pacmanMapPreview.dds"
    },
    "pacmanMap.bob": {
        "md5": "c3123b22e06547968b6ec5d6c6986a0f",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/pacmanMap/pacmanMap.bob",
        "target": "ba_data/models/pacmanMap.bob"
    },
    "pacmanMapColor.ktx": {
        "md5": "4c622b279250158afcfe9137a8d8b11a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/pacmanMap/pacmanMapColor.ktx",
        "target": "ba_data/textures/pacmanMapColor.ktx"
    },
    "pacmanMapColor.dds": {
        "md5": "4c797309320a6d8e6426ae5534e7a140",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/pacmanMap/pacmanMapColor.dds",
        "target": "ba_data/textures/pacmanMapColor.dds"
    },
    "pacmanMapPreview.ktx": {
        "md5": "1c2bf698b76cd05157b75d14cd84d6ac",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/pacmanMap/pacmanMapPreview.ktx",
        "target": "ba_data/textures/pacmanMapPreview.ktx"
    },
    "pacmanMapCob.cob": {
        "md5": "47843aac9f607568e9cb087302984088",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/pacmanMap/pacmanMapCob.cob",
        "target": "ba_data/models/pacmanMapCob.cob"
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
    # This file generated from "pacmanMap.ma"
    points = {}
    boxes = {}
    points['ffa_spawn1'] = (-9.67927, 0.58588, -7.13608) + (0.65447, 0.05, 0.58413)
    points['ffa_spawn2'] = (8.08484, 0.58588, 5.82097) + (0.71956, 0.05, 0.64222)
    points['ffa_spawn3'] = (-8.18949, 0.58588, 5.81325) + (0.65447, 0.05, 0.58413)
    points['ffa_spawn4'] = (9.5672, 0.58588, -7.12513) + (0.71956, 0.05, 0.64222)
    points['flag1'] = (-0.01855, 0.91513, 9.92087)
    points['flag2'] = (-0.05367, 0.92024, -7.16025)
    points['flag_default'] = (-0.05154, 0.99034, -0.74039)
    points['powerup_spawn1'] = (-9.6929, 0.93028, -8.68649)
    points['powerup_spawn2'] = (9.59894, 0.93028, -8.60753)
    points['powerup_spawn3'] = (-9.72155, 0.93028, 5.58694)
    points['powerup_spawn4'] = (9.72079, 0.93028, 5.6272)
    points['powerup_spawn5'] = (-0.01869, 0.93028, 1.34941)
    points['spawn1'] = (-0.01986, 0.77565, 9.98158) + (3.94253, 0.05, 0.38847)
    points['spawn2'] = (-0.05893, 0.77565, -7.1692) + (3.90012, 0.05, 0.3592)
    points['tnt1'] = (-1.42239, 0.98812, -0.69979)
    points['tnt2'] = (1.40068, 0.98811, -0.77369)
    boxes['area_of_interest_bounds'] = (-0.08534, 2.76726, 2.09197) + (0, 0, 0) + (14.50743, 14.58622, 28.3354)
    boxes['map_bounds'] = (-0.0229, 9.33466, -0.52407) + (0, 0, 0) + (21.48431, 18.8591, 22.6373)

class PortalPM(ba.Actor):
    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 position2: Sequence[float] = (0.0, 1.0, 0.0),
                 color: Sequence[float] = (1.0, 1.0, 1.0)):
        super().__init__()
        shared = SharedObjects.get()

        self.radius = 1.1
        self.position = position
        self.position2 = position2
        self.cooldown = False

        self.portalmaterial = ba.Material()
        self.portalmaterial.add_actions(
            conditions=(
                ('they_have_material', shared.player_material)
            ),
            actions=(('modify_part_collision','collide',True),
                     ('modify_part_collision','physical',False),
                     ('call','at_connect', self.portal)),
        )

        self.portalmaterial.add_actions(
            conditions=(
                ('they_have_material', shared.object_material),
                'or',
                ('they_dont_have_material', shared.player_material),
            ),
            actions=(('modify_part_collision','collide',True),
                     ('modify_part_collision','physical',False),
                     ('call','at_connect', self.objportal)),
        )

        self.node = ba.newnode(
            'region',
            attrs={'position':(self.position[0],
                               self.position[1],
                               self.position[2]),
                   'scale':(0.1,0.1,0.1),
                   'type':'sphere',
                   'materials':[self.portalmaterial]}
        )
        ba.animate_array(self.node, 'scale', 3,
                        {0: (0,0,0), 0.5: (self.radius,
                                           self.radius,
                                           self.radius)})

        self.portal2material = ba.Material()
        self.portal2material.add_actions(
            conditions=(
                ('they_have_material', shared.player_material)
            ),
            actions=(('modify_part_collision','collide',True),
                     ('modify_part_collision','physical',False),
                     ('call','at_connect', self.portal2)),
        )

        self.portal2material.add_actions(
            conditions=(
                ('they_have_material', shared.object_material),
                'or',
                ('they_dont_have_material', shared.player_material),
            ),
            actions=(('modify_part_collision','collide',True),
                     ('modify_part_collision','physical',False),
                     ('call','at_connect', self.objportal2)),
        )

        self.node2 = ba.newnode(
            'region',
            attrs={'position':(self.position2[0],
                               self.position2[1],
                               self.position2[2]),
                   'scale':(0.1,0.1,0.1),
                   'type':'sphere',
                   'materials':[self.portal2material]}
        )
        ba.animate_array(self.node2, 'scale', 3,
                        {0: (0,0,0), 0.5: (self.radius,
                                           self.radius,
                                           self.radius)})

    def cooldown1(self):
        self.cooldown = True
        def off():
            self.cooldown = False
        ba.timer(0.01, off)

    def portal(self):
        sound = ba.getsound('powerup01')
        ba.playsound(sound)
        node = ba.getcollision().opposingnode
        node.handlemessage(ba.StandMessage(self.node2.position))

    def portal2(self):
        sound = ba.getsound('powerup01')
        ba.playsound(sound)
        node = ba.getcollision().opposingnode
        node.handlemessage(ba.StandMessage(self.node.position))

    def objportal(self):
        node = ba.getcollision().opposingnode
        if node.getnodetype() == 'spaz':
            return
        v = node.velocity
        if not self.cooldown:
            node.position = self.position2
            self.cooldown1()
        def vel():
            node.velocity = v
        ba.timer(0.01, vel)

    def objportal2(self):
        node = ba.getcollision().opposingnode
        if node.getnodetype() == 'spaz':
            return
        v = node.velocity
        if not self.cooldown:
            node.position = self.position
            self.cooldown1()
        def vel():
            node.velocity = v
        ba.timer(0.01, vel)

class PacMan(ba.Map):
    defs = Defs()
    name = 'PAC-MAN'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'pacmanMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('pacmanMap'),
            'collide_model': ba.getcollidemodel('pacmanMapCob'),
            'tex': ba.gettexture('pacmanMapColor')
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
        gnode.tint = (1.3, 1.2, 1.0)
        gnode.ambient_color = (1.3, 1.2, 1.0)
        gnode.vignette_outer = (0.57, 0.57, 0.57)
        gnode.vignette_inner = (0.9, 0.9, 0.9)
        gnode.vr_camera_offset = (0.0, -4.2, -1.1)
        gnode.vr_near_clip = 0.5

        PortalPM(position=(-10.2929, 0.1028, -0.68649),
                 position2=(10.2929, 0.1028, -0.68649),
                 color=(3,0,9))

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(PacMan)
