# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Multi-layer perceptron
# Version d'origine:
# Copyright (C) 2011  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License.
# Modifié par B. Lamiroy
# -----------------------------------------------------------------------------
# This is an implementation of the multi-layer perceptron with retropropagation
# learning.
# -----------------------------------------------------------------------------
import numpy as np
import perceptron as mlp


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import matplotlib
    import matplotlib.pyplot as plt

    def learn(network,samples, epochs=2500, vitesse=.1, inertie=0.1):
        # Train 
        for i in range(epochs):
            n = np.random.randint(samples.size)
            network.propagation( samples['input'][n] )
            network.retropropagation( samples['output'][n], vitesse, inertie )
        # Test
        for i in range(samples.size):
            o = network.propagation( samples['input'][i] )
            print ((i, samples['input'][i], '%.2f' % o[0]))
            print ('(expected %.2f)' % samples['output'][i])
        print

    network = mlp.Perceptron(2,2,1)
    samples = np.zeros(4, dtype=[('input',  float, 2), ('output', float, 1)])

    # Example 1 : OR logical function
    # -------------------------------------------------------------------------
    print ("Learning the OR logical function")
    network.reset()
    samples[0] = (0,0), 0
    samples[1] = (1,0), 1
    samples[2] = (0,1), 1
    samples[3] = (1,1), 1
    learn(network, samples)

    # Example 2 : AND logical function
    # -------------------------------------------------------------------------
    print ("Learning the AND logical function")
    network.reset()
    samples[0] = (0,0), 0
    samples[1] = (1,0), 0
    samples[2] = (0,1), 0
    samples[3] = (1,1), 1
    learn(network, samples)

    # Example 3 : XOR logical function
    # -------------------------------------------------------------------------
    print ("Learning the XOR logical function")
    network.reset()
    samples[0] = (0,0), 0
    samples[1] = (1,0), 1
    samples[2] = (0,1), 1
    samples[3] = (1,1), 0
    learn(network, samples)