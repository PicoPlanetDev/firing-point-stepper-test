import RPi.GPIO as GPIO
import time

# This is probably not great because it's not realtime

STEP_SEQUENCE = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

STEPS_PER_REVOLUTION = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

class Stepper():
    def __init__(self, pins, step_delay=0.002) -> None:
        """Sets up a stepper motor

        Args:
            pins (array): A four item array of integer board pin numbers corresponding to the stepper motor's pins in order (IN1 to IN4)
            step_delay (float): The amount of time to sleep between each step in seconds
        """
        self.pins = pins
        self.step_delay = step_delay

        GPIO.setmode(GPIO.BOARD)

        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def cleanup(self):
        """Turns off each of the motor pins and cleans up GPIO"""
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()

    def spin(self, rotations, clockwise):
        """Spins the stepper motor

        Args:
            rotations (float): The number of rotations to spin the motor
            clockwise (bool): Whether to spin the motor clockwise or counter-clockwise
        """
        step_count = int(rotations * STEPS_PER_REVOLUTION)
        motor_step_counter = 0

        for i in range(step_count):
            for pin in range(0, len(self.pins)):
                GPIO.output(self.pins[pin], STEP_SEQUENCE[motor_step_counter][pin])
            if clockwise:
                motor_step_counter = (motor_step_counter - 1) % 8
            else:
                motor_step_counter = (motor_step_counter + 1) % 8
            time.sleep(self.step_delay)

if __name__ == "__main__":
    my_stepper = Stepper([11, 12, 13, 15], step_delay=0.001)
    my_stepper.spin(rotations=1, clockwise=True)
    my_stepper.spin(rotations=1, clockwise=False)
    my_stepper.cleanup()