import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])


browser = webdriver.Chrome(
    ChromeDriverManager().install(), options=options)
browser.get("https://betway.es/es/sports/cpn/tennis/231")
time.sleep(3)


def tennis_data_betway():

    try:
        # This is necessary to properly click on the button when changing match type:
        html = browser.find_element_by_tag_name('html')
        html.send_keys(Keys.ARROW_DOWN)
        html.send_keys(Keys.ARROW_DOWN)
        html.send_keys(Keys.ARROW_DOWN)
        html.send_keys(Keys.ARROW_DOWN)

        # ATP:

        elements = browser.find_elements_by_class_name('oneLineEventItem')

        matches_dict = {}
        for element in elements:
            teams = element.find_elements_by_class_name('teamName')
            team1 = teams[0].text[:-1].replace("● ", "")
            team2 = teams[1].text.replace(" ●", "")

            odds = element.find_element_by_class_name(
                "eventMarket").text.split("\n")

            if odds != ["Cancelled"]:
                matches_dict[team1 + '- '+team2] = odds

        # WTA:

        buttons = browser.find_elements_by_class_name(
            "contentSelectorItemButton")
        buttons[-2].click()

        time.sleep(1)

        elements = browser.find_elements_by_class_name('oneLineEventItem')

        for element in elements:
            teams = element.find_elements_by_class_name('teamName')
            team1 = teams[0].text[:-1].replace("● ", "")
            team2 = teams[1].text.replace(" ●", "")

            odds = element.find_element_by_class_name(
                "eventMarket").text.split("\n")

            if odds != ["Cancelled"]:
                matches_dict[team1 + '- '+team2] = odds

        # Challenger:
        buttons = browser.find_elements_by_class_name(
            "contentSelectorItemButton")
        buttons[-1].click()
        time.sleep(1)

        elements = browser.find_elements_by_class_name('oneLineEventItem')

        for element in elements:
            teams = element.find_elements_by_class_name('teamName')
            team1 = teams[0].text[:-1].replace("● ", "")
            team2 = teams[1].text.replace(" ●", "")

            odds = element.find_element_by_class_name(
                "eventMarket").text.split("\n")

            if odds != ["Cancelled"] and '-' not in odds:
                matches_dict[team1 + '- '+team2] = odds

    except:
        print("Betway has failed")

    browser.quit()

    return matches_dict
