# ------- BIBLIOTECAS  -------
import matplotlib.pyplot as plt
import random
import math
import numpy as np

# ------- DEFINIÇÃO DAS FUNÇÕES  -------
def imprime_crit():
  print("\n"*10) 
  print('*************** TOPSIS ****************')
  print('*                                     *')
  print('* Digite o nome do critério           *') 
  print('*                                     *') 
  print('* Digite (n), caso não deseje inserir *')   
  print('* mais critérios                      *')
  print('*                                     *')  
  print('***************************************')


def imprime_alt():
  print("\n"*10) 
  print('*************** TOPSIS ****************')
  print('*                                     *')
  print('* Digite uma alternativa              *') 
  print('*                                     *') 
  print('* Digite (n), caso não deseje inserir *')   
  print('* mais alternativas                   *')
  print('*                                     *')  
  print('***************************************')



def round_down(n, decimals=0):
  multiplier = 10 ** decimals
  return math.floor(n * multiplier) / multiplier

def round_up(n, decimals=0):
  multiplier = 10 ** decimals
  return math.ceil(n * multiplier) / multiplier

def pula_linhas():
  print("\n"*10)

# ------- DEFINIÇÃO DAS CLASSES  -------
class TOPSIS(object):

  def __init__(self, matriz, matriz_norm, matriz_norm_polar, matriz_crit, array_peso_crit, array_alt, 
               sol_ideal_pos, sol_ideal_neg, array_dist_pos, array_dist_neg, array_proximidade_relat, num_crit, num_alt):
    self.matriz = matriz
    self.matriz_norm = matriz_norm
    self.matriz_norm_polar = matriz_norm_polar
    self.matriz_crit = matriz_crit
    self.array_peso_crit = array_peso_crit
    self.array_alt = array_alt
    self.sol_ideal_pos = sol_ideal_pos
    self.sol_ideal_neg = sol_ideal_neg
    self.array_dist_pos = array_dist_pos
    self.array_dist_neg = array_dist_neg
    self.array_proximidade_relat = array_proximidade_relat
    self.num_crit = num_crit
    self.num_alt = num_alt
    
  def define_matriz(self):
    array_crit = list([])
    array_minoumax = list([])

    "Determina os critérios e seu número"
    imprime_crit()
    criterio = input()
    while(criterio != "n"):
      array_crit.append(criterio)
      self.num_crit = self.num_crit + 1
      tipo = ""
      while(tipo!="min" and tipo!="max"):
        pula_linhas()
        tipo = input("O Critério " + criterio + " é maximizador (max) ou minimizador (min)? ")
        if (tipo!="max" and tipo!="min"):
          print("\n Erro, digite min ou max para determinar característica do critério. \n")
      array_minoumax.append(tipo)
      imprime_crit()
      criterio = input()
    
    array_crit = np.array(array_crit)
    array_minoumax = np.array(array_minoumax)

    "Insere as alternativas e seu número"
    imprime_alt()
    alternativa = input()
    while(alternativa != "n"):
      imprime_alt()
      self.array_alt.append(alternativa)
      self.num_alt = self.num_alt + 1
      alternativa = input()
    self.array_alt = np.array(self.array_alt)

    #cria matrizes
    self.matriz = np.ones([self.num_alt,self.num_crit], float)
    self.matriz_norm = np.ones([self.num_alt,self.num_crit], float)
    self.matriz_norm_polar = np.ones([self.num_alt,self.num_crit], float)

    
    self.matriz_crit.append(array_crit)
    self.matriz_crit.append(array_minoumax)

    self.matriz_crit = np.array(self.matriz_crit)
    #self.matriz_crit = np.transpose(self.matriz_crit)
      

  def preenche_matriz(self):
    "Determina valores dos critérios, dados as alternativas"
    print("\n"*9) 
    for i in range (0, self.num_alt):
      print("\n")
      for j in range (0, self.num_crit):
        self.matriz[i][j] = float(input("Digite o valor atribuido para o alternativa " + self.array_alt[i] + " (critério: " + self.matriz_crit[0][j] + ") " ))

  def normaliza_matriz(self):
    "Normaliza matriz inicial - somatorio é das colunas"
    soma = 0
    for i in range(0, self.num_alt):
      for j in range(0, self.num_crit):
        soma = np.sum(self.matriz[:,j]**2, axis=0)
        self.matriz_norm[i][j] = (self.matriz[i][j])/math.sqrt(soma)
  
  
  def atribui_pesos(self):
    soma = 0
    while(soma!=100):
      for i in range(0, self.num_crit):
        peso = float(input("Digite o valor decimal do peso do critério " + self.matriz_crit[0][i] + ": "))
        self.array_peso_crit.append(peso)
        soma = soma + peso
      soma = soma*100

      if(soma!=100):
        print("Erro soma dos pesos ponderados não resultou em 100%, resultou em " + int(soma) + "%. Tente novamente.") 
        soma = 0
        self.array_peso_crit = list([])
    self.array_peso_crit = np.array(self.array_peso_crit)

  def pondera_matriz_norm(self):
    "->Produz matriz ponderada"
    for i in range(0, self.num_alt):
      for j in range(0, self.num_crit):
        self.matriz_norm_polar[i][j] = (self.matriz_norm[i][j])*(self.array_peso_crit[j])
  
  def solucoes_ideais(self):
    for j in range(0,self.num_crit):
      if (self.matriz_crit[1][j] == "min"):
        self.sol_ideal_pos.append(np.amin(self.matriz_norm_polar[:,j]))
        self.sol_ideal_neg.append(np.amax(self.matriz_norm_polar[:,j]))
      else:
        self.sol_ideal_pos.append(np.amax(self.matriz_norm_polar[:,j]))
        self.sol_ideal_neg.append(np.amin(self.matriz_norm_polar[:,j]))
    
    self.sol_ideal_pos = np.array(self.sol_ideal_pos)
    self.sol_ideal_neg = np.array(self.sol_ideal_neg)

  def define_arrays_distancias(self):
    "Calcula a raiz do somatório dos quadrados das subtrações de elementos das colunas pelo vetor solução ideal, em uma linha"
    for i in range(0, self.num_alt):
      somatorio_pos = 0
      somatorio_neg = 0
      for j in range(0, self.num_crit):
        somatorio_pos = somatorio_pos + (self.matriz_norm_polar[i][j] - self.sol_ideal_pos[j])**2
        somatorio_neg = somatorio_neg + (self.matriz_norm_polar[i][j] - self.sol_ideal_neg[j])**2

      D_pos = math.sqrt(somatorio_pos)
      D_neg = math.sqrt(somatorio_neg)
      self.array_dist_pos.append(D_pos)
      self.array_dist_neg.append(D_neg)
    self.array_dist_pos = np.array(self.array_dist_pos)
    self.array_dist_neg = np.array(self.array_dist_neg)

  def calcula_proximidade_relat(self):
    for j in range(0,self.num_alt):
      C = (self.array_dist_neg[j])/(self.array_dist_pos[j]+self.array_dist_neg[j])
      self.array_proximidade_relat.append(C)
    self.array_proximidade_relat = np.array(self.array_proximidade_relat)    
  
  def ordem_de_preferencia(self):
    ordem = list([])
    resultado = -np.sort(-self.array_proximidade_relat) 
    for x in range(0, self.num_alt):
      i = np.where(self.array_proximidade_relat == resultado[x])
      ordem.append([x+1, self.array_alt[i[0][0]], resultado[x]])

    ordem = np.array(ordem)

    return ordem
    
  def imprime_matriz(self):
    print(self.matriz)
  
  def imprime_matriz_norm(self):
    print(self.matriz_norm)   
  
  def imprime_matriz_norm_polar(self):
    print(self.matriz_norm_polar)  

  def imprime_matriz_crit(self):
    print(self.matriz_crit)     

  def imprime_peso_crit(self):
    print(self.array_peso_crit)    

  def imprime_alternativas(self):
    print(self.array_alt)  

  def imprime_sol_ideal_pos(self):
    print(self.sol_ideal_pos)

  def imprime_sol_ideal_neg(self):
    print(self.sol_ideal_neg)
  
  def imprime_dist_pos(self):
    print(self.array_dist_pos)
  
  def imprime_dist_neg(self):
    print(self.array_dist_neg)

  def imprime_array_proximidade_relat(self):
    print(self.array_proximidade_relat)

  def imprime_numero_crit(self):
    print(self.num_crit)

  def imprime_numero_alt(self):
    print(self.num_alt)

