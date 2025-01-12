from flask import Flask, render_template, request, json, redirect, url_for, send_from_directory, jsonify
import os
import urllib.parse
import random
from datetime import datetime
import requests
from hijri_converter import convert
from datetime import date
import pytz

app = Flask(__name__)

# Load JSON data dynamically
def load_data(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, "data", filename)
    print(f"Loading data from: {filepath}")
    print(f"Current working directory: {os.getcwd()}")
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None

HADITHS = {
    "الأخلاق والسلوك": ["إنما الأعمال بالنيات، وإنما لكل امرئ ما نوى", "رواه البخاري عن عمر بن الخطاب رضي الله عنه"],
    "حسن الخلق": ["من حسن إسلام المرء تركه ما لا يعنيه", "رواه الترمذي عن أبي هريرة رضي الله عنه"],
    "النصيحة": ["الدين النصيحة", "رواه مسلم عن تميم الداري رضي الله عنه"],
    "الصدق": ["عليكم بالصدق فإن الصدق يهدي إلى البر وإن البر يهدي إلى الجنة", "رواه مسلم عن عبد الله بن مسعود رضي الله عنه"],
    "الأمانة": ["أد الأمانة إلى من ائتمنك ولا تخن من خانك", "رواه أبو داود والترمذي عن أبي هريرة رضي الله عنه"]
}

@app.route('/get-daily-hadith')
def get_daily_hadith():
    # Use today's date as seed for random selection
    today = datetime.now().strftime('%Y-%m-%d')
    random.seed(today)
    
    # Select a random hadith
    title = random.choice(list(HADITHS.keys()))
    hadith_text, hadith_source = HADITHS[title]
    
    return jsonify({
        'title': title,
        'text': hadith_text,
        'source': hadith_source
    })

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/salah')
def salah():
    salah_data = load_data("salah_mistakes.json")
    if salah_data is None:
        return "Error loading data for salah", 500
    return render_template('category.html', title="أخطاء الصلاة", data=salah_data)

@app.route('/wudu')
def wudu():
    wudu_data = load_data("wudu_mistakes.json")
    if wudu_data is None:
        return "Error loading data for wudu", 500
    return render_template('category.html', title="أخطاء الوضوء", data=wudu_data)

@app.route('/quiz/<category>')
def quiz(category):
    quiz_data = load_data(f"{category}_quiz.json")
    return render_template('quiz.html', questions=quiz_data)
    
@app.route('/islamic')
def islamic():
    islamic_data = load_data("islamic_concepts.json")
    if islamic_data is None:
        return "Error loading data for islamic", 500
    return render_template('category.html', title="مفاهيم إسلامية", data=islamic_data)

@app.route('/social')
def social():
    social_data = load_data("social_mistakes.json")
    if social_data is None:
        return "Error loading data for social", 500
    return render_template('category.html', title="أخطاء اجتماعية", data=social_data)

@app.route('/communication')
def communication():
    communication_data = load_data("communication_mistakes.json")
    if communication_data is None:
        return "Error loading data for communication", 500
    return render_template('category.html', title="أخطاء في التواصل", data=communication_data)

@app.route('/quran')
def quran():
    quran_data = load_data("quran_mistakes.json")
    if quran_data is None:
        return "Error loading data for quran", 500
    return render_template('category.html', title="أخطاء في قراءة القرآن", data=quran_data)

@app.route('/fasting')
def fasting():
    fasting_data = load_data("fasting_mistakes.json")
    if fasting_data is None:
        return "Error loading data for fasting", 500
    return render_template('category.html', title="أخطاء في الصيام", data=fasting_data)

@app.route('/hajj')
def hajj():
    hajj_data = load_data("hajj_mistakes.json")
    if hajj_data is None:
        return "Error loading data for hajj", 500
    return render_template('category.html', title="أخطاء في الحج والعمرة", data=hajj_data)

@app.route('/family')
def family():
    family_data = load_data("family_mistakes.json")
    if family_data is None:
        return "Error loading data for family", 500
    return render_template('category.html', title="أخطاء في العلاقات الأسرية", data=family_data)

@app.route('/financial')
def financial():
    financial_data = load_data("financial_mistakes.json")
    if financial_data is None:
        return "Error loading data for financial", 500
    return render_template('category.html', title="أخطاء في المعاملات المالية", data=financial_data)

