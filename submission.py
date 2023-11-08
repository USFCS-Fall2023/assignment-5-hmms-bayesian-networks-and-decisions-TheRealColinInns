import os

import HMM

if __name__=="__main__":
    model = HMM.HMM()
    model.load("partofspeech.browntags.trained")
    states, values = model.generate(10)
    print(states)
    print(values)
    test_results = []
    observed = []
    with open("ambiguous_sents.obs") as observations:
        for observation in observations:
            if observation != '\n':
                print("Final State Aprox for (" + observation.strip() + ") is |" + str(model.forwarding(observation.split())) + "|")
    with open("ambiguous_sents.obs") as observations:
        for observation in observations:
            if observation != '\n':
                observed.append(observation.strip())
                result = " ".join(model.viterbi(observation.split()))
                test_results.append(result)
                print("Observation: " + observation.strip())
                print("Result: " + result)
    exec(open('alarm.py').read())
    exec(open('carnet.py').read())



