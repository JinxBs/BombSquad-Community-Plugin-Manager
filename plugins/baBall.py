# ba_meta require api 6
from __future__ import annotations
from typing import TYPE_CHECKING

import ba,_ba,random,time,datetime,weakref,json,os
from bastd.gameutils import SharedObjects
from bastd.actor.bomb import (BombFactory, ImpactMessage)

if TYPE_CHECKING:
    from typing import List, Sequence, Optional, Dict, Any

class StickyBall(ba.Actor):
    def __init__(self,
                 scale: float = 1.0,
                 position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
    
        self.scale = scale
        shared = SharedObjects.get()
        bomb = BombFactory.get()
        materials = [shared.object_material,
                     bomb.impact_blast_material]
        
        model = ba.getmodel('frostyPelvis')
        tex = ba.gettexture('powerupStickyBombs')
        
        self.bounce = False
        self.old_pos = position
        self.position = (position[0], position[1]+2, position[2])
        
        self.node = ba.newnode('prop', delegate=self,
                   attrs={'position': self.position,
                          'body': 'sphere',
                          'body_scale': self.scale,
                          'model': model,
                          'shadow_size': 0.3,
                          'color_texture': tex,
                          'reflection': 'powerup',
                          'reflection_scale': [1.5],
                          'materials': materials})
        ba.animate(self.node, 'model_scale',
            {0: 0, 0.2: 1.3 * self.scale, 0.26: self.scale})

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ImpactMessage):
            if self.bounce:
                self.node.handlemessage(
                        'impulse', self.node.position[0], self.node.position[1],
                        self.node.position[2], -self.node.velocity[0]*2,
                        self.node.velocity[1]+10, -self.node.velocity[2]*2,
                        -50, -50, 0, 0, -self.node.velocity[0]*2,
                        self.node.velocity[1]+10, -self.node.velocity[2]*2)
                ba.playsound(ba.getsound('bunnyJump'),position=self.node.position)
        elif isinstance(msg, ba.HitMessage):
            self.node.handlemessage('impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                msg.velocity[0], msg.velocity[1], msg.velocity[2], msg.magnitude,
                msg.velocity_magnitude, msg.radius, 0,
                msg.velocity[0], msg.velocity[1], msg.velocity[2])
        elif isinstance(msg, ba.OutOfBoundsMessage):
            self.node.position = self.position
            self.node.velocity = (0.0, 0.0, 0.0)
            self.node.extra_acceleration = (0.0, 0.0, 0.0)
        elif isinstance(msg, ba.PickedUpMessage):
            self.bounce = False
        elif isinstance(msg, ba.DroppedMessage):
            self.bounce = True
        elif isinstance(msg, ba.DieMessage):
            if self.node:
                self.node.delete()
            StickyBall(scale=self.scale,
                       position=self.old_pos).autoretain()
        else:
            return super().handlemessage(msg)

super_map = ba.Map.__init__
def new_map(self, *args, **kwargs):
    super_map(self, *args, **kwargs)
    spawn1 = self.defs.points['spawn1']
    StickyBall(position=spawn1).autoretain()
    
def plugin():
    ba.Map.__init__ = new_map
    
# ba_meta export plugin
class Ball(ba.Plugin):
    plugin()