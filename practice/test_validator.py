from src.validator import PlateValidator

validator = PlateValidator()

plates = [

    "MH20EJ0364",
    "DL7CN5617",
    "KA01AB1234",
    "0269LKL",
    "DL7CN561I",
    "ABC123"

]

for plate in plates:

    print(
        plate,
        "->",
        validator.is_valid(plate)
    )