"""Super Smash mini-game."""

# Created by: Mrmaxmeier
# Edited to BombSquad 1.5.x by: byANG3L

# ba_meta require api 6
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import random
from ba import _math
from bastd.actor.spazfactory import SpazFactory
from bastd.actor.scoreboard import Scoreboard
from bastd.game.elimination import EliminationGame, Icon, Player, Team
from bastd.actor.bomb import Bomb, Blast
from bastd.actor.playerspaz import PlayerSpaz

if TYPE_CHECKING:
	from typing import (Any, Tuple, Dict, Type, List, Sequence, Optional,
						Union)


class PowBox(Bomb):

	def __init__(self, position=(0, 1, 0), velocity=(0, 0, 0)):

		Bomb.__init__(self, position, velocity,
						bomb_type='tnt', blast_radius=2.5,
						source_player=None, owner=None)
		self.set_pow_text()

	def set_pow_text(self):
		m = ba.newnode('math', owner=self.node,
					   attrs={'input1': (0, 0.7, 0),
							  'operation': 'add'})
		self.node.connectattr('position', m, 'input2')
		self._pow_text = ba.newnode('text',
									  owner=self.node,
									  attrs={'text':'POW!',
											 'in_world': True,
											 'shadow': 1.0,
											 'flatness': 1.0,
											 'color': (1, 1, 0.4),
											 'scale':0.0,
											 'h_align':'center'})
		m.connectattr('output', self._pow_text, 'position')
		ba.animate(self._pow_text, 'scale', {0: 0.0, 1.0: 0.01})

	def pow(self):
		self.explode()

	def handlemessage(self, m):
		if isinstance(m, ba.PickedUpMessage):
			self._heldBy = m.node
		elif isinstance(m, ba.DroppedMessage):
			ba.timer(0.6, self.pow)
		Bomb.handlemessage(self, m)


