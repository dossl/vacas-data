import random, pandas as pd
from datetime import date, timedelta
import numpy as np

# Reproducibility
random.seed(42)
np.random.seed(42)

ref_date = date(2025, 12, 24)

N_TOTAL = 200
N_DAIRY = 100
N_BEEF = 100

dicose = "7654321"
padrones = {
    "Tambo Antonina": "12001",
    "Potrero 1": "12002",
    "Potrero 2": "12003",
    "Potrero 3": "12004",
    "Potrero 4": "12005",
    "Potrero 5": "12006",
    "Potrero 6": "12007",
}
mangas = {
    "Tambo Antonina": "Manga Larga",
    "Potrero 1": "Manga Potrero 1",
    "Potrero 2": "Manga Potrero 2",
    "Potrero 3": "Manga Potrero 3",
    "Potrero 4": "Manga Potrero 4",
    "Potrero 5": "Manga Potrero 5",
    "Potrero 6": "Manga Potrero 6",
}

dairy_breeds = ["Holando", "Jersey", "Kiwi Cross"]
beef_breeds = ["Hereford", "Angus", "Braford"]

# Caravanas: "UY" + 9 digits (unique)
_ids = set()
def new_caravana():
    while True:
        s = f"UY{random.randint(0, 999_999_999):09d}"
        if s not in _ids:
            _ids.add(s)
            return s

caravanas = [new_caravana() for _ in range(N_TOTAL)]

# Birthdates with full years (365-day years) + remainder days at reference date
max_diff_days = 8 * 365 + 364
diff_days = np.random.randint(0, max_diff_days + 1, size=N_TOTAL)

