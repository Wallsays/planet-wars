#!/usr/bin/env python
#

"""
// The DoTurn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist. Inside this function, you issue orders using the
// pw.IssueOrder() function. For example, to send 10 ships from planet 3 to
// planet 8, you would say pw.IssueOrder(3, 8, 10).
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own. Check out the tutorials and articles on the contest website at
// http://www.ai-contest.com/resources.
"""
from PlanetWars import PlanetWars

import sys

def DoTurn(pw, group_ids):
  # (1) If we currently have a fleet in flight, just do nothing.
  if len(pw.MyFleets()) >= 2:
    return
  # (2) Find my strongest planet.
  source = -1
  source_score = -999999.0
  source_num_ships = 0
  my_planets = pw.MyPlanets()
  for p in my_planets:
    score = float(p.NumShips())
    if score > source_score:
      source_score = score
      source = p.PlanetID()
      source_num_ships = p.NumShips()

  # (3) Find the weakest enemy or neutral planet.
  dest = -1
  dest_score = -999999.0
  not_my_planets = pw.NotMyPlanets()

  # (3.1) remove group members planets from list
  tmp = []
  for p in not_my_planets:
    if p.Owner() in group_ids:
      continue
    tmp.append(p)
  not_my_planets = tmp
  
  # (3.2) remove planets which awaiting group member fleets
  planet_ids = [] # not_my_planets ids
  if not_my_planets:
    planet_ids = ([p.PlanetID() for p in not_my_planets])
  gfp_ids = [] # group_fleet_planet_ids
  for fl in pw.EnemyFleets():
    if fl.Owner() in group_ids and fl.DestinationPlanet() in planet_ids:
      gfp_ids.append(fl.DestinationPlanet())
  gfp_ids = set(gfp_ids)

  for p in not_my_planets:
    score = 1.0 / (1 + p.NumShips())
    if score > dest_score:
      dest_score = score
      dest = p.PlanetID()

  # (4) Send half the ships from my strongest planet to the weakest
  # planet that I do not own.
  if source >= 0 and dest >= 0:
    num_ships = source_num_ships / 2
    pw.IssueOrder(source, dest, num_ships)


def main():
  f = open('MyBot3.log', 'w')
  group_ids = []
  if '-g' in sys.argv:
    group_ids = [int(k) for k in sys.argv[2].split(',')]
  f.write('group: ' + str(group_ids) + '\n')

  map_data = ''
  while(True):
    current_line = raw_input()
    f.write(current_line + '\n')
    if len(current_line) >= 1 and current_line.startswith("."):
      pw = PlanetWars(map_data)
      DoTurn(pw, group_ids)
      pw.FinishTurn()
      map_data = ''
    else:
      map_data += current_line + '\n'


if __name__ == '__main__':
  try:
    import psyco
    psyco.full()
  except ImportError:
    pass
  try:
    main()
  except KeyboardInterrupt:
    print 'ctrl-c, leaving ...'
