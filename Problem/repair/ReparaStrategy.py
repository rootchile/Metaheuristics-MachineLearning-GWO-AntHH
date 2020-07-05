#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 23:00:31 2019

@author: mauri
"""

# import readOrProblems as rOP
from . import solution as sl
from . import heuristic as he
import random
import numpy as np


class ReparaStrategy:

    def __init__(self, matrix, pesos, row, cols):

        #        pesos, matrix = rOP.generaMatrix(instanceFile) #Se generan los pesos y la matrix desde la instancia a ejecutar
        matrix = np.array(matrix)
        #        print(matrix.shape)
        #        exit()
        self.rows = row
        self.cols = cols
        self.pesos = np.array(pesos)
        self.matrix = matrix
        self.rHeuristic = he.getRowHeuristics(matrix)
        self.dictCol = he.getColumnRow(matrix)
        #        row, cols = matrix.shape #Se extrae el tamaño del problema
        self.dictcHeuristics = {}
        self.cHeuristic = []
        self.lSolution = []
        self.dict = he.getRowColumn(matrix)

    def repara_one(self, solution):
        #return self.reparaSimple(solution)
        return self.repara(solution)

    def repara(self, solution):
        #        print(f'solution {len(solution)}')
        lSolution = [i for i in range(len(solution)) if solution[i] == 1]
        #        print(f'lSolution {len(lSolution)}')
        #        exit()
        lSolution, numReparaciones = sl.generaSolucion(lSolution, self.matrix, self.pesos, self.rHeuristic,
                                                       self.dictcHeuristics, self.dict, self.cHeuristic, self.dictCol)
        sol = np.zeros(self.cols, dtype=np.float)
        sol[lSolution] = 1
        return sol.tolist(), numReparaciones

    def reparaSimple(self, solution):
        numRep = 0
        indices = list(range(self.rows))
        random.shuffle(indices)
        for i in indices:
            if np.sum(self.matrix[i] * solution) < 1:
                idxRestriccion = np.argwhere((self.matrix[i]) > 0)
                idxMenorPeso = idxRestriccion[np.argmin(self.pesos[idxRestriccion])]
                solution[idxMenorPeso[0]] = 1
                numRep += 1
        return solution, numRep

    def cumple(self, solucion):
        for i in range(self.rows):
            if np.sum(self.matrix[i] * solucion) < 1: return 0
        return 1