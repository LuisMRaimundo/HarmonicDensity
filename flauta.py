#flauta.py#

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, Matern

def converter_notacao(nota):
    """Converte a notação personalizada para a notação padrão.

    Args:
        nota (str): A nota na notação personalizada.

    Returns:
        str: A nota na notação padrão.
    """
    if 'b' in nota:  # Verifica se a nota contém um bemol
        nota_sustenido = nota.replace('b', '#')  # Substitui 'b' por '#'
        if '-' in nota:
            nota_sustenido = nota_sustenido.replace('#-', '#+')  # Substitui '#-' por '#+'
        elif '+' in nota:
            nota_sustenido = nota_sustenido.replace('#+', '#-')  # Substitui '#+' por '#-'
        return nota_sustenido
    return nota  # Retorna a nota original se não precisar converter




# Define the spectral data for each note and dynamic level
spectral_data = {
    'C4': {'pp': 4.723, 'mf': 11.721, 'ff': 18.528},
    'C#-4': {'pp': 4.723, 'mf': 11.721, 'ff': 18.528},
    'C#4': {'pp': 4.518, 'mf': 10.958, 'ff': 18.414},
    'C#+4': {'pp': 4.576, 'mf': 10.527, 'ff': 18.497},
    'D4': {'pp': 4.872, 'mf': 10.282, 'ff': 18.883},
    'D#-4': {'pp': 4.9, 'mf': 10.106, 'ff': 19.127},
    'D#4': {'pp': 4.733, 'mf': 9.465, 'ff': 19.465},
    'D#+4': {'pp': 4.665, 'mf': 9.0, 'ff': 19.005},
    'E4': {'pp': 4.894, 'mf': 8.278, 'ff': 17.054},
    'E#-4': {'pp': 5.206, 'mf': 8.35, 'ff': 16.193},
    'F4': {'pp': 6.193, 'mf': 9.398, 'ff': 14.68},
    'F#-4': {'pp': 6.269, 'mf': 9.965, 'ff': 13.853},
    'F#4': {'pp': 5.321, 'mf': 10.424, 'ff': 13.26},
    'F#+4': {'pp': 5.515, 'mf': 10.893, 'ff': 13.037},
    'G4': {'pp': 7.408, 'mf': 11.903, 'ff': 12.966},
    'G#-4': {'pp': 7.503, 'mf': 12.065, 'ff': 12.688},
    'G#4': {'pp': 6.547, 'mf': 11.894, 'ff': 12.149},
    'G#+4': {'pp': 5.864, 'mf': 11.253, 'ff': 11.99},
    'A4': {'pp': 4.861, 'mf': 9.739, 'ff': 12.007},
    'A#-4': {'pp': 4.403, 'mf': 9.191, 'ff': 11.654},
    'A#4': {'pp': 3.865, 'mf': 8.868, 'ff': 10.374},
    'A#+4': {'pp': 3.595, 'mf': 8.837, 'ff': 10.217},
    'B4': {'pp': 3.044, 'mf': 8.733, 'ff': 10.573},
    'B#-4': {'pp': 2.834, 'mf': 8.625, 'ff': 10.559},
    'C5': {'pp': 2.761, 'mf': 8.203, 'ff': 9.801},
    'C#-5': {'pp': 2.722, 'mf': 7.532, 'ff': 8.731},
    'C#5': {'pp': 2.752, 'mf': 5.848, 'ff': 6.324},
    'C#+5': {'pp': 2.761, 'mf': 5.763, 'ff': 5.876},
    'D5': {'pp': 2.759, 'mf': 6.847, 'ff': 6.37},
    'D#-5': {'pp': 2.77, 'mf': 7.093, 'ff': 6.689},
    'D#5': {'pp': 2.776, 'mf': 6.416, 'ff': 6.742},
    'D#+5': {'pp': 2.743, 'mf': 5.96, 'ff': 6.616},
    'E5': {'pp': 2.634, 'mf': 5.377, 'ff': 6.563},
    'E#-5': {'pp': 2.628, 'mf': 5.242, 'ff': 6.182},
    'F5': {'pp': 2.691, 'mf': 5.34, 'ff': 5.047},
    'F#-5': {'pp': 2.669, 'mf': 5.102, 'ff': 4.389},
    'F#5': {'pp': 2.518, 'mf': 4.282, 'ff': 3.783},
    'F#+5': {'pp': 2.572, 'mf': 4.187, 'ff': 3.439},
    'G5': {'pp': 2.841, 'mf': 4.743, 'ff': 3.274},
    'G#-5': {'pp': 2.902, 'mf': 4.988, 'ff': 3.508},
    'G#5': {'pp': 2.821, 'mf': 5.225, 'ff': 4.505},
    'G#+5': {'pp': 2.751, 'mf': 4.989, 'ff': 4.829},
    'A5': {'pp': 2.609, 'mf': 4.121, 'ff': 5.019},
    'A#-5': {'pp': 2.537, 'mf': 3.442, 'ff': 4.818},
    'A#5': {'pp': 2.488, 'mf': 2.908, 'ff': 4.183},
    'A#+5': {'pp': 2.541, 'mf': 2.829, 'ff': 3.915},
    'B5': {'pp': 2.707, 'mf': 3.186, 'ff': 3.3},
    'B#-5': {'pp': 3.087, 'mf': 3.271, 'ff': 3.23},
    'C6': {'pp': 3.912, 'mf': 2.957, 'ff': 3.345},
    'C#-6': {'pp': 3.578, 'mf': 2.388, 'ff': 2.828},
    'C#6': {'pp': 1.734, 'mf': 1.11, 'ff': 1.198},
    'C#+6': {'pp': 1.309, 'mf': 1.278, 'ff': 1.125},
    'D6': {'pp': 2.255, 'mf': 3.165, 'ff': 2.763},
    'D#-6': {'pp': 2.435, 'mf': 3.471, 'ff': 2.76},
    'D#6': {'pp': 2.573, 'mf': 3.239, 'ff': 1.467},
    'D#+6': {'pp': 2.571, 'mf': 2.91, 'ff': 1.072},
    'E6': {'pp': 2.492, 'mf': 1.856, 'ff': 0.574},
    'E#-6': {'pp': 2.428, 'mf': 1.632, 'ff': 0.503},
    'F6': {'pp': 2.339, 'mf': 2.014, 'ff': 0.725},
    'F#-6': {'pp': 2.272, 'mf': 2.203, 'ff': 0.834},
    'F#6': {'pp': 2.161, 'mf': 2.434, 'ff': 0.96},
    'F#+6': {'pp': 2.163, 'mf': 2.507, 'ff': 1.007},
    'G6': {'pp': 2.3, 'mf': 2.481, 'ff': 1.011},
    'G#-6': {'pp': 2.193, 'mf': 2.327, 'ff': 0.941},
    'G#6': {'pp': 1.797, 'mf': 1.96, 'ff': 0.739},
    'G#+6': {'pp': 1.681, 'mf': 1.972, 'ff': 0.802},
    'A6': {'pp': 1.716, 'mf': 2.396, 'ff': 1.206},
    'A#-6': {'pp': 1.741, 'mf': 2.68, 'ff': 1.437},
    'A#6': {'pp': 1.709, 'mf': 2.858, 'ff': 1.536},
    'A#+6': {'pp': 1.625, 'mf': 2.687, 'ff': 1.359},
    'B6': {'pp': 1.363, 'mf': 1.87, 'ff': 0.664},
    'B#-6': {'pp': 1.264, 'mf': 1.472, 'ff': 0.445},
    'C7': {'pp': 1.079, 'mf': 0.454, 'ff': 0.185},
    'C#-7': {'pp': 1.016, 'mf': 0.35, 'ff': 0.154},
    'C#7': {'pp': 0.799, 'mf': 0.647, 'ff': 0.145},
 
}

