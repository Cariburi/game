from pygame import init, Rect, display, draw, time, Surface
from pygame.font import Font
import random
import keyboard as k
import math as m
init()

def _snapToGrid(grid: int, co: int) -> int:
    return m.floor((co / grid) * grid)

# Class to initialise players
class Player(Rect):
    def __init__(self, screen_width: int, screen_height: int, grid: int):
        self.grid = grid
        self.score = 0 # Total score
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.name = ""
        self.chase = 0
        self.rage_mode = False
        self.width = 20 # Width of object
        self.height = 20 # Height of object
        self.left = _snapToGrid(self.grid, random.randrange(1, 400)) # Spawn co-ordinates
        self.top = _snapToGrid(self.grid, random.randrange(1, 400)) # Same here

    def _switch_of_rage_mode(self):
        self.rage_mode = False
        return
    
    def draw(self, screen: Surface, colour): # Draw object
        draw.rect(screen, colour, self)

    def spawn(self): # Spawn Object
        self.left = _snapToGrid(self.grid, random.randrange(1, 400))
        self.top = _snapToGrid(self.grid, random.randrange(1, 400))

    def collision_detect(self): # Detect wall collision
        if self.screen_width < self.x + self.width:
            self.x = self.screen_width - self.width

        elif self.x < 0:
            self.x = 0

        if self.screen_height < self.y + self.height:
            self.y = self.screen_height - self.height

        elif self.y < 0:
            self.y = 0

    def CrashPlayer(self, other_player): # Kill player
        collide = self.colliderect(other_player)
        if collide:
            other_player.score += 1
            other_player.spawn()
    
    def RageMode(self, t):
        if t == 1400:
            self.rage_mode = False
            return
        
        self.rage_mode = True
    
    def activate_chase_mode(self):
        self.chase = 1

    def deactivate_chase_mode(self):
        self.chase = 0

    def _collide_bot_detection(self, bot):

        collide = self.colliderect(bot)

        if collide:
            bot._spawn()
            self.score += 5

class Bot(Rect):
    def __init__(self, grid: int, screen: Surface, sw: int, sh: int, difficulty: int = 0): 
        self.grid = grid - difficulty # if difficulty is negative the the difficulty of the bot rises
        self.sw = sw
        self.sh = sh
        self.screen = screen
        self.left = _snapToGrid(grid, random.randrange(1, 400))
        self.top = _snapToGrid(grid, random.randrange(1, 400))
        self.width = 20
        self.height = 50
    
    def __check_corners(self):
        if self.x == 0 and self.y == 0:
            self.x -= self.grid
            self.y += self.grid
        elif self.x == 500 and self.y == 500:
            self.x += self.grid
            self.y -= self.grid
        elif self.x == 500 and self.y == 0:
            self.x += self.grid
            self.y +=self.grid
        elif self.x == 0 and self.y == 500:
            self.x -= self.grid
            self.y -= self.grid
        else:
            return

    def _move_from_rage_mode(self, player: Player):      
        steps_x = self.x - player.x
        steps_y = self.y - player.y

        self.__check_corners()
        
        if steps_x >= -100 :
            
            if self.x == 0:
                self.x += self.grid

            self.x += self.grid

        elif steps_x <= 100:

            if self.x == 0:
                self.x -= self.grid

            self.x -= self.grid

        if steps_y >= -100:

            if self.y == 0:
                self.y += self.grid
            
            self.y += self.grid

        elif steps_y <= 100:
            
            if self.y == 0:
                self.y += self.grid
            
            self.y -= self.grid

        else:
            pass
        
        return None

    def _spawn(self):
        self.left = _snapToGrid(self.grid, random.randrange(1, 400))
        self.top = _snapToGrid(self.grid, random.randrange(1, 400))

    def _check_obj_collision(self, player: Player):
        if player.rage_mode:
            return
        
        collide = self.colliderect(player)
        if collide:
            player.score -= 2
            player.spawn()
            return 
    
    def _check_wall_collision(self):
        
        if self.sw < self.x + self.width:
            self.x = self.sw - self.width

        elif self.x < 0:
            self.x = 0

        if self.sh < self.y + self.height:
            self.y = self.sh - self.height

        elif self.y < 0:
            self.y = 0

    def _enumarate_path_to_player(self, player: Player):
        steps_x = self.x - player.x
        steps_y = self.y - player.y

        if steps_x < 0:
            self.x += self.grid
        else:
            self.x -= self.grid

        if steps_y < 0:
            self.y += self.grid
        else:
            self.y -= self.grid
    
    def draw(self):
        draw.rect(self.screen, (20, 20, 70), self)

    def run(self, player):
        if player.rage_mode == True:
            self._move_from_rage_mode(player)
            self._move_from_rage_mode(player)
            self._check_wall_collision()
            return
        
        self._enumarate_path_to_player(player)
        self._check_obj_collision(player)
        self._check_wall_collision()
        return

# Class for target Object
class Target(Rect): 
    def __init__(self, screen_width: int, screen_height: int, grid):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 20
        self.height = 20
        self.grid = grid
        self.left = _snapToGrid(grid, random.randrange(1, 400))
        self.top = _snapToGrid(grid, random.randrange(1, 400))

    def draw(self, screen): # draw target
        draw.rect(screen, (23, 234, 45), self)
    
    def spawn(self): # spawn target
        self.left = _snapToGrid(self.grid, random.randrange(1, 400))
        self.top = _snapToGrid(self.grid, random.randrange(1, 400))

    def checkDeath(self, player: Player): # Check collision with player
        collide = self.colliderect(player)
        if collide:
            player.score += 1
            self.spawn()

dif = -1 #Difficulty level

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
