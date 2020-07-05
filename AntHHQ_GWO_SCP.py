from Github import pushGithub

from Problem.util import read_instance as Instance
from Problem import SCP
from pathlib import Path
from os import path as pathcheck

import numpy as np
import time
np.seterr(divide='ignore', invalid='ignore')


from MachineLearning import QLearning

class AntHH():
    '''
    ************************+*********   Parámetros *************************************
    # alfa: control relativo de rastro de feromona
    # beta: control relativo de visibilidad
    # p: factor de evaporación feromona.
    # ti: feromona item i hormiga k
    # delta Tik: { G(Lk): si item i es agregado, 0 en otro caso } .
    # G(Lk): En Minimización: Q/Lk, En Maximización Q*Lk, donde Lk = fitness. Q = parámetro
    # Q: 1/sum.i(valor aportado por item i), parametro para  los item.
    # iteraciones: máximo de iteraciones.
    # ants: cantidad de hormigas
    '''

    def __init__(self,instancia,resultado,ants,lobos,iterMax,run,ql_alfa,ql_gamma):

        self.run = run

        #ACO
        self.ants = ants
        self.iterMax = iterMax
        self.maxSteps = 1
        self.evaporacion = 0.3
        self.alfa = 1
        self.beta = 5

        #QL
        self.ql_alfa = ql_alfa
        self.ql_gamma = ql_gamma


        #instancia
        self.rootdir = str(Path().cwd()) + '/'
        pathInstance = self.rootdir + 'Problem/Instances/SCP/'
        self.repo = 'MagisterMHML'
        self.resultado = resultado
        self.instancia = instancia


        if not pathcheck.exists(pathInstance + instancia):
            print("No se encontró la instancia: " + pathInstance + self.instancia)
            return False

        instance = Instance.Read(pathInstance + self.instancia)
        self.matrizCobertura = np.array(instance.get_r())
        self.vectorCostos = np.array(instance.get_c())

        f = open(self.rootdir + self.resultado, 'w')
        linea = 'problem|solver|instance|population|run|iter|ds|metric|executionTime|ant_population|ql_alpha|ql_gamma'
        f.write(linea)
        f.write('\n')
        f.close();

        # GWO
        self.dim = len(self.vectorCostos)
        self.Lobos = lobos

        self.Alpha_pos = np.zeros(self.dim )
        self.Alpha_score = float("inf")

        self.Beta_pos = np.zeros(self.dim )
        self.Beta_score = float("inf")

        self.Delta_pos = np.zeros(self.dim )
        self.Delta_score = float("inf")

        # Posicion inicial de lobos
        self.posLobos = np.zeros((self.Lobos, self.dim ))
        for i in range(self.dim ):
            self.posLobos[:, i] = np.random.uniform(0, 1, self.Lobos)


        #acciones a escoger

        transferFunction = ['V1', 'V2', 'V3', 'V4', 'S1', 'S2', 'S3', 'S4']
        operatorBinarization = ['Standard']

        self.Metric_k = [np.inf]*self.ants
        self.DS_actions = [tf + "," + ob for tf in transferFunction for ob in operatorBinarization]

        self.Prob_tkx = np.ones(shape=(self.iterMax, self.ants,len(self.DS_actions)), dtype=np.float64)
        self.Phe_x = np.ones(shape=(len(self.DS_actions)), dtype=np.float64)

        #Variable decision hormiga
        self.X_tk = np.zeros(shape=(self.iterMax,self.ants, len(self.DS_actions)), dtype=np.int)

        self.bestMetric = np.inf

    def HH(self):

        qualityMetric = 0
        agente = QLearning.QAgent(self.ql_alfa, self.ql_gamma, self.DS_actions, self.iterMax)
        agente.Qvalues[0] = np.random.randint(0,len(self.DS_actions))
        esquema = np.random.randint(0,len(self.DS_actions))

        for iter in range(0,self.iterMax):

            agente.Qnuevo(qualityMetric, esquema, iter)
            Qvalues = agente.Qvalues

            action = agente.getAccion(iter)
            agente.Qnuevo(qualityMetric, action, iter)

            #print(Qvalues[iter])

            #print("----------- iter "+str(iter)+" -----------------------")

            timerStart = time.time()

            for ant in range(0,self.ants):

                #Update pheromona
                self.Pheromona(agente.Qvalues[iter])

                #Seleccion esquema segun Probs
                esquema = self.seleccionRuleta(iter,ant)

                #QLearning
                action = agente.getAccion(iter)
                agente.Qnuevo(qualityMetric, action, iter)

                #print(agente.Qvalues[iter])

                ############################### GWO #######################################################

                for lobo in range(0, self.Lobos):

                    # F.O por cada lobo
                    self.posLobos[lobo, :], fitness = SCP.SCP(self.posLobos[lobo, :], self.vectorCostos, self.matrizCobertura, self.DS_actions[esquema])

                    # Actualizamos alpha,beta, delta
                    if fitness < self.Alpha_score:
                        self.Alpha_score = fitness;
                        self.Alpha_pos = self.posLobos[lobo, :].copy()

                    if (fitness > self.Alpha_score and fitness < self.Beta_score):
                        self.Beta_score = fitness
                        self.Beta_pos = self.posLobos[lobo, :].copy()

                    if (fitness > self.Alpha_score and fitness > self.Beta_score and fitness < self.Delta_score):
                        self.Delta_score = fitness
                        self.Delta_pos = self.posLobos[lobo, :].copy()

                    # parametro linealmente decreciente  2->0
                a = 2 - iter * ((2) / self.iterMax);

                # Lobos
                for lobo in range(0, self.Lobos):
                    for j in range(0, self.dim):
                        r1 = np.random.uniform(0, 1)  # random [0,1]
                        r2 = np.random.uniform(0, 1)  # random [0,1]

                        A1 = 2 * a * r1 - a;  # Equation (3.3)
                        C1 = 2 * r2;  # Equation (3.4)

                        D_alpha = abs(C1 * self.Alpha_pos[j] - self.posLobos[lobo, j]);
                        X1 = self.Alpha_pos[j] - A1 * D_alpha;

                        r1 = np.random.uniform(0, 1)  # random [0,1]
                        r2 = np.random.uniform(0, 1)  # random [0,1]

                        A2 = 2 * a * r1 - a;
                        C2 = 2 * r2;

                        D_beta = abs(C2 * self.Beta_pos[j] - self.posLobos[lobo, j]);
                        X2 = self.Beta_pos[j] - A2 * D_beta;

                        r1 = np.random.uniform(0, 1)  # random [0,1]
                        r2 = np.random.uniform(0, 1)  # random [0,1]

                        A3 = 2 * a * r1 - a;
                        C3 = 2 * r2;

                        D_delta = abs(C3 * self.Delta_pos[j] - self.posLobos[lobo, j]);
                        X3 = self.Delta_pos[j] - A3 * D_delta;

                        self.posLobos[lobo, j] = (X1 + X2 + X3) / 3

                #solucion_bin, fitness = SCP.SCP(solucion_random, self.vectorCostos, self.matrizCobertura, self.DS_actions[esquema])

                if self.Metric_k[ant] > self.Alpha_score:
                    self.Metric_k[ant] = self.Alpha_score
                    self.X_tk[iter][ant][esquema] = 1


                if self.Alpha_score < self.bestMetric:
                    self.bestMetric = self.Alpha_score

                qualityMetric = self.Alpha_score

            timeEnd = time.time()
            execution = round(timeEnd - timerStart, 2)

            linea_r = "SCP|AntHHQ-GWO|" \
                      + str(self.instancia) + "|" \
                      + str(self.Lobos) + "|" \
                      + str(self.run) + "|" \
                      + str(iter) + "|" \
                      + str(self.DS_actions[esquema]) + "|" \
                      + str(self.bestMetric) + "|" \
                      + str(execution)+ "|" \
                      + str(self.ants)+ "|" \
                      + str(self.ql_alfa) + "|" \
                      + str(self.ql_gamma)

            if iter % 100 == 0:
                print(linea_r)

            f = open(self.rootdir + self.resultado, 'a')
            f.write(linea_r)
            f.write('\n')
            f.close();

        try:
            pushGithub.pushGithub(self.repo, self.resultado, 'Resultado final corrida ' + str(self.run))
        except:
            print("No se logró hacer push a github")

        return True

    #por definir o dejar en n=1
    def infoHeuristica(self):

        return 1


    def seleccionRuleta(self,iter,ant):


        random = np.random.uniform(0,2)

        probs = self.Probabilidad(iter,ant)

        selected = 0
        for i, prob in enumerate(probs):
            random -= prob
            if random <= 0:
                selected = i
                break

        return selected


    def Probabilidad(self,iter,ant):

        heuristica = self.infoHeuristica()

        # DENOMINADOR
        prob_sum = 0
        for ds in range(len(self.X_tk[iter][ant])):  # [0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 ]
            prob_sum +=  (self.Phe_x[ds] ** self.alfa) * (heuristica ** self.beta)

        for ds in range(len(self.X_tk[iter][ant])):
            self.Prob_tkx[iter][ant][ds] = np.divide(((self.Phe_x[ds] ** self.alfa) * (heuristica ** self.beta)), prob_sum)

        return self.Prob_tkx[iter][ant]


    def Pheromona(self,Qnuevo_t):

        self.Phe_x = Qnuevo_t

        return True



