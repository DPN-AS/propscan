"""Utility for ordering property listings by geographic proximity."""

import argparse
import csv
import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Property:
    """Simple representation of a property listing."""

    address: str
    latitude: float
    longitude: float


def google_maps_link(lat: float, lon: float) -> str:
    """Return a Google Maps link for routing to the given coordinates."""
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"


def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Calculate the great-circle distance between two (lat, lon) coordinates."""
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def read_properties(csv_path: str) -> List[Property]:
    """Load properties from a CSV file.

    The parser is case-insensitive for latitude/longitude fields and will use
    the ``ADDRESS`` column as a descriptive label.
    """

    def get_value(row: dict, *keys: str) -> str:
        for key in keys:
            if key in row:
                return row[key]
        return ""

    properties: List[Property] = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat = float(get_value(row, "LATITUDE", "latitude"))
            lon = float(get_value(row, "LONGITUDE", "longitude"))
            address = get_value(row, "ADDRESS", "address")
            properties.append(Property(address, lat, lon))
    return properties


def order_properties(properties: List[Property]) -> List[Property]:
    """Return properties ordered by a nearest-neighbor heuristic."""
    if not properties:
        return []

    remaining = properties.copy()
    ordered = [remaining.pop(0)]
    while remaining:
        last = ordered[-1]
        last_coord = (last.latitude, last.longitude)
        nearest_idx = min(
            range(len(remaining)),
            key=lambda i: haversine(last_coord, (remaining[i].latitude, remaining[i].longitude)),
        )
        ordered.append(remaining.pop(nearest_idx))
    return ordered


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Sort properties by proximity")
    parser.add_argument(
        "csv",
        help="Path to CSV file containing ADDRESS, LATITUDE, and LONGITUDE columns",
    )
    args = parser.parse_args(argv)

    props = read_properties(args.csv)
    ordered = order_properties(props)
    for prop in ordered:
        link = google_maps_link(prop.latitude, prop.longitude)
        print(f"{prop.address} - {link}")


if __name__ == "__main__":
    main()
