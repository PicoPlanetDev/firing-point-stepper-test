import math
import stepper

class Roll():
    def __init__(self, initial_length, inner_diameter, paper_thickness) -> None:
        """Sets up a roll of paper

        Args:
            initial_length (float): The length of the paper in millimeters
            inner_diameter (float): The inner diameter of the roll in millimeters
            thickness (float): The thickness of the paper in millimeters
        """
        self.initial_length = initial_length
        self.length = initial_length
        self.inner_diameter = inner_diameter
        self.thickness = paper_thickness

        self.stepper = stepper.Stepper([11, 12, 13, 15])

    def get_outer_diameter(self):
        """Returns the outer diameter of the roll in millimeters"""
        return math.sqrt(4 * self.length * self.thickness + math.pow(self.inner_diameter, 2) * math.pi)/math.sqrt(math.pi)
    
    def use_paper(self, length):
        """Uses the specified amount of paper

        Args:
            length (float): The amount of paper to use in millimeters
        """
        self.length -= length

    def reset_roll(self):
        """Resets the roll to its initial length"""
        self.length = self.initial_length

    def move_distance(self, distance, clockwise):
        """Moves the roll the specified distance

        Args:
            distance (float): The distance to move in millimeters
            clockwise (bool): Whether to move the roll clockwise or counter-clockwise
        """
        self.use_paper(distance)
        rotations = distance / (self.get_outer_diameter() * math.pi)
        self.stepper.spin(rotations, clockwise)

if __name__ == "__main__":
    # 50 ft roll is 15240 mm
    # 13 mm inner diameter
    # 0.05 mm thickness
    roll = Roll(15240, 13, 0.05)
    print(roll.get_outer_diameter())