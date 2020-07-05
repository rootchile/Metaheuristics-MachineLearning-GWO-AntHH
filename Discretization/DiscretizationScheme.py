#  Author: Diego Tapia R.
#  E-mail: root.chile@gmail.com - diego.tapia.r@mail.pucv.cl

import numpy as np
import math

class DiscretizationScheme:

    def __init__(self, solution,transferFunction, binarizationOperator):

        self.solution = solution #numpy array
        self.transferFunction = transferFunction
        self.binarizationOperator = binarizationOperator

        #output
        self.probs = np.zeros(shape=len(self.solution))
        self.solution_int = np.zeros(shape=len(self.solution))



    #Funciones de Transferencia


    def T_V1(self):

        for i in range(len(self.solution)):
            self.probs[i] = math.fabs(math.erf((math.sqrt(math.pi)/2)*self.solution[i]))

        return self.probs


    def T_V2(self):

        for i in range(len(self.solution)):
            self.probs[i] = abs(np.tanh(self.solution[i]))

        return self.probs

    def T_V3(self):

        for i in range(len(self.solution)):
            self.probs[i] = math.fabs(self.solution[i]/math.sqrt(1+(self.solution[i]**2)))

        return self.probs

    def T_V4(self):

        for i in range(len(self.solution)):
            self.probs[i] = math.fabs((2/math.pi)*math.atan((math.pi/2)*self.solution[i]))

        return self.probs

    def T_S1(self):

        for i in range(len(self.solution)):
            self.probs[i] = 1 / (1 + math.exp(-2 * self.solution[i]))

        return self.probs

    def T_S2(self):

        for i in range(len(self.solution)):
            self.probs[i] = 1/(1+math.exp(-1*self.solution[i]))

        return self.probs


    def T_S3(self):

        for i in range(len(self.solution)):
            self.probs[i] = 1/(1+math.exp(-1*self.solution[i]/2))

        return self.probs


    def T_S4(self):

        for i in range(len(self.solution)):
            self.probs[i] = 1 / (1 + math.exp(-1 * self.solution[i] / 3))

        return self.probs



    #Binarization

    def B_Standard(self):

        for i in range(len(self.solution)):

            rand = np.random.uniform(0, 1)

            if rand < self.probs[i]:
                self.solution_int[i] = 1
            else:
                self.solution_int[i] = 0

        return self.solution_int


    def binariza(self):

        if self.transferFunction == 'V1':
            self.T_V1()

        if self.transferFunction == 'V2':
            self.T_V2()

        if self.transferFunction == 'V3':
            self.T_V3()

        if self.transferFunction == 'V4':
            self.T_V4()

        if self.transferFunction == 'S1':
            self.T_S1()

        if self.transferFunction == 'S2':
            self.T_S2()

        if self.transferFunction == 'S3':
            self.T_S3()

        if self.transferFunction == 'S4':
            self.T_S4()

        if self.binarizationOperator == 'Standard':
            self.B_Standard()

        return self.solution_int
