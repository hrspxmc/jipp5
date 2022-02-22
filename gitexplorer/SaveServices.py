from abc import ABC, abstractmethod
import pickle
import csv
from collections.abc import MutableMapping
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Sequence, create_engine

Base = declarative_base()
class RepoEntity(Base):
    __tablename__ = 'repos'
    id = Column(Integer, Sequence("repo_id"), primary_key=True)
    url = Column(String)
    name = Column(String)
    query = Column(String)

def _flatten_dict(d, parent_key = '', sep ='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
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

class CsvSaveService(SaveServiceInterface):
    service_name = "csv"
    def save_repository(self, repo, query):
        flatten_repo = [_flatten_dict(ii) for ii in repo]
        with open(self.db_path+query.replace(" ","_")+".csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = flatten_repo[1].keys())
            writer.writeheader()
            writer.writerows(flatten_repo)
class SQLiteSaveService(SaveServiceInterface):
    service_name = "SQLite"

    def __init__(self, db_path):
        self.db_path = db_path
        self.engine = create_engine('sqlite:///'+self.db_path)
        self.session = sessionmaker(bind=self.engine)()

    def save_repository(self, repo, query):
        for ii in repo:
            tmp_repo = RepoEntity(
                url = ii['url'],
                name = ii['name'],
                query = query) 
            self.session.add(tmp_repo)
        self.session.commit()

