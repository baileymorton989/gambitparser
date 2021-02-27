#payoffparser example
import gambitparser
import argparse

#add arguments to use in the command line
# --title Z
def argparser():
    parsed = argparse.ArgumentParser()                            
    parsed.add_argument("--file",help = "the title of the game", default='Game.txt')
    args = parsed.parse_args()
    return parsed,args

if __name__ == '__main__':
    parsed,args = argparser()
    payoffparser = gambitparser.PayoffParser(args.file)
    payoffparser.preprocess()
    payoffparser.build()
    payoffparser.solve()
    payoffparser.parse()