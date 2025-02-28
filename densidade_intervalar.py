#densidade intervalar.py#

import re
import math
import numpy as np
import matplotlib.pyplot as plt

# Define o tamanho da oitava microtonal
TAMANHO_OITAVA_MICROTONAL = 24
SIGMA = 50.0

# Unified microtonal scale definition
escala_microtonal = {
    'C': 1, 'C#-': 2, 'C#': 3, 'C#+': 4, 
    'D': 5, 'D#-': 6, 'D#': 7, 'D#+': 8,
    'E': 9, 'E#-': 10, 
    'F': 11, 'F#-': 12, 'F#': 13, 'F#+': 14,
    'G': 15, 'G#-': 16, 'G#': 17, 'G#+': 18, 
    'A': 19, 'A#-': 20, 'A#': 21, 'A#+': 22,
    'B': 23, 'B#-': 24, 
    'Cb+': 24, 
    'Db+': 2, 'Db': 3, 'Db-': 4, 
    'Eb+': 6, 'Eb': 7, 'Eb-': 8, 
    'Fb+': 10, 
    'Gb+': 12, 'Gb': 13, 'Gb-': 14, 
    'Ab+': 16, 'Ab': 17, 'Ab-': 18, 
    'Bb+': 20, 'Bb': 21, 'Bb-': 22,
}

# Create a list of all possible notes
lista_notas = list(escala_microtonal.keys())

def decrescimo_gaussiano(steps):
    # steps: diferença intervalar em passos microtonais
    return math.exp(-(steps**2) / (2 * (SIGMA**2)))    

def intervalo_para_numero(intervalo_string):
    """Extrai o número de passos de uma string de intervalo."""
    match = re.search(r'\(intervalo (\d+)\)', intervalo_string)
    return int(match.group(1)) if match else None

densidade_intervalo = {
    interval: decrescimo_gaussiano(steps)
    for interval, steps in {
        'unisono': 0, 'unisono+': 1, 'm2': 2, 'm2+': 3, 'M2': 4, 'M2+': 5, 
        'm3': 6, 'm3+': 7, 'M3': 8, 'M3+': 9, 'P4': 10, 'P4+': 11, 'aug4': 12,
        'aug4+': 13, 'P5': 14, 'P5+': 15, 'm6': 16, 'm6+': 17, 'M6': 18, 
        'M6+': 19, 'm7': 20, 'm7+': 21, 'M7': 22, 'M7+': 23, 'oitava': 24
    }.items()
}

def obter_densidade_intervalo(interval):
    return densidade_intervalo.get(interval, 0)

def traduzir_para_intervalo_tradicional(passos_microtonais):
    nomes_intervalos = {
        0: 'unisono', 1: 'unisono+', 2: 'm2', 3: 'm2+', 4: 'M2', 5: 'M2+',
        6: 'm3', 7: 'm3+', 8: 'M3', 9: 'M3+', 10: 'P4', 11: 'P4+', 12: 'aug4',
        13: 'aug4+', 14: 'P5', 15: 'P5+', 16: 'm6', 17: 'm6+', 18: 'M6',
        19: 'M6+', 20: 'm7', 21: 'm7+', 22: 'M7', 23: 'M7+', 24: 'oitava'
    }
    oitavas = passos_microtonais // 24
    restante = passos_microtonais % 24
    nome_tradicional = nomes_intervalos[restante]
    if oitavas > 0:
        nome_tradicional += f" + {oitavas} oitava(s)"
    return nome_tradicional

def nota_para_posicao(nota):
    correspondencia = re.match(r'([A-G][#b]?[-+]?)([0-9x])', nota)
    if not correspondencia:
        raise ValueError(f"Nota {nota} não corresponde ao padrão esperado.")
    nota_sem_oitava, oitava = correspondencia.groups()
    if oitava == 'x':
        return None
    oitava = int(oitava)
    if nota_sem_oitava not in escala_microtonal:
        raise ValueError(f"Nota {nota_sem_oitava} não está definida na escala_microtonal.")
    posicao = escala_microtonal[nota_sem_oitava] + (24 * oitava)
    return posicao

def obter_intervalos(notas):
    posicoes = [nota_para_posicao(nota) for nota in notas if nota_para_posicao(nota) is not None]
    print(f"Posições das notas: {posicoes}")
    intervalos = []
    for i in range(len(posicoes)):
        for j in range(i + 1, len(posicoes)):
            intervalo = abs(posicoes[i] - posicoes[j])
            intervalos.append(f"{traduzir_para_intervalo_tradicional(intervalo)} (intervalo {intervalo})")
    return intervalos

def calcular_densidade_intervalar(notas):
    """Calcula a densidade intervalar total com base no decaimento gaussiano."""
    intervalos_str = obter_intervalos(notas)
    densidade_total = 0
    for intervalo_str in intervalos_str:
        passos_microtonais = intervalo_para_numero(intervalo_str)
        if passos_microtonais is not None:
            # Não multiplique por 2 novamente, pois já está em passos microtonais
            densidade_intervalo = decrescimo_gaussiano(passos_microtonais)
            densidade_total += densidade_intervalo
            print(f"Microtons: {passos_microtonais}, Densidade(Gauss): {densidade_intervalo}")
    return densidade_total

def calcular_amplitude_agregado(notas):
    posicoes = [nota_para_posicao(nota) for nota in notas if nota_para_posicao(nota) is not None]
    if not posicoes:
        return 0
    return max(posicoes) - min(posicoes)

def calcular_densidade_agregado(notas, dinamicas, quantidade_notas, dinamica_para_alpha):
    posicoes = [nota_para_valor(nota) for nota in notas if nota_para_valor(nota) is not None]
    if not posicoes:
        return 0
    densidade_total = 0
    for i, pitch in enumerate(posicoes):
        dinamica = dinamicas[i]
        multiplicador_dinamica = dinamica_para_alpha.get(dinamica, 0.7)
        num_notas = quantidade_notas[i]
        densidade_nota = pitch * multiplicador_dinamica * num_notas
        densidade_total += densidade_nota
    amplitude = max(posicoes) - min(posicoes) if len(posicoes) > 1 else 1
    if amplitude == 0:
        return 0
    densidade_refinada_agregado = densidade_total / amplitude
    return densidade_refinada_agregado

if __name__ == "__main__":
    print("Testando decrescimo_gaussiano:")
    print(decrescimo_gaussiano(2))
    print(decrescimo_gaussiano(12))
    print(decrescimo_gaussiano(24))