birthdates = [ref_date - timedelta(days=int(d)) for d in diff_days]
edad_anios = [int(d // 365) for d in diff_days]
edad_dias = [int(d % 365) for d in diff_days]

# Sex distribution
dairy_sex = ["Hembra"] * 90 + ["Macho"] * 10
random.shuffle(dairy_sex)
beef_sex = ["Hembra"] * 95 + ["Macho"] * 5
random.shuffle(beef_sex)
sexes = dairy_sex + beef_sex

# Use and breeds
uses = ["Leche"] * N_DAIRY + ["Carne"] * N_BEEF
breeds = [random.choice(dairy_breeds) for _ in range(N_DAIRY)] + [random.choice(beef_breeds) for _ in range(N_BEEF)]

# Locations
dairy_locations = ["Tambo Antonina", "Potrero 1", "Potrero 2", "Potrero 3", "Potrero 4"]
dairy_loc_assign = [dairy_locations[i % len(dairy_locations)] for i in range(N_DAIRY)]
random.shuffle(dairy_loc_assign)

beef_locations = ["Potrero 5", "Potrero 6"]
beef_loc_assign = [beef_locations[i % len(beef_locations)] for i in range(N_BEEF)]
random.shuffle(beef_loc_assign)

locations = dairy_loc_assign + beef_loc_assign

# Health and diseases (curable, requiring confinement)
health = ["Sana"] * N_TOTAL
dairy_indices = list(range(0, N_DAIRY))
beef_indices = list(range(N_DAIRY, N_TOTAL))

sick_dairy = random.sample(dairy_indices, 6)
sick_beef = random.sample(beef_indices, 7)
for idx in sick_dairy + sick_beef:
    health[idx] = "Enferma"

dairy_diseases = [
    "Mastitis clínica",
    "Metritis posparto",
    "Cojera (pododermatitis)",
    "Retención de placenta",
    "Hipocalcemia (fiebre de leche)",
]
beef_diseases = [
    "Queratoconjuntivitis infecciosa (pinkeye)",
    "Cojera (lesión de pezuña)",
    "Neumonía leve",
    "Anaplasmosis leve",
    "Herida/absceso con drenaje",
]

disease = [""] * N_TOTAL
for idx in sick_dairy:
    disease[idx] = random.choice(dairy_diseases)
for idx in sick_beef:
    disease[idx] = random.choice(beef_diseases)

# Reproductive status
def repro_status(use, sex, age_years):
    if sex == "Macho":
        if age_years < 1:
            return "Ternero"
        elif age_years < 2:
            return "Torete"
        return "Toro"
    if age_years < 1:
        return "Ternera"
    if age_years < 2:
        return "Vaquillona (recría)"
    r = random.random()
    if r < 0.30:
        return "Gestante"
    if r < 0.55:
        return "Lactando"
    if r < 0.70:
        return "Seca"
    if r < 0.90:
        return "Vacía (ciclo)"
    return "Posparto (≤30 días)"

repro = [repro_status(uses[i], sexes[i], edad_anios[i]) for i in range(N_TOTAL)]

# Parity and gestations
parity = [""] * N_TOTAL
gestations = [""] * N_TOTAL
for i in range(N_TOTAL):
    if sexes[i] == "Hembra":
        p = 0 if edad_anios[i] < 2 else random.randint(0, max(0, edad_anios[i] - 1))
        g = p + (1 if repro[i] == "Gestante" else 0)
        if edad_anios[i] >= 4 and random.random() < 0.05:
            g = max(g, p + 1)
        parity[i] = p
        gestations[i] = g

# Weight estimates (kg)
def weight_est(use, age_years, sex):
    if use == "Leche":
        base = {0:60, 1:220, 2:430, 3:520, 4:560, 5:590, 6:610, 7:620, 8:630}[age_years]
        if sex == "Macho":
            base *= 1.08
    else:
        base = {0:70, 1:250, 2:420, 3:500, 4:540, 5:570, 6:590, 7:600, 8:610}[age_years]
        if sex == "Macho":
            base *= 1.10
    return int(round(base + random.randint(-15, 15)))

weights = [weight_est(uses[i], edad_anios[i], sexes[i]) for i in range(N_TOTAL)]

# Body condition score
bcs = []
for i in range(N_TOTAL):
    if health[i] == "Enferma":
        bcs.append(round(max(1.5, min(4.5, np.random.normal(2.5, 0.4))), 1))
    else:
        target = 3.0 if uses[i] == "Leche" else 3.2
        bcs.append(round(max(2.0, min(4.5, np.random.normal(target, 0.35))), 1))

# Milk yield (dairy, lactating only)
milk_yield = [""] * N_TOTAL
for i in range(N_TOTAL):
    if uses[i] == "Leche" and repro[i] == "Lactando":
        peak = 26 if breeds[i] == "Holando" else (20 if breeds[i] == "Kiwi Cross" else 18)
        age_factor = 0.75 if edad_anios[i] == 2 else (1.0 if edad_anios[i] in [3, 4, 5] else 0.9)
        milk_yield[i] = int(round(peak * age_factor + random.randint(-3, 3)))

# Management dates
def random_past_date(max_days_back):
    return ref_date - timedelta(days=random.randint(30, max_days_back))

last_clostridial = [random_past_date(365).isoformat() for _ in range(N_TOTAL)]
last_deworm = [random_past_date(240).isoformat() for _ in range(N_TOTAL)]

# Confinement in manga if sick
current_manga = [mangas[locations[i]] if health[i] == "Enferma" else "" for i in range(N_TOTAL)]
dicose_padron = [f"{dicose}-{padrones[loc]}" for loc in locations]

df = pd.DataFrame({
    "Caravana": caravanas,
    "Fecha nacimiento": [d.isoformat() for d in birthdates],
    "Edad (años)": edad_anios,
    "Edad (días)": edad_dias,
    "Sexo": sexes,
    "Raza": breeds,
    "Uso": uses,
    "DICOSE-Padrón (ubicación actual)": dicose_padron,
    "Lugar": locations,
    "Manga": current_manga,
    "Estado reproductivo": repro,
    "N° partos": parity,
    "N° gestaciones": gestations,
    "Peso (kg)": weights,
    "BCS (1-5)": bcs,
    "Producción leche (L/día)": milk_yield,
    "Salud": health,
    "Enfermedad (si aplica)": disease,
    "Últ. vacuna clostridial": last_clostridial,
    "Últ. antiparasitario": last_deworm,
})

out_path = "./Rebano_Ficticio_Uruguay_200_Bovinos.csv"
df.to_csv(out_path, index=False, encoding="utf-8")
