import RPi.GPIO as GPIO
import time
import motor
m1 = motor

min_distance = 10 # or whatever value you want to use
# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
# Set GPIO pin of HC-SR04 to Raspberry 4
trig = 23
echo = 24
# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Initialize GPIO Pin as outputs
GPIO.setup(trig, GPIO.OUT)
# Initialize GPIO Pin as input
GPIO.setup(echo, GPIO.IN)

def distance(min_distance):
    while True:
        # Send a trigger pulse to the HC-SR04
        GPIO.output(trig, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig, GPIO.LOW)

        # Measure the duration of the echo pulse
        while GPIO.input(echo) == GPIO.LOW:
            pulse_start = time.time()

        while GPIO.input(echo) == GPIO.HIGH:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        # Calculate the distance to the object
        distance = pulse_duration * 17150
        if distance > min_distance:
            return True
        else:
            m1.stop()
