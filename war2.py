#!/usr/local/bin/python
# war2, a script to repeatedly play games using the python engine
# Copyright (C) 2010 Benjamin S Wolf
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Benjamin S Wolf <jokeserver@gmail.com>

import os
import sys
import engine

def runnable_ize(bot):
    if bot.endswith(".jar"):
        return 'java -jar %s' % bot
    else:
        # return './%s' % bot
        return bot

def main(map, bots, gui=False):
    players = [ { "path" : ".", "command" : runnable_ize(bot) } for bot in bots]
    mapfile = "maps/map%s.txt" % map
    outcome = engine.play_game(mapfile, 1000, 70, players, False)
    sys.stdout.write("game result: \n%s\n" %\
            "\n".join(["%s: %s" % (a,b) for (a,b) in outcome.iteritems()
                                        if a != "playback"]))
    if gui:
        with open("playback.log", "w") as f:
            f.write(outcome["playback"])
        os.system("java -jar tools/ShowGame.jar < playback.log")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.stderr.write("""Usage: %s <n> <bot1> <bot2> [bot3, ...] [--gui]
to play a game with bot1 against bot2 (and optionally more) on map n,
with a time limit of <time> milliseconds for each turn, for <turns> turns.
Add the flag --gui to display the game in gui mode once it is done.
""" % sys.argv[0])
        sys.exit(1)
    if sys.argv[-1] == "--gui":
        main(sys.argv[1], sys.argv[2:-1], True)
    else:
        main(sys.argv[1], sys.argv[2:])
