from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from flask import render_template
import pandas as pd

app = Flask(__name__)

engine = create_engine("sqlite:///mental_health.db")

@app.route("/")
def home():
    return jsonify({"message": "Mental Health API is running"})

# EP 1 - Sample records
@app.route("/records", methods = ["GET"])
def get_records():
    n = int(request.args.get("n", 10))
    query = f"SELECT * FROM survey_responses LIMIT {n}"
    df = pd.read_sql(query, engine)
    return df.to_dict(orient = "records")

''' df = pd.DataFrame({'col1': [1, 2],
                   'col2': [0.5, 0.75]},
                  index=['row1', 'row2'])
list of each row as one object
[{'col1': 1, 'col2': 0.5}, {'col1': 2, 'col2': 0.75}] '''

# EP 2 - Filter by year
@app.route("/year/<int:year>", methods = ["GET"])
def get_by_year(year):
    query = f"SELECT * FROM survey_responses WHERE survey_year = {year}"
    df = pd.read_sql(query, engine)
    return df.to_dict(orient = "records")

# EP 3 - Stats summary
@app.route("/stats", methods = ["GET"])
def get_stats():
    query = '''SELECT survey_year, 
    AVG(productivity_affected) AS avg_productivity_impact,
    AVG(employer_importance_mental) AS avg_employer_support
    FROM survey_responses
    GROUP BY survey_year''' 
    df = pd.read_sql(query, engine)
    return df.to_dict(orient = "records")

# EP 4 - Age trends
@app.route("/trends/age", methods = ["GET"])
def awareness_trends():
    query = '''SELECT
        survey_year,
        AVG(age) AS avg_age
        FROM survey_responses
        GROUP BY survey_year
        ORDER BY survey_year'''
    df = pd.read_sql(query, engine)
    return df.to_dict(orient = records)

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
