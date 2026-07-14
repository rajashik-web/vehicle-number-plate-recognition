from src.database import DatabaseManager


class ParkingManager:

    def __init__(self):

        self.db = DatabaseManager()

    def vehicle_entry(self, plate_number):

        if plate_number.strip() == "":
            return False, "Please enter the vehicle number."

        success = self.db.add_vehicle(
            plate_number.upper()
        )

        if success:
            return True, f"{plate_number.upper()} entered successfully."

        return False, f"{plate_number.upper()} is already inside."

    def vehicle_exit(self, plate_number):

        if plate_number.strip() == "":
            return False, "Please enter the vehicle number."

        success = self.db.vehicle_exit(
            plate_number.upper()
        )

        if success:
            return True, f"{plate_number.upper()} exited successfully."

        return False, "Vehicle not found."

    def dashboard(self):

        return self.db.get_dashboard_stats()

    def records(self):

        return self.db.get_all_records()

    def search(self, plate_number):

        return self.db.search_vehicle(
            plate_number.upper()
        )