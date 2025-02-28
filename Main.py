#Main.py

import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import numpy as np
import matplotlib.pyplot as plt

from densidade_intervalar import calcular_densidade_intervalar, obter_intervalos, lista_notas
from advanced_density_analysis import calculate_spectral_moments, apply_kernel_density_estimation
from plot_metr_espectrais import extract_and_plot_metrics
from flauta import calculate_max_possible_density


def converter_para_sustenido(nota):
    """
    Converte uma nota com bemol para sua equivalente em sustenido.
    Exemplo: 'Db' -> 'C#'
    """
    equivalencias = {
        'Cb': 'B', 'Db': 'C#', 'Eb': 'D#', 'Fb': 'E', 'Gb': 'F#',
        'Ab': 'G#', 'Bb': 'A#',
        'C-': 'B#', 'D-': 'C#+', 'E-': 'D#+', 'F-': 'E#+', 'G-': 'F#+',
        'A-': 'G#+', 'B-': 'A#+',
        'C+': 'B-', 'D+': 'C#-', 'E+': 'D#-', 'F+': 'E-', 'G+': 'F#-',
        'A+': 'G#-', 'B+': 'A#-',
    }

    import re
    correspondencia = re.match(r'([A-Ga-g][#b]?[-+]?)([0-9x]?)', nota)
    if correspondencia:
        base_nota, oitava = correspondencia.groups()
        if base_nota in equivalencias:
            base_nota = equivalencias[base_nota]
        return f"{base_nota}{oitava}"
    else:
        raise ValueError(f"Nota inválida: {nota}")



# Helper function to convert note names to MIDI numbers
def note_to_midi(note):
    note_base = {
        'C': 0, 'C#': 1, 'Db': 1, 'C#-': 0.5, 'C#+': 1.5,
        'D': 2, 'D#': 3, 'Eb': 3, 'D#-': 2.5, 'D#+': 3.5,
        'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'F#-': 5.5, 'F#+': 6.5,
        'G': 7, 'G#': 8, 'Ab': 8, 'G#-': 7.5, 'G#+': 8.5,
        'A': 9, 'A#': 10, 'Bb': 10, 'A#-': 9.5, 'A#+': 10.5,
        'B': 11, 'C-': 11.5, 'B#': 12, 'B#-': 11.5
    }
    pitch = note[:-1]
    octave = int(note[-1])
    midi_number = 12 * (octave + 1) + note_base[pitch]
    return midi_number

def midi_to_hz(midi_pitch):
    return 440 * 2**((midi_pitch - 69) / 12)

def load_instrument_module(instrument_name):
    try:
        module = importlib.import_module(instrument_name)
        return module
    except ModuleNotFoundError:
        raise ImportError(f"Module for {instrument_name} not found.")

