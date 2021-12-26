"""DeathMatch game and support classes."""
# Created by: byANG3L #
# YT: https://www.youtube.com/c/JoseANG3LYT #

# ba_meta require api 6
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import ba
import _ba
from bastd.actor.bomb import Bomb, BombFactory
from bastd.actor.flag import Flag
from bastd.actor.playerspaz import PlayerSpaz
from bastd.actor.scoreboard import Scoreboard
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Type, List, Dict, Optional, Sequence, Union

class MagicBox(Bomb):

    def __init__(self,
                 position: Sequence[float] = (0.0, 1.5, 0.0),
                 velocity: Sequence[float] = (0.0, 0.0, 0.0),
                 bomb_type: srt = 'tnt',
                 blast_radius: float = 2.0,
                 source_player: ba.Player = None,
                 owner: ba.Node = None):

        ba.Actor.__init__(self)

        shared = SharedObjects.get()
        factory = BombFactory.get()

        self.bomb_type = 'impact'
        self._exploded = False
        self.blast_radius = blast_radius

        # tnt
        self.blast_radius *= 9.45
        self._explode_callbacks = []

        # the player this came from
        self.source_player = self._source_player = source_player

        # by default our hit type/subtype is our own,
        # but we pick up types of whoever
        # sets us off so we know what caused a chain reaction
        self.hit_type = 'explosion'
        self.hit_subtype = self.bomb_type

        # if no owner was provided, use an unconnected node ref
        if owner is None:
            owner = ba.Node(None)

        # The node this came from.
        # FIXME: can we unify this and source_player?
        self.owner = owner

        materials = (factory.bomb_material, shared.footing_material,
                     shared.object_material)
        materials = materials + (factory.normal_sound_material, )

        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'position': position,
                                   'velocity': velocity,
                                   'model': factory.impact_bomb_model,
                                   'light_model': factory.impact_bomb_model,
                                   'body': 'crate',
                                   'shadow_size': 0.3,
                                   'color_texture': factory.impact_tex,
                                   'reflection': 'powerup',
                                   'reflection_scale': [1.5],
                                   'materials': materials
                              })

        # self.node.extraAcceleration = (0, 40, 0)
        self.held_by = 0
        self._is_dead = False

        ba.animate(self.node,
                   'model_scale',
                   {0: 0.5, 2: 1, 20: 5.3, 22: 5, 24: 5, 40: 20})

    def _add_impact_material(self) -> None:
        if not self.node:
            return
        shared = SharedObjects.get()
        factory = BombFactory.get()
        materials = (factory.impact_blast_material, factory.bomb_material,
                     shared.footing_material, shared.object_material)
        new_materials = materials + (factory.normal_sound_material, )
        self.node.materials = new_materials

        intex = (factory.impact_lit_tex, factory.impact_tex,
                 factory.impact_tex)
        self.texture_sequence = ba.newnode('texture_sequence',
                                           owner=self.node,
                                           attrs={
                                               'rate': 100,
                                               'input_textures': intex
                                           })
        self.texture_sequence.connectattr('output_texture', self.node,
                                          'color_texture')
        ba.playsound(factory.activate_sound,
                     0.5,
                     position=self.node.position)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.PickedUpMessage):
            _ba.getactivity()._update_box_state()
            ba.timer(1.0, self._add_impact_material)
        elif isinstance(msg, ba.DroppedMessage):
            self.held_by -= 1
            ba.timer(0.01, self._update_floatyness)
            ba.timer(0.2, _ba.getactivity()._update_box_state)
        elif isinstance(msg, ba.DieMessage):
            if not self._is_dead:
                ba.timer(1.0,  _ba.getactivity()._spawn_box)
            self._is_dead = True
        super().handlemessage(msg)

    def _update_floatyness(self) -> None:
        if self.node:
            old_y = self.node.extra_acceleration[1]
            new_y = {0: 0, 1: 39, 2: 19 + 20 * 2,
                     3: 19 + 20 * 3}.get(self.held_by, 0)
            time = 0.3 if (old_y >= new_y) else 1.0
            keys = {0: (0, old_y, 0), time: (0, new_y, 0)}
            ba.animate_array(self.node, 'extra_acceleration', 3, keys)

    def _hide_score_text(self) -> None:
        if self._score_text:
            assert isinstance(self._score_text.scale, float)
            ba.animate(self._score_text, 'scale', {
                0.0: self._score_text.scale,
                0.2: 0.0
            })

    def set_score_text(self, text: str) -> None:
        """Show a message over the flag; handy for scores."""
        if not self.node:
            return
        try:
            exists = self._score_text
        except Exception:
            exists = False
        if not exists:
            start_scale = 0.0
            math = ba.newnode('math',
                              owner=self.node,
                              attrs={
                                  'input1': (0, 0.6, 0),
                                  'operation': 'add'
                              })
            self.node.connectattr('position', math, 'input2')
            self._score_text = ba.newnode('text',
                                          owner=self.node,
                                          attrs={
                                              'text': text,
                                              'in_world': True,
                                              'scale': 0.02,
                                              'shadow': 0.5,
                                              'flatness': 1.0,
                                              'h_align': 'center'
                                          })
            math.connectattr('output', self._score_text, 'position')
        else:
            assert isinstance(self._score_text.scale, float)
            start_scale = self._score_text.scale
            self._score_text.text = text
        self._score_text.color = ba.safecolor((1.0, 1.0, 0.4))
        ba.animate(self._score_text, 'scale', {0: start_scale, 0.2: 0.02})
        self._score_text_hide_timer = ba.Timer(
            1.0, ba.WeakCall(self._hide_score_text))

