import psycopg2
from datetime import datetime

from src.config import DATABASE_URL
from src.parking_service import ParkingService


class DatabaseManager:

    def __init__(self):
        self.create_table()

    def connect(self):
        return psycopg2.connect(DATABASE_URL)

    def create_table(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_records (

            id SERIAL PRIMARY KEY,

            plate_number VARCHAR(20),

            entry_time TIMESTAMP,

            exit_time TIMESTAMP,

            status VARCHAR(20),

            parking_fee DECIMAL(10,2),

            image_path TEXT

        );
        """)

        conn.commit()

        cursor.close()
        conn.close()
            
    def vehicle_exists(self, plate_number):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM parking_records
            WHERE plate_number = %s
            AND status = 'INSIDE'
            """,
            (plate_number,)
        )

        exists = cursor.fetchone() is not None

        cursor.close()
        conn.close()

        return exists
        
    def add_vehicle(self, plate_number, image_path):

        if self.vehicle_exists(plate_number):
            print(f"{plate_number} is already inside.")
            return False

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO parking_records
            (
                plate_number,
                entry_time,
                status,
                parking_fee,
                image_path
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                plate_number,
                datetime.now(),
                "INSIDE",
                0,
                image_path
            )
        )   # <-- This closing bracket was missing

        conn.commit()

        cursor.close()
        conn.close()

        print(f"{plate_number} entered successfully.")

        return True
    
    def get_all_records(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                plate_number,
                entry_time,
                exit_time,
                status,
                parking_fee
            FROM parking_records
            ORDER BY entry_time DESC
        """)

        records = cursor.fetchall()

        cursor.close()
        conn.close()

        return records
    
        
    def vehicle_exit(self, plate_number):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, entry_time
            FROM parking_records
            WHERE plate_number = %s
            AND status = 'INSIDE'
            ORDER BY entry_time DESC
            LIMIT 1
            """,
            (plate_number,)
        )

        record = cursor.fetchone()

        if record is None:

            cursor.close()
            conn.close()

            print("Vehicle not found.")

            return False

        record_id = record[0]
        entry_time = record[1]

        exit_time = datetime.now()

        duration = exit_time - entry_time

        hours = duration.total_seconds() / 3600
        
        parking_service = ParkingService()

        fee = parking_service.calculate_fee(hours)

        cursor.execute(
            """
            UPDATE parking_records
            SET
                exit_time = %s,
                status = 'EXITED',
                parking_fee = %s
            WHERE id = %s
            """,
            (
                exit_time,
                fee,
                record_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        print(f"Vehicle exited successfully.")
        print(f"Parking Duration : {duration}")
        print(f"Parking Fee : ₹{fee}")

        return True
    
    
    def get_dashboard_stats(self):

        conn = self.connect()
        cursor = conn.cursor()

        # Vehicles currently inside
        cursor.execute("""
            SELECT COUNT(*)
            FROM parking_records
            WHERE status='INSIDE'
        """)
        vehicles_inside = cursor.fetchone()[0]

        # Total vehicles
        cursor.execute("""
            SELECT COUNT(*)
            FROM parking_records
        """)
        total_vehicles = cursor.fetchone()[0]

        # Total revenue
        cursor.execute("""
            SELECT COALESCE(SUM(parking_fee), 0)
            FROM parking_records
        """)
        total_revenue = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return {
            "inside": vehicles_inside,
            "total": total_vehicles,
            "revenue": total_revenue
        }
        
        
    def search_vehicle(self, plate_number):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                plate_number,
                entry_time,
                exit_time,
                status,
                parking_fee
            FROM parking_records
            WHERE plate_number = %s
            ORDER BY entry_time DESC
            LIMIT 1
            """,
            (plate_number,)
        )

        record = cursor.fetchone()

        cursor.close()
        conn.close()

        return record