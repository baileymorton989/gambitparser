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
    parser = gambitparser.Parser(args.num_moves,args.num_players, args.title)
    parser.build()
    #get the payoffs for each path
    def make_payoffs(parser):
        parser.outcomes = []
        for path in parser.all_paths:
            prelim_outcomes =[]
            for i in range(len(path)):
                if path[0] == 1 and path[1] == 1:
                    high_quality_payoff = 2
                    low_quality_payoff = 1
                    if int(path[i]) % 2 != 0:
                        prelim_outcomes.append(low_quality_payoff)
                    elif int(path[i]) % 2 == 0:                                                              
                        prelim_outcomes.append(high_quality_payoff)
                elif path[0] == 1 and path[1] == 2:
                    high_quality_payoff = 3
                    low_quality_payoff = 0
                    if int(path[i]) % 2 !=0:
                        prelim_outcomes.append(high_quality_payoff)
                    elif int(path[i]) % 2 == 0:
                        prelim_outcomes.append(low_quality_payoff) 
                elif path[0] == 2 and path[1] == 1:
                    high_quality_payoff = 0
                    low_quality_payoff = 3
                    if int(path[i]) % 2 !=0:
                        prelim_outcomes.append(low_quality_payoff)
                    elif int(path[i]) % 2 == 0:
                        prelim_outcomes.append(high_quality_payoff)                          
                elif path[0] == 2 and path[1] == 2:
                    high_quality_payoff = 2
                    low_quality_payoff = 2
                    if int(path[i]) % 2 !=0:
                        prelim_outcomes.append(low_quality_payoff)
                    elif int(path[i]) % 2 == 0:
                        prelim_outcomes.append(high_quality_payoff)                               
            parser.outcomes.append(prelim_outcomes)
        return parser.outcomes
    parser.outcomes = make_payoffs(parser)
    parser.payoffs()
    parser.solve()
    parser.parse()
