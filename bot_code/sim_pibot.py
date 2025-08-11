class SimPiBot:
    def __init__(self, **kwargs):
        print(f"SimPiBot initialized with kwargs: {kwargs}")
        self.current_speed = 0

    def move_forward(self, speed, duration=None):
        print(f"SimPiBot moving forward with speed={speed}, duration={duration}")
        self.current_speed = speed

    def stop(self, duration=None):
        print(f"SimPiBot stopping, duration={duration}")
        self.current_speed = 0

    def move_backward(self, speed, duration=None):
        print(f"SimPiBot moving backward with speed={speed}, duration={duration}")
        self.current_speed = speed

    def change_speed(self, speed):
        print(f"SimPiBot changing speed from {self.current_speed} to {speed}")
        self.current_speed = speed

    def turn_round(self, speed=None, clockwise=True, duration=3.0):
        print(f"SimPiBot turning round with speed={speed}, clockwise={clockwise}, duration={duration}")

    def stop_turn_left(self, speed=None, duration=1):
        print(f"SimPiBot stop turn left with speed={speed}, duration={duration}")

    def stop_turn_right(self, speed=None, duration=1):
        print(f"SimPiBot stop turn right with speed={speed}, duration={duration}")

    def turn_left(self, ratio=60, duration=None):
        print(f"SimPiBot turning left with ratio={ratio}, duration={duration}")

    def turn_right(self, ratio=60, duration=None):
        print(f"SimPiBot turning right with ratio={ratio}, duration={duration}")

    def clean(self):
        print("SimPiBot cleaning up...")

    def get_speed(self):
        print(f"SimPiBot current speed: {self.current_speed}")
        return self.current_speed

    def accelerate(self, delta=10):
        print(f"SimPiBot accelerating by delta={delta}")
        self.current_speed += delta