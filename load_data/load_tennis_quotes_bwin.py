from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

browser = webdriver.Chrome(
    ChromeDriverManager().install(), options=options)
browser.get("https://sports.bwin.es/es/sports/tenis-5/apuestas")


def tennis_data_bwin():

    matches_dict = {}

    time.sleep(0.5)

    try:
        main = BeautifulSoup(browser.find_element_by_class_name(
            'event-list').get_attribute('innerHTML'), 'html.parser')

        live_matches = main.find_all(
            'div', attrs={'class': 'grid-event-wrapper'})

        for match in live_matches:

            teams = match.find_all(
                'div', attrs={'class': 'participant-wrapper'})

            # .strip(" ") is used to remove the trailing space left at the end
            team1 = teams[0].text.strip(
                " ")[:-3] if (teams[0].text[0]) == " " else teams[0].text[-3:-1]
            team2 = teams[1].text.strip(
                " ")[:-3] if (teams[1].text[0]) == " " else teams[1].text[-3:-1]

            processed_teams = team1.replace(
                "/", " / ") + ' - ' + team2.replace("/", " / ")

            odds = match.find_all(
                'ms-option', attrs={'class': 'grid-option'})[0:2]

            odds = [odd.text for odd in odds]
            for odd in odds:
                if odd == "":
                    odds[odds.index(odd)] = "0"

            if odds and len(odds) == 2:
                matches_dict[processed_teams.replace("Reserves", "")] = odds
    except:
        print("Bwin has failed")

    browser.quit()

    return matches_dict

    # for [key, value] in matches_dict.items():
    #     print(key+': '+f'{value}')
