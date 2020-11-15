#!/usr/bin/env python3
import random

# Probability of winning on a certain attempt = prob(losses on winning_attempt-1 tries) * prob(win on winning_attempt try), counting from attempt 1,2,...
def probattempt(initial_boxes: int, winning_attempt: int) -> float:

    # Initialise probability to the multiplicative identity
    prob = 1

    # First calculate the loosing probabilities that lead up to the win
    loosing_attempts = winning_attempt - 1
    for i in range(loosing_attempts):
        boxes_remaining = initial_boxes - i
        prob *= (boxes_remaining-1)/boxes_remaining

    # Then multiply by the probability of the win on the winning_attempt
    prob *= 1/(initial_boxes - winning_attempt + 1)

    return prob

# Theoretical price of a ticket if the expected winnings of the game are $0 i.e. if the expected cost ==  $prize
def theoreticalprice(initial_boxes: int, prize: float) -> float:

    total = 0

    # sum i * Prob(win on attempt i)
    for attempt in range(1, initial_boxes+1):
        total += attempt * probattempt(initial_boxes, attempt)

    # theoretical price = prize/sum(i*prob(win on attempt i))
    return(prize/total)

# A single simulated run of the box game returning the winnings of the player
def singlerun(initial_boxes: int, prize: float, ticket_cost: float, max_spend: float) -> float:
    winnings = 0
    spend = 0
    boxes = list(range(initial_boxes))
    winning_box = random.choice(boxes)

    print('Running simulation: winning_box: {}, max_spend: {}, ticket_cost: {}'.format(winning_box, max_spend, ticket_cost))
    for _ in range(initial_boxes):
        if spend + ticket_cost > max_spend:
            return winnings

        spend += ticket_cost
        winnings -= ticket_cost
        box_to_open = random.choice(boxes)

        print('Attempt: spend: {}, box_to_open: {}, boxes: {}'.format(spend, box_to_open, boxes))
        if box_to_open == winning_box:
            winnings += prize
            return winnings

        boxes.remove(box_to_open)

    return winnings

# Multiple runs of the box game simulation, returning the avg winnings of the player
def runsim(simulation_runs: int, initial_boxes: int, prize: float, ticket_cost: float) -> float:
    # For a standard naive scenario set max_spend to allow player to always complete the game
    max_spend = ticket_cost * (initial_boxes + 1)
    winnings = [ singlerun(initial_boxes, prize, ticket_cost, max_spend) for _ in range(simulation_runs)]

    return sum(winnings)/len(winnings)

# Improved version of runsim where each player has a random wallet, up to max_wallet_size, and will have a max spend as a random proportion of that wallet
# Assume players will have enough to buy at least one ticket
def improvedrunsim(simulation_runs: int, initial_boxes: int, prize: float, ticket_cost: float, max_wallet_size: float) -> float:

    if max_wallet_size < ticket_cost:
        raise Exception('Players must be able to play at least one round of the game')

    winnings = []
    for _ in range(simulation_runs):
        player_wallet = round(random.uniform(ticket_cost, max_wallet_size), 2)
        player_max_spend_fraction = random.uniform(0, 1)
        player_max_spend = round(max(ticket_cost, player_max_spend_fraction * player_wallet), 2)

        winnings.append(singlerun(initial_boxes, prize, ticket_cost, player_max_spend))

    return sum(winnings)/len(winnings)

def main():
    # The number of simulated runs of the game over which to avg the winnings
    simulation_runs = 5000
    # The number of boxes used in the game
    initial_boxes = 4
    # If using improvedrunsim, this max_wallet_size is the max amount of $ a player can have
    max_wallet_size = 500
    # The $ amount in the winning box
    prize = 100
    # The 'fair price' of a ticket assuming 0 expected winnings over time
    theoretical_cost = theoreticalprice(initial_boxes, prize)
    # A profit spread above the theoretical cost of a ticket to play the game. If > 0 seller has advantage, if < 0 player has the advantage
    spread = -0.2000
    # The ticket cost accounting for profit spread
    ticket_cost = (1 + spread) * theoretical_cost
    # If true then use the improved simulation accounting for player wallet size
    use_improved_sim = True

    if use_improved_sim:
        result = improvedrunsim(simulation_runs, initial_boxes, prize, ticket_cost, max_wallet_size)
    else:
        result = runsim(simulation_runs, initial_boxes, prize, ticket_cost)

    print('Simulation average winnings: {}, over simulation_runs: {}, with theoretical_cost: {}, and ticket_cost: {}'.format(result, simulation_runs, theoretical_cost, ticket_cost))

if __name__ == '__main__':
    main()
