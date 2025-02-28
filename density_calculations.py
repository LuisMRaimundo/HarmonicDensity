# density_calculations.py

def calcular_massa(notas):
    """Calcula a massa de uma banda sonora com base no número de notas."""
    return len(notas)


def calcular_volume(notas):
    """Calcula o volume (intervalo de alturas) em semitons."""
    if not notas:
        return 0
    notas_ordenadas = sorted(notas)  # Ordena as notas antes do cálculo
    return notas_ordenadas[-1] - notas_ordenadas[0]


def calcular_densidade_intervalar(notas):
    """Calcula a densidade de intervalo como a média de todos os intervalos."""
    if len(notas) < 2:
        return 0
    intervalos = []
    for i in range(len(notas)):
        for j in range(i + 1, len(notas)):
            intervalos.append(abs(notas[i] - notas[j]))  # Considera todos os pares de notas
    return sum(intervalos) / len(intervalos)


def calcular_densidade(notas):
    """Calcula a densidade geral para um conjunto de notas."""
    massa = calcular_massa(notas)
    volume = calcular_volume(notas)
    densidade = massa / volume if volume != 0 else 0
    return densidade

