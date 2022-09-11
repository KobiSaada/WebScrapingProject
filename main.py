from BBC.BBC_Scraping import BBC_Scraping
from AirPort_BG.AirPortScraping import AirPortScraping

def run():
    a=AirPortScraping()
    b=BBC_Scraping()
    b.to_csv_file_and_print()
    b.search_in_articles("boas")
    b.driver.close()


if __name__ == '__main__':
    run()



