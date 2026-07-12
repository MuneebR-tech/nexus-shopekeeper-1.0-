"""
Nexus Shopkeeper - Phase 1: Physical Rack-to-Coordinate Mapping System
Maps rack IDs to physical coordinates (x, y, z) in meters and performs spatial queries
such as finding nearest items and pathing shopping routes.
"""

import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Add project root to python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from data.schemas.inventory_schema import InventoryItem


class RackMap:
    """
    Physical layout map of the retail store.
    Grid layout:
    - 6 aisles (A, B, C, D, E, F) mapped to X-coordinate (meters):
        A=2.0m, B=4.0m, C=6.0m, D=8.0m, E=10.0m, F=12.0m (with aisles separated by 2m)
    - 5 sections (1, 2, 3, 4, 5) mapped to Y-coordinate (meters):
        1=1.5m, 2=3.5m, 3=5.5m, 4=7.5m, 5=9.5m (sections separated by 2m)
    - Each rack has 5 shelves (1 to 5) mapped to Z-coordinate (meters):
        1=0.3m, 2=0.7m, 3=1.1m, 4=1.5m, 5=1.9m
    - Entrance/Checkout at (0.0, 0.0, 0.0)
    """

    AISLE_MAP = {"A": 2.0, "B": 4.0, "C": 6.0, "D": 8.0, "E": 10.0, "F": 12.0}
    SECTION_MAP = {1: 1.5, 2: 3.5, 3: 5.5, 4: 7.5, 5: 9.5}
    SHELF_MAP = {1: 0.3, 2: 0.7, 3: 1.1, 4: 1.5, 5: 1.9}

    def __init__(self, inventory_path: Optional[Path] = None):
        self.inventory: Dict[str, InventoryItem] = {}
        self.rack_contents: Dict[str, List[InventoryItem]] = {}
        
        # Initialize rack layout buckets
        for aisle in self.AISLE_MAP.keys():
            for section in self.SECTION_MAP.keys():
                rack_id = f"{aisle}{section}"
                self.rack_contents[rack_id] = []

        if inventory_path:
            self.load_inventory(inventory_path)

    def load_inventory(self, path: Path):
        """Loads inventory items and assigns them to physical racks."""
        if not path.exists():
            raise FileNotFoundError(f"Inventory file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            items_data = json.load(f)

        for item_dict in items_data:
            item = InventoryItem(**item_dict)
            self.inventory[item.item_id] = item
            rack_id = item.rack_id
            if rack_id in self.rack_contents:
                self.rack_contents[rack_id].append(item)
            else:
                self.rack_contents[rack_id] = [item]

    @classmethod
    def get_rack_coordinates(cls, rack_id: str, shelf_position: int = 3) -> Tuple[float, float, float]:
        """
        Translates a rack ID and shelf position into (x, y, z) coordinates in meters.
        Default shelf position is 3 (middle shelf).
        """
        if len(rack_id) < 2:
            raise ValueError(f"Invalid rack_id: {rack_id}")
        
        aisle_letter = rack_id[0].upper()
        try:
            section_num = int(rack_id[1:])
        except ValueError:
            raise ValueError(f"Invalid section suffix in rack_id: {rack_id}")

        x = cls.AISLE_MAP.get(aisle_letter, 2.0)
        y = cls.SECTION_MAP.get(section_num, 1.5)
        z = cls.SHELF_MAP.get(shelf_position, 1.1)
        return x, y, z

    def get_item_location(self, item_id: str) -> Optional[Tuple[float, float, float]]:
        """Returns the physical (x, y, z) coordinates of an item by ID."""
        item = self.inventory.get(item_id)
        if not item:
            return None
        return self.get_rack_coordinates(item.rack_id, item.shelf_position)

    def get_nearest_items(self, x: float, y: float, z: float, n: int = 5) -> List[Tuple[InventoryItem, float]]:
        """
        Finds the n nearest items in the store relative to the given coordinates.
        Returns list of (InventoryItem, distance_in_meters).
        """
        distances = []
        for item in self.inventory.values():
            ix, iy, iz = self.get_rack_coordinates(item.rack_id, item.shelf_position)
            dist = math.sqrt((x - ix) ** 2 + (y - iy) ** 2 + (z - iz) ** 2)
            distances.append((item, dist))

        # Sort by distance
        distances.sort(key=lambda item_dist: item_dist[1])
        return distances[:n]

    def calculate_shopping_route(self, item_list: List[str]) -> Tuple[List[str], float]:
        """
        Calculates an optimized shopping route for a list of item IDs using a 
        Nearest Neighbor heuristic (solving TSP starting and ending at Entrance (0,0,0)).
        Returns (ordered_item_ids, total_distance_meters).
        """
        # Validate items and get locations
        targets = []
        for item_id in item_list:
            if item_id in self.inventory:
                loc = self.get_item_location(item_id)
                if loc:
                    targets.append((item_id, loc))

        if not targets:
            return [], 0.0

        current_loc = (0.0, 0.0, 0.0)  # Start at Entrance
        route = []
        total_distance = 0.0

        while targets:
            # Find nearest remaining target
            nearest_idx = -1
            min_dist = float("inf")
            for idx, (_, loc) in enumerate(targets):
                dist = math.sqrt(
                    (current_loc[0] - loc[0]) ** 2 +
                    (current_loc[1] - loc[1]) ** 2 +
                    (current_loc[2] - loc[2]) ** 2
                )
                if dist < min_dist:
                    min_dist = dist
                    nearest_idx = idx

            # Move to nearest target
            nearest_item_id, nearest_loc = targets.pop(nearest_idx)
            route.append(nearest_item_id)
            total_distance += min_dist
            current_loc = nearest_loc

        # Return to checkout/entrance at (0, 0, 0)
        final_dist = math.sqrt(current_loc[0]**2 + current_loc[1]**2 + current_loc[2]**2)
        total_distance += final_dist

        return route, total_distance

    def print_layout_map(self):
        """Prints a visual 2D layout grid representing rack placement and item counts."""
        print("\n========================================================================")
        # Sort section indices descending so section 5 is at the top of the print layout
        sections = sorted(self.SECTION_MAP.keys(), reverse=True)
        aisles = sorted(self.AISLE_MAP.keys())

        print("                   STORE FLOOR PLAN (RACK GRID LAYOUT)")
        print("          Entrance & Checkout located at bottom-left origin (0, 0)\n")
        print("        " + "      ".join([f"Aisle {a}" for a in aisles]))
        print("        " + "------".join(["-" * 8 for _ in aisles]))

        for sec in sections:
            row_str = f"Sec {sec} | "
            for aisle in aisles:
                rack_id = f"{aisle}{sec}"
                items_in_rack = self.rack_contents.get(rack_id, [])
                count = len(items_in_rack)
                row_str += f"[{rack_id}:{count:02d}]  "
            print(row_str)

        print("        " + "------".join(["-" * 8 for _ in aisles]))
        print("  X coords: " + "    ".join([f"{self.AISLE_MAP[a]:4.1f}m" for a in aisles]))
        print("========================================================================\n")


def main():
    print("========================================================================")
    print("  NEXUS SHOPKEEPER - Phase 1 Physical Rack Mapping Demonstration")
    print("========================================================================")

    inventory_file = PROJECT_ROOT / "data" / "raw" / "inventory.json"
    
    # Initialize RackMap
    try:
        rack_map = RackMap(inventory_file)
        print(f"Loaded {len(rack_map.inventory)} items from inventory.")
    except Exception as e:
        print(f"Error loading inventory: {e}")
        print("Initializing empty map.")
        rack_map = RackMap()

    # Visual map
    rack_map.print_layout_map()

    if rack_map.inventory:
        # Test spatial query
        print("Spatial Queries:")
        sample_item = list(rack_map.inventory.values())[0]
        loc = rack_map.get_item_location(sample_item.item_id)
        print(f"  Item: {sample_item.name} ({sample_item.item_id})")
        print(f"  Location: rack={sample_item.rack_id}, shelf={sample_item.shelf_position} -> Coord: {loc}")

        # Test nearest items
        test_coord = (5.0, 4.0, 1.0)
        print(f"\n  Querying 3 nearest items to coordinate {test_coord}:")
        nearest = rack_map.get_nearest_items(test_coord[0], test_coord[1], test_coord[2], n=3)
        for item, dist in nearest:
            iloc = rack_map.get_item_location(item.item_id)
            print(f"    - {item.name} ({item.item_id}) at {item.rack_id} (shelf {item.shelf_position}, coord={iloc}) - Distance: {dist:.2f}m")

        # Test route optimization
        route_item_ids = [item.item_id for item, _ in nearest]
        print(f"\n  Calculating shopping route for items: {route_item_ids}")
        route, distance = rack_map.calculate_shopping_route(route_item_ids)
        print("    Optimized Route Path:")
        print("      Origin (0.0, 0.0, 0.0)")
        for step_id in route:
            it = rack_map.inventory[step_id]
            iloc = rack_map.get_item_location(step_id)
            print(f"      -> {it.name} at rack {it.rack_id} (coord={iloc})")
        print("      -> Checkout (0.0, 0.0, 0.0)")
        print(f"    Total Route distance: {distance:.2f} meters")


if __name__ == "__main__":
    main()
