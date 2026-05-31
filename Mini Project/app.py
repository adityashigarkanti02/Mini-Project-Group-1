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


@app.route("/")
def home():

    return render_template(
        "index.html",
        students=students
    )


# ==========================
# REGISTER STUDENT
# ==========================

@app.route("/register", methods=["POST"])
def register():

    sid = request.form["sid"]
    name = request.form["name"]
    age = request.form["age"]
    marks = float(request.form["marks"])

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


# ==========================
# DISPLAY STUDENTS
# ==========================

@app.route("/display")
def display():

    return render_template(
        "index.html",
        students=students
    )


# ==========================
# LINEAR SEARCH
# ==========================

@app.route("/search", methods=["POST"])
def search():

    sid = request.form["search_id"]

    result = None

    for student in students:

        if student["ID"] == sid:

            result = student
            break

    return render_template(
        "index.html",
        students=students,
        result=result
    )


# ==========================
# BUBBLE SORT (ASCENDING)
# ==========================

@app.route("/sort")
def sort_students():

    n = len(students)

    for i in range(n):

        for j in range(n - 1):

            if students[j]["Marks"] > students[j + 1]["Marks"]:

                temp = students[j]

                students[j] = students[j + 1]

                students[j + 1] = temp

    return render_template(
        "index.html",
        students=students
    )


# ==========================
# BINARY SEARCH
# ==========================

@app.route("/binarysearch", methods=["POST"])
def binary_search():

    sid = request.form["binary_id"]

    students.sort(key=lambda x: x["ID"])

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


# ==========================
# FEE CALCULATION
# ==========================

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

            break

    return render_template(
        "index.html",
        students=students,
        fee=fee_result
    )


# ==========================
# SAVE RECORDS
# ==========================

@app.route("/save")
def save():

    with open(FILE_NAME, "w", newline="") as file:

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


# ==========================
# LOAD RECORDS
# ==========================

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


# ==========================
# DIRECTORY SCAN
# ==========================

@app.route("/scan")
def scan():

    files = os.listdir()

    return render_template(
        "index.html",
        students=students,
        files=files
    )


# ==========================
# ANALYTICS
# ==========================

@app.route("/analytics")
def analytics():

    if len(students) == 0:

        return render_template(
            "index.html",
            students=students
        )

    df = pd.DataFrame(students)

    marks = np.array(df["Marks"])

    avg = np.mean(marks)
    high = np.max(marks)
    low = np.min(marks)

    # Bar Graph

    plt.figure(figsize=(6, 4))

    plt.bar(df["Name"], df["Marks"])

    plt.title("Student Marks")

    plt.savefig("static/bar.png")

    plt.close()

    # Line Graph

    plt.figure(figsize=(6, 4))

    plt.plot(
        df["Name"],
        df["Marks"],
        marker="o"
    )

    plt.title("Performance Trend")

    plt.savefig("static/line.png")

    plt.close()

    # Pie Chart

    grades = df["Grade"].value_counts()

    plt.figure(figsize=(5, 5))

    plt.pie(
        grades,
        labels=grades.index,
        autopct="%1.1f%%"
    )

    plt.title("Grade Distribution")

    plt.savefig("static/pie.png")

    plt.close()

    analytics_result = (
        f"Average : {avg:.2f} | "
        f"Highest : {high} | "
        f"Lowest : {low}"
    )

    return render_template(
        "index.html",
        students=students,
        analytics=analytics_result,
        show_graphs=True
    )


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    app.run(debug=True)