import sys

print("AntHHQ-GWO, configurando ...")

if len(sys.argv[1:]) != 9:
    print("Ingrese todos los argumentos: ruta_instancia,ruta_resultados,lobos_poblacion,iteraciones,corridas_start,corridas_end,ants_poblacion,ql_alfa,ql_gamma")

else :

    print ("Instancia %s" % (sys.argv[1]))
    print ("Resultados %s" % (sys.argv[2]))
    print ("Poblacion %s" % (sys.argv[3]))
    print ("Iteraciones %s" % (sys.argv[4]))
    print ("Corridas_start %s" % (sys.argv[5]))
    print ("Corridas_end %s" % (sys.argv[6]))
    print ("Ant_poblacion %s" % (sys.argv[7]))
    print ("QL_alfa %s" % (sys.argv[8]))
    print ("QL_gamma %s" % (sys.argv[9]))


    if not sys.argv[3].isnumeric():

        print("Poblacion no es numérico")

    elif not sys.argv[4].isnumeric() :

        print("Iteraciones no es numérico")

    elif not sys.argv[5].isnumeric():

        print("Corridas_start no es numérico")

    elif not sys.argv[6].isnumeric():

        print("Corridas_end no es numérico")

    elif not sys.argv[7].isnumeric():

        print("Ant_Poblacion no es numérico")

    elif not isinstance(float(sys.argv[8]), float):

        print("QL_alpha  no es numérico")

    elif not isinstance(float(sys.argv[9]), float):

        print("QL_gamma no es numérico")

    else :
        print("Iterando...")

        for run in range(int(sys.argv[5]),int(sys.argv[6])+1):
            # instancia,resultado,ants,lobos,iterMax,run):
            ACO = AntHH(sys.argv[1],sys.argv[2], int(sys.argv[7]), int(sys.argv[3]), int(sys.argv[4]),run,float(sys.argv[7]),float(sys.argv[8]))

            ACO.HH()

        print("Finalizamos.")








