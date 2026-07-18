from src.database import DatabaseManager


class ParkingManager:

    def __init__(self):
        self.db = DatabaseManager()

    def process_vehicle(self, plate_number, image_path=""):

        plate_number = plate_number.strip().upper()

        if plate_number == "":
            return False, "Invalid vehicle number."

        # Vehicle already inside?
        if self.db.vehicle_exists(plate_number):

            success = self.db.vehicle_exit(plate_number)

            if success:
                return True, f"{plate_number} exited successfully."

            return False, f"Unable to exit {plate_number}."

        # Otherwise create a new entry
        success = self.db.add_vehicle(
            plate_number,
            image_path
        )

        if success:
            return True, f"{plate_number} entered successfully."

        return False, "Database error."

    # -------------------------
    # Manual Entry
    # -------------------------

    def vehicle_entry(self, plate_number, image_path=""):

        plate_number = plate_number.strip().upper()

        if plate_number == "":
            return False, "Please enter vehicle number."

        success = self.db.add_vehicle(
            plate_number,
            image_path
        )

        if success:
            return True, f"{plate_number} entered successfully."

        return False, f"{plate_number} is already inside."

    # -------------------------
    # Manual Exit
    # -------------------------

    def vehicle_exit(self, plate_number):

        plate_number = plate_number.strip().upper()

        if plate_number == "":
            return False, "Please enter vehicle number."

        success = self.db.vehicle_exit(plate_number)

        if success:
            return True, f"{plate_number} exited successfully."

        return False, "Vehicle not found."

    # -------------------------
    # Dashboard
    # -------------------------

    def dashboard(self):
        return self.db.get_dashboard_stats()

    # -------------------------
    # Records
    # -------------------------

    def records(self):
        return self.db.get_all_records()

    # -------------------------
    # Search
    # -------------------------

    def search(self, plate_number):
        return self.db.search_vehicle(
            plate_number.upper()
        )