class PlayerSpaz_Smash(PlayerSpaz):
	multiplyer = 1
	is_dead = False

	def oob_effect(self):
		if self.is_dead:
			return
		self.is_dead = True
		if self.multiplyer > 1.25:
			blast_type = 'tnt'
			radius = min(self.multiplyer * 5, 20)
		else:
			# penalty for killing people with low multiplyer
			blast_type = 'ice'
			radius = 7.5
		Blast(position=self.node.position,
				 blast_radius=radius,
				 blast_type=blast_type).autoretain()

	def handlemessage(self, m: Any) -> Any:
		if isinstance(m, ba.HitMessage):
			if not self.node.exists():
				return
			if self.node.invincible == True:
				ba.playsound(SpazFactory.get().block_sound, 1.0,
							position=self.node.position)
				return True
			t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
			if self._last_hit_time is None or t_ms - self._last_hit_time > 1000:
				self._num_times_hit += 1
				self._last_hit_time = t_ms

			mag = m.magnitude * self.impact_scale
			velocity_mag = m.velocity_magnitude * self.impact_scale

			damage_scale = 0.22

			# if they've got a shield, deliver it to that instead..
			if self.shield is not None:
				if m.flat_damage:
					damage = m.flat_damage * self.impact_scale
				else:
					# hit our spaz with an impulse but tell it to only return
					# theoretical damage; not apply the impulse..
					self.node.handlemessage("impulse",
											m.pos[0],
											m.pos[1],
											m.pos[2],
											m.velocity[0],
											m.velocity[1],
											m.velocity[2],
											mag, velocity_mag,
											m.radius, 1,
											m.force_direction[0],
											m.force_direction[1],
											m.force_direction[2])
					damage = damage_scale * self.node.damage

				self.shield_hitpoints -= damage

				self.shield.hurt = (
					1.0 - self.shield_hitpoints / self.shield_hitpoints_max)
				# its a cleaner event if a hit just kills the shield
				# without damaging the player..
				# however, massive damage events should still be able
				# to damage the player..
				# this hopefully gives us a happy medium.
				max_spillover = 500
				if self.shield_hitpoints <= 0:
					# fixme - transition out perhaps?..
					self.shield.delete()
					self.shield = None
					ba.playsound(SpazFactory.get().shield_down_sound, 1.0,
								position=self.node.position)
					# emit some cool lookin sparks when the shield dies
					t = self.node.position
					ba.emitfx(position=(t[0], t[1]+0.9, t[2]),
							  velocity=self.node.velocity,
							  count=random.randrange(20, 30), scale=1.0,
							  spread=0.6, chunk_type='spark')

				else:
					ba.playsound(SpazFactory.get().shield_hit_sound, 0.5,
								position=self.node.position)

				# emit some cool lookin sparks on shield hit
				ba.emitfx(position=m.pos,
						  velocity=(m.force_direction[0]*1.0,
									m.force_direction[1]*1.0,
									m.force_direction[2]*1.0),
						  count=min(30, 5+int(damage*0.005)), scale=0.5,
									spread=0.3, chunk_type='spark')


				# if they passed our spillover threshold,
				#  pass damage along to spaz
				if self.shield_hitpoints <= -max_spillover:
					leftover_damage = -max_spillover - self.shield_hitpoints
					shield_leftover_ratio = leftover_damage / damage

					# scale down the magnitudes applied to spaz accordingly..
					mag *= shield_leftover_ratio
					velocity_mag *= shield_leftover_ratio
				else:
					return True # good job shield!
			else: shield_leftover_ratio = 1.0

			if m.flat_damage:
				damage = (
					m.flat_damage * self.impact_scale * shield_leftover_ratio)
			else:
				# hit it with an impulse and get the resulting damage
				#bs.screenMessage(str(velocityMag))
				if self.multiplyer > 3.0:
					# at about 8.0 the physics glitch out
					velocity_mag *= (
						min((3.0 + (self.multiplyer-3.0)/4), 7.5) ** 1.9)
				else:
					velocity_mag *= self.multiplyer ** 1.9
				self.node.handlemessage("impulse",
										m.pos[0],
										m.pos[1],
										m.pos[2],
										m.velocity[0],
										m.velocity[1],
										m.velocity[2],
										mag, velocity_mag, m.radius, 0,
										m.force_direction[0],
										m.force_direction[1],
										m.force_direction[2])

				damage = damage_scale * self.node.damage
			self.node.handlemessage("hurt_sound")

			# play punch impact sound based on damage if it was a punch
			if m.hit_type == 'punch':

				self.on_punched(damage)

				# lets always add in a super-punch sound
				# with boxing gloves just to differentiate them
				if m.hit_subtype == 'super_punch':
					ba.playsound(SpazFactory.get().punch_sound_stronger, 1.0,
								 position=self.node.position)

				if damage > 500:
					sounds = SpazFactory.get().punch_sound_strong
					sound = sounds[random.randrange(len(sounds))]
				else: sound = SpazFactory.get().punch_sound
				ba.playsound(sound, 1.0, position=self.node.position)

				# throw up some chunks
				ba.emitfx(position=m.pos,
						  velocity=(m.force_direction[0]*0.5,
									m.force_direction[1]*0.5,
									m.force_direction[2]*0.5),
						  count=min(10, 1+int(damage*0.0025)),
								scale=0.3, spread=0.03)

				ba.emitfx(position=m.pos,
						  chunk_type='sweat',
						  velocity=(m.force_direction[0]*1.3,
									m.force_direction[1]*1.3+5.0,
									m.force_direction[2]*1.3),
						  count=min(30, 1 + int(damage * 0.04)),
						  scale=0.9,
						  spread=0.28)
				# momentary flash
				hurtiness = damage*0.003
				hurtiness = min(hurtiness, 750 * 0.003)
				punch_pos = (m.pos[0]+m.force_direction[0]*0.02,
							m.pos[1]+m.force_direction[1]*0.02,
							m.pos[2]+m.force_direction[2]*0.02)
				flash_color = (1.0, 0.8, 0.4)
				light = ba.newnode("light",
								   attrs={'position':punch_pos,
										  'radius':0.12+hurtiness*0.12,
										  'intensity':0.3*(1.0+1.0*hurtiness),
										  'height_attenuated':False,
										  'color':flash_color})
				ba.timer(0.06, light.delete)


				flash = ba.newnode("flash",
								   attrs={'position':punch_pos,
										  'size':0.17+0.17*hurtiness,
										  'color':flash_color})
				ba.timer(0.06, flash.delete)

			if m.hit_type == 'impact':
				ba.emitfx(position=m.pos,
						  velocity=(m.force_direction[0]*2.0,
									m.force_direction[1]*2.0,
									m.force_direction[2]*2.0),
						  count=min(10, 1 + int(damage * 0.01)),
									scale=0.4, spread=0.1)

			if self.hitpoints > 0:

				# its kinda crappy to die from impacts,
				# so lets reduce impact damage
				# by a reasonable amount if it'll keep us alive
				if m.hit_type == 'impact' and damage > self.hitpoints:
					# drop damage to whatever puts us at 10 hit points,
					# or 200 less than it used to be
					# whichever is greater
					# (so it *can* still kill us if its high enough)
					new_damage = max(damage-200, self.hitpoints-10)
					damage = new_damage

				self.node.handlemessage("flash")
				# if we're holding something, drop it
				if damage > 0.0 and self.node.hold_node.exists():
					self.node.hold_node = ba.Node(None)
				#self.hitPoints -= damage
				self.multiplyer += min(damage / 2000, 0.15)
				if damage/2000 > 0.05:
					self.set_score_text(str(int((self.multiplyer-1)*100))+"%")
				#self.node.hurt = 1.0 - self.hitPoints/self.hitPointsMax
				self.node.hurt = 0.0
				# if we're cursed, *any* damage blows us up
				if self._cursed and damage > 0:
					bs.timer(0.05, bs.WeakCall(self.curse_explode,
												m.source_player))
				# if we're frozen, shatter.. otherwise die if we hit zero
				#if self.frozen and (damage > 200 or self.hitPoints <= 0):
				#	self.shatter()
				#elif self.hitPoints <= 0:
				#	self.node.handleMessage(bs.DieMessage(how='impact'))

			# if we're dead, take a look at the smoothed damage val
			# (which gives us a smoothed average of recent damage) and shatter
			# us if its grown high enough
			#if self.hitPoints <= 0:
			#	damageAvg = self.node.damageSmoothed * damageScale
			#	if damageAvg > 1000:
			#		self.shatter()
		elif isinstance(m, ba.DieMessage):
			self.oob_effect()
			super().handlemessage(m)
		elif isinstance(m, ba.PowerupMessage):
			if m.poweruptype == 'health':
				if self.multiplyer > 2:
					self.multiplyer *= 0.5
				else:
					self.multiplyer *= 0.75
				self.multiplyer = max(1, self.multiplyer)
				self.set_score_text(str(int((self.multiplyer-1)*100))+"%")
			super().handlemessage(m)
		else:
			super().handlemessage(m)


