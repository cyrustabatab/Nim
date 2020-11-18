import pygame
import random
import time


pygame.init()

SCREEN_WIDTH = SCREEN_HEIGHT  = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))



font = pygame.font.SysFont("comicsansms",42)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
pygame.display.set_caption("NIM")

done = False

def create_piles(n=5):
    
    piles = []
    for _ in range(n):
        pile_size = random.randint(2,12)
        piles.append(pile_size)
    

    return piles



def draw_piles(piles):

    headings = []
    
    top_offset = 10
    left_offset = 30
    gap = 20
    circle_gap = 30
    circle_radius = 10
    left_gap = 2
    for i in range(len(piles)):
        pile_size = piles[i]
        text = font.render(f"Pile {i + 1}: ",True,BLACK)
        screen.blit(text,(left_offset,top_offset + (gap + text.get_height()) * i))
        right_edge_of_text = left_offset + text.get_width()
        for j in range(pile_size):
            pygame.draw.circle(screen,RED,(right_edge_of_text +left_gap+ (circle_gap) * j,top_offset + (gap + text.get_height()) * i + text.get_height()//2),circle_radius)
        
        amount_text = font.render(str(pile_size),True,BLACK)
        screen.blit(amount_text,(right_edge_of_text + left_gap + circle_gap * pile_size,(gap + amount_text.get_height()) * i))





        


    





def remove_from_pile(piles,pile_number,number_of_sticks_to_remove):

    piles[pile_number] -= number_of_sticks_to_remove



def check_game_over(pile):

    return all(amount == 0 for amount in pile)

number_of_piles = 5

        
piles = create_piles()

prompt_text = font.render("Pile Number: ",True,BLACK)
info_text = None
getting_pile_number = True
prompt_answer = ''
prompt_answer_text = None
waiting = False
pile_number = None
number_of_sticks_to_remove = None
game_over = False
turn = 1
turn_text = font.render(f"Player {turn}'s turn",True,BLACK)

while not done:

    if waiting:

        current_time = time.time()

        if current_time - start_time >= 1:
            waiting = False
            info_text = None


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif not waiting and event.type == pygame.KEYDOWN:
            if prompt_answer and event.key == pygame.K_BACKSPACE:
                prompt_answer = prompt_answer[:-1]
                prompt_answer_text = font.render(prompt_answer,True,BLACK)
            elif game_over and event.key == pygame.K_RETURN:
                piles = create_piles()
                game_over = False
                getting_pile_number = True
                turn = 1
                turn_text = font.render(f"Player {turn}'s turn",True,BLACK)
                info_text = None
            elif prompt_answer and event.key == pygame.K_RETURN:
                if getting_pile_number:
                    if 1 <= int(prompt_answer) <= number_of_piles and piles[int(prompt_answer) - 1] > 0:
                        pile_number = int(prompt_answer) - 1
                        prompt_text = font.render("# Dots to Remove: ",True,BLACK)
                        getting_pile_number = False
                    else:
                        info_text = font.render("Invalid Pile Number",True,BLACK)
                        waiting = True
                        start_time = time.time()
                else:
                    if 1 <= int(prompt_answer) <= piles[pile_number]:
                        number_of_sticks_to_remove = int(prompt_answer)
                        remove_from_pile(piles,pile_number,number_of_sticks_to_remove)
                        game_over = check_game_over(piles)
                        if game_over:
                            info_text = font.render("GAME OVER",True,BLACK)
                            if turn ==1:
                                turn_text = font.render(f"PLAYER 2 WINS!!",True,BLACK)
                            else:
                                turn_text = font.render(f"PLAYER 1 WINS!!",True,BLACK)
                        else:
                            getting_pile_number = True
                            prompt_text = font.render("Pile Number: ",True,BLACK)
                            if turn == 1:
                                turn = 2
                            else:
                                turn = 1
                            turn_text = font.render(f"Player {turn}'s turn",True,BLACK)
                    else:
                        info_text = font.render("Invalid Move",True,BLACK)
                        waiting = True
                        start_time = time.time()
                prompt_answer_text = None
                prompt_answer = ''
            elif pygame.K_0 <= event.key <= pygame.K_9:
                prompt_answer += chr(event.key)
                prompt_answer_text = font.render(prompt_answer,True,BLACK)


            
                    




    
    screen.fill(WHITE)
    draw_piles(piles)
    screen.blit(prompt_text,(30,SCREEN_HEIGHT - 20 - prompt_text.get_height()))
    if prompt_answer_text:
        screen.blit(prompt_answer_text,(30 + prompt_text.get_width(),SCREEN_HEIGHT - 20 - prompt_answer_text.get_height()))
    screen.blit(turn_text,(30 + turn_text.get_width(),SCREEN_HEIGHT - 20 - prompt_text.get_height() - 20 - turn_text.get_height()))
    if info_text:
        screen.blit(info_text,(SCREEN_WIDTH - 30 - info_text.get_width(),SCREEN_HEIGHT - 20 - info_text.get_height()))
    pygame.display.update()




