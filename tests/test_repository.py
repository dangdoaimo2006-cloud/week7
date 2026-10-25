import unittest

from src.device import (
    AirConditionerRemote,
    ProjectorRemote,
    WirelessMicrophone,
)
from src.repository import DuplicateIdException, InMemoryRepository


class TestInMemoryRepository(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.projector = ProjectorRemote(
            "P01", "Remote may chieu 1", "Tu A", 80
        )
        self.air_remote = AirConditionerRemote(
            "A01", "Remote dieu hoa 1", "Tu B", ["101", "102"]
        )
        self.microphone = WirelessMicrophone(
            "M01", "Micro khong day 1", "Tu C", 75, 90
        )

    def test_add_and_find_by_id(self):
        self.repo.add(self.projector)
        self.assertIs(self.repo.find_by_id("P01"), self.projector)

    def test_duplicate_id_is_rejected(self):
        self.repo.add(self.projector)
        another = ProjectorRemote("P01", "Remote khac", "Tu D", 60)

        with self.assertRaises(DuplicateIdException):
            self.repo.add(another)

    def test_find_missing_id_returns_none(self):
        self.assertIsNone(self.repo.find_by_id("missing"))

    def test_remove_existing_and_missing_items(self):
        self.repo.add(self.projector)
        self.assertTrue(self.repo.remove("P01"))
        self.assertFalse(self.repo.remove("P01"))
        self.assertIsNone(self.repo.find_by_id("P01"))

    def test_get_all_returns_a_separate_list(self):
        self.repo.add(self.projector)
        items = self.repo.get_all()
        items.clear()
        self.assertEqual(len(self.repo.get_all()), 1)

    def test_find_all_filters_items(self):
        self.repo.add(self.projector)
        self.repo.add(self.air_remote)
        self.repo.add(self.microphone)

        result = self.repo.find_all(
            lambda item: item.is_ready_for_use()
        )
        self.assertEqual(len(result), 3)

    def test_repository_accepts_different_device_types(self):
        self.repo.add(self.projector)
        self.repo.add(self.air_remote)
        self.repo.add(self.microphone)

        self.assertEqual(len(self.repo.get_all()), 3)
        self.assertIsInstance(self.repo.find_by_id("P01"), ProjectorRemote)
        self.assertIsInstance(
            self.repo.find_by_id("A01"), AirConditionerRemote
        )
        self.assertIsInstance(
            self.repo.find_by_id("M01"), WirelessMicrophone
        )

    def test_none_cannot_be_added(self):
        with self.assertRaises(ValueError):
            self.repo.add(None)

    def test_find_all_requires_condition(self):
        with self.assertRaises(ValueError):
            self.repo.find_all(None)


if __name__ == "__main__":
    unittest.main()
