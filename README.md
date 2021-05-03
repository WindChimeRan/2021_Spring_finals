# Monte Carlo Simulation of the Buttered Toast Phenomenon

## How to run

Use pygame to show the animation

```sh
python main.py --demo
```

Run Monte Carlo Simulation without pygame
```sh
python main.py --demo
```

This repo simulate the falling of a buttered bread, conditioned on multiple variables:

- The position of the bread on the palm/table: u(-15, 15). uniformed distribution
- Palm force: n(-20000, 20000). normal distribution
- The height of palm/table u(50, 180). uniformed distribution

The output of the Monte Carlo Simulation is the probability of butter-side down

For example, using the varables above, the simulation will give an output: 
    P(Butter-Side Down) = 7.9%

You can try your own parameters in the function simulation.

## Demo

