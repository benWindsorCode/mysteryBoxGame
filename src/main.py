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

def runsim(simulation_runs: int, initial_boxes: int, prize: float, ticket_cost: float) -> float:
    winnings = [ singlerun(initial_boxes, prize, ticket_cost) for _ in range(simulation_runs)]

    return sum(winnings)/len(winnings)

def main():
    simulation_runs = 2
    initial_boxes = 4
    prize = 100
    theoretical_cost = theoreticalprice(initial_boxes, prize)
    ticket_cost = 40

    result = runsim(simulation_runs, initial_boxes, prize, ticket_cost)
    print('Simulation average winnings: {}, over simulation_runs: {}, with theoretical_cost: {}'.format(result, simulation_runs, theoretical_cost))

if __name__ == '__main__':
    main()
