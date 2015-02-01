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

import random
import sys

messageHistory = []
allies_nicks = []
next_targets = []


def DoTurn(pw, group_ids, nickname, f):
  commandGame = False

  # send planet position
  if not messageHistory:
    mes = pw.MyPlanets()[0].PlanetID()
    pw.SendMessage(nickname,mes)
  # else:
  #   mes = random.randint(-214783648, 2147483647)

  # write message log
  tmp = []
  for mes in pw.Messages():
    tmp.append((mes.Nickname(), mes.Number()))
  messageHistory.append(tmp)


  # # find out and remember party nickname  
  if not allies_nicks and messageHistory:
    tmp = messageHistory[-1]
    for msh in tmp:
      # f.write('=====msh[1]' + str(msh[1] ) + '\n')
      for pln in pw.Planets():
        if pln.PlanetID() == int(msh[1]) and \
          pln.Owner() in group_ids:
          # f.write('=====if' + str(pln.PlanetID() ) + '\n')
          for gip in group_ids:
            if pln.Owner() == int(gip):
              allies_nicks.append(( msh[0], pln.Owner() ))
              # f.write('=====planet.Owner()' + str(pln.Owner() ) + '\n')
              
  f.write('last mes: ' + str(messageHistory[-1]) + '\n')
  f.write('allies_nicks ' + str(allies_nicks) + '\n')

  # Ship count
  mySize = 0
  alliesSize = 0
  enemySize = 0
  # Ships growth
  myGrowth = 0
  alliesGrowth = 0
  enemyGrowth = 0
  # Planets
  myPlanets = []
  enemyPlanets = []
  alliesPlanets = []
  # Fleets
  myFleets = []
  partyFleets = []
  alliesFleets = []
  enemyFleets = []

  # Group fleets
  for fleet in pw.Fleets():
    if fleet.Owner() == 1 or \
      fleet.Owner() in group_ids:
      partyFleets.append(fleet)

  # My fleets
  for fleet in pw.MyFleets():
    myFleets.append(fleet)

  # Allies fleets
  for fleet in pw.EnemyFleets():
    if fleet.Owner() in group_ids:
      alliesFleets.append(fleet)

  # Enemy fleets
  for fleet in pw.EnemyFleets():
    if fleet.Owner() not in group_ids:
      enemyFleets.append(fleet)

  # My power
  for p in pw.MyPlanets():
    myPlanets.append(p)
    mySize += p.NumShips()
    myGrowth += p.GrowthRate()

  # Allies power
  for p in pw.EnemyPlanets():
    if p.Owner() in group_ids:
      alliesPlanets.append(p)
      alliesSize += p.NumShips()
      alliesGrowth += p.GrowthRate()

  # Enemies power
  for p in pw.EnemyPlanets():
    if p.Owner() not in group_ids:
      enemyPlanets.append(p)
      enemySize += p.NumShips()
      enemyGrowth += p.GrowthRate()

  if ( enemySize <= 0 ):
    winRatio = 0
  else:
    winRatio = float(mySize)/enemySize
  
  f.write('winRatio: ' + str(winRatio) + '\n')

  # available ships
  available_ships = {}
  for my_pln in myPlanets:
    available_ships[my_pln.PlanetID()] = my_pln.NumShips()
  f.write('available_ships: ' + str(available_ships) + '\n')


  f.write('======= Stop Spreading Enemy on NP ======= \n')
  for efl in enemyFleets:
    if efl.TurnsRemaining() < 5 and\
      pw.GetPlanet(efl.DestinationPlanet()).Owner() == 0:
      enemyPlanets.append(pw.GetPlanet(efl.DestinationPlanet()))

  f.write('======= Co-op Targets Processing ======= \n')
  if len(messageHistory) > 2:
    for msh in messageHistory[-1]:
      if msh[0] in ([nick[0] for nick in allies_nicks]):
        # f.write('pick: ' + str(msh[0]) + '\n')
        targets = []
        targets.append(int(str(msh[1])[0:3:]) - 100)
        targets.append(int(str(msh[1])[3:6:]) - 100)
        targets.append(int(str(msh[1])[6:9:]) - 100)
        f.write('targets: ' + str(targets) + '\n')
        for trg in targets:
          f.write('next_targets: ' + str(next_targets) + '\n')
          if trg in next_targets:
            att_pln = pw.GetPlanet(trg)
            # f.write('att_pln: ' + str(att_pln) + '\n')
            req_ships = int(att_pln.NumShips() * .10)
            f.write('req_ships: ' + str(req_ships) + '\n')
            f.write('attack_planet: ' + str(att_pln) + '\n')
            if (alliesSize + mySize) > req_ships:
              scores = []
              for my_pl in myPlanets:
                if my_pl.NumShips() < my_pl.GrowthRate()*10:
                  continue
                f.write('score: pw.Distance(...): ' + str(pw.Distance(my_pl.PlanetID(), att_pln.PlanetID())) + '\n')
                score = float(my_pl.NumShips()) / pw.Distance(my_pl.PlanetID(), att_pln.PlanetID())
                scores.append([my_pl, score])
              scores.sort(key=lambda x: x[1], reverse=True)
              f.write('scores: ' + str(scores) + '\n')
              
              distances = scores
              # req_orig_ships = att_pln.NumShips()
              # f.write('req_orig_ships: ' + str(req_orig_ships) + '\n')
              req_ships = att_pln.NumShips() + 1
              still_need = req_ships
              # f.write('enemyFleets: ' + str(enemyFleets) + '\n')
              # send only req-d num of ships
              for flt in partyFleets:
                if flt.DestinationPlanet() == att_pln.PlanetID():
                  still_need += flt.NumShips() - (att_pln.GrowthRate() * flt.TurnsRemaining())*2
              req_ships = still_need


              if len(distances) > 0:
                source1 = distances[0][0] # source planet
                if len(distances) > 1:
                  f.write('111\n')
                  source2 = distances[1][0] 
                  if source1.NumShips() > 0 and source2.NumShips() > 0:
                    # f.write('111 1: ' + str(float(source1.NumShips()) / source2.NumShips()) +'\n')
                    # if source1 is very strong
                    if float(source1.NumShips()) / source2.NumShips() > 3:
                      source1 = source2
                    # if source2 is very strong
                    elif float(source2.NumShips()) / source1.NumShips() > 3:
                      f.write('111 2\n')
                      source2 = source1
                    else:
                      if att_pln.NumShips() == 0:
                        koef1 = 1
                        koef2 = 1
                      else:
                        koef1= float(source1.NumShips()) / att_pln.NumShips() 
                        koef2= float(source2.NumShips()) / att_pln.NumShips() 
                      if koef1 > 0 and koef2 >0:
                        if koef1 > koef2:
                          koef = koef2/koef1
                        else:
                          koef = koef1/koef2
                        req_ships1 = req_ships*koef
                        req_ships2 = req_ships - req_ships1
                        if available_ships[source1.PlanetID()] >= req_ships1 and \
                          available_ships[source2.PlanetID()] >= req_ships2:
                          "ee"
                          # available_ships[source1.PlanetID()] -= req_ships1
                          # available_ships[source2.PlanetID()] -= req_ships2
                          # pw.IssueOrder(source1.PlanetID(), att_pln.PlanetID(), req_ships1)
                          # pw.IssueOrder(source2.PlanetID(), att_pln.PlanetID(), req_ships2)
                if len(distances) == 1 or \
                  source1.PlanetID() == source2.PlanetID():
                  f.write('222\n')
                  req_ships += att_pln.GrowthRate()*distances[0][1]
                  # req_ships += att_pln.GrowthRate()*pw.Distance(source1.PlanetID(), att_pln.PlanetID())
                  # req_ships += att_pln.GrowthRate()*3
                  # req_ships += available_ships[source1.PlanetID()] - 10
                  f.write("new req: " + str(req_ships) + '\n')
                  f.write("available: " + str(available_ships[source1.PlanetID()]) + '\n')
                  if req_ships > 0 and \
                    available_ships[source1.PlanetID()] >= req_ships:
                    f.write('av: ' + str(available_ships[source1.PlanetID()]) + '\n')
                    available_ships[source1.PlanetID()] -= req_ships
                    pw.IssueOrder(source1.PlanetID(), att_pln.PlanetID(), req_ships)
                    
                    # attack_targets[att_pln.PlanetID()] = [source1.PlanetID(), req_ships]
                  # else:  
                    # next_targets.append(att_pln.PlanetID())






  f.write('======= Calculate Targets ======= \n')
  # next_targets = []
  del next_targets[:]
  attack_targets = {}
  for att_pln in enemyPlanets:
    distances = []
    for my_pl in myPlanets:
      if my_pl.NumShips() < my_pl.GrowthRate()*10:
          continue
      # score = float(my_pl.NumShips()) / pw.Distance(my_pl.PlanetID(), att_pln.PlanetID())
      dist = pw.Distance(my_pl.PlanetID(), att_pln.PlanetID())
      distances.append([my_pl, dist])
    distances.sort(key=lambda x: x[1], reverse=True)
    f.write('distances: ' + str(distances) + '\n')
    
    # req_orig_ships = att_pln.NumShips()
    # f.write('req_orig_ships: ' + str(req_orig_ships) + '\n')
    req_ships = att_pln.NumShips() + 1
    f.write('req_ships: ' + str(req_ships) + '\n')
    if len(distances) > 0:
      source1 = distances[0][0] # source planet
      if len(distances) > 1:
        f.write('111\n')
        source2 = distances[1][0] 
        if source1.NumShips() > 0 and source2.NumShips() > 0:
          # f.write('111 1: ' + str(float(source1.NumShips()) / source2.NumShips()) +'\n')
          # if source1 is very strong
          if float(source1.NumShips()) / source2.NumShips() > 3:
            f.write('111 1\n')
            source1 = source2
          # if source2 is very strong
          elif float(source2.NumShips()) / source1.NumShips() > 3:
            f.write('111 2\n')
            source2 = source1
          else:
            f.write('111 3\n')
            if source1.NumShips() > 0 and source2.NumShips() > 0:
              if att_pln.NumShips() == 0:
                koef1 = 1
                koef2 = 1
              else:
                koef1= float(source1.NumShips()) / att_pln.NumShips() 
                koef2= float(source2.NumShips()) / att_pln.NumShips() 
              if koef1 > 0 and koef2 >0:
                if koef1 > koef2:
                  koef = koef2/koef1
                else:
                  koef = koef1/koef2
                req_ships1 = req_ships*koef
                req_ships2 = req_ships - req_ships1
                if available_ships[source1.PlanetID()] >= req_ships1 and \
                  available_ships[source2.PlanetID()] >= req_ships2:
                # koef1= source1.NumShips() / att_pln.NumShips() 
                # koef2= source2.NumShips() / att_pln.NumShips() 
                # if available_ships[source1.PlanetID()] >= req_ships and \
                #   available_ships[source2.PlanetID()] >= req_ships:
                  # available_ships[source1.PlanetID()] -= req_ships
                  # if attack_targets.has_key(att_pln.PlanetID()):
                  #   attack_targets[att_pln.PlanetID()] += [source1.PlanetID(), req_ships]
                  # else:
                  #   attack_targets[att_pln.PlanetID()] = [source1.PlanetID(), req_ships]
                  # "ee"
                  available_ships[source1.PlanetID()] -= req_ships1
                  available_ships[source2.PlanetID()] -= req_ships2
                  pw.IssueOrder(source1.PlanetID(), att_pln.PlanetID(), req_ships1)
                  pw.IssueOrder(source2.PlanetID(), att_pln.PlanetID(), req_ships2)


            else:  
              next_targets.append(att_pln.PlanetID())
      if len(distances) == 1 or \
        source1.PlanetID() == source2.PlanetID():
        f.write('222\n')
        req_ships += att_pln.GrowthRate()*distances[0][1]
        req_ships += att_pln.GrowthRate()*3
        f.write("new req: " + str(req_ships) + '\n')
        if available_ships[source1.PlanetID()] >= req_ships:
          f.write('av: ' + str(available_ships[source1.PlanetID()]) + '\n')
          available_ships[source1.PlanetID()] -= req_ships
          if attack_targets.has_key(att_pln.PlanetID()):
            attack_targets[att_pln.PlanetID()] += [source1.PlanetID(), req_ships]
          else:
            attack_targets[att_pln.PlanetID()] = [source1.PlanetID(), req_ships]
        else:  
          next_targets.append(att_pln.PlanetID())
    else:  
      next_targets.append(att_pln.PlanetID())
  
  f.write('next_targets (init): ' + str(next_targets) + '\n')

  tmp = []
  score = -999999
  for nt in next_targets:
    nt = pw.GetPlanet(nt)
    gr = nt.GrowthRate()
    sr = nt.NumShips()
    if nt.GrowthRate() == 0:
      gr = 1
    if nt.NumShips() == 0:
      sr = 1
    score = gr / sr
    tmp.append([nt.PlanetID(), score])
  tmp.sort(key=lambda x: x[1], reverse=True)
  # next_targets = []
  del next_targets[:]
  for pl_rate in tmp:
    next_targets.append(pl_rate[0])


  f.write('attack_targets: ' + str(attack_targets) + '\n')
  f.write('next_targets: ' + str(next_targets) + '\n')
    # if source1 and source2:
    # else:
      # if 
      # pw.IssueOrder(source.PlanetID(), att_pln.PlanetID(), num_ships)




    # rank = 
    # attack_targets.append([p, rank])

  # planets_rank.sort(key=lambda x: x[1], reverse=True)




  # if not commandGame:
    # # (1) If we currently have a fleet in flight, just do nothing.
    # # if len(pw.MyFleets()) >= 2:
    # #   return
    
    # # (2) Find my strongest planet.
    # source = -1
    # source_score = -999999.0
    # # source_num_ships = 0
    # my_planets = pw.MyPlanets()
    # for p in my_planets:
    #   score = float(p.NumShips())
    #   # if score > source_score:
    #   if score > p.GrowthRate() * 10:
    #     source_score = score
    #     source = p #.PlanetID()
    #     # source_num_ships = p.NumShips()

    #     # (3) Find the weakest enemy or neutral planet.
    #     # dest = -1
    #     # dest_score = -999999.0
    #     # not_my_planets = pw.NotMyPlanets()
    #     planets = pw.Planets()
        
    #     # (3.1) remove group members planets from list
    #     tmp = []
    #     for p in planets:
    #       if p.Owner() in group_ids:
    #         continue
    #       tmp.append(p)
    #     planets = tmp
    #     # f.write('not_my_planets: ' + ', '.join([str( p.Owner() ) for p in not_my_planets]) + '\n')
        
    #     # (3.2) remove planets which awaiting group member fleets
    #     planet_ids = [] # not_my_planets ids
    #     if planets:
    #       planet_ids = ([p.PlanetID() for p in planets])
    #     # f.write('planet_ids: ' + ', '.join([str( p ) for p in planet_ids]) + '\n')
    #     # f.write('planet_ids: ' + ', '.join([str( p ) for p in planet_ids]) + '\n')
    #     gfp_ids = [] # group_fleet_planet_ids
    #     # f.write('EnemyFleets DestinationPlanets: ' + ', '.join([str( fl.DestinationPlanet() ) for fl in pw.EnemyFleets() ]) + '\n')
    #     for fl in pw.EnemyFleets():
    #       if fl.Owner() in group_ids and fl.DestinationPlanet() in planet_ids:
    #         gfp_ids.append(fl.DestinationPlanet())
    #     gfp_ids = set(gfp_ids)
    #     # f.write('gfp_ids: ' + ', '.join([str( fl ) for fl in gfp_ids]) + '\n')

    #     # (3.3) remove planets which awaiting my fleets
    #     # my_fp_ids = [] # my_fleet_planet_ids
    #     # # f.write('EnemyFleets DestinationPlanets: ' + ', '.join([str( fl.DestinationPlanet() ) for fl in pw.EnemyFleets() ]) + '\n')
    #     # for fl in pw.MyFleets():
    #     #   if fl.DestinationPlanet() in planet_ids:
    #     #     my_fp_ids.append(fl.DestinationPlanet())
    #     # my_fp_ids = set(my_fp_ids)

    #     # ATTACK Planets
    #     # not_my_planets

    #     my_planet_ids = ([p.PlanetID() for p in pw.MyPlanets()])
    #     # (4) analyze planets
    #     # not_my_planets = tmp
    #     # f.write('not_my_planets: ' + ', '.join([str( p.Owner() ) for p in not_my_planets]) + '\n')
    #     planets_rank = [] 
    #     for p in planets:
    #       if p.PlanetID() in gfp_ids: # or p.PlanetID() in my_fp_ids:
    #         continue 
    #       # planet's obtain score or defeat
    #       killrate = 1
    #       defeat = 1
    #       if winRatio >= 1.5:
    #         # Killer mode
    #         f.write('KILLMODE \n')
    #         if p.Owner() != 0: # enemy
    #           killrate += 1000
    #       elif p.PlanetID() in my_planet_ids:
    #         for fleet in pw.EnemyFleets():
    #           if fl.Owner() in group_ids:
    #             continue
    #           if fleet.DestinationPlanet() == p.PlanetID():
    #             defeat = 1000
    #             # defeat = ( pw.Distance(source.PlanetID(), p.PlanetID()) )
    #       score = (1.0 * p.GrowthRate() * killrate * defeat ) / (1 + p.NumShips() + 2 * pw.Distance(source.PlanetID(), p.PlanetID())) 

    #       planets_rank.append([p, score])
    #       # if score > dest_score:
    #       #   dest_score = score
    #       #   dest = p #.PlanetID()
    #     # f.write('planets_rank: ' + ', '.join([str( p[1] ) for p in planets_rank]) + '\n')
    #     planets_rank.sort(key=lambda x: x[1], reverse=True)
    #     f.write('planets_rank Owner: ' + ', '.join([str( p[0].Owner() ) for p in planets_rank]) + '\n')
    #     # f.write('planets_rank NumShips: ' + ', '.join([str( p[0] ) for p in planets_rank]) + '\n')
    #     f.write('planets_rank: ' + ', '.join([str( p[1] ) for p in planets_rank]) + '\n')

    #     # (5) Send ships from my strongest planet to others
    #     sent_ships = 0
    #     for elem in planets_rank:
    #       f.write('planet: ' + str(elem[0]) + '\n')
    #       f.write('planets score: ' + str(elem[1]) + '\n')
    #       if (source.NumShips() - sent_ships * 3) <= 0:
    #         break
    #       dest = elem[0] # planet
    #       req_num_ships = dest.NumShips()

    #       # NOTE: worse result on current
    #       #
    #       for fleet in pw.EnemyFleets():
    #         if fl.Owner() in group_ids:
    #           continue
    #         if fleet.DestinationPlanet() == dest.PlanetID():
    #           req_num_ships += fleet.NumShips()

    #       for fleet in pw.MyFleets():
    #         if fleet.DestinationPlanet() == dest.PlanetID():
    #           req_num_ships -= fleet.NumShips()

    #       if req_num_ships < 0:
    #         continue 

    #       f.write('req_num_ships: ' + str(req_num_ships) + '\n')
    #       add_ships = 1
    #       f.write('dest.Owner(): ' + str(dest.Owner()) + '\n')
    #       if dest.Owner() != 0: # foe (not neutral)
    #         add_ships += dest.GrowthRate() * int(pw.Distance(source.PlanetID(), dest.PlanetID() ))
    #         f.write('add_ships: ' + str(add_ships) + '\n')
    #         if winRatio >= 1.5:
    #           # Killer mode
    #           add_ships += int(add_ships * 0.3)
    #       num_ships = req_num_ships * 2 + add_ships
    #       f.write('num_ships: ' + str(num_ships) + '\n')
    #       if (source.NumShips() - sent_ships - num_ships) >= 0:
    #         sent_ships += num_ships
    #         pw.IssueOrder(source.PlanetID(), dest.PlanetID(), num_ships)
    #       # else:
    #       #   num_ships = source.NumShips() - sent_ships
    #       #   if num_ships > 50:
    #       #     sent_ships += int(num_ships/2)
    #       #     pw.IssueOrder(source.PlanetID(), dest.PlanetID(), int(num_ships/2))
  # end of "if not commandGame:"



  f.write('======= Message Send Section ======= \n')
  # keep actual nickname (not dead)
  if len(messageHistory) > 1 and allies_nicks:
    nicknames = []
    for nick in allies_nicks:
      nick = nick[0]
      if nick in ([msh[0] for msh in messageHistory[-1]]):
        nicknames.append(nick)
      # for msh in messageHistory[-1]:
      #   f.write('======= msh: ' + str(msh) + '\n')
      #   if nick in ([msh_nick[0] for msh_nick in msh]):
          
    f.write('======= nicknames: ' + str(nicknames) + '\n')
    if nicknames:
      # for trg in next_targets[:3]:
      next_target1 = '100'
      next_target2 = '100'
      next_target3 = '100'
      if len(next_targets) == 1:
        next_target1 = str(int('100') + next_targets[0])
      elif len(next_targets) == 2:
        next_target1 = str(int('100') + next_targets[0])
        next_target2 = str(int('100') + next_targets[1])
      elif len(next_targets) > 2:
        next_target1 = str(int('100') + next_targets[0])
        next_target2 = str(int('100') + next_targets[1])
        next_target3 = str(int('100') + next_targets[2])
      # gtype = '1' # rush/save-game
      # planet = '000'
      # leader = '00'
      # vote = '0'
      mes = int(next_target1 + next_target2 + next_target3)
      f.write('======= mes: ' + str(mes) + '\n')
      pw.SendMessage(nickname,mes)



def main():
  group_ids = []
  nickname = 'X'
  if '-g' in sys.argv:
    group_ids = [int(k) for k in sys.argv[2].split(',')]
  if '-n' in sys.argv:
    nickname = str(sys.argv[4])
  f = open('MyBot4_' + str(nickname)+ '.log', 'w')
  f.write('group: ' + str(group_ids) + '\n')
  f.write('nick: ' + str(nickname) + '\n')

  map_data = ''
  while(True):
    current_line = raw_input()
    f.write(current_line + '\n')
    if len(current_line) >= 1 and current_line.startswith("."):
      pw = PlanetWars(map_data)
      f.write('-------------- NEW TURN ----------------\n')
      DoTurn(pw, group_ids, nickname, f)
      f.write('----------------------------------------\n')
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