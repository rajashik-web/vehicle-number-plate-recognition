import re


class PlatePostProcessor:

    def clean(self, text):

        if text is None:
            return ""

        text = text.upper()

        # Remove spaces
        text = text.replace(" ", "")

        # Remove hyphen
        text = text.replace("-", "")

        # Remove brackets
        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("(", "")
        text = text.replace(")", "")

        # Keep only letters and numbers
        text = re.sub(
            r"[^A-Z0-9]",
            "",
            text
        )

        return text