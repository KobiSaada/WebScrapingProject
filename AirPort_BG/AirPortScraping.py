# SELENIUM:
import Utils.MyWebdriver as wd


# UTILS:
import pandas as pd
import numpy as np
from tabulate import tabulate
from AirPort_BG.get_data_Flights import get_data_Flights
import Utils.config as c
import json


class AirPortScraping:
    def __init__(self):
        self.df_a, self.df_d = self.get2df()
        self.driver = wd.MyWebdriver.initialize_driver(c.AirPort_Path)
        self.flights = get_data_Flights(self.driver, self.df_a, self.df_d)
        self.departure_flight = self.flight.list_depat_flight
        self.arrival_flight = self.flights.list_ariv_flight

    def get2df(self):
        """
          get 2 data frames for arrival flight and departure flight
           @param self
           @return:
                    """
        try:
            df_a = pd.read_csv("airPort_Ariv_BG.csv")
            df_d = pd.read_csv("airPort_Depat_BG.csv")
        except:
            df_a = pd.DataFrame()
            df_d = pd.DataFrame()
        return df_a, df_d

    def to_csv_file(self):
        """
         save the csv and print the table
           @param self
            @return:
              """
        self.flights.df_a = self.flights.df_a[
            self.flights.df_a.columns.drop(list(self.flights.df_a.filter(regex='Unnamed')))]
        self.flights.df_a.reset_index(drop=True, inplace=True)
        self.flights.df_d = self.flights.df_d[
            self.flights.df_d.columns.drop(list(self.flights.df_d.filter(regex='Unnamed')))]
        self.flights.df_d.reset_index(drop=True, inplace=True)
        # saving the dataframe
        prettyprint = tabulate(self.flights.df_a, headers='keys', tablefmt='psql')
        print(prettyprint)
        csv_a = 'airPort_Ariv_BG.csv'
        csv_d = "airPort_Depat_BG.csv"
        self.flights.df_a.to_csv(csv_a)
        self.flights.df_d.to_csv(csv_d)

    def create_arriv_json(self):
        """
        create a json from flight type arrival
        then save the json
        @return:
        """

        json_object = json.dumps(self.arrival_flight, indent=2)
        dir_path = c.AirPort_ariv_Path_dir
        num = 0
        name_file = 'arrival' + str(num)
        self.__file_create(dir_path, name_file, json_object)
        num = num + 1

    def create_depart_json(self):
        """
        create a json from flight type departure
        then save the json
        @return:
        """

        json_object = json.dumps(self.departure_flight, indent=2)
        dir_path = c.AirPort_dept_Path_dir
        num = 0
        name_file = 'departure' + str(num)
        self.__file_create(dir_path, name_file, json_object)
        num = num + 1

    def __file_create(self, dir_path, s, json_object):
        """
        save json
        @param dir_path: the path to the wright directory
        @param flight_num: flight number
        @param json_object: the json object of the current flight
        @return:
        """
        # Writing to sample.json
        file_name = s + ".json"
        file_full_path = dir_path + file_name
        with open(file_full_path, "w") as outfile:
            outfile.write(json_object)

    def search_in_arriv_flight(self, search_text):
        """
        the function go over all the content of the arrival flight
        then print the flight  that contain at list half of the words in search
        @param self: string that contain words
        @return:
        """
        text_lower = search_text.lower()
        text_list = list(text_lower.split(" "))
        listofResTo_return=[]
        for word in text_list:

            mask = np.column_stack(
                [self.df_a[col].astype(str).str.contains(word, case=False, na=False) for col in self.df_a])
            listofResTo_return.append((self.df_a.loc[mask.any(axis=1)], word))


        pdTable=pd.DataFrame(listofResTo_return)

        table = tabulate(pdTable)

        print(table)
        return table


    def search_in_arriv_flight(self, search_text):
        """
        the function go over all the content of the departure flight
        then print the flight  that contain at list half of the words in search
        @param self: string that contain words
        @return:
        """
        text_lower = search_text.lower()
        text_list = list(text_lower.split(" "))
        listofResTo_return=[]
        for word in text_list:
            mask = np.column_stack(
                [self.df_d[col].astype(str).str.contains(word, case=False, na=False) for col in self.df_d])
            listofResTo_return.append((self.df_d.loc[mask.any(axis=1)], word))

        pdTable = pd.DataFrame(listofResTo_return)

        table = tabulate(pdTable)

        print(table)
        return table




