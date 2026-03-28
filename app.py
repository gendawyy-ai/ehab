from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_ehab_sherif'

DEFAULT_THEME = {
    "branding": {
        "site_title_suffix": "Premium Property Consultant",
        "meta_description": "Senior Property Consultant at NCB Developments. Find the best property investments in Egypt's New Capital.",
        "contact_email": "ehabsherif1310@gmail.com",
        "footer_rights_text": "All Rights Reserved."
    },
    "colors": {
        "primary": "#000000",
        "secondary": "#ff0000",
        "accent": "#ff0000",
        "text_light": "#ffffff",
        "text_dark": "#8892b0",
        "bg_light": "#ffffff",
        "bg_dark": "#000000"
    },
    "navigation": {
        "home_label": "Home",
        "projects_label": "Projects",
        "contact_label": "Contact"
    },
    "home": {
        "hero_title": "Elevate Your Investment",
        "hero_description": "Discover exclusive opportunities with NCB Developments. Expert guidance for your next premium property acquisition in the New Administrative Capital.",
        "hero_cta_text": "View All Projects",
        "hero_background_image": "https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1920&q=80",
        "offers_section_title": "Special & Seasonal Offers",
        "offers_section_description": "Take advantage of limited-time seasonal payment plans and exclusive discounts."
    },
    "projects_page": {
        "title": "Projects Menu",
        "description": "Explore our current developments and find the unit that suits your needs.",
        "card_cta_text": "Explore",
        "units_title": "Available Units & Payment Plans",
        "map_title": "Location Map"
    },
    "contact_page": {
        "hero_badge": "Get In Touch",
        "hero_title": "Contact Me",
        "hero_description": "I'm here to help you find the perfect property investment.",
        "hero_background_image": "https://images.unsplash.com/photo-1423666639041-f56000c27a9a?auto=format&fit=crop&w=1920&q=80",
        "form_title": "Approach Me",
        "form_description": "Fill out the form below, and I will contact you immediately via WhatsApp or Phone.",
        "submit_text": "Send Request"
    }
}


def deep_merge(defaults, overrides):
    merged = {}
    for key, value in defaults.items():
        override_value = overrides.get(key) if isinstance(overrides, dict) else None
        if isinstance(value, dict):
            merged[key] = deep_merge(value, override_value or {})
        else:
            merged[key] = override_value if override_value is not None else value

    if isinstance(overrides, dict):
        for key, value in overrides.items():
            if key not in merged:
                merged[key] = value

    return merged


def normalize_data(data):
    data.setdefault("consultant", {})
    data.setdefault("projects", [])
    data.setdefault("offers", [])
    data["theme"] = deep_merge(DEFAULT_THEME, data.get("theme", {}))
    return data

def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return normalize_data(json.load(f))

def save_data(data):
    data = normalize_data(data)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    data = load_data()
    return render_template(
        'index.html',
        consultant=data['consultant'],
        projects=data['projects'],
        offers=data.get('offers', []),
        theme=data['theme']
    )

@app.route('/projects')
def projects():
    data = load_data()
    return render_template(
        'projects.html',
        consultant=data['consultant'],
        projects=data['projects'],
        theme=data['theme']
    )

@app.route('/contact')
def contact():
    data = load_data()
    return render_template(
        'contact.html',
        consultant=data['consultant'],
        theme=data['theme']
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'Ehab' and password == 'Gendawi':
            session['user'] = 'Ehab'
            return redirect(url_for('admin'))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    data = load_data()
    return render_template('admin.html', data=data)

@app.route('/admin/save', methods=['POST'])
@login_required
def admin_save():
    new_data = request.json
    save_data(new_data)
    return jsonify({"success": True})

@app.route('/api/projects/<int:project_id>')
def get_project(project_id):
    data = load_data()
    project = next((p for p in data['projects'] if p['id'] == project_id), None)
    if project:
        return jsonify(project)
    return jsonify({"error": "Project not found"}), 404

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    # Mock subscription logic for lead generation
    return jsonify({"success": "Subscription successful. You will receive the latest offers via push notifications!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