@app.route('/ethics')
def ethics():
    ethics_data = load_data("ethics_mistakes.json")
    if ethics_data is None:
        return "Error loading data for ethics", 500
    return render_template('category.html', title="أخطاء في الأخلاق والسلوك", data=ethics_data)

@app.route('/dua')
def dua():
    dua_data = load_data("dua_mistakes.json")
    if dua_data is None:
        return "Error loading data for dua", 500
    return render_template('category.html', title="أخطاء في الدعاء", data=dua_data)

@app.route('/work')
def work():
    work_data = load_data("work_mistakes.json")
    if work_data is None:
        return "Error loading data for work", 500
    return render_template('category.html', title="أخطاء في العمل والوظيفة", data=work_data)

@app.route('/technology')
def technology():
    technology_data = load_data("technology_mistakes.json")
    if technology_data is None:
        return "Error loading data for technology", 500
    return render_template('category.html', title="أخطاء في استخدام التكنولوجيا", data=technology_data)

@app.route('/health')
def health():
    health_data = load_data("health_mistakes.json")
    if health_data is None:
        return "Error loading data for health", 500
    return render_template('category.html', title="أخطاء في الصحة والنظافة", data=health_data)

@app.route('/solution/<category>/<fault>')
def solution(category, fault):
    # Map categories to filenames
    filename_map = {
        "أخطاء الصلاة": "salah_mistakes.json",
        "أخطاء الوضوء": "wudu_mistakes.json",
        "مفاهيم إسلامية": "islamic_concepts.json",
        "أخطاء اجتماعية": "social_mistakes.json",
        "أخطاء في التواصل": "communication_mistakes.json",
        "أخطاء في قراءة القرآن": "quran_mistakes.json",
        "أخطاء في الصيام": "fasting_mistakes.json",
        "أخطاء في الحج والعمرة": "hajj_mistakes.json",
        "أخطاء في العلاقات الأسرية": "family_mistakes.json",
        "أخطاء في المعاملات المالية": "financial_mistakes.json",
        "أخطاء في الأخلاق والسلوك": "ethics_mistakes.json",
        "أخطاء في الدعاء": "dua_mistakes.json",
        "أخطاء في العمل والوظيفة": "work_mistakes.json",
        "أخطاء في استخدام التكنولوجيا": "technology_mistakes.json",
        "أخطاء في الصحة والنظافة": "health_mistakes.json"
    }
    filename = filename_map.get(category)
    if not filename:
        return "Category not found", 404

    fault = urllib.parse.unquote(fault)
    data = load_data(filename)
    if data is None:
        return "Error loading data for solution", 500
    solutions = data.get(fault, ["لا يوجد حل محدد لهذا الخطأ."])
    return render_template('solution.html', category=category, fault=fault, solutions=solutions)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = []
        categories = ["salah_mistakes.json", "wudu_mistakes.json", "islamic_concepts.json", "social_mistakes.json", "communication_mistakes.json", "quran_mistakes.json", "fasting_mistakes.json", "hajj_mistakes.json", "family_mistakes.json", "financial_mistakes.json", "ethics_mistakes.json", "dua_mistakes.json", "work_mistakes.json", "technology_mistakes.json", "health_mistakes.json"]
        for category in categories:
            data = load_data(category)
            if data is None:
                continue
            for key, value in data.items():
                if query in key or any(query in item for item in value):
                    results.append((category.split('.')[0], key, value))
        return render_template('search_results.html', query=query, results=results)
    return render_template('search.html')

