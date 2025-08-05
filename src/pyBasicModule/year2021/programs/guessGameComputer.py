import random

low =1; high = 1000; next=''
while next != 'C':
    print('range {} - {}'.format(low, high))
    guess = random.randint(low, high)
    next = input(f'My guess is {guess}. Suggest next hint : H/h (high), L/l (low) or C/c (correct)').upper()
    if next == 'H':
        low = guess
    elif next == 'L':
        high = guess

print(f'your number was {guess}')

print('#' * 10, 'Lets play other way!!' , '#' * 10)

low =1; high = 1000;
computer_guess = random.randint(low, high)
next= int(input("Enter your guess"))

while next != computer_guess:
     if next > computer_guess:
         next = int(input("Guess Low"))
     elif next < computer_guess:
         next = int(input("Guess High"))

print('Yay, you guessed it {}'.format(next))
print(computer_guess)
