# ba_meta require api 6

#Copy pasted from ExplodoRun by Blitz,just edited Bots and map 😝


from __future__ import annotations

import random
from typing import TYPE_CHECKING

import ba
from bastd.actor.spazbot import SpazBotSet, ChargerBot, SpazBotDiedMessage
from bastd.actor.onscreentimer import OnScreenTimer

if TYPE_CHECKING:
    from typing import Any, Type, Dict, List, Optional

## MoreMinigames.py support ##
def ba_get_api_version():
    return 6

def ba_get_levels():
    return [ba._level.Level(
            'Infinite Ninjas',gametype=InfiniteNinjasGame,
            settings={},
            preview_texture_name = 'footballStadiumPreview'),
            ba._level.Level(
            'Epic Infinite Ninjas',gametype=InfiniteNinjasGame,
            settings={'Epic Mode':True},
            preview_texture_name = 'footballStadiumPreview')]
## MoreMinigames.py support ##

class Player(ba.Player['Team']):
    """Our player type for this game."""


class Team(ba.Team[Player]):
    """Our team type for this game."""

# ba_meta export game
class InfiniteNinjasGame(ba.TeamGameActivity[Player, Team]):
    name = "Infinite Ninjas"
    description = "How long can you survive from Ninjas??"
    available_settings = [ba.BoolSetting('Epic Mode', default=False)]
    scoreconfig = ba.ScoreConfig(label='Time',
                                 scoretype=ba.ScoreType.MILLISECONDS,
                                 lower_is_better=False)
    default_music = ba.MusicType.TO_THE_DEATH
    
    def __init__(self, settings:dict):
        settings['map'] = "Football Stadium"
        self._epic_mode = settings.get('Epic Mode', False)
        if self._epic_mode:
            self.slow_motion = True
        super().__init__(settings)
        self._timer: Optional[OnScreenTimer] = None
        self._winsound = ba.getsound('score')
        self._won = False
        self._bots = SpazBotSet()
        self.wave = 1
    
    def on_begin(self) -> None:
        super().on_begin()
        
        self._timer = OnScreenTimer()
        ba.timer(2.5, self._timer.start)
        
        #Bots Hehe
        ba.timer(2.5,self.street)

    def street(self):
        for a in range(self.wave):
            p1 = random.choice([-5,-2.5,0,2.5,5])
            p3 = random.choice([-4.5,-4.14,-5,-3])
            time = random.choice([1,1.5,2.5,2])
            self._bots.spawn_bot(ChargerBot, pos=(p1,0.4,p3),spawn_time = time)
        self.wave += 1
        
    def botrespawn(self):
        if not self._bots.have_living_bots():
            self.street()
    def handlemessage(self, msg: Any) -> Any:

        # A player has died.
        if isinstance(msg, ba.PlayerDiedMessage):
            super().handlemessage(msg)  # Augment standard behavior.
            self._won = True
            self.end_game()
        
        # A spaz-bot has died.
        elif isinstance(msg, SpazBotDiedMessage):
            # Unfortunately the bot-set will always tell us there are living
            # bots if we ask here (the currently-dying bot isn't officially
            # marked dead yet) ..so lets push a call into the event loop to
            # check once this guy has finished dying.
            ba.pushcall(self.botrespawn)

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
    
    