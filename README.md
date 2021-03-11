# gambitparser

`gambitparser` is a Python library built on top of [gambit](https://gambitproject.readthedocs.io/en/latest/pyapi.html) for efficiently building, solving and parsing perfect information games. It is currently designed for simple games where each player has the same number of moves at each stage of the game. There are two parser modules: `Parser` and `PayoffParser`.

The `Parser` module is the standard approach for parsing games. The user needs to pass in the number of players in the game, the number of moves for each player, and they can provide a game title as well if needed for keeping track of multiple projects. Additionally, the user will need to provide their own payoff function which outputs a list of lists with the outcomes for each player for each combination of actions.

Here is a simple example of the format that the payoff function should output, where Player 1 has actions {1,2} and Player 2 has actions {1,2}:

	[[2,-2],[1,-1],[-1,1],[-2,2],[1,-1],[-1,1]]

For the first list, we can interpret this as "Player 1 chose 1 and received a payoff of 2, Player 2 chose 1 and received a payoff of -2".

The `PayoffParser` module allows a user to pass in a list of the payoffs for a game. The user will simply need to provide a text file of the payoffs in which the numeric action labels for each player are listed as well as the corresponding payoffs for each player.

Here is a simple example:

	1,1:50/3,50/3
	1,2:20,20
	1,3:25,25
	2,1:20,20
	2,2:50/3,50/3
	2,3:20,20
	3,1:25,25
	3,2:20,20
	3,3:50/3,50/3

We can interpret the first line as "Player 1 chose 1, Player 2 chose 1 : Player 1 had a payoff of 50/3, Player 2 had a payoff of 50/3". To read more about the documentation, visit the [src](https://github.com/baileymorton989/gambitparser_private/tree/master/src) folder.

## Installation

Installation will soon be made simple by using [pip](https://pip.pypa.io/en/stable/)

```bash
pip install gambitparser
```

For now you can simply clone the repo and run the following:

```bash
pip install -e .
```

## Usage

Here are two simple examples using `Parser` and `PayoffParser`. We will use `gambit` library to build the game object and we can use `argparse` to provide the number of moves, number of players, and game title. Then the user will just need to provide a payoff function for the `Parser` module and a .txt file with the payoffs for the `PayoffParser` module.

`Parser` Example : 

```python
#parser example 	
import gambitparser
import argparse 

#add arguments to use in the command line
# --num_moves X --num_players Y --title Z
def argparser():
    parsed = argparse.ArgumentParser()
    parsed.add_argument("--num_moves", help="the number of moves in the game", default = 2)
    parsed.add_argument("--num_players", help="the number of players in the game", default =2)
    parsed.add_argument("--title",help = "the title of the game", default="Game")
    args = parsed.parse_args()
    return parsed,args

#build, solve, and parse the game
if __name__ == '__main__':
    parsed,args = argparser()
    parser = gambitparser.Parser(args.num_moves,args.num_players,args.title)
    parser.build()
    #get the payoffs for each path
    def make_payoffs(parser):
	parser.outcomes = []
	for path in parser.all_paths:
	    num_high_quality = 0
	    num_med_quality = 0
	    num_low_quality = 0
	    prelim_outcomes =[]
	    for i in range(len(path)):
		if path[i] == 1:
		    num_low_quality +=1
		elif path[i] == 2:
		    num_med_quality +=1
		elif path[i] == 3:
		    num_high_quality +=1
	    for i in range(len(path)):
		high_quality_payoff = Fraction(100/(3*num_high_quality + 2*num_med_quality + num_low_quality)).limit_denominator(10)
		med_quality_payoff = Fraction(100/(2*num_high_quality + 3*num_med_quality + 2*num_low_quality)).limit_denominator(10)
		low_quality_payoff = Fraction(100/(num_high_quality + 2*num_med_quality + 3*num_low_quality)).limit_denominator(10)
		if path[i] == 1:
		    prelim_outcomes.append(low_quality_payoff)
		elif path[i] == 2:
		    prelim_outcomes.append(med_quality_payoff)
		elif path[i] == 3:
		    prelim_outcomes.append(high_quality_payoff)                      
	    parser.outcomes.append(prelim_outcomes)
	return parser.outcomes
    parser.outcomes = make_payoffs(parser)
    parser.payoffs()
    parser.solve()
    parser.parse()
```

`PayoffParser` Example:

```python
#payoffparser example
import gambitparser
import argparse

#add arguments to use in the command line
# --title Z
def argparser():
    parsed = argparse.ArgumentParser()                            
    parsed.add_argument("--file",help = "the title of the payoff file", default='Simple_Game.txt')
    parsed.add_argument("--title",help = "the title of the game", default='Simple_Game')
    args = parsed.parse_args()
    return parsed,args

#build, solve, and parse the game
if __name__ == '__main__':
    parsed,args = argparser()
    payoffparser = gambitparser.PayoffParser(args.file,args.title)
    payoffparser.preprocess()
    payoffparser.build()
    payoffparser.solve()
    payoffparser.parse()
```

These examples and other can be found in the [test](https://github.com/baileymorton989/gambitparser_private/tree/master/tests) folder. Currently, [gambit](https://gambitproject.readthedocs.io/en/latest/pyapi.html) only supports Python 2 environments, so all scripts which `gambitparser` must be run in the following way:

```bash
python2 gambitparser-example.py
```

## Operating System
This package was developed using Ubuntu and we have not tested it using other operating systems. We recommend building Gambit on a Linux machine with >=Ubuntu 16.04. More information on building and working with Gambit can be found on their [build](http://www.gambit-project.org/gambit16/16.0.0/build.html) page.

## Contributing
We are open to pull requests and look forward to expanding this library further to tackle more complex games. Please open an issue to discuss any changes or improvements.
To install `gambitparser`, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
pip install -e .[dev]
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
