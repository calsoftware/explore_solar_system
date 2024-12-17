# This program allows users to query information about planets in the solar system.
# It uses a JSON file to store planet data such as name, mass, distance from the Sun, and moons.
# Users can interact through a graphical user interface (GUI) built with Tkinter to query specific attributes.

import json  # Import JSON library to read and parse JSON data
import tkinter as tk  # Import Tkinter for GUI elements
from tkinter import messagebox  # Import messagebox for displaying pop-up messages
import os  # Import os to fetch the current working directory

class Planet:
    def __init__(self, name, mass, distance_from_sun, moons):
        # Planet class initialises a planet object with name, mass, distance from the sun, and moons
        self.name = name  # Name of the planet
        self.mass = mass  # Mass of the planet
        self.distance_from_sun = distance_from_sun  # Distance of the planet from the Sun in km
        self.moons = moons  # List containing the names of the planet's moons

    def __str__(self):
        # Returns a string representation of the planet's attributes
        return (f"Name: {self.name}\n"  # Planet's name
                f"Mass: {self.mass} kg\n"  # Planet's mass
                f"Distance from Sun: {self.distance_from_sun} km\n"  # Distance from Sun
                f"Moons: {', '.join(self.moons) if self.moons else 'None'}")  # List of moons or 'None'

class SolarSystem:
    def __init__(self):
        # SolarSystem class initialises an empty list to store Planet objects
        self.planets = []  # List to store Planet objects

    def load_data(self, file_path):
        # Load planet data from a JSON file located in the same directory as the script
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
        full_path = os.path.join(base_dir, file_path)  # Combine directory with file name
        try:
            with open(full_path, 'r') as file:  # Open the JSON file for reading
                data = json.load(file)  # Parse the JSON data into a Python structure
                for planet_data in data:  # Iterate through each planet in the JSON data
                    planet = Planet(planet_data['name'], planet_data['mass'], 
                                    planet_data['distance_from_sun'], planet_data['moons'])  # Create Planet object
                    self.planets.append(planet)  # Append the Planet object to the planets list
        except FileNotFoundError:  # Handle missing file error
            messagebox.showerror("Error", f"Data file not found. Ensure 'planets.json' is in the same directory as the script: {full_path}")

    def get_planet_by_name(self, name):
        # Retrieve a planet object by its name (case-insensitive search)
        for planet in self.planets:  # Iterate through the list of planets
            if planet.name.lower() == name.lower():  # Compare input name with planet name (case-insensitive)
                return planet  # Return the matching Planet object
        return None  # Return None if no planet matches the input name

# GUI Application Class
class SolarSystemApp:
    def __init__(self, root):
        # Initialise the GUI application and load planet data
        self.root = root  # Root window for the GUI
        self.root.title("Explore Solar System")  # Set the title of the window
        self.solar_system = SolarSystem()  # Create an instance of the SolarSystem class
        self.solar_system.load_data('planets.json')  # Load planet data from 'planets.json'

        # GUI Elements
        tk.Label(root, text="Enter Planet Name:").grid(row=0, column=0, pady=5)  # Label for input prompt
        self.entry_planet = tk.Entry(root, width=30)  # Entry field for planet name input
        self.entry_planet.grid(row=0, column=1, pady=5)  # Position entry field on the grid

        # Buttons for interacting with the application
        tk.Button(root, text="Show Details", command=self.show_details).grid(row=1, column=0, pady=5)  # Show planet details
        tk.Button(root, text="Check Existence", command=self.check_existence).grid(row=1, column=1, pady=5)  # Check if planet exists
        tk.Button(root, text="Get Mass", command=self.get_mass).grid(row=2, column=0, pady=5)  # Retrieve planet mass
        tk.Button(root, text="Get Moon Count", command=self.get_moons).grid(row=2, column=1, pady=5)  # Retrieve moon count
        tk.Button(root, text="Exit", command=root.quit).grid(row=3, column=0, columnspan=2, pady=10)  # Exit button

    def show_details(self):
        # Display all details of a planet based on the user input
        name = self.entry_planet.get()  # Retrieve user input for planet name
        planet = self.solar_system.get_planet_by_name(name)  # Search for the planet
        if planet:  # If planet is found
            messagebox.showinfo("Planet Details", str(planet))  # Show planet details in a pop-up message
        else:  # If planet is not found
            messagebox.showerror("Error", "Planet not found.")  # Show error message

    def check_existence(self):
        # Check if a planet exists in the solar system
        name = self.entry_planet.get()  # Retrieve user input for planet name
        planet = self.solar_system.get_planet_by_name(name)  # Search for the planet
        if planet:  # If planet exists
            messagebox.showinfo("Check Existence", f"Yes, {name} exists in the list.")  # Display confirmation message
        else:  # If planet does not exist
            messagebox.showinfo("Check Existence", f"No, {name} is not in the list.")  # Show 'not found' message

    def get_mass(self):
        # Retrieve and display the mass of a planet
        name = self.entry_planet.get()  # Retrieve user input for planet name
        planet = self.solar_system.get_planet_by_name(name)  # Search for the planet
        if planet:  # If planet is found
            messagebox.showinfo("Planet Mass", f"The mass of {planet.name} is {planet.mass} kg.")  # Display planet mass
        else:  # If planet is not found
            messagebox.showerror("Error", "Planet not found.")  # Show error message

    def get_moons(self):
        # Retrieve and display the number of moons for a planet
        name = self.entry_planet.get()  # Retrieve user input for planet name
        planet = self.solar_system.get_planet_by_name(name)  # Search for the planet
        if planet:  # If planet is found
            messagebox.showinfo("Moon Count", f"{planet.name} has {len(planet.moons)} moon(s).")  # Display moon count
        else:  # If planet is not found
            messagebox.showerror("Error", "Planet not found.")  # Show error message

# Run the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the root Tkinter window
    app = SolarSystemApp(root)  # Create an instance of the SolarSystemApp class
    root.mainloop()  # Run the Tkinter main event loop
