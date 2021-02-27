#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import to allow for decimal values as payoffs
from __future__ import division
from fractions import Fraction

#ignore warnings
import warnings
warnings.filterwarnings("ignore")

#import the gambit library
import gambit
import itertools

#import the time library to keep track of the script run time
import time

#import the subprocess,sys modules to call command-line functions
import subprocess
import sys

#import pandas and numpy to aid in parsing the game output
import pandas as pd
import numpy as np

#import logging to clean up print statements
import logging
    
#class for parser
class Parser:
    
    def __init__(self, num_moves, num_players, outcomes = [],solver = 'enumpureP',title = 'Game'):
        self.game = gambit.Game.new_tree()
        self.num_moves = num_moves
        self.num_players = num_players
        self.outcomes = outcomes
        self.solver = solver
        self.title = title
        
    #build the game
    def build(self):
        
        #get start time
        def start_time():
            start_Time = time.time()
            self.start_Time= start_Time
            return self.start_Time
        
        start_time()
            
        #make game title
        def game_title():
            self.game.title = self.title
            return self.game.title
            
        game_title()

        #add the player names
        def add_players():
            for i in range(self.num_players):
                self.game.players.add('Player' + str(i + 1))
            return self.game.players
                
        add_players()
    
        #define number of infosets
        def infosetter():
            self.num_infosets = 0
            for x in range(self.num_players):
                self.num_infosets += self.num_moves**x
            return self.num_infosets
    
        #create the root node
        def create_node() :
            if len(self.game.infosets) == 0:
                move = self.game.root.append_move(self.game.players[0],self.num_moves)
                move.label = 'Player1'
                for i in range(self.num_moves) :
                    move.actions[i].label = str(i+1)
    
        create_node()
    
        #create all subsequent nodes
        def create_subsequent_nodes() :
            for info in self.game.infosets:
                if len(self.game.infosets) < infosetter():
                    for member in info.members:
                        if member.is_terminal == False:
                            for i in range(self.num_moves):
                                move = member.children[i].append_move(self.game.players[member.player.number+1],self.num_moves)
                                move.label = 'Player {} Chose {}'.format(member.player.number+1,i+1)
                                for i in range(self.num_moves):
                                    move.actions[i].label = str(i+1)
                else:
                    break
    
        create_subsequent_nodes()
    
        ##get all the terminal nodes
        def get_terminal_nodes() :
            self.terminal_nodes = []
            for infoset in self.game.infosets:
                if self.game.players[len(self.game.players)-1].label in infoset.player.label:
                    for member in infoset.members:
                        for i in range(len(member.children)):
                            self.terminal_nodes.append(member.children[i])
            return self.terminal_nodes
    
        get_terminal_nodes()
    
        #get the paths
        def get_paths():
            self.all_paths =[]
            for i in range(len(self.terminal_nodes)):
                prelim_paths =[]
                while self.terminal_nodes[i].parent != None:
                    prelim_paths.append(int(self.terminal_nodes[i].prior_action.label))
                    self.terminal_nodes[i] = self.terminal_nodes[i].parent
                self.all_paths.append(prelim_paths)
            for path in self.all_paths:
                path.reverse()
    
            return self.all_paths
    
        get_paths()
        
        return self.start_Time, self.game.title, self.game.players, self.terminal_nodes, self.all_paths
    
    #make the payoffs of the game
    def payoffs(self): 
        #flatten the outcomes
        def flat_outs():  
            flatten = itertools.chain.from_iterable
            self.flat_outs = list(flatten(self.outcomes))
            return self.flat_outs
        
        flat_outs()
        
        #get the terminal nodes
        def get_terminal_nodes() :
            self.terminal_nodes = []
            for infoset in self.game.infosets:
                if self.game.players[len(self.game.players)-1].label in infoset.player.label:
                    for member in infoset.members:
                        for i in range(len(member.children)):
                            self.terminal_nodes.append(member.children[i])
            return self.terminal_nodes
    
        #reset the terminal nodes
        def reset_terminal_nodes():
            self.terminal_nodes = get_terminal_nodes()
            return self.terminal_nodes
    
        reset_terminal_nodes()
    
        #assign the payoffs at each terminal node
        def assign_payoffs():
            self.assigned_outcomes = []
            for i in range(len(self.outcomes)):
                for j in range(self.num_moves):
                    out = self.game.outcomes.add("{} chose {}".format(self.game.players[len(self.game.players)-1].label,j+1))
                    self.assigned_outcomes.append(out)
            for out, j in zip(self.assigned_outcomes, range(len(self.outcomes))):
                for k in range(self.num_players):
                    out[k] = self.outcomes[j][k]
            for node, out in zip(self.terminal_nodes, self.assigned_outcomes):
                for i in range(self.num_players):
                    node.outcome = out
            return self.assigned_outcomes, self.terminal_nodes
    
        assign_payoffs()
    
        #save the game to the efg format
        def save_game():
            self.efg = self.game.write('efg')
            self.game_file = open("{}-output.efg".format(self.game.title), "w")
            self.game_file.write(self.efg)
            self.game_file.close()
            return self.efg, self.game_file
        
        save_game()
        
        #runtime to build the game
        def game_time():
            self.game_time = time.time() 
            return self.game_time
        
        game_time()

        return self.flat_outs, self.assigned_outcomes, self.terminal_nodes, self.efg, self.game_file, self.game_time
    
    #solve the game
    def solve(self):
        #solve the game using the terminal
        def solve_external():
            # can take value "enumpureP"
            if self.solver == 'enumpureP':
                self.command = ['gambit-' +self.solver[:-1], '-P']
            else:
                sys.exit('unknown solver')
            self.command.append(self.game_file.name)
            self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.stdout, self.stderr = self.process.communicate()
            return self.stdout,self.command, self.process, self.stderr

        solve_external()

        #runtime to solve the game
        def solve_time():
            self.solve_time = time.time() 
            return self.solve_time
        
        solve_time()

        return self.stdout,self.command, self.process, self.stderr, self.solve_time

    #parse for the ideal output format
    def parse(self):
        #save the output
        def output_cleaner():
            self.output_text = open("{}-output.txt".format(self.game.title), "w")
            self.output_text.write(self.stdout)
            self.output_text.close()
            #read output as text into a dataframe
            self.outcome_df = pd.read_table("{}-output.txt".format(self.game.title), delim_whitespace=True, names=('Infoset','Action','Prob','Value', 'Final'))
            #parse the output
            self.stdout_strip = self.stdout.strip()
            self.output_cleaned = self.stdout_strip.split('NE,')[1:]
            self.output_cleaned  = [x.replace('\n', '') for x in self.output_cleaned]
            self.output_cleaned = [out.split(',') for out in self.output_cleaned]
            for i in range(len(self.output_cleaned)):
                self.output_cleaned[i][:] = [int(x) for x in self.output_cleaned[i]]
            return self.output_text, self.outcome_df, self.stdout_strip, self.output_cleaned
        
        output_cleaner()
        
        #redefine the infoset counter 
        def infosetter_output():
            self.num_infosets_out = 0
            for x in range(1,self.num_players):
                self.num_infosets_out += self.num_moves**x
            return self.num_infosets_out
        
        #create list of  probability dictionaries for each equilibria
        def prob_dict() :
            self.prob_dict = []
            for i in range(len(self.output_cleaned)) :
                mid_dict = {}
                for player in self.game.players:
                    mid_dict.update({player.label : self.output_cleaned[i][infosetter_output() :infosetter_output() + self.num_moves**int(player.label[-1])]})
                self.prob_dict.append(mid_dict)
            return self.prob_dict
        
        prob_dict()
    
        #create probability list
        def prob_list() :
            self.prob_list = []
            for prob in self.prob_dict:
                for key in sorted(prob.keys()):
                    for outcome, i in zip(prob[key], range(len(self.all_paths))):
                        self.prob_list.append(prob[key])
            self.prob_list = [list(x) for x in set(tuple(x) for x in self.prob_list)]
            self.prob_list.sort(key  = len)
            return self.prob_list
    
        prob_list()
    
        #create probability list by player
        def player_prob_list() :
            self.player_prob_list = []
            for prob in self.prob_dict :
                for key in sorted(prob.keys()):
                    prob_prelim = []
                    for pro in prob[key]:
                        prob_prelim.append(pro)
                    self.player_prob_list.append(prob_prelim)
            self.player_prob_list =[self.player_prob_list[x:x+len(self.game.players)] for x in range(0, len(self.player_prob_list),len(self.game.players))]
            return self.player_prob_list
    
        player_prob_list()

        #reshape player probabilities into arrays for multiplication
        def player_prob_arrays():
            self.player_prob_arrays = []
            for player in self.player_prob_list:
                for play in player:
                    self.player_prob_arrays.append(np.array(play).reshape(-1,1))
            self.player_prob_arrays =[self.player_prob_arrays[x:x+len(self.game.players)] for x in range(0, len(self.player_prob_arrays),len(self.game.players))]                        
            return self.player_prob_arrays

        player_prob_arrays()

        #create action list
        def action_list():
            self.action_list = []
            for prob in self.prob_dict:
                for key in sorted(prob.keys()):
                    for outcome, i in zip(prob[key], range(len(self.all_paths))):
                        self.action_list.append(int(self.terminal_nodes[i].prior_action.label))
            return self.action_list
    
        action_list()

        #create action dictionary
        def action_dict():
            self.action_dict = {}
            for player in self.game.players :
                if int(player.label[-1]) == 1:
                    self.action_dict.update({player.label : self.action_list[0: self.num_moves**(int(player.label[-1])-1) *(int(player.label[-1])-1)+ self.num_moves**int(player.label[-1])]})
                else:
                    self.action_dict.update({player.label : self.action_list[self.num_moves**(int(player.label[-1])-1): self.num_moves**(int(player.label[-1])-1) + self.num_moves**(int(player.label[-1]))]})                
            return self.action_dict
    
        action_dict()

        #create action list by the players
        def player_action_list():
            self.player_action_list = []
            for key in sorted(self.action_dict.keys()):
                self.action_prelim = []
                for action in self.action_dict[key]:
                    self.action_prelim.append(action)
                self.player_action_list.append(self.action_prelim)  
            return self.player_action_list
    
        player_action_list()

        #unpack each list
        def player_action_list_cleaned():
            self.player_action_list_cleaned = []
            for i in range(len(self.player_prob_arrays)):
                self.player_action_list_cleaned.append(self.player_action_list)
            return self.player_action_list_cleaned
        
        player_action_list_cleaned()
    
        #reshape list into arrays for multiplication
        def action_arrays():
            self.action_arrays = []
            for action in self.player_action_list_cleaned:
                for act in action:
                   self.action_arrays.append(np.array(act).reshape(-1,1))
            self.action_arrays =[self.action_arrays[x:x+len(self.game.players)] for x in range(0, len(self.action_arrays),len(self.game.players))]
            return self.action_arrays
    
        action_arrays()
    
        #get all the combinations of actions and probabilties that lead to equilibria
        def results():
            self.results =  np.multiply(self.player_prob_arrays, self.action_arrays)
            return self.results
        
        results()

        #convert the arrays of equilibria to lists
        def results_cleaned():
            self.results_cleaned = []
            for result in self.results:
                for res in result:
                    self.results_cleaned.append(res.tolist())
            return self.results_cleaned
    
        results_cleaned()

        #unpack the list of equilibria
        def results_unpacked():
            self.results_unpacked =[]
            for result in self.results_cleaned :
                self.results_unpacked.append([int(x) for [x] in result])
            self.results_unpacked =[self.results_unpacked[x:x+len(self.game.players)] for x in range(0, len(self.results_unpacked),len(self.game.players))]
            return self.results_unpacked
    
        results_unpacked()
                
        #condense the probability lists for each player
        def results_condensed():
            self.results_condensed  = []
            for res in self.results_unpacked:
                for i in range(len(res)):
                    rest = res[i]
                    rest =[rest[x:x+self.num_moves] for x in range(0, len(rest),self.num_moves)]
                    self.results_condensed .append(rest)
            self.results_condensed  = [self.results_condensed [x:x+len(self.game.players)] for x in range(0, len(self.results_condensed ),len(self.game.players))]
            return self.results_condensed
    
        results_condensed()

        #get the true equilibria
        def true_equilibria():
            flatten = itertools.chain.from_iterable     
            self.result_position = []
            self.result_move = []
            for i in range(len(self.results_condensed)):
                self.condensed = self.results_condensed[i]
                for j in range(len(self.condensed)):
                    if j == 0:
                        flat= list(flatten(self.condensed[j]))
                        for k in range(len(flat)):
                            if flat[k] != 0.0:
                                self.result_position.append((k))
                                self.result_move.append(flat[k])
                    else:
                        flat= list(flatten(self.condensed[j]))
                        self.condensed_list = self.condensed[j][self.result_position[-1]]
                        self.condensed_outcome = []
                        for condense in self.condensed_list :
                            if condense != 0.0:
                                self.condensed_outcome.append(condense)
                        for l in range(self.num_moves*self.result_position[-1],self.num_moves*self.result_position[-1]+self.num_moves):
                            if flat[l] != 0.0:
                             self.result_position.append((l))
                             self.result_move.append(flat[l])        
            self.result_move =  [self.result_move[x:x+len(self.game.players)] for x in range(0, len(self.result_move),len(self.game.players))]
            self.results_final = [tuple(x) for x in set(tuple(x) for x in self.result_move)]
            return self.result_move, self.results_final 
    
        true_equilibria()
    
        #make paths in to tuples to use as dictionary keys
        def paths_tuple():
            self.paths_tuple = [tuple(path) for path in self.all_paths]
            return self.paths_tuple
        
        paths_tuple()
    
        #create dictionary of the paths
        def payoff_dict():
            self.payoff_dict = {}
            for path, payoff in zip(self.paths_tuple, self.outcomes):
                self.payoff_dict.update({path:(payoff)})
            return self.payoff_dict
    
        payoff_dict()
    
        #create list of the payoffs
        def payoff_list():
            self.payoff_list = []
            for key in sorted(self.payoff_dict.keys()):
                self.pay_prelim = []
                for pay in self.payoff_dict[key]:
                    self.pay_prelim.append(pay)
                    self.payoff_list.append(self.pay_prelim)
            return self.payoff_list
    
        payoff_list()
                  
        #create action_payoff_list
        def action_payoff_list():
            self.action_payoff_list = []
            for action in self.results_final:
                if action in self.payoff_dict.keys():
                    self.action_payoff_list.append((action,self.payoff_dict[action]))
            return self.action_payoff_list
    
        action_payoff_list()
    
        #create the list of outcomes
        def outcome_list() :
            self.outcome_list = []
            for i in range(self.num_moves+1):
                for j in range(len(self.action_payoff_list)):
                    for act, pay in zip(self.action_payoff_list[j][0], self.action_payoff_list[j][1]):
                        self.outcome_list.append('{} : {}'.format(act,round(float(pay),1)))
            self.outcome_list = [self.outcome_list[x:x+len(self.game.players)] for x in range(0, len(self.outcome_list),len(self.game.players))]
            self.outcome_list = [list(x) for x in set(tuple(x) for x in self.outcome_list)]
            return self.outcome_list

        outcome_list()
        
        #runtime to parse the game
        def parse_time():
            self.parse_time = time.time()
            return self.parse_time
        
        parse_time()

        #print all info
        def output_printer():
        #check runtime to build the game
            print('')
            print(self.efg)
            for outcome in self.outcome_list:
                for out, i in zip(outcome, range(len(self.outcome_list[0])*len(self.outcome_list))):
                    if (i + 1) % (len(self.game.players)) == 0:
                        print('Player {} chose {}'.format(i+1,out))
                        logging.info('Player {} chose {}'.format(i+1,out))
                        print('')
                    else:
                        print('Player {} chose {}'.format(i+1,out))
                        logging.info('Player {} chose {}'.format(i+1,out))
        output_printer()

        return self.output_text, self.outcome_df, self.stdout_strip, self.output_cleaned, self.prob_dict, self.prob_list, self.player_prob_list, self.player_prob_arrays, self.action_list, self.action_dict, self.player_action_list, self.player_action_list_cleaned, self.action_arrays, self.results, self.results_cleaned, self.results_unpacked, self.results_condensed, self.result_move, self.results_final , self.paths_tuple, self.payoff_dict, self.payoff_list, self.action_payoff_list, self.outcome_list, self.parse_time
    
