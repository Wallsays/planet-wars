# java -jar tools/PlayGame.jar maps/map1.txt 200 200 log.txt "python ./MyBot.py" "python ./MyBot.py" "python ./MyBot2.py -g 1" "python ./MyBot2.py -g 1" | java -jar tools/ShowGame.jar
# java -jar tools/PlayGame.jar maps/map1.txt 200 200 log.txt "python ./MyBot.py" "python ./MyBot.py" "python ./MyBot2.py -g 4" "python ./MyBot3.py -g 3" | java -jar tools/ShowGame.jar

# 
# initial test:
# 
#   2 bots idle vs. 2 in group
# java -jar tools/PlayGame.jar maps/map1.txt 200 200 log.txt "python ./MyBot.py" "python ./MyBot.py" "python ./MyBot2.py -g 4" "python ./MyBot2.py -g 3" | java -jar tools/ShowGame.jar
# 
#   2 bots idle - one of them in group with others
# java -jar tools/PlayGame.jar maps/map1.txt 200 200 log.txt "python ./MyBot.py" "python ./MyBot.py" "python ./MyBot2.py -g 4,2" "python ./MyBot2.py -g 3,2" | java -jar tools/ShowGame.jar

# example_bots vs. 2 in group
# java -jar tools/PlayGame.jar maps/map1.txt 200 200 log.txt "java -jar example_bots/RageBot.jar" "java -jar example_bots/DualBot.jar" "python ./MyBot2.py -g 4" "python ./MyBot3.py -g 3"   | java -jar tools/ShowGame.jar
# java -jar tools/PlayGame.jar maps/map11.txt 200 200 log.txt "java -jar example_bots/RageBot.jar" "java -jar example_bots/DualBot.jar" "python ./MyBot2.py -g 4" "python ./MyBot3.py -g 3"   | java -jar tools/ShowGame.jar
# java -jar tools/PlayGame.jar maps/map16.txt 200 200 log.txt "java -jar example_bots/RageBot.jar" "java -jar example_bots/DualBot.jar" "python ./MyBot4.py -g 4 -n J" "python ./MyBot3.py -g 3 -n K"  # | java -jar tools/ShowGame.jar
# java -jar tools/PlayGame.jar maps/map1.txt 200 200 log.txt "java -jar example_bots/RageBot.jar" "python ./GBot.py" "python ./MyBot2.py -g 4" "python ./MyBot3.py -g 3"   | java -jar tools/ShowGame.jar

# python war2.py 13 "example_bots/RageBot.jar" "example_bots/DualBot.jar" --gui
# python war2.py 16 "example_bots/RageBot.jar" "example_bots/DualBot.jar" "python ./MyBot4.py -g 4 -n J" "python ./MyBot3.py -g 3 -n K" --gui
# python war2.py 16 "example_bots/RageBot.jar" "example_bots/DualBot.jar" "example_bots/RageBot.jar" "example_bots/DualBot.jar" --gui
# python war2.py 13 "python ./MyBot4.py" "python ./MyBot3.py" --gui

#
#   Nickanmes format: %s%d (ex. R1)
#
# python war2.py 16 "python ./RageBot.py -g 2 -n R1" "python ./RageBot.py -g 1 -n R2" "python ./MyBot4.py -g 4 -n K1" "python ./MyBot4.py -g 3 -n K2" --gui
# python war2.py 16 "python ./DualBot.py -g 2 -n R1" "python ./RageBot.py -g 1 -n R2" "python ./MyBot4.py -g 4 -n K1" "python ./MyBot4.py -g 3 -n K2" --gui
# python war2.py 70 "python ./DualBot.py -g 2 -n R1" "python ./RageBot.py -g 1 -n R2" "python ./MyBot4.py -g 4 -n K1" "python ./MyBot4.py -g 3 -n K2" --gui

# 100 planets map
# python war2.py 110 "python ./DualBot.py -g 2 -n R1" "python ./DualBot.py -g 1 -n R2" "python ./RageBot.py -g 4 -n K1" "python ./RageBot.py -g 3 -n K2" "python ./MyBot4.py -g 6,7,8 -n E1" "python ./MyBot4.py -g 5,7,8 -n E2" "python ./MyBot4.py -g 5,6,8 -n E3" "python ./MyBot4.py -g 5,6,7 -n E4"

# python war2.py 16 "python ./RageBot.py -g 1 -n R2" "python ./MyBot4.py -g 3,4 -n K1" "python ./MyBot4.py -g 2,4 -n K2" "python ./MyBot4.py -g 2,3 -n K3" --gui
# python war2.py 48 "python ./DualBot.py -g 2 -n R1" "python ./RageBot.py -g 1 -n R2" "python ./MyBot4.py -g 4 -n K1" "python ./MyBot4.py -g 3 -n K2" --gui
# python war2.py 48 "python ./DualBot.py -g 2 -n R1" "python ./DualBot.py -g 1 -n R2" "python ./MyBot4.py -g 4 -n K1" "python ./MyBot4.py -g 3 -n K2" --gui
# python war2.py 165 "python ./DualBot.py -g 2,3 -n C1" "python ./DualBot.py -g 1,3 -n C2" "python ./DualBot.py -g 2,3 -n R1" "python ./MyBot4.py -g 5 -n K1" "python ./MyBot4.py -g 4 -n K2" #--gui
# python war2.py 16 "python ./DualBot.py -g 2 -n R1" "python ./RageBot.py -g 1 -n R2" "python ./MyBot4.py -g 4 -n K1" "python ./MyBot4.py -g 3 -n K2" --gui
# python war2.py 32 "python ./DualBot.py -g 2 -n R1" "python ./RageBot.py -g 1 -n R2" "python ./MyBot4.py -g 4 -n K1" "python ./MyBot4.py -g 3 -n K2" --gui
# python war2.py 32 "python ./RageBot.py -g 2 -n R2" "python ./DualBot.py -g 1 -n R1"  "python ./MyBot4.py -g 4 -n K1" "python ./MyBot4.py -g 3 -n K2" --gui
# python war2.py 80 "python ./DualBot.py -g 2 -n R1" "python ./RageBot.py -g 1 -n R2" "python ./MyBot4.py -g 4 -n K1" "python ./MyBot4.py -g 3 -n K2" --gui

# New map format 
#
# python war2.py 900 "python ./RageBot.py -g 2 -n R" "python ./RageBot.py -g 1 -n S" "python ./MyBot4.py -g 4 -n K" "python ./MyBot4.py -g 3 -n J" --gui
# python war2.py 900 "python ./MyBot4.py -g 2 -n K" "python ./MyBot4.py -g 1 -n J" "python ./RageBot.py -g 4 -n R" "python ./RageBot.py -g 3 -n S"  --gui 

#  1,2 - first group, 3,4 - 2nd group
# python war2.py 901 "python ./RageBot.py -g 2 -n R" "python ./RageBot.py -g 1 -n S" "python ./MyBot4.py -g 4 -n K" "python ./MyBot4.py -g 3 -n J" --gui
# python war2.py 900 "python ./RageBot.py -g 2 -n R" "python ./RageBot.py -g 1 -n S" "python ./MyBot4.py -g 4 -n K" "python ./MyBot4.py -g 3 -n J" --gui
python war2.py 900  "python ./MyBot4.py -g 2 -n K" "python ./MyBot4.py -g 1 -n J" "python ./RageBot.py -g 4 -n R" "python ./RageBot.py -g 3 -n S" --gui




