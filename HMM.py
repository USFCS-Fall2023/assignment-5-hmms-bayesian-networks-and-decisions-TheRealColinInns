

import random
import numpy as np
import argparse
import codecs
import os
import numpy

# observations
class Observation:
    def __init__(self, stateseq, outputseq):
        self.stateseq  = stateseq   # sequence of states
        self.outputseq = outputseq  # sequence of outputs
    def __str__(self):
        return ' '.join(self.stateseq)+'\n'+' '.join(self.outputseq)+'\n'
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.outputseq)

# hmm model
class HMM:
    def __init__(self, transitions={}, emissions={}):
        """creates a model from transition and emission probabilities"""
        ## Both of these are dictionaries of dictionaries. e.g. :
        # {'#': {'C': 0.814506898514, 'V': 0.185493101486},
        #  'C': {'C': 0.625840873591, 'V': 0.374159126409},
        #  'V': {'C': 0.603126993184, 'V': 0.396873006816}}

        self.transitions = transitions
        self.emissions = emissions

    ## part 1 - you do this.
    def load(self, basename):
        with open(basename + ".emit") as emit_file:
            self.emissions = load_helper(emit_file)
        with open(basename + ".trans") as trans_file:
            self.transitions = load_helper(trans_file)



   ## you do this.
    def generate(self, n):
        curr_state = '#'
        curr_value = ''
        states = []
        values = []
        for i in range(n):
            next_states = []
            state_weights = []
            for next_state in self.transitions[curr_state]:
                next_states.append(next_state)
                state_weights.append(self.transitions[curr_state][next_state])
            curr_state = random.choices(next_states, weights=state_weights, k=1)[0]
            states.append(curr_state)
            next_values = []
            value_weights = []
            for next_value in self.emissions[curr_state]:
                next_values.append(next_value)
                value_weights.append(self.emissions[curr_state][next_value])
            curr_value = random.choices(next_values, weights=value_weights, k=1)[0]
            values.append(curr_value)
        return states, values

    def forwarding(self, obs):
        m = matrix_gen(self.transitions, self.emissions, obs)
        curr_max = -1
        curr_state = "N/A"
        for state, weight in m[(len(obs) - 1)].items():
            if weight > curr_max:
                curr_state = state
                curr_max = weight
        return curr_state






    ## you do this: Implement the Viterbi alborithm. Given an Observation (a list of outputs or emissions)
    ## determine the most likely sequence of states.

    def viterbi(self, observation):
        m = matrix_gen(self.transitions, self.emissions, observation)
        state_path = []
        for i in range(len(observation)):
            curr_max = -1
            curr_state = "N/A"
            for state, weight in m[i].items():
                if weight > curr_max:
                    curr_state = state
                    curr_max = weight
            state_path.append(curr_state)
        return state_path


def load_helper(file):
    dic = {}
    for line in file:
        tok = line.split()
        if dic.keys().__contains__(tok[0]):
            dic[tok[0]][tok[1]] = float(tok[2])
        else:
            dic[tok[0]] = {}
            dic[tok[0]][tok[1]] = float(tok[2])
    return dic


def matrix_gen(transitions, emissions, obs):
    state_values = emissions.keys()
    m = {0: {}}
    for s in state_values:
        if emissions[s].keys().__contains__(obs[0]):
            m[0][s] = transitions['#'][s] * emissions[s][obs[0]]
        else:
            m[0][s] = 0
    for i in range(1, len(obs)):
        m[i] = {}
        curr_sum = {}
        for prev_state in state_values:
            for next_state in state_values:
                if emissions[next_state].__contains__(obs[i]):
                    if curr_sum.__contains__(next_state):
                        curr_sum[next_state] += m[i - 1][prev_state] * transitions[prev_state][next_state] * \
                                                emissions[next_state][obs[i]]
                    else:
                        curr_sum[next_state] = m[i - 1][prev_state] * transitions[prev_state][next_state] * \
                                               emissions[next_state][obs[i]]
                else:
                    if curr_sum.__contains__(next_state):
                        curr_sum[next_state] += 0
                    else:
                        curr_sum[next_state] = 0
        for state_sum in curr_sum:
            m[i][state_sum] = curr_sum[state_sum]
    return m
