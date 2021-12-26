"""Flotating Mine."""

# Made By : SOUL
# My GOOGLE PLAY ID : SOULXGAMING96

# Update to (1.5 - 1.6) by: byANG3L

# ba_meta require api 6

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
from ba._map import Map
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    pass


# ba_meta export plugin
class FlotatingMine(ba.Plugin):

    Map.__old_init__ = Map.__init__
    def __init__(self,
                 vr_overlay_offset: Optional[Sequence[float]] = None) -> None:
        self.__old_init__(vr_overlay_offset)
        shared = SharedObjects.get()
        from bastd import mainmenu
        in_game = not isinstance(_ba.get_foreground_host_session(),
                                 mainmenu.MainMenuSession)
        if not in_game:
            return
        def path():
            p = ba.newnode(
                'prop',
                attrs={
                    'position': (-5.750,4.3515026107,2.0),
                    'velocity': (2.0,1.0,0),
                    'sticky': False,
                    'body': 'landMine',
                    'model': ba.getmodel('landMine'),
                    'model_scale': 1.0,
                    'color_texture': ba.gettexture('achievementWall'),
                    'body_scale': 1.0,
                    'reflection': 'powerup',
                    'reflection_scale': [1.0],
                    'density': 99999 * 99999,
                    'gravity_scale': 0.0,
                    'shadow_size': 0.0,
                    'materials': [shared.footing_material,
                                 shared.object_material]
                })
            ba.animate_array(p, 'position', 3,
                            {0: (1.830634, 4.830635, 3.830636),
                            10: (4.8306378, 4.83063588, -6.830639),
                            20: (-5.422572086, 4.228850685, 2.803988636),
                            25: (-6.859406739, 4.429165244, -6.588618549),
                            30: (-6.859406739, 4.429165244, -6.588618549),
                            35: (3.148493267, 4.429165244, -6.588618549),
                            40: (1.830377363, 4.228850685, 2.803988636),
                            45: (-5.422572086, 4.228850685, 2.803988636),
                            50: (-5.422572086, 4.228850685, 2.803988636),
                            55: (1.830377363, 4.228850685, 2.803988636),
                            60: (3.148493267, 4.429165244, -6.588618549),
                            70: (1.830377363, 4.228850685, 2.803988636),
                            75: (3.148493267, 4.429165244, -6.588618549),
                            80: (-5.422572086, 4.228850685, 2.803988636),
                            90: (-6.859406739, 4.429165244, -6.588618549),
                            95: (-6.859406739, 4.429165244, -6.588618549)},
                            loop = True)
        ba.timer(0.1, path)
    Map.__init__ = __init__