2# ------- PROGRAMA  -------
                
topsis = TOPSIS(np.ones(1, int), np.ones(1, int), np.ones(1, int), list([]), list([]), list([]), list([]), list([]), list([]), list([]), list([]), 0, 0)

topsis.define_matriz()


pula_linhas()
topsis.imprime_matriz_crit()
topsis.imprime_matriz()
pula_linhas()

topsis.preenche_matriz()

pula_linhas()
topsis.imprime_matriz()
pula_linhas()

topsis.normaliza_matriz()

pula_linhas()
topsis.imprime_matriz_norm()
pula_linhas()

topsis.atribui_pesos()

pula_linhas()
topsis.imprime_peso_crit()
pula_linhas()

topsis.pondera_matriz_norm()

pula_linhas()
topsis.imprime_matriz_norm_polar()
pula_linhas()

topsis.solucoes_ideais()

pula_linhas()
topsis.imprime_sol_ideal_neg()
topsis.imprime_sol_ideal_pos()
pula_linhas()

topsis.define_arrays_distancias()

pula_linhas()
topsis.imprime_dist_neg()
topsis.imprime_dist_pos()
pula_linhas()

topsis.calcula_proximidade_relat()

pula_linhas()
topsis.imprime_array_proximidade_relat()
pula_linhas()

ordem = topsis.ordem_de_preferencia()

print(ordem)

jogadores = np.array(["Joao","Pedro","Vitor","Ricardo"])
final = np.array([0.87,9,0.3,20])
podio = -np.sort(-final)

lista = list([])


for x in range(0,len(final)):
  i = np.where(final == podio[x])
  alternativa = jogadores[i]
  lista.append([x+1, jogadores[i[0][0]], podio[x]])

print(lista)