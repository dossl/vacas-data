import pandas as pd
# Tabla: número de celos que se espera antes de servir (Uruguay, orientativo por tipo/raza)
rows = [
    {"Tipo": "Leche", "Raza (común)": "Holando (Holstein)", "Categoría": "Vaquillona", "Celos que se espera antes de servir": "2–3", "Nota práctica": "Mejor fertilidad si ya cicló ≥2 veces antes de la 1.ª IA."},
    {"Tipo": "Leche", "Raza (común)": "Jersey", "Categoría": "Vaquillona", "Celos que se espera antes de servir": "2–3", "Nota práctica": "Suele alcanzar pubertad antes, pero se prioriza madurez vs 1.º celo."},
    {"Tipo": "Carne", "Raza (común)": "Angus", "Categoría": "Vaquillona", "Celos que se espera antes de servir": "2–3", "Nota práctica": "Se busca llegar a la temporada ya ciclando; 3.º celo suele ser más fértil que el puberal."},
    {"Tipo": "Carne", "Raza (común)": "Hereford", "Categoría": "Vaquillona", "Celos que se espera antes de servir": "2–3", "Nota práctica": "Idem razas británicas: ciclicidad previa + peso/condición adecuados."},
    {"Tipo": "Carne", "Raza (común)": "Brangus", "Categoría": "Vaquillona", "Celos que se espera antes de servir": "3 (ideal)", "Nota práctica": "En cruzas con influencia índica se intenta asegurar mayor ciclicidad previa y desarrollo."},
    {"Tipo": "Carne", "Raza (común)": "Braford", "Categoría": "Vaquillona", "Celos que se espera antes de servir": "3 (ideal)", "Nota práctica": "Se prioriza que no sea el 1.º celo puberal y que llegue bien desarrollada al servicio."},
    {"Tipo": "Leche", "Raza (común)": "Holando/Jersey", "Categoría": "Vaca posparto", "Celos que se espera antes de servir": "0 (primer celo elegible)", "Nota práctica": "Tras período voluntario de espera (≈45–60 días), se sirve al primer celo detectado o con sincronización."},
    {"Tipo": "Carne", "Raza (común)": "Angus/Hereford/Braford/Brangus", "Categoría": "Vaca posparto", "Celos que se espera antes de servir": "0–1", "Nota práctica": "En cría a campo se sirve cuando retoma ciclicidad en la temporada; si se pierde un celo, se sirve el siguiente dentro del entore."},
]

df = pd.DataFrame(rows)

# Exportar CSV
csv_path = "./csv/Celos_Esperados_Antes_De_Servir_Uruguay.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")


