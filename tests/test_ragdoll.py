import os
import sys
import unittest

# Add the parent directory to the path to import the ragdoll module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import Ragdoll


class TestRagdoll(unittest.TestCase):
    def setUp(self):
        """Set up a ragdoll instance for testing."""
        self.ragdoll = Ragdoll(400, 300)

    def test_ragdoll_initialization(self):
        """Test if the ragdoll initializes with the correct number of parts and constraints."""
        self.assertEqual(
            len(self.ragdoll.parts), 6
        )  # Head, Torso, Left Arm, Right Arm, Left Leg, Right Leg
        self.assertEqual(len(self.ragdoll.constraints), 5)  # Connections between parts

    def test_ragdoll_update(self):
        """Test if the ragdoll's update method works without errors."""
        initial_positions = [(part["x"], part["y"]) for part in self.ragdoll.parts]
        self.ragdoll.update()
        updated_positions = [(part["x"], part["y"]) for part in self.ragdoll.parts]

        # Ensure positions have changed due to gravity
        self.assertNotEqual(initial_positions, updated_positions)

    def test_constraints(self):
        """Test if constraints are applied correctly."""
        # Manually move parts to violate constraints
        self.ragdoll.parts[0]["x"] = 100  # Move head far away
        self.ragdoll.parts[0]["y"] = 100

        # Apply multiple updates to allow constraints to correct the distance
        for _ in range(10):
            self.ragdoll.update()

        # Check if the constraint pulls the parts back
        dx = self.ragdoll.parts[1]["x"] - self.ragdoll.parts[0]["x"]
        dy = self.ragdoll.parts[1]["y"] - self.ragdoll.parts[0]["y"]
        distance = (dx**2 + dy**2) ** 0.5
        self.assertLess(
            distance, 60
        )  # Constraint distance is 50, allowing some tolerance


if __name__ == "__main__":
    unittest.main()
