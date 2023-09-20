from manage_portal.support_desk import SupportDeskOperations
from manage_portal.tickets import TicketOperations


class SupportDeskMaster(SupportDeskOperations):
    def __init__(self, browser):
        super().__init__(browser)


class TicketMaster(TicketOperations):
    def __init__(self, browser):
        super().__init__(browser)


class Operations:
    def __init__(self, browser):
        self.browser = browser
        self.support_desk_master = SupportDeskMaster(browser)
        self.ticket_master = TicketMaster(browser)

    def main_loop(self):
        url = self.browser.driver.current_url
        number_of_tickets = self.support_desk_master.support_desk_retrieve_rows_length()
        print(number_of_tickets)
        for i in range(number_of_tickets):
            link = self.support_desk_master.support_desk_retrieve_url(i)
            self.browser.click_element(link)
            ticket_info = self.ticket_master.scrape_ticket()
            title, description, property, unit, resident = ticket_info
            print(f"{title} |---| {unit}, {resident}")
            self.browser.driver.get(url)
