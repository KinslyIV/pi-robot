import RPi.GPIO as GPIO
import time

# Motor 1 Pins
IN1 = 17
IN2 = 27
EN1 = 22

# Motor 2 Pins
IN3 = 23
IN4 = 24
EN2 = 25

# Pin Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(EN1, GPIO.OUT)

GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(EN2, GPIO.OUT)

# Set up PWM for speed control
pwm_motor1 = GPIO.PWM(EN1, 1000)
pwm_motor1.start(0)  # Start with 0% duty cycle
pwm_motor2 = GPIO.PWM(EN2, 1000)
pwm_motor2.start(0)

def motor_forward(in1, in2, pwm, speed=50):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def motor_backward(in1, in2, pwm,  speed=50):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def motor_stop(in1, in2, pwm):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

# Example usage
motor_forward(IN1, IN2, pwm_motor1, 60)
motor_forward(IN3, IN4, pwm_motor2, 60)
time.sleep(2)
# motor_backward(60)
# time.sleep(2)
motor_stop(IN1, IN2, pwm_motor1)
motor_stop(IN3, IN4, pwm_motor2)


GPIO.cleanup()

