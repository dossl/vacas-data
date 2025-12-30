import pandas as pd

# Datos de los hitos del ganado lechero en Uruguay (tabla previamente generada)
dairy_cattle_data = [
    {
        "Hito": "Nacimiento",
        "Edad aproximada": "Día 0",
        "Acciones del productor": "Supervisión del parto, desinfección del ombligo, identificación.",
        "Machos": "Nacen a campo o en maternidad",
        "Hembras": "Nacen a campo o en maternidad",
        "Dónde se realiza": "Potrero / corral de maternidad"
    },
    {
        "Hito": "Toma de calostro",
        "Edad aproximada": "Primeras 6-8 h",
        "Acciones del productor": "Asegurar que beban calostro (a mano o directamente).",
        "Machos": "Sí",
        "Hembras": "Sí",
        "Dónde se realiza": "Corral o potrero"
    },
    {
        "Hito": "Separación de la madre",
        "Edad aproximada": "1-2 días",
        "Acciones del productor": "Separación para manejo individual, control de sanidad.",
        "Machos": "Sí",
        "Hembras": "Sí",
        "Dónde se realiza": "Corral de terneros / guachera"
    },
    {
        "Hito": "Guachera (cría artificial)",
        "Edad aproximada": "2 días a ~60 días",
        "Acciones del productor": "Alimentación con leche o sustituto. Desparasitación. Vacunación.",
        "Machos": "Sí",
        "Hembras": "Sí",
        "Dónde se realiza": "Guachera (corrales individuales o grupales)"
    },
    {
        "Hito": "Destete",
        "Edad aproximada": "60-75 días",
        "Acciones del productor": "Cese de alimentación láctea. Paso a alimentación sólida.",
        "Machos": "Sí",
        "Hembras": "Sí",
        "Dónde se realiza": "Corrales / potrero"
    },
    {
        "Hito": "Recría",
        "Edad aproximada": "2-12 meses",
        "Acciones del productor": "Pastoreo, alimentación balanceada, control sanitario.",
        "Machos": "En general vendidos o engorde propio",
        "Hembras": "Recría para futuras vacas",
        "Dónde se realiza": "Campo / instalaciones lecheras"
    },
    {
        "Hito": "Selección",
        "Edad aproximada": "3-12 meses",
        "Acciones del productor": "Venta de machos no útiles, selección de hembras para reposición.",
        "Machos": "Vendidos / engorde / descarte",
        "Hembras": "Reposición",
        "Dónde se realiza": "Manga / campo"
    },
    {
        "Hito": "Primer servicio (hembras)",
        "Edad aproximada": "15-18 meses",
        "Acciones del productor": "Inseminación o servicio natural.",
        "Machos": "-",
        "Hembras": "Sí",
        "Dónde se realiza": "Campo / brete / veterinario"
    },
    {
        "Hito": "Preñez",
        "Edad aproximada": "Confirmada a los 2 meses",
        "Acciones del productor": "Diagnóstico de gestación. Preparación para lactancia.",
        "Machos": "-",
        "Hembras": "Sí",
        "Dónde se realiza": "Manga / campo"
    },
    {
        "Hito": "Secado",
        "Edad aproximada": "60 días antes del parto",
        "Acciones del productor": "Detener ordeñe para regeneración mamaria.",
        "Machos": "-",
        "Hembras": "Sí (vacas en producción)",
        "Dónde se realiza": "Potrero / sala de ordeñe"
    },
    {
        "Hito": "Parición (2° ciclo)",
        "Edad aproximada": "24-27 meses de vida",
        "Acciones del productor": "Supervisión y preparación para inicio de producción.",
        "Machos": "-",
        "Hembras": "Sí",
        "Dónde se realiza": "Potrero de maternidad"
    },
    {
        "Hito": "Inicio ordeñe",
        "Edad aproximada": "Post parto (día 1-3)",
        "Acciones del productor": "Ingreso a rutina de ordeñe 2 veces al día. Registro de producción.",
        "Machos": "-",
        "Hembras": "Sí",
        "Dónde se realiza": "Sala de ordeñe / campo"
    },
    {
        "Hito": "Lactancia",
        "Edad aproximada": "300 días (aprox.)",
        "Acciones del productor": "Control sanitario, nutrición, control de mastitis.",
        "Machos": "-",
        "Hembras": "Sí",
        "Dónde se realiza": "Campo y sala de ordeñe"
    },
    {
        "Hito": "Faena / descarte",
        "Edad aproximada": "Variable según sistema",
        "Acciones del productor": "Cuando baja la producción o hay problemas sanitarios.",
        "Machos": "A los 6-18 meses (engorde)",
        "Hembras": "Luego de 3-6 lactancias",
        "Dónde se realiza": "Frigorífico / venta"
    }
]

# Crear DataFrame
df_dairy_life = pd.DataFrame(dairy_cattle_data)

# Guardar como CSV
csv_path = "./csv/Hitos_Vida_Ganado_Lechero_Uruguay.csv"
df_dairy_life.to_csv(csv_path, index=False, encoding="utf-8")

