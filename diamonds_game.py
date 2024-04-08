import pygame
import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"


class Deck:
    def __init__(self, suit):
        self.cards = [Card(suit, rank) for rank in range(2, 15)]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return self.cards[:num_cards]


class Player:
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit
        self.hand = []
        self.score = 0

    def deal_cards(self, deck):
        self.hand = deck.deal(13)

    def human_bid(self):
        # No strategy implemented, player chooses a card manually
        while True:
            card_choice = input(f"{self.name}, choose a card (e.g., 7{self.suit}): ")
            for card in self.hand:
                if str(card) == card_choice:
                    self.hand.remove(card)  # Remove the selected card from the player's hand
                    return card
            print(f"Invalid card choice for {self.name}.")

    def computer_bid(self, revealed_diamond_rank):
        # Find the highest card in the hand
        highest_card = max(self.hand, key=lambda card: card.rank)
        self.hand.remove(highest_card)
        return highest_card

    def collect_diamond(self, user_card, computer_card):
        if user_card.rank == computer_card.rank:

            print("Both players played the same card.")
        else:
            highest_rank = max(user_card.rank, computer_card.rank)
            self.score += highest_rank  # Update the score based on the highest rank bid

def draw_game(screen, player1, player2, revealed_diamond, computer_card, winner_message=None, same_card=None):
    screen.fill((0, 128, 0))  # Green background
    font = pygame.font.Font(None, 36)
    text = font.render("Diamond Card Game", True, (255, 255, 255))
    screen.blit(text, (300, 20))

    # Calculate the width and height of a card based on screen dimensions
    card_width = screen.get_width() // 15  # Adjust the divisor as needed
    card_height = card_width * 3 // 2  # Assuming standard card aspect ratio

    # Draw player1's hand
    for i, card in enumerate(player1.hand):
        card_image = pygame.image.load(f"images/{card.rank}{card.suit}.png")
        card_image = pygame.transform.scale(card_image, (card_width, card_height))
        screen.blit(card_image, (50 + i * (card_width + 5), 400))

    # Draw player2's hand (show only back of cards)
    card_back_image = pygame.image.load("images/card_back.png")
    for i in range(len(player2.hand)):
        card_back_image = pygame.transform.scale(card_back_image, (card_width, card_height))
        screen.blit(card_back_image, (50 + i * (card_width + 5), 50))

    # Draw revealed diamond if available
    if revealed_diamond:
        diamond_image = pygame.image.load(f"images/{revealed_diamond.rank}D.png")
        diamond_image = pygame.transform.scale(diamond_image, (card_width, card_height))
        screen.blit(diamond_image, (300, 200))

    # Draw computer's card choice
    if computer_card:
        if same_card:
            card_image = pygame.image.load(f"images/{same_card.rank}{same_card.suit}.png")
        else:
            card_image = pygame.image.load(f"images/{computer_card.rank}{computer_card.suit}.png")
        card_image = pygame.transform.scale(card_image, (card_width, card_height))
        screen.blit(card_image, (350, 50))  # Adjust position as needed

    # Draw scores
    font = pygame.font.Font(None, 24)
    player1_score_text = font.render(f"{player1.name}: {player1.score}", True, (255, 255, 255))
    player2_score_text = font.render(f"{player2.name}: {player2.score}", True, (255, 255, 255))
    screen.blit(player1_score_text, (50, 360))
    screen.blit(player2_score_text, (50, 20))

    # Draw winner message if available
    if winner_message:
        winner_text = font.render(winner_message, True, (255, 255, 255))
        screen.blit(winner_text, (300, 300))

    pygame.display.flip()



def handle_input(player1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # Check if the click is on one of the player's cards
            for i, card in enumerate(player1.hand):
                card_width = screen.get_width() // 15
                card_height = card_width * 3 // 2
                if 50 + i * (card_width + 5) <= x <= 50 + (i + 1) * (card_width + 5) and 400 <= y <= 400 + card_height:
                    selected_card = player1.hand.pop(i)
                    return selected_card
    return None


def play_game(screen):
    # Setup players and decks
    player1_name = input("Enter your name: ")
    player1 = Player(player1_name, random.choice(["S", "H", "C"]))
    player2 = Player("Computer", list({"S", "H", "C"} - {player1.suit})[0])

    # Setup decks
    deck1 = Deck(player1.suit)
    deck2 = Deck(player2.suit)
    diamond_deck = Deck("D")
    diamond_deck.shuffle()

    # Deal cards
    deck1.shuffle()
    deck2.shuffle()
    player1.deal_cards(deck1)
    player2.deal_cards(deck2)

    # Main game loop
    winner_message = None
    while diamond_deck.cards and player1.hand and player2.hand:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        draw_game(screen, player1, player2, diamond_deck.cards[-1], None, winner_message)  # Pass None for computer_card
        selected_card = handle_input(player1)
        if selected_card:
            # Player selected a card, handle the game logic
            player2_card = player2.computer_bid(diamond_deck.cards[-1].rank)
            if selected_card.rank == player2_card.rank:
                # Both players played cards of the same rank
                diamond_card = diamond_deck.deal(1)[0]
                split_score = player2_card.rank // 2  # Calculate the split score
                player1.score += split_score  # Add half of the diamond card's rank to player 1's score
                player2.score += split_score  # Add half of the diamond card's rank to player 2's score
                winner_message = "Both players played the same card."

           
            else:
                winner = player1 if selected_card.rank > player2_card.rank else player2
                winner_message = f"{winner.name} wins the trick!"
                winner.collect_diamond(selected_card, player2_card)  # Pass both cards to collect_diamond method

            # Display updated scores
            draw_game(screen, player1, player2, diamond_deck.cards[-1], player2_card, winner_message)

            # Introduce a short delay before proceeding to the next iteration
            pygame.time.delay(2000)  # Delay for 2 seconds (adjust as needed)

            # Print both players' card choices
            print(f"{player1.name} chose: {selected_card}")
            print(f"{player2.name} chose: {player2_card}")

            # Print scores
            print(f"Scores: {player1.name}: {player1.score}, {player2.name}: {player2.score}")

    # Determine and display the winner message
    winner_message = f"{player1.name} wins the game with a score of {player1.score}!" if player1.score > player2.score else f"{player2.name} wins the game with a score of {player2.score}!"
    draw_game(screen, player1, player2, None, None, winner_message)
    # Pass None for both revealed_diamond and computer_card
    pygame.time.delay(4000)
    print(winner_message)
    print("Final Scores:")
    print(f"{player1.name}: {player1.score}")
    print(f"{player2.name}: {player2.score}")
    return winner_message


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Diamond Card Game")
    play_game(screen)
