from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

class BaseNormalizer(ABC):
    """
    Abstract Base Class for normalizing external API data into a standard internal format.
    """

    @abstractmethod
    def normalize(self, raw_data: Union[Dict, List]) -> Union[Dict, List]:
        """
        Takes raw data (dict or list) and transforms it into the normalized schema.
        """
        pass

    def normalize_collection(self, collection: List[Dict]) -> List[Dict]:
        """
        Helper method to normalize a list of items.
        """
        return [self.normalize(item) for item in collection]
