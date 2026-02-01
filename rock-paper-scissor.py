
# import the libs ie random etc
import random

# generate random r, p, s
emojis = {
    'r': '🪨',
    'p': '📃',
    's': '✂️'
}

choices = ('r', 'p', 's')

wins = 0
losses= 0

# inside while loop, 
while True:
# take user input ie r, p, s
    user_input = input("Let's play rock, paper scissor. (r, p, s): \n").lower().strip()

    # validate user input
    if user_input not in choices:
        print("invalid input")
        continue

    computer_choice = random.choice(choices)

    print(f'You chose {emojis[user_input]}')
    print(f'Computer chose {emojis[computer_choice]}')

# compare user input with coomputer random generated
    if user_input == computer_choice:
        print("Tie!!")
    elif (
            user_input == 'r' and computer_choice == 's') or \
            (user_input == 's' and computer_choice == 'p') \
            or (user_input == 'p' and computer_choice == 'r'):
        print(f'Congrats, You winnn!!')
        wins += 1
    else:
        print(f'Sorry mate, you lost it this time :)')
        losses += 1
    
    shall_continue = input('Do you wanna continues playing? "y/n" ').lower()
    if shall_continue == 'n':
        break
    else:
        continue

print(f'Total Wins: {wins}')
print(f'Total losses: {losses}')

