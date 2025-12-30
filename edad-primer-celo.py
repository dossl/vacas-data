import re
import pandas as pd

# Base data (same as before)
rows = [
    {"Tipo": "Leche", "Raza": "Holando (Holstein)", "Promedio_meses": 11.0, "Rango_meses": "8–13"},
    {"Tipo": "Leche", "Raza": "Jersey", "Promedio_meses": 9.5, "Rango_meses": "9–10"},
    {"Tipo": "Carne", "Raza": "Angus (Bos taurus)", "Promedio_meses": 13.0, "Rango_meses": "12–14"},
    {"Tipo": "Carne", "Raza": "Hereford (Bos taurus)", "Promedio_meses": 13.0, "Rango_meses": "12–14"},
    {"Tipo": "Carne", "Raza": "Brangus (cruza con influencia Bos indicus)", "Promedio_meses": 13.6, "Rango_meses": "13.2–14.1 (401–428 días)"},
    {"Tipo": "Carne", "Raza": "Braford (influencia Bos indicus)", "Promedio_meses": 15.0, "Rango_meses": "14–16"},
]

df = pd.DataFrame(rows)

# Conversions
DAYS_PER_YEAR_FOR_SPLIT = 365  # to match user's examples for years/days columns
DAYS_PER_YEAR = 365.25
DAYS_PER_MONTH = DAYS_PER_YEAR / 12

# Compute average days
df["Edad promedio (días)"] = (df["Promedio_meses"] * DAYS_PER_MONTH).round(0).astype(int)

# Split into years + residual days
df["Edad (años)"] = (df["Edad promedio (días)"] // DAYS_PER_YEAR_FOR_SPLIT).astype(int)
df["Edad (días)"] = (df["Edad promedio (días)"] % DAYS_PER_YEAR_FOR_SPLIT).astype(int)

def parse_range_to_days(range_str: str):
    """
    Return (lower_days, upper_days) for the 'Rango_meses' field.
    - If explicit days like '(401–428 días)' exist, use those.
    - Otherwise parse the first 'a–b' as months and convert to days.
    """
    # normalize dash types
    s = range_str.replace("-", "–")
    
    # If explicit days are present in parentheses, use them
    m_days = re.search(r"\((\d+)\s*–\s*(\d+)\s*d[ií]as\)", s, flags=re.IGNORECASE)
    if m_days:
        return int(m_days.group(1)), int(m_days.group(2))
    
    # Otherwise parse the first range as months
    m_months = re.search(r"(\d+(?:\.\d+)?)\s*–\s*(\d+(?:\.\d+)?)", s)
    if not m_months:
        return None, None
    
    lo_m = float(m_months.group(1))
    hi_m = float(m_months.group(2))
    lo_d = int(round(lo_m * DAYS_PER_MONTH))
    hi_d = int(round(hi_m * DAYS_PER_MONTH))
    return lo_d, hi_d

df[["Edad promedio inferior", "Edad promedio superior"]] = df["Rango_meses"].apply(
    lambda x: pd.Series(parse_range_to_days(x))
)

# Final table with requested columns
df_out = df[[
    "Tipo",
    "Raza",
    "Edad (años)",
    "Edad (días)",
    "Edad promedio (días)",
    "Edad promedio inferior",
    "Edad promedio superior"
]].copy()

# Export CSV
csv_path = "./csv/Edad_Primer_Celo_Vacas_Uruguay_Por_Raza_Anios_Dias_Rango_Dias.csv"
df_out.to_csv(csv_path, index=False, encoding="utf-8")

