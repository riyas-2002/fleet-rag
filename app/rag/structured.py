import json


def load_driver_data():
    with open("data/logs/driver_routes.json", "r") as f:
        return json.load(f)


def get_all_drivers():
    data = load_driver_data()
    return list(set(d["driver"].lower() for d in data))


def get_routes_by_driver(name):
    data = load_driver_data()
    return [d["route"] for d in data if d["driver"].lower() == name.lower()]