from flask import Flask, redirect, url_for, render_template,request
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split

app = Flask (__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def page():
    return render_template('page.html')



@app.route('/base')
def base():
    return render_template('base.html')


import re

@app.route('/visualize', methods=["GET", "POST"])
def visualize():
    histogram_files, train_html, test_html = [], None, None

    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Xóa tất cả file histogram cũ trong static/
            for f in os.listdir(app.static_folder):
                if f.startswith("histogram_") and f.endswith(".png"):
                    try:
                        os.remove(os.path.join(app.static_folder, f))
                    except Exception as e:
                        print("Không xóa được:", f, e)

            # Đọc dữ liệu
            data = pd.read_csv(filepath)

            # Chỉ lấy các cột số
            numeric_cols = data.select_dtypes(include=["number"]).columns

            histogram_files = []
            for col in numeric_cols:
                fig, ax = plt.subplots()
                data[col].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
                ax.set_title(f"Histogram of {col}")

                # Làm sạch tên cột để tạo tên file an toàn
                safe_col = re.sub(r'[^A-Za-z0-9_]', '_', col)
                filename = f"histogram_{safe_col}.png"

                path = os.path.join(app.static_folder, filename)
                fig.savefig(path)
                plt.close(fig)

                histogram_files.append(filename)

            # Chia train/test
            train, test = train_test_split(data, test_size=0.15, random_state=42)
            train_html = train.head(10).to_html(classes="data-table", index=False)
            test_html = test.head(10).to_html(classes="data-table", index=False)

    return render_template(
        "visualize.html",
        histograms=histogram_files,
        train_html=train_html,
        test_html=test_html
    )



@app.route('/predict')
def predict():
    return render_template('predict.html')

if __name__ == "__main__":
    app.run(debug=True)