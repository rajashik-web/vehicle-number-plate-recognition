import os
import csv
import cv2

from src.ocr import OCRReader

ocr = OCRReader()

correct = 0
total = 0

with open(
    "data/test_plates/labels.csv",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        image_path = os.path.join(
            "data/test_plates/images",
            row["image"]
        )

        image = cv2.imread(image_path)

        result = ocr.read_text(image)

        predicted = result["text"]

        expected = row["plate"]

        print("-" * 60)
        print("Image     :", row["image"])
        print("Expected  :", expected)
        print("Predicted :", predicted)
        print("Confidence:", result["confidence"])

        if predicted == expected:

            correct += 1

        total += 1

print("=" * 60)

accuracy = (correct / total) * 100 if total else 0

print(f"Accuracy : {accuracy:.2f}%")