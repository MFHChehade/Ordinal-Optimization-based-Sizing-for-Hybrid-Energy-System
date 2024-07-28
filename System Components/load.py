import pandas as pd
from component import Component 

class Load(Component):
    def __init__(self, load_data: pd.DataFrame):
        """
        Initialize a new Load object with specified load data.

        - load_data (DataFrame): A pandas DataFrame containing the load data with required columns.
        """
        self.load_data = self.validate_load_data(load_data)

    def validate_load_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Validate that the DataFrame contains all required columns for load operations.

        - data (DataFrame): The load dataset to validate.
        """
        required_columns = ["month", "day", "hour", "demand"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required data columns: {missing_columns}")
        return data

    def get_demand(self, month: int, day: int, hour: int) -> float:
        """
        Retrieve the demand for a given time.

        - month (int): Month of the year.
        - day (int): Day of the month.
        - hour (int): Hour of the day.

        Returns:
        - float: Demand in kWh at the specified time.
        """
        record = self.load_data[(self.load_data['month'] == month) &
                                (self.load_data['day'] == day) &
                                (self.load_data['hour'] == hour)]
        if record.empty:
            return None  # Or handle with a default value or error message
        return record.iloc[0]['demand']
    
    def investment_cost(self):
        return 0 

    # Getters and Setters
    def get_load_data(self):
        return self.load_data

    def set_load_data(self, new_data: pd.DataFrame):
        self.load_data = self.validate_load_data(new_data)

    def __repr__(self):
        return f"Load(data_columns={list(self.load_data.columns)})"
