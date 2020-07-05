# -*- coding: utf-8 -*-
#  Author: Diego Tapia R.
#  E-mail: root.chile@gmail.com - diego.tapia.r@mail.pucv.cl

########################################### EJECUCIÓN  #########################################################
# python GWO_SCP.py instancia (string)
#                   resultados(string)
#                   poblacion (int)
#                   iteraciones (int)
#                   corrida_start (int)
#                   corrida_end (int)
#                   ql_apha (float)
#                   ql_gamma (float)
###############################################################################################################


from Github import pushGithub


from Problem.util import read_instance as Instance
from Problem import SCP
from pathlib import Path

from os import path as pathcheck

import numpy as np
import time

from MachineLearning import QLearning


def LoboGris_SCP(instancia,resultado,lobos,maxIter,run_start,run_end,QL_alpha,QL_gamma):

    rootdir = str(Path().cwd())+'/'

    pathInstance = rootdir+'Problem/Instances/SCP/'
    repo = 'MagisterMHML'

    if not pathcheck.exists(pathInstance+instancia):
        print("No se encontró la instancia: " + pathInstance+instancia)
        return False

    instance = Instance.Read(pathInstance+instancia)

    matrizCobertura = np.array(instance.get_r())
    vectorCostos = np.array(instance.get_c())

    dim = len(vectorCostos)
    Lobos = lobos
    maxIter = maxIter


    # Main loop

    f = open(rootdir+resultado, 'w')
    linea = 'problem|solver|instance|population|run|iter|ds|metric|executionTime|QL_alpha|QL_gamma'
    f.write(linea)
    f.write('\n')
    f.close();

    for run in range(run_start,run_end+1):

        #alpha, beta, and delta_pos
        Alpha_pos = np.zeros(dim)
        Alpha_score = float("inf")

        Beta_pos = np.zeros(dim)
        Beta_score = float("inf")

        Delta_pos = np.zeros(dim)
        Delta_score = float("inf")

        # iniciamos poblacion
        posLobos = np.zeros((Lobos, dim))
        for i in range(dim):
            posLobos[:, i] = np.random.uniform(0, 1, Lobos)

        convergencia = np.zeros(maxIter)


        #QLEARNING DECISION

        transferFunction = ['V1', 'V2', 'V3', 'V4', 'S1', 'S2', 'S3', 'S4']
        operatorBinarization = ['Standard']

        DS_actions = [tf + "," + ob for tf in transferFunction for ob in operatorBinarization]

        qualityMetric = 0
        agente = QLearning.QAgent(QL_alpha, QL_gamma, DS_actions, maxIter)
        actionDS = agente.getAccion(0)

        for iter in range(0, maxIter):

            timerStart = time.time()

            # Seleccion de Esquema desde DS
            if iter > 0:
                agente.Qnuevo(qualityMetric, actionDS, iter)
                actionDS = agente.getAccion(iter)

            for lobo in range(0, Lobos):

                # F.O por cada lobo
                posLobos[lobo, :], fitness = SCP.SCP(posLobos[lobo,:],vectorCostos,matrizCobertura,DS_actions[actionDS])

                # Actualizamos alpha,beta, delta
                if fitness < Alpha_score:
                    Alpha_score = fitness;
                    Alpha_pos = posLobos[lobo, :].copy()

                if (fitness > Alpha_score and fitness < Beta_score):
                    Beta_score = fitness
                    Beta_pos = posLobos[lobo, :].copy()

                if (fitness > Alpha_score and fitness > Beta_score and fitness < Delta_score):
                    Delta_score = fitness
                    Delta_pos = posLobos[lobo, :].copy()

            #parametro linealmente decreciente  2->0
            a = 2 - iter * ((2) / maxIter);

            # Lobos
            for lobo in range(0, Lobos):
                for j in range(0, dim):
                    r1 = np.random.uniform(0,1) #random [0,1]
                    r2 = np.random.uniform(0,1) #random [0,1]

                    A1 = 2 * a * r1 - a;  # Equation (3.3)
                    C1 = 2 * r2;  # Equation (3.4)

                    D_alpha = abs(C1 * Alpha_pos[j] - posLobos[lobo, j]);
                    X1 = Alpha_pos[j] - A1 * D_alpha;

                    r1 = np.random.uniform(0, 1)  # random [0,1]
                    r2 = np.random.uniform(0, 1)  # random [0,1]

                    A2 = 2 * a * r1 - a;
                    C2 = 2 * r2;

                    D_beta = abs(C2 * Beta_pos[j] - posLobos[lobo, j]);
                    X2 = Beta_pos[j] - A2 * D_beta;

                    r1 = np.random.uniform(0, 1)  # random [0,1]
                    r2 = np.random.uniform(0, 1)  # random [0,1]

                    A3 = 2 * a * r1 - a;
                    C3 = 2 * r2;

                    D_delta = abs(C3 * Delta_pos[j] - posLobos[lobo, j]);
                    X3 = Delta_pos[j] - A3 * D_delta;

                    posLobos[lobo, j] = (X1 + X2 + X3) / 3

            timeEnd = time.time()
            execution = round(timeEnd - timerStart,2)

            linea_r = "SCP|GWO-Q|" \
                      + str(instancia) + "|" \
                      + str(len(posLobos)) + "|" \
                      + str(run) + "|" \
                      + str(iter) + "|" \
                      + str(DS_actions[actionDS]) + "|" \
                      + str(Alpha_score) + "|" \
                      + str(execution) + "|" \
                      + str(QL_alpha) + "|" \
                      + str(QL_gamma)

            #update Metrica calidad
            qualityMetric = Alpha_score

            if iter % 100 == 0:
                print(linea_r)

            f = open(rootdir+resultado, 'a')
            f.write(linea_r)
            f.write('\n')
            f.close();

            '''
            #Push a Github cada 500 iteraciones
            if iter%500 == 0:
                try:
                    pushGithub.pushGithub(repo,resultado,'Resultado intermedio iteración '+str(iter)+' corrida '+str(run))
                except:
                    print("No se hizo push")
            '''

            convergencia[iter] = Alpha_score;

        try:
            pushGithub.pushGithub(repo,resultado, 'Resultado final corrida '+str(run)+' de '+str(run_end))
        except:
            print("Error al hacer push")


    return convergencia

