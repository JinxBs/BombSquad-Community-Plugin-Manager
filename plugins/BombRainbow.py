"""Define a simple example plugin."""

# ba_meta require api 6

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import random
from bastd.actor import bomb
from bastd.actor.bomb import (SplatMessage, ExplodeMessage, ImpactMessage,
                              ArmMessage, WarnMessage, ExplodeHitMessage,
                              BombFactory, Blast)
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    pass


class NewBomb(ba.Actor):
    """A standard bomb and its variants such as land-mines and tnt-boxes.

    category: Gameplay Classes
    """

    # Ew; should try to clean this up later.
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 velocity: Sequence[float] = (0.0, 0.0, 0.0),
                 bomb_type: str = 'normal',
                 blast_radius: float = 2.0,
                 bomb_scale: float = 1.0,
                 source_player: ba.Player = None,
                 owner: ba.Node = None):
        """Create a new Bomb.

        bomb_type can be 'ice','impact','land_mine','normal','sticky', or
        'tnt'. Note that for impact or land_mine bombs you have to call arm()
        before they will go off.
        """
        super().__init__()

        shared = SharedObjects.get()
        factory = BombFactory.get()

        if bomb_type not in ('ice', 'impact', 'land_mine', 'normal', 'sticky',
                             'tnt'):
            raise ValueError('invalid bomb type: ' + bomb_type)
        self.bomb_type = bomb_type

        self._exploded = False
        self.scale = bomb_scale

        self.texture_sequence: Optional[ba.Node] = None

        if self.bomb_type == 'sticky':
            self._last_sticky_sound_time = 0.0

        self.blast_radius = blast_radius
        if self.bomb_type == 'ice':
            self.blast_radius *= 1.2
        elif self.bomb_type == 'impact':
            self.blast_radius *= 0.7
        elif self.bomb_type == 'land_mine':
            self.blast_radius *= 0.7
        elif self.bomb_type == 'tnt':
            self.blast_radius *= 1.45

        self._explode_callbacks: List[Callable[[Bomb, Blast], Any]] = []

        # The player this came from.
        self._source_player = source_player

        # By default our hit type/subtype is our own, but we pick up types of
        # whoever sets us off so we know what caused a chain reaction.
        # UPDATE (July 2020): not inheriting hit-types anymore; this causes
        # weird effects such as land-mines inheriting 'punch' hit types and
        # then not being able to destroy certain things they normally could,
        # etc. Inheriting owner/source-node from things that set us off
        # should be all we need I think...
        self.hit_type = 'explosion'
        self.hit_subtype = self.bomb_type

        # The node this came from.
        # FIXME: can we unify this and source_player?
        self.owner = owner

        # Adding footing-materials to things can screw up jumping and flying
        # since players carrying those things and thus touching footing
        # objects will think they're on solid ground.. perhaps we don't
        # wanna add this even in the tnt case?
        materials: Tuple[ba.Material, ...]
        if self.bomb_type == 'tnt':
            materials = (factory.bomb_material, shared.footing_material,
                         shared.object_material)
        else:
            materials = (factory.bomb_material, shared.object_material)

        if self.bomb_type == 'impact':
            materials = materials + (factory.impact_blast_material, )
        elif self.bomb_type == 'land_mine':
            materials = materials + (factory.land_mine_no_explode_material, )

        if self.bomb_type == 'sticky':
            materials = materials + (factory.sticky_material, )
        else:
            materials = materials + (factory.normal_sound_material, )

        if self.bomb_type == 'land_mine':
            fuse_time = None
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'model': factory.land_mine_model,
                                       'light_model': factory.land_mine_model,
                                       'body': 'landMine',
                                       'body_scale': self.scale,
                                       'shadow_size': 0.44,
                                       'color_texture': factory.land_mine_tex,
                                       'reflection': 'powerup',
                                       'reflection_scale': [1.0],
                                       'materials': materials
                                   })

        elif self.bomb_type == 'tnt':
            fuse_time = None
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'model': factory.tnt_model,
                                       'light_model': factory.tnt_model,
                                       'body': 'crate',
                                       'body_scale': self.scale,
                                       'shadow_size': 0.5,
                                       'color_texture': factory.tnt_tex,
                                       'reflection': 'soft',
                                       'reflection_scale': [0.23],
                                       'materials': materials
                                   })

        elif self.bomb_type == 'impact':
            fuse_time = 20.0
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'body': 'sphere',
                                       'body_scale': self.scale,
                                       'model': factory.impact_bomb_model,
                                       'shadow_size': 0.3,
                                       'color_texture': factory.impact_tex,
                                       'reflection': 'powerup',
                                       'reflection_scale': [1.5],
                                       'materials': materials
                                   })
            self.arm_timer = ba.Timer(
                0.2, ba.WeakCall(self.handlemessage, ArmMessage()))
            self.warn_timer = ba.Timer(
                fuse_time - 1.7, ba.WeakCall(self.handlemessage,
                                             WarnMessage()))

        else:
            fuse_time = 3.0
            if self.bomb_type == 'sticky':
                sticky = True
                model = factory.sticky_bomb_model
                rtype = 'sharper'
                rscale = 1.8
            else:
                sticky = False
                model = factory.bomb_model
                rtype = 'sharper'
                rscale = 1.8
            if self.bomb_type == 'ice':
                tex = factory.ice_tex
            elif self.bomb_type == 'sticky':
                tex = factory.sticky_tex
            else:
                tex = factory.regular_tex
            self.node = ba.newnode('bomb',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'model': model,
                                       'body_scale': self.scale,
                                       'shadow_size': 0.3,
                                       'color_texture': tex,
                                       'sticky': sticky,
                                       'owner': owner,
                                       'reflection': rtype,
                                       'reflection_scale': [rscale],
                                       'materials': materials
                                   })

            if self.bomb_type == 'normal':
                self.red = ba.gettexture('aliColorMask')
                self.blue = ba.gettexture('bombColorIce')
                self.green = ba.gettexture('bombStickyColor')
                self.purple = ba.gettexture('eggTex3')
                self.yellow = ba.gettexture('powerupBomb')
                rainbow: Sequence[ba.Texture]
                rainbow = (self.red, self.blue, self.green,
                           self.purple, self.yellow)
                self.texture_sequence = ba.newnode('texture_sequence',
                                                   owner=self.node,
                                                   attrs={
                                                       'rate': 30,
                                                       'input_textures': rainbow
                                                   })
                self.texture_sequence.connectattr('output_texture', self.node,
                                                  'color_texture')

            sound = ba.newnode('sound',
                               owner=self.node,
                               attrs={
                                   'sound': factory.fuse_sound,
                                   'volume': 0.25
                               })
            self.node.connectattr('position', sound, 'position')
            ba.animate(self.node, 'fuse_length', {0.0: 1.0, fuse_time: 0.0})

        # Light the fuse!!!
        if self.bomb_type not in ('land_mine', 'tnt'):
            assert fuse_time is not None
            ba.timer(fuse_time,
                     ba.WeakCall(self.handlemessage, ExplodeMessage()))

        ba.animate(self.node, 'model_scale', {
            0: 0,
            0.2: 1.3 * self.scale,
            0.26: self.scale
        })

    def get_source_player(
            self, playertype: Type[PlayerType]) -> Optional[PlayerType]:
        """Return the source-player if one exists and is the provided type."""
        player: Any = self._source_player
        return (player if isinstance(player, playertype) and player.exists()
                else None)

    def on_expire(self) -> None:
        super().on_expire()

        # Release callbacks/refs so we don't wind up with dependency loops.
        self._explode_callbacks = []

    def _handle_die(self) -> None:
        if self.node:
            self.node.delete()

    def _handle_oob(self) -> None:
        self.handlemessage(ba.DieMessage())

    def _handle_impact(self) -> None:
        node = ba.getcollision().opposingnode

        # If we're an impact bomb and we came from this node, don't explode.
        # (otherwise we blow up on our own head when jumping).
        # Alternately if we're hitting another impact-bomb from the same
        # source, don't explode. (can cause accidental explosions if rapidly
        # throwing/etc.)
        node_delegate = node.getdelegate(object)
        if node:
            if (self.bomb_type == 'impact' and
                (node is self.owner or
                 (isinstance(node_delegate, NewBomb) and node_delegate.bomb_type
                  == 'impact' and node_delegate.owner is self.owner))):
                return
            self.handlemessage(ExplodeMessage())

    def _handle_dropped(self) -> None:
        if self.bomb_type == 'land_mine':
            self.arm_timer = ba.Timer(
                1.25, ba.WeakCall(self.handlemessage, ArmMessage()))

        # Once we've thrown a sticky bomb we can stick to it.
        elif self.bomb_type == 'sticky':

            def _setsticky(node: ba.Node) -> None:
                if node:
                    node.stick_to_owner = True

            ba.timer(0.25, lambda: _setsticky(self.node))

    def _handle_splat(self) -> None:
        node = ba.getcollision().opposingnode
        if (node is not self.owner
                and ba.time() - self._last_sticky_sound_time > 1.0):
            self._last_sticky_sound_time = ba.time()
            assert self.node
            ba.playsound(BombFactory.get().sticky_impact_sound,
                         2.0,
                         position=self.node.position)

    def add_explode_callback(self, call: Callable[[NewBomb, Blast], Any]) -> None:
        """Add a call to be run when the bomb has exploded.

        The bomb and the new blast object are passed as arguments.
        """
        self._explode_callbacks.append(call)

    def explode(self) -> None:
        """Blows up the bomb if it has not yet done so."""
        if self._exploded:
            return
        self._exploded = True
        if self.node:
            blast = Blast(position=self.node.position,
                          velocity=self.node.velocity,
                          blast_radius=self.blast_radius,
                          blast_type=self.bomb_type,
                          source_player=ba.existing(self._source_player),
                          hit_type=self.hit_type,
                          hit_subtype=self.hit_subtype).autoretain()
            for callback in self._explode_callbacks:
                callback(self, blast)

        # We blew up so we need to go away.
        # NOTE TO SELF: do we actually need this delay?
        ba.timer(0.001, ba.WeakCall(self.handlemessage, ba.DieMessage()))

    def _handle_warn(self) -> None:
        if self.texture_sequence and self.node:
            self.texture_sequence.rate = 30
            ba.playsound(BombFactory.get().warn_sound,
                         0.5,
                         position=self.node.position)

    def _add_material(self, material: ba.Material) -> None:
        if not self.node:
            return
        materials = self.node.materials
        if material not in materials:
            assert isinstance(materials, tuple)
            self.node.materials = materials + (material, )

    def arm(self) -> None:
        """Arm the bomb (for land-mines and impact-bombs).

        These types of bombs will not explode until they have been armed.
        """
        if not self.node:
            return
        factory = BombFactory.get()
        intex: Sequence[ba.Texture]
        if self.bomb_type == 'land_mine':
            intex = (factory.land_mine_lit_tex, factory.land_mine_tex)
            self.texture_sequence = ba.newnode('texture_sequence',
                                               owner=self.node,
                                               attrs={
                                                   'rate': 30,
                                                   'input_textures': intex
                                               })
            ba.timer(0.5, self.texture_sequence.delete)

            # We now make it explodable.
            ba.timer(
                0.25,
                ba.WeakCall(self._add_material,
                            factory.land_mine_blast_material))
        elif self.bomb_type == 'impact':
            intex = (factory.impact_lit_tex, factory.impact_tex,
                     factory.impact_tex)
            self.texture_sequence = ba.newnode('texture_sequence',
                                               owner=self.node,
                                               attrs={
                                                   'rate': 100,
                                                   'input_textures': intex
                                               })
            ba.timer(
                0.25,
                ba.WeakCall(self._add_material,
                            factory.land_mine_blast_material))
        else:
            raise Exception('arm() should only be called '
                            'on land-mines or impact bombs')
        self.texture_sequence.connectattr('output_texture', self.node,
                                          'color_texture')
        ba.playsound(factory.activate_sound, 0.5, position=self.node.position)

    def _handle_hit(self, msg: ba.HitMessage) -> None:
        ispunched = (msg.srcnode and msg.srcnode.getnodetype() == 'spaz')

        # Normal bombs are triggered by non-punch impacts;
        # impact-bombs by all impacts.
        if (not self._exploded and
            (not ispunched or self.bomb_type in ['impact', 'land_mine'])):

            # Also lets change the owner of the bomb to whoever is setting
            # us off. (this way points for big chain reactions go to the
            # person causing them).
            source_player = msg.get_source_player(ba.Player)
            if source_player is not None:
                self._source_player = source_player

                # Also inherit the hit type (if a landmine sets off by a bomb,
                # the credit should go to the mine)
                # the exception is TNT.  TNT always gets credit.
                # UPDATE (July 2020): not doing this anymore. Causes too much
                # weird logic such as bombs acting like punches. Holler if
                # anything is noticeably broken due to this.
                # if self.bomb_type != 'tnt':
                #     self.hit_type = msg.hit_type
                #     self.hit_subtype = msg.hit_subtype

            ba.timer(0.1 + random.random() * 0.1,
                     ba.WeakCall(self.handlemessage, ExplodeMessage()))
        assert self.node
        self.node.handlemessage('impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                                msg.velocity[0], msg.velocity[1],
                                msg.velocity[2], msg.magnitude,
                                msg.velocity_magnitude, msg.radius, 0,
                                msg.velocity[0], msg.velocity[1],
                                msg.velocity[2])

        if msg.srcnode:
            pass

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ExplodeMessage):
            self.explode()
        elif isinstance(msg, ImpactMessage):
            self._handle_impact()
        # Ok the logic below looks like it was backwards to me.
        # Disabling for now; can bring back if need be.
        # elif isinstance(msg, ba.PickedUpMessage):
        #     # Change our source to whoever just picked us up *only* if it
        #     # is None. This way we can get points for killing bots with their
        #     # own bombs. Hmm would there be a downside to this?
        #     if self._source_player is not None:
        #         self._source_player = msg.node.source_player
        elif isinstance(msg, SplatMessage):
            self._handle_splat()
        elif isinstance(msg, ba.DroppedMessage):
            self._handle_dropped()
        elif isinstance(msg, ba.HitMessage):
            self._handle_hit(msg)
        elif isinstance(msg, ba.DieMessage):
            self._handle_die()
        elif isinstance(msg, ba.OutOfBoundsMessage):
            self._handle_oob()
        elif isinstance(msg, ArmMessage):
            self.arm()
        elif isinstance(msg, WarnMessage):
            self._handle_warn()
        else:
            super().handlemessage(msg)

# ba_meta export plugin
class BombRainbowMod(ba.Plugin):
    """My first ballistica plugin!"""

    bomb.Bomb = NewBomb
