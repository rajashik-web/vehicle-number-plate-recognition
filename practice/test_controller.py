from src.services.anpr_controller import ANPRController

controller = ANPRController()

controller.start()

controller.add_plate("MH20EJ0364")
controller.add_plate("MH20EJ0364")
controller.add_plate("MH20EJO364")
controller.add_plate("MH20EJ0364")

print(controller.finish())