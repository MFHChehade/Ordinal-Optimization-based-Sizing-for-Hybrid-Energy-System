from system import System
from battery import Battery  # Assuming battery.py contains the Battery class
from pv_panel import PVPanel  # Assuming pv_panel.py contains the PVPanel class
from diesel_gen import DieselGen  # Assuming diesel_gen.py contains the DieselGen class
from grid import Grid  # Assuming grid.py contains the Grid class
from load import Load  # Assuming load.py contains the Load class

class HybridEnergySystem(System):
    def __init__(self, pv: PVPanel, battery: Battery, diesel_gen: DieselGen, grid: Grid, load: Load):
        """
        Initialize a Hybrid Energy System with specified components.

        - pv (PVPanel): A photovoltaic panel system.
        - battery (Battery): A battery storage system.
        - diesel_gen (DieselGen): A diesel generator system.
        - grid (Grid): The grid connection.
        - load (Load): The load profile.
        """
        self.pv = pv
        self.battery = battery
        self.diesel_gen = diesel_gen
        self.grid = grid
        self.load = load

    def total_investment_cost(self):
        """
        Calculate the total investment cost of the hybrid energy system by summing up
        the investment costs of the PV panels, battery, and diesel generator.

        The grid and load generally do not contribute to the investment cost. 
        
        Returns:
        - float: Total investment cost of the system.
        """
        return (self.pv.investment_cost() +
                self.battery.investment_cost() +
                self.diesel_gen.investment_cost() + 
                self.grid.investment_cost() + 
                self.load.investment_cost())