#%%


import sys

print("Lobo Gris, configurando ...")

if len(sys.argv[1:]) != 8:
    print("Ingrese todos los argumentos: ruta_instancia,ruta_resultados,poblacion,iteraciones,corrida_start,corrida_end,QL_alpha,QL_gamma")

else :

    print ("Instancia %s" % (sys.argv[1]))
    print ("Resultados %s" % (sys.argv[2]))
    print ("Poblacion %s" % (sys.argv[3]))
    print ("Iteraciones %s" % (sys.argv[4]))
    print("Corridas_start %s" % (sys.argv[5]))
    print("Corridas_end %s" % (sys.argv[6]))

    print("--- Qlearning parametros ----")

    print("Alfa %s" % (sys.argv[7]))
    print("Gamma %s" % (sys.argv[8]))


    #Validamos argumentos


    if not sys.argv[3].isnumeric():

        print("Poblacion no es numérico")

    elif not sys.argv[4].isnumeric() :

        print("Iteraciones no es numérico")

    elif not sys.argv[5].isnumeric():

        print("Corridas_start no es numérico")

    elif not sys.argv[6].isnumeric():

        print("Corridas_end no es numérico")

    elif not isinstance(float(sys.argv[7]), float):

        print("QL_alpha  no es numérico")

    elif not isinstance(float(sys.argv[8]), float):

        print("QL_gamma no es numérico")

    else :
        print("Iterando...")

        LoboConvergencia = LoboGris_SCP(sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),float(sys.argv[7]),float(sys.argv[8]))

        print("Finalizamos.")