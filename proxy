import random
import time

def frameCheck(counter):
    a = random.randint(0,99)
    if counter <= 3:
        if a < 5:
          print("Dropped frame, retry")

          # your code for retrying the frame send here

        elif (a >=5 and a < 15):
          print("Frame " + str(counter) + " delayed")
          delayTime = round(random.random()*4 + 1,1)
          print delayTime

          time.sleep(delayTime)

          counter = counter + 1
          frameCheck(counter)

        else:
          print("Successful transfer of frame " + str(counter))
          counter = counter + 1
          frameCheck(counter)

counter = 1
frameCheck(counter)

print("")
