import requests, collections


def main():
    print("in main")
    level = game_start()
    board = get_board(level)

    guesses = []
    game_continue = True
    while game_continue and len(guesses)<10:
        display_previous_guesses(guesses)
        guess = input("Please enter your guess (ex: 0123): ")
        while not validate_guess(guess, board):
            guess = input("Please enter your guess (ex: 0123): ")
        new_guess = check_input(guess, board)
        guesses.append(new_guess)
        game_continue = new_guess["continue"]
    
    if game_continue: #ran out of guesses, didnt guess correctly
        ans = 0
        for num in board:
            ans = ans*10 + num 
        print(f"The number was {ans}. Better luck next time!")
    game_end()

def game_start():
    print("Welcome to Mastermind!")
    level = input("Please choose a level: easy, medium, hard: ").lower().strip()
    while level not in {"easy", "medium", "hard"}:
        level = input ("Please enter a valid level: easy, medium, hard: ").lower().strip()

    game_instructions(level)
    return level

def game_instructions(level):
    level_length = {
        "easy": 4, 
        "medium": 6,
        "hard": 8}
    print("You will have 10 tries to guess the correct number combinations. Each number will be between 0 and 7. \n")
    print(f"The selected level difficulty is {level} and the number of digits is {level_length[level]}. \n")
    print("At the end of each guess, you will receive feedback on whether you have successfully guessed the number and/or its location.\n")

def display_previous_guesses(guesses):
    if guesses:
        print("\n")
        print("*"*40)
        print("Previous guesses:")
    for idx, guess in enumerate(guesses):
        print(f'Guess {idx+1}: {guess["board"]} | Correct Numbers: {guess["corr_num"]} | Correct Location: {guess["corr_loc"]}')
    print("*"*40)
    print("\n")
    print(f"You have {10 - len(guesses)} guesses left.")    

def validate_guess(guess, board):
    if len(guess) != len(board):
        print(f"Please enter a valid guess, {len(board)} digits are required.")
        return False
    elif not guess.isnumeric():
        print(f"Please enter a valid guess. {guess} is not a valid number combination.")
        return False
    for num in guess:
        # print(num)
        if int(num) not in range(0,8):
            print(f"Please enter a valid guess. All digits should be between 0 and 7.")
            return False
    return True

def game_end():
    print("Game over! Thanks for playing!")
    # print("Would you like to play again? (y/n)")

def get_board(level):
    difficulty = {
        "easy": 4, 
        "medium": 6,
        "hard": 8}
    
    board_size = difficulty[level]    
    path = f"https://www.random.org/integers/?num={board_size}&min=0&max=7&col=1&base=10&format=plain&rnd=new"

    response = requests.get(path)
    # print(response) #returns the response code 
    response_body = response.text
    # print(response_body)
    board= [int(num) for num in response_body.split("\n") if num != ""]
    # print([num for num in response_body.split("\n")])
    return board

# print(get_board("easy"))
# print(get_board("medium"))
# print(get_board("hard"))

def check_input(guess, board):
    board_count = collections.defaultdict(int)
    for num in board:
        board_count[num] += 1
    # print(board_count)

    corr_loc = 0
    corr_num = 0

    guess_list = [int(num) for num in guess]
    if guess_list == board:
        print("You win!")
        return {"board":guess, "corr_num": len(guess_list), "corr_loc":len(guess_list), "continue":False}
    for i, num in enumerate(guess_list):
        if num in board_count:
            board_count[num] -= 1
            if board_count[num] >= 0:
                corr_num += 1
            if num == board[i]:#num has to be in the board to be at the correct location
                corr_loc += 1
    
    if not corr_loc and not corr_num:
        print("all incorrect")
    elif corr_loc or corr_num:
        print(f"{corr_num} correct number{'s' if corr_num > 1 else ''} and {corr_loc} correct location{'s' if corr_loc > 1 else ''}")
    
    return {"board":guess, "corr_num": corr_num, "corr_loc":corr_loc, "continue":True}

if __name__ == "__main__":
    main()