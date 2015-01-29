import sys

# f = open('MyBot2_log.txt', 'w')
# f.write("\n------\n".join(sys.argv) + '\n')
# f.write('------' + '\n')
print sys.argv
arr = [int(k) for k in sys.argv[2].split(',')]
print arr
# if sys.argv[1] == '-g':
if '-g' in sys.argv:
  print "jeee"
  