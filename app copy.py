from flask import Flask, render_template, json

app = Flask(__name__)

# Load JSON data dynamically
def load_data(filename):
    with open(f"data/{filename}", encoding="utf-8") as file:
        return json.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/salah')
def salah():
    salah_data = load_data("salah_mistakes.json")
    return render_template('category.html', title="أخطاء الصلاة", data=salah_data)

@app.route('/wudu')
def wudu():
    wudu_data = load_data("wudu_mistakes.json")
    return render_template('category.html', title="أخطاء الوضوء", data=wudu_data)

@app.route('/islamic')
def islamic():
    islamic_data = load_data("islamic_concepts.json")
    return render_template('category.html', title="مفاهيم إسلامية", data=islamic_data)

@app.route('/solution/<category>/<fault>')
def solution(category, fault):
    # Map categories to filenames
    filename_map = {
        "الصلاة": "salah_mistakes.json",
        "الوضوء": "wudu_mistakes.json",
        "مفاهيم_إسلامية": "islamic_concepts.json"
    }
    filename = filename_map.get(category)
    if not filename:
        return "Category not found", 404

    data = load_data(filename)
    solutions = data.get(fault, ["لا يوجد حل محدد لهذا الخطأ."])
    return render_template('solution.html', category=category, fault=fault, solutions=solutions)

if __name__ == '__main__':
    app.run(debug=True)
