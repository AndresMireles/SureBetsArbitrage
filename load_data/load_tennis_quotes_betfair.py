from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])


def tennis_data_betfair():

    browser = webdriver.Chrome(
        ChromeDriverManager().install(), options=options)
    browser.get("https://www.betfair.es/sport/tennis")

    time.sleep(1)

    # We handle the cookies button:
    try:
        cookies = browser.find_element_by_id("onetrust-accept-btn-handler")
        cookies.click()
    except:
        pass

    matches_dict = {}
    try:
        live = browser.find_element_by_class_name("section-list")

        # Get the entire list of matches:
        matches = BeautifulSoup(
            live.get_attribute('innerHTML'), 'html.parser')

        # Each match:
        matches_bak = matches.find_all(
            'div', attrs={'class':
                          lambda e: e.startswith('event-information ui') if e else False}
        )

        for match in matches_bak:
            # The team names (we use anonymous lambda functions to grab classes that start with a string since there are cases where unique IDs are added to each class, and we want to capture, for example, all classes that start with event-name):
            teams = match.find_all('span', attrs={'class': 'team-name'})

            teams = teams[0].text.replace(
                "\n", "").replace("• ", "") + ' - ' + teams[1].text.replace("\n", "").replace("• ", "")

            # The odds:
            odds = []
            for ultag in match.find_all('ul', {'class': 'runner-list-selections'}):
                for litag in ultag.find_all('li'):
                    if litag.text != '\n':
                        odds.append(litag.text.replace("\n", ""))

            matches_dict[teams] = odds
    except:
        print("Betfair has failed")

    browser.quit()
    return matches_dict
