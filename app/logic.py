from .models import Truck, Package
from typing import Dict, List, Optional

# Simulated in-memory database
TRUCKS: Dict[str, Truck] = {}
PACKAGES: Dict[str, Package] = {}
DELAYED_PACKAGES: List[str] = []


def validate_dimensions(length: float, width: float, height: float):
    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError("All dimensions must be positive numbers.")


def add_truck(length: float, width: float, height: float) -> Truck:
    validate_dimensions(length, width, height)
    truck = Truck(length, width, height)
    TRUCKS[truck.id] = truck
    return truck


def add_package(length: float, width: float, height: float) -> Package:
    validate_dimensions(length, width, height)
    package = Package(length, width, height)
    PACKAGES[package.id] = package
    return package


def assign_packages(package_ids: List[str]) -> dict:
    valid_packages = [PACKAGES[pid] for pid in package_ids if pid in PACKAGES]
    if not valid_packages:
        return {
            "status": "delayed",
            "deferred_packages": package_ids,
            "reason": "No valid packages found"
        }

    total_volume = sum(p.volume for p in valid_packages)

    best_truck: Optional[Truck] = None
    best_fill = 0.0

    # Try to assign to truck with 80%-100% fill
    for truck in TRUCKS.values():
        if truck.assigned_packages:
            continue  # truck already used
        fill_ratio = total_volume / truck.volume
        if 0.8 <= fill_ratio <= 1.0 and fill_ratio > best_fill:
            best_fill = fill_ratio
            best_truck = truck

    if best_truck:
        best_truck.assigned_packages = [p.id for p in valid_packages]
        return {
            "status": "assigned",
            "truck_id": best_truck.id,
            "assigned_packages": best_truck.assigned_packages
        }

    # Try partial assignment
    for truck in TRUCKS.values():
        if truck.assigned_packages:
            continue
        assigned = []
        used_volume = 0.0
        for p in valid_packages:
            if used_volume + p.volume <= truck.volume:
                assigned.append(p.id)
                used_volume += p.volume

        if assigned:
            truck.assigned_packages = assigned
            deferred = [p.id for p in valid_packages if p.id not in assigned]
            DELAYED_PACKAGES.extend(deferred)
            return {
                "status": "partial",
                "truck_id": truck.id,
                "assigned_packages": assigned,
                "deferred_packages": deferred
            }

    # No truck could accept the packages
    deferred = [p.id for p in valid_packages]
    DELAYED_PACKAGES.extend(deferred)
    return {
        "status": "delayed",
        "deferred_packages": deferred,
        "reason": "No suitable truck found"
    }