#class for payoffparser
class PayoffParser:
    
    def __init__(self, text_file_name, solver = 'enumpureP',title= 'Game'):
        self.game = gambit.Game.new_tree()
        self.text_file_name = text_file_name
        self.solver = solver
        self.title = title

    #preprocess the text file to be usable for parsing
    def preprocess(self):
        
        def readfile():
            self.text_file = pd.read_table(self.text_file_name, delim_whitespace=False, header = None)
            self.text_file.columns = ['Outcomes']
            return self.text_file
        
        readfile()
        
        #parse the text file
        def simple_parser():
            self.text_file_parsed = [outcome.split(':') for outcome in self.text_file['Outcomes']]
            return self.text_file_parsed
    
        simple_parser()
    
        #find number of players and number of movesd
        def get_moves_and_players():
            self.num_players = len(self.text_file_parsed[0][0]) - 1
            self.num_moves = int(len(self.text_file_parsed) / (self.num_players+1))
            return self.num_players, self.num_moves
    
        get_moves_and_players()

        return self.text_file, self.text_file_parsed, self.num_players, self.num_moves
        
    #build the game
    def build(self):
        
        #get start time
        def start_time():
            start_Time = time.time()
            self.start_Time= start_Time
            return self.start_Time
        
        start_time()
            
        #make game title
        def game_title():
            self.game.title = self.title
            return self.game.title
            
        game_title()

        #add the player names
        def add_players():
            for i in range(self.num_players):
                self.game.players.add('Player' + str(i + 1))
            return self.game.players
                
        add_players()
    
        #define number of infosets
        def infosetter():
            self.num_infosets = 0
            for x in range(self.num_players):
                self.num_infosets += self.num_moves**x
            return self.num_infosets
    
        #create the root node
        def create_node() :
            if len(self.game.infosets) == 0:
                move = self.game.root.append_move(self.game.players[0],self.num_moves)
                move.label = 'Player1'
                for i in range(self.num_moves) :
                    move.actions[i].label = str(i+1)
    
        create_node()
    
        #create all subsequent nodes
        def create_subsequent_nodes() :
            for info in self.game.infosets:
                if len(self.game.infosets) < infosetter():
                    for member in info.members:
                        if member.is_terminal == False:
                            for i in range(self.num_moves):
                                move = member.children[i].append_move(self.game.players[member.player.number+1],self.num_moves)
                                move.label = 'Player {} Chose {}'.format(member.player.number+1,i+1)
                                for i in range(self.num_moves):
                                    move.actions[i].label = str(i+1)
                else:
                    break
    
        create_subsequent_nodes()
    
        ##get all the terminal nodes
        def get_terminal_nodes() :
            self.terminal_nodes = []
            for infoset in self.game.infosets:
                if self.game.players[len(self.game.players)-1].label in infoset.player.label:
                    for member in infoset.members:
                        for i in range(len(member.children)):
                            self.terminal_nodes.append(member.children[i])
            return self.terminal_nodes
    
        get_terminal_nodes()
    
        #get the paths
        def get_paths():
            self.all_paths =[]
            for i in range(len(self.terminal_nodes)):
                prelim_paths =[]
                while self.terminal_nodes[i].parent != None:
                    prelim_paths.append(int(self.terminal_nodes[i].prior_action.label))
                    self.terminal_nodes[i] = self.terminal_nodes[i].parent
                self.all_paths.append(prelim_paths)
            for path in self.all_paths:
                path.reverse()
    
            return self.all_paths
    
        get_paths()
        

        #get the payoffs for each path
        def payoffs():
            self.outcomes = [split[1].split(',') for split in self.text_file_parsed]
            self.outcomes = [Fraction(out) for outcome in self.outcomes for out in outcome] 
            self.outcomes =[self.outcomes[x:x+len(self.game.players)] for x in range(0, len(self.outcomes),len(self.game.players))]
            
            #get flattened outcomes for parsing
            flatten = itertools.chain.from_iterable
            self.flat_outs = list(flatten(self.outcomes))
            return self.outcomes,self.flat_outs
    
        payoffs()

        #reset the terminal nodes
        def reset_terminal_nodes():
            self.terminal_nodes = get_terminal_nodes()
            return self.terminal_nodes
    
        reset_terminal_nodes()
    
        #assign the payoffs at each terminal node
        def assign_payoffs():
            self.assigned_outcomes = []
            for i in range(len(self.outcomes)):
                for j in range(self.num_moves):
                    out = self.game.outcomes.add("{} chose {}".format(self.game.players[len(self.game.players)-1].label,j+1))
                    self.assigned_outcomes.append(out)
            for out, j in zip(self.assigned_outcomes, range(len(self.outcomes))):
                for k in range(self.num_players):
                    out[k] = self.outcomes[j][k]
            for node, out in zip(self.terminal_nodes, self.assigned_outcomes):
                for i in range(self.num_players):
                    node.outcome = out
            return self.assigned_outcomes, self.terminal_nodes
    
        assign_payoffs()
    
        #save the game to the efg format
        def save_game():
            self.efg = self.game.write('efg')
            self.game_file = open("{}-output.efg".format(self.game.title), "w")
            self.game_file.write(self.efg)
            self.game_file.close()
            return self.efg, self.game_file
        
        save_game()
        
        #runtime to build the game
        def game_time():
            self.game_time = time.time() 
            return self.game_time
        
        game_time()

        return self.start_Time, self.game.title, self.game.players, self.all_paths, self.flat_outs, self.assigned_outcomes, self.terminal_nodes, self.efg, self.game_file, self.game_time
    
    #solve the game
    def solve(self):
        
        #solve the game using the terminal
        def solve_external():
            # can take value "enumpureP"
            if self.solver == 'enumpureP':
                self.command = ['gambit-' +self.solver[:-1], '-P']
            else:
                sys.exit('unknown solver')
            self.command.append(self.game_file.name)
            self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.stdout, self.stderr = self.process.communicate()
            return self.stdout,self.command, self.process, self.stderr

        solve_external()

        #runtime to solve the game
        def solve_time():
            self.solve_time = time.time() 
            return self.solve_time
        
        solve_time()

        return self.stdout,self.command, self.process, self.stderr, self.solve_time

    #parse for the ideal output format
    def parse(self):
        
        #save the output
        def output_cleaner():
            self.output_text = open("{}-output.txt".format(self.game.title), "w")
            self.output_text.write(self.stdout)
            self.output_text.close()
            #read output as text into a dataframe
            self.outcome_df = pd.read_table("{}-output.txt".format(self.game.title), delim_whitespace=True, names=('Infoset','Action','Prob','Value', 'Final'))
            #parse the output
            self.stdout_strip = self.stdout.strip()
            self.output_cleaned = self.stdout_strip.split('NE,')[1:]
            self.output_cleaned  = [x.replace('\n', '') for x in self.output_cleaned]
            self.output_cleaned = [out.split(',') for out in self.output_cleaned]
            for i in range(len(self.output_cleaned)):
                self.output_cleaned[i][:] = [int(x) for x in self.output_cleaned[i]]
            return self.output_text, self.outcome_df, self.stdout_strip, self.output_cleaned
        
        output_cleaner()
        
        #redefine the infoset counter 
        def infosetter_output():
            self.num_infosets_out = 0
            for x in range(1,self.num_players):
                self.num_infosets_out += self.num_moves**x
            return self.num_infosets_out
        
        #create list of  probability dictionaries for each equilibria
        def prob_dict() :
            self.prob_dict = []
            for i in range(len(self.output_cleaned)) :
                mid_dict = {}
                for player in self.game.players:
                    mid_dict.update({player.label : self.output_cleaned[i][infosetter_output() :infosetter_output() + self.num_moves**int(player.label[-1])]})
                self.prob_dict.append(mid_dict)
            return self.prob_dict
        
        prob_dict()
    
        #create probability list
        def prob_list() :
            self.prob_list = []
            for prob in self.prob_dict:
                for key in sorted(prob.keys()):
                    for outcome, i in zip(prob[key], range(len(self.all_paths))):
                        self.prob_list.append(prob[key])
            self.prob_list = [list(x) for x in set(tuple(x) for x in self.prob_list)]
            self.prob_list.sort(key  = len)
            return self.prob_list
    
        prob_list()
    
        #create probability list by player
        def player_prob_list() :
            self.player_prob_list = []
            for prob in self.prob_dict :
                for key in sorted(prob.keys()):
                    prob_prelim = []
                    for pro in prob[key]:
                        prob_prelim.append(pro)
                    self.player_prob_list.append(prob_prelim)
            self.player_prob_list =[self.player_prob_list[x:x+len(self.game.players)] for x in range(0, len(self.player_prob_list),len(self.game.players))]
            return self.player_prob_list
    
        player_prob_list()

        #reshape player probabilities into arrays for multiplication
        def player_prob_arrays():
            self.player_prob_arrays = []
            for player in self.player_prob_list:
                for play in player:
                    self.player_prob_arrays.append(np.array(play).reshape(-1,1))
            self.player_prob_arrays =[self.player_prob_arrays[x:x+len(self.game.players)] for x in range(0, len(self.player_prob_arrays),len(self.game.players))]                        
            return self.player_prob_arrays

        player_prob_arrays()

        #create action list
        def action_list():
            self.action_list = []
            for prob in self.prob_dict:
                for key in sorted(prob.keys()):
                    for outcome, i in zip(prob[key], range(len(self.all_paths))):
                        self.action_list.append(int(self.terminal_nodes[i].prior_action.label))
            return self.action_list
    
        action_list()

        #create action dictionary
        def action_dict():
            self.action_dict = {}
            for player in self.game.players :
                if int(player.label[-1]) == 1:
                    self.action_dict.update({player.label : self.action_list[0: self.num_moves**(int(player.label[-1])-1) *(int(player.label[-1])-1)+ self.num_moves**int(player.label[-1])]})
                else:
                    self.action_dict.update({player.label : self.action_list[self.num_moves**(int(player.label[-1])-1): self.num_moves**(int(player.label[-1])-1) + self.num_moves**(int(player.label[-1]))]})                
            return self.action_dict
    
        action_dict()

        #create action list by the players
        def player_action_list():
            self.player_action_list = []
            for key in sorted(self.action_dict.keys()):
                self.action_prelim = []
                for action in self.action_dict[key]:
                    self.action_prelim.append(action)
                self.player_action_list.append(self.action_prelim)  
            return self.player_action_list
    
        player_action_list()

        #unpack each list
        def player_action_list_cleaned():
            self.player_action_list_cleaned = []
            for i in range(len(self.player_prob_arrays)):
                self.player_action_list_cleaned.append(self.player_action_list)
            return self.player_action_list_cleaned
        
        player_action_list_cleaned()
    
        #reshape list into arrays for multiplication
        def action_arrays():
            self.action_arrays = []
            for action in self.player_action_list_cleaned:
                for act in action:
                   self.action_arrays.append(np.array(act).reshape(-1,1))
            self.action_arrays =[self.action_arrays[x:x+len(self.game.players)] for x in range(0, len(self.action_arrays),len(self.game.players))]
            return self.action_arrays
    
        action_arrays()
    
        #get all the combinations of actions and probabilties that lead to equilibria
        def results():
            self.results =  np.multiply(self.player_prob_arrays, self.action_arrays)
            return self.results
        
        results()

        #convert the arrays of equilibria to lists
        def results_cleaned():
            self.results_cleaned = []
            for result in self.results:
                for res in result:
                    self.results_cleaned.append(res.tolist())
            return self.results_cleaned
    
        results_cleaned()

        #unpack the list of equilibria
        def results_unpacked():
            self.results_unpacked =[]
            for result in self.results_cleaned :
                self.results_unpacked.append([int(x) for [x] in result])
            self.results_unpacked =[self.results_unpacked[x:x+len(self.game.players)] for x in range(0, len(self.results_unpacked),len(self.game.players))]
            return self.results_unpacked
    
        results_unpacked()
                
        #condense the probability lists for each player
        def results_condensed():
            self.results_condensed  = []
            for res in self.results_unpacked:
                for i in range(len(res)):
                    rest = res[i]
                    rest =[rest[x:x+self.num_moves] for x in range(0, len(rest),self.num_moves)]
                    self.results_condensed .append(rest)
            self.results_condensed  = [self.results_condensed [x:x+len(self.game.players)] for x in range(0, len(self.results_condensed ),len(self.game.players))]
            return self.results_condensed
    
        results_condensed()

        #get the true equilibria
        def true_equilibria():
            flatten = itertools.chain.from_iterable     
            self.result_position = []
            self.result_move = []
            for i in range(len(self.results_condensed)):
                self.condensed = self.results_condensed[i]
                for j in range(len(self.condensed)):
                    if j == 0:
                        flat= list(flatten(self.condensed[j]))
                        for k in range(len(flat)):
                            if flat[k] != 0.0:
                                self.result_position.append((k))
                                self.result_move.append(flat[k])
                    else:
                        flat= list(flatten(self.condensed[j]))
                        self.condensed_list = self.condensed[j][self.result_position[-1]]
                        self.condensed_outcome = []
                        for condense in self.condensed_list :
                            if condense != 0.0:
                                self.condensed_outcome.append(condense)
                        for l in range(self.num_moves*self.result_position[-1],self.num_moves*self.result_position[-1]+self.num_moves):
                            if flat[l] != 0.0:
                             self.result_position.append((l))
                             self.result_move.append(flat[l])        
            self.result_move =  [self.result_move[x:x+len(self.game.players)] for x in range(0, len(self.result_move),len(self.game.players))]
            self.results_final = [tuple(x) for x in set(tuple(x) for x in self.result_move)]
            return self.result_move, self.results_final 
    
        true_equilibria()
    
        #make paths in to tuples to use as dictionary keys
        def paths_tuple():
            self.paths_tuple = [tuple(path) for path in self.all_paths]
            return self.paths_tuple
        
        paths_tuple()
    
        #create dictionary of the paths
        def payoff_dict():
            self.payoff_dict = {}
            for path, payoff in zip(self.paths_tuple, self.outcomes):
                self.payoff_dict.update({path:(payoff)})
            return self.payoff_dict
    
        payoff_dict()
    
        #create list of the payoffs
        def payoff_list():
            self.payoff_list = []
            for key in sorted(self.payoff_dict.keys()):
                self.pay_prelim = []
                for pay in self.payoff_dict[key]:
                    self.pay_prelim.append(pay)
                    self.payoff_list.append(self.pay_prelim)
            return self.payoff_list
    
        payoff_list()
                  
        #create action_payoff_list
        def action_payoff_list():
            self.action_payoff_list = []
            for action in self.results_final:
                if action in self.payoff_dict.keys():
                    self.action_payoff_list.append((action,self.payoff_dict[action]))
            return self.action_payoff_list
    
        action_payoff_list()
    
        #create the list of outcomes
        def outcome_list() :
            self.outcome_list = []
            for i in range(self.num_moves+1):
                for j in range(len(self.action_payoff_list)):
                    for act, pay in zip(self.action_payoff_list[j][0], self.action_payoff_list[j][1]):
                        self.outcome_list.append('{} : {}'.format(act,round(float(pay),1)))
            self.outcome_list = [self.outcome_list[x:x+len(self.game.players)] for x in range(0, len(self.outcome_list),len(self.game.players))]
            self.outcome_list = [list(x) for x in set(tuple(x) for x in self.outcome_list)]
            return self.outcome_list

        outcome_list()
        
        #runtime to parse the game
        def parse_time():
            self.parse_time = time.time()
            return self.parse_time
        
        parse_time()

        #print all info
        def output_printer():
        #check runtime to build the game
            print('')
            print(self.efg)
            for outcome in self.outcome_list:
                for out, i in zip(outcome, range(len(self.outcome_list[0])*len(self.outcome_list))):
                    if (i + 1) % (len(self.game.players)) == 0:
                        print('Player {} chose {}'.format(i+1,out))
                        logging.info('Player {} chose {}'.format(i+1,out))
                        print('')
                    else:
                        print('Player {} chose {}'.format(i+1,out))
                        logging.info('Player {} chose {}'.format(i+1,out))
        output_printer()

        return self.output_text, self.outcome_df, self.stdout_strip, self.output_cleaned, self.prob_dict, self.prob_list, self.player_prob_list, self.player_prob_arrays, self.action_list, self.action_dict, self.player_action_list, self.player_action_list_cleaned, self.action_arrays, self.results, self.results_cleaned, self.results_unpacked, self.results_condensed, self.result_move, self.results_final , self.paths_tuple, self.payoff_dict, self.payoff_list, self.action_payoff_list, self.outcome_list, self.parse_time