class BoxState(Enum):
    """States our single flag can be in."""
    NEW = 0
    UNCONTESTED = 1
    CONTESTED = 2
    HELD = 3

class Player(ba.Player['Team']):
    """Our player type for this game."""

class Team(ba.Team[Player]):
    """Our team type for this game."""

    def __init__(self, timeremaining: int) -> None:
        self.timeremaining = timeremaining
        self.holdingbox = False

# ba_meta export game
class AtomicBomb(ba.TeamGameActivity[Player, Team]):

    name = 'Atomic Bomb'
    description = 'Get the bomb and start flying.'

    available_settings = [
        ba.IntSetting(
            'Hold Time',
            min_value=10,
            default=30,
            increment=10,
        ),
        ba.IntChoiceSetting(
            'Time Limit',
            choices=[
                ('None', 0),
                ('1 Minute', 60),
                ('2 Minutes', 120),
                ('5 Minutes', 300),
                ('10 Minutes', 600),
                ('20 Minutes', 1200),
            ],
            default=0,
        ),
        ba.FloatChoiceSetting(
            'Respawn Times',
            choices=[
                ('Shorter', 0.25),
                ('Short', 0.5),
                ('Normal', 1.0),
                ('Long', 2.0),
                ('Longer', 4.0),
            ],
            default=1.0,
        ),
        ba.BoolSetting('Epic Mode', default=False),
    ]
    scoreconfig = ba.ScoreConfig(label='Time Held')

    @classmethod
    def supports_session_type(cls, sessiontype: Type[ba.Session]) -> bool:
        return (issubclass(sessiontype, ba.DualTeamSession)
                or issubclass(sessiontype, ba.FreeForAllSession))

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[ba.Session]) -> List[str]:
        return ba.getmaps('keep_away')

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._scoreboard = Scoreboard()
        self._swipsound = ba.getsound('swip')
        self._tick_sound = ba.getsound('tick')
        self._countdownsounds = {
            10: ba.getsound('announceTen'),
            9: ba.getsound('announceNine'),
            8: ba.getsound('announceEight'),
            7: ba.getsound('announceSeven'),
            6: ba.getsound('announceSix'),
            5: ba.getsound('announceFive'),
            4: ba.getsound('announceFour'),
            3: ba.getsound('announceThree'),
            2: ba.getsound('announceTwo'),
            1: ba.getsound('announceOne')
        }

        self._flag_spawn_pos: Optional[Sequence[float]] = None
        self._update_timer: Optional[ba.Timer] = None
        self._holding_players: List[Player] = []
        self._box_state: Optional[BoxState] = None
        self._box_light: Optional[ba.Node] = None
        self._box: Optional[Box] = None
        self._hold_time = int(settings['Hold Time'])
        self._time_limit = float(settings['Time Limit'])
        self._epic_mode = bool(settings['Epic Mode'])

        # Base class overrides
        self.slow_motion = self._epic_mode
        self.default_music = (ba.MusicType.EPIC
                              if self._epic_mode else ba.MusicType.CHOSEN_ONE)

    def get_instance_description(self) -> Union[str, Sequence]:
        return 'Hold the bomb for ${ARG1} seconds.', self._hold_time

    def get_instance_description_short(self) -> Union[str, Sequence]:
        return 'Hold the bomb for ${ARG1} seconds', self._hold_time

    def create_team(self, sessionteam: ba.SessionTeam) -> Team:
        return Team(timeremaining=self._hold_time)

    def on_team_join(self, team: Team) -> None:
        self._update_scoreboard()

    def on_begin(self) -> None:
        super().on_begin()
        self.setup_standard_time_limit(self._time_limit)
        self.setup_standard_powerup_drops(enable_tnt=False)
        self._box_spawn_pos = self.map.get_flag_position(None)
        self._spawn_box()
        self._update_timer = ba.Timer(1.0, call=self._tick, repeat=True)
        self._update_box_state()

    def _tick(self) -> None:
        self._update_box_state()

        # Award points to all living players holding the flag.
        for player in self._holding_players:
            if player:
                assert self.stats
                self.stats.player_scored(player,
                                         3,
                                         screenmessage=False,
                                         display=False)

        scoreteam = self._scoring_team

        if scoreteam is not None:

            if scoreteam.timeremaining > 0:
                ba.playsound(self._tick_sound)

            scoreteam.timeremaining = max(0, scoreteam.timeremaining - 1)
            self._update_scoreboard()
            if scoreteam.timeremaining > 0:
                assert self._box is not None
                self._box.set_score_text(str(scoreteam.timeremaining))

            # announce numbers we have sounds for
            if scoreteam.timeremaining in self._countdownsounds:
                ba.playsound(self._countdownsounds[scoreteam.timeremaining])

            # Winner!
            if scoreteam.timeremaining <= 0:
                self.end_game()

    def end_game(self) -> None:
        results = ba.GameResults()
        for team in self.teams:
            results.set_team_score(team, self._hold_time - team.timeremaining)
        self.end(results=results, announce_delay=0)

    def _update_box_state(self) -> None:
        for team in self.teams:
            team.holdingbox = False
        self._holding_players = []
        for player in self.players:
            holdingbox = False
            try:
                assert isinstance(player.actor, (PlayerSpaz, type(None)))
                if (player.actor and player.actor.node
                        and player.actor.node.hold_node):
                    holdingbox = (
                        player.actor.node.hold_node == self._box.node)
            except Exception:
                ba.print_exception('Error checking hold box.')
            if holdingbox:
                self._holding_players.append(player)
                player.team.holdingbox = True

        if self._box is not None and self._box:
            self._box.held_by = len(self._holding_players)
            self._box._update_floatyness()

        holdingteams = set(t for t in self.teams if t.holdingbox)
        prevstate = self._box_state
        assert self._box is not None
        assert self._box.node
        if len(holdingteams) > 1:
            self._box_state = BoxState.CONTESTED
            self._scoring_team = None
        elif len(holdingteams) == 1:
            holdingteam = list(holdingteams)[0]
            self._box_state = BoxState.HELD
            self._scoring_team = holdingteam
        else:
            self._box_state = BoxState.UNCONTESTED
            self._scoring_team = None

        if self._box_state != prevstate:
            ba.playsound(self._swipsound)

    def _spawn_box(self) -> None:
        ba.playsound(self._swipsound)
        self._flash_box_spawn()
        self._box =  MagicBox(position=self._box_spawn_pos)
        self._box_state = BoxState.NEW
        self._box_light = ba.newnode('light',
                                     owner=self._box.node,
                                     attrs={
                                         'intensity': 0.2,
                                         'radius': 0.3,
                                         'color': (0.2, 0.2, 0.2)
                                     })
        assert self._box.node
        self._box.node.connectattr('position', self._box_light, 'position')
        self._update_box_state()

    def _flash_box_spawn(self) -> None:
        light = ba.newnode('light',
                           attrs={'position': self._box_spawn_pos,
                                  'color': (1.0 ,1.0 ,1.0),
                                  'radius': 0.3,
                                  'height_attenuated': False
                           })
        ba.animate(light, 'intensity', {0.0: 0, 0.25: 0.5, 0.5: 0}, loop=True)
        ba.timer(1.0, light.delete)

    def _update_scoreboard(self) -> None:
        for team in self.teams:
            self._scoreboard.set_team_value(team,
                                            team.timeremaining,
                                            self._hold_time,
                                            countdown=True)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.PlayerDiedMessage):
            # Augment standard behavior.
            super().handlemessage(msg)
            player = msg.getplayer(Player)
            self.respawn_player(player)
        else:
            super().handlemessage(msg)
