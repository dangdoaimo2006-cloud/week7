import unittest

from src.device import (
    DeviceStatus,
    ProjectorRemote,
    AirConditionerRemote,
    WirelessMicrophone,
    DeviceNotReadyException,
)


class TestTeachingDevice(unittest.TestCase):
    def setUp(self):
        self.projector = ProjectorRemote(
            "PR01", "Remote may chieu", "Tu A", 80
        )
        self.air_conditioner = AirConditionerRemote(
            "AC01", "Remote dieu hoa", "Tu B",
            ["P101", "P102"]
        )
        self.microphone = WirelessMicrophone(
            "MIC01", "Micro khong day", "Tu C", 70, 80
        )

    def test_projector_ready(self):
        self.assertTrue(self.projector.is_ready_for_use())
        self.assertEqual(
            self.projector.get_default_priority_score(), 80
        )

    def test_projector_low_battery(self):
        remote = ProjectorRemote(
            "PR02", "Remote yeu pin", "Tu A", 10
        )
        self.assertFalse(remote.is_ready_for_use())

    def test_air_conditioner_compatible_room(self):
        self.assertTrue(
            self.air_conditioner.is_compatible_with("P101")
        )
        self.assertFalse(
            self.air_conditioner.is_compatible_with("P103")
        )

    def test_microphone_ready(self):
        self.assertTrue(self.microphone.is_ready_for_use())
        self.assertEqual(
            self.microphone.get_default_priority_score(), 75
        )

    def test_borrow_changes_status(self):
        self.projector.borrow()
        self.assertEqual(
            self.projector.status, DeviceStatus.BORROWED
        )

    def test_cannot_borrow_unready_device(self):
        remote = ProjectorRemote(
            "PR03", "Remote hong pin", "Tu A", 5
        )
        with self.assertRaises(DeviceNotReadyException):
            remote.borrow()

    def test_return_device(self):
        self.projector.borrow()
        self.projector.return_device()
        self.assertEqual(
            self.projector.status, DeviceStatus.AVAILABLE
        )


if __name__ == "__main__":
    unittest.main()
