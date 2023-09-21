from manage_portal.support_desk import SupportDeskOperations
from manage_portal.tickets import TicketOperations
from resmap.navigation import ResmapNav
from general_tools.interpretation import Interpretation
from general_tools.general_info import GeneralInfo
from selenium.webdriver.common.by import By


class Operations:
    def __init__(self, browser):
        self.browser = browser
        self.support_desk_master = SupportDeskMaster(browser)
        self.ticket_master = TicketMaster(browser)
        self.resmap_nav_master = ResmapNavMaster(browser)
        self.interpretation_master = InterpretationMaster()
        self.general_info = GeneralInfo()

    def main_loop(self):
        url = self.browser.driver.current_url
        idx = 0
        # while True:
        number_of_tickets = self.support_desk_master.support_desk_retrieve_rows_length()
        # if idx >= number_of_tickets:
        #     break
        link = self.support_desk_master.support_desk_retrieve_url(13)
        self.browser.click_element(link)
        ticket_info = self.ticket_master.scrape_ticket()
        title, description, property, unit, resident = ticket_info
        ticket_title_and_description = title + description
        if unit is not None and resident is not None:
            operation = self.interpretation_master.determine_operation(
                ticket_title_and_description
            )
            if operation:
                ticket_info = self.interpretation_master.retrieve_ticket_info(
                    operation, ticket_title_and_description
                )
                self.browser.launch_operation(self.browser.resmap_url)
                self.resmap_nav_master.open_ticket(property, unit)
                self.perform_operation(operation, ticket_info)
        self.browser.driver.get(url)
        # idx += 1

    def perform_operation(self, operation, ticket_info):
        if operation == "add_monthly_taxes":
            self.add_monthly_taxes(*ticket_info)

    def add_monthly_taxes(self, amount, month):
        self.resmap_nav_master.nav_to_resident_fees()
        select = self.browser.define_select()
        select.select_by_visible_text("Taxes" or "Rent Tax")
        amount_element = self.browser.find_element(By.NAME, "amount")
        begin_date_element = self.browser.find_element(By.NAME, "begindate")
        end_date_element = self.browser.find_element(By.NAME, "enddate")
        self.browser.send_keys_to_element(amount_element, amount)
        self.browser.send_keys_to_element(
            begin_date_element, f"{month}/01/{self.general_info.year}"
        )
        self.browser.send_keys_to_element(
            end_date_element, f"{month - 1}/30/{self.general_info.year + 1}"
        )


class InterpretationMaster(Interpretation):
    def __init__(self):
        super().__init__()
        self.general_info = GeneralInfo()

    def retrieve_ticket_info(self, operation, text):
        if operation == "add_monthly_taxes":
            amount = self.extract_dollar_amount(text)
            month = (
                self.extract_month(text)
                if not None
                else self.general_info.months_array[
                    self.general_info.month if self.general_info.month <= 11 else 0
                ]
            )
            month_number = self.general_info.months[month]
            print(amount, month)
            if amount is None or month is None:
                return None
            return [amount, month_number]


class ResmapNavMaster(ResmapNav):
    def __init__(self, browser):
        super().__init__(browser)

    def open_ticket(self, property, unit):
        self.nav_to_unit(property, unit)


class SupportDeskMaster(SupportDeskOperations):
    def __init__(self, browser):
        super().__init__(browser)


class TicketMaster(TicketOperations):
    def __init__(self, browser):
        super().__init__(browser)
