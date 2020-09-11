# Bouncing Ball Simulator
# Code is NOT original; followed a HowTo by Christian Thompson
# Youtube link: https://www.youtube.com/watch?v=HHQV3ifJopo

# Part 1: Getting started

import turtle
import random

wn = turtle.Screen()

print(wn.screensize())
# print(type(wn.screensize()))

wn.bgcolor("black")
wn.title("Bouncing Ball Simulator")
wn.tracer(0)

balls = []

for _ in range(5):
	balls.append(turtle.Turtle())

colors = ["red","orange","yellow","green","blue","purple","white"]
shapes = ["circle", "triangle", "square"]

for ball in balls:
	
	ball.shape(random.choice(shapes))
	ball.color(random.choice(colors))
	ball.penup() # the object will draw a line of its path when the pen is down 
	ball.speed(0) # animation speed, not speed of movement
	x = random.randint(-300, 300)
	y = random.randint(-400, 400)
	ball.goto(x, y)
	ball.dy = 0
	ball.dx = random.randint(-3,3)
	ball.da = random.randint(-5,5)

gravity = 0.1


while True:
	wn.update()

	for ball in balls:
		ball.rt(ball.da)
		ball.dy -= gravity
		ball.sety(ball.ycor() + ball.dy) # changes ycor to ycor+dy
		ball.setx(ball.xcor() + ball.dx)

		if ball.xcor() > 300:
			ball.dx *= -1
			ball.da *= -1

		if ball.xcor() < -300:
			ball.dx *= -1
			ball.da *= -1

		if ball.ycor() < -300:
			# ball.sety(-300)
			ball.dy *= -1
			ball.da *= -1

wn.mainloop()
