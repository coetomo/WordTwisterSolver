import inspect
from itertools import permutations

from hidden import roll

MAX_BRUTE_LEN = 8


def anagram_brute(letters):
    """
    Returns a list of all possible strings using different orderings of letters
    """
    print("calling brute")
    max_len = min(len(letters)+1, MAX_BRUTE_LEN)
    return ["".join(ordering) for r in range(3, max_len) for ordering in permutations(letters, r)]


def anagram_cheat(_letters):
    """
    Get the actual answers through Javascript and return those answers as a list
    """
    # Hacky way to get the driver object from the previous stack frame; Do not try this at home! :)
    frame = inspect.currentframe()
    while frame:
        if 'driver' in frame.f_locals:
            driver = frame.f_locals['driver']
            break
        frame = frame.f_back
    puzzle_config = driver.execute_script("return __puzzle__")
    dic_puzzle = eval(puzzle_config)
    return [dic['word'] for dic in dic_puzzle['_words']]


AVAILABLE_FUNCS = [anagram_brute, anagram_cheat]


def ask_anagram_strategy(driver, lst_strategy=AVAILABLE_FUNCS):
    if not lst_strategy:
        raise ValueError("List of anagram strategies is empty")

    print("\nAvailable anagram strategies: ")
    for i, strat in enumerate(lst_strategy):
        print(f"{i}: {strat.__name__}")
    while True:
        ans = input(f"Choose strategy [0-{i}]: ")
        if ans == 'r':
            roll(driver)
            input()
        if ans.isdigit() and 0 <= int(ans) < len(lst_strategy):
            return lst_strategy[int(ans)]
        print("Invalid index! ", end='')
