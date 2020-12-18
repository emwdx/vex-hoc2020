
# 42 kg


DRIVE_STRAIGHT = 0
TURN_LEFT = 1
TURN_RIGHT = 2
AT_EDGE = 3
OBJECT_DETECTED = 4
BACK_UP = 5


currentState = DRIVE_STRAIGHT


def updateSystem():
    pass

def evaluateState():
    global currentState
    if(currentState == DRIVE_STRAIGHT):
        if(down_eye.detect(BLUE)):
            currentState = BACK_UP
    elif(currentState == BACK_UP):
        if(down_eye.detect(NONE)):
            if(round(brain.timer_time(SECONDS)%2 ==0)):
                currentState = TURN_LEFT
            else:
                currentState = TURN_RIGHT
    elif(currentState == TURN_LEFT or currentState == TURN_RIGHT):
        if(distance.found_object()):
            currentState = DRIVE_STRAIGHT

def reactToState():
    global currentState
    if(currentState == DRIVE_STRAIGHT):
        drivetrain.drive_for(FORWARD,50,MM)
    elif(currentState == TURN_LEFT):
        drivetrain.turn_for(LEFT,20,DEGREES)
    elif(currentState == TURN_RIGHT):
        drivetrain.turn_for(RIGHT,20,DEGREES)
    elif(currentState == BACK_UP):
        drivetrain.drive_for(REVERSE,200,MM)

def when_started1():
    global currentState
    
    while(True):
        updateSystem()
        evaluateState()
        reactToState()

    wait(1,MSEC)
    pass

vr_thread(when_started1())
