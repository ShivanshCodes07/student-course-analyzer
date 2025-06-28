from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# ✅ Load CSV with proper spacing handled
df = pd.read_csv("data.csv", skipinitialspace=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_id = request.form["ID"]
        id_value = request.form["id_value"].strip()

        if selected_id == "student_id":
            student_data = df[df["Student id"].astype(str) == str(id_value)]
            if not student_data.empty:
                total_marks = student_data["Marks"].sum()
                return render_template("student.html",
                                       student_data=student_data.to_dict("records"),
                                       total=total_marks,
                                       id_value=id_value)
            else:
                return render_template("error.html", message="Invalid Student ID.")

        elif selected_id == "course_id":
            course_data = df[df["Course id"].astype(str) == str(id_value)]
            if not course_data.empty:
                avg = round(course_data["Marks"].mean(), 2)
                max_marks = course_data["Marks"].max()

                # 📊 Generate and save histogram
                plt.figure(figsize=(6, 4), dpi=80)
                plt.hist(course_data["Marks"], bins=10, color="skyblue", edgecolor="black")
                plt.title(f"Marks Distribution for Course ID: {id_value}")
                plt.xlabel("Marks")
                plt.ylabel("Number of Students")
                plt.tight_layout()
                plt.savefig(os.path.join("static", "histogram.png"))
                plt.close()

                return render_template("course.html",
                                       avg=avg,
                                       max_marks=max_marks,
                                       id_value=id_value)
            else:
                return render_template("error.html", message="Invalid Course ID.")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
