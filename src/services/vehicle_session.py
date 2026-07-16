class VehicleSession:

    def __init__(self):

        self.active = False

        self.frames = 0

        self.plates = []

    def start(self):

        self.active = True
        self.frames = 0
        self.plates.clear()

    def add_plate(self, text, image):

        if text != "":

            self.plates.append(
                {
                    "text": text,
                    "image": image
                }
            )

        self.frames += 1

    def finish(self):

        self.active = False

        return self.plates

    def reset(self):

        self.active = False
        self.frames = 0
        self.plates.clear()