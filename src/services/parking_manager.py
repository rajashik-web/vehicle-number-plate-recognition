from src.database import DatabaseManager


class ParkingManager:

    def __init__(self):

        self.db = DatabaseManager()

    def vehicle_entry(self, plate_number, image_path=""):

        plate_number = plate_number.strip().upper()

        if plate_number == "":
            return False, "Please enter the vehicle number."

        success = self.db.add_vehicle(
            plate_number,
            image_path
        )

        if success:
            return True, f"{plate_number} entered successfully."

        return False, f"{plate_number} is already inside."

    def vehicle_exit(self, plate_number):

        plate_number = plate_number.strip().upper()

        if plate_number == "":
            return False, "Please enter the vehicle number."

        success = self.db.vehicle_exit(
            plate_number
        )

        if success:
            return True, f"{plate_number} exited successfully."

        return False, "Vehicle not found."

    def dashboard(self):

        return self.db.get_dashboard_stats()

    def records(self):

        return self.db.get_all_records()

    def search(self, plate_number):

        return self.db.search_vehicle(
            plate_number.upper()
        )