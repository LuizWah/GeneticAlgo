
QUANTIDADE_DADOS = 20


def calc_media(values):
    media = 0
    for i in range(QUANTIDADE_DADOS):
        media += values[i] 
    media = media/QUANTIDADE_DADOS
    return media


def calc_desvio_padrao(dados, media):
    somatorio = 0
    for i in range(QUANTIDADE_DADOS):
        somatorio += pow(dados[i] - media, 2)
    Desvio = pow(somatorio/(QUANTIDADE_DADOS - 1), 0.5) 

    print(Desvio)   


values1 = [16.5,16.5,17,17.5,17,19,16.5,17,17,16.5,18.5,16.5,16,16.5,16,16.5,16.5,18,15.5,17.5]
media1 = 0

values2 = [17,14,16,14,15,15,14,17,14,14,16,14,13,15,14,14,15,15,15,16]
media2 = 0



media1 = calc_media(values1)
calc_desvio_padrao(values1, media1)


media2 = calc_media(values2)
calc_desvio_padrao(values2, media2)
