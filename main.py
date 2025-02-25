import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 60
WAIT_TIME = 500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font("font/Pixeltype.ttf", 60)

# Game state vars
player_position = 0
dice_value = 0
game_track = []

gold = 0
health = 100
min_health = 0
max_health = 120
min_gold = 0

name = ""
game_over = False

display_timer = 0
gold_change = 0
health_change = 0

def main_menu():
    menu_font = pygame.font.Font("font/Pixeltype.ttf", 80)
    menu_options = ["2. Quit", "1. Start Game", " Gambler's Survival"]

    while True:
        screen.fill(BLACK)

        for i, option in enumerate(menu_options, start=1):
            text_render(option, 2, i + 0.4)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return  # Start the game
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()  # Quit the game

class Bandit:
    def __init__(self):
        self.gold_penalty = random.randint(25, 50)
        self.health_penalty = random.randint(10, 30)

    def render(self):
        text_render(f"Bandit has appeared! What will you do?", 2, 1.5)
        text_render(f"1. Pay {self.gold_penalty} gold to avoid a fight", 2, 1.2)
        text_render(f"2. Battle the bandit and risk losing {self.health_penalty} health", 2, 1.1)

    def handle_choice(self, choice):
        global end_text

        if choice == 1 and gold >= self.gold_penalty:
            return f"Opened the chest. Gained {self.gold_penalty} gold.", -self.gold_penalty, 0
        elif choice == 2:
            return f"Opened the chest. Gained {self.gold_penalty} gold.", 0, -self.health_penalty
        else:
            return f"Opened the chest. Gained {self.gold_penalty} gold.", 0, -self.health_penalty

class Chest:
    def __init__(self):
        self.gold_reward = random.randint(15, 35)
        self.mimic_chance = 0.1  # 10% chance of encountering a Mimic

    def render(self):
         text_render(f"You have found a chest!", 2, 1.5)
         text_render(f"1. Open the chest and take the gold ({self.gold_reward} gold)", 2, 1.2)
         text_render(f"2. Leave the chest without taking anything", 2, 1.1)

    def handle_choice(self, choice):
        global end_text

        mimic = Mimic()

        if random.random() < self.mimic_chance and choice == 1:
            screen.fill(BLACK)
            display_info()
            mimic.render()
            mimic_choice = get_player_choice()
            return mimic.handle_choice(mimic_choice)
        else:
            
            if choice == 1:
                #end_text = f"Opened the chest. Gained {self.gold_reward} gold."
                return f"Opened the chest. Gained {self.gold_reward} gold.", self.gold_reward, 0
            elif choice == 2:
                #end_text = "Left the chest without taking anything."
                return f"Opened the chest. Gained {self.gold_reward} gold.", 0, 0
            else:
                #end_text = "Invalid choice. You missed the opportunity!"
                return f"Opened the chest. Gained {self.gold_reward} gold.", 0, 0

class Trader:
    def __init__(self):
        self.potion_cost = random.randint(5, 20)
        self.potion_health_increase = random.randint(20, 50)

    def render(self):
        text_render(f"A trader appears! What will you do?", 2, 1.5)
        text_render(f"1. Buy a healing potion ({self.potion_cost} gold, +{self.potion_health_increase} health)", 2, 1.2)
        text_render(f"2. Leave and continue rolling the dice", 2, 1.1)

    def handle_choice(self, choice):
        if choice == 1 and gold >= self.potion_cost:
            return f"Bought a healing potion. Gained {self.potion_health_increase} health.", -self.potion_cost, self.potion_health_increase
        elif choice == 1:
            return "Not enough gold to buy a potion. The trader is disappointed.", 0, 0
        elif choice == 2:
            return "Left the trader. Continued rolling the dice.", 0, 0
        else:
            return "Invalid choice. The trader looks confused.", 0, 0

class Mimic:
    def __init__(self):
        self.low_health_penalty = random.randint(5, 10)
        self.high_health_penalty = random.randint(10, 20)
        self.gold_reward = random.randint(30, 60)

    def render(self):
        text_render(f"Uh-oh! The chest is a Mimic!", 2, 1.5)
        text_render(f"1. Run away (lose a bit of health({self.low_health_penalty}) and get no gold)", 2, 1.2)
        text_render(f"2. Fight the Mimic again (risk losing more health({self.high_health_penalty}) but gain more gold({self.gold_reward}))", 2, 1.1)

    def handle_choice(self, choice):
        global player
        if choice == 1:
            player.health -= self.low_health_penalty
            return f"Ran away from the Mimic. Lost {self.low_health_penalty} health.", 0, -self.low_health_penalty
        elif choice == 2:
            gold_reward = self.gold_reward
            player.health -= self.high_health_penalty
            return f"Fought the Mimic again. Lost {self.high_health_penalty} health but gained {gold_reward} gold.", gold_reward, -self.high_health_penalty
        else:
            return "Invalid choice. The Mimic attacks!", 0, -self.low_health_penalty

