from uuid import uuid4


class Truck:
    def __init__(self, length: float, width: float, height: float):
        self.id = str(uuid4())
        self.length = length
        self.width = width
        self.height = height
        self.volume = length * width * height
        self.assigned_packages = []


class Package:
    def __init__(self, length: float, width: float, height: float):
        self.id = str(uuid4())
        self.length = length
        self.width = width
        self.height = height
        self.volume = length * width * height
