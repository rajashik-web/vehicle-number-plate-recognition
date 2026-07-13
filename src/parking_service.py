class ParkingService:

    RATE_PER_HOUR = 20

    def calculate_fee(self, hours):

        return round(hours * self.RATE_PER_HOUR, 2)