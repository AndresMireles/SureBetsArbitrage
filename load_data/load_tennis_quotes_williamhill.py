from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

browser = webdriver.Chrome(
    ChromeDriverManager().install(), options=options)
browser.get(
    "https://sports.williamhill.es/betting/es-es/tenis/partidos/competici%C3%B3n/hoy")
time.sleep(0.5)


def tennis_data_williamhill():

    SCROLL_PAUSE_TIME = 0.8

    try:
        # Get the scroll height
        last_height = browser.execute_script(
            "return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait for the page to load
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate the new scroll height and compare with the last scroll height
            new_height = browser.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        matches = browser.find_elements_by_class_name("event")

        matches_dict = {}
        for match_elem in matches:
            match = BeautifulSoup(
                match_elem.get_attribute('innerHTML'), 'html.parser')

            teams = match.find('div', attrs={
                'class': "btmarket__link-name btmarket__link-name--ellipsis show-for-desktop-medium"
            }).text.replace("                        ", "").replace(" v ", " - ").replace("                   ", "").replace("\n ", "").replace("\n", "")

            odds = match.find_all(
                'div', attrs={'class': 'btmarket__selection'})

            odds = [odd.text[:-1].replace("\n", "") for odd in odds]

            matches_dict[teams.replace("\n", "").replace("/", " / ")] = odds
    except:
        print("William Hill has failed")

    browser.quit()

    return matches_dict