@app.route('/suggest', methods=['GET', 'POST'])
def suggest():
    if request.method == 'POST':
        category = request.form['category']
        mistake = request.form['mistake']
        solution = request.form['solution']
        source = request.form['source']
        filename_map = {
            "الصلاة": "salah_mistakes.json",
            "الوضوء": "wudu_mistakes.json",
            "مفاهيم_إسلامية": "islamic_concepts.json",
            "اجتماعية": "social_mistakes.json",
            "التواصل": "communication_mistakes.json",
            "قراءة_القرآن": "quran_mistakes.json",
            "الصيام": "fasting_mistakes.json",
            "الحج_والعمرة": "hajj_mistakes.json",
            "العلاقات_الأسرية": "family_mistakes.json",
            "المعاملات_المالية": "financial_mistakes.json",
            "الأخلاق_والسلوك": "ethics_mistakes.json",
            "الدعاء": "dua_mistakes.json",
            "العمل_والوظيفة": "work_mistakes.json",
            "استخدام_التكنولوجيا": "technology_mistakes.json",
            "الصحة_والنظافة": "health_mistakes.json"
        }
        filename = filename_map.get(category)
        if filename:
            data = load_data(filename)
            if data is None:
                data = {}
            data[mistake] = [solution, source]
            with open(f"data/{filename}", 'w', encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        return redirect(url_for('home'))
    return render_template('suggest.html')

@app.route('/mental_health')
def mental_health():
    mental_health_data = load_data("mental_health_mistakes.json")
    if mental_health_data is None:
        return "Error loading data for mental health", 500
    return render_template('category.html', title="الصحة النفسية", data=mental_health_data)

@app.route('/environment')
def environment():
    environment_data = load_data("environment_mistakes.json")
    if environment_data is None:
        return "Error loading data for environment", 500
    return render_template('category.html', title="البيئة والاستدامة", data=environment_data)

@app.route('/digital_ethics')
def digital_ethics():
    digital_ethics_data = load_data("digital_ethics_mistakes.json")
    if digital_ethics_data is None:
        return "Error loading data for digital ethics", 500
    return render_template('category.html', title="أخلاقيات العالم الرقمي", data=digital_ethics_data)

@app.route('/prayer')
def prayer():
    prayer_data = load_data("salah_mistakes.json")
    if prayer_data is None:
        return "Error loading prayer data", 500
    return render_template('category.html', title="الصلاة", data=prayer_data)

@app.route('/static/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('static/data', filename)

@app.route('/static/hadiths.json')
def serve_hadiths():
    try:
        with open('moslim app/moslimf - Copie/static/hadiths.json', 'r', encoding='utf-8') as file:
            return jsonify(json.load(file))
    except Exception as e:
        print(f"Error loading hadiths.json: {e}")
        return jsonify({"error": "Failed to load hadiths"}), 500

@app.route('/prayer-times')
def prayer_times():
    return render_template('prayer_times.html')

@app.route('/calendar')
def calendar():
    try:
        # Get today's Gregorian date
        today = date.today()
        
        # Convert to Hijri
        hijri = convert.Gregorian(today.year, today.month, today.day).to_hijri()
        
        # Arabic month names
        hijri_months = {
            1: "محرم",
            2: "صفر",
            3: "ربيع الأول",
            4: "ربيع الثاني",
            5: "جمادى الأولى",
            6: "جمادى الآخرة",
            7: "رجب",
            8: "شعبان",
            9: "رمضان",
            10: "شوال",
            11: "ذو القعدة",
            12: "ذو الحجة"
        }
        
        calendar_data = {
            'hijri': f"{hijri.day} {hijri_months[hijri.month]} {hijri.year}",
            'gregorian': today.strftime('%Y-%m-%d'),
            'hijri_month': hijri_months[hijri.month],
            'hijri_day': hijri.day,
            'hijri_year': hijri.year
        }
        
        return render_template('calendar.html', calendar=calendar_data)
    except Exception as e:
        print(f"Error in calendar route: {e}")
        return render_template('calendar.html', error="Unable to load calendar")

# API endpoints for AJAX calls
@app.route('/api/prayer-times')
def get_prayer_times():
    try:
        # Get coordinates from request parameters
        lat = request.args.get('lat', '48.8566')  # Default to Paris if not provided
        lon = request.args.get('lon', '2.3522')
        
        # Get current date
        today = datetime.now().strftime('%d-%m-%Y')
        
        # Call Aladhan API
        url = f'http://api.aladhan.com/v1/timings/{today}?latitude={lat}&longitude={lon}&method=2'
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data['code'] == 200:
            timings = data['data']['timings']
            prayer_data = {
                'fajr': timings['Fajr'],
                'dhuhr': timings['Dhuhr'],
                'asr': timings['Asr'],
                'maghrib': timings['Maghrib'],
                'isha': timings['Isha']
            }
            return jsonify(prayer_data)
        else:
            return jsonify({'error': 'Unable to fetch prayer times'}), 500
            
    except Exception as e:
        print(f"Error in get_prayer_times: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/calendar')
def get_calendar():
    try:
        # Add your calendar API logic here
        today = datetime.date.today()
        calendar_data = {
            'hijri': 'التاريخ الهجري',
            'gregorian': today.strftime('%Y-%m-%d')
        }
        return jsonify(calendar_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
