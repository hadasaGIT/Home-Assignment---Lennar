from pydantic import BaseModel
from typing import List


class TruckCreate(BaseModel):
    length: float
    width: float
    height: float


class PackageCreate(BaseModel):
    length: float
    width: float
    height: float


class AssignRequest(BaseModel):
    package_ids: List[str]


class AssignResponseAssigned(BaseModel):
    status: str
    truck_id: str
    assigned_packages: List[str]


class AssignResponsePartial(BaseModel):
    status: str
    truck_id: str
    assigned_packages: List[str]
    deferred_packages: List[str]


class AssignResponseDelayed(BaseModel):
    status: str
    deferred_packages: List[str]
