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
from PlanetWars import Planet

import sys

distances = []
nearestNeighbors = []

def Distance(p1id, p2id, f):
  # f.write('check: 1.3.1'+ '\n')
  if isinstance(p1id, Planet) and isinstance(p2id, Planet):
    # f.write('check: 1.3.2'+ '\n')
    return distances[p1id.PlanetID()][p2id.PlanetID()][1]
  # f.write('check: 1.3.3'+ '\n')
  return distances[p1id][p2id][1]

def ComputePlanetDistances(pw, f):
  planets = sorted(pw.Planets(), key=lambda x: x.PlanetID())
  # f.write('check: 1.1'+ '\n')
  # f.write('planets: ' + ', '.join([str( p.PlanetID() ) for p in planets]) + '\n')
  for p in planets:
    # f.write('check: 1.2'+ '\n')
    dists = []
    for q in planets:
      # f.write('check: 1.3'+ '\n')
      dists.append((q.PlanetID(), pw.Distance(p.PlanetID(),q.PlanetID())))
      # f.write('check: 1.4'+ '\n')
    nearestNeighbors.append(sorted(dists, key=lambda x: x[1]))
    # f.write('check: 1.5'+ '\n')
    distances.append(dists)

def DoTurn(pw, group_ids, f):
  orders = []
  urgentPlanets = []
  enemyTargets = []
  myTargets = []
  # Planets
  myPlanets = pw.MyPlanets()
  alliesPlanets = []
  neutralPlanets = pw.NeutralPlanets()
  enemyPlanets = pw.EnemyPlanets()
  # Fleets
  myFleets = pw.MyFleets()
  alliesFleets = pw.EnemyFleets()
  enemyFleets = pw.EnemyFleets()
  # Ship count
  mySize = 0
  alliesSize = 0
  enemySize = 0
  # Ships growth
  myGrowth = 0
  alliesGrowth = 0
  enemyGrowth = 0

  # f.write('check: 1'+ '\n')
  # Interplanetary distances will come in handy
  if not distances:
    ComputePlanetDistances(pw, f)
  # f.write('check: 2'+ '\n')
  
  # Allies planets
  for p in enemyPlanets:
    if p.Owner() in group_ids:
      alliesPlanets.append(p)

  # My power
  for p in pw.MyPlanets():
    mySize += p.NumShips()
    myGrowth += p.GrowthRate()

  # Allies power
  for p in enemyPlanets:
    if p.Owner() in group_ids:
      alliesSize += p.NumShips()
      alliesGrowth += p.GrowthRate()

  # Enemies power
  for p in enemyPlanets:
    enemySize += p.NumShips()
    enemyGrowth += p.GrowthRate()

  # Enemies targets
  for fleet in pw.EnemyFleets():
    if fleet.Owner() in group_ids:
      continue
    enemyTargets.append(fleet)

  if ( enemySize <= 0 ):
    winRatio = 0
  else:
    winRatio = float(mySize + alliesSize)/enemySize

  f.write('winRatio: ' + str(winRatio) + '\n')

  # urgentPlanets.sort(key=lambda x: x[0].GrowthRate(), reverse=True)  

  # Defence
  for fleet in enemyTargets:
    my_planet_ids = ([p.PlanetID() for p in myPlanets])
    if fleet.DestinationPlanet() in my_planet_ids:
      f.write('DANGER: ' + str(fleet.NumShips()) + '\n')
      urgentPlanets.append( )



  # Spread strategy
  if len(myPlanets) <= 3 and len(neutralPlanets) > 5 :
    # nearest_planets = neutralPlanets.sort(key=lambda x: x.GrowthRate(), reverse=True)  
    # nearest_planets = sorted(neutralPlanets, key=lambda x: x.GrowthRate(), reverse=True )
    # f.write('nearest_planets: ' + ', '.join([str( p.NumShips() ) for p in nearest_planets]) + '\n')
    # nearest_planets = []
    f.write('myPlanets: ' + ', '.join([str( p.NumShips() ) for p in myPlanets]) + '\n')
    plannedSend = []
    for hunter in myPlanets:
      ship_avail = hunter.NumShips()
      for meat in sorted(neutralPlanets, key=lambda x: Distance(x,hunter,f))[:2]:
        req_send = meat.NumShips() + int(ship_avail*.10)
        if ship_avail > req_send:
          ship_avail -= req_send
          plannedSend.append((hunter, meat, req_send))


    # for meat in neutralPlanets:
    #   f.write('meat: ' + str(meat.NumShips()) + '\n')
    #   totalNeeded = meat.NumShips()
    #   helpsofar = 0
    #   # Prefer close hunting
    #   for hunter in sorted(myPlanets, key=lambda x: Distance(x,meat,f)):
    #     f.write('hunter: ' + str(hunter.NumShips()) + '\n')
    #     tosend = hunter.NumShips()
    #     plannedSend.append((hunter, meat, tosend))
    #     helpsofar += tosend
    #     if helpsofar >= totalNeeded:
    #       break
    #   f.write('-----------------------------<<<\n')

    for plan in plannedSend:
      f.write('-----------------------------\n')
      f.write('plan[0]: ' + str(plan[0].NumShips()) + '\n')
      f.write('plan[1]: ' + str(plan[1].NumShips()) + '\n')
      f.write('plan[2]: ' + str(plan[2]) + '\n')
      f.write('-----------------------------\n')
      pw.IssueOrder(plan[0].PlanetID(), plan[1].PlanetID(), plan[2])

      
    # f.write('nearest_planets: ' + ', '.join([str( p.PlanetID() ) for p in nearest_planets]) + '\n')


      # nearest_planets.append()

  # else:
  #   return
  

  # # (1) If we currently have a fleet in flight, just do nothing.
  # if len(pw.MyFleets()) >= 2:
  #   return

  # # (2) Find my strongest planet.
  # source = -1
  # source_score = -999999.0
  # # source_num_ships = 0
  # my_planets = pw.MyPlanets()
  # for p in my_planets:
  #   score = float(p.NumShips())
  #   if score > source_score:
  #     source_score = score
  #     source = p #.PlanetID()
  #     # source_num_ships = p.NumShips()

  # # (3) Find the weakest enemy or neutral planet.
  # # dest = -1
  # # dest_score = -999999.0
  # not_my_planets = pw.NotMyPlanets()
  
  # # (3.1) remove group members planets from list
  # tmp = []
  # for p in not_my_planets:
  #   if p.Owner() in group_ids:
  #     continue
  #   tmp.append(p)
  # not_my_planets = tmp
  # # f.write('not_my_planets: ' + ', '.join([str( p.Owner() ) for p in not_my_planets]) + '\n')
  
  # # (3.2) remove planets which awaiting group member fleets
  # planet_ids = [] # not_my_planets ids
  # if not_my_planets:
  #   planet_ids = ([p.PlanetID() for p in not_my_planets])
  # # f.write('planet_ids: ' + ', '.join([str( p ) for p in planet_ids]) + '\n')
  # # f.write('planet_ids: ' + ', '.join([str( p ) for p in planet_ids]) + '\n')
  # gfp_ids = [] # group_fleet_planet_ids
  # # gfp_need_help_ids = [] # group_fleet_planet_ids
  # # f.write('EnemyFleets DestinationPlanets: ' + ', '.join([str( fl.DestinationPlanet() ) for fl in pw.EnemyFleets() ]) + '\n')
  # for fl in pw.EnemyFleets():
  #   # f.write('fl.NumShips(): ' + str(fl.NumShips()) + '\n')
  #   # f.write('fl.DestinationPlanet(): ' + str(fl.DestinationPlanet()) + '\n')
  #   # f.write('fl.DestinationPlanet().NumShips(): ' + str(fl.DestinationPlanet().NumShips()) + '\n')
  #   if fl.Owner() in group_ids and fl.DestinationPlanet() in planet_ids: # and fl.NumShips() > fl.DestinationPlanet().NumShips(): #  + fl.DestinationPlanet().GrowthRate() * fl.TurnsRemaining() ):
  #     gfp_ids.append(fl.DestinationPlanet())
  # gfp_ids = set(gfp_ids)
  # # f.write('gfp_ids: ' + ', '.join([str( fl ) for fl in gfp_ids]) + '\n')

  # # (3.3) calculate enemy planets which need help from team-mates
  # need_help_p = []
  # for p in not_my_planets:
  #   if p.PlanetID() in gfp_ids and p.Owner() == 2 :
  #     ships_awaiting = 0 
  #     for fl in pw.EnemyFleets():
  #       if fl.Owner() in group_ids and fl.DestinationPlanet() == p.PlanetID():
  #         ships_awaiting += fl.NumShips()
  #     # f.write('ships_awaiting: ' + str(ships_awaiting) + '\n')
  #     if ships_awaiting < ( p.NumShips() + p.GrowthRate() * fl.TurnsRemaining() ):
  #       need_help_p.append(p)
  # f.write('need_help_p ids: ' + ', '.join([str( pl.PlanetID() ) for pl in need_help_p ]) + '\n')
  

  # # (3.4) remove planets which awaiting my fleets
  # my_fp_ids = [] # my_fleet_planet_ids
  # # f.write('EnemyFleets DestinationPlanets: ' + ', '.join([str( fl.DestinationPlanet() ) for fl in pw.EnemyFleets() ]) + '\n')
  # for fl in pw.MyFleets():
  #   if fl.DestinationPlanet() in planet_ids:
  #     my_fp_ids.append(fl.DestinationPlanet())
  # my_fp_ids = set(my_fp_ids)

  # # ATTACK Planets
  # # not_my_planets

  # # (4) analyze planets
  # # not_my_planets = tmp
  # # f.write('not_my_planets: ' + ', '.join([str( p.Owner() ) for p in not_my_planets]) + '\n')
  # planets_rank = [] 
  # need_help_pids = ([p.PlanetID() for p in need_help_p])
  # f.write('need_help_pids: ' + ', '.join([str( p ) for p in need_help_pids]) + '\n')
  # for p in not_my_planets:
  #   # if p.PlanetID() in gfp_ids or p.PlanetID() in my_fp_ids:
  #   if (p.PlanetID() in gfp_ids and p.PlanetID() not in need_help_pids) or p.PlanetID() in my_fp_ids:
  #     continue 
  #   safety = 1.0
  #   tmp = []
  #   for plt in not_my_planets:
  #     # distance to enemy planets
  #     if plt.PlanetID() in gfp_ids or plt.PlanetID() in my_fp_ids or plt.Owner() == 0:
  #       continue
  #     tmp.append(pw.Distance(p.PlanetID(), plt.PlanetID())) 
  #   if tmp != 0:
  #     f.write('tmp: ' + ', '.join([str( ttt ) for ttt in tmp]) + '\n')
  #     tmp.sort(reverse=True)
  #     f.write('tmp: ' + ', '.join([str( ttt ) for ttt in tmp]) + '\n')
  #     safety = safety / (sum(tmp[:5]) + 1.0)
  #     f.write('safety: ' + str(safety) + '\n')

  #   # planet's score for obtaining
  #   # score = (1.0 * p.GrowthRate() ) / (1 + p.NumShips()**pw.Distance(source.PlanetID(), p.PlanetID())) 
  #   score = (1.0 + p.GrowthRate()/source.GrowthRate() + safety) / (1.0 + p.NumShips()/source.NumShips() + 2**pw.Distance(source.PlanetID(), p.PlanetID())) 
  #   planets_rank.append([p, score])
  #   # if score > dest_score:
  #   #   dest_score = score
  #   #   dest = p #.PlanetID()
  # # f.write('planets_rank: ' + ', '.join([str( p[1] ) for p in planets_rank]) + '\n')
  # planets_rank.sort(key=lambda x: x[1], reverse=True)
  # f.write('planets_rank Owner: ' + ', '.join([str( p[0].Owner() ) for p in planets_rank]) + '\n')
  # # f.write('planets_rank NumShips: ' + ', '.join([str( p[0] ) for p in planets_rank]) + '\n')
  # f.write('planets_rank: ' + ', '.join([str( p[1] ) for p in planets_rank]) + '\n')

  # # (5) Send ships from my strongest planet to others
  # sent_ships = 0
  # for elem in planets_rank:
  #   f.write('planet: ' + str(elem[0]) + '\n')
  #   f.write('planets score: ' + str(elem[1]) + '\n')
  #   if (source.NumShips() - sent_ships * 3) <= 0:
  #     return
  #   dest = elem[0] # planet
  #   req_num_ships = dest.NumShips()
  #   f.write('req_num_ships: ' + str(req_num_ships) + '\n')
  #   add_ships = 1
  #   f.write('dest.Owner(): ' + str(dest.Owner()) + '\n')
  #   if dest.Owner() != 0 and dest.Owner() not in group_ids: # foe (not neutral)
  #     add_ships += dest.GrowthRate()  * int(pw.Distance(source.PlanetID(), dest.PlanetID() ))
  #     f.write('add_ships: ' + str(add_ships) + '\n')
  #   num_ships = req_num_ships * 2 + add_ships
  #   # num_ships = req_num_ships * 2 - req_num_ships/4 + add_ships
  #   f.write('num_ships: ' + str(num_ships) + '\n')
  #   if (source.NumShips() - sent_ships - num_ships) >= 0:
  #     sent_ships += num_ships
  #     pw.IssueOrder(source.PlanetID(), dest.PlanetID(), num_ships)





def main():
  f = open('MyBot2.log', 'w')
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
      f.write('--------------- NEW TURN ----------------------------\n')
      DoTurn(pw, group_ids, f)
      f.write('-----------------------------------------------------\n')
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
