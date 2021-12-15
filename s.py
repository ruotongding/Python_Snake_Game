#The resolution of the game is 1280x720.
#The oringinal direction control key is <→>, <←>, <↑>, <↓>.
#The boss key is <b>, and if want to return to tha game just press <n>.
#If you want to pause the game, please press <space>, and just press any move button to continue the game
#The cheating code is the button <c>, the speed of the snake will slow down! Check and do not tell anyone else!!
#If you reach the highest speed you will win the game! Try and challenge yourself!
#when you want to leave just press the key <s> and close the window.
#when you want to load the game. enter the game and press the key <l>. Your stats will restore then!


from tkinter import Message, Tk, Canvas, PhotoImage, messagebox
import random


width = 1280
height = 720

def setWindowDimensions(w,h):
    window = Tk()
    window.title("Snake Game")
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (x/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y)) 
    return window

#Place the food function
def placeFood():
    global food, foodX, foodY
    food = canvas.create_image(0,0, image = apple)
    foodX = random.randint(0,width-snakeSize)
    foodY = random.randint(0,height-snakeSize)
    canvas.move(food, foodX, foodY)


#Snake directions functions
def leftKey(event):
    global direction
    direction = "left"

def rightKey(event):
    global direction
    direction = "right"

def upKey(event):
    global direction
    direction = "up"

def downKey(event):
    global direction
    direction = "down"

#function of pause the game
def pauseKey(event):
    global direction
    direction = "pause"

#cheating key
def cheatKey(event):
    global speed
    speed += 25

#The boss key
def bossKey(event):
    global img1
    img1 = canvas.create_image(width/2, height/2, image = bKeyimg)

#return to the game of the bosskey image
def reBosKey(event):
    global img1
    canvas.delete(img1)

#function of save 
def saveKey(event):
    file = open("save.txt", "w")
    file.write(str(score))
    file.write("\n" + str(speed))
    file.write("\n" + str(playername))
    file.write("\n" + str(len(snake)))
    for i in range(len(snake)):
        file.write("\n" + str(canvas.coords(snake[i])))
    
    file.close()

#function of load
def loadKey(event):
    file = open("save.txt")
    info = file.readlines()
    global speed
    speed = int(info[1])
    global score
    score = int(info[0])
    txt = "score "+ str(score)
    canvas.itemconfigure(scoreText, text = txt)
    global playername, playernameText1
    playername = str(info[2]).strip('\n')
    playernameText2 = canvas.create_text(width/2, 30, fill = "white", font="Times 15 italic bold", text = "Playername: " + playername)
    canvas.delete(playernameText1)

    global snake
    lastElement = int(info[3])  
    for i in range(int(info[3])-1):
        lastElementPos = canvas.coords(snake[i])
        snake.append(canvas.create_oval(0,0,snakeSize,snakeSize, fill="#008080")) 
    file.close()

    


#move food
def moveFood():
    global food, foodX, foodY
    canvas.move(food, (foodX*(-1)), foodY*(-1))
    foodX = random.randint(0, width-snakeSize)
    foodY = random.randint(0, height-snakeSize)
    canvas.move(food, foodX, foodY)

#grow the snake
def growSnake():
    lastElement = len(snake) - 1
    lastElementPos = canvas.coords(snake[lastElement])
    snake.append(canvas.create_oval(0,0,snakeSize,snakeSize, fill="#008080"))
    if (direction == "left"):
        canvas.coords(snake[lastElement+1], lastElementPos[0]+snakeSize, lastElementPos[1], lastElementPos[2]+snakeSize, lastElementPos[3])  
    elif (direction == "right"):
        canvas.coords(snake[lastElement+1], lastElementPos[0]-snakeSize, lastElementPos[1], lastElementPos[2]-snakeSize, lastElementPos[3])
    
    elif (direction == "up"):
        canvas.coords(snake[lastElement+1], lastElementPos[0], lastElementPos[1] + snakeSize, lastElementPos[2], lastElementPos[3]+snakeSize)
    
    else:
        canvas.coords(snake[lastElement+1], lastElementPos[0], lastElementPos[1] - snakeSize, lastElementPos[2], lastElementPos[3]-snakeSize)
    
    
    global score
    score += 3
    txt = "score "+ str(score)
    canvas.itemconfigure(scoreText, text = txt)


#check for the collisions function
def overlappingfood(a,b):
    if a[0] < b[0] + 9  and a[2] > b[0] - 9 and a[1] < b[1] + 9  and a[3] > b[1] - 9 :
        return True
    return False

def overlappingbody(a, b):
	if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
		return True
	return False

#write the score board	
def scoreRecord():
    file = open("leadingboard.txt", "a")
    file.write("\n" + playername + ":" + str(score))
    file.close()

