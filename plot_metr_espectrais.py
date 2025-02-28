# plot_metr_espectrais.py

import matplotlib.pyplot as plt
import numpy as np
from advanced_density_analysis import calculate_spectral_moments
from math import log2

NOTAS_CROMATICAS = ["C", "C#", "D", "D#", "E", "F", 
                    "F#", "G", "G#", "A", "A#", "B"]

def midi_to_note_name(midi_number):
    if midi_number < 0 or midi_number > 127:
        return "N/A"
    octave = (midi_number // 12) - 1
    note = NOTAS_CROMATICAS[midi_number % 12]
    return f"{note}{octave}"

def semitons_to_note_name(semitons_from_c4):
    # Supondo C4 = MIDI 60.
    midi_base = 60  # C4
    midi_note = midi_base + semitons_from_c4
    midi_int = int(round(midi_note))
    octave = (midi_int // 12) - 1
    note_name = NOTAS_CROMATICAS[midi_int % 12]
    return f"{note_name}{octave}"

# Caso queira testar a conversão de semitons para notas, deixe no main guard:
# if __name__ == "__main__":
#     ticks = [-2, -1, 0, 1, 2]
#     tick_labels = [semitons_to_note_name(t) for t in ticks]
#     plt.figure()
#     plt.plot([0,1],[0,2])  # gráfico qualquer
#     plt.yticks(ticks, tick_labels)
#     plt.show()

def plot_spectral_metrics(spectral_centroid_freq, spectral_spread, centroid_note, spectral_skewness):
    """
    Plota uma tabela com métricas espectrais de forma clara e profissional.
    """
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.axis('off')

    data = [
        ["Spectral Centroid (Freq)", f"{spectral_centroid_freq:.2f} Hz"],
        ["Spectral Centroid (Note)", centroid_note],
        ["Spectral Spread", f"±{spectral_spread:.2f} Hz"],
        ["Spectral Skewness", f"{spectral_skewness:.4f}"]
    ]

    table = ax.table(cellText=data, colLabels=["Metric", "Value"], cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)

    plt.title("Spectral Metrics Summary", fontsize=14, fontweight='bold', pad=10)
    plt.tight_layout()
    #plt.show()
    plt.show(block=False)

def extract_and_plot_metrics(notas, duracoes, instrumentos, numeros_instrumentos, densidades_instrumento):
    """
    Extrai métricas espectrais a partir de pitches e densidades fornecidos,
    e plota um gráfico mostrando o centroid como nota, o spread em semitons e a skewness como número.
    """
    try:
        # Ajuste este import conforme o nome do seu arquivo principal.
        from Main import note_to_midi  
        pitches = [note_to_midi(nota) for nota in notas]

        amplitudes = densidades_instrumento

        spectral_results = calculate_spectral_moments(pitches, amplitudes)
        spectral_centroid_freq = spectral_results["spectral_centroid"]["frequency"]
        spectral_centroid_note = spectral_results["spectral_centroid"]["note"]
        spectral_spread_hz = spectral_results["spectral_spread"]["deviation"]
        spectral_skewness = spectral_results.get("spectral_skewness", np.nan)

        # Converter spread de Hz para semitons
        if spectral_centroid_freq > 0:
            upper_freq = spectral_centroid_freq + spectral_spread_hz
            if upper_freq <= 0:
                spread_semitons = np.nan
            else:
                spread_semitons = 12 * log2(upper_freq / spectral_centroid_freq)
        else:
            spread_semitons = np.nan

        print(f"Spectral Centroid (Note): {spectral_centroid_note}")
        print(f"Spectral Spread (Semitons): ±{spread_semitons:.2f}")
        print(f"Spectral Skewness: {spectral_skewness:.4f}")

        metric_labels = ["Spectral Centroid (Note)", "Spectral Spread (Semitons)", "Spectral Skewness"]

        centroid_value = 0.0
        spread_value = spread_semitons if not np.isnan(spread_semitons) else 0.0
        skewness_value = spectral_skewness if not np.isnan(spectral_skewness) else 0.0

        metric_values = [centroid_value, spread_value, skewness_value]
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

        plt.figure(figsize=(8, 5))
        plt.title("Spectral Metrics (Note and Semitones)", fontsize=14, fontweight="bold")
        plt.axhline(y=0, color='black', linewidth=1)

        x_positions = [1, 2, 3]

        for x, val, label, c in zip(x_positions, metric_values, metric_labels, colors):
            plt.plot([x, x], [0, val], color=c, linewidth=3)
            plt.plot(x, val, 'o', color=c, markersize=8)
            if label == "Spectral Centroid (Note)":
                plt.text(x, val + 0.05, spectral_centroid_note, ha='center', va='bottom', fontsize=10, fontweight='bold', color=c)
            else:
                plt.text(x, val*1.05 if val != 0 else 0.05, f"{val:.2f}", ha='center', va='bottom', fontsize=10, fontweight='bold', color=c)

        plt.xticks(x_positions, metric_labels, fontsize=10)
        plt.ylabel("Value", fontsize=12)
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)

        plt.text(1, centroid_value - 0.2, "Note shown as label", ha='center', va='top', fontsize=8, color='#1f77b4')

        plt.tight_layout()
        plt.show()
       

    except KeyError as e:
        print(f"Chave ausente no retorno de calculate_spectral_moments: {e}")
    except Exception as e:
        print(f"Erro ao calcular e plotar métricas espectrais: {e}")