# ba_meta export game
class SuperSmash(EliminationGame):

	name = 'Super Smash'
	description = 'Knock everyone off the map.'

	def on_begin(self) -> None:
		self._start_time = ba.time()
		self.setup_standard_time_limit(self._time_limit)
		if self._solo_mode:
			self._vs_text = ba.NodeActor(
				ba.newnode('text',
						   attrs={
							   'position': (0, 105),
							   'h_attach': 'center',
							   'h_align': 'center',
							   'maxwidth': 200,
							   'shadow': 0.5,
							   'vr_depth': 390,
							   'scale': 0.6,
							   'v_attach': 'bottom',
							   'color': (0.8, 0.8, 0.3, 1.0),
							   'text': ba.Lstr(resource='vsText')
						   }))

		# If balance-team-lives is on, add lives to the smaller team until
		# total lives match.
		if (isinstance(self.session, ba.DualTeamSession)
				and self._balance_total_lives and self.teams[0].players
				and self.teams[1].players):
			if self._get_total_team_lives(
					self.teams[0]) < self._get_total_team_lives(self.teams[1]):
				lesser_team = self.teams[0]
				greater_team = self.teams[1]
			else:
				lesser_team = self.teams[1]
				greater_team = self.teams[0]
			add_index = 0
			while (self._get_total_team_lives(lesser_team) <
				   self._get_total_team_lives(greater_team)):
				lesser_team.players[add_index].lives += 1
				add_index = (add_index + 1) % len(lesser_team.players)

		self._update_icons()

		# We could check game-over conditions at explicit trigger points,
		# but lets just do the simple thing and poll it.
		ba.timer(1.0, self._update, repeat=True)

		self.setup_standard_powerup_drops(enable_tnt=False)
		self._pow = None
		self._tnt_drop_timer = ba.Timer(1.1, ba.WeakCall(
									  self._drop_pow_box),
									  repeat=True)

	def _drop_pow_box(self) -> None:
		pos = random.choice(self.map.tnt_points)
		pos = (pos[0], pos[1] + 1, pos[2])
		tnt_alive = self._pow is not None and self._pow.node
		if not tnt_alive:
			# Respawn if its been long enough.. otherwise just increment our
			# how-long-since-we-died value.
			if self._pow is None or self._wait_time >= 20:
				self._pow = PowBox(position=pos, velocity=(0, 1, 0))
				self._wait_time = 0.0
			else:
				self._wait_time += 1.1

	def spawn_player(self, player: Player) -> ba.Actor:
		if (isinstance(self.session, ba.DualTeamSession)):
			position = self.map.get_start_position(player.team.id)
		else:
			position = self.map.get_ffa_start_position(self.players)
		angle = None

		name = player.getname()
		light_color = _math.normalized_color(player.color)
		display_color = ba.safecolor(player.color, target_intensity=0.75)

		spaz = PlayerSpaz_Smash(color=player.color,
								highlight=player.highlight,
								character=player.character,
								player=player)
		player.actor = spaz

		spaz.node.name = name
		spaz.node.name_color = display_color

		ba.playsound(self._spawn_sound, 1, position=spaz.node.position)
		light = ba.newnode('light', attrs={'color': light_color})
		spaz.node.connectattr('position', light, 'position')

		ba.animate(light, 'intensity', {0: 0, 0.25: 1, 0.5: 0})

		ba.timer(0.7, light.delete)

		spaz.connect_controls_to_player()
		spaz.handlemessage(
			ba.StandMessage(
				position,
				angle if angle is not None else random.uniform(0, 360)))

		if not self._solo_mode:
			ba.timer(0.3, ba.Call(self._print_lives, player))

		# If we have any icons, update their state.
		for icon in player.icons:
			icon.handle_player_spawned()

		return spaz
