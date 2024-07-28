from component import Component

class DieselGen(Component):
    def __init__(self, capacity: float = 10000, minimum_power=0.2, cost_per_kwh: float = 0.5,
                 lifetime: int = 20, initial_cost: float = 200000, annual_om_cost: float = 10000):
        """
        Initialize a new Diesel Generator with specified parameters.
        
        - capacity (float): Maximum power output of the generator in kW (default: 10,000 kW).
        - minimum_power: Minimum power output as a percentage of capacity (e.g., 0.2 for 20%) or directly in kW.
        - cost_per_kwh (float): Operational cost of the generator per kWh, primarily related to fuel cost (default: $0.50/kWh).
        - lifetime (int): Expected operational lifetime of the generator in years (default: 20 years).
        - initial_cost (float): Initial investment cost of the generator in USD (default: $200,000).
        - annual_om_cost (float): Annual fixed operational and maintenance cost in USD (default: $10,000).
        """
        self.capacity = capacity
        self._set_minimum_power(minimum_power)
        self.cost_per_kwh = cost_per_kwh
        self.lifetime = lifetime
        self.initial_cost = initial_cost
        self.annual_om_cost = annual_om_cost

    def __repr__(self):
        return (f"DieselGen(capacity={self.capacity}, minimum_power={self.minimum_power}, "
                f"cost_per_kwh={self.cost_per_kwh}, lifetime={self.lifetime}, initial_cost={self.initial_cost}, "
                f"annual_om_cost={self.annual_om_cost})")

    def investment_cost(self, newly_installed: bool) -> float:
        """
        Calculate the investment cost of the diesel generator if it is newly installed.

        - newly_installed (bool): Flag indicating whether the generator is newly installed or not.
        
        Returns:
        - float: The investment cost if newly installed, otherwise 0.
        """
        if newly_installed:
            # Calculate annualized investment cost using a simple linear amortization
            annual_investment_cost = self.initial_cost / self.lifetime
            return annual_investment_cost + self.annual_om_cost
        else:
            return self.annual_om_cost


    # Getters
    def get_capacity(self):
        return self.capacity

    def get_minimum_power(self):
        return self.minimum_power

    def get_cost_per_kwh(self):
        return self.cost_per_kwh

    # Setters
    def set_capacity(self, value):
        self.capacity = value
        # Re-calculate minimum power if it was set as a percentage
        if hasattr(self, '_min_power_percentage'):
            self.set_minimum_power(self._min_power_percentage)

    def set_minimum_power(self, value):
        self._set_minimum_power(value)

    def set_cost_per_kwh(self, value):
        self.cost_per_kwh = value

    def _set_minimum_power(self, value):
        # Internal method to handle setting minimum power
        if isinstance(value, (int, float)) and value < 1:  # Treat as percentage if less than 1
            self.minimum_power = self.capacity * value
            self._min_power_percentage = value  # Save the percentage for recalculations
        else:
            self.minimum_power = value
            if hasattr(self, '_min_power_percentage'):
                del self._min_power_percentage  # Remove percentage if absolute value is set