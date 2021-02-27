#parsed example 	
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
    parsed,args = argparsed()
    parser = gambitparser.Parser(args.num_moves,args.num_players, args.title)
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
