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

def DoTurn(pw, group_ids, f):
  # (1) If we currently have a fleet in flight, just do nothing.
  if len(pw.MyFleets()) >= 2:
    return

  # (2) Find my strongest planet.
  source = -1
  source_score = -999999.0
  # source_num_ships = 0
  my_planets = pw.MyPlanets()
  for p in my_planets:
    score = float(p.NumShips())
    if score > source_score:
      source_score = score
      source = p #.PlanetID()
      # source_num_ships = p.NumShips()

  # (3) Find the weakest enemy or neutral planet.
  # dest = -1
  # dest_score = -999999.0
  not_my_planets = pw.NotMyPlanets()
  
  # (3.1) remove group members planets from list
  tmp = []
  for p in not_my_planets:
    if p.Owner() in group_ids:
      continue
    tmp.append(p)
  not_my_planets = tmp
  # f.write('not_my_planets: ' + ', '.join([str( p.Owner() ) for p in not_my_planets]) + '\n')
  
  # (3.2) remove planets which awaiting group member fleets
  planet_ids = [] # not_my_planets ids
  if not_my_planets:
    planet_ids = ([p.PlanetID() for p in not_my_planets])
  # f.write('planet_ids: ' + ', '.join([str( p ) for p in planet_ids]) + '\n')
  # f.write('planet_ids: ' + ', '.join([str( p ) for p in planet_ids]) + '\n')
  gfp_ids = [] # group_fleet_planet_ids
  # f.write('EnemyFleets DestinationPlanets: ' + ', '.join([str( fl.DestinationPlanet() ) for fl in pw.EnemyFleets() ]) + '\n')
  for fl in pw.EnemyFleets():
    if fl.Owner() in group_ids and fl.DestinationPlanet() in planet_ids:
      gfp_ids.append(fl.DestinationPlanet())
  gfp_ids = set(gfp_ids)
  # f.write('gfp_ids: ' + ', '.join([str( fl ) for fl in gfp_ids]) + '\n')

  # (3.3) remove planets which awaiting my fleets
  my_fp_ids = [] # my_fleet_planet_ids
  # f.write('EnemyFleets DestinationPlanets: ' + ', '.join([str( fl.DestinationPlanet() ) for fl in pw.EnemyFleets() ]) + '\n')
  for fl in pw.MyFleets():
    if fl.DestinationPlanet() in planet_ids:
      my_fp_ids.append(fl.DestinationPlanet())
  my_fp_ids = set(my_fp_ids)

  # ATTACK Planets
  # not_my_planets

  # (4) analyze planets
  # not_my_planets = tmp
  # f.write('not_my_planets: ' + ', '.join([str( p.Owner() ) for p in not_my_planets]) + '\n')
  planets_rank = [] 
  for p in not_my_planets:
    if p.PlanetID() in gfp_ids or p.PlanetID() in my_fp_ids:
      continue 
    # planet's score for obtaining
    score = (1.0 * p.GrowthRate() ) / (1 + p.NumShips() + pw.Distance(source.PlanetID(), p.PlanetID())) 
    planets_rank.append([p, score])
    # if score > dest_score:
    #   dest_score = score
    #   dest = p #.PlanetID()
  # f.write('planets_rank: ' + ', '.join([str( p[1] ) for p in planets_rank]) + '\n')
  planets_rank.sort(key=lambda x: x[1], reverse=True)
  f.write('planets_rank Owner: ' + ', '.join([str( p[0].Owner() ) for p in planets_rank]) + '\n')
  # f.write('planets_rank NumShips: ' + ', '.join([str( p[0] ) for p in planets_rank]) + '\n')
  f.write('planets_rank: ' + ', '.join([str( p[1] ) for p in planets_rank]) + '\n')

  # (5) Send ships from my strongest planet to others
  sent_ships = 0
  for elem in planets_rank:
    f.write('planet: ' + str(elem[0]) + '\n')
    f.write('planets score: ' + str(elem[1]) + '\n')
    if (source.NumShips() - sent_ships * 3) <= 0:
      return
    dest = elem[0] # planet
    req_num_ships = dest.NumShips()
    f.write('req_num_ships: ' + str(req_num_ships) + '\n')
    add_ships = 1
    if dest.Owner() == 2: # foe (not neutral)
      add_ships += dest.GrowthRate()  * int(pw.Distance(source.PlanetID(), dest.PlanetID() ))
      f.write('add_ships: ' + str(add_ships) + '\n')
    num_ships = req_num_ships * 2 + add_ships
    f.write('num_ships: ' + str(num_ships) + '\n')
    if (source.NumShips() - sent_ships - num_ships) >= 0:
      sent_ships += num_ships
      pw.IssueOrder(source.PlanetID(), dest.PlanetID(), num_ships)





def main():
  f = open('MyBot2_log.txt', 'w')
  group_ids = []
  if '-g' in sys.argv:
    group_ids = [int(k) for k in sys.argv[2].split(',')]
  f.write('group: ' + str(group_ids) + '\n')

  map_data = ''
  while(True):
    current_line = raw_input()
    f.write(current_line + '\n')
    if len(current_line) >= 2 and current_line.startswith("go"):
      pw = PlanetWars(map_data)
      DoTurn(pw, group_ids, f)
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
