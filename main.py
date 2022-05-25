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

from anagram import anagram_cheat, ask_anagram_strategy

URL_TWISTER_GAME = 'https://zone.msn.com/gameplayer/gameplayerHTML.aspx?game=mswordtwister'
EASY = 0
NORMAL = 1
HARD = 2
INIT_PLAY_BUTTON_XPATH = "/html/body/app-root/div/div[1]/app-layout/div/app-map/div/div[2]/div[2]/app-map-quick-play-view/div[2]/button"
TIMEOUT_TIMER = 30
ADS_TIMER = 120


def close_tab(driver, n):
    driver.switch_to.window(driver.window_handles[n])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def init_driver(url):
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--mute-audio")

    # Installs AdBlock extension
    options.add_extension('./adblock.crx')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Close AdBlock tab in second tab
    time.sleep(.75)
    close_tab(driver, 1)

    return driver


def auto_setup(driver=None, url=URL_TWISTER_GAME, difficulty=EASY):
    if driver is None:
        driver = init_driver(url)
    # Click Play button in the main menu
    WebDriverWait(driver, TIMEOUT_TIMER).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "game-player-iframe")))
    WebDriverWait(driver, ADS_TIMER).until(
        EC.element_to_be_clickable((By.ID, "btnPlayAgain"))).click()

    # Wait for Ads
    print("Waiting for ads...")
    WebDriverWait(driver, TIMEOUT_TIMER).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "gameFrame")))

    # Click the skip button
    print("Skipping tutorials for babies...")
    WebDriverWait(driver, ADS_TIMER).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".skip-button.ui-button.red.en-US"))).click()

    print("Disabling tutorials through in game menu...")
    WebDriverWait(driver, TIMEOUT_TIMER).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.labeled-button.menu-button"))).click()
    WebDriverWait(driver, TIMEOUT_TIMER).until(
        EC.element_to_be_clickable((By.ID, "btnGameOptions"))).click()
    time.sleep(1)
    WebDriverWait(driver, TIMEOUT_TIMER).until(
        EC.presence_of_element_located((By.ID, "show-wordTwister-tutorial"))).click()
    time.sleep(.5)
    WebDriverWait(driver, TIMEOUT_TIMER).until(
        EC.presence_of_element_located((By.ID, "hints"))).click()
    time.sleep(.5)
    WebDriverWait(driver, TIMEOUT_TIMER).until(
        EC.presence_of_element_located((By.ID, "quick-tips"))).click()
    time.sleep(.5)
    WebDriverWait(driver, TIMEOUT_TIMER).until(
        EC.element_to_be_clickable((By.ID, "btnClose"))).click()

    time.sleep(.5)
    # Click the Play under Quick play section
    WebDriverWait(driver, TIMEOUT_TIMER).until(
        EC.element_to_be_clickable((By.XPATH, INIT_PLAY_BUTTON_XPATH))).click()

    if difficulty == EASY:
        print("Playing on 'Easy' difficulty (n00b)...")
        # Click Easy button (can be changed dependant on the difficulty)
        WebDriverWait(driver, TIMEOUT_TIMER).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-button.green"))).click()
    elif difficulty == NORMAL:
        print("Playing on 'Normal' difficulty (normies)...")
        # Click Easy button (can be changed dependant on the difficulty)
        WebDriverWait(driver, TIMEOUT_TIMER).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-button.yellow"))).click()
    elif difficulty == HARD:
        print("Playing on 'Hard' difficulty (nice)...")
        # Click Easy button (can be changed dependant on the difficulty)
        WebDriverWait(driver, TIMEOUT_TIMER).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-button.red"))).click()
    else:
        raise ValueError("Difficulty does not exist!")


def skip_tutorials(driver: webdriver.Chrome):
    elems = driver.find_elements(by=By.CSS_SELECTOR, value=".skip-button.ui-button.red.en-US")
    if not elems:
        return
    elems[0].click()


def solve_puzzle(driver=None, url=INIT_PLAY_BUTTON_XPATH):
    if driver is None:
        driver = init_driver(url)
    continue_puzzle = True
    while continue_puzzle:
        # Setup for solving puzzle
        anagram_strategy = ask_anagram_strategy(driver)
        print(f"\nUsing '{anagram_strategy.__name__}'...")
        input("Ready? Press Enter to continue!")
        puzzle_config = driver.execute_script("return __puzzle__")
        dic_puzzle = eval(puzzle_config)
        letters = dic_puzzle["_letters"]

        retry_solve = True
        while retry_solve:
            action = ActionChains(driver)
            for guess in anagram_strategy(letters):
                print("Testing:", guess);
                action.send_keys(guess + Keys.ENTER).perform()
                time.sleep(1)
                action.reset_actions()
                # skip_tutorials(driver)

            repeat_question = 1
            while repeat_question:
                ans = input("Done! Solve more puzzle? [y/n/r] ").lower()
                # Continue and wait until next puzzle has been manually loaded
                if ans == 'y':
                    retry_solve = False
                # Finish up the program
                elif ans == 'n':
                    continue_puzzle = False
                # Restart the solving algorithm
                elif ans == 'r':
                    pass
                else:
                    print("Invalid answer! ", end='')
                    repeat_question += 1
                repeat_question -= 1


def main():
    driver = init_driver(URL_TWISTER_GAME)
    auto_setup(driver=driver, difficulty=NORMAL)
    solve_puzzle(driver)
    print("Exiting and closing...")
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()


# try:
#     # Press next game
#     WebDriverWait(driver, 8).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-button.gold"))).click()
#     retry = False
# except TimeoutException as e:
#     # The solving process was interrupted mid-execution, will need to retry
#     print("Puzzle not finished! Retrying!")
#     time.sleep(.75)
# except ElementClickInterceptedException as e:
#     # If intercepted for whatever reason, try click again (should only happen once)
#     print("Click intercepted! Retrying to click again!")
#     time.sleep(2)
#     driver.find_element(by=By.CSS_SELECTOR, value=".ui-button.gold").click()
