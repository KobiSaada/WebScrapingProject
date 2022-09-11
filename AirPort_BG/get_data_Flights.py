# SELENIUM:
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
# UTILS:
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


class get_data_Flights:
    def __init__(self, driver, df_ariv, df_depat):
        self.df_a = df_ariv
        self.list_ariv_flight = self.get_flights_Ariv_list(driver, 0)
        self.df_d = df_depat
        self.list_depat_flight = self.get_flights_depart_list(driver, 0)

    def get_Full_Arival_table(self, driver):
        """
        the function click the next button until the full table of arrival flights is shown
        then click the cancel automatic update,
        its imported that we can extract the information without that the web elements will change.
        then save all the flight information in to json files
        @return:
        """
        driver.implicitly_wait(10)
        button_next = driver.find_element(By.CSS_SELECTOR, 'button[id="next"]')
        style_state = button_next.get_attribute("style")
        while style_state == '':
            driver.implicitly_wait(5)
            button_next.click()
            button_next = driver.find_element(By.CSS_SELECTOR, 'button[id="next"]')
            style_state = button_next.get_attribute("style")
        # cancel automatic update
        button_update = driver.find_element(By.CSS_SELECTOR, 'a[id="toggleAutoUpdate"][role="button"]')
        button_update.click()

    def get_Full_departures_table(self, driver):
        """
         first the function click a button to go to the departure flights table,
         then it clicks the next button until the full table of departure flights is shown
         then save all the flight information in to json files
         @return:
         """
        # button to go to departure table
        button_deap = driver.find_element(By.CSS_SELECTOR, 'a[id="tab--departures_flights-label"]')
        button_deap.click()
        # wait until the next button is available

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="next"][type="button"]')))
        button_next = driver.find_element(By.CSS_SELECTOR, 'button[id="next"][type="button"]')
        style_state = button_next.get_attribute("style")
        while style_state == "":
            driver.implicitly_wait(5)
            button_next.click()
            button_next = driver.find_element(By.CSS_SELECTOR, 'button[id="next"]')
            style_state = button_next.get_attribute("style")

    def get_flights_depart_list(self, driver, row):
        """
         get all flights_depart
         @return:
         """
        while True:

            self.get_Full_departures_table(driver)

            try:

                driver.implicitly_wait(10)
                ContentTab = driver.find_element(By.CLASS_NAME, "tabs-content")
                driver.implicitly_wait(5)
                BodyTab = ContentTab.find_elements(By.TAG_NAME, "tbody")
                driver.implicitly_wait(10)
                # self.driver.execute_cdp_cmd('Emulation.setScriptExecutionDisabled', {'value': True})

                RowTab = BodyTab[1].find_elements(By.CLASS_NAME, "flight_row")
                Flights = []
                driver.implicitly_wait(5)
                LenRowTab = len(RowTab)

                while row < LenRowTab:
                    Flights_dict = {}
                    airline = RowTab[row].find_element(By.CLASS_NAME, "td-airline")
                    airline_text = airline.get_attribute("innerHTML")
                    Flights_dict['חברת תעופה'] = airline_text

                    driver.implicitly_wait(10)

                    flight = RowTab[row].find_element(By.CLASS_NAME, "td-flight")
                    flight_text = flight.get_attribute("innerHTML")
                    Flights_dict['טיסה'] = flight_text

                    driver.implicitly_wait(10)

                    from_city = RowTab[row].find_element(By.CLASS_NAME, "td-city")
                    city_text = from_city.get_attribute("innerHTML")
                    Flights_dict['נוחת-מ-'] = city_text

                    terminal = RowTab[row].find_element(By.CLASS_NAME, "td-terminal")
                    terminal_text = terminal.get_attribute("innerHTML")
                    Flights_dict['טרמינל'] = terminal_text

                    driver.implicitly_wait(10)

                    scheduled_time = RowTab[row].find_element(By.CLASS_NAME, "td-scheduledTime")
                    scheduled_time_date = scheduled_time.find_element(By.TAG_NAME, "strong").get_attribute("innerHTML")
                    scheduled_time_time = scheduled_time.find_element(By.TAG_NAME, "div").get_attribute("innerHTML")
                    scheduled_time_text = f"{scheduled_time_date} {scheduled_time_time}"
                    Flights_dict['זמן-מתוכנן'] = scheduled_time_text

                    driver.implicitly_wait(10)

                    updated_time = RowTab[row].find_element(By.CLASS_NAME, "td-updatedTime")
                    updated_time_text = updated_time.find_element(By.TAG_NAME, "time").get_attribute("innerHTML")
                    Flights_dict['זמן-עדכני'] = updated_time_text

                    driver.implicitly_wait(10)

                    counter = RowTab[row].find_element(By.CLASS_NAME, "td-counter")
                    counter_text = counter.get_attribute("innerHTML")
                    Flights_dict['דלפק'] = counter_text

                    driver.implicitly_wait(10)

                    check_in = RowTab[row].find_element(By.CLASS_NAME, "row-checkIn")
                    check_in_text = check_in.get_attribute("href")
                    Flights_dict['צ׳ק-אין'] = check_in_text

                    driver.implicitly_wait(10)

                    status = RowTab[row].find_element(By.CLASS_NAME, "row-status")
                    status_text = status.find_element(By.TAG_NAME, "div").get_attribute("innerHTML")
                    Flights_dict['סטאטוס'] = status_text

                    driver.implicitly_wait(10)

                    Flights.append(Flights_dict)
                    self.df_d = pd.concat([self.df_d, pd.DataFrame.from_records([Flights_dict])], axis=0,
                                          ignore_index=True)
                    # self.df_d = pd.concat(Flights_dict, ignore_index=True)
                    # self.df_d = self.df_d.append(Flights_dict, ignore_index=True)
                    row = row + 1

                return Flights

            except:
                row1 = row
                self.get_flights_depart_list(driver, row1)

    def get_flights_Ariv_list(self, driver, row):
        """
               get all flights_Ariv_list
               @return:
               """

        while True:
            self.get_Full_Arival_table(driver)
            try:

                driver.implicitly_wait(10)
                ContentTab = driver.find_element(By.CLASS_NAME, "tabs-content")
                driver.implicitly_wait(5)
                BodyTab = ContentTab.find_elements(By.TAG_NAME, "tbody")
                driver.implicitly_wait(10)
                # self.driver.execute_cdp_cmd('Emulation.setScriptExecutionDisabled', {'value': True})

                RowTab = BodyTab[0].find_elements(By.CLASS_NAME, "flight_row")
                Flights = []
                driver.implicitly_wait(5)
                LenRowTab = len(RowTab)

                while row < LenRowTab:
                    Flights_dict = {}
                    airline = RowTab[row].find_element(By.CLASS_NAME, "td-airline")
                    airline_text = airline.get_attribute("innerHTML")
                    Flights_dict['חברת תעופה'] = airline_text

                    driver.implicitly_wait(10)

                    flight = RowTab[row].find_element(By.CLASS_NAME, "td-flight")
                    flight_text = flight.get_attribute("innerHTML")
                    Flights_dict['טיסה'] = flight_text

                    driver.implicitly_wait(10)

                    from_city = RowTab[row].find_element(By.CLASS_NAME, "td-city")
                    city_text = from_city.get_attribute("innerHTML")
                    Flights_dict['נוחת-מ-'] = city_text

                    terminal = RowTab[row].find_element(By.CLASS_NAME, "td-terminal")
                    terminal_text = terminal.get_attribute("innerHTML")
                    Flights_dict['טרמינל'] = terminal_text

                    driver.implicitly_wait(10)

                    scheduled_time = RowTab[row].find_element(By.CLASS_NAME, "td-scheduledTime")
                    scheduled_time_date = scheduled_time.find_element(By.TAG_NAME, "strong").get_attribute("innerHTML")
                    scheduled_time_time = scheduled_time.find_element(By.TAG_NAME, "div").get_attribute("innerHTML")
                    scheduled_time_text = f"{scheduled_time_date} {scheduled_time_time}"
                    Flights_dict['זמן-מתוכנן'] = scheduled_time_text

                    driver.implicitly_wait(10)

                    updated_time = RowTab[row].find_element(By.CLASS_NAME, "td-updatedTime")
                    updated_time_text = updated_time.find_element(By.TAG_NAME, "time").get_attribute("innerHTML")
                    Flights_dict['זמן-עדכני'] = updated_time_text

                    driver.implicitly_wait(10)

                    status = RowTab[row].find_element(By.CLASS_NAME, "row-status")
                    status_text = status.find_element(By.TAG_NAME, "div").get_attribute("innerHTML")
                    Flights_dict['סטאטוס'] = status_text

                    driver.implicitly_wait(10)

                    Flights.append(Flights_dict)
                    self.df_a = pd.concat([self.df_a, pd.DataFrame.from_records([Flights_dict])], axis=0,
                                          ignore_index=True)
                    # self.df_d = pd.concat(Flights_dict, ignore_index=True)
                    # self.df_a = self.df_a.append(Flights_dict, ignore_index=True)
                    row = row + 1

                return Flights

            except:
                row1 = row
                self.get_flights_Ariv_list(driver, row1)
