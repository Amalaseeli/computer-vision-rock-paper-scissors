
import random

#Get computer choice
def get_computer_choice():
    guess={}
    with open('labels.txt') as f:
        for content in f:
            key,value=content.split()
            guess[key]=value

        print(guess)
        f.close()
    #list=['rock','paper','scissors']
    computer_choice=random.choice(list(guess.values())).lower()
    return computer_choice

#get user choice
def get_user_choice():
    user_choice=input("Enter your coice:")
    return user_choice

def play():
    computer_choice=get_computer_choice()
    user_choice=get_user_choice()
    print(computer_choice)
    if (computer_choice=="rock" and user_choice=="scissors") or (computer_choice=="paper" and user_choice=="rock") or (computer_choice=="scissors" and user_choice=="paper"):
        print("Computer wins") 
    elif (computer_choice=="rock" and user_choice=="paper") or (computer_choice=="paper" and user_choice=="scissors") or (computer_choice=="scissors" and user_choice=="rock"):
        print("User wins") 
    else:
        print("Draw game")

play()   