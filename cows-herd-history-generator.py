import os
import random
from datetime import date, datetime, timedelta
from io import StringIO

import numpy as np
import pandas as pd

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
edad_total_dias = [int(d) for d in diff_days]

# Sex distribution
dairy_sex = ["Hembra"] * 90 + ["Macho"] * 10
random.shuffle(dairy_sex)
beef_sex = ["Hembra"] * 95 + ["Macho"] * 5
random.shuffle(beef_sex)
sexes = dairy_sex + beef_sex

# Use and breeds
uses = ["Leche"] * N_DAIRY + ["Carne"] * N_BEEF
breeds = [random.choice(dairy_breeds) for _ in range(N_DAIRY)] + [
    random.choice(beef_breeds) for _ in range(N_BEEF)
]

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
    "Mastitis clinica",
    "Metritis posparto",
    "Cojera (pododermatitis)",
    "Retencion de placenta",
    "Hipocalcemia (fiebre de leche)",
]
beef_diseases = [
    "Queratoconjuntivitis infecciosa (pinkeye)",
    "Cojera (lesion de pezuna)",
    "Neumonia leve",
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
        if age_years < 2:
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
        base = {0: 60, 1: 220, 2: 430, 3: 520, 4: 560, 5: 590, 6: 610, 7: 620, 8: 630}[
            age_years
        ]
        if sex == "Macho":
            base *= 1.08
    else:
        base = {0: 70, 1: 250, 2: 420, 3: 500, 4: 540, 5: 570, 6: 590, 7: 600, 8: 610}[
            age_years
        ]
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

# Confinement in manga if sick
current_manga = [mangas[locations[i]] if health[i] == "Enferma" else "" for i in range(N_TOTAL)]
dicose_padron = [f"{dicose}-{padrones[loc]}" for loc in locations]

os.makedirs("./csv", exist_ok=True)

FIRST_HEAT_CSV = "./csv/Edad_Primer_Celo_Vacas_Uruguay_Por_Raza_Anios_Dias_Rango_Dias.csv"
FIRST_HEAT_CSV_TEXT = """Tipo,Raza,Edad (años),Edad (días),Edad promedio (días),Edad promedio inferior,Edad promedio superior
Leche,Holando (Holstein),0,335,335,244,396
Leche,Jersey,0,289,289,274,304
Carne,Angus (Bos taurus),1,31,396,365,426
Carne,Hereford (Bos taurus),1,31,396,365,426
Carne,Brangus (cruza con influencia Bos indicus),1,49,414,401,428
Carne,Braford (influencia Bos indicus),1,92,457,426,487
"""
BREED_ALIASES = {
    "Holando": "Holando (Holstein)",
    "Jersey": "Jersey",
    "Angus": "Angus (Bos taurus)",
    "Hereford": "Hereford (Bos taurus)",
    "Braford": "Braford (influencia Bos indicus)",
}


def load_first_heat_df():
    if os.path.exists(FIRST_HEAT_CSV):
        return pd.read_csv(FIRST_HEAT_CSV)
    return pd.read_csv(StringIO(FIRST_HEAT_CSV_TEXT))


FIRST_HEAT_DF = load_first_heat_df()


def sample_normal_days(mean_days, std_days, min_days=None, max_days=None):
    if std_days <= 0:
        return int(round(mean_days))
    for _ in range(8):
        value = np.random.normal(mean_days, std_days)
        if min_days is not None and value < min_days:
            continue
        if max_days is not None and value > max_days:
            continue
        return int(round(value))
    value = np.random.normal(mean_days, std_days)
    if min_days is not None:
        value = max(value, min_days)
    if max_days is not None:
        value = min(value, max_days)
    return int(round(value))


def first_heat_stats(use, breed):
    alias = BREED_ALIASES.get(breed, breed)
    row = FIRST_HEAT_DF[FIRST_HEAT_DF["Raza"] == alias]
    if not row.empty:
        data = row.iloc[0]
        mean = int(data["Edad promedio (días)"])
        lower = int(data["Edad promedio inferior"])
        upper = int(data["Edad promedio superior"])
        return mean, lower, upper
    type_rows = FIRST_HEAT_DF[FIRST_HEAT_DF["Tipo"] == use]
    if not type_rows.empty:
        mean = int(round(type_rows["Edad promedio (días)"].mean()))
        lower = int(round(type_rows["Edad promedio inferior"].mean()))
        upper = int(round(type_rows["Edad promedio superior"].mean()))
        return mean, lower, upper
    mean = int(round(FIRST_HEAT_DF["Edad promedio (días)"].mean()))
    lower = int(round(FIRST_HEAT_DF["Edad promedio inferior"].mean()))
    upper = int(round(FIRST_HEAT_DF["Edad promedio superior"].mean()))
    return mean, lower, upper


def random_time_on(day):
    return datetime(day.year, day.month, day.day, random.randint(6, 18), random.randint(0, 59))


def add_event(events, day, location, hito, note):
    if day > ref_date:
        return
    events.append(
        {
            "hito": hito,
            "fecha": random_time_on(day),
            "ubicacion": location,
            "nota": note,
        }
    )


def add_age_event(events, birthdate, min_days, max_days, location, hito, note):
    start = birthdate + timedelta(days=min_days)
    end = birthdate + timedelta(days=max_days)
    if start > ref_date:
        return
    if end > ref_date:
        end = ref_date
    if end < start:
        return
    delta_days = (end - start).days
    day = start + timedelta(days=random.randint(0, delta_days))
    add_event(events, day, location, hito, note)


def add_calf_events(events, birthdate, use):
    birth_location = "Potrero de paricion" if use == "Carne" else "Potrero / corral de maternidad"
    add_event(events, birthdate, birth_location, "Nacimiento", "Registro del nacimiento.")
    add_age_event(events, birthdate, 0, 1, "Corral o potrero", "Primer calostro", "Asegurar calostrado.")
    add_age_event(events, birthdate, 1, 5, "Manga / campo", "Colocacion de caravana oficial", "Identificacion oficial.")
    add_age_event(
        events,
        birthdate,
        1,
        7,
        "Instalaciones sanitarias",
        "Control de ombligo y signos vitales",
        "Revision sanitaria inicial.",
    )
    add_age_event(
        events,
        birthdate,
        3,
        10,
        "Oficina / app",
        "Ingreso al sistema (SNIG)",
        "Registro del nacimiento.",
    )
    add_age_event(
        events,
        birthdate,
        5,
        15,
        "Manga / campo",
        "Vacunas iniciales",
        "Plan sanitario local.",
    )
    add_age_event(
        events,
        birthdate,
        7,
        20,
        "Campo / instalaciones",
        "Revision general de salud",
        "Chequeo clinico.",
    )
    add_age_event(
        events,
        birthdate,
        30,
        40,
        "Oficina / app",
        "Carga de nacimiento en SNIG",
        "Cierre de registro.",
    )


def add_dairy_milestones(events, birthdate, sex):
    add_age_event(
        events,
        birthdate,
        1,
        2,
        "Corral de terneros / guachera",
        "Separacion de la madre",
        "Separacion para manejo individual.",
    )
    add_age_event(
        events,
        birthdate,
        2,
        60,
        "Guachera",
        "Guachera (cria artificial)",
        "Cria artificial y control sanitario.",
    )
    add_age_event(
        events,
        birthdate,
        60,
        75,
        "Corrales / potrero",
        "Destete",
        "Paso a alimentacion solida.",
    )
    add_age_event(
        events,
        birthdate,
        90,
        365,
        "Campo / instalaciones lecheras",
        "Recria",
        "Pastoreo y ganancia de peso.",
    )
    add_age_event(
        events,
        birthdate,
        90,
        365,
        "Manga / campo",
        "Seleccion",
        "Seleccion de reposicion o descarte.",
    )
    if sex == "Hembra":
        add_age_event(
            events,
            birthdate,
            450,
            540,
            "Campo / brete / veterinario",
            "Primer servicio (hembras)",
            "Inicio de vida reproductiva.",
        )


def add_beef_milestones(events, birthdate, sex):
    add_age_event(events, birthdate, 0, 240, "Campo", "Lactancia", "Permanencia con la madre.")
    if sex == "Macho":
        add_age_event(
            events,
            birthdate,
            30,
            90,
            "Brete / campo",
            "Castracion (si aplica)",
            "Castracion sanitaria.",
        )
    add_age_event(
        events,
        birthdate,
        60,
        120,
        "Manga / campo",
        "Marcacion / caravanas",
        "Marcacion y vacunas.",
    )
    add_age_event(
        events,
        birthdate,
        180,
        240,
        "Potrero de destete",
        "Destete",
        "Separacion de la madre.",
    )
    add_age_event(
        events,
        birthdate,
        240,
        540,
        "Campo / pasturas mejoradas",
        "Recria",
        "Ganancia de peso y control sanitario.",
    )
    if sex == "Hembra":
        add_age_event(
            events,
            birthdate,
            360,
            540,
            "Manga / potrero",
            "Seleccion de vientres",
            "Seleccion de reposicion.",
        )
    if sex == "Macho":
        add_age_event(
            events,
            birthdate,
            540,
            1080,
            "Campo / suplemento",
            "Engorde / terminacion",
            "Inicio de terminacion.",
        )


def add_vaccination_events(events, birthdate, base_location):
    clostridial_dates = []
    first = birthdate + timedelta(days=60)
    booster = first + timedelta(days=30)
    if first <= ref_date:
        clostridial_dates.append(first)
    if booster <= ref_date:
        clostridial_dates.append(booster)
    follow = booster + timedelta(days=365)
    while follow <= ref_date:
        clostridial_dates.append(follow)
        follow += timedelta(days=365)

    for idx, day in enumerate(clostridial_dates):
        note = "Vacunacion clostridial" if idx < 2 else "Refuerzo anual clostridial."
        add_event(events, day, base_location, "Vacunacion clostridial", note)

    deworm_dates = []
    day = birthdate + timedelta(days=90)
    while day <= ref_date:
        deworm_dates.append(day)
        day += timedelta(days=180)
    for day in deworm_dates:
        add_event(events, day, base_location, "Desparasitacion", "Antiparasitario programado.")

    last_clostridial = max(clostridial_dates) if clostridial_dates else None
    last_deworm = max(deworm_dates) if deworm_dates else None
    return last_clostridial, last_deworm


def add_repro_events(events, use, sex, breed, birthdate, age_days, status, base_location, parity_target):
    if sex != "Hembra":
        return "", ""

    gestation_days = 283
    parity_target = int(parity_target) if parity_target != "" else 0

    mean_days, lower_days, upper_days = first_heat_stats(use, breed)
    std_days = max(1, upper_days - lower_days)
    first_heat_age = sample_normal_days(
        mean_days, std_days, min_days=lower_days, max_days=upper_days
    )
    first_heat_date = birthdate + timedelta(days=first_heat_age)

    third_heat_date = None
    if first_heat_date <= ref_date:
        add_event(events, first_heat_date, base_location, "Primer Celo", "Primer celo detectado.")
        second_heat_date = first_heat_date + timedelta(days=sample_normal_days(22, 4, min_days=1))
        if second_heat_date <= ref_date:
            add_event(events, second_heat_date, base_location, "Segundo Celo", "Segundo celo detectado.")
        third_heat_date = second_heat_date + timedelta(days=sample_normal_days(22, 4, min_days=1))
        if third_heat_date <= ref_date:
            add_event(events, third_heat_date, base_location, "Tercer Celo", "Tercer celo detectado.")

    service_dates = []
    if third_heat_date and third_heat_date <= ref_date:
        add_event(events, third_heat_date, base_location, "Servicio (IA o natural)", "Servicio exitoso.")
        service_dates.append(third_heat_date)
        preg_check = third_heat_date + timedelta(days=60)
        if preg_check <= ref_date:
            add_event(events, preg_check, base_location, "Prenez confirmada", "Diagnostico de gestacion.")

    if status in ["Lactando", "Posparto (≤30 días)"] and parity_target == 0 and service_dates:
        parity_target = 1

    calving_dates = []
    has_current_pregnancy = False
    current_service = service_dates[0] if service_dates else None

    while current_service and len(calving_dates) < parity_target:
        calving = current_service + timedelta(days=gestation_days)
        if calving > ref_date:
            has_current_pregnancy = True
            break
        calving_dates.append(calving)
        calving_location = "Potrero de maternidad" if use == "Leche" else "Potrero de paricion"
        add_event(events, calving, calving_location, "Paricion", "Supervision del parto.")
        if use == "Leche":
            add_event(events, calving + timedelta(days=1), base_location, "Inicio ordene", "Ingreso a rutina.")
            add_event(events, calving + timedelta(days=2), base_location, "Lactancia", "Inicio de lactancia.")
        else:
            add_event(events, calving + timedelta(days=2), base_location, "Lactancia", "Lactancia con ternero.")

        if len(calving_dates) >= parity_target:
            break

        postpartum_offset = sample_normal_days(56, 8, min_days=20)
        postpartum_heat = calving + timedelta(days=postpartum_offset)
        if postpartum_heat > ref_date:
            break
        add_event(events, postpartum_heat, base_location, "Primer Celo posparto", "Retorno al celo.")
        add_event(events, postpartum_heat, base_location, "Servicio (IA o natural)", "Servicio exitoso.")
        service_dates.append(postpartum_heat)
        preg_check = postpartum_heat + timedelta(days=60)
        if preg_check <= ref_date:
            add_event(events, preg_check, base_location, "Prenez confirmada", "Diagnostico de gestacion.")
        current_service = postpartum_heat

    if status == "Vacía (ciclo)":
        heat_days = sample_normal_days(14, 5, min_days=5, max_days=25)
        heat = ref_date - timedelta(days=heat_days)
        add_event(events, heat, base_location, "Celo detectado", "En espera de servicio.")
    elif status == "Posparto (≤30 días)":
        if calving_dates:
            last_calving = calving_dates[-1]
        else:
            postpartum_days = sample_normal_days(12, 6, min_days=1, max_days=30)
            last_calving = ref_date - timedelta(days=postpartum_days)
            calving_dates.append(last_calving)
            calving_location = "Potrero de maternidad" if use == "Leche" else "Potrero de paricion"
            add_event(events, last_calving, calving_location, "Paricion", "Posparto reciente.")
            if use == "Leche":
                add_event(
                    events,
                    last_calving + timedelta(days=1),
                    base_location,
                    "Inicio ordene",
                    "Ingreso a rutina.",
                )
        add_event(events, last_calving + timedelta(days=2), base_location, "Posparto", "Periodo posparto.")
    elif status == "Lactando":
        if not calving_dates:
            max_days = min(300, age_days) if use == "Leche" else min(240, age_days)
            mean_days = 150 if use == "Leche" else 120
            sd_days = 60 if use == "Leche" else 50
            lact_days = sample_normal_days(mean_days, sd_days, min_days=20, max_days=max_days)
            last_calving = ref_date - timedelta(days=lact_days)
            calving_dates.append(last_calving)
            calving_location = "Potrero de maternidad" if use == "Leche" else "Potrero de paricion"
            add_event(events, last_calving, calving_location, "Paricion", "Supervision del parto.")
            if use == "Leche":
                add_event(
                    events,
                    last_calving + timedelta(days=1),
                    base_location,
                    "Inicio ordene",
                    "Ingreso a rutina.",
                )
                add_event(
                    events,
                    last_calving + timedelta(days=2),
                    base_location,
                    "Lactancia",
                    "Inicio de lactancia.",
                )
            else:
                add_event(
                    events,
                    last_calving + timedelta(days=2),
                    base_location,
                    "Lactancia",
                    "Lactancia con ternero.",
                )
    elif status in ["Gestante", "Seca"]:
        if not has_current_pregnancy:
            if calving_dates:
                conception = calving_dates[-1] + timedelta(days=sample_normal_days(56, 8, min_days=20))
            elif third_heat_date and third_heat_date <= ref_date:
                conception = third_heat_date
            else:
                conception = None
            if conception and conception <= ref_date:
                add_event(
                    events,
                    conception,
                    base_location,
                    "Servicio (IA o natural)",
                    "Servicio exitoso.",
                )
                preg_check = conception + timedelta(days=60)
                if preg_check <= ref_date:
                    add_event(
                        events,
                        preg_check,
                        base_location,
                        "Prenez confirmada",
                        "Diagnostico de gestacion.",
                    )
                has_current_pregnancy = True
            if status == "Seca" and conception:
                due_date = conception + timedelta(days=gestation_days)
                dry_start = due_date - timedelta(days=60)
                add_event(events, dry_start, base_location, "Secado", "Inicio de periodo seco.")

    parity_count = len(calving_dates)
    gestations_count = parity_count + (1 if has_current_pregnancy else 0)
    return parity_count, gestations_count


last_clostridial = [""] * N_TOTAL
last_deworm = [""] * N_TOTAL

for i in range(N_TOTAL):
    events = []
    birthdate = birthdates[i]
    use = uses[i]
    sex = sexes[i]
    status = repro[i]
    age_days = edad_total_dias[i]
    base_location = f"{locations[i]} ({dicose}-{padrones[locations[i]]})"

    add_calf_events(events, birthdate, use)
    if use == "Leche":
        add_dairy_milestones(events, birthdate, sex)
    else:
        add_beef_milestones(events, birthdate, sex)

    parity_val, gest_val = add_repro_events(
        events,
        use,
        sex,
        breeds[i],
        birthdate,
        age_days,
        status,
        base_location,
        parity[i],
    )
    if sex == "Hembra":
        parity[i] = parity_val
        gestations[i] = gest_val

    if health[i] == "Enferma":
        diag_day = ref_date - timedelta(days=random.randint(1, 20))
        add_event(
            events,
            diag_day,
            mangas[locations[i]],
            "Diagnostico de enfermedad",
            disease[i],
        )
        add_event(
            events,
            diag_day + timedelta(days=1),
            mangas[locations[i]],
            "Tratamiento en curso",
            "Confinamiento en manga.",
        )

    clost_date, deworm_date = add_vaccination_events(events, birthdate, base_location)
    last_clostridial[i] = clost_date.isoformat() if clost_date else ""
    last_deworm[i] = deworm_date.isoformat() if deworm_date else ""

    events.sort(key=lambda e: e["fecha"])
    df_hist = pd.DataFrame(
        {
            f"Hito [{caravanas[i]}]": [e["hito"] for e in events],
            "Fecha y Hora": [e["fecha"].strftime("%Y-%m-%d %H:%M") for e in events],
            "Ubicación": [e["ubicacion"] for e in events],
            "Nota": [e["nota"] for e in events],
        }
    )
    df_hist.to_csv(f"./csv/{caravanas[i]}.csv", index=False, encoding="utf-8")

df = pd.DataFrame(
    {
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
    }
)

out_path = "./csv/Rebano_Ficticio_Uruguay_200_Bovinos.csv"
df.to_csv(out_path, index=False, encoding="utf-8")
