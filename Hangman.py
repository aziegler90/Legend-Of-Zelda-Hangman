
# A Legend of Zelda themed hangman game
#
# Date: 8/10/2022
# Purpose: This is a proof of concept for me to learn and understand Python 3
#
# Author: Amber Ziegler
# Legend of Zelda API Credit: https://docs.zelda-api.apius.cc/docs/


import os
import random
import requests


# *** Global Variables ***
# The word to be guessed
wordInPlay = ""
# The subject the word belongs to
subjectInPlay = ""
# Track the letters that are guessed
letterTracking = []
# Keeps track of how many wrong guesses have been made
wrongGuessCount = 0
# Nested array that displays the entire image and letters
hangmanArray = [["       ", "_", "_", "_", "_", "_"],
                ["      |"," "," "," "," "," ","|"],
                ["      |"," "," "," "," "," ","|"," "," "," "," "," "," "," "],
                ["      |"],
                ["      |"],
                ["      |"],
                ["      |"],
                ["      |"," "," "," "," "," "," "," "," "," "," "," "," "," "],
                ["      |"],
                ["      |"],
                ["      |","_","_","_","_","_","_","_","_"]]


# This function displays welcome message
def welcomeMessage():
    os.system('cls')
    print("             Let's play hangman!\n       *** Legend of Zelda Edition ***")
    displayTheMan()
    print()
    input("          Press ENTER to continue\n\n")


# This function displays the current hangman image
def displayTheMan():
    for x in range(len(hangmanArray)):
        for y in hangmanArray[x]:
            print(y, end = "")
        print()


# This function establishes the games subject and the word to be guessed
def getSubjectAndWord():
    global wordInPlay
    global subjectInPlay
    subjectNumber = random.randrange(1,8)

    # Determine the subject based on a number from 1 - 8
    match subjectNumber:
        case 1:
            subject = "games"
            totalPages = 1
        case 2:
            subject = "characters"
            totalPages = 33
        case 3:
            subject = "monsters"
            totalPages = 16
        case 4:
            subject = "bosses"
            totalPages = 5
        case 5:
            subject = "dungeons"
            totalPages = 7
        case 6:
            subject = "places"
            totalPages = 29
        case 7:
            subject = "items"
            totalPages = 37

    # Add subject to global variable
    subjectInPlay = subject

    try:
        # Select random number between 1 and the total number of pages for that subject
        randomPageNum = random.randrange(1, totalPages + 1)
        requestURL = "https://zelda.fanapis.com/api/" + subject +  "?limit=50&page=" + str(randomPageNum)
        # Call API to return the data set for that subject and page number
        wordsArray = requests.get(requestURL)
        # Word is determined by a random index number within that data set
        randomIndex = random.randrange(0, wordsArray.json()['count'])
        # Add word to global variable
        wordInPlay = wordsArray.json()['data'][randomIndex]['name']

        # Add a line for each letter in the word
        for letter in wordInPlay:
            if letter == " ":
                hangmanArray[7].append(" ")
            else:
                hangmanArray[7].append("_")
    except ValueError as err:
        # Redo the function if an error occurs due to a random number occurrence that points to a null value
        getSubjectAndWord()


# This function displays the end game content
def endGame(winOrLose):
    global wordInPlay
    wordInPlay = wordInPlay.upper()
    # Clear the wrong letters section
    del hangmanArray[2][14:]

    # Player won
    if winOrLose == True:
        hangmanArray[2].append("*** YOU WIN! ***")
    # Player lost 
    else:
        # Display losing statement
        hangmanArray[2].append("YOU LOSE!")
        # Reveal the word
        del hangmanArray[7][15:]        
        hangmanArray[7][14] = wordInPlay


# This function checks if the entire word has been guessed
def checkForCompleteness():
    wordLength = len(wordInPlay)
    isComplete = False
    for x in range(14, wordLength + 14):
        if hangmanArray[7][x].isalpha() or hangmanArray[7][x] == " ":
            isComplete = True
        else:
            isComplete = False
            break

    if isComplete == True:
        endGame(True)
    
    return isComplete


