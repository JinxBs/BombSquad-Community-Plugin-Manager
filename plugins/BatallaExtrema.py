"""Batalla Extrema | byANG3L"""

# ba_meta require api 6
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import ba
from bastd.actor.spazbot import (SpazBotSet, BomberBotStaticLite,
                                 BomberBotStatic, BrawlerBotLite, BrawlerBot,
                                 StickyBotStatic, ExplodeyBotNoTimeLimit,
                                 BrawlerBotProShielded, SpazBotDiedMessage)
from bastd.actor.onscreentimer import OnScreenTimer

if TYPE_CHECKING:
    from typing import Any, Optional


def ba_get_api_version():
    return 6

def ba_get_levels():
	return [ba._level.Level(
            '${GAME}',
			gametype=BatallaExtrema,
			settings={},
			preview_texture_name='stepRightUpPreview')]

class Player(ba.Player['Team']):
    """Our player type for this game."""


class Team(ba.Team[Player]):
    """Our team type for this game."""


# ba_meta export game
class BatallaExtrema(ba.TeamGameActivity[Player, Team]):
    """
    A co-op game where you try to defeat a group
    of Ninjas as fast as possible
    """

    name = 'Batalla Extrema'
    description = 'Acaba lo antes posible(SIN HACKS)'
    scoreconfig = ba.ScoreConfig(label='Time',
                                 scoretype=ba.ScoreType.MILLISECONDS,
                                 lower_is_better=True)
    default_music = ba.MusicType.TO_THE_DEATH

    @classmethod
    def get_supported_maps(cls, sessiontype: type[ba.Session]) -> list[str]:
        # For now we're hard-coding spawn positions and whatnot
        # so we need to be sure to specify that we only support
        # a specific map.
        return ['Step Right Up']

    @classmethod
    def supports_session_type(cls, sessiontype: type[ba.Session]) -> bool:
        # We currently support Co-Op only.
        return issubclass(sessiontype, ba.CoopSession)

    # In the constructor we should load any media we need/etc.
    # ...but not actually create anything yet.
    def __init__(self, settings: dict):
        super().__init__(settings)
        self._winsound = ba.getsound('score')
        self._won = False
        self._timer: Optional[OnScreenTimer] = None
        self._bots = SpazBotSet()
        self._bots_pos: list = [(4.6196701116, 5.110914413, -4.292515158),
                                (-4.6196701116, 5.110914413, -4.292515158)]
        self._bots_pos2: list = [(4.6196701116, 5.110914413, -6.292515158),
                                 (4.6196701116, 5.110914413, -2.292515158),
                                 (-4.6196701116, 5.110914413, -6.292515158),
                                 (-4.6196701116, 5.110914413, -2.292515158)]
        self._bots_pos3: list = [(0.9196701116, 5.110914413, -6.292515158),
                                 (0.3196701116, 5.110914413, -6.292515158),
                                 (7.1196701116, 5.110914413, 2.292515158),
                                 (-7.1196701116, 5.110914413, 2.292515158)]
        self._bots_pos4: list = [(0.9196701116, 5.110914413, -6.292515158),
                                 (0.3196701116, 5.110914413, -6.292515158),
                                 (7.1196701116, 5.110914413, 2.292515158),
                                 (-7.1196701116, 5.110914413, 2.292515158)]
        self._bots_pos5: list = [(7.9196701116, 6.310914413, -4.292515158),
                                 (-7.3196701116, 6.310914413, -4.292515158)]
        self._bots_pos6: list = [(8.8196701116, 8.310914413, -4.292515158),
                                 (-8.8196701116, 8.310914413, -4.292515158)]
        self._bots_pos7: list = (0.3196701116, 5.110914413, 2.292515158)

    # Called when our game actually begins.
    def on_begin(self) -> None:
        super().on_begin()
        self.setup_standard_powerup_drops()

        # Make our on-screen timer and start it roughly when our bots appear.
        self._timer = OnScreenTimer()
        ba.timer(2.0, self._timer.start)

        for i in range(2):
            self._spawn_bots(
                BomberBotStaticLite, 6.0, 2.0, self._bots_pos[i])

        for i in range(4):
            self._spawn_bots(
                BomberBotStatic, 12.0, 9.0, self._bots_pos2[i])

        for i in range(4):
            self._spawn_bots(
                BrawlerBotLite, 24.0, 9.0, self._bots_pos3[i])

        for i in range(4):
            self._spawn_bots(
                BrawlerBot, 36.0, 9.0, self._bots_pos4[i])

        for i in range(2):
            self._spawn_bots(
                StickyBotStatic, 45.0, 9.0, self._bots_pos5[i])

        for i in range(2):
            self._spawn_bots(
                ExplodeyBotNoTimeLimit, 60.0, 9.0, self._bots_pos6[i])

        ba.timer(6.0, lambda: self._bots.spawn_bot(
            BrawlerBotProShielded, pos=self._bots_pos7, spawn_time=80.0))

    def _spawn_bots(self, bot: Any, time: float,
                    spawn_time: float, pos: float) -> None:
        ba.timer(time, lambda: self._bots.spawn_bot(
            bot, pos=pos, spawn_time=spawn_time))

    # Called for each spawning player.
    def spawn_player(self, player: Player) -> ba.Actor:

        # Let's spawn close to the center.
        spawn_center = (0.3196, 5.1109, -4.2925)
        pos = (spawn_center[0] + random.uniform(-1.5, 1.5), spawn_center[1],
               spawn_center[2] + random.uniform(-1.5, 1.5))
        return self.spawn_player_spaz(player, position=pos)

    def _check_if_won(self) -> None:
        # Simply end the game if there's no living bots.
        # FIXME: Should also make sure all bots have been spawned;
        #  if spawning is spread out enough that we're able to kill
        #  all living bots before the next spawns, it would incorrectly
        #  count as a win.
        if not self._bots.have_living_bots():
            self._won = True
            self.end_game()

    # Called for miscellaneous messages.
    def handlemessage(self, msg: Any) -> Any:

        # A player has died.
        if isinstance(msg, ba.PlayerDiedMessage):
            super().handlemessage(msg)  # Augment standard behavior.
            self.respawn_player(msg.getplayer(Player))

        # A spaz-bot has died.
        elif isinstance(msg, SpazBotDiedMessage):
            # Unfortunately the bot-set will always tell us there are living
            # bots if we ask here (the currently-dying bot isn't officially
            # marked dead yet) ..so lets push a call into the event loop to
            # check once this guy has finished dying.
            ba.pushcall(self._check_if_won)

        # Let the base class handle anything we don't.
        else:
            return super().handlemessage(msg)
        return None

    # When this is called, we should fill out results and end the game
    # *regardless* of whether is has been won. (this may be called due
    # to a tournament ending or other external reason).
    def end_game(self) -> None:

        # Stop our on-screen timer so players can see what they got.
        assert self._timer is not None
        self._timer.stop()

        results = ba.GameResults()

        # If we won, set our score to the elapsed time in milliseconds.
        # (there should just be 1 team here since this is co-op).
        # ..if we didn't win, leave scores as default (None) which means
        # we lost.
        if self._won:
            elapsed_time_ms = int((ba.time() - self._timer.starttime) * 1000.0)
            ba.cameraflash()
            ba.playsound(self._winsound)
            for team in self.teams:
                for player in team.players:
                    if player.actor:
                        player.actor.handlemessage(ba.CelebrateMessage())
                results.set_team_score(team, elapsed_time_ms)

        # Ends the activity.
        self.end(results)
