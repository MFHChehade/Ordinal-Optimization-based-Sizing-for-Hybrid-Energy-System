from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def investment_cost(self):
        """
        Method to calculate the investment cost of the component.
        This method should be implemented in the subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")
