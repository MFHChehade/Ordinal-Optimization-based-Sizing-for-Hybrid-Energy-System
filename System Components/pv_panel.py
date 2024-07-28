import pandas as pd
from component import Component
import numpy as np

class PVPanel(Component):
    def __init__(self, irradiance_data: pd.DataFrame, 
                 G_0: float = 1000.0, G_N: float = 800.0,
                 T_0: float = 25.0, TC_N: float = 43, Talpha_N: float = 25.0,
                 Beta_p: float = - 0.34 * 1e-2, P_max: float = 555.0, lifetime:int = 25, cost: float = 750.0):
        """
        Initialize a new PV panel with specified parameters.

        - irradiance_data (DataFrame) - A pandas DataFrame containing the irradiance data with required columns.
        - G_0 (float) - Standard test condition (STC) irradiance in W/m^2 (default: 1000.0 W/m^2).
        - G_N (float) - Nominal operating cell irradiance in W/m^2 (default: 800.0 W/m^2).
        - T_0 (float) - STC temperature in degrees Celsius (default: 25.0°C).
        - TC_N (float) - Nominal operating cell temperature (NOCT) in degrees Celsius (default: 43.0°C).
        - Talpha_N (float) - Ambient temperature at NOCT in degrees Celsius (default: 25.0°C).
        - Beta_p (float) - The coeffient of power as a funtion of temperature (default: = -0.0034 W/°C).
        - P_max (float) - Maximum power output under standard test conditions in Watts (default: 555.0 Watts).
        - lifetime (int) - Lifetime of the PV Panel in years (default: 10 years).
        - cost (float) - Total cost of the battery in USD (default: 750.0 USD).
        """
        
        self.irradiance_data = self.validate_irradiance_data(irradiance_data)
        self.G_0 = G_0
        self.G_N = G_N
        self.T_0 = T_0
        self.TC_N = TC_N
        self.Talpha_N = Talpha_N
        self.Beta_p = Beta_p
        self.P_max = P_max

        self.lifetime = lifetime
        self.cost = cost

    def validate_irradiance_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Validate that the DataFrame contains all required columns for processing.
        - data (DataFrame): The irradiance dataset to validate.
        """
        required_columns = ["month", "day", "hour", "horizontal irradiance", "temperature", "solar zenith"]
        if not all(col.lower() in data.columns.str.lower() for col in required_columns):
            raise ValueError(f"Dataframe must contain the following columns: {required_columns}")
        return data

    # Getters
    def get_G_0(self):
        return self.G_0

    def get_G_N(self):
        return self.G_N

    def get_T_0(self):
        return self.T_0

    def get_TC_N(self):
        return self.TC_N

    def get_Talpha_N(self):
        return self.Talpha_N

    def get_Beta_p(self):
        return self.Beta_p

    def get_P_max(self):
        return self.P_max

    # Setters
    def set_G_0(self, value):
        self.G_0 = value

    def set_G_N(self, value):
        self.G_N = value

    def set_T_0(self, value):
        self.T_0 = value

    def set_TC_N(self, value):
        self.TC_N = value

    def set_Talpha_N(self, value):
        self.Talpha_N = value

    def set_Beta_p(self, value):
        self.Beta_p = value

    def set_P_max(self, value):
        self.P_max = value


    # Cost
    
    def calculate_investment_cost(self, interest_rate: float) -> float:
        """
        Calculate the annualized investment cost of the PV panel based on the provided interest rate.

        - interest_rate (float): The annual interest rate used for the annuity calculation, expressed as a decimal.

        Returns:
        - float: The annual cost of the PV panel, considering its initial cost and lifetime.
        """
        if not (0 < interest_rate < 1):
            raise ValueError("Interest rate should be a decimal between 0 and 1.")

        # Annuity formula to calculate annualized cost
        annual_cost = (self.cost * interest_rate) / (1 - (1 + interest_rate) ** -self.lifetime)

        return annual_cost


    # Irradiance calculations

    def calculate_power_output(self) -> pd.DataFrame:
        """
        Calculate the power output of the panel for each time step in the internal weather dataset.
        This method takes into account the irradiance and temperature effects based on the panel's specifications.

        Returns:
        - DataFrame: The internal weather data updated with an additional column for calculated power output.
        """
        if 'Calculated_Irradiance' not in self.irradiance_data.columns:
            raise ValueError("Irradiance data must be calculated first. Use calculate_irradiance_vector method.")

        irradiance = self.irradiance_data['Calculated_Irradiance']
        temperature = self.irradiance_data['Temperature']  # Ensure this column name matches dataset

        # Calculate the temperature of the solar cell
        temp_coeff = (self.TCN - self.Talpha_N) / self.G_N
        temp_cell = temp_coeff * irradiance + temperature
        
        P_panel = self.P_max * (irradiance / self.G_0) * (1 + self.b_p * (temp_cell - self.T_0))

        # Add power output data to the DataFrame
        self.irradiance_data['Power_Output'] = P_panel

        return self.irradiance_data


    def radiation_slope_surface(self, day: int, time: float, G_horizontal_radiation: float, solar_zenith: float,
                            longitude: float = 33.9009, latitude: float = 35.4811,
                            timezone_index: int = 2, tilt_angle: float = None,
                            surface_azim: float = 0, ground_reflectance: float = 0.6) -> float:
        """
        Calculate the solar radiation on a sloped surface at a specific time and day using the HDKR model.

        - day (int): The day of the year.
        - time (float): The time of day in hours.
        - G_horizontal_radiation (float): Horizontal solar radiation at the given time in W/m^2.
        - solar_zenith (float): Solar zenith angle in degrees.
        - longitude (float): Geographical longitude of the location (default: 33.9009 degrees).
        - latitude (float): Geographical latitude of the location (default: 35.4811 degrees).
        - timezone_index (int): Timezone index relative to GMT (default: 2).
        - tilt_angle (float): Tilt angle of the panel in degrees (default: latitude of the location).
        - surface_azim (float): Surface azimuth angle in degrees from north (default: 0).
        - ground_reflectance (float): Ground reflectance factor (default: 0.6).

        Returns:
        - s_radiation (float): Calculated solar radiation on the slope surface in W/m^2.
        """
        if tilt_angle is None:
            tilt_angle = latitude  # Default tilt angle to latitude if not provided

        if G_horizontal_radiation == 0 or solar_zenith < 0:
            return 0

        # Incidence angle calculation
        longit_zone = 15 * timezone_index
        b = (day - 1) * (360 / 365)
        e = 229.2 * (0.000075 + 0.001868 * np.cos(np.radians(b)) - 0.032077 * np.sin(np.radians(b)) -
                    0.014615 * np.cos(np.radians(2 * b)) - 0.04089 * np.sin(np.radians(2 * b)))
        t_solar = time + (4 * (longitude - longit_zone) + e) / 60

        delta = 23.45 * np.sin(np.radians((360 * (284 + day) / 365)))

        if t_solar >= 12:
            sign = 1
        else:
            sign = -1
        solar_azimuth = sign * abs(np.degrees(np.arccos((np.cos(np.radians(solar_zenith)) * np.sin(np.radians(latitude)) -
                                                        np.sin(np.radians(delta))) / (np.sin(np.radians(solar_zenith)) * np.cos(np.radians(latitude))))))

        theta = np.cos(np.radians(solar_zenith)) * np.cos(np.radians(tilt_angle)) + \
                np.sin(np.radians(solar_zenith)) * np.sin(np.radians(tilt_angle)) * np.cos(np.radians(solar_azimuth - surface_azim))

        # Calculating radiation on a sloped surface
        Gsc = 1367
        solar_radiation = Gsc * (1.000110 + 0.034221 * np.cos(np.radians(b)) + 0.001280 * np.sin(np.radians(b)) +
                                0.000719 * np.cos(np.radians(2 * b)) + 0.000077 * np.sin(np.radians(2 * b)))

        clearness_index = G_horizontal_radiation / (solar_radiation * np.cos(np.radians(solar_zenith)))

        if clearness_index <= 0.35:
            Ro_d = 1 - 0.249 * clearness_index
        elif clearness_index > 0.75:
            Ro_d = 0.177
        else:
            Ro_d = 1.557 - 1.84 * clearness_index

        diffuse_radiation = Ro_d * G_horizontal_radiation
        beam_radiation = (1 - Ro_d) * G_horizontal_radiation

        Rb = np.cos(np.radians(theta)) / np.cos(np.radians(solar_zenith))
        Ai = beam_radiation / (solar_radiation * np.cos(np.radians(solar_zenith)))
        beam_radiation_HDKR = (beam_radiation + (diffuse_radiation * Ai)) * Rb

        f = np.sqrt(beam_radiation / G_horizontal_radiation)
        diffuse_radiation_HDKR = diffuse_radiation * (1 - Ai) * ((1 + np.cos(np.radians(tilt_angle))) / 2) * (1 + (f * np.sin(np.radians(tilt_angle / 2))**3))

        diffuse_radiation_reflected = G_horizontal_radiation * ground_reflectance * ((1 - np.cos(np.radians(tilt_angle))) / 2)

        s_radiation = beam_radiation_HDKR + diffuse_radiation_HDKR + diffuse_radiation_reflected
        return s_radiation

    def calculate_irradiance_vector(self) -> pd.DataFrame:
        """
        Calculate the solar irradiance for every time step in the internal weather dataset using the HDKR model.
        Automatically adjusts for leap and non-leap years based on the dataset provided.
        
        Returns:
        - DataFrame: The internal weather data updated with an additional column for calculated irradiance.
        """
        # Validate and extract necessary columns dynamically
        required_columns = {
            'month': None,
            'day': None,
            'hour': None,
            'horizontal irradiance': None,
            'temperature': None,
            'solar zenith': None
        }

        for col in self.irradiance_data.columns:
            for req in required_columns:
                if req in col.lower():
                    required_columns[req] = col

        if None in required_columns.values():
            missing = [key for key, value in required_columns.items() if value is None]
            raise ValueError(f"Missing required data columns: {missing}")

        # Extracting data
        month = self.irradiance_data[required_columns['month']]
        day = self.irradiance_data[required_columns['day']]
        hour = self.irradiance_data[required_columns['hour']]
        horizontal_irradiance = self.irradiance_data[required_columns['horizontal irradiance']]
        solar_zenith = self.irradiance_data[required_columns['solar zenith']]

        # Check for leap year
        year_days = day.iloc[-1] + np.cumsum([31, (29 if (len(self.irradiance_data) > 8760) else 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])[month.iloc[-1]-1] - 1
        if year_days == 366:
            # Adjust for leap year
            DY_per_MO = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            DY_per_MO = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        # Calculate day of year
        cum_days = np.cumsum(DY_per_MO) - DY_per_MO
        day_of_year = day + cum_days[month - 1]

        # Prepare the output irradiance array
        T = len(self.irradiance_data)
        irradiance = np.zeros(T)

        # Apply the HDKR Model on the irradiance data:
        for t in range(T):
            d = day_of_year.iloc[t]
            h = hour.iloc[t]
            sza = solar_zenith.iloc[t]
            GHR = horizontal_irradiance.iloc[t]

            irradiance_HDKR = self.radiation_slope_surface(d, h, GHR, sza)

            irradiance[t] = irradiance_HDKR

        # Add irradiance data to the DataFrame
        self.irradiance_data['Calculated_Irradiance'] = irradiance

        return self.irradiance_data

    
    # Display
    def __repr__(self):
    return (f"PVPanel(G_0={self.G_0}, G_N={self.G_N}, T_0={self.T_0}, "
            f"TC_N={self.TC_N}, Talpha_N={self.Talpha_N}, Beta_p={self.Beta_p}, "
            f"P_max={self.P_max}, cost={self.cost}, lifetime={self.lifetime})")


