from abc import ABC, abstractmethod
import pickle

class SaveServiceInterface(ABC):
    def __init__(self, db_path):
        self.db_path = db_path

    @property
    @abstractmethod
    def service_name(self):
        pass

    @abstractmethod
    def save_repository(self, repo, query):
        pass

class PickleSaveService(SaveServiceInterface):
    service_name = "pickle"
    def save_repository(self, repo, query):
        pickle.dump(repo, open(self.db_path+query.replace(" ","_")+".pickle", "wb"))

