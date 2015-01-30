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

# example_bot vs. 3 in group
java -jar tools/PlayGame.jar maps/map0.txt 200 200 log.txt "java -jar example_bots/RageBot.jar" "java -jar example_bots/DualBot.jar" "python ./MyBot2.py -g 4" "python ./MyBot3.py -g 3"   | java -jar tools/ShowGame.jar
