#advanced_density_analysis.py"

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import warnings


def midi_to_frequency(midi_note):
    """Convert MIDI note number to frequency in Hz."""
    return 440.0 * (2 ** ((midi_note - 69) / 12))


def frequency_to_note_name(frequency):
    """Convert frequency to the nearest musical note name."""
    if frequency <= 0 or np.isnan(frequency) or np.isinf(frequency):
        print(f"Invalid frequency: {frequency}")
        return "Invalid"

    try:
        A4 = 440
        C0 = A4 * pow(2, -4.75)
        h = round(12 * np.log2(frequency / C0))
        octave = h // 12
        n = h % 12
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                      'F#', 'G', 'G#', 'A', 'A#', 'B']
        if 0 <= n < len(note_names):
            return f"{note_names[n]}{octave}"
        else:
            print(f"Invalid n value: {n}")
            return "Invalid"
    except Exception as e:
        print(f"Error converting frequency {frequency} to note name: {e}")
        return "Invalid"


def calculate_spectral_moments(pitches, spectral_densities):
    """Calculate spectral moments, including centroid, spread, and skewness."""
    pitches = np.array(pitches)
    spectral_densities = np.nan_to_num(spectral_densities) # Replace NaN with 0

    total_weight = np.sum(spectral_densities)
    if total_weight == 0:
        return {
            "spectral_centroid": {"frequency": np.nan, "note": "Invalid"},
            "spectral_spread": {"deviation": np.nan},
            "spectral_skewness": np.nan,
        }

    weighted_sum = np.sum(pitches * spectral_densities)
    spectral_centroid_midi = weighted_sum / total_weight

    # Calculate spectral spread (desvio padrão)
    spread_sum = np.sum(spectral_densities * (pitches - spectral_centroid_midi) ** 2)
    spectral_spread_midi = np.sqrt(spread_sum / total_weight)

    # Calcular o skewness
    # Primeiro o terceiro momento central:
    skewness_sum = np.sum(spectral_densities * (pitches - spectral_centroid_midi) ** 3)

    # Se o spread (desvio padrão) for 0, evitamos divisão por zero
    if spectral_spread_midi == 0:
        spectral_skewness = np.nan
    else:
        spectral_skewness = (skewness_sum / total_weight) / (spectral_spread_midi ** 3)

    # Converter centroid e spread para frequência
    spectral_centroid_freq = midi_to_frequency(spectral_centroid_midi)
    spectral_spread_freq = midi_to_frequency(spectral_centroid_midi + spectral_spread_midi) - spectral_centroid_freq
    spectral_centroid_note = frequency_to_note_name(spectral_centroid_freq)

    return {
        "spectral_centroid": {"frequency": spectral_centroid_freq, "note": spectral_centroid_note},
        "spectral_spread": {"deviation": spectral_spread_freq},
        "spectral_skewness": spectral_skewness,
    }



def apply_kernel_density_estimation(pitches, densities, bandwidth=1.0):
    """Apply KDE to pitches, handling invalid input data."""
    print("Entrando em apply_kernel_density_estimation")
    print("Pitches:", pitches)
    print("Densities:", densities)

    if not pitches or not densities:
        print("Erro: pitches ou densities vazios.")
        return None, None
    if len(pitches) != len(densities):
        print("Erro: pitches e densities devem ter o mesmo tamanho.")
        return None, None

    try:
        print("Calculando o KDE...")
        kde = gaussian_kde(pitches, weights=densities, bw_method=bandwidth)
        pitch_range = np.linspace(min(pitches), max(pitches), 1000)
        kde_values = kde(pitch_range)
        print("KDE calculado com sucesso.")
        return pitch_range, kde_values
    except Exception as e:
        print(f"Erro ao aplicar KDE: {e}")
        return None, None




def plot_note_densities(pitches, densities, title="Densidade por Nota", font_size=10, show_grid=True):
    """Plot note densities."""
    try:
        note_names = [frequency_to_note_name(midi_to_frequency(p)) for p in pitches]

        plt.figure(figsize=(12, 6))
        plt.bar(note_names, densities, color='skyblue')

        plt.title(title, fontsize=font_size + 2)
        plt.xlabel("Notas", fontsize=font_size)
        plt.ylabel("Densidade", fontsize=font_size)
        plt.xticks(rotation=45, fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.grid(show_grid, axis='y')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Erro ao plotar densidades: {e}")


def plot_kde_with_note_names(pitch_range, kde_values, title="Distribuição Espectral", plot_type="Linear", font_size=10, show_grid=True):
    """Plot KDE with note names on x-axis."""

    try:
        plt.figure(figsize=(12, 6))

        if plot_type == "Logarithmic":
            plt.yscale("log")

        plt.plot(pitch_range, kde_values, label="Densidade Espectral", linewidth=2)

        tick_positions = np.linspace(0, len(pitch_range) - 1, num=12, dtype=int)
        tick_labels = [frequency_to_note_name(midi_to_frequency(pitch_range[pos])) for pos in tick_positions]

        plt.xticks(tick_positions, tick_labels, rotation=45, fontsize=font_size)
        plt.title(title, fontsize=font_size + 2)
        plt.xlabel("Notas", fontsize=font_size)
        plt.ylabel("Densidade", fontsize=font_size)
        plt.grid(show_grid)
        plt.legend(fontsize=font_size)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Erro ao plotar KDE: {e}")


def plot_stable_values(pitches, densities, title="Valores Estáveis de Densidade", font_size=10, show_grid=True):
    """Plot stable density values."""
    try:
        note_names = [frequency_to_note_name(midi_to_frequency(p)) for p in pitches]
        plt.figure(figsize=(12, 6))
        plt.plot(note_names, densities, marker='o', linestyle='-', color='b')
        plt.title(title, fontsize=font_size + 2)
        plt.xlabel("Notas", fontsize=font_size)
        plt.ylabel("Densidade", fontsize=font_size)
        plt.xticks(rotation=45, fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.grid(show_grid)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Erro ao plotar valores estáveis: {e}")


