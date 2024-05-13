from abc import ABC, abstractmethod
from api.models.transaction import TransactionModelPandas, TransactionModel


# creating this this way so it is easier if we would decide to move away from a pandas df
class TransactionRepo(ABC):
    
    @abstractmethod
    def iterate_all(self) -> TransactionModel:
        pass



class PandasTransactionRepo:
    def __init__(self, df) -> None:
        self.df = df

    # / get all
    def iterate_all(self):
        for _, row in self.df.iterrows():
            yield TransactionModelPandas(row)

