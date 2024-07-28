from abc import ABC, abstractmethod

class System(ABC):

    @abstractmethod
    def total_investment_cost(self):
        """
        Method to calculate the total investment cost of the energy system.
        This method should be implemented in the subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def __repr__(self):
        """
        Return a string representation of the energy system.
        This method should be implemented by all subclasses to ensure that each system
        can provide a clear and useful representation of its state.
        """
        raise NotImplementedError("Subclasses must implement this method")