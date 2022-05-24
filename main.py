from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def anagram_brute(word):
    letters = tuple(word)



if __name__ == '__main__':

    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--mute-audio")
    options.add_extension('./adblock.crx')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get('https://zone.msn.com/gameplayer/gameplayerHTML.aspx?game=mswordtwister')

    # Click Play button in the main menu
    driver.switch_to.frame("game-player-iframe")
    driver.find_element(by=By.ID, value="btnPlayAgain").click()

    # Wait for Ads
    input("Waiting for ads... Press Enter after the video ad finished playing!")

    driver.switch_to.frame("gameFrame")

    # Click the skip button
    driver.find_element(by=By.CSS_SELECTOR, value=".skip-button.ui-button.red.en-US").click()
    time.sleep(1.5)

    # Click the Play under Quick play section
    driver.find_element(by=By.XPATH,
                        value="/html/body/app-root/div/div[1]/app-layout/div/app-map/div/div[2]/div[2]/app-map-quick-play-view/div[2]/button").click()
    time.sleep(1.5)

    # Click Easy button (can be changed dependant on the difficulty)
    driver.find_element(by=By.CSS_SELECTOR, value=".ui-button.green").click()
    # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "btnPlayAgain")))

    input("Ready? Press Enter to continue!")
    puzzle_config = driver.execute_script("return __puzzle__")
    dic_puzzle = eval(puzzle_config)
    for guess in dic_puzzle['_words']:
        ActionChains(driver).send_keys(guess['word'] + Keys.ENTER).perform()
        time.sleep(.5)
    # Press next game
    driver.find_element(by=By.CSS_SELECTOR, value=".ui-button.gold").click()

    input("Done!")

    driver.close()
    driver.quit()
