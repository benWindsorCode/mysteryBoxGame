# Mystery Box Game
The 'mystery box game' is a standard quant interview question 'suppose you have ten boxes and one has $100 in it, you can pay for a key to open a box, once you open a box it stays open and you can keep paying for keys to open the boxes. How much should you pay for the key?'.

# Closed Form Solution
You can construct a closed form solution for the game, by following through the probability tree. 

Let us study the closed form solution with four boxes, suppose the ticket price is \$x, and the prize in the box is \$100. Then at each stage we have the following payoffs:
- Win after one box = 100 - x
- Win after two boxes = 100 - 2x
- Win after three boxes = 100 - 3x
- Win after four boaxes = 100 - 4x

To price the game fairly we can assume then that this payoff is described by a random variable W (for winnings). A fair price will then mean that E[W] = 0. Hence we can construct the following equation, after working out the expected value of W

(1/4)(100 - x) + (3/4)(1/3)(100 - 2x) + (3/4)(2/3)(1/2)(100 - 3x) + (3/4)(2/3)(1/2)(1)(100 - 3x) = 0

Hence X = \$40. So if you pay \$40 a ticket overall youll breakeven. As the owner of the game you should therefore charge \$40+e where e is an additional profit margin. As the player of the game you should only play if the ticket price is < \$40.

# Simulation
We have now seen the theory of how we could theoretically price the ticket to this game, this repo will now exlpore the reality of this by simulating the game and running multiple runs through the game to find an expected winnings.

To run the simulation:
1. Clone the repo
2. From within the mysteryBoxGame directory run 'python3 src/main.py'

Feel free to play with the parameters of the game in the 'main' funciton in src/main.py
