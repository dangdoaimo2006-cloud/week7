from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")


class NoSuitableItemException(Exception):
    """Loi khi khong co doi tuong phu hop."""

    pass


class ISelectionStrategy(ABC, Generic[T]):
    """Giao dien cho cac chien luoc lua chon."""

    @abstractmethod
    def select(self, candidates: list[T]) -> T:
        pass


class HighestPriorityStrategy(ISelectionStrategy[T]):
    """Chon doi tuong co diem uu tien cao nhat."""

    def select(self, candidates: list[T]) -> T:
        if not candidates:
            raise NoSuitableItemException("Khong co doi tuong phu hop.")
        return max(candidates, key=lambda item: item.get_default_priority_score())


class FirstAvailableStrategy(ISelectionStrategy[T]):
    """Chon doi tuong dau tien trong danh sach ung vien."""

    def select(self, candidates: list[T]) -> T:
        if not candidates:
            raise NoSuitableItemException("Khong co doi tuong phu hop.")
        return candidates[0]
