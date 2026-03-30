from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from pymongo import MongoClient
import certifi
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5500", "http://127.0.0.1:5500"]}})

@app.route('/')
def home():
    return "Backend is running successfully "
# ── MongoDB Connection (SSL fix for Windows) ───────────────────────────────────
MONGO_URI = (
    "mongodb+srv://dhanowarakansha_db_user:akansha123"
    "@cluster0.cgge4ms.mongodb.net/busDB"
    "?retryWrites=true&w=majority"
)

try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000
    )
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    client = None

db = client["busDB"] if client else None


# ── Seed buses ────────────────────────────────────────────────────────────────
def seed_buses():
    if db is None:
        return
    if db.buses.count_documents({"source": "Mumbai", "destination": "Pune"}) >= 11:
        print("✅ Buses already seeded.")
        return

    buses = [
        {
            "name": "Swift Luxury Express",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 1200, "travelDate": "2026-03-30",
            "reliability": 95, "type": "A/C Sleeper (2+1)",
            "departure": "21:45", "arrival": "05:15",
            "availableSeats": 32, "womenSafe": True, "specialFriendly": True,
            "bookedSeats": [],
            "safety_metrics": {"rating": 4.8, "womenRating": 4.9},
            "women_reviews": {"sos_rating": 4.7, "hygiene_rating": 4.8, "staff_rating": 4.9, "total_reviews": 312},
            "delay_data": {"avg_delay": 8, "max_delay": 25, "on_time_pct": 88, "cancel_pct": 1},
            "points": {
                "boarding": [
                    {"loc": "Dadar Station", "time": "21:45"},
                    {"loc": "Sion Circle", "time": "22:00"},
                    {"loc": "Kurla LBS Road", "time": "22:15"},
                    {"loc": "Vashi Navi Mumbai", "time": "22:40"},
                    {"loc": "Kharghar Sector 7", "time": "23:00"}
                ],
                "dropping": [
                    {"loc": "Wakad Bridge", "time": "03:30"},
                    {"loc": "Hinjewadi Phase 1", "time": "03:50"},
                    {"loc": "Baner Road", "time": "04:10"},
                    {"loc": "Shivajinagar Bus Stand", "time": "04:40"},
                    {"loc": "Swargate Terminal", "time": "05:15"}
                ]
            }
        },
        {
            "name": "Pune Rajdhani Express",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 950, "travelDate": "2026-03-30",
            "reliability": 88, "type": "A/C Seater (2+2)",
            "departure": "06:00", "arrival": "09:30",
            "availableSeats": 40, "womenSafe": True, "specialFriendly": True,
            "bookedSeats": [],
            "safety_metrics": {"rating": 4.5, "womenRating": 4.6},
            "women_reviews": {"sos_rating": 4.6, "hygiene_rating": 4.5, "staff_rating": 4.7, "total_reviews": 198},
            "delay_data": {"avg_delay": 12, "max_delay": 35, "on_time_pct": 82, "cancel_pct": 2},
            "points": {
                "boarding": [
                    {"loc": "Mumbai Central", "time": "06:00"},
                    {"loc": "Worli Sea Face", "time": "06:20"},
                    {"loc": "Sion Station", "time": "06:40"},
                    {"loc": "Kurla Terminal", "time": "07:00"},
                    {"loc": "Thane Station", "time": "07:30"}
                ],
                "dropping": [
                    {"loc": "Talegaon", "time": "08:30"},
                    {"loc": "Dehu Road", "time": "08:50"},
                    {"loc": "Pimpri Chinchwad", "time": "09:00"},
                    {"loc": "Shivajinagar", "time": "09:20"},
                    {"loc": "Pune Station", "time": "09:30"}
                ]
            }
        },
        {
            "name": "Deccan Gold Travels",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 700, "travelDate": "2026-03-30",
            "reliability": 80, "type": "Non-A/C Seater (2+2)",
            "departure": "07:30", "arrival": "11:00",
            "availableSeats": 50, "womenSafe": False, "specialFriendly": False,
            "bookedSeats": [],
            "safety_metrics": {"rating": 3.9, "womenRating": 3.7},
            "women_reviews": None,
            "delay_data": {"avg_delay": 20, "max_delay": 60, "on_time_pct": 65, "cancel_pct": 5},
            "points": {
                "boarding": [
                    {"loc": "Dadar TT Circle", "time": "07:30"},
                    {"loc": "Mahim Causeway", "time": "07:50"},
                    {"loc": "Chembur Naka", "time": "08:10"},
                    {"loc": "Vashi Station", "time": "08:35"},
                    {"loc": "Panvel Bus Stand", "time": "09:00"}
                ],
                "dropping": [
                    {"loc": "Urse Phata", "time": "10:00"},
                    {"loc": "Nigdi", "time": "10:20"},
                    {"loc": "Akurdi", "time": "10:35"},
                    {"loc": "Chinchwad", "time": "10:50"},
                    {"loc": "Kothrud", "time": "11:00"}
                ]
            }
        },
        {
            "name": "Orange City Cruiser",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 1500, "travelDate": "2026-03-30",
            "reliability": 97, "type": "A/C Sleeper (1+1)",
            "departure": "22:30", "arrival": "06:00",
            "availableSeats": 18, "womenSafe": True, "specialFriendly": True,
            "bookedSeats": [],
            "safety_metrics": {"rating": 4.9, "womenRating": 5.0},
            "women_reviews": {"sos_rating": 5.0, "hygiene_rating": 4.9, "staff_rating": 5.0, "total_reviews": 427},
            "delay_data": {"avg_delay": 4, "max_delay": 15, "on_time_pct": 96, "cancel_pct": 0},
            "points": {
                "boarding": [
                    {"loc": "Andheri West", "time": "22:30"},
                    {"loc": "Bandra Kurla Complex", "time": "22:50"},
                    {"loc": "Chunabhatti", "time": "23:10"},
                    {"loc": "Govandi", "time": "23:30"},
                    {"loc": "Kharghar Node 4", "time": "23:55"}
                ],
                "dropping": [
                    {"loc": "Wakad Phata", "time": "04:00"},
                    {"loc": "Aundh Road", "time": "04:20"},
                    {"loc": "Pashan", "time": "04:40"},
                    {"loc": "Karve Road", "time": "05:15"},
                    {"loc": "Katraj Bus Stand", "time": "06:00"}
                ]
            }
        },
        {
            "name": "Sahyadri Volvo Express",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 1100, "travelDate": "2026-03-30",
            "reliability": 92, "type": "A/C Semi-Sleeper (2+2)",
            "departure": "23:00", "arrival": "04:30",
            "availableSeats": 36, "womenSafe": True, "specialFriendly": True,
            "bookedSeats": [],
            "safety_metrics": {"rating": 4.7, "womenRating": 4.8},
            "women_reviews": {"sos_rating": 4.8, "hygiene_rating": 4.7, "staff_rating": 4.9, "total_reviews": 256},
            "delay_data": {"avg_delay": 6, "max_delay": 20, "on_time_pct": 91, "cancel_pct": 1},
            "points": {
                "boarding": [
                    {"loc": "Borivali East", "time": "23:00"},
                    {"loc": "Kandivali Station", "time": "23:15"},
                    {"loc": "Malad West", "time": "23:30"},
                    {"loc": "Goregaon Market", "time": "23:45"},
                    {"loc": "Jogeshwari Flyover", "time": "00:00"}
                ],
                "dropping": [
                    {"loc": "Bhosari", "time": "03:00"},
                    {"loc": "Vishrantwadi", "time": "03:20"},
                    {"loc": "Yerawada", "time": "03:45"},
                    {"loc": "Koregaon Park", "time": "04:10"},
                    {"loc": "Hadapsar", "time": "04:30"}
                ]
            }
        },
        {
            "name": "Western Express Liner",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 850, "travelDate": "2026-03-30",
            "reliability": 85, "type": "Non-A/C Sleeper (2+1)",
            "departure": "20:00", "arrival": "02:00",
            "availableSeats": 28, "womenSafe": False, "specialFriendly": False,
            "bookedSeats": [],
            "safety_metrics": {"rating": 4.1, "womenRating": 3.9},
            "women_reviews": None,
            "delay_data": {"avg_delay": 18, "max_delay": 50, "on_time_pct": 70, "cancel_pct": 3},
            "points": {
                "boarding": [
                    {"loc": "Borivali Bus Depot", "time": "20:00"},
                    {"loc": "Dahisar Toll", "time": "20:20"},
                    {"loc": "Mira Road Station", "time": "20:40"},
                    {"loc": "Bhayander East", "time": "21:00"},
                    {"loc": "Vasai Road", "time": "21:20"}
                ],
                "dropping": [
                    {"loc": "Lonavala", "time": "00:30"},
                    {"loc": "Khandala", "time": "00:50"},
                    {"loc": "Talegaon Dabhade", "time": "01:10"},
                    {"loc": "Ravet", "time": "01:35"},
                    {"loc": "Pimpri Bus Stand", "time": "02:00"}
                ]
            }
        },
        {
            "name": "Mumbai Pune Superfast",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 1350, "travelDate": "2026-03-30",
            "reliability": 93, "type": "A/C Sleeper (2+1)",
            "departure": "08:00", "arrival": "11:30",
            "availableSeats": 30, "womenSafe": True, "specialFriendly": True,
            "bookedSeats": [],
            "safety_metrics": {"rating": 4.6, "womenRating": 4.7},
            "women_reviews": {"sos_rating": 4.6, "hygiene_rating": 4.8, "staff_rating": 4.7, "total_reviews": 189},
            "delay_data": {"avg_delay": 7, "max_delay": 20, "on_time_pct": 90, "cancel_pct": 1},
            "points": {
                "boarding": [
                    {"loc": "CST Mumbai", "time": "08:00"},
                    {"loc": "Fort Area", "time": "08:15"},
                    {"loc": "Parel Station", "time": "08:30"},
                    {"loc": "Wadala", "time": "08:50"},
                    {"loc": "Govandi Station", "time": "09:10"}
                ],
                "dropping": [
                    {"loc": "Dapodi", "time": "10:30"},
                    {"loc": "Khadki", "time": "10:50"},
                    {"loc": "Deccan Gymkhana", "time": "11:05"},
                    {"loc": "Swargate", "time": "11:20"},
                    {"loc": "Kondhwa", "time": "11:30"}
                ]
            }
        },
        {
            "name": "GreenLine Travels",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 600, "travelDate": "2026-03-30",
            "reliability": 75, "type": "Non-A/C Seater (2+3)",
            "departure": "05:30", "arrival": "09:30",
            "availableSeats": 55, "womenSafe": False, "specialFriendly": False,
            "bookedSeats": [],
            "safety_metrics": {"rating": 3.5, "womenRating": 3.3},
            "women_reviews": None,
            "delay_data": {"avg_delay": 28, "max_delay": 75, "on_time_pct": 55, "cancel_pct": 7},
            "points": {
                "boarding": [
                    {"loc": "Kalyan Bus Stand", "time": "05:30"},
                    {"loc": "Dombivli Station", "time": "05:50"},
                    {"loc": "Ambivli", "time": "06:10"},
                    {"loc": "Titwala", "time": "06:30"},
                    {"loc": "Khopoli Junction", "time": "07:00"}
                ],
                "dropping": [
                    {"loc": "Kamshet", "time": "08:00"},
                    {"loc": "Dehu", "time": "08:30"},
                    {"loc": "Alandi Road", "time": "08:50"},
                    {"loc": "Chakan", "time": "09:10"},
                    {"loc": "Pune Nagar Road", "time": "09:30"}
                ]
            }
        },
        {
            "name": "Platinum Sleeper Coach",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 1800, "travelDate": "2026-03-30",
            "reliability": 99, "type": "A/C Sleeper (1+1) Premium",
            "departure": "22:00", "arrival": "04:00",
            "availableSeats": 14, "womenSafe": True, "specialFriendly": True,
            "bookedSeats": [],
            "safety_metrics": {"rating": 5.0, "womenRating": 5.0},
            "women_reviews": {"sos_rating": 5.0, "hygiene_rating": 5.0, "staff_rating": 5.0, "total_reviews": 503},
            "delay_data": {"avg_delay": 2, "max_delay": 10, "on_time_pct": 98, "cancel_pct": 0},
            "points": {
                "boarding": [
                    {"loc": "Juhu Beach Road", "time": "22:00"},
                    {"loc": "Santacruz West", "time": "22:15"},
                    {"loc": "Vile Parle East", "time": "22:30"},
                    {"loc": "Andheri Subway", "time": "22:45"},
                    {"loc": "Powai Lake Road", "time": "23:05"}
                ],
                "dropping": [
                    {"loc": "Magarpatta City", "time": "02:30"},
                    {"loc": "Kharadi IT Park", "time": "02:50"},
                    {"loc": "Viman Nagar", "time": "03:10"},
                    {"loc": "Kalyani Nagar", "time": "03:30"},
                    {"loc": "Sopan Baug", "time": "04:00"}
                ]
            }
        },
        {
            "name": "Konkan Coastal Rides",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 799, "travelDate": "2026-03-30",
            "reliability": 82, "type": "A/C Seater (2+2)",
            "departure": "14:00", "arrival": "18:00",
            "availableSeats": 44, "womenSafe": True, "specialFriendly": True,
            "bookedSeats": [],
            "safety_metrics": {"rating": 4.2, "womenRating": 4.3},
            "women_reviews": {"sos_rating": 4.5, "hygiene_rating": 4.3, "staff_rating": 4.6, "total_reviews": 143},
            "delay_data": {"avg_delay": 15, "max_delay": 40, "on_time_pct": 78, "cancel_pct": 2},
            "points": {
                "boarding": [
                    {"loc": "Nerul Station", "time": "14:00"},
                    {"loc": "Belapur CBD", "time": "14:20"},
                    {"loc": "Kharghar Hills", "time": "14:40"},
                    {"loc": "Kamothe", "time": "15:00"},
                    {"loc": "Panvel Highway", "time": "15:20"}
                ],
                "dropping": [
                    {"loc": "Warje", "time": "16:30"},
                    {"loc": "Bavdhan", "time": "16:50"},
                    {"loc": "Sus Road", "time": "17:10"},
                    {"loc": "Pashan Sus", "time": "17:30"},
                    {"loc": "Baner Gaon", "time": "18:00"}
                ]
            }
        },
        {
            "name": "Night Rider Express",
            "source": "Mumbai", "destination": "Pune",
            "baseFare": 999, "travelDate": "2026-03-30",
            "reliability": 90, "type": "A/C Semi-Sleeper (2+1)",
            "departure": "00:30", "arrival": "05:00",
            "availableSeats": 38, "womenSafe": True, "specialFriendly": False,
            "bookedSeats": [],
            "safety_metrics": {"rating": 4.4, "womenRating": 4.5},
            "women_reviews": {"sos_rating": 4.5, "hygiene_rating": 4.4, "staff_rating": 4.6, "total_reviews": 167},
            "delay_data": {"avg_delay": 10, "max_delay": 30, "on_time_pct": 85, "cancel_pct": 2},
            "points": {
                "boarding": [
                    {"loc": "Ghatkopar East", "time": "00:30"},
                    {"loc": "Vikhroli Parksite", "time": "00:50"},
                    {"loc": "Kanjurmarg Station", "time": "01:05"},
                    {"loc": "Bhandup Complex", "time": "01:20"},
                    {"loc": "Mulund Octroi", "time": "01:40"}
                ],
                "dropping": [
                    {"loc": "Moshi", "time": "03:30"},
                    {"loc": "Chikhali", "time": "03:50"},
                    {"loc": "Pradhikaran", "time": "04:10"},
                    {"loc": "Sangvi", "time": "04:30"},
                    {"loc": "Aundh Depot", "time": "05:00"}
                ]
            }
        }
    ]
    db.buses.insert_many(buses)
    print(f"✅ Seeded {len(buses)} buses into MongoDB!")

