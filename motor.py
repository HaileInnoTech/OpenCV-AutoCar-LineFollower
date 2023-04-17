import RPi.GPIO as GPIO      
import paho.mqtt.publish as publish
import ultrasonic
from ultrasonic import min_distance
broker_address = "35.165.89.144"
topic = "linetracking"
topic2 = "Carcontrol"
port = 1883
activated = False
signal = None

US = ultrasonic

# Set GPIO pin of L298N to Raspberry 4
in1 = 13
in2 = 12
in3 = 21
in4 = 20
en1 = 6
en2 = 26

# Set speed for car
initialvaluespeed = 40
speed_turn = 35
speed = 35

# Set speed for car
initialvaluespeed = 40
speed_turn = 35
speed = 35

# Initialize GPIO Pin as outputs
GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

# Initialize power of L289N motor
p1 = GPIO.PWM(en1, 100)
p2 = GPIO.PWM(en2, 100)

# Clear the  start speed of car
p1.start(initialvaluespeed)
p2.start(initialvaluespeed)

# Clear  pins of L298N motor
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

# Change speed function


def changeSpeed():
    p1.start(speed_turn)
    p2.start(speed_turn)

# Change speed turn function


def changeSpeedTurn():
    p1.start(speed)
    p2.start(speed)

# Change default speed  function


def setSpeedDefault():
    p1.start(initialvaluespeed)
    p2.start(initialvaluespeed)

# Stop function


def stop():
    message = "Stop"
    publish.single(topic, message, hostname=broker_address)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

# Turn right function


def turn_right():
    message = "Turn Right"
    publish.single(topic, message, hostname=broker_address)
    changeSpeed()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

# Go forward function, stop when see obstackle


def forward():
    US.distance(min_distance)
    message = "On Track!"
    publish.single(topic, message, hostname=broker_address)
    setSpeedDefault()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

# Turn left function


def turn_left():
    message = "Turn Left"
    publish.single(topic, message, hostname=broker_address)
    changeSpeed()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

# Go backward function


def backward():
    message = "Go Backwards"
    publish.single(topic, message, hostname=broker_address)
    setSpeedDefault()
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)