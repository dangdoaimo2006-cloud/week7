from abc import ABC
from enum import Enum


class DeviceStatus(Enum):
    # Cac trang thai cua thiet bi
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    UNDER_MAINTENANCE = "UnderMaintenance"


class DeviceNotReadyException(Exception):
    pass


class TeachingDevice(ABC):
    def __init__(self, device_id, name, storage_location,
                 status=DeviceStatus.AVAILABLE):
        self.id = device_id
        self.name = name
        self.storage_location = storage_location
        self.status = status

    def is_ready_for_use(self):
        return self.status == DeviceStatus.AVAILABLE

    def get_default_priority_score(self):
        return 0

    def borrow(self):
        if not self.is_ready_for_use():
            raise DeviceNotReadyException(
                "Thiet bi chua san sang de muon."
            )
        self.status = DeviceStatus.BORROWED

    def return_device(self):
        if self.status == DeviceStatus.BORROWED:
            self.status = DeviceStatus.AVAILABLE

    def __str__(self):
        return (
            f"ID: {self.id}, Ten: {self.name}, "
            f"Vi tri: {self.storage_location}, "
            f"Trang thai: {self.status.value}"
        )


class ProjectorRemote(TeachingDevice):
    def __init__(self, device_id, name, storage_location,
                 battery_level, status=DeviceStatus.AVAILABLE):
        super().__init__(
            device_id, name, storage_location, status
        )
        self.battery_level = battery_level

    def is_ready_for_use(self):
        return (
            self.status == DeviceStatus.AVAILABLE
            and self.battery_level >= 20
        )

    def get_default_priority_score(self):
        return self.battery_level


class AirConditionerRemote(TeachingDevice):
    def __init__(self, device_id, name, storage_location,
                 compatible_rooms, status=DeviceStatus.AVAILABLE):
        super().__init__(
            device_id, name, storage_location, status
        )
        self.compatible_rooms = set(compatible_rooms)

    def is_compatible_with(self, room_id):
        return room_id in self.compatible_rooms

    def is_ready_for_use(self):
        return self.status == DeviceStatus.AVAILABLE

    def get_default_priority_score(self):
        return 100 if self.is_ready_for_use() else 0


class WirelessMicrophone(TeachingDevice):
    def __init__(self, device_id, name, storage_location,
                 battery_level, signal_quality,
                 status=DeviceStatus.AVAILABLE):
        super().__init__(
            device_id, name, storage_location, status
        )
        self.battery_level = battery_level
        self.signal_quality = signal_quality

    def is_ready_for_use(self):
        return (
            self.status == DeviceStatus.AVAILABLE
            and self.battery_level >= 30
            and self.signal_quality >= 40
        )

    def get_default_priority_score(self):
        return (self.battery_level + self.signal_quality) / 2
