from abc import ABC, abstractclassmethod


class StructInterface(ABC):

    @abstractclassmethod
    def default(cls: 'StructInterface') -> 'StructInterface':
        ...