# This keeps track of wrong guesses and drawing the hangman
def wrongGuess(wrongLetter):
    # Increment number of wrong guesses
    global wrongGuessCount
    wrongGuessCount += 1
    
    if len(hangmanArray[2]) == 14:
        # Add the wrong letters line
        hangmanArray[2].append("Wrong Letters: " + wrongLetter + " ")
    else:
        # Add letters to the wrong letters line
        hangmanArray[2].append(wrongLetter + " ")

    # Add to hangman
    match wrongGuessCount:
        case 1:
            # Add the head
            hangmanArray[2][4] = "_"
            hangmanArray[2][5] = "_"
            hangmanArray[2][7] = "_"
            for x in range(2):
                hangmanArray[3].append(" ")
                hangmanArray[4].append(" ")
            hangmanArray[3].append("/")
            hangmanArray[4].append("\\")
            for x in range(4):
                hangmanArray[3].append(" ")
                hangmanArray[4].append("_")
            hangmanArray[3].append("\\")
            hangmanArray[4].append("/")
        case 2:
            # Add body
            for x in range(4):
                hangmanArray[5].append(" ")
                hangmanArray[6].append(" ")
            hangmanArray[5].append("|")
            hangmanArray[6].append("|")
            hangmanArray[7][5] = "|"
        case 3:
            # Add left arm
            hangmanArray[6][4] = "/"
        case 4:
            # Add right arm
            hangmanArray[6].append("\\")
        case 5:
            # Add left leg
            for x in range(3):
                hangmanArray[8].append(" ")
            hangmanArray[8].append("/")
        case 6:
            # Add right leg
            hangmanArray[8].append(" ")
            hangmanArray[8].append("\\")
        case 7:
            # Add left foot
            hangmanArray[8][3] = ("_")
        case 8:
            # Add right foot
            hangmanArray[8].append("_")
        case 9:
            # Add left eye
            hangmanArray[3][4] = "X"
        case 10:
            # Add right eye
            hangmanArray[3][7] = "X"
        case 11:
            # Add mouth and game ending content
            hangmanArray[4][5] = "ᗣ"
            endGame(False)


# This function analyzes the players guess against the main word
def takeTurn(playerGuess, wordInPlay):
    global letterTracking
    guessResult = ""
    playerGuess = playerGuess.upper()
    wordInPlay = wordInPlay.upper()

    # Test to make sure the guess is one letter
    if len(playerGuess) == 1 and playerGuess.isalpha():
        # Test if the letter was already guessed
        if (playerGuess in letterTracking):
            guessResult = ""
        else:
            # Test if the guess is correct
            if (playerGuess in wordInPlay):
                # Keep track of how many times the correct letter occurs in the word
                letterOccurrences = [x for x in range(len(wordInPlay)) if wordInPlay.startswith(playerGuess, x)]
                # Fill the blank with the correct letter
                for eachNum in letterOccurrences:
                    hangmanArray[7][eachNum + 14] = playerGuess

                # Check to see if the full word has been guessed
                isComplete = checkForCompleteness()
                if (isComplete == True):
                    guessResult = "Winner!"
                else:
                    guessResult = playerGuess + " is correct!"
            else:
                wrongGuess(playerGuess)
                guessResult = playerGuess + " is incorrect."
            
            # Add letter to list of already guessed letters
            letterTracking.append(playerGuess)
    else:
        guessResult = "Invalid choice! Please enter one letter at a time."

    return guessResult


# This function facilitates the main gameplay
def playTheGame():
    gameplay = True
    # Feedback from the players turn
    turnResult = ""
    # Ensure the game gets both the subject and the word
    while (wordInPlay == "" or subjectInPlay == ""):
        getSubjectAndWord()
    
    # Main gameplay
    while (gameplay == True):
        os.system('cls')
        print()
        print("             Subject: " + subjectInPlay + "\n\n      Guess a letter...")
        displayTheMan()
        print("\n      " + turnResult)
        print()
        # Get player input
        playerGuess = input("      ...or press 0 to exit.\n\n")

        # Game ends if player presses 0
        if (playerGuess == '0'):
            gameplay = False
        # Player loses and game ends if there are too many incorrect guesses
        elif (wrongGuessCount == 11):
            endGame(False)
            gameplay = False
        # The player won the game
        elif (turnResult == "Winner!"):
                gameplay = False
        # The player made a guess attempt
        else:
            turnResult = takeTurn(playerGuess, wordInPlay)


# Display welcome message before gameplay
welcomeMessage()
playTheGame()