class Player:
    def __init__(self, name, health, gold,):
        self.name = name
        self.health = health
        self.gold = gold


# Initialize player
player = Player("Gambler", 100, 10)

# Pygame screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gambler's Survival")

# Main game loop
def main():
    global player_position, game_over, in_game

    initialize_game_track()

    while not game_over:
        if in_game:
            handle_events()
            update_game()
            render_game()
        else:
            main_menu()
            pygame.time.wait(500)
            in_game = True

        pygame.time.Clock().tick(FPS)

    pygame.quit()
    sys.exit()

# Handle input events
def handle_events():
    global game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True

# Update game state
def update_game():
    global dice_value, player_position, gold, health

    if health <= min_health:
        game_over_screen("Game Over - You Lose")

    if player_position >= 100:
        game_over_screen("Congratulations! You Win")

    if dice_value == 0:
        roll_dice()

    else:
        update_player()

        current_time = pygame.time.get_ticks()
        if current_time - display_timer >= 1000:
            dice_value = 0

        pygame.time.wait(WAIT_TIME)

# Render game elements
def render_game():
    screen.fill(BLACK)
    display_info()
    pygame.display.update()

# Roll the dice
def roll_dice():
    global dice_value
    keys = pygame.key.get_pressed()

    if any(keys):
        dice_value = random.randint(1, 6)

def update_player():
    global player_position, gold, health, gold_change, health_change, game_track

    player_position += dice_value

    # Ensure player_position is within the valid range
    player_position = min(max(player_position, 0), len(game_track) - 1)

    current_event = game_track[player_position]["event"]

    if current_event:
        current_event.render()
        choice = get_player_choice()
        message, gold_change, health_change = current_event.handle_choice(choice)

    gold += gold_change
    health += health_change

    if health > max_health:
        health = max_health

    if gold < min_gold:
        gold = min_gold


def get_player_choice():
    pygame.display.update()
    choice = 0
    while choice not in [1, 2]:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choice = 1
                elif event.key == pygame.K_2:
                    choice = 2
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    return choice

def initialize_game_track():
    global game_track

    game_track = []

    for position in range(100):
        if position % random.randint(5, 9) == 0:
            event = Bandit()
        elif position % random.randint(2, 7) == 0:
            event = Chest()
        elif position % 10 == 0:
            event = Trader()
        else:
            event = None

        game_track.append({"event": event})


# Display information on the screen
def display_info():
    global player_position, dice_value, gold, health, gold_change, health_change

    text_render(f"Player moved to position {player_position}", 7, 1.3)
    text_render(f"Dice: {dice_value}", 7, 1.25)
    
    text_render(f"Gold: {gold} ({gold_change})", 7, 1.2)
    text_render(f"Health: {health} ({'' if health_change >= 0 else ''}{health_change})", 7, 1.15)

    previous_vertical_position = 5  

    for i in range(1, 6):
        next_position = min(player_position + i, len(game_track) - 1)
        next_event = game_track[next_position]["event"]

        vertical_position = previous_vertical_position - 0.5

        if next_event:
            text_render(f"Position {next_position}: {next_event.__class__.__name__}", 2, vertical_position)
        else:
            text_render(f"Position {next_position}: Nothing", 2, vertical_position)

        previous_vertical_position = vertical_position

            
    if dice_value != 0:
        display_timer = pygame.time.get_ticks()
        if display_timer >= 1000:
            gold_change = 0 
            health_change = 0
            end_text = ""

    pygame.display.update()


# Display game over screen
def game_over_screen(message):
    screen.fill(BLACK)
    text_render(message, 2, 3)

    if "Congratulations" in message:  # Check if it's the win screen
        text_render(f"Total Gold left: {gold}", 2, 2)

    pygame.display.update()
    pygame.time.delay(3000)  # Display for 3 seconds before exiting
    pygame.quit()
    sys.exit()

# Function to render text on the screen
def text_render(target_text, width_var, height_var):
    text_surface = FONT.render(target_text, False, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // width_var, HEIGHT // height_var))
    screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    in_game = False
    main()