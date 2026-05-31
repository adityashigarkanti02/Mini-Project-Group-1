from flask import Flask, render_template, request
import csv
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

app = Flask(__name__)

students = []

FILE_NAME = "students.csv"

# =====================================================
# HOME
# =====================================================

@app.route("/")

def home():

    return render_template(
        "index.html",
        students=students
    )

# =====================================================
# REGISTER STUDENT
# =====================================================

@app.route("/register", methods=["POST"])

def register():

    sid = request.form["sid"]

    name = request.form["name"]

    age = request.form["age"]

    marks = float(request.form["marks"])

    # Grade Calculation

    if marks >= 90:

        grade = "A"

    elif marks >= 75:

        grade = "B"

    elif marks >= 60:

        grade = "C"

    elif marks >= 40:

        grade = "D"

    else:

        grade = "F"

    student = {

        "ID": sid,
        "Name": name,
        "Age": age,
        "Marks": marks,
        "Grade": grade

    }

    students.append(student)

    return render_template(
        "index.html",
        students=students
    )

# =====================================================
# DISPLAY STUDENTS
# =====================================================

@app.route("/display")

def display():

    return render_template(
        "index.html",
        students=students
    )

# =====================================================
# LINEAR SEARCH
# =====================================================

@app.route("/search", methods=["POST"])

def search():

    sid = request.form["search_id"]

    result = None

    for student in students:

        if student["ID"] == sid:

            result = student

    return render_template(

        "index.html",

        students=students,

        result=result

    )

# =====================================================
# BUBBLE SORT
# =====================================================

@app.route("/sort")

def sort_students():

    n = len(students)

    for i in range(n):

        for j in range(0, n-i-1):

            if students[j]["Marks"] < students[j+1]["Marks"]:

                students[j], students[j+1] = (

                    students[j+1],
                    students[j]

                )

    return render_template(
        "index.html",
        students=students
    )

# =====================================================
# BINARY SEARCH
# =====================================================

@app.route("/binarysearch", methods=["POST"])

def binary_search():

    sid = request.form["binary_id"]

    students.sort(
        key=lambda x: x["ID"]
    )

    low = 0

    high = len(students) - 1

    result = None

    while low <= high:

        mid = (low + high) // 2

        if students[mid]["ID"] == sid:

            result = students[mid]

            break

        elif students[mid]["ID"] < sid:

            low = mid + 1

        else:

            high = mid - 1

    return render_template(

        "index.html",

        students=students,

        result=result

    )

# =====================================================
# FEE CALCULATION
# =====================================================

@app.route("/fee", methods=["POST"])

def fee():

    sid = request.form["fee_id"]

    fee_result = None

    for student in students:

        if student["ID"] == sid:

            total_fee = 5000

            fee_result = (

                f"Student : {student['Name']} | "
                f"Fee : ₹ {total_fee}"

            )

    return render_template(

        "index.html",

        students=students,

        fee=fee_result

    )

# =====================================================
# SAVE RECORDS
# =====================================================

@app.route("/save")

def save():

    with open(
        FILE_NAME,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            "ID",
            "Name",
            "Age",
            "Marks",
            "Grade"

        ])

        for student in students:

            writer.writerow([

                student["ID"],
                student["Name"],
                student["Age"],
                student["Marks"],
                student["Grade"]

            ])

    return render_template(

        "index.html",

        students=students

    )

# =====================================================
# LOAD RECORDS
# =====================================================

@app.route("/load")

def load():

    try:

        with open(FILE_NAME, "r") as file:

            reader = csv.DictReader(file)

            students.clear()

            for row in reader:

                students.append({

                    "ID": row["ID"],
                    "Name": row["Name"],
                    "Age": row["Age"],
                    "Marks": float(row["Marks"]),
                    "Grade": row["Grade"]

                })

    except:

        pass

    return render_template(

        "index.html",

        students=students

    )

# =====================================================
# DIRECTORY SCAN
# =====================================================

@app.route("/scan")

def scan():

    files = os.listdir()

    return render_template(

        "index.html",

        students=students,

        files=files

    )

# =====================================================
# ANALYTICS
# =====================================================

@app.route("/analytics")
def analytics():

    if len(students) == 0:

        return render_template(
            "index.html",
            students=students
        )

    df = pd.DataFrame(students)

    marks = np.array(df["Marks"])

    average = np.mean(marks)

    highest = np.max(marks)

    lowest = np.min(marks)

    # ==================================
    # BAR GRAPH
    # ==================================

    plt.figure(figsize=(8,5))

    plt.bar(
        df["Name"],
        df["Marks"]
    )

    plt.title("Student Marks Comparison")

    plt.xlabel("Students")

    plt.ylabel("Marks")

    plt.savefig("static/bar.png")

    plt.close()

    # ==================================
    # LINE GRAPH
    # ==================================

    plt.figure(figsize=(8,5))

    plt.plot(
        df["Name"],
        df["Marks"],
        marker="o"
    )

    plt.title("Student Performance Trend")

    plt.xlabel("Students")

    plt.ylabel("Marks")

    plt.grid(True)

    plt.savefig("static/line.png")

    plt.close()

    # ==================================
    # PIE CHART
    # ==================================

    grade_count = df["Grade"].value_counts()

    plt.figure(figsize=(6,6))

    plt.pie(
        grade_count,
        labels=grade_count.index,
        autopct="%1.1f%%"
    )

    plt.title("Grade Distribution")

    plt.savefig("static/pie.png")

    plt.close()

    analytics_result = (

        f"Average Marks : {average:.2f} | "
        f"Highest Marks : {highest} | "
        f"Lowest Marks : {lowest}"

    )

    return render_template(

        "index.html",

        students=students,

        analytics=analytics_result,

        show_graphs=True
    )

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    app.run(debug=True)
