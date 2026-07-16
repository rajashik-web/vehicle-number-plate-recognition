from src.services.anpr_state import ANPRState
from src.services.vehicle_session import VehicleSession
from src.services.ocr_voter import OCRVoter


class ANPRController:

    def __init__(self):

        self.state = ANPRState.WAITING

        self.session = VehicleSession()

        self.voter = OCRVoter()

    def start(self):

        self.state = ANPRState.COLLECTING

        self.session.start()

        self.voter.clear()

    def add_plate(self, text, image):

        self.session.add_plate(
            text,
            image
        )

        self.voter.add(text)

    def finish(self):

        self.state = ANPRState.PROCESSING

        best_text = self.voter.best_result()

        best_image = None

        for plate in self.session.plates:

            if plate["text"] == best_text:

                best_image = plate["image"]

                break

        self.reset()

        return best_text, best_image

    def reset(self):

        self.state = ANPRState.WAITING

        self.session.reset()

        self.voter.clear()