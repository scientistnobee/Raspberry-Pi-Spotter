# This version uses new-style automatic setup/destroy/mapping
# Need to change /etc/webiopi

# Imports
import webiopi
import os
import subprocess
import time
import glob



# Retrieve GPIO lib
GPIO = webiopi.GPIO

# -------------------------------------------------- #
# Constants definition                               #
# -------------------------------------------------- #

R2=9  # H-Bridge 1
R1=10 # H-Bridge 2
RS=11 # H-Bridge 1,2EN

# second motor GPIOs
L2=23 # H-Bridge 3
L1=24 # H-Bridge 4
LS=25 # H-Bridge 3,4EN


# -------------------------------------------------- #
# Convenient PWM Function                            #
# -------------------------------------------------- #

# Set the speed of two motors
def set_speed(speed):
    GPIO.pulseRatio(LS, speed)
    GPIO.pulseRatio(RS, speed)

# -------------------------------------------------- #
# Left Motor Functions                               #
# -------------------------------------------------- #

def forward():
    GPIO.output(R1, GPIO.HIGH)
    GPIO.output(R2, GPIO.LOW)

def backward():
    GPIO.output(R2, GPIO.HIGH)
    GPIO.output(R1, GPIO.LOW)
def left():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.HIGH)

def right():
    GPIO.output(L2, GPIO.LOW)
    GPIO.output(L1, GPIO.HIGH)

def st():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.LOW)
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)


# -------------------------------------------------- #
# Macro definition part                              #
# -------------------------------------------------- #
@webiopi.macro
def go_forward():
    forward()


@webiopi.macro
def go_backward():
    backward()

@webiopi.macro
def turn_left():
    left()

@webiopi.macro
def turn_right():
    right()


@webiopi.macro
def stop():
    st()
    
# Called by WebIOPi at script loading
def setup():
    # Setup GPIOs
    GPIO.setFunction(LS, GPIO.PWM)
    GPIO.setFunction(L1, GPIO.OUT)
    GPIO.setFunction(L2, GPIO.OUT)
    
    GPIO.setFunction(RS, GPIO.PWM)
    GPIO.setFunction(R1, GPIO.OUT)
    GPIO.setFunction(R2, GPIO.OUT)
    
    set_speed(0.5)
    stop()


# Called by WebIOPi at server shutdown
def destroy():
    # Reset GPIO functions
    GPIO.setFunction(LS, GPIO.IN)
    GPIO.setFunction(L1, GPIO.IN)
    GPIO.setFunction(L2, GPIO.IN)
    
    GPIO.setFunction(RS, GPIO.IN)
    GPIO.setFunction(R1, GPIO.IN)
    GPIO.setFunction(R2, GPIO.IN)
    
@webiopi.macro
def get_done():
    print("spotter start")
    newest = max(glob.iglob('*.[j][p][g]'), key=os.path.getctime)
    cmd = "sudo ./deepbelief  {}  > try6.txt & ".format(newest)
    proc = subprocess.Popen(cmd, shell=True)
    cmd2 = "cp {} raju2.png".format(newest)
    proc2 = subprocess.Popen(cmd2, shell=True)
    webiopi.sleep(10)
    print("spotter stop")

  #  for line in fileinput.input(["try6.txt"], inplace=True, backup='.bak'):
   #     if line !='/n':
    #        pre,post=line.split()
     #       post2=pre
      #      pre2=post
       #     sys.stdout.write(pre2+' '+str(float(post2)*100)+' %\n')
        #else:
         #   sys.stdout.write(line)

@webiopi.macro
def get_text():
    global a
    with open ("try6.txt", "r") as myfile:
       a=myfile.read()
       print (a)
       return (a)



