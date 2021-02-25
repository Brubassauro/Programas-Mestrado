import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ====================================================================================================================================================================== #
# Funcoes de Ajuste

def func(x,a,b,c,d,e,f):
    return a + b*x + c*np.exp(-(x-d)**2/(2*e**2)) + f*x**2

def reta(x,a,b):
    return a + b*x

def gauss(x,c,d,e):
    return c*np.exp(-(x-d)**2/(2*e**2))

# ====================================================================================================================================================================== #
# Ajuste Alvo de 9Be
    
def plotBe(nome):
    
    # Leitura do arquivo de entrada
    arq = open('Dados/' + nome,'r')
    X1 = []
    Y1 = []    
    c = 1

    for line in arq:     
        line = line.replace('\n','')
        
        if line == '': break
        if c == 1:
            sum = line.split('sum= ')[1]
            c = 0
        
        else:
            line = line.split('=')
            X1 += [float(line[2])]
            Y1 += [4*float(line[1].replace(', x',''))]
    
    # Listas de pontos
    X = np.array(X1)
    Y = np.array(Y1)
    
    # Estimativa de picos de espalhamento elástico
    a = 15 # 4He2+
    
    # Algoritmo de ajuste
    popt, pcov = curve_fit(func, X[4*a:], Y[4*a:], p0=[2000, -40, 1000, 23, 0.6, 0.1]) # Ajuste da curva
    #popt, pcov = curve_fit(gauss, X[4*a:], Y[4*a:], p0=[50, 18, 0.6]) # Ajuste da curva

    # Plot de histograma de dados
    plt.grid(zorder=2)
    plt.bar(X1,Y1,zorder=10,label=r'Cont (%s)' %(sum))
    plt.title('Distribuição de contagens em energia $^4$He+$^{%s}$%s a %s$^o$' %(nome[:len(nome)-4],nome[:len(nome)-2][len(nome)-4:],nome[len(nome)-2:]))
    plt.ylabel('Cont$_{canal}$/$\Delta$E')
    plt.xlim(0,30)
    plt.ylim(0,max(Y)*1.1)
    plt.xlabel('E (MeV)')

    # Plot da funcao ajustada
    xdata = [a-0.5+0.1*i for i in range(200)]
    ydata = [func(xdata[i],popt[0],popt[1],popt[2],popt[3],popt[4],popt[5]) for i in range(200)]
    #ydata = [gauss(xdata[i],popt[0],popt[1],popt[2]) for i in range(200)]
    
    plt.plot(xdata, ydata, zorder=12, color='red',label='$^4$He$^{2+}$ ('+str(int(np.sqrt(2*np.pi)*float(popt[2])*float(popt[4])))+')') #curva​ ajustada
    #plt.plot(xdata, ydata, zorder=12, color='red',label='$^4$He$^{2+}$ ('+str(int(np.sqrt(2*np.pi)*float(popt[0])*float(popt[2])))+')') #curva​ ajustada
    plt.legend()
    
    plt.savefig('Ajustes/' + nome)
    plt.show()
    arq.close()

# ====================================================================================================================================================================== #
# Ajuste Alvo de 197Au

def plotAu(nome):
    
    # Leitura do arquivo de entrada
    arq = open('Dados/' + nome,'r')
    X1 = []
    Y1 = []
    c = 1

    for line in arq:
        line = line.replace('\n','')
        
        if line == '': break
        if c == 1:
            sum = line.split('sum= ')[1]
            c = 0
        
        else:
            line = line.split('=')
            X1 += [float(line[2])]
            Y1 += [4*float(line[1].replace(', x',''))]
    
    # Listas de pontos
    X = np.array(X1)
    Y = np.array(Y1)
    
    # Estimativa de picos de espalhamento elástico
    a = 5 # 4He1+
    b = 23 # 4He2+
    
    # Algoritmo de ajuste
    popt1, pcov1 = curve_fit(gauss, X[:4*(a+4)], Y[:4*(a+4):], p0=[3000, a, 0.6]) # Ajuste da curva
    popt2, pcov2 = curve_fit(gauss, X[4*(b-4):], Y[4*(b-4):], p0=[3000, b, 0.6]) # Ajuste da curva
    
    # Plot de histograma de dados
    plt.grid(zorder=2)
    plt.bar(X1,Y1,zorder=10,label=r'Cont (%s)' %(sum))
    plt.title('Distribuição de contagens em energia $^4$He+$^{%s}$%s a %s$^o$' %(nome[:len(nome)-4],nome[:len(nome)-2][len(nome)-4:],nome[len(nome)-2:]))
    plt.ylabel('Cont$_{canal}$/$\Delta$E')
    plt.xlim(0,30)
    plt.ylim(0,max(Y)*1.1)
    plt.xlabel('E (MeV)')

    # Plot da funcao ajustada
    xdata1 = [popt1[1]-4+0.1*i for i in range(80)]
    ydata1 = [gauss(xdata1[i],popt1[0],popt1[1],popt1[2]) for i in range(len(xdata1))]
    xdata2 = [popt2[1]-4+0.1*i for i in range(80)]
    ydata2 = [gauss(xdata2[i],popt2[0],popt2[1],popt2[2]) for i in range(len(xdata2))]
    
    plt.plot(xdata1, ydata1, zorder=12, color='red',label='$^4$He$^{1+}$ ('+str(int(np.sqrt(2*np.pi)*float(popt1[0])*float(popt1[2])))+')') #curva​ ajustada
    plt.plot(xdata2, ydata2, zorder=12, color='green',label='$^4$He$^{2+}$ ('+str(int(np.sqrt(2*np.pi)*float(popt2[0])*float(popt2[2])))+')') #curva​ ajustada
    plt.legend()
    
    plt.savefig('Ajustes/' + nome)
    plt.show()
    arq.close()
    
# ====================================================================================================================================================================== #
# Chamada de dados main()

def main():
    
    initBe = 15 # 48 para não fazer
    initAu = 15 # 48 para não fazer
    
    # Chamada para Alvo de 9Be
    for i in range(int(1+(45-initBe)/3)):
        plotBe('9Be' + str(int(initBe+3*i)))
        print('9Be: '+ str(int(initBe+3*i)))

    # Chamada para Alvo de 197Au
    for i in range(int(1+(45-initAu)/3)):
        plotAu('197Au' + str(int(initAu+3*i)))
        print('197Au: '+ str(int(initAu+3*i)))
    
main()