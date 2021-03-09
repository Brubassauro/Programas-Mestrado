O código realiza a conversão das medidas do experimento de canais para energia (em MeV).

A conversão é feita a partir de uma linearização do tipo E+k.DE. Em que k é um parâmetro de calibração entre os canais de ambos detectores (E e DE).

No código é utilizado uma função recursiva que aproxima o valor de k para o valor ideal utilizando o χ² dos ajustes como parâmetro.
