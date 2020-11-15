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
def singlerun(initial_boxes: int, prize: float, ticket_cost: float) -> float:
    print('Running simulation')
    winnings = 0
    boxes = list(range(initial_boxes))
    winning_box = random.choice(boxes)

    for _ in range(initial_boxes):
        winnings -= ticket_cost
        box_to_open = random.choice(boxes)

        print('Run: {}, winning_box: {}, winnings: {}, box_to_open: {}, boxes: {}'.format(_, winning_box, winnings, box_to_open, boxes))
        if box_to_open == winning_box:
            winnings += prize
            return winnings

        boxes.remove(box_to_open)

    return winnings

# Multiple runs of the box game simulation, returning the avg winnings of the player
def runsim(simulation_runs: int, initial_boxes: int, prize: float, ticket_cost: float) -> float:
    winnings = [ singlerun(initial_boxes, prize, ticket_cost) for _ in range(simulation_runs)]

    return sum(winnings)/len(winnings)

def main():
    # The number of simulated runs of the game over which to avg the winnings
    simulation_runs = 1
    # The number of boxes used in the game
    initial_boxes = 100
    # The $ amount in the winning box
    prize = 160000
    # The 'fair price' of a ticket assuming 0 expected winnings over time
    theoretical_cost = theoreticalprice(initial_boxes, prize)
    # A profit spread above the theoretical cost of a ticket to play the game. If > 0 seller has advantage, if < 0 player has the advantage
    spread = 0.0000
    # The ticket cost accounting for profit spread
    ticket_cost = (1 + spread) * theoretical_cost

    result = runsim(simulation_runs, initial_boxes, prize, ticket_cost)
    print('Simulation average winnings: {}, over simulation_runs: {}, with theoretical_cost: {}, and ticket_cost: {}'.format(result, simulation_runs, theoretical_cost, ticket_cost))

if __name__ == '__main__':
    main()
