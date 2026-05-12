import pandas as pd
import os

ejecutables = ["mxmPosixFxC", "mxmPosixFxT", "mxmForkFxC", "mxmForkFxT"]
tamanios    = [100, 200, 400, 800]
hilos       = [1, 2, 4]

resultados = []

for exe in ejecutables:
    for size in tamanios:
        for hilo in hilos:
            archivo = f"Soluciones/{exe}-{size}-Hilos-{hilo}.dat"
            if os.path.exists(archivo):
                df = pd.read_csv(archivo, header=None)
                media = df[0].mean()
                std   = df[0].std()
                resultados.append({
                    "Algoritmo": exe,
                    "Tamaño":    size,
                    "Hilos":     hilo,
                    "Media_us":  round(media, 2),
                    "Std_us":    round(std, 2)
                })
            else:
                print(f"No encontrado: {archivo}")

resultado_df = pd.DataFrame(resultados)
resultado_df.to_excel("promedios.xlsx", index=False)
print("Listo! Archivo promedios.xlsx generado.")
