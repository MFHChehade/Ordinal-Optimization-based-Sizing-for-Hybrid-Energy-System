from component import Component

class Battery(Component):
    def __init__(self, SOC_min=0.2, SOC_max=0.9, SOC_init=0.5,
                 eff_ch=0.95, eff_disch=0.95, capacity=100.0,
                 min_charging_time=4.0, lifetime=10, cost=10000):
        """
        Initialize a new battery component with the specified parameters.

        - SOC_min (float) - Minimum state of charge, unitless (default: 0.2).
        - SOC_max (float) - Maximum state of charge, unitless (default: 0.9).
        - SOC_init (float) - Initial state of charge, unitless (default: 0.5).
        - eff_ch (float) - Charging efficiency, unitless (default: 0.95).
        - eff_disch (float) - Discharging efficiency, unitless (default: 0.95).
        - capacity (float) - Capacity of the battery in kWh (default: 100 kWh).
        - min_charging_time (float) - Minimum charging time in hours (default: 4 hours).
        - lifetime (int) - Lifetime of the battery in years (default: 10 years).
        - cost (float) - Total cost of the battery in USD (default: 10000 USD).
        """
        
        # State of charge parameters
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max
        self.SOC_init = SOC_init
        
        # Efficiency parameters
        self.eff_ch = eff_ch
        self.eff_disch = eff_disch
        
        # Physical and economic parameters
        self.capacity = capacity
        self.min_charging_time = min_charging_time
        self.P_B_max = capacity / min_charging_time  # Max power to/from battery, kW
        self.lifetime = lifetime
        self.cost = cost

    def investment_cost(self, interest_rate):
        """
        Calculate the annualized investment cost of the battery using the annuity formula.
        - interest_rate (float): The interest rate for the annuity calculation, expressed as a decimal.
        - return (float): Annual cost of the battery in USD.
        """
        annual_cost = (self.cost * interest_rate) / (1 - (1 + interest_rate) ** -self.lifetime)
        return annual_cost

    
    # Getters
    def get_SOC_min(self):
        return self.SOC_min

    def get_SOC_max(self):
        return self.SOC_max

    def get_SOC_init(self):
        return self.SOC_init

    def get_eff_ch(self):
        return self.eff_ch

    def get_eff_disch(self):
        return self.eff_disch

    def get_capacity(self):
        return self.capacity

    def get_min_charging_time(self):
        return self.min_charging_time

    def get_P_B_max(self):
        return self.P_B_max

    def get_lifetime(self):
        return self.lifetime

    def get_cost(self):
        return self.cost

    # Setters
    def set_SOC_min(self, value):
        self.SOC_min = value

    def set_SOC_max(self, value):
        self.SOC_max = value

    def set_SOC_init(self, value):
        self.SOC_init = value

    def set_eff_ch(self, value):
        self.eff_ch = value

    def set_eff_disch(self, value):
        self.eff_disch = value

    def set_capacity(self, value):
        self.capacity = value
        self.P_B_max = self.capacity / self.min_charging_time  # Update P_B_max if capacity changes

    def set_min_charging_time(self, value):
        self.min_charging_time = value
        self.P_B_max = self.capacity / self.min_charging_time  # Update P_B_max if min charging time changes

    def set_lifetime(self, value):
        self.lifetime = value

    def set_cost(self, value):
        self.cost = value

    # Display
    def __repr__(self):
    return (f"Battery(SOC_min={self.SOC_min}, SOC_max={self.SOC_max}, SOC_init={self.SOC_init}, "
            f"eff_ch={self.eff_ch}, eff_disch={self.eff_disch}, capacity={self.capacity}, "
            f"min_charging_time={self.min_charging_time}, P_B_max={self.P_B_max}, "
            f"lifetime={self.lifetime}, cost={self.cost})")
