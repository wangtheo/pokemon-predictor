from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv

def winner(d):
    wait = WebDriverWait(d, timeout)
    playButton = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Play (music off)')]")))
    playButton.click()
    goTo = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), ' Go to turn...')]")))
    goTo.click()
    alert = d.switch_to_alert()
    alert.send_keys('10000')
    alert.accept()
    try: 
        battleHistory = d.find_elements_by_css_selector("div.battle-history")
        winner = battleHistory[-1].find_element_by_tag_name("strong").text
        player = d.find_element_by_css_selector("a.subtle").text
        if player == winner: 
            return 1
        else: 
            return 0
    except (NoSuchElementException, TimeoutException) as exception:
        return 1

def teams(d):
    wait = WebDriverWait(d, timeout)
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div.battle-history")))
    t = d.find_elements_by_css_selector("div.battle-history")
    playerTeam = t[0].find_element_by_tag_name("em").text
    oppTeam = t[1].find_element_by_tag_name("em").text
    return (playerTeam, oppTeam)

opts = Options()
driver = webdriver.Chrome(options=opts)
driver.get('https://replay.pokemonshowdown.com')
timeout = 10
wait = WebDriverWait(driver, timeout)
genInput = wait.until(ec.visibility_of_element_located((By.NAME, "format")))
genInput.send_keys("gen7ou")
genSearch = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Search by format')]")))
genSearch.click()

gamesList = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "ul + ul.linklist")))
_wait = WebDriverWait(gamesList, timeout)
_wait.until(ec.visibility_of_element_located((By.TAG_NAME, "li")))
games = gamesList.find_elements_by_tag_name("li")

while len(games) < 1000: 
    more = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'More')]")))
    more.click()
    gamesList = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "ul + ul.linklist")))
    _wait = WebDriverWait(gamesList, timeout)
    _wait.until(ec.visibility_of_element_located((By.TAG_NAME, "li")))
    games = gamesList.find_elements_by_tag_name("li")

gameURLS = list(map(lambda x: x.find_element_by_tag_name("a").get_attribute('href'), games))


with open('train.csv', mode='w') as replays:
    replay_writer = csv.writer(replays, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for game in gameURLS:
        driver.get(game)
        victor = str(winner(driver))
        playerTeam, oppTeam = teams(driver)
        replay_writer.writerow([victor, playerTeam + " | " + oppTeam])