seed_buses()


# ── Helper ────────────────────────────────────────────────────────────────────
def str_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc


# ── Signup ────────────────────────────────────────────────────────────────────
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request body"}), 400
    name     = data.get("name", "").strip()
    email    = data.get("email", "").lower().strip()
    password = data.get("password", "")
    if not name or not email or not password:
        return jsonify({"message": "Name, email and password are required"}), 400
    if len(password) < 8:
        return jsonify({"message": "Password must be at least 8 characters"}), 400
    if db.users.find_one({"email": email}):
        return jsonify({"message": "An account with this email already exists"}), 400
    user = {
        "name": name, "email": email, "phone": "", "dob": "", "gender": "",
        "password": generate_password_hash(password), "history": []
    }
    db.users.insert_one(user)
    return jsonify({"message": "Account created successfully"}), 201


# ── Login ─────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request body"}), 400
    email    = data.get("email", "").lower().strip()
    password = data.get("password", "")
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    user = db.users.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Incorrect email or password"}), 401
    return jsonify({
        "id": str(user["_id"]), "name": user["name"], "email": user["email"],
        "phone": user.get("phone", ""), "dob": user.get("dob", ""),
        "gender": user.get("gender", ""), "history": user.get("history", [])
    }), 200


# ── Update Profile ────────────────────────────────────────────────────────────
@app.route('/update-profile', methods=['POST'])
def update_profile():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request body"}), 400
    try:
        user_oid = ObjectId(data.get("userId", ""))
    except Exception:
        return jsonify({"message": "Invalid user ID"}), 400

    update_fields = {}
    if data.get("name"):    update_fields["name"]   = data["name"].strip()
    if data.get("phone"):   update_fields["phone"]  = data["phone"].strip()
    if data.get("dob"):     update_fields["dob"]    = data["dob"].strip()
    if data.get("gender"):  update_fields["gender"] = data["gender"].strip()

    if not update_fields:
        return jsonify({"message": "No fields to update"}), 400

    result = db.users.update_one({"_id": user_oid}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify({"message": "User not found"}), 404

    user = db.users.find_one({"_id": user_oid})
    return jsonify({
        "id": str(user["_id"]), "name": user["name"], "email": user["email"],
        "phone": user.get("phone", ""), "dob": user.get("dob", ""),
        "gender": user.get("gender", ""), "history": user.get("history", [])
    }), 200


# ── Search ────────────────────────────────────────────────────────────────────
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request body"}), 400
    source      = data.get("source", "").strip()
    destination = data.get("destination", "").strip()
    travel_date = data.get("travelDate", "").strip()
    if not source or not destination or not travel_date:
        return jsonify({"message": "Source, destination and travelDate are required"}), 400
    query = {
        "source":      {"$regex": f"^{source}$", "$options": "i"},
        "destination": {"$regex": f"^{destination}$", "$options": "i"},
        "travelDate":  travel_date
    }
    buses = [str_id(b) for b in db.buses.find(query)]
    return jsonify(buses), 200


# ── Predict Delay ─────────────────────────────────────────────────────────────
@app.route('/predict-delay', methods=['POST'])
def predict_delay():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request body"}), 400
    bus_name = data.get("busName", "")
    traffic  = data.get("traffic", "medium")
    weather  = data.get("weather", "clear")
    bus = db.buses.find_one({"name": bus_name})
    if not bus:
        return jsonify({"message": "Bus not found"}), 404
    dd = bus.get("delay_data", {"avg_delay": 10, "max_delay": 30, "on_time_pct": 80, "cancel_pct": 2})
    avg_delay   = dd.get("avg_delay", 10)
    on_time_pct = dd.get("on_time_pct", 80)
    cancel_pct  = dd.get("cancel_pct", 2)
    traffic_mult = {"low": 0.7, "medium": 1.0, "high": 1.6}.get(traffic, 1.0)
    weather_mult = {"clear": 0.8, "rain": 1.3, "heavy rain": 1.9}.get(weather, 1.0)
    expected_delay = round(avg_delay * traffic_mult * weather_mult)
    base_prob = 100 - on_time_pct
    if traffic == "high":        base_prob += 15
    if weather == "rain":        base_prob += 10
    if weather == "heavy rain":  base_prob += 25
    delay_probability = min(int(base_prob), 99)
    if delay_probability < 25:   risk_level = "Low"
    elif delay_probability < 55: risk_level = "Medium"
    else:                        risk_level = "High"
    reasons = []
    if traffic == "high":        reasons.append("heavy traffic on route")
    if weather == "rain":        reasons.append("rainy conditions")
    if weather == "heavy rain":  reasons.append("heavy rainfall affecting road speed")
    if avg_delay > 15:           reasons.append("historically high average delays on this route")
    if cancel_pct > 4:           reasons.append("elevated cancellation history")
    if not reasons:              reasons.append("normal operating conditions expected")
    reason = "Delay likely due to " + " and ".join(reasons) + "."
    return jsonify({
        "expected_delay": f"{expected_delay} mins",
        "delay_probability": f"{delay_probability}%",
        "risk_level": risk_level,
        "reason": reason
    }), 200


# ── Smart Seats ───────────────────────────────────────────────────────────────
@app.route('/smart-seats', methods=['POST'])
def smart_seats():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request body"}), 400
    bus_name     = data.get("busName", "")
    gender_pref  = data.get("genderPreference", "no_preference")
    travel_type  = data.get("travelType", "no_preference")
    seat_pref    = data.get("seatPreference", "no_preference")
    booked_seats = data.get("bookedSeats", [])
    bus = db.buses.find_one({"name": bus_name})
    if not bus:
        return jsonify({"message": "Bus not found"}), 404
    total_seats  = 40
    window_seats = [f"S{i}" for i in [1,4,5,8,9,12,13,16,17,20,21,24,25,28,29,32,33,36,37,40]]
    aisle_seats  = [f"S{i}" for i in [2,3,6,7,10,11,14,15,18,19,22,23,26,27,30,31,34,35,38,39]]
    genders      = ["male", "female"]
    p_types      = ["solo", "family", "group"]
    noise_levels = ["low", "medium", "high"]
    occupancy = {}
    for i in range(1, total_seats + 1):
        sid = f"S{i}"
        if sid in booked_seats:
            occupancy[sid] = {"occupied": True, "passenger_type": random.choice(p_types), "gender": random.choice(genders), "noise_level": random.choice(noise_levels)}
        else:
            occupancy[sid] = {"occupied": False}
    scored = []
    for i in range(1, total_seats + 1):
        sid = f"S{i}"
        if occupancy[sid]["occupied"]:
            continue
        score = 50
        reasons_list = []
        if seat_pref == "window" and sid in window_seats:
            score += 20; reasons_list.append("window seat as preferred")
        elif seat_pref == "aisle" and sid in aisle_seats:
            score += 20; reasons_list.append("aisle seat as preferred")
        elif seat_pref == "no_preference":
            score += 10
        neighbour_ids = [f"S{i-1}", f"S{i+1}"]
        for nid in neighbour_ids:
            if nid in occupancy and occupancy[nid]["occupied"]:
                nb = occupancy[nid]
                if gender_pref == "female_only":
                    if nb["gender"] == "female":
                        score += 30; reasons_list.append("seated next to female passenger")
                    else:
                        score -= 50; reasons_list.append("male neighbour violates female-only preference")
                nl = nb.get("noise_level", "medium")
                pt = nb.get("passenger_type", "solo")
                if travel_type in ["quiet", "work"]:
                    if nl == "low":
                        score += 25; reasons_list.append("quiet neighbour ideal for your travel style")
                    elif nl == "high":
                        score -= 40; reasons_list.append("high-noise neighbour unsuitable for quiet travel")
                    if pt == "group":
                        score -= 20; reasons_list.append("group nearby may disturb")
                elif travel_type == "social":
                    if nl in ["medium", "high"]:
                        score += 15; reasons_list.append("social atmosphere nearby")
                elif travel_type == "sleep":
                    if nl == "low":
                        score += 25; reasons_list.append("quiet environment good for sleeping")
                    elif nl == "high":
                        score -= 35
        reason_str = (", ".join(reasons_list) if reasons_list else "Good general availability") + "."
        scored.append({"seat_number": sid, "match_score": score, "reason": reason_str.capitalize()})
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return jsonify({"recommended_seats": scored[:3]}), 200


# ── Finalize Booking ──────────────────────────────────────────────────────────
@app.route('/finalize-booking', methods=['POST'])
def finalize_booking():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request body"}), 400
    for field in ["userId", "busName", "seats", "totalAmount", "boarding", "dropping", "travelDate"]:
        if field not in data:
            return jsonify({"message": f"Missing field: {field}"}), 400
    try:
        user_oid = ObjectId(data["userId"])
    except Exception:
        return jsonify({"message": "Invalid user ID"}), 400
    booking = {
        "busName": data["busName"], "seats": data["seats"], "totalAmount": data["totalAmount"],
        "boarding": data["boarding"], "dropping": data["dropping"],
        "status": "Upcoming", "tripId": "SWFT" + str(ObjectId())[:6].upper(),
        "date": data["travelDate"],
        "passengers": data.get("passengers", [])
    }
    result = db.users.update_one({"_id": user_oid}, {"$push": {"history": booking}})
    if result.matched_count == 0:
        return jsonify({"message": "User not found"}), 404
    db.buses.update_one(
        {"name": data["busName"], "travelDate": data["travelDate"]},
        {"$push": {"bookedSeats": {"$each": data["seats"]}}}
    )
    return jsonify({"message": "Booking confirmed", "tripId": booking["tripId"]}), 200


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(port=5000, debug=True)