#show the top5 leadingboard
def showBoard():
    file = open("leadingboard.txt")
    boarddic = []
    rank1 = []
    for line in file.readlines():
        line = line.strip('\n')
        sco = line.split(":")
        boarddic.append(sco)
    boarddic = dict(boarddic)
    rank1 = sorted(boarddic.items(), key = lambda d: int(d[1]), reverse= True)
    file.close()

    file=open("leadingboard_o.txt", "w")
    for i in range(5):
        btext = str(rank1[i])
        btext = btext.replace("(", "")
        btext = btext.replace("(", "")
        btext = btext.replace(")", "")
        btext = btext.replace("'", "")
        btext = btext.replace(",", ":")
        file.write(str(btext) + "\n")
    file.close()
    file = open("leadingboard_o.txt")
    
    rank = file.read() 
    messagebox.showinfo(title = "leadingboard", message = rank)
    




#Move the snake function
def moveSnake():
    canvas.pack()
    positions = []
    positions.append(canvas.coords(snake[0]))
    #cross the walls
    if positions[0][0]<0:
        canvas.coords(snake[0], width, positions[0][1], width-snakeSize, positions[0][3])
    elif positions[0][2]>width:
        canvas.coords(snake[0], 0-snakeSize, positions[0][1], 0, positions[0][3])
    elif positions[0][3]>height:
        canvas.coords(snake[0], positions[0][0], 0-snakeSize, positions[0][2], 0)
    elif positions[0][1]<0:
        canvas.coords(snake[0], positions[0][0], height, positions[0][2], height-snakeSize)
    #update snake head positions
    positions.clear()
    #append positions of snake head to he data structure
    positions.append(canvas.coords(snake[0]))
    #move the snake head
    if direction == "left":
        canvas.move(snake[0], -snakeSize, 0)
    elif direction == "right":
        canvas.move(snake[0], snakeSize, 0)
    elif direction == "up":
        canvas.move(snake[0], 0, -snakeSize)
    elif direction == "down":
        canvas.move(snake[0], 0, snakeSize)
    elif direction == "pause":
        canvas.move(snake[0],0,0)

    headPos = canvas.coords(snake[0])
    foodPos = canvas.coords(food)
    if overlappingfood(headPos, foodPos):     
        moveFood()
        growSnake()
        #increase the speed after eatting the food
        global speed
        speed -= 3


    for i in range (1,len(snake)):
        if overlappingbody(headPos, canvas.coords(snake[i])):
            gameOver = True
            canvas.create_text(width/2 ,330, fill="red", font="Times 20 italic bold", text = "game over!!")
            scoreRecord()
            showBoard()
        #win the game if the speed reaches 0
        if speed == 0:
            gameOver = True
            canvas.create_text(width/2 ,330, fill="blue", font="Times 20 italic bold", text = "You win the game!!")
        
    
    for i in range(1, len(snake)):
        positions.append(canvas.coords(snake[i]))
    #pause the game
    if direction == "pause":
        pass
    else:
        for i in range (len(snake)-1):
            canvas.coords(snake[i+1],positions[i][0], positions[i][1], positions[i][2], positions[i][3])
           

    if "gameOver" not in locals():
        window.after(speed, moveSnake)
    

playername = str(input("Please enter your name: "))


window = setWindowDimensions(width, height)
canvas = Canvas(window, bg="black", width=width, height=height)
bgimage = PhotoImage(file = "bgimage.gif")
apple = PhotoImage(file = "apple.gif")
bKeyimg = PhotoImage(file = "work.gif")
canvas.create_image(width/2, height/2, image = bgimage)
showBoard()

snake = []
snakeSize = 33
snake.append(canvas.create_rectangle(snakeSize, snakeSize, snakeSize * 2, snakeSize * 2, fill = "#48D1CC"))

speed = 80
score = 0
txt = "Score: " + str(score)

scoreText = canvas.create_text(width/2, 10, fill = "white", font = "Times 20 italic bold", text = txt)
playernameText1 = canvas.create_text(width/2, 20, fill = "white", font="Times 15 italic bold", text = "Playername: " + playername)
keytipsText = canvas.create_text(width/2, height/2, fill = "white", font ="Times 15 italic bold", text = "bossKey: <b>, retern: <n> ,cheatKey: <c>, save: <s>, load: <l>"  )
keytipsText = canvas.create_text(width/2, 380, fill = "white", font ="Times 15 italic bold", text = "direction control key: <→>, <←>, <↑>, <↓>, pause key: <space>")


#Binding Keys
canvas.bind("<Left>", leftKey)
canvas.bind("<Right>", rightKey)
canvas.bind("<Up>", upKey)
canvas.bind("<Down>", downKey)
canvas.bind("<space>", pauseKey)
canvas.bind("<c>", cheatKey)
canvas.bind("<b>", bossKey)
canvas.bind("<n>", reBosKey)
canvas.bind("<s>", saveKey)
canvas.bind("<l>", loadKey)
canvas.focus_set()

direction = "right"

#place the food
placeFood()

#move the snake's head
moveSnake()

window.mainloop()