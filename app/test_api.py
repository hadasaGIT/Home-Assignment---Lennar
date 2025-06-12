import pytest
import requests

BASE_URL = "http://localhost:8000"


# Clear state before each test (relies on your FastAPI app having in-memory data)
def setup_function():
    requests.post(f"{BASE_URL}/reset")  # You can implement this if needed


def create_truck(length, width, height):
    res = requests.post(f"{BASE_URL}/trucks", json={
        "length": length, "width": width, "height": height
    })
    assert res.status_code == 200, f"Truck creation failed: {res.text}"
    return res.json()["truck_id"]


def create_package(length, width, height):
    res = requests.post(f"{BASE_URL}/packages", json={
        "length": length, "width": width, "height": height
    })
    assert res.status_code == 200, f"Package creation failed: {res.text}"
    return res.json()["package_id"]


def assign_packages(package_ids):
    res = requests.post(f"{BASE_URL}/assign", json={
        "package_ids": package_ids
    })
    assert res.status_code == 200, f"Assignment failed: {res.text}"
    return res.json()


@pytest.mark.status
def test_status_assigned():
    truck_id = create_truck(5, 5, 5)  # Volume = 125
    packages = [
        create_package(2, 2, 2),  # 8
        create_package(3, 3, 3),  # 27
        create_package(3, 2, 4),  # 24
        create_package(3, 3, 2.5),  # 22.5
        create_package(2, 2, 3),  # 12
        create_package(2, 2, 2)  # 8 -> Total = 101.5 (≈81.2%)
    ]

    result = assign_packages(packages)

    assert result["status"] == "assigned", f"Expected 'assigned', got: {result}"
    assert "truck_id" in result
    assert "assigned_packages" in result
    assert set(result["assigned_packages"]) == set(packages)
    print("✔ test_status_assigned passed.")


@pytest.mark.status
def test_status_partial():
    truck_id = create_truck(5, 5, 5)  # Volume = 125
    packages = [create_package(3, 3, 4) for _ in range(5)]  # Each = 36 → Total = 180

    result = assign_packages(packages)

    assert result["status"] == "partial", f"Expected 'partial', got: {result}"
    assert "truck_id" in result
    assert "assigned_packages" in result
    assert "deferred_packages" in result
    assert len(result["assigned_packages"]) < len(packages)
    print("✔ test_status_partial passed.")


@pytest.mark.status
def test_status_delayed():
    truck_id = create_truck(2, 2, 2)  # Volume = 8
    package_id = create_package(5, 5, 5)  # Volume = 125 → too big for any truck

    result = assign_packages([package_id])

    assert result["status"] == "delayed", f"Expected 'delayed', got: {result}"
    assert package_id in result["deferred_packages"]
    print("✔ test_status_delayed passed.")


@pytest.mark.status
def test_status_empty_package_list():
    truck_id = create_truck(5, 5, 5)

    result = assign_packages([])

    assert result["status"] == "delayed"
    assert "reason" in result
    print("✔ test_status_empty_package_list passed.")
