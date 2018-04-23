from abc import ABC, abstractmethod
from app import gmaps

class BaseController(ABC):

    def __init__(self):
        self.language = "en-US"
        self.api = gmaps