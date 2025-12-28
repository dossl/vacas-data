import random, pandas as pd
from datetime import date, timedelta
import numpy as np

random.seed(42)
np.random.seed(42)

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

ids = set()
def new_caravana():
    while True:
        num = random.randint(0, 999_999_999)
        s = f"UY{num:09d}"
        if s not in ids:
            ids.add(s)
            return s

caravanas = [new_caravana() for _ in range(N_TOTAL)]

ages = np.random.randint(0, 9, size=N_TOTAL)
today = date(2025, 12, 26)

def birthdate_from_age(age_years):
    start = today - timedelta(days=int((age_years+1)*365.25))
    end = today - timedelta(days=int(age_years*365.25))
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta,0)))

birthdates = [birthdate_from_age(a) for a in ages]

dairy_sex = ["Hembra"]*90 + ["Macho"]*10
random.shuffle(dairy_sex)
beef_sex = ["Hembra"]*95 + ["Macho"]*5
random.shuffle(beef_sex)

sexes = dairy_sex + beef_sex
uses = ["Leche"]*N_DAIRY + ["Carne"]*N_BEEF
breeds = [random.choice(dairy_breeds) for _ in range(N_DAIRY)] + [random.choice(beef_breeds) for _ in range(N_BEEF)]

dairy_locations = ["Tambo Antonina","Potrero 1","Potrero 2","Potrero 3","Potrero 4"]
dairy_loc_assign = [dairy_locations[i % len(dairy_locations)] for i in range(N_DAIRY)]
random.shuffle(dairy_loc_assign)

beef_locations = ["Potrero 5","Potrero 6"]
beef_loc_assign = [beef_locations[i % len(beef_locations)] for i in range(N_BEEF)]
random.shuffle(beef_loc_assign)

locations = dairy_loc_assign + beef_loc_assign

health = ["Sana"]*N_TOTAL
dairy_indices = list(range(0, N_DAIRY))
beef_indices = list(range(N_DAIRY, N_TOTAL))

sick_dairy = random.sample(dairy_indices, 6)
sick_beef = random.sample(beef_indices, 7)
for idx in sick_dairy + sick_beef:
    health[idx] = "Enferma"

dairy_diseases = ["Mastitis clínica", "Metritis posparto", "Cojera (pododermatitis)", "Retención de placenta", "Hipocalcemia"]
beef_diseases  = ["Queratoconjuntivitis infecciosa", "Cojera", "Neumonía leve", "Anaplasmosis leve", "Absceso drenado"]

disease = [""]*N_TOTAL
for idx in sick_dairy:
    disease[idx] = random.choice(dairy_diseases)
for idx in sick_beef:
    disease[idx] = random.choice(beef_diseases)

def repro_status(use, sex, age):
    if sex == "Macho":
        if age < 1: return "Ternero"
        if age < 2: return "Torete"
        return "Toro"
    if age < 1: return "Ternera"
    if age < 2: return "Vaquillona"
    r = random.random()
    if r < 0.3: return "Gestante"
    if r < 0.55: return "Lactando"
    if r < 0.7: return "Seca"
    if r < 0.9: return "Vacía"
    return "Posparto"

repro = [repro_status(uses[i], sexes[i], ages[i]) for i in range(N_TOTAL)]

parity, gestations = [""]*N_TOTAL, [""]*N_TOTAL
for i in range(N_TOTAL):
    if sexes[i] == "Hembra":
        p = 0 if ages[i] < 2 else random.randint(0, max(0, ages[i]-1))
        g = p + (1 if repro[i] == "Gestante" else 0)
        parity[i], gestations[i] = p, g

def weight_est(use, age, sex):
    base = {0:60,1:220,2:430,3:520,4:560,5:590,6:610,7:620,8:630}[age] if use=="Leche" \
           else {0:70,1:250,2:420,3:500,4:540,5:570,6:590,7:600,8:610}[age]
    if sex=="Macho": base*=1.1
    return int(round(base + random.randint(-15,15)))

weights = [weight_est(uses[i], ages[i], sexes[i]) for i in range(N_TOTAL)]

current_manga = [mangas[locations[i]] if health[i]=="Enferma" else "" for i in range(N_TOTAL)]
dicose_padron = [f"{dicose}-{padrones[loc]}" for loc in locations]

df = pd.DataFrame({
    "Caravana": caravanas,
    "Fecha nacimiento": [d.isoformat() for d in birthdates],
    "Edad (años)": ages,
    "Sexo": sexes,
    "Raza": breeds,
    "Uso": uses,
    "DICOSE-Padrón": dicose_padron,
    "Lugar": locations,
    "Manga": current_manga,
    "Estado reproductivo": repro,
    "N° partos": parity,
    "N° gestaciones": gestations,
    "Peso (kg)": weights,
    "Salud": health,
    "Enfermedad": disease
})

path = "./herd_ficticio_uruguay_200_bovinos.csv"
df.to_csv(path, index=False, encoding="utf-8")
