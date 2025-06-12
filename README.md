
# 📦 Warehouse & Truck Assignment System

## 🧭 Overview
A lightweight backend system that manages packages and trucks. The main goal is to assign packages to trucks such that the truck is at least 80% full. Otherwise, the shipment is delayed.

## ✅ Features
- Add trucks and packages (with dimensions)
- Auto volume calculation
- Volume-based truck assignment logic
- Supports: assigned / partial / delayed
- FastAPI-based REST API
- Pytest coverage for all cases

## 🗄️ Database
- Current: In-Memory (Dict-based)
- Production: PostgreSQL + SQLAlchemy recommended

## 🚚 Data Models
### Truck:
- id: UUID
- length, width, height: float
- volume: float (computed)
- assigned_packages: List[str]

### Package:
- id: UUID
- length, width, height: float
- volume: float

## 🚀 Run the App
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🔌 Run Tests
```bash
pytest app/test_api.py -v
```

## 🧠 Bin Packing (Bonus)
Instead of naive volume comparison, Best-Fit Decreasing or similar heuristics can be applied to simulate realistic package arrangement.

## 📚 Technologies Used
- FastAPI
- Pydantic
- UUID
- Pytest

## 📄 Attached Files
- System_Design.pdf
- Work_Item_3_Bin_Packing.pdf
