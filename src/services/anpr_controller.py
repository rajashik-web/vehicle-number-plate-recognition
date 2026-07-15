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

    def add_plate(self, text):

        self.session.add_plate(text)

        self.voter.add(text)

    def finish(self):

        self.state = ANPRState.PROCESSING

        result = self.voter.best_result()

        self.reset()

        return result

    def reset(self):

        self.state = ANPRState.WAITING

        self.session.reset()

        self.voter.clear()