# Function to convert pitch notation to an integer
def nota_para_int(nota):
    """Converte a notação de altura para um inteiro."""
    try:
        nota_base, oitava = nota[:-1], int(nota[-1])
        escala = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        return escala[nota_base] + (oitava * 12)
    except (KeyError, ValueError):
        raise ValueError(f"Nota inválida: {nota}")


# Function to calculate density based on real spectral data (added)
def calcular_densidade(nota, dinamica):
    """Calcula a densidade com base nos dados espectrais."""
    try:
        return spectral_data[nota][dinamica]
    except KeyError:
        raise ValueError(f"Dados espectrais não encontrados para a nota {nota} e dinâmica {dinamica}")


# Existing function to predict intermediate dynamics with updated methods
def predict_intermediate_dynamics(pitches, pp_values, mf_values, ff_values):
    """Prevê dinâmicas intermediárias usando Gaussian Process Regression."""
    dynamic_levels = {"pppp": 1, "ppp": 2, "pp": 3, "p": 4, "mf": 5, "f": 6, "ff": 7, "fff": 8, "ffff": 9}
    all_dynamics = list(dynamic_levels.keys())
    predictions = {dynamic: [] for dynamic in all_dynamics}

    # Otimização com NumPy:
    existing_levels = np.array([dynamic_levels[d] for d in ["pp", "mf", "ff"]]).reshape(-1, 1)
    all_levels = np.array([dynamic_levels[d] for d in all_dynamics]).reshape(-1, 1)
    y_train = np.array([pp_values, mf_values, ff_values]).T

    matern_kernel = C(1.0) * Matern(length_scale=1.0, nu=1.5)
    gpr = GaussianProcessRegressor(kernel=matern_kernel, n_restarts_optimizer=10, alpha=1e-1)

    for y in y_train:
        gpr.fit(existing_levels, y)
        y_pred = gpr.predict(all_levels)
        for j, dynamic in enumerate(all_dynamics):
            predictions[dynamic].append(y_pred[j])

    return {k: np.array(v) for k, v in predictions.items()}

def get_max_note_density(nota, num): # Removido o parâmetro dinamica, que não era usado
    """Retorna a densidade máxima da nota."""
    return max(spectral_data.get(nota, {}).values()) * np.sqrt(num) if nota in spectral_data else 0


def calculate_max_possible_density(notas, dinamicas, numeros_instrumentos):
    """Calcula a densidade máxima possível."""
    return sum(get_max_note_density(nota, num) for nota, num in zip(notas, numeros_instrumentos)) 


def get_max_note_density(nota, dinamica, num):
    """Retorna a densidade máxima da nota, considerando a dinâmica e o número de instrumentos.
       Retorna 0 se a nota não for encontrada no dicionário spectral_data.
    """
    nota_padrao = converter_notacao(nota)  # Converte a notação, se necessário
    if nota_padrao in spectral_data:
        return max(spectral_data[nota_padrao].values()) * np.sqrt(num)
    return 0  # Retorna 0 se a nota não estiver no dicionário spectral_data


def calculate_max_possible_density(notas, dinamicas, numeros_instrumentos):
    """Calcula a densidade máxima possível para um conjunto de notas, dinâmicas e número de instrumentos."""
    max_density = 0
    for nota, dinamica, num in zip(notas, dinamicas, numeros_instrumentos):
        max_density += get_max_note_density(nota, dinamica, num)
    return max_density





