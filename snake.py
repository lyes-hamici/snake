import pygame
import sys
from pygame import *
from pygame.locals import *
from random import *
from button import Button
import random
import time


pygame.init()


black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
orange = pygame.Color(255, 87, 51 )


snake_speed = 30
espace = " "

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH,HEIGHT))
white = (255 , 255 , 255)

BG = pygame.image.load("img/BG.jpg")
BG_VERT = pygame.image.load("img\Background_score.jpg")
BG_SNAKE = pygame.image.load("img\Back_snake.jpg")


pygame.display.set_caption("Snake LH")


fps = pygame.time.Clock()


snake_position = [100, 50]


snake_body = [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			]


fruit_position = [random.randrange(1, (WIDTH//10)) * 10, 
				random.randrange(1, (HEIGHT//10)) * 10]

fruit_spawn = True

direction = 'RIGHT'
change_to = direction


score = 0


def afficher_texte(texte, x, y, couleur=white):

    texte_affiche = get_font(20).render(texte, True, couleur)

    screen.blit(texte_affiche, (x, y))

def get_font(size): 
    return pygame.font.Font("img/font.ttf", size)


def afficher_score(choice,color, font, size):

	score_font = pygame.font.SysFont(font, size)

	score_surface = score_font.render('Score : ' + str(score), True, color)

	score_rect = score_surface.get_rect()
	
	screen.blit(score_surface, score_rect)


def game_over():

	my_font = pygame.font.SysFont("img/font.ttf", 50)
	
	game_over_surface = my_font.render(
		'Score : ' + str(score), True, white)
	
	game_over_rect = game_over_surface.get_rect()
	
	game_over_rect.midtop = (WIDTH/2, HEIGHT/4)
	
	screen.blit(game_over_surface, game_over_rect)
	pygame.display.flip()
	time.sleep(1)
	player_choice()
    
    
	

def game():
    global change_to , direction,fruit_position,fruit_spawn,score,snake_position,snake_body
    musique= pygame.mixer.music.load("music\Push It To The Limit (scarface).mp3")
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)
    snake_position = [100, 50]
    snake_body = [[100, 50],
                [90, 50],
                [80, 50],
                [70, 50]
                ]
    score = 0
    while True:
	
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'


        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()
            
        if not fruit_spawn:
            fruit_position = [random.randrange(1, (WIDTH//10)) * 10, 
                            random.randrange(1, (HEIGHT//10)) * 10]
            
        fruit_spawn = True
        screen.blit(BG_SNAKE,(0,0))
        
        for pos in snake_body:
            pygame.draw.rect(screen, orange,
                            pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screen, white, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))

        if snake_position[0] < 0 or snake_position[0] > WIDTH-10:
            game_over()
            snake_position = [100, 50]

        if snake_position[1] < 0 or snake_position[1] > HEIGHT-10:
            game_over()
            

        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()
                

        afficher_score(1, white, "img/font.ttf", 20)
        
        pygame.display.update()

        
        fps.tick(snake_speed)

        



def tableau_score():
    tableau_scores = []
    running = True
    with open("score.txt", "r") as fichier:
        lines = fichier.readlines()
        for i in range(len(lines)):  # Parcours tous les noms de joueurs
            if i < len(lines):  
                player_name = lines[i].strip()
                tableau_scores.append((player_name))  
    
    while running:
        screen.blit(BG_VERT, (0,0))

        MENU_TEXT = get_font(100).render("SCORE", True, "#FFFFFF")

        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        screen.blit(MENU_TEXT, MENU_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()

        y = 300
        for player in tableau_scores:
            score_text = f"{player} points"
            afficher_texte(score_text, 100, y,white)
            y += 50  # Espacement vertical entre chaque ligne du tableau

        afficher_texte("Appuyez sur Echap pour revenir sur l'ecran d'aceuill", 100, 600)
        
        pygame.display.update()


def main():
    while True:

        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#FFFFFF")

        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("img/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#FFFFFF", hovering_color="White")
        
        SCORE_BUTTON = Button(image=pygame.image.load("img/Options Rect.png"), pos=(640, 400), 
                            text_input="SCORE", font=get_font(75), base_color="#FFFFFF", hovering_color="White")
        
        QUIT_BUTTON = Button(image=pygame.image.load("img/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#FFFFFF", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON,SCORE_BUTTON]:

            button.changeColor(MENU_MOUSE_POS)

            button.update(screen)

        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):

                    game()

                if SCORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    tableau_score()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):

                    pygame.quit()

                    sys.exit()


        pygame.display.update()


def player_choice():
    time.sleep(2)
    global player
    name_player = ""
    player_exists = False
    running = True
    while running:
        screen.blit(BG, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
                if event.key == pygame.K_RETURN:
                    with open("score.txt", "r+") as fichier:
                        lines = fichier.readlines()
                        for line in lines:
                            if line.strip().lower() == name_player.lower():
                                player_exists = True
                                break
                        
                        if not player_exists:
                            fichier.write(name_player.lower()+ str(espace))
                            fichier.write(str(score) + '\n' )
                            main()
                    player = name_player
                    name_player = ""
                else:
                    lettre = chr(event.key)
                    name_player += lettre

        afficher_texte("Entrer vôtre pseudo :",100,100)
        afficher_texte("Seul les lettres en minuscules sont autoriser.",100,50)
        display_word = get_font(10).render(' '.join(name_player), True, white)
        afficher_texte(f"{name_player}", 150 ,150, white) 
        
        pygame.display.update()

main()