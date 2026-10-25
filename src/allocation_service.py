from typing import Callable, Generic, TypeVar

from src.device import TeachingDevice
from src.repository import IRepository
from src.selection_strategy import ISelectionStrategy


T = TypeVar("T", bound=TeachingDevice)


class AllocationService(Generic[T]):
    """Tim va cap phat thiet bi theo repository va chien luoc."""

    def __init__(self, repository: IRepository[T], strategy: ISelectionStrategy[T]):
        self._repository = repository
        self._strategy = strategy

    def change_strategy(self, strategy: ISelectionStrategy[T]) -> None:
        if strategy is None:
            raise ValueError("Chien luoc khong duoc la None.")
        self._strategy = strategy

    def allocate(self, condition: Callable[[T], bool] | None = None) -> T:
        candidates = self._repository.find_all(
            lambda item: item.is_ready_for_use()
            and (condition is None or condition(item))
        )
        selected = self._strategy.select(candidates)
        selected.borrow()
        return selected
