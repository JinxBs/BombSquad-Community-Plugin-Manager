"""Define a simple example plugin."""

# ba_meta require api 6

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
import random
from ba._gameactivity import GameActivity
from ba._messages import PlayerDiedMessage, StandMessage
from bastd.actor.bomb import Bomb

if TYPE_CHECKING:
    pass

# ba_meta export plugin
class InmortalMod(ba.Plugin):
    """My first ballistica plugin!"""

    def new_spawn_player_spaz(self,
                          player: PlayerType,
                          position: Sequence[float] = (1, 0, 0),
                          angle: float = None) -> PlayerSpaz:
        """Create and wire up a ba.PlayerSpaz for the provided ba.Player."""
        # pylint: disable=too-many-locals
        # pylint: disable=cyclic-import
        from ba import _math
        from ba._gameutils import animate
        from ba._coopsession import CoopSession
        from bastd.actor.playerspaz import PlayerSpaz
        name = player.getname()
        color = player.color
        highlight = player.highlight

        light_color = _math.normalized_color(color)
        display_color = _ba.safecolor(color, target_intensity=0.32)
        spaz = PlayerSpaz(color=color,
                          highlight=highlight,
                          character=player.character,
                          player=player)

        player.actor = spaz
        assert spaz.node

        # If this is co-op and we're on Courtyard or Runaround, add the
        # material that allows us to collide with the player-walls.
        # FIXME: Need to generalize this.
        if isinstance(self.session, CoopSession) and self.map.getname() in [
                'Courtyard', 'Tower D'
        ]:
            mat = self.map.preloaddata['collide_with_wall_material']
            assert isinstance(spaz.node.materials, tuple)
            assert isinstance(spaz.node.roller_materials, tuple)
            spaz.node.materials += (mat, )
            spaz.node.roller_materials += (mat, )

        spaz.node.name = name
        spaz.node.name_color = display_color
        spaz.connect_controls_to_player()

        # Move to the stand position and add a flash of light.
        spaz.handlemessage(
            StandMessage(
                position,
                angle if angle is not None else random.uniform(0, 380)))
        _ba.playsound(self._spawn_sound, 1, position=spaz.node.position)
        light = _ba.newnode('light', attrs={'color': light_color})
        spaz.node.connectattr('position', light, 'position')
        animate(light, 'intensity', {0: 3, 0.2: 1, 0.2: 0})
        _ba.timer(0.5, light.delete)

        def _safesetattr(node: Optional[ba.Node], attr: str,
                         val: Any) -> None:
            if node:
                setattr(node, attr, val)
        ba.timer(1.0, ba.Call(_safesetattr, spaz.node, 'invincible',
                              False))

        spaz._punch_power_scale = spaz.punch_power_scale_gloves = 1
        spaz.bomb_type = spaz.bomb_type_default = 'sticky'

        def emit() -> None:
            ba.emitfx(position=spaz.node.position,
                      velocity=spaz.node.velocity,
                      count=int(1.0),
                      scale=0.10,
                      spread=0.10,
                      chunk_type='ice')
        ba.timer(0.5, emit, repeat=True)

        def stickers() -> None:
            ba.emitfx(position=spaz.node.position,
                      velocity=spaz.node.velocity,
                      count=50,
                      spread=0.16,
                      scale=0.13,
                      chunk_type='spark',
                      emit_type='stickers')
        ba.timer(0.5, stickers, repeat=True)

        light = ba.newnode('dark',
                           owner=spaz.node,
                           attrs={
                                'position': spaz.node.position,
                                'volume_intensity_scale': 0.3,
                                'radius': 1.0,
                                'intensity':0.4,
                                'color': (9.2, 9.2, 9.7)
                                })
        spaz.node.connectattr('position', light, 'position')

        return spaz

    GameActivity.spawn_player_spaz = new_spawn_player_spaz
