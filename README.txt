

Current strategy - "Kill Game":
  1. Gang murder if my next-targets in any message from team-mate
  1. Analyze enemy planets
  2. Hit 'em from most closest and powerfull planets
  3. Send next 3 targets in message

Messaging algo:
  1. Send planet-ID on first turn
  2. Send 3 next-targets

Other:
  - EndTurn message changed from default 'go' to '.'
  - Task bot - MyBot4.py in root dir
  - How to run:
    1. Runner. Cmd: 'bash runner.sh' - there few examples (last paragrapth 
       section should work)
    2. war2. Cmd: 'python ./war2 <map number> <bot1> <bot2> [bot3, ...] [--gui]'
      * Run a game using a modified version of the official game engine.
      * The timeout is preset to 1000 milliseconds and the turn limit is 200.
      * These can be changed in the script itself.
      *
      * As in war, each bot is a filename, either a jar or an executable.
      * You don't need to include the "java -jar" or the "./" as the script 
      * will add those for you.
      *
      * You can include any number of bots this way. However, the map must 
      * have more planets than bots. Each bot numbered n will start with
      * Planet ID n (so players 1, 2, 3 get planets 1, 2, 3).
      *
      * The map number is just a number.
      *
      * Add the flag --gui to record the playback from the game to playback.log
      * and feed that to the Java visualizer included in your starter package.
    3. Note: current turns count limit up 70 due to slow proccessing.
       U can change it in was2.py on 34-th line.
    

Improvements (next version);
  General Strategy:
    1. Don't lose planets
    2. Make ships faster than the enemy
    3. Minimize enemy's ships growth rate
    4. Minimize distance when ships are sent
  Messaging:
    1. Add game styles (kill/spread/growth-mode like DualBot, but on group-level)
    2. Smart planets obtaining:
      a) Landing player1 army (or several armies if it's neutral) to 
         kill all ships on planet
      b) Landing player2 army to occupy and protect planet from initial invasion
    3. Note: we don't need voting feature (for leader) coz every bot
             can analyze each other situation
  IceBox:
    1. Simulate next enemy turns



-----------------------------------------------------------------------------

The files in this package are part of a starter package from the Google AI
Challenge. The Google AI Challenge is an Artificial Intelligence programming
contest. You can get more information by visiting www.ai-contest.com.

The entire contents of this starter package are released under the Apache
license as is all code related to the Google AI Challenge. See
code.google.com/p/ai-contest/ for more details.

There are a bunch of tutorials on the ai-contest.com website that tell you
what to do with the contents of this starter package. For the impatient, here
is a brief summary.
  * In the root directory, there are a bunch of code files. These are a simple
    working contest entry that employs a basic strategy. These are meant to be
    used as a starting point for you to start writing your own entry.
    Alternatively, you can just package up the starter package as-is and submit
    it on the website.
  * The tools directory contains a game engine and visualizer. This is meant
    to be used to test your bot. See the relevant tutorials on the website for
    information about how to use the tools.
  * The example_bots directory contains some sample bots for you to test your
    own bot against.
