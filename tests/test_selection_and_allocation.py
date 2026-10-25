import unittest

from src.allocation_service import AllocationService
from src.device import AirConditionerRemote, ProjectorRemote, WirelessMicrophone, DeviceStatus
from src.repository import InMemoryRepository
from src.selection_strategy import (
    FirstAvailableStrategy,
    HighestPriorityStrategy,
    NoSuitableItemException,
)


class SelectionStrategyTests(unittest.TestCase):
    def test_highest_priority_selects_projector_with_more_battery(self):
        items = [
            ProjectorRemote("P1", "Remote 1", "A", 40),
            ProjectorRemote("P2", "Remote 2", "A", 85),
        ]
        self.assertEqual(HighestPriorityStrategy().select(items).id, "P2")

    def test_first_available_returns_first_candidate(self):
        items = [
            WirelessMicrophone("M1", "Mic 1", "A", 60, 70),
            WirelessMicrophone("M2", "Mic 2", "A", 90, 90),
        ]
        self.assertEqual(FirstAvailableStrategy().select(items).id, "M1")

    def test_empty_candidates_raise_exception(self):
        with self.assertRaises(NoSuitableItemException):
            FirstAvailableStrategy().select([])


class AllocationServiceTests(unittest.TestCase):
    def test_allocate_filters_not_ready_devices_and_borrows_selected(self):
        repo = InMemoryRepository()
        repo.add(ProjectorRemote("P1", "Low battery", "A", 10))
        repo.add(ProjectorRemote("P2", "Good battery", "A", 75))
        service = AllocationService(repo, HighestPriorityStrategy())
        chosen = service.allocate()
        self.assertEqual(chosen.id, "P2")
        self.assertEqual(chosen.status, DeviceStatus.BORROWED)

    def test_allocate_air_conditioner_for_requested_room(self):
        repo = InMemoryRepository()
        repo.add(AirConditionerRemote("A1", "Remote A", "A", ["101"]))
        repo.add(AirConditionerRemote("A2", "Remote B", "A", ["202"]))
        service = AllocationService(repo, FirstAvailableStrategy())
        chosen = service.allocate(lambda item: item.is_compatible_with("202"))
        self.assertEqual(chosen.id, "A2")

    def test_strategy_can_be_changed(self):
        repo = InMemoryRepository()
        repo.add(ProjectorRemote("P1", "Remote 1", "A", 40))
        repo.add(ProjectorRemote("P2", "Remote 2", "A", 80))
        service = AllocationService(repo, FirstAvailableStrategy())
        self.assertEqual(service.allocate().id, "P1")
        # Tra lai thiet bi de kiem tra chien luoc tiep theo.
        repo.find_by_id("P1").return_device()
        service.change_strategy(HighestPriorityStrategy())
        self.assertEqual(service.allocate().id, "P2")

    def test_no_ready_candidate_raises_exception(self):
        repo = InMemoryRepository()
        repo.add(ProjectorRemote("P1", "Low battery", "A", 10))
        service = AllocationService(repo, HighestPriorityStrategy())
        with self.assertRaises(NoSuitableItemException):
            service.allocate()

    def test_repository_works_with_multiple_device_types(self):
        repo = InMemoryRepository()
        repo.add(ProjectorRemote("P1", "Remote", "A", 50))
        repo.add(WirelessMicrophone("M1", "Mic", "A", 70, 60))
        self.assertEqual(len(repo.get_all()), 2)


if __name__ == "__main__":
    unittest.main()
