import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# =============================================================================================== #
# FUNCAO DE REGRESSAO LINEAR

def Reg(DE, D, E, k, Data, Nomes = 0):

    y = []
    for i in range(len(E)):
        y += E[i]
    
    x = []
    Ex = [[] for i in range(len(DE))]

    for i in range(len(DE)):
        for j in range(len(DE[i])):
            Ex[i] += [float(DE[i][j]) + k*float(D[i][j])]
        x += Ex[i]
        
    x = np.array(x)
    x = x.reshape(-1, 1)

    reg = LinearRegression()
    reg.fit(x,y)
    
    if Nomes == 0: return reg.score(x, y) # Retorna o X^2 do ajuste com k de entrada
    
    # Caso contrario plota o grafico do ajuste final

    X = np.array([0,4000])
    X = X.reshape(-1,1)

    size=10
    plt.plot(X, reg.predict(X), color='black', zorder = 1)
    
    for i in range(len(Nomes)):
        plt.scatter(Ex[i],E[i], label = Nomes[i], s = size, zorder = 2)

    plt.xlim(0,4000)
    plt.ylim(0,30)
    plt.title('Telescópio %s    k=%s' %(Data[1], str(round(k,8))))
    plt.legend()
    #plt.grid()
    plt.xlabel('Canal')
    plt.ylabel('E (MeV)')

    Xescrita= 1000
    Yescrita= 27
    plt.text(Xescrita, Yescrita, r'Coef$_{linear}$= %s' %(round(reg.intercept_,2)), fontsize=12)
    plt.text(Xescrita, Yescrita-2.5, r'Coef$_{angular}$= %s' %(round(reg.coef_[0],5)), fontsize=12)
    plt.text(Xescrita, Yescrita-5, r'$\chi^2$= %s' %(round(reg.score(x, y),4)), fontsize=12)
    plt.savefig('Resultados/%s' %(Data), dpi = 300)
    plt.show()
    
# =============================================================================================== #
# LE E RETORNA OS DADOS DE ENTRADA
    
def Dados(Nome): # "Nome" sendo o nome do arquivo .txt de entrada
    
    arq = open('Dados/' + Nome + '.txt','r')
    
    Nomes,DE,D,E = [],[[]],[[]],[[]]
    chave = 0
    lista = 0
    
    for line in arq:
        line = line.replace('\n','')

        if chave == 0:
            Nomes += [line]
            chave = 1
        elif line == '':
            chave = 0
            lista += 1
            DE += [[]]
            D  += [[]]
            E  += [[]]
        else: 
            line = line.split(',')
            DE[lista] += [float(line[0])]
            D[lista]  += [float(line[1])]
            E[lista]  += [float(line[2])]
            
    #print(Nomes, DE, D, E)
    return Nomes, DE, D, E

# =============================================================================================== #
# FUNCAO RECURSIVA PARA VARIACAO DO PARAMETRO K
    
def Recursiva(DE, D, E, Data, I, Bound, Nomes):

    X = [0 for i in range(11)]
    for k in range(11):
        X[k] = Reg(DE, D, E, Bound[0] + k*(Bound[1] - Bound[0])/10, Data)
    
    B0, B1 = Bound[0], Bound[1]
    Bound[0] = B0 + X.index(max(X))*(B1 - B0)/10
    
    # Retorna o plot final caso seja a ultima iteracao I = 1
    if I == 1: return Reg(DE, D, E, Bound[0], Data, Nomes)

    # Caso contrario retorna os novos limites de variacao do parametro k
    X1 = [X[i] for i in range(len(X))]
    X1.pop(X.index(max(X)))
    Bound[1] = B0 + X.index(max(X1))*(B1 - B0)/10
    Bound.sort()
    
    Recursiva(DE, D, E, Data, int(I - 1), Bound, Nomes) # Reteorna a funcao recursiva com I-=1

# =============================================================================================== #
# MAIN
    
def main(Data, I):
    
    Nomes, DE, D, E = Dados(Data)
    
    Recursiva(DE, D, E, Data, I, [0,1], Nomes)

    
# =============================================================================================== #

main('T3', 3)