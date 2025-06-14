#COMMMMMMMMMMMMMMMMMMMMEEEEEEEEEEEEENNNNNNNNNTTTTTSSSSSSS
from pygame import init, Rect, display, draw, time, Surface
from pygame.font import Font
from Objs import Player, Target, Bot
import keyboard as k
init()

dif = -1

def _print_on_screen(texto: str, font: Font, co: tuple[int, int], colour: tuple[int, int, int], screen: Surface):
    render = font.render(texto, True, colour)
    screen.blit(render, co)

# Display score on screen
def _print_score(player, font: Font, colour: tuple[int, int, int], co: tuple[int, int], screen: Surface):
    render = font.render(f"Score: {player.score}", True, colour)
    screen.blit(render, co)

# Initialise title for window
def _show_title():
    display.set_caption(title="GAME")

# Snap objects to game grid

def declare_winner(player_1, player_2):
    if player_1.score < player_2.score:
        return f"Winner: {player_2.name}"
    
    elif player_1.score > player_2.score:
        return f"Winner: {player_1.name}"
    
    elif player_1.score == player_2.score:
        return "Draw"

    return ""

_show_title()

def _set_bot_difficulty(grid: int, screen: Surface, sh: int, sw: int, choice: int = 0) -> Bot:
    if choice == 1:
        return Bot(grid=grid, screen=screen, sh=sh, sw=sw, difficulty=-5)
    
    elif choice == -1:
        Bot(grid=grid, screen=screen, sh=sh, sw=sw, difficulty=5)
    
    elif choice == 0:
        return Bot(grid=grid, screen=screen, sh=sh, sw=sw)
    
    return Bot(grid=grid, screen=screen, sh=sh, sw=sw)

time_s = 0
run = True
SH = 500 # Screen Height
SW = 500 # Screen Width
GRID = 15 # Grid for screen


if __name__ == "__main__":
    screen = Surface(size=(SW, SH)) # Screen
    font = Font(None, 40)
    GAME_OVERfont = Font(None, 60)
    
    clock = time.Clock()
    player1 = Player(grid=GRID, screen_height=SH, screen_width=SW)
    p1_colour = 89, 98, 67
    player2 = Player(grid=GRID, screen_height=SH, screen_width=SW)
    p2_colour = 16, 78, 150
    opp = Target(grid=GRID, screen_width=SW, screen_height=SH)

    screen = display.set_mode(screen.get_size())

    bot = _set_bot_difficulty(choice=dif, grid=GRID, screen=screen, sh=SH, sw=SW)

    while run: # Same as While True
        
        if k.is_pressed("ctrl+r"):
            run = False

        screen.fill((0, 0, 0))

        bot.run(player1)
        
        if time_s % 100 == 1:
            bot.run(player=player2)
        
        elif time_s % 200 == 1:
            bot.run(player1)
        
        if time_s / 300 == 1:
            player1.RageMode(time_s)
            player2.RageMode(time_s)
        
        if time_s / 900 == 1:
            player1._switch_of_rage_mode()
            player2._switch_of_rage_mode()
        
        if player1.rage_mode == True:
            player1._collide_bot_detection(bot)
            player2._collide_bot_detection(bot)
        
        

        player1.draw(screen, p1_colour)
        player2.draw(screen, p2_colour)
        opp.draw(screen)
        bot.draw()

        player1.collision_detect()
        player2.collision_detect()
        opp.checkDeath(player=player1)
        opp.checkDeath(player=player2)

        # if-else blocks for player movement        

        if k.is_pressed("w"):
            player1.y -= 15
        elif k.is_pressed("s"):
            player1.y += 15
        elif k.is_pressed("d"):
            player1.x += 15
        elif k.is_pressed("a"):
            player1.x -= 15

        if k.is_pressed("left"):
            player2.x -= 15
        elif k.is_pressed("right"):
            player2.x += 15
        elif k.is_pressed("down"):
            player2.y += 15
        elif k.is_pressed("up"):
            player2.y -= 15

        _print_score(player1, font, p1_colour, (20, 10), screen) # display p1 score
        _print_score(player2, font, p2_colour, (20, 35), screen) # display p2 score
        if time_s == 1000:
            _print_on_screen("GAME OVER", GAME_OVERfont, (180, 250), (255, 0, 0), screen)
            _print_on_screen(declare_winner(player_1=player1, player_2=player2), font=font, co=(180, 200), colour=(255, 0, 0), screen=screen)

        display.flip()
        
        time_s += 1
        print(time_s)

        clock.tick(20) # Resolution