def ao_clicar_no_botao_calcular():
    try:
        # Convertendo notas para o formato sustenido
        notas = [
            converter_para_sustenido(f"{nota_vars[i].get()}{oitava_vars[i].get()}")
            for i in range(len(nota_vars)) if estados_vars[i].get() == 1
        ]
        dinamicas = [dinamica_vars[i].get() for i in range(len(dinamica_vars)) if estados_vars[i].get() == 1]
        instrumentos = [instrumento_vars[i].get() for i in range(len(instrumento_vars)) if estados_vars[i].get() == 1]
        numeros_instrumentos = [int(numero_instrumentos_vars[i].get()) for i in range(len(numero_instrumentos_vars)) if estados_vars[i].get() == 1]
        duracoes = [int(dur.get()) for dur, est in zip(duracao_vars, estados_vars) if est.get() == 1]

        if not notas or not dinamicas or not instrumentos or not numeros_instrumentos:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        densidade_intervalar_val = calcular_densidade_intervalar(notas)
        instrument_module = load_instrument_module(instrumentos[0])
        densidades_instrumento = []

        for nota, dinamica, num in zip(notas, dinamicas, numeros_instrumentos):
            if dinamica in ['pp', 'mf', 'ff']:
                densidade = instrument_module.calcular_densidade(nota, dinamica)
            else:
                pp_value = instrument_module.calcular_densidade(nota, 'pp')
                mf_value = instrument_module.calcular_densidade(nota, 'mf')
                ff_value = instrument_module.calcular_densidade(nota, 'ff')
                predicted_values = instrument_module.predict_intermediate_dynamics([nota], [pp_value], [mf_value], [ff_value])
                densidade = predicted_values[dinamica][0]
            scaled_density = densidade * np.sqrt(num)
            densidades_instrumento.append(scaled_density)

        densidade_instrumento_val = sum(densidades_instrumento)
        weight_factor = weight_factor_slider.get()
        densidade_ponderada_val = (densidade_instrumento_val * weight_factor) + (densidade_intervalar_val * (1 - weight_factor))

        pitches = [note_to_midi(nota) for nota in notas]
        amplitude = max(pitches) - min(pitches)
        densidade_refinada_val = densidade_ponderada_val / amplitude if amplitude != 0 else densidade_ponderada_val

        result = calculate_spectral_moments(pitches, densidades_instrumento)
        spectral_centroid_freq = result["spectral_centroid"]["frequency"]
        spectral_centroid_note = result["spectral_centroid"]["note"]
        spectral_spread_deviation = result["spectral_spread"]["deviation"]
        spectral_skewness = result.get("spectral_skewness", np.nan)

        max_possible_density = instrument_module.calculate_max_possible_density(notas, dinamicas, numeros_instrumentos)
        densidade_total_val = (densidade_refinada_val * spectral_spread_deviation) / max_possible_density if max_possible_density != 0 else densidade_refinada_val

        texto_resultado.delete(1.0, tk.END)
        output_string = (f"Densidade Intervalar: {densidade_intervalar_val:.4f}\n"
                         f"Densidade do Instrumento: {densidade_instrumento_val:.4f}\n"
                         f"Densidade Ponderada: {densidade_ponderada_val:.4f}\n"
                         f"Densidade Refinada: {densidade_refinada_val:.4f}\n"
                         f"Densidade Total: {densidade_total_val:.4f}\n"
                         f"Spectral Centroid Frequency: {spectral_centroid_freq:.2f} Hz, Note: {spectral_centroid_note}\n"
                         f"Spectral Spread: ±{spectral_spread_deviation:.2f} Hz\n"
                         f"Spectral Skewness: {spectral_skewness:.4f}\n")
                     
        texto_resultado.insert(tk.END, output_string)

        extract_and_plot_metrics(notas, duracoes, instrumentos, numeros_instrumentos, densidades_instrumento)

    except ValueError as e:
        messagebox.showerror("Nota Inválida", str(e))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular e plotar métricas: {e}")




def ao_clicar_no_botao_limpar():
    for var in nota_vars:
        var.set('')
    for var in oitava_vars:
        var.set('4')
    for var in dinamica_vars:
        var.set('mf')
    for var in instrumento_vars:
        var.set('flauta')
    for var in numero_instrumentos_vars:
        var.set('1')
    for var in estados_vars:
        var.set(0)
    for var in duracao_vars:
        var.set('1')
    texto_resultado.delete(1.0, tk.END)

def toggle_state(index):
    state = 'normal' if estados_vars[index].get() == 1 else 'disabled'
    nota_menus[index].config(state=state)
    oitava_menus[index].config(state=state)
    dinamica_menus[index].config(state=state)
    instrumento_menus[index].config(state=state)
    numero_instrumentos_menus[index].config(state=state)
    duracao_menus[index].config(state=state)

raiz = tk.Tk()
raiz.title("Calculadora de Densidade Integrada")

canvas = tk.Canvas(raiz)
scroll_y = tk.Scrollbar(raiz, orient="vertical", command=canvas.yview)
frame_entrada = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_entrada, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)
canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

frame_entrada.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

slider_label = tk.Label(raiz, text="Adjust Weight Factor (Instrument vs Interval Density)")
slider_label.pack(pady=(10, 0))
weight_factor_slider = tk.Scale(raiz, from_=0, to=1, orient="horizontal", resolution=0.01)
weight_factor_slider.set(0.5)
weight_factor_slider.pack()

