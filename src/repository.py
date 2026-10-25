from abc import ABC, abstractmethod
from typing import Callable, Generic, Optional, Protocol, TypeVar


class IIdentifiable(Protocol):
    """Cac doi tuong co ma dinh danh."""

    @property
    def id(self):
        ...


T = TypeVar("T", bound=IIdentifiable)


class DuplicateIdException(Exception):
    """Loi khi them doi tuong co ID da ton tai."""

    pass


class IRepository(ABC, Generic[T]):
    """Giao dien repository cho cac doi tuong co ID."""

    @abstractmethod
    def add(self, item: T) -> None:
        pass

    @abstractmethod
    def remove(self, item_id) -> bool:
        pass

    @abstractmethod
    def find_by_id(self, item_id) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def find_all(self, condition: Callable[[T], bool]) -> list[T]:
        pass


class InMemoryRepository(IRepository[T]):
    def __init__(self):
        self._items: dict[object, T] = {}

    def add(self, item: T) -> None:
        if item is None:
            raise ValueError("Khong the them doi tuong None.")

        item_id = item.id
        if item_id in self._items:
            raise DuplicateIdException(
                f"ID '{item_id}' da ton tai trong repository."
            )

        self._items[item_id] = item

    def remove(self, item_id) -> bool:
        if item_id not in self._items:
            return False

        del self._items[item_id]
        return True

    def find_by_id(self, item_id) -> Optional[T]:
        return self._items.get(item_id)

    def get_all(self) -> list[T]:
        # Tra ve ban sao de ben ngoai khong sua truc tiep duoc kho du lieu.
        return list(self._items.values())

    def find_all(self, condition: Callable[[T], bool]) -> list[T]:
        if condition is None:
            raise ValueError("Dieu kien tim kiem khong duoc la None.")

        return [item for item in self._items.values() if condition(item)]
