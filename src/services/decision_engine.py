class DecisionEngine:

    def should_accept(
        self,
        plate,
        confidence
    ):

        if plate == "":
            return False

        if confidence < 0.80:
            return False

        return True