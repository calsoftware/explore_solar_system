# This unit test file tests the 'explore_solar_system' program.
# Purpose: To ensure all functionalities of the SolarSystem program work as intended, using automated tests.
# Details: The tests include validating file handling, input validation, planet retrieval functionality,
#          and edge cases based on the attached test plan.
# How: A unittest framework is used to run multiple test cases, including successful and failing scenarios.
#      A temporary 'planets.json' file is created in the current directory to ensure proper execution.
#      Mock data is dynamically written and cleaned up after the tests.

import unittest  # Import unittest for test case creation
from unittest.mock import patch, mock_open  # Mocking file operations
import os  # Operating system library for file path operations
import json  # JSON library to handle JSON file writing and parsing
from explore_solar_system import SolarSystem, Planet  # Import the main program classes

class TestSolarSystem(unittest.TestCase):  # Create a test class inheriting from unittest.TestCase
    @classmethod
    def setUpClass(cls):
        """Set up the environment before all tests by creating a mock planets.json file"""
        cls.mock_data = [  # Mock JSON data for testing
            {"name": "Earth", "mass": "5.97237e24", "distance_from_sun": "149600000", "moons": ["Moon"]},
            {"name": "Mars", "mass": "6.4171e23", "distance_from_sun": "227900000", "moons": ["Phobos", "Deimos"]},
            {"name": "Jupiter", "mass": "1.8982e27", "distance_from_sun": "778500000", "moons": ["Io", "Europa"]},
            {"name": "Mercury", "mass": "3.3011e23", "distance_from_sun": "57910000", "moons": []}
        ]
        cls.json_path = os.path.join(os.path.dirname(__file__), "planets.json")  # File path for the mock JSON
        with open(cls.json_path, "w") as file:  # Create and write mock data to planets.json
            json.dump(cls.mock_data, file)  # Write the mock data as JSON

        cls.solar_system = SolarSystem()  # Create an instance of the SolarSystem class
        cls.solar_system.load_data("planets.json")  # Load the mock JSON data into the SolarSystem instance

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests by deleting the mock planets.json file"""
        if os.path.exists(cls.json_path):  # Check if planets.json exists
            os.remove(cls.json_path)  # Delete the file

    # File Handling Tests
    def test_data_loads_successfully(self):
        """Test that data loads correctly from a valid file"""
        self.assertEqual(len(self.solar_system.planets), 4)  # Expect 4 planets to be loaded

    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for a missing file"""
        solar_system = SolarSystem()  # Create a new instance
        with self.assertRaises(FileNotFoundError):  # Check for FileNotFoundError
            solar_system.load_data("non_existent.json")  # Load a non-existent file

    def test_invalid_json_format(self):
        """Test that JSONDecodeError is raised for an invalid JSON format"""
        with open(self.json_path, "w") as file:  # Overwrite planets.json
            file.write("Invalid JSON")  # Write invalid JSON data
        with self.assertRaises(json.JSONDecodeError):  # Check for JSONDecodeError
            self.solar_system.load_data("planets.json")  # Attempt to load invalid JSON

    # Input Validation Tests
    def test_case_insensitive_planet_name(self):
        """Test that planet search is case insensitive"""
        planet = self.solar_system.get_planet_by_name("earth")  # Search for Earth in lowercase
        self.assertEqual(planet.name, "Earth")  # Confirm that Earth is returned

    def test_invalid_planet_name(self):
        """Test that None is returned for a non-existent planet"""
        planet = self.solar_system.get_planet_by_name("Vulcan")  # Search for a non-existent planet
        self.assertIsNone(planet)  # Expect None as the result

    def test_blank_input(self):
        """Test that blank input returns None"""
        planet = self.solar_system.get_planet_by_name("")  # Search with an empty string
        self.assertIsNone(planet)  # Expect None as the result

    # Functional Tests
    def test_get_mass(self):
        """Test that the mass of a planet is retrieved correctly"""
        planet = self.solar_system.get_planet_by_name("Mars")  # Search for Mars
        self.assertEqual(planet.mass, "6.4171e23")  # Confirm the mass

    def test_get_distance_from_sun(self):
        """Test that the distance from the sun is retrieved correctly"""
        planet = self.solar_system.get_planet_by_name("Jupiter")  # Search for Jupiter
        self.assertEqual(planet.distance_from_sun, "778500000")  # Confirm the distance

    def test_get_moons(self):
        """Test that moon count is accurate for a planet with moons"""
        planet = self.solar_system.get_planet_by_name("Mars")  # Search for Mars
        self.assertEqual(len(planet.moons), 2)  # Confirm moon count

    def test_planet_with_no_moons(self):
        """Test that planets with no moons return an empty list"""
        planet = self.solar_system.get_planet_by_name("Mercury")  # Search for Mercury
        self.assertEqual(len(planet.moons), 0)  # Confirm no moons

    # Edge Cases
    def test_special_character_input(self):
        """Test behavior when input contains special characters"""
        planet = self.solar_system.get_planet_by_name("@#")  # Search with special characters
        self.assertIsNone(planet)  # Expect None as the result

    def test_numeric_input(self):
        """Test behavior when numeric input is given"""
        planet = self.solar_system.get_planet_by_name("123")  # Search with numbers
        self.assertIsNone(planet)  # Expect None as the result

if __name__ == "__main__":
    unittest.main()  # Run all test cases
