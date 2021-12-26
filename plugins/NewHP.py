"""Define a simple example plugin."""

# ba_meta require api 6

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
from bastd.actor.spaz import Spaz

if TYPE_CHECKING:
    from typing import Any, Type, Optional, Tuple, List, Dict


#######################
version = 1.0
creador = "byANG3L"
logo = 'cuteSpaz'
settings = False

# def openWindow():
#     NewHPWindow()
#######################


# ba_meta export plugin
class NewHPText(ba.Plugin):
    """My first ballistica plugin!"""

    Spaz._old_init = Spaz.__init__
    def _new_init(self,
                 color: Sequence[float] = (1.0, 1.0, 1.0),
                 highlight: Sequence[float] = (0.5, 0.5, 0.5),
                 character: str = 'Spaz',
                 source_player: ba.Player = None,
                 start_invincible: bool = True,
                 can_accept_powerups: bool = True,
                 powerups_expire: bool = False,
                 demo_mode: bool = False):
        self._old_init(color,highlight,character,source_player,
                       start_invincible,can_accept_powerups,
                       powerups_expire,demo_mode)
        def _new_hp():
            if not self.node:
                return
            hp = ba.newnode('math',
                            owner=self.node,
                            attrs={
                                'input1': (
                                    0, 1.37, 0) if self.source_player else (
                                    0, 1.20, 0),
                                'operation': 'add'
                            })
            self.node.connectattr('torso_position', hp, 'input2')
            self.hp = ba.newnode('text',
                                 owner=self.node,
                                 attrs={
                                    'text': '',
                                    'in_world': True,
                                    'shadow': 1.0,
                                    'flatness': 1.0,
                                    'scale': 0.012,
                                    'h_align': 'center',
                                 })
            hp.connectattr('output', self.hp, 'position')
            ba.animate(self.hp, 'scale', {0:0, 0.2:0, 0.6:0.018, 0.8:0.012})

            def _update():
                if not self.hp:
                    return
                if self.shield:
                    hptext = int(
                        (self.shield_hitpoints/self.shield_hitpoints_max)*100)
                else:
                    hptext = int(self.hitpoints*0.1)
                if hptext >= 75:
                    color = (0.2, 1.0, 0.2)
                elif hptext >= 50:
                    color = (1.0, 1.0, 0.2)
                elif hptext >= 25:
                    color = (1.0, 0.5, 0.2)
                else:
                    color = (1.0, 0.2, 0.2)
                self.hp.text = str(hptext) + '%'
                self.hp.color = (0.2, 1.0, 0.8) if self.shield else color
            ba.timer(0.05, _update, repeat=True)
        _new_hp()
        # app = _ba.app
        # cfg = app.config
        # new_hp = cfg.get('New HP', True)
        # if new_hp:
        #     _new_hp()

    Spaz.__init__ = _new_init
