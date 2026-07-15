from src.corrector import PlateCorrector

corrector = PlateCorrector()

tests = [

    "DL7CN561I",
    "MH20EJO364",
    "KA01AB12S4",
    "TN21BZO768"

]

for plate in tests:

    print()

    print("OCR      :", plate)

    print("Corrected:", corrector.correct(plate))