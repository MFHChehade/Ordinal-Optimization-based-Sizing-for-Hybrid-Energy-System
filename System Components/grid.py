import pandas as pd
from component import Component

class Grid(Component):
    def __init__(self, grid_data: pd.DataFrame):
        """
        Initialize a new Grid object with a specified dataset.

        - grid_data (DataFrame): A pandas DataFrame containing the grid data with required columns.
        """
        self.grid_data = self.validate_grid_data(grid_data)

    def validate_grid_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Validate that the DataFrame contains all required columns for grid operations.

        - data (DataFrame): The grid dataset to validate.
        """
        required_columns = ["month", "day", "hour", "tariff", "status"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required data columns: {missing_columns}")
        return data

    def get_grid_status_and_tariff(self, month: int, day: int, hour: int) -> tuple:
        """
        Retrieve the grid status and tariff for a given time.

        - month (int): Month of the year.
        - day (int): Day of the month.
        - hour (int): Hour of the day.

        Returns:
        - tuple: Contains (status, tariff) where status is 0 (off) or 1 (on) and tariff is the cost.
        """
        record = self.grid_data[(self.grid_data['month'] == month) &
                                (self.grid_data['day'] == day) &
                                (self.grid_data['hour'] == hour)]
        if record.empty:
            return (None, None)  # or some default or error handling
        status = record.iloc[0]['status']
        tariff = record.iloc[0]['tariff']
        return (status, tariff)

    def calculate_investment_cost(self):
        """
        Calculate the investment cost of using the grid, which is 0 for grid users.

        Returns:
        - float: The investment cost, which is 0.
        """
        return 0

    # Getters
    def get_grid_data(self):
        return self.grid_data

    # Setters
    def set_grid_data(self, new_data: pd.DataFrame):
        self.grid_data = self.validate_grid_data(new_data)

    def __repr__(self):
        return f"Grid(data_columns={list(self.grid_data.columns)})"
