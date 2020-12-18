# The electromagnet did nothing. I did another trial with it commented out to see what it did, and it seemed to decrease the average further.

# I'm curious about using the same algorithm but with a higher speed to see if that changes anything.
DRIVE_STRAIGHT = 0
TURN_LEFT = 1
TURN_RIGHT = 2
PAUSED = 3
RETURN_TO_CENTER = 4
BACK_UP = 5

PAUSE_TIME = 1

currentState = DRIVE_STRAIGHT
hasPickedUpBottle = False

def updateSystem():
    drivetrain.set_drive_velocity(100,PERCENT)

    pass

def evaluateState():
    global currentState
    global hasPickedUpBottle
    if(currentState == DRIVE_STRAIGHT):
        if(not(hasPickedUpBottle) and location.position(X,MM)>10):
            hasPickedUpBottle = True
            pen.move(DOWN)
            currentState = PAUSED
        elif(down_eye.detect(BLUE)):
            drivetrain.set_drive_velocity(30,PERCENT)
            currentState = BACK_UP
        elif(brain.timer_time(SECONDS)>3.0):
            
            randomValue = round(brain.timer_time(SECONDS)%3 ==0)
            brain.timer_reset()
            if(randomValue == 0):
                currentState = TURN_LEFT
            elif(randomValue == 1):
                currentState = TURN_RIGHT
            else:
                currentState = RETURN_TO_CENTER
    elif(currentState == BACK_UP):
        if(down_eye.detect(NONE)):
            drivetrain.set_drive_velocity(50,PERCENT)
            randomValue = round(brain.timer_time(SECONDS)%3 ==0)
            if(randomValue == 0):
                currentState = TURN_LEFT
            elif(randomValue == 1):
                currentState = TURN_RIGHT
            else:
                currentState = RETURN_TO_CENTER
    elif(currentState == TURN_LEFT or currentState == TURN_RIGHT):
        if(down_eye.detect(BLUE)):
            drivetrain.set_drive_velocity(30,PERCENT)
            currentState = BACK_UP
        elif(distance.found_object() and distance.get_distance(MM)<500):
            currentState = DRIVE_STRAIGHT
        elif(brain.timer_time(SECONDS)>2.0):  
            randomValue = round(brain.timer_time(SECONDS)%3 == 0)
            brain.timer_reset()
            if(randomValue == 0):
                currentState = TURN_LEFT
            elif(randomValue == 1):
                currentState = TURN_RIGHT
            else:
                currentState = RETURN_TO_CENTER
    elif(currentState == RETURN_TO_CENTER):
        if(calculateDistanceToCenter < 10):
            currentState = DRIVE_STRAIGHT
        

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
    elif(currentState == RETURN_TO_CENTER):
        drivetrain.set_heading(calculateHeadingToCenter(),DEGREES)
        drivetrain.drive_for(FORWARD,calculateDistanceToCenter(),MM)
    if(currentState == PAUSED):
        if(brain.timer_time(SECONDS)> PAUSE_TIME):
            currentState = DRIVE_STRAIGHT
            brain.timer_reset()
        

def calculateHeadingToCenter():
    x = location.position(X,mm)
    y = location.position(Y,mm)
    angle = Math.atan2(x/y)* 180/ Math.PI
    if(x > 0):
        if(y>0):
            return 90.0 + angle
        else:
            return 180 - angle
    else:
        if(y>0):
            return 90.0 + angle
        else:
            return angle

def calculateDistanceToCenter():
    x = location.position(X,mm)
    y = location.position(Y,mm)
    return round(Math.sqrt(x*x + y*y))

def when_started1():
    global currentState
    
    drivetrain.turn_to_heading(270, DEGREES)
    drivetrain.drive_for(FORWARD, 800, MM)
    drivetrain.turn_to_heading(45, DEGREES)
    drivetrain.drive_for(FORWARD, 1100, MM)
    drivetrain.turn_to_heading(90, DEGREES)
    drivetrain.drive_for(FORWARD, 700, MM)
    drivetrain.turn_to_heading(0, DEGREES)
    while(True):
        updateSystem()
        evaluateState()
        reactToState()
        wait(1,MSEC)

    pass

vr_thread(when_started1())
