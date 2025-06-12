from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from .logic import add_truck, add_package, assign_packages

app = FastAPI()


class Dimensions(BaseModel):
    length: float = Field(..., gt=0)
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)


class PackageRequest(BaseModel):
    package_ids: List[str]


@app.post("/trucks")
def create_truck(dimensions: Dimensions):
    try:
        truck = add_truck(dimensions.length, dimensions.width, dimensions.height)
        return {"truck_id": truck.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/packages")
def create_package(dimensions: Dimensions):
    try:
        package = add_package(dimensions.length, dimensions.width, dimensions.height)
        return {"package_id": package.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/assign")
def assign(package_request: PackageRequest):
    result = assign_packages(package_request.package_ids)

    if result["status"] == "assigned":
        return {
            "status": "assigned",
            "truck_id": result["truck_id"],
            "assigned_packages": result["assigned_packages"]
        }
    elif result["status"] == "partial":
        return {
            "status": "partial",
            "truck_id": result["truck_id"],
            "assigned_packages": result["assigned_packages"],
            "deferred_packages": result["deferred_packages"]
        }
    else:
        return {
            "status": "delayed",
            "deferred_packages": result.get("deferred_packages", []),
            "reason": result.get("reason", "Unknown")
        }


@app.post("/reset")
def reset_data():
    from .logic import TRUCKS, PACKAGES, DELAYED_PACKAGES
    TRUCKS.clear()
    PACKAGES.clear()
    DELAYED_PACKAGES.clear()
    return {"status": "reset"}