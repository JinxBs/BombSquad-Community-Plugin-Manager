# ba_meta require api 6
from __future__ import annotations
import ba, _ba
from ba import _map
from bastd.gameutils import SharedObjects
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

package_name = 'gravityFallsMap'

package_files = {
    "gravityFallsMap.bob": {
        "md5": "8835ac3225f7f79fd239d55968f52dc1",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gravityFallsMap/gravityFallsMap.bob",
        "target": "ba_data/models/gravityFallsMap.bob"
    },
    "gravityFallsMapCob.cob": {
        "md5": "eab0568aff3978e0c79bcc0b4e5d4462",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gravityFallsMap/gravityFallsMapCob.cob",
        "target": "ba_data/models/gravityFallsMapCob.cob"
    },
    "gravityFallsMapD.bob": {
        "md5": "d280b120b35af472e163a4d7a054c2aa",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gravityFallsMap/gravityFallsMapD.bob",
        "target": "ba_data/models/gravityFallsMapD.bob"
    },
    "gravityFallsMapColor.ktx": {
        "md5": "0cfddb31c4c4834d982b56e33e6b6e1b",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gravityFallsMap/gravityFallsMapColor.ktx",
        "target": "ba_data/textures/gravityFallsMapColor.ktx"
    },
    "gravityFallsMapPreview.dds": {
        "md5": "8d1be1942ef3f01b90ee2932ac757151",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gravityFallsMap/gravityFallsMapPreview.dds",
        "target": "ba_data/textures/gravityFallsMapPreview.dds"
    },
    "gravityFallsMapColor.dds": {
        "md5": "adfc0b76353a860bc8352d709c4f116a",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gravityFallsMap/gravityFallsMapColor.dds",
        "target": "ba_data/textures/gravityFallsMapColor.dds"
    },
    "gravityFallsMapPreview.ktx": {
        "md5": "b225a5dac315a2c9e68b444659f0bc64",
        "url": "https://raw.githubusercontent.com/JinxBs/BombSquad-Community-Plugin-Manager/main/Maps/gravityFallsMap/gravityFallsMapPreview.ktx",
        "target": "ba_data/textures/gravityFallsMapPreview.ktx"
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
    points['ffa_spawn1'] = (-6.97783, 2.05753, -4.75154) + (1.4663, 0.05, 0.87378)
    points['ffa_spawn2'] = (7.28045, 2.0837, -5.7546) + (1.67437, 0.05, 0.87378)
    points['ffa_spawn3'] = (12.50401, 2.04888, -1.16587) + (0.48506, 0.05, 1.59702)
    points['ffa_spawn4'] = (-10.66812, 2.04888, 1.1377) + (0.48506, 0.05, 1.59702)
    points['flag1'] = (-12.62698, 3.02028, -2.23155)
    points['flag2'] = (11.71206, 2.51231, -4.23504)
    points['flag_default'] = (0.16225, 2.56307, -1.87058)
    points['powerup_spawn1'] = (-8.4451, 2.39672, -2.23429)
    points['powerup_spawn2'] = (5.24553, 2.45735, 2.6822)
    points['powerup_spawn3'] = (-13.7492, 2.43847, 2.63631)
    points['powerup_spawn4'] = (11.17395, 2.43847, -6.65691)
    points['spawn1'] = (-12.93303, 2.01032, 0.78771) + (1.6634, 0.05, 0.87378)
    points['spawn2'] = (13.39258, 2.03649, -1.57687) + (1.6634, 0.05, 0.87378)
    points['tnt1'] = (-4.29628, 2.48705, -10.83656)
    boxes['area_of_interest_bounds'] = (-1.0776, 2.93491, -2.53375) + (0, 0, 0) + (46.36258, 11.84662, 21.07336)
    boxes['map_bounds'] = (-1.22571, 3.39742, -4.04047) + (0, 0, 0) + (46.29672, 20.86748, 34.08423)

class PortalGF(ba.Actor):
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
                        {0: (0,0,0), 0.5: (self.radius*5,
                                           self.radius*5,
                                           self.radius*5)})

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
                        {0: (0,0,0), 0.5: (self.radius*5,
                                           self.radius*5,
                                           self.radius*5)})

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
        return

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
        return

class GravityFallsMap(ba.Map):
    defs = Defs()
    name = 'Gravity Falls'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','keep_away','team_flag','king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'gravityFallsMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('gravityFallsMap'),
            'collide_model': ba.getcollidemodel('gravityFallsMapCob'),
            'modeld': ba.getmodel('gravityFallsMapD'),
            'tex': ba.gettexture('gravityFallsMapColor')
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

        self.noded = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['modeld'],
                'materials': [shared.footing_material,
                              shared.death_material]
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.8, 0.9, 1.3)
        gnode.ambient_color = (0.8, 0.9, 1.3)
        gnode.vignette_outer = (0.79, 0.79, 0.69)
        gnode.vignette_inner = (0.97, 0.97, 0.99)

        PortalGF(position=(7.5929, -10.1028, -1.68649),
                 position2=(5.2929, 11.1028, -2.78649),
                 color=(3,0,9))

# ba_meta export plugin
class Map(ba.Plugin):
    def on_app_launch(self):
        _map.register_map(GravityFallsMap)
