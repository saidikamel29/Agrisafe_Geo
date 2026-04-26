from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import json

app = Flask(__name__)
# السماح باستقبال الطلبات حتى لو قمت بفتح HTML مباشرة من الجهاز
CORS(app)

# ==========================================
# إعدادات الاتصال بقاعدة بيانات PostgreSQL (pgAdmin)
# ==========================================
DB_HOST = "localhost"         
DB_PORT = "5432"              
DB_NAME = "agrisafe_db"      
DB_USER = "postgres"         
DB_PASS = "110628042911"     

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # إنشاء جدول لبيانات الفلاح والحقل إذا لم يكن موجوداً
        # في PostgreSQL نستخدم SERIAL للأرقام التلقائية بدلاً من AUTOINCREMENT
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id SERIAL PRIMARY KEY,
                farmer_name VARCHAR(255),
                national_id VARCHAR(255),
                dob VARCHAR(255),
                pob VARCHAR(255),
                id_culture VARCHAR(255),
                field_type VARCHAR(255),
                field_category VARCHAR(255),
                field_choix VARCHAR(255),
                area REAL,
                coordinates TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ تم الاتصال بقاعدة بيانات PostgreSQL بنجاح وتم التأكد من وجود الجدول.")
    except Exception as e:
        print("\n⚠️ حدث خطأ أثناء الاتصال بقاعدة البيانات!")
        print("- تأكد من أن خدمة PostgreSQL تعمل.")
        print("- تأكد من أنك قمت بإنشاء قاعدة بيانات باسم:", DB_NAME)
        print("- تأكد من صحة كلمة المرور واسم المستخدم في الكود.\n")
        print("تفاصيل الخطأ:", e)

# تهيئة قاعدة البيانات عند تشغيل السيرفر
init_db()

@app.route('/api/save', methods=['POST'])
def save_data():
    try:
        data = request.json
        print("تم استلام البيانات بنجاح:", data)
        
        # استخراج البيانات من JSON
        farmer = data.get('farmer', {})
        field = data.get('field', {})
        map_data = data.get('map', {})
        
        # تحويل الإحداثيات (المصفوفة) إلى نص JSON ليتم حفظه
        coords_str = json.dumps(map_data.get('coordinates', []))
        
        # فتح الاتصال بقاعدة البيانات
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # في PostgreSQL نستخدم %s كعناصر نائبة (Placeholders) بدلاً من علامة الاستفهام (?)
        cursor.execute('''
            INSERT INTO registrations (
                farmer_name, national_id, dob, pob, id_culture,
                field_type, field_category, field_choix, area, coordinates
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            farmer.get('fullName'), farmer.get('nationalId'), farmer.get('dob'),
            farmer.get('pob'), farmer.get('idCulture'),
            field.get('type'), field.get('category'), field.get('choix'),
            map_data.get('area'), coords_str
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "تم حفظ البيانات في PostgreSQL بنجاح!"}), 200

    except Exception as e:
        print("حدث خطأ أثناء الحفظ:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("\n🚀 السيرفر يعمل الآن على http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
