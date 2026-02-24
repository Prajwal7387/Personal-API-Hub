from typing import Type, TypeVar, Generic, List, Optional, Any
from django.db import models

T = TypeVar('T', bound=models.Model)

class BaseRepository(Generic[T]):
    """
    Abstract Base Repository for all model-specific repositories.
    """
    def __init__(self, model: Type[T]):
        self.model = model

    def get_by_id(self, id: Any) -> Optional[T]:
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None

    def list_all(self) -> List[T]:
        return list(self.model.objects.all())

    def filter(self, **kwargs) -> List[T]:
        return list(self.model.objects.filter(**kwargs))

    def create(self, **kwargs) -> T:
        return self.model.objects.create(**kwargs)

    def update(self, instance: T, **kwargs) -> T:
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance: T) -> None:
        instance.delete()
