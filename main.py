# Some things cleaned up here. The random value was correctly implemented after looking at a block code example. 
# The performance isn't as good as other versions, but there seems to be less happening by accident. 
# This is important for knowing what I am changing in each iteration.

DRIVE_STRAIGHT = 0
TURN_LEFT = 1
TURN_RIGHT = 2
PAUSED = 3
RETURN_TO_CENTER = 4
BACK_UP = 5

PAUSE_TIME = 1.0

currentState = DRIVE_STRAIGHT
hasPickedUpBottle = False
randomVariable = 0.0

def updateSystem():
    
    pen.move(DOWN)

    pass

def evaluateState():
    global currentState
    global hasPickedUpBottle
    global randomVariable
    if(currentState == DRIVE_STRAIGHT):
       
        if(down_eye.detect(BLUE)):
            drivetrain.set_drive_velocity(30,PERCENT)
            currentState = BACK_UP
        elif(distance.get_distance(MM)<10 or brain.timer_time(SECONDS)>3.5):
            randomValue = random.randint(0, 6)
            print(randomValue)
            brain.timer_reset()
            if(randomValue == 0):
                currentState = TURN_LEFT
            else:
                currentState = TURN_RIGHT
           
    elif(currentState == BACK_UP):
        if(down_eye.detect(NONE)):
            drivetrain.set_drive_velocity(30,PERCENT)
            randomValue = randomValue = random.randint(0, 6)
            if(randomValue == 0):
                currentState = TURN_LEFT
            else:
                currentState = TURN_RIGHT
        
    elif(currentState == TURN_LEFT or currentState == TURN_RIGHT):
        if(down_eye.detect(BLUE)):
            
            currentState = BACK_UP
        elif(distance.found_object() and distance.get_distance(MM)<1000):
            currentState = DRIVE_STRAIGHT
        elif(brain.timer_time(SECONDS)>3.5):  
            print(brain.timer_time(SECONDS))
            
            randomValue = random.randint(0, 6)
            brain.timer_reset()
            if(randomValue == 0):
                currentState = TURN_LEFT
            else:
                currentState = TURN_RIGHT
        
    
    else:
        pass   

def reactToState():
    global currentState
    if(currentState == DRIVE_STRAIGHT):
        drivetrain.drive_for(FORWARD,60,MM)
    elif(currentState == TURN_LEFT):
        drivetrain.turn_for(LEFT,10,DEGREES)
    elif(currentState == TURN_RIGHT):
        drivetrain.turn_for(RIGHT,10,DEGREES)
    elif(currentState == BACK_UP):
        drivetrain.drive_for(REVERSE,100,MM)
   
    if(currentState == PAUSED):
        if(brain.timer_time(SECONDS)> PAUSE_TIME):
            currentState = DRIVE_STRAIGHT
            brain.timer_reset()
        
def when_started1():
    global currentState
    global randomVariable
    monitor_variable("randomValue")
    drivetrain.turn_to_heading(45, DEGREES)
    drivetrain.drive_for(FORWARD, 1000, MM)
    drivetrain.turn_to_heading(0, DEGREES)
    drivetrain.drive_for(FORWARD, 800, MM)
    while(True):
        updateSystem()
        evaluateState()
        reactToState()
        wait(1,MSEC)

    pass

vr_thread(when_started1())
