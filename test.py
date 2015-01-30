import sys

f = open('MyBot2_log.txt', 'w')
# f.write("\n------\n".join(sys.argv) + '\n')
# f.write('------' + '\n')
print sys.argv
arr = [int(k) for k in sys.argv[2].split(',')]
print arr
# if sys.argv[1] == '-g':
if '-g' in sys.argv:
  print "jeee"
  
# a 
# for i, val in enumerate(a):
  # print i, val

# f.write('------' +  )

class Planet:
  def __init__(self, planet_id, owner, num_ships, growth_rate, x, y):
    self._planet_id = planet_id
    self._owner = owner
    self._num_ships = num_ships
    self._growth_rate = growth_rate
    self._x = x
    self._y = y

  def PlanetID(self):
    return self._planet_id

  def Owner(self, new_owner=None):
    if new_owner == None:
      return self._owner
    self._owner = new_owner

  def NumShips(self, new_num_ships=None):
    if new_num_ships == None:
      return self._num_ships
    self._num_ships = new_num_ships

  def GrowthRate(self):
    return self._growth_rate

  def X(self):
    return self._x

  def Y(self):
    return self._y

  def AddShips(self, amount):
    self._num_ships += amount

  def RemoveShips(self, amount):
    self._num_ships -= amount


pl1 = Planet(0, 1,100, 5, 3.0, -4.5)
pl2 = Planet(1, 2,100, 5, 1.0, 7.5)
pl3 = Planet(2, 0,100, 5, 5.0, 10.5)

arr  = [pl1, pl2, pl3]
arr2 =  ([str( p.PlanetID() ) for p in arr])
print arr
print arr2

planet_ids = []
# if planet_ids:
# planet_ids = ([int( p.PlanetID() ) for p in not_my_planets])
f.write(', '.join([str( pid ) for pid in planet_ids]))
print planet_ids   

