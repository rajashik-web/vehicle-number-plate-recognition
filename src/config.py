"""
Application configuration.
"""
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = "models/license_plate/best.pt"

DATABASE_URL = os.getenv("DATABASE_URL")
OUTPUT_FOLDER = "data/output"

SUPPORTED_IMAGE_TYPES = [
    "jpg",
    "jpeg",
    "png",
]

APP_TITLE = "Vehicle Number Plate Recognition"

CONFIDENCE_THRESHOLD = 0.50

MAX_MISSING_FRAMES = 15

SHOW_CONFIDENCE = True

SHOW_BOUNDING_BOX = True