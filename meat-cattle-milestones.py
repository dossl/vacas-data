import pandas as pd
# from caas_jupyter_tools import display_dataframe_to_user  # Not available on PyPI, not used in script

beef_life_milestones = [
    {"Hito":"Nacimiento","Edad aproximada":"Día 0","Acciones del productor":"Supervisar parto, desinfección de ombligo, identificación (caravana).","Machos":"Nacen en pariciones naturales","Hembras":"Nacen en pariciones naturales","Dónde se realiza":"Potrero de parición"},
    {"Hito":"Toma de calostro","Edad aproximada":"Primeras 6–8 h","Acciones del productor":"Verificar que el ternero mame. Asistencia si es necesario.","Machos":"Calostro materno","Hembras":"Calostro materno","Dónde se realiza":"Campo"},
    {"Hito":"Lactancia","Edad aproximada":"0 a 6–8 meses","Acciones del productor":"Permanencia con la madre, chequeo de salud, control parasitario.","Machos":"Lactancia natural","Hembras":"Lactancia natural","Dónde se realiza":"Campo"},
    {"Hito":"Castración (si aplica)","Edad aproximada":"1–3 meses","Acciones del productor":"Castración (técnica quirúrgica o elastrador), registro y control sanitario.","Machos":"Sí (machos no reproductores)","Hembras":"No","Dónde se realiza":"Brete / campo"},
    {"Hito":"Marcación / caravanas","Edad aproximada":"2–4 meses","Acciones del productor":"Colocación de caravana oficial, vacunas, registro en SNIG.","Machos":"Sí","Hembras":"Sí","Dónde se realiza":"Manga / campo"},
    {"Hito":"Destete","Edad aproximada":"6–8 meses","Acciones del productor":"Separación de la madre. Suplementación según categoría.","Machos":"Destete","Hembras":"Destete","Dónde se realiza":"Potrero de destete"},
    {"Hito":"Recría","Edad aproximada":"8–18 meses","Acciones del productor":"Ganancia de peso, control sanitario, trazabilidad.","Machos":"Recría para engorde o exportación en pie","Hembras":"Recría para reposición o venta","Dónde se realiza":"Campo / pasturas mejoradas"},
    {"Hito":"Selección de vientres","Edad aproximada":"12–18 meses","Acciones del productor":"Evaluación fenotípica y sanitaria para reposición.","Machos":"-","Hembras":"Algunas se eligen como futuras madres","Dónde se realiza":"Manga / potrero"},
    {"Hito":"Engorde / terminación","Edad aproximada":"18–36 meses","Acciones del productor":"Finalización a campo o con suplemento. Control de peso y condición corporal.","Machos":"Sí, según sistema","Hembras":"Si no son seleccionadas como madres","Dónde se realiza":"Campo / suplemento (feedlot ocasional)"},
    {"Hito":"Servicio / inseminación (hembras de reposición)","Edad aproximada":"15–18 meses en adelante","Acciones del productor":"Primer celo. Servicio natural o IA para hembras seleccionadas.","Machos":"-","Hembras":"Sí (vientres de reposición)","Dónde se realiza":"Campo / brete"},
    {"Hito":"Faena","Edad aproximada":"24–36 meses (promedio)","Acciones del productor":"Traslado a frigorífico con documentación sanitaria y trazabilidad.","Machos":"Sí","Hembras":"Sí (si no se quedan como madres)","Dónde se realiza":"Frigorífico habilitado (INAC)"},
    {"Hito":"Descarte (vacas adultas)","Edad aproximada":"4–10 años","Acciones del productor":"Retiro por baja productividad, enfermedad o edad; venta o envío a faena.","Machos":"-","Hembras":"Sí","Dónde se realiza":"Frigorífico o venta a campo"},
]

df_beef_life = pd.DataFrame(beef_life_milestones)

csv_path = "./csv/Hitos_Vida_Ganado_Carne_Uruguay.csv"
df_beef_life.to_csv(csv_path, index=False, encoding="utf-8")