nota_vars, oitava_vars, dinamica_vars = [], [], []
instrumento_vars, numero_instrumentos_vars, estados_vars = [], [], []
duracao_vars = []
nota_menus, oitava_menus, dinamica_menus = [], [], []
instrumento_menus, numero_instrumentos_menus, duracao_menus = [], [], []
lista_oitavas = [str(i) for i in range(10)]
niveis_dinamicos = ['pppp', 'ppp', 'pp', 'p', 'mf', 'f', 'ff', 'fff', 'ffff']
instrumentos = ['flautim', 'flauta', 'Oboe', 'Corne_ingles', 'clarinete', 'clarinete baixo', 'fagote', 'contrafagote', 'violino']

for i in range(60):
    estado_var = tk.IntVar(value=0)
    estados_vars.append(estado_var)
    checkbutton = tk.Checkbutton(frame_entrada, variable=estado_var, command=lambda i=i: toggle_state(i))
    checkbutton.grid(row=i, column=0, padx=5, pady=5)

    nota_var = tk.StringVar()
    nota_vars.append(nota_var)
    menu_nota = ttk.Combobox(frame_entrada, textvariable=nota_var, values=lista_notas, width=5, state='disabled')
    menu_nota.grid(row=i, column=1, padx=5, pady=5)
    nota_menus.append(menu_nota)

    oitava_var = tk.StringVar(value='4')
    oitava_vars.append(oitava_var)
    menu_oitava = ttk.Combobox(frame_entrada, textvariable=oitava_var, values=lista_oitavas, width=5, state='disabled')
    menu_oitava.grid(row=i, column=2, padx=5, pady=5)
    oitava_menus.append(menu_oitava)

    dinamica_var = tk.StringVar(value='mf')
    dinamica_vars.append(dinamica_var)
    menu_dinamica = ttk.Combobox(frame_entrada, textvariable=dinamica_var, values=niveis_dinamicos, width=5, state='disabled')
    menu_dinamica.grid(row=i, column=3, padx=5, pady=5)
    dinamica_menus.append(menu_dinamica)

    instrumento_var = tk.StringVar(value='flauta')
    instrumento_vars.append(instrumento_var)
    menu_instrumento = ttk.Combobox(frame_entrada, textvariable=instrumento_var, values=instrumentos, width=10, state='disabled')
    menu_instrumento.grid(row=i, column=4, padx=5, pady=5)
    instrumento_menus.append(menu_instrumento)

    numero_instrumentos_var = tk.StringVar(value='1')
    numero_instrumentos_vars.append(numero_instrumentos_var)
    menu_numero_instrumentos = ttk.Combobox(frame_entrada, textvariable=numero_instrumentos_var, values=[str(j) for j in range(1, 21)], width=5, state='disabled')
    menu_numero_instrumentos.grid(row=i, column=5, padx=5, pady=5)
    numero_instrumentos_menus.append(menu_numero_instrumentos)

    duracao_var = tk.StringVar(value='1')
    duracao_vars.append(duracao_var)
    menu_duracao = ttk.Combobox(frame_entrada, textvariable=duracao_var, values=[str(j) for j in range(1, 17)], width=5, state='disabled')
    menu_duracao.grid(row=i, column=6, padx=5, pady=5)
    duracao_menus.append(menu_duracao)

frame_botoes = tk.Frame(raiz)
frame_botoes.pack(pady=10)

botao_calcular = tk.Button(frame_botoes, text="Calcular", command=ao_clicar_no_botao_calcular)
botao_calcular.pack(side=tk.LEFT, padx=5, pady=5)

botao_limpar = tk.Button(frame_botoes, text="Limpar", command=ao_clicar_no_botao_limpar)
botao_limpar.pack(side=tk.LEFT, padx=5, pady=5)

texto_resultado = tk.Text(raiz, height=10, width=50)
texto_resultado.pack(pady=10)

if __name__ == "__main__":
    raiz.mainloop()



