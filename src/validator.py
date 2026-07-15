import re


class PlateValidator:

    def __init__(self):

        self.pattern = re.compile(
            r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$"
        )

    def is_valid(self, plate):

        if plate is None:
            return False

        return self.pattern.match(plate) is not None