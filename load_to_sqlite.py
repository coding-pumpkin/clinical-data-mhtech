import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("final_clean.csv")

df = df.drop(columns=["Unnamed: 0"], errors="ignore")

engine = create_engine("sqlite:///mental_health.db")

df.to_sql(
    "survey_responses",
    engine,
    index=False,
    if_exists="replace"
)

print("Successful")

with engine.connect() as conn:
    preview = pd.read_sql("SELECT * FROM survey_responses LIMIT 5", conn)
    print(preview)

