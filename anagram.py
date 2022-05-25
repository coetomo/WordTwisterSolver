import inspect
from itertools import permutations


def anagram_brute(letters):
    """
    Returns a list of all possible orderings of letters
    """
    max_len = max(len(letters)+1, 8)
    return [ordering for r in range(3, max_len) for ordering in permutations(letters, r)]


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


def ask_anagram_strategy(lst_strategy=AVAILABLE_FUNCS):
    print("Available anagram strategies: ")
    for i, strat in enumerate(lst_strategy):
        print(i, strat.__name__)
    while True:
        ans = input("Choose strategy: ")
        if ans.idigit() and 0 <= ans < len(lst_strategy):
            return lst_strategy[ans]
        print("Invalid index! ", end='')