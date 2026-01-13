# Leah Kalantarov
# Semester Project final draft 
# Falling Words


import Draw
import random
import time

#returns list of words to be used in the game 	
def getWords():
	words = []
	fin = open("1000words.txt")
	
	#read each line from the text file
	#remove extra lines and make everything lowercase 
	for line in fin:
		w=line.strip().lower() 
		
		#keep only words that are 3-8 letters long and no punctuation
		if len(w)>=3 and len(w)<=8 and w.isalpha():
			words.append(w)
					
	fin.close()
	
	#shuffle the words so they come in a different order each time
	random.shuffle(words)
	return words


#moves all on screen words down by a fixed amount
def moveDown(onScreen):
	fallAmount = 3
	#each on screen item looks like [word,x,y]
	for i in onScreen:
		i[2] = i[2] + fallAmount
		
#removes any words that have reached the ground
#returns list of words that have not hit the ground 
def checkHitGround(onScreen):
	ans = [ ] 
	ground = 490
	wordHeight = 30
	
	#keep the word if the bottom is still above the ground
	for i in onScreen:
		if i[2] < ground - wordHeight:	
			ans.append(i)
			
	return ans 
	
#checks if current guess matches a word on screen, and if yes removes it
#returns a new list containing the words that do not match guess 
def checkTypedWord(onScreen,guess):
	ans = [ ]
	for i in onScreen:
		if guess != i[0]:
			ans.append(i)
	return ans


def drawBoard(onScreen, guess, lives, score):
	
	#clear the board and draw the background
	Draw.clear()
	Draw.picture("skyimage.gif",0,0)
	
	ground = 490
	
	
	#draw the lives, score, and guess 
	Draw.setColor(Draw.WHITE)
	Draw.setFontFamily("Arial Rounded MT Bold")
	Draw.setFontSize(20)
	Draw.setFontBold(True)
	
	
	Draw.string("Lives: " + str(lives), 730, 540)
	Draw.string("Score: " + str(score), 730, 570)
	
	Draw.setFontSize(35)
	Draw.string("Guess: " + guess, 50, 530)
	
	
	#draw every falling word 
	for w in onScreen:
		word = w[0]
		x = w[1]
		y = w[2]
		
		#draw a black outline so that words dont blend with clouds
		Draw.setColor(Draw.BLACK)
		Draw.string(word, x+2, y+2)
		
		#if the word is close to the ground make it red
		if y> ground - 50:
			#draw the string in red
			Draw.setColor(Draw.RED)
			Draw.string(word, x, y)
			
		#if the word starts with guess draw the word in white
		#and draw the matching part in green on top 
		elif word.startswith(guess) and guess!="":
			#add outline around words for better visibility 
			
			Draw.setColor(Draw.WHITE)
			Draw.string(word, x, y)	
			
			#draw the string with the matching chars in green
			Draw.setColor(Draw.GREEN)
			Draw.string(guess, x, y)
					
		
		#otherwise just draw the entire word yellow 
		else:
			#draw the string in yellow
			Draw.setColor(Draw.YELLOW)
			Draw.string(word, x, y)
	
	Draw.show(25)
	
	
#game is over so ask if the user wants to play again
def playAgain(score):
	#clear the screen and show a game over screen
	Draw.clear()
	Draw.picture("skyimage.gif",0,0)
	
	Draw.setFontFamily("Arial Rounded MT Bold")
	Draw.setFontBold(True)
	Draw.setFontSize(60)
	
	#outline effect on "Game Over" to make it stand out 
	Draw.setColor(Draw.WHITE)
	Draw.string("GAME OVER", 233, 103)
	Draw.setColor(Draw.RED)
	Draw.string("GAME OVER", 230, 100)	
	
	#show the final score and instructions to restart game 
	Draw.setFontSize(30)
	
	scoreFinalText= "Final Score: " + str(score)
	questionText= "Play again? (y/n)"
	
	#outline final score and question as well
	Draw.setColor(Draw.BLACK)
	Draw.string(scoreFinalText, 302, 202)
	Draw.string(questionText, 282, 252)
		
	
	Draw.setColor(Draw.WHITE)
	Draw.string(scoreFinalText, 300, 200)
	
	Draw.setColor(Draw.GREEN)
	Draw.string(questionText, 280, 250)
	
	Draw.show()
	
	
	# Keep looping until the user decides if they want to play again
	# (types a "y" or "n")
	while True:
		if Draw.hasNextKeyTyped():
			newKey = Draw.nextKeyTyped().lower() 
			if newKey == "y":
				return True
			elif newKey == "n":
				return False

#runs entire game and returns final score when game is over 
def playGame(words):
	
	#game difficulty controls 
	timeGap = 1.5
	shrinkGapTime = 20	
	
	guess = ""
	lives = 5
	score = 0
	
	#each item is [word, x, y]
	onScreen = []
	
	#timers to check if enough time has passed to update 
	lastWordTime = time.time()-timeGap
	lastGapShrinkTime = time.time()
	tick = 0	
	
	#while the game’s not over (lives is not zero)
	while lives !=0 :
		
		#increase the time of how long the game has been running 
		tick+=1
		
		#take keyboard input
		if Draw.hasNextKeyTyped():
			
			#get the key and make it lowercase so caps wont matter
			newKey = Draw.nextKeyTyped().lower()
			
			
			#backspace deletes a letter if one is available
			if newKey=="backspace":
				if len(guess)>0:
					#slice off the rightmost character of the guess
					guess=guess[:-1]
				
			
			#if the key is a letter build the guess string
			#only accepts letters 
			elif len(newKey)==1 and newKey.isalpha():
				#append it to guess
				guess+=newKey
				
				
		#spawn a new word every timeGap seconds 
		if time.time()-lastWordTime>timeGap:
			
			#if there are words left
			if len(words)>0:
				newWord = random.choice(words)
				words.remove(newWord)
				
				#random x so words fall in different places 
				x = random.randint(0,700)
				
				#start slightly above screen 
				#word looks like its falling in			
				onScreen.append([newWord, x , -10])
				
				
				#reset time so we wait timeGap seconds again 
				lastWordTime=time.time()					
		#every shrinkGapTime seconds speedup game to increase difficulty
		if time.time()-lastGapShrinkTime>shrinkGapTime:
			#smaller timeGap makes more words spawn
			timeGap=.99*timeGap
			lastGapShrinkTime=time.time()
			
			#not so fast that its unplayable  
			if timeGap<0.5:
				timeGap=0.5			
	
	
		#every few ticks words fall, update the lives, score, and redraw 
		if tick%10==0:
			
			#make all words fall a little
			moveDown(onScreen)
		
		
			#remove words that hit the ground
			#lose a life if any did 
			wordsCount= len(onScreen)
			onScreen=checkHitGround(onScreen)
			if len(onScreen)<wordsCount:
				lives-=1
						
			#remove a word if it matches guess
			#increase score if any did and reset guess
			if guess !="":
				wordsCount=len(onScreen)
				onScreen=checkTypedWord(onScreen,guess)
				if len(onScreen)<wordsCount:		
					score+=1
					drawBoard(onScreen, guess, lives, score)	
					guess=""
			
			#redraw updated board after these updates
			drawBoard(onScreen, guess, lives, score)
			
	#send final score to main so it can be shown on game over screen 		
	return score 
		
		
def main(): 
	#create the canvas 
	Draw.setCanvasSize(850,600)
 
	#get the words list from the file shuffled 
	words=getWords()
	score= playGame(words)
	
	while playAgain(score) == True:
		words=getWords()
		score= playGame(words)	
main()
