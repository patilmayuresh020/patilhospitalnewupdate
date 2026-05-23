from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import pymysql
import pymysql.cursors
import os

# Connect to DB: Use XAMPP MySQL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'mayuresh0132'
MYSQL_DB = 'hospital_db'

app = Flask(__name__, static_folder=PROJECT_ROOT, static_url_path='')
CORS(app)

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e), "type": str(type(e))}), 500

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/admin')
def serve_admin():
    response = app.send_static_file('admin.html')
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "running",
        "migration": MIGRATION_STATUS,
        "version": "v3.0.0-mysql",
        "db_type": "MySQL"
    })

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

def get_db_connection(with_db=True):
    try:
        if with_db:
            conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB, cursorclass=pymysql.cursors.DictCursor)
        else:
            conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, cursorclass=pymysql.cursors.DictCursor)
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def execute_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    conn = get_db_connection()
    if not conn:
        return None if not fetchall else []
        
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if commit:
                conn.commit()
                return cur
            if fetchone:
                return cur.fetchone()
            if fetchall:
                return cur.fetchall()
    finally:
        if conn:
            conn.close()

def create_schema(conn):
    print("Creating database schema...")
    with conn.cursor() as cur:
        # 1. USERS TABLE
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT,
            mobile VARCHAR(20) UNIQUE NOT NULL,
            role VARCHAR(50) DEFAULT 'patient',
            department VARCHAR(100),
            education VARCHAR(100),
            status VARCHAR(50) DEFAULT 'Available',
            queue_current INT DEFAULT 0,
            queue_total INT DEFAULT 0,
            room_number VARCHAR(50),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # 2. APPOINTMENTS TABLE
        cur.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            dept VARCHAR(100) NOT NULL,
            doctor_name VARCHAR(255),
            date VARCHAR(100) NOT NULL,
            status VARCHAR(50) DEFAULT 'Pending',
            user_mobile VARCHAR(20) NOT NULL,
            patient_name VARCHAR(255),
            patient_age INT,
            report_id VARCHAR(50),
            FOREIGN KEY (user_mobile) REFERENCES users (mobile)
        )
        ''')
        
        # 3. REPORTS TABLE
        cur.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            appointment_id INT NOT NULL UNIQUE,
            diagnosis TEXT,
            medicines TEXT,
            notes TEXT,
            file_path TEXT,
            symptoms TEXT,
            follow_up_date VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 4. SYSTEM SETTINGS
        cur.execute('''
        CREATE TABLE IF NOT EXISTS system_settings (
            `key` VARCHAR(100) PRIMARY KEY,
            `value` TEXT
        )
        ''')
        
        # 5. MESSAGES TABLE
        cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            subject VARCHAR(255),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        conn.commit()

    # Seed Data if empty
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) as count FROM users")
        result = cur.fetchone()
        user_count = result.get('count', 0) if isinstance(result, dict) else result[0]

        if user_count == 0:
            print("Seeding initial data...")
            
            # System Settings
            try:
                 cur.execute("INSERT INTO system_settings (`key`, `value`) VALUES (%s, %s)", ('wait_time', '15'))
            except:
                 pass # might exist
                 
            # Demo Patient
            cur.execute("INSERT INTO users (name, age, mobile, role) VALUES (%s, %s, %s, %s)", 
                       ('Demo User', 25, '9876543210', 'patient'))
            
            doctors = [
                ('Dr. Nikhil Patil', 'General Physician', 'admin1', '101', 'Expert in general health and primary care.', 'MBBS, MD'),
                ('Dr. Sagar Patil', 'Dental', 'admin2', '205', 'Specialist in dental surgery and oral health.', 'BDS, MDS'),
                ('Dr. Pratiksha Patil', 'ENT', 'admin3', '310', 'Specializes in ear, nose, and throat disorders.', 'MBBS, MS (ENT)'),
                ('Dr. Sharma', 'Orthopedic', 'admin4', 'D-12', 'Expert in bone and joint treatments.', 'MBBS, MS (Ortho)'),
                ('Dr. Tiwari', 'Cardiology', 'admin5', '302', 'Specialist in heart diseases and surgery.', 'MBBS, MD, DM (Cardiology)'),
                ('Dr. Nethe', 'Pediatrics', 'admin6', '303', 'Child healthcare specialist.', 'MBBS, MD (Pediatrics)')
            ]
            
            for name, dept, pwd, room, desc, edu in doctors:
                cur.execute(
                    "INSERT INTO users (name, age, mobile, role, department, education, status, queue_current, queue_total, room_number, description) VALUES (%s, %s, %s, 'doctor', %s, %s, 'Available', 0, 0, %s, %s)",
                    (name, 45, pwd, dept, edu, room, desc)
                )
            conn.commit()


MIGRATION_STATUS = "Not Started"

def run_migrations(conn):
    global MIGRATION_STATUS
    print("Checking for required migrations...")
    try:
        with conn.cursor() as cur:
             # MySQL migration check for education
             cur.execute("SHOW COLUMNS FROM users")
             user_columns = [row['Field'] for row in cur.fetchall()]
             if 'education' not in user_columns:
                 print("Migrating: Adding 'education' to users")
                 cur.execute("ALTER TABLE users ADD COLUMN education VARCHAR(100)")

             cur.execute("SHOW COLUMNS FROM reports")
             columns = [row['Field'] for row in cur.fetchall()]
        
             if 'symptoms' not in columns:
                 print("Migrating: Adding 'symptoms' to reports request")
                 cur.execute("ALTER TABLE reports ADD COLUMN symptoms TEXT")
                 
             if 'follow_up_date' not in columns:
                 print("Migrating: Adding 'follow_up_date' to reports request")
                 cur.execute("ALTER TABLE reports ADD COLUMN follow_up_date TEXT")
                 
             conn.commit()
             print("Migrations check completed.")
             MIGRATION_STATUS = "Success"
        
    except Exception as e:
        print(f"Migration Error: {e}")
        MIGRATION_STATUS = f"Error: {str(e)}"

def init_db_if_needed():
    # Attempt to connect without DB first to create it
    conn = get_db_connection(with_db=False)
    if not conn:
        print("DB Init Error: Failed to connect to MySQL server")
        return
        
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
        conn.commit()
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()
        
    # Reconnect with DB
    conn = get_db_connection()
    if not conn:
        return
    
    tables_exist = False
    try:
        with conn.cursor() as cur:
            # Check if users table exists
            cur.execute("SHOW TABLES LIKE 'users'")
            result = cur.fetchone()
            tables_exist = result is not None
    except Exception as e:
        print(f"DB Check Error: {e}")
    finally:
        conn.close()

    if not tables_exist:
        # Reconnect to create schema
        conn = get_db_connection()
        if conn:
            try:
                create_schema(conn)
            except Exception as e:
                print(f"Schema Creation Error: {e}")
            finally:
                conn.close()

    # Run migrations on a fresh connection
    conn = get_db_connection()
    if conn:
        try:
            run_migrations(conn)
        except Exception as e:
            print(f"DB Init Error: {e}")
        finally:
            conn.close()



@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    mobile = data['mobile']
    
    # Use execute_query helper
    user = execute_query('SELECT * FROM users WHERE mobile = %s', (mobile,), fetchone=True)
    
    print(f"DEBUG LOGIN: Mobile='{mobile}' UserFound={user if user else 'None'}")
    
    if user:
        # Existing User (Patient or Doctor)
        # Check if Admin (Hardcoded for now based on plans, or just role check)
        return jsonify({"status": "success", "user": user})
    else:
        # New Patient Registration
        if 'name' not in data or 'age' not in data:
             return jsonify({"error": "Name and Age required for new registration"}), 400

        name = data['name']
        age = data['age']
        
        # Insert new user
        cursor = execute_query(
            'INSERT INTO users (name, age, mobile, role, department, status, queue_current, queue_total) VALUES (%s, %s, %s, %s, NULL, NULL, 0, 0)', 
            (name, age, mobile, 'patient'),
            commit=True
        )
        
        # Get ID of inserted user
        # Postgres uses RETURNING, SQLite uses last_insert_rowid()
        # My execute_query doesn't return ID easily for both.
        # Let's simple query back.
        user_new = execute_query('SELECT * FROM users WHERE mobile = %s', (mobile,), fetchone=True)
        
        return jsonify({"status": "success", "user": user_new})

# --- PUBLIC APIS ---

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    # Added mobile to query so frontend can use it for login ID
    doctors = execute_query('SELECT id, name, mobile, department, education, status, queue_current, queue_total, room_number, description FROM users WHERE role = %s', ('doctor',), fetchall=True)
    return jsonify(doctors)

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    mobile = request.args.get('mobile')
    if not mobile:
        return jsonify([])
    
    # Join with users to get real doctor name, and reports for follow_up_date
    query = '''
        SELECT 
            a.*,
            COALESCE(d.name, a.doctor_name, 'Assigned') as doctor_name,
            r.follow_up_date 
        FROM appointments a
        LEFT JOIN users d ON a.doctor_name = d.name AND d.role = 'doctor'
        LEFT JOIN reports r ON a.report_id = 'generated' AND a.id = r.appointment_id
        WHERE a.user_mobile = %s 
        ORDER BY a.id DESC
    '''
    appointments = execute_query(query, (mobile,), fetchall=True)
    
    return jsonify(appointments)

@app.route('/api/book', methods=['POST'])
def book_appointment():
    data = request.json
    
    execute_query(
        'INSERT INTO appointments (dept, doctor_name, date, status, user_mobile, report_id, patient_name, patient_age) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
        (data['dept'], data.get('doctor_name'), data['date'], 'Scheduled', data['mobile'], None, data.get('patient_name'), data.get('patient_age')),
        commit=True
    )
    
    # We need the ID for UI? The frontend might not use it immediately, but let's try to get it.
    # For now, return status success is enough as per old code logic (old code returned new_id, but frontend might ignore it).
    # To be safe, let's select max id for this user.
    last_apt = execute_query('SELECT id FROM appointments WHERE user_mobile = %s ORDER BY id DESC LIMIT 1', (data['mobile'],), fetchone=True)
    new_id = last_apt['id'] if last_apt else 0
    
    return jsonify({"status": "success", "id": new_id})

# --- DOCTOR API ---

@app.route('/api/admin/appointments') # Legacy or alternative path
def get_all_appointments_legacy():
    return get_all_appointments_admin()

@app.route('/api/admin/all_appointments')
def get_all_appointments_admin():
    query = '''
        SELECT 
            a.id, 
            a.date, 
            a.status, 
            a.dept,
            u.name as patient_name,
            u.mobile as patient_mobile,
            d.name as doctor_name
        FROM appointments a
        LEFT JOIN users u ON a.user_mobile = u.mobile
        LEFT JOIN users d ON a.doctor_name = d.name 
        ORDER BY a.date DESC
    '''
    # Note: joining on name for doctor might be fragile if names aren't unique, 
    # but based on schema, doctor_name is stored in appointments.
    
    results = execute_query(query, fetchall=True)
    return jsonify([dict(row) for row in results])

@app.route('/api/doctor/appointments', methods=['GET'])
def get_all_appointments():
    # Join with users to get patient names
    query = '''
        SELECT a.*, u.name as patient_name, u.age as patient_age, u.mobile as patient_mobile
        FROM appointments a
        LEFT JOIN users u ON a.user_mobile = u.mobile
        ORDER BY a.date DESC, a.id DESC
    '''
    appointments = execute_query(query, fetchall=True)
    return jsonify(appointments)

@app.route('/api/doctor/patient_history/<mobile>', methods=['GET'])
def get_patient_history(mobile):
    # Fetch all appointments for this mobile that are completed
    query = '''
        SELECT a.*, r.diagnosis, r.medicines, r.symptoms, r.follow_up_date 
        FROM appointments a
        LEFT JOIN reports r ON a.report_id = 'generated' AND a.id = r.appointment_id
        WHERE a.user_mobile = %s
        ORDER BY a.date DESC
    '''
    history = execute_query(query, (mobile,), fetchall=True)
    return jsonify(history)

@app.route('/api/doctor/report', methods=['POST'])
def save_report():
    # Handle both JSON and FormData (including urlencoded)
    if 'multipart/form-data' in request.content_type or 'application/x-www-form-urlencoded' in request.content_type:
        data = request.form
        file = request.files.get('file')
    else:
        # Assume JSON or try to parse it
        data = request.get_json(silent=True) or {}
        file = None

    apt_id = data['appointment_id']
    file_path = None

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        file_path = filename
    
    # Check if report exists
    existing = execute_query('SELECT id FROM reports WHERE appointment_id = %s', (apt_id,), fetchone=True)
    
    if existing:
        if file_path:
            execute_query(
                'UPDATE reports SET diagnosis = %s, medicines = %s, notes = %s, file_path = %s WHERE appointment_id = %s',
                (data['diagnosis'], data['medicines'], data['notes'], file_path, apt_id),
                commit=True
            )
        else:
            execute_query(
                'UPDATE reports SET diagnosis = %s, medicines = %s, notes = %s, symptoms = %s, follow_up_date = %s WHERE appointment_id = %s',
                (data['diagnosis'], data['medicines'], data['notes'], data.get('symptoms'), data.get('follow_up_date'), apt_id),
                commit=True
            )
    else:
        execute_query(
            'INSERT INTO reports (appointment_id, diagnosis, medicines, notes, file_path, symptoms, follow_up_date) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (apt_id, data['diagnosis'], data['medicines'], data['notes'], file_path, data.get('symptoms'), data.get('follow_up_date')),
            commit=True
        )
        
        # Update Appointment status
        execute_query(
            "UPDATE appointments SET status = 'Completed', report_id = %s WHERE id = %s", 
            ('generated', apt_id),
            commit=True
        )

    return jsonify({"status": "success"})

@app.route('/api/report/<int:apt_id>', methods=['GET'])
def get_report(apt_id):
    report = execute_query('SELECT * FROM reports WHERE appointment_id = %s', (apt_id,), fetchone=True)
    
    if report:
        return jsonify(report)
    else:
        return jsonify({"error": "Report not found"}), 404

@app.route('/api/appointments/<int:apt_id>', methods=['DELETE'])
def delete_appointment(apt_id):
    execute_query('DELETE FROM appointments WHERE id = %s', (apt_id,), commit=True)
    return jsonify({"status": "deleted"})

@app.route('/api/appointments/<int:apt_id>/confirm', methods=['POST'])
def confirm_appointment(apt_id):
    execute_query("UPDATE appointments SET status = 'Confirmed' WHERE id = %s", (apt_id,), commit=True)
    return jsonify({"status": "success"})

@app.route('/api/appointments/<int:apt_id>/cancel', methods=['POST'])
def cancel_appointment(apt_id):
    execute_query("UPDATE appointments SET status = 'Cancelled' WHERE id = %s", (apt_id,), commit=True)
    return jsonify({"status": "success"})

@app.route('/api/queue', methods=['GET'])
def get_queue_status():
    # Aggregate data from all doctors
    result = execute_query('SELECT SUM(queue_current) as current, SUM(queue_total) as total FROM users WHERE role = %s', ('doctor',), fetchone=True)
    
    # Check result type since SUM can return distinct types or None
    current = result['current'] if result and result.get('current') else 0
    total = result['total'] if result and result.get('total') else 0
    
    # Simple logic regarding wait time (e.g., 5 mins per patient in queue)
    # This is just a global average estimatation
    active_queue = total - current
    active_queue = active_queue if active_queue > 0 else 0
    wait_time = active_queue * 15 # default 15 mins per patient
    
    return jsonify({
        "current": int(current),
        "total": int(total),
        "waitTime": int(wait_time)
    })

# --- DOCTOR APIS ---

@app.route('/api/doctor/status', methods=['POST'])
def update_doctor_status():
    data = request.json
    doc_id = data.get('id')
    
    if 'status' in data:
        execute_query('UPDATE users SET status = %s WHERE id = %s', (data['status'], doc_id), commit=True)
    
    if 'queue_current' in data:
        execute_query('UPDATE users SET queue_current = %s WHERE id = %s', (data['queue_current'], doc_id), commit=True)
        
    if 'queue_total' in data:
        execute_query('UPDATE users SET queue_total = %s WHERE id = %s', (data['queue_total'], doc_id), commit=True)
        
    return jsonify({"message": "Status Updated"})


@app.route('/api/contact', methods=['POST'])
def save_contact_message():
    data = request.json
    execute_query(
        'INSERT INTO messages (name, subject, message) VALUES (%s, %s, %s)',
        (data.get('name', 'Anonymous'), data['subject'], data['message']),
        commit=True
    )
    return jsonify({"status": "success"})


@app.route('/api/doctor/messages', methods=['GET'])
def get_messages():
    msgs = execute_query('SELECT * FROM messages ORDER BY created_at DESC', fetchall=True)
    return jsonify(msgs)

@app.route('/api/messages/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    execute_query('DELETE FROM messages WHERE id = %s', (msg_id,), commit=True)
    return jsonify({"status": "deleted"})

# --- ADMIN API ---

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    # 1. Counts
    doc_count = execute_query('SELECT count(*) as count FROM users WHERE role = %s', ('doctor',), fetchone=True)['count']
    patient_count = execute_query('SELECT count(*) as count FROM users WHERE role = %s', ('patient',), fetchone=True)['count']
    appt_count = execute_query('SELECT count(*) as count FROM appointments', fetchone=True)['count']
    
    # 2. Revenue (Mock logic: Assuming $50 per completed appointment)
    completed_appts = execute_query("SELECT count(*) as count FROM appointments WHERE status = 'Completed'", fetchone=True)['count']
    revenue = completed_appts * 50
    
    # 3. Recent Activity (Last 5 appointments)
    recent = execute_query("SELECT a.id, a.date, a.status, u.name as patient_name FROM appointments a LEFT JOIN users u ON a.user_mobile = u.mobile ORDER BY a.id DESC LIMIT 5", fetchall=True)

    return jsonify({
        "doctors": doc_count,
        "patients": patient_count,
        "appointments": appt_count,
        "revenue": revenue,
        "recent_activity": recent
    })

@app.route('/api/admin/doctors', methods=['GET', 'POST', 'DELETE'])
def manage_doctors():
    if request.method == 'GET':
        doctors = execute_query('SELECT * FROM users WHERE role = %s', ('doctor',), fetchall=True)
        return jsonify(doctors)
    
    if request.method == 'DELETE':
        doc_id = request.args.get('id')
        execute_query('DELETE FROM users WHERE id = %s AND role = %s', (doc_id, 'doctor'), commit=True)
        return jsonify({"status": "deleted"})
        
    if request.method == 'POST':
        data = request.json
        # Add new doctor
        # Simple password generation (mobile as password for now)
        try:
            execute_query(
                "INSERT INTO users (name, age, mobile, role, department, education, status, queue_current, queue_total, room_number, description) VALUES (%s, %s, %s, 'doctor', %s, %s, 'Available', 0, 0, %s, %s)",
                (data['name'], 45, data['mobile'], data['department'], data.get('education', ''), data['room'], data['description']),
                commit=True
            )
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@app.route('/api/admin/patients', methods=['GET', 'DELETE'])
def manage_patients():
    if request.method == 'GET':
        patients = execute_query('SELECT * FROM users WHERE role = %s', ('patient',), fetchall=True)
        return jsonify(patients)

    if request.method == 'DELETE':
        patient_id = request.args.get('id')
        try:
            # First fetch the mobile number for cascade deletion
            user = execute_query('SELECT mobile FROM users WHERE id = %s AND role = %s', (patient_id, 'patient'), fetchone=True)
            if user:
                mobile = user['mobile']
                # Delete related reports if any
                apts = execute_query('SELECT id FROM appointments WHERE user_mobile = %s', (mobile,), fetchall=True)
                if apts:
                    for apt in apts:
                        execute_query('DELETE FROM reports WHERE appointment_id = %s', (apt['id'],), commit=True)
                # Delete appointments
                execute_query('DELETE FROM appointments WHERE user_mobile = %s', (mobile,), commit=True)
            
            # Finally, delete the actual patient user record
            execute_query('DELETE FROM users WHERE id = %s AND role = %s', (patient_id, 'patient'), commit=True)
            return jsonify({"status": "deleted"})
        except Exception as e:
            # If backend error happens, let frontend know
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/admin/all_appointments', methods=['GET'])
def get_admin_appointments():
    # Fetch all appointments with details
    query = '''
        SELECT a.*, u.name as patient_name, u.age as patient_age, u.mobile as patient_mobile
        FROM appointments a
        LEFT JOIN users u ON a.user_mobile = u.mobile
        ORDER BY a.date DESC, a.id DESC
    '''
    appointments = execute_query(query, fetchall=True)
    return jsonify(appointments)

# Run DB Init on Import (for Gunicorn/Render)
init_db_if_needed()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
