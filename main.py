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
ADS_TIMER = 200


def close_tab(driver, n):
    """
    Closes tab after installing adblock
    :param driver: WebDriver from Selenium
    :param n: the n-th tab
    :return: None
    """
    driver.switch_to.window(driver.window_handles[n])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def init_driver(url):
    """
    Initialize WebDriver settings. Must have ChromeDriver Manager installed
    :param url: Target URL for WebDriver
    :return: the initialized WebDriver object
    """
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
    """
    Automatically opens up the browser, sets up the Word Twister game online by skipping tutorial and change in-game
    options for an undisturbed experience for the WebDriver
    :param driver: WebDriver object
    :param url: target URL
    :param difficulty: the desired difficulty of the game
    :return: None
    """
    if driver is None:
        driver = init_driver(url)
    wait = WebDriverWait(driver, TIMEOUT_TIMER)
    ads_wait = WebDriverWait(driver, ADS_TIMER)

    # Click Play button in the main menu
    wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "game-player-iframe")))
    ads_wait.until(
        EC.element_to_be_clickable((By.ID, "btnPlayAgain"))).click()

    # Wait for Ads
    print("Waiting for ads...")
    wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "gameFrame")))

    # Click the skip button
    print("Skipping tutorials for babies...")
    ads_wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".ftue-button.ui-button.red.en-US"))).click()

    print("Disabling tutorials through in game menu...")
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button"))).click()
    wait.until(
        EC.element_to_be_clickable((By.ID, "btnGameOptions"))).click()
    time.sleep(1)
    driver.execute_script("arguments[0].click();",wait.until(
        EC.presence_of_element_located((By.ID, "show-wordTwister-tutorial"))))
    time.sleep(.5)
    driver.execute_script("arguments[0].click();", wait.until(
        EC.presence_of_element_located((By.ID, "hints"))))
    time.sleep(.5)
    driver.execute_script("arguments[0].click();", wait.until(
        EC.presence_of_element_located((By.ID, "quick-tips"))))
    time.sleep(.5)
    wait.until(
        EC.element_to_be_clickable((By.ID, "btnClose"))).click()

    time.sleep(.5)
    # Click the Play under Quick play section
    # WebDriverWait(driver, TIMEOUT_TIMER).until(
    #     EC.element_to_be_clickable((By.XPATH, INIT_PLAY_BUTTON_XPATH))).click()
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.play-button.next-button.ui-button.blue"))).click()

    if difficulty == EASY:
        print("Playing on 'Easy' difficulty (n00b)...")
        # Click Easy button (can be changed dependant on the difficulty)
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.quick-play-button.ui-button.green"))).click()
    elif difficulty == NORMAL:
        print("Playing on 'Normal' difficulty (normies)...")
        # Click Easy button (can be changed dependant on the difficulty)
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.quick-play-button.ui-button.yellow"))).click()
    elif difficulty == HARD:
        print("Playing on 'Hard' difficulty (nice)...")
        # Click Easy button (can be changed dependant on the difficulty)
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#btnHard"))).click()
    else:
        raise ValueError("Difficulty does not exist!")


def skip_tutorials(driver):
    """
    Control the driver to skip the tutorial section of the game
    :param driver:
    :return:
    """
    elems = driver.find_elements(by=By.CSS_SELECTOR, value=".skip-button.ui-button.red.en-US")
    if not elems:
        return
    elems[0].click()


def solve_puzzle(driver=None, url=URL_TWISTER_GAME):
    """
    Attempts to solve the puzzle indefinitely. Assumes that the browser game is opened.
    :param driver: WebDriver object
    :param url: target URL
    :return: None
    """
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
                print("Testing:", guess)
                action.send_keys(guess)
                action.send_keys(Keys.ENTER)
                action.perform()
                time.sleep(.8)
                action.reset_actions()
                # skip_tutorials(driver)

            repeat_question = True
            while repeat_question:
                ans = input("Done! Solve more puzzle? [y/n/r] ").lower()
                # Continue and wait until next puzzle has been manually loaded
                if ans == 'y':
                    continue_puzzle = True
                    retry_solve = False
                    repeat_question = False
                # Finish up the program
                elif ans == 'n':
                    continue_puzzle = False
                    retry_solve = False
                    repeat_question = False
                # Restart the solving algorithm
                elif ans == 'r':
                    continue_puzzle = False
                    retry_solve = True
                    repeat_question = False
                else:
                    print("Invalid answer! ", end='')


def main():
    """
    Main function
    """
    driver = init_driver(URL_TWISTER_GAME)
    # auto_setup(driver=driver, difficulty=NORMAL)
    solve_puzzle(driver)
    print("Exiting and closing...")
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
