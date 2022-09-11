
# SELENIUM:
import Utils.MyWebdriver as wd

# UTILS:
import warnings
import numpy as np
import pandas as pd
import Utils.config as c
from BBC.get_data_bbc import get_data_bbc
warnings.simplefilter(action='ignore', category=FutureWarning)
from tabulate import tabulate



class BBC_Scraping:

    def __init__(self):

        self.driver = wd.MyWebdriver.initialize_driver(c.BBC_Path)
        self.articles = get_data_bbc(self.driver)
        self.df = self.articles.df


    def search_in_articles(self, search_text):
        """
        the function go over all the content of the articles
        then print the name and link of all articles that contain attlist half of the words in search
        @param self: string that contain words
        @return:
        """
        text_lower = search_text.lower()
        text_list = list(text_lower.split(" "))
        listofLinksTo_return=[]
        for word in text_list:

            mask = np.column_stack(
                [self.df[col].astype(str).str.contains(word, case=False, na=False) for col in self.df])

            listofLinksTo_return.append({
                'link':self.df.loc[mask.any(axis=1)].page_url,
                'word':word
            })
        pdTable=pd.DataFrame(listofLinksTo_return)

        table = tabulate(pdTable)

        print(table)
        return table


    def to_csv_file_and_print(self):
        """
              save the csv and print the table
              @param self
              @return:
              """
        # saving the dataframe
        self.df = self.df[
            self.df.columns.drop(list(self.df.filter(regex='Unnamed')))]
        self.df.reset_index(drop=True, inplace=True)
        prettyprint = tabulate(self.df)
        print(prettyprint)
        self.df.to_csv(c.csv_file)









if __name__ == "__main__":
    ans = BBC_Scraping()

    ans.to_csv_file_and_print()

    l = ans.search_in_articles('King Charles III has praised the Queen')
    print(l)
    ans.driver.quit()
