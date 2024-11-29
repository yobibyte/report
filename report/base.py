from abc import ABC, abstractmethod


class Report(ABC):
    def __init__(self, title):
        self._title = title

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

    def save(self):
        # TODO(yobibyte)
        pass

    def generate(self):
        self.load_data()
        self.prepare()
        self.save()
