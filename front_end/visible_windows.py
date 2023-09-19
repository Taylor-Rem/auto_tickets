from front_end.helper_windows import HelperWidget


class TicketWindow(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Run Auto Ticket")
        self.create_button("Run Auto Ticket", self.run_auto_ticket)

    def run_auto_ticket(self):
        self.operations.main_loop()
