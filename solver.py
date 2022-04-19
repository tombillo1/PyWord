import numpy as np
import pandas as pd
import string, sys
import csv
import requests
import webbrowser
import PySimpleGUI as sg

#max length of the words and format
MAX_LENGTH = 5
#list of invalid words to be used in helper
invalid_letters = []

def wordle_helper(guess, word):

    #takes words from URL and spits to get the sorted data
    url = "https://www.nytimes.com/games/wordle/main.bfba912f.js"

    response = requests.get(url)
    data = response.text.split("Ma=")[1].split(",Ra=")[0]
    sorted_data = data.split('"')[1::2]

    #writes to a .csv file
    f = csv.writer(open('data.csv', 'w', newline='')) # Create a file to write
    f.writerow(['Possible Words'])

    #Takes user input:
    #
    # Con: Guess and format must have a length of 5
    #
    guess_list = list(guess)

    #Adds on to list of invalid characters as well as the list of correct values
    #
    #Con: Must use the format "GYR"
    #
    i = -1
    check_val = []
    filler_wrong = '&'
    filler_correct = '!'

    for char in word:
        i += 1
        if  char == "G" or char == "Y" or char == "R":
            if char == "G":
                check_val.append(guess_list[i])
            elif char == "Y":
                check_val.append(filler_correct)
            elif char == "R":
                check_val.append(filler_wrong)
                invalid_letters.append(guess[i])
            else:
                check_val.append(char.lower)
        else:
            sys.exit("Invalid format!")
    
    print("Check val: ", check_val)
    print("invalid_letters: ", invalid_letters)
        
    #adds the words to the data set
    for words in sorted_data:
        c = 0
        flag = False
        check_words = list(words)
        #filters out words that dont have the right letters in the position
        for i in check_val:
            #checks for already correct words
            if i.isalpha() and check_val[c] != check_words[c]:
               flag = True
            #checks for 'almost' correct words
            if i == '!' and (check_words[c] == guess_list[c] or guess_list[c] not in check_words):
                flag = True
            c += 1
                    
        #checks to see if there are any invalid letters in the word
        res = any(ele in words for ele in invalid_letters)
        if res:
            continue
        if flag == False:
            f.writerow([words])

#main method
if __name__ == "__main__":
    #goes until input to stop
    flag = True
    while(flag == True):
        #color
        sg.theme('TanBlue')
        #Window content
        layout = [  
            [sg.Text('Welcome to WordPy! Please enter the information down below.')],
            [sg.Text('Enter your guess: '), sg.InputText()],
            [sg.Text('Enter the format of your guess: \n Enter values in form XXXXX, \n R should represent a grey square \n Y should represent a yellow square \n G should represent a green square'), sg.InputText()],
            [sg.Button('Save'), sg.Button('Cancel'), sg.Button('Continue')] 
            ]

        # Create the Window
        window = sg.Window('WordPy', layout)
        #Events if buttons are pressed
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': #closes if window shuts or cancel is pressed
                flag = False
                break
            elif event == 'Save':
                guess = values[0]
                word = values[1]
                if len(guess) != 5 or len(word) != 5:
                    flag = False
                    sys.exit("Invalid!")
            if event == 'Continue':
                flag = True
                break

        
        window.close()

        wordle_helper(guess, word)

        fileh = pd.read_csv('data.csv')
        fileh.to_html('Table.html')
        webbrowser.open('Table.html')
