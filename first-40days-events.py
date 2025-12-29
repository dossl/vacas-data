import pandas as pd

# Datos de la tabla de eventos de los primeros 40 días de vida del ternero en Uruguay
events_40_days = [
    {
        "Día": "Día 0",
        "Evento": "Nacimiento",
        "Carne": "A campo",
        "Leche": "A campo o corral",
        "Campo o instalaciones": "Supervisión del parto, higiene del ombligo"
    },
    {
        "Día": "Día 0–1",
        "Evento": "Primer calostro",
        "Carne": "Mamada natural",
        "Leche": "Por succión o mamadera",
        "Campo o instalaciones": "Instalaciones controladas en leche; campo en carne"
    },
    {
        "Día": "Día 1–5",
        "Evento": "Colocación de caravana oficial (definitiva)",
        "Carne": "Sí",
        "Leche": "Sí",
        "Campo o instalaciones": "A campo o en brete/guachera"
    },
    {
        "Día": "Día 1–7",
        "Evento": "Control del ombligo, signos vitales, primeros controles sanitarios",
        "Carne": "Básico",
        "Leche": "Estricto",
        "Campo o instalaciones": "A campo o instalaciones sanitarias"
    },
    {
        "Día": "Día 3–10",
        "Evento": "Ingreso al sistema (registro en SNIG)",
        "Carne": "Productor o técnico registra",
        "Leche": "Idem",
        "Campo o instalaciones": "Desde app, oficina rural o web del MGAP"
    },
    {
        "Día": "Día 5–15",
        "Evento": "Vacunas iniciales (si aplica plan sanitario local)",
        "Carne": "A criterio del plan",
        "Leche": "Generalmente sí",
        "Campo o instalaciones": "Depende de plan y condiciones epidemiológicas"
    },
    {
        "Día": "Día 7–20",
        "Evento": "Revisión general de salud",
        "Carne": "Visual",
        "Leche": "Ficha sanitaria formal",
        "Campo o instalaciones": "Instalaciones más sistematizadas en tambos"
    },
    {
        "Día": "Día 10–30",
        "Evento": "Reposición de caravana si se pierde",
        "Carne": "Si se pierde, se repone",
        "Leche": "Idem",
        "Campo o instalaciones": "Se registra cambio de caravana"
    },
    {
        "Día": "Día 30–40",
        "Evento": "Límite para cargar nacimiento en SNIG",
        "Carne": "Obligatorio",
        "Leche": "Obligatorio",
        "Campo o instalaciones": "Registro online o con asistencia técnica"
    }
]

# Crear DataFrame
df_events_40 = pd.DataFrame(events_40_days)

# Guardar como CSV (UTF-8, con separador coma)
csv_path_40 = "./Eventos_Primeros_40_Dias_Ternero_Uruguay.csv"
df_events_40.to_csv(csv_path_40, index=False, encoding="utf-8")

