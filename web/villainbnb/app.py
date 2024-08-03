from flask import Flask, request, render_template, redirect, url_for, flash, Blueprint, jsonify, abort
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests, secrets, os
from random import choice


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(8)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
FLAG = "SIVUSCG{fake_flag_for_testing}"


api_bp = Blueprint('api', __name__, url_prefix='/api')

def localhost_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.remote_addr != '127.0.0.1':
            return jsonify({'error': 'Access denied'}), 403
        return func(*args, **kwargs)
    return wrapper

@api_bp.route('/listings', methods=['GET'])
@localhost_only
def manage_listings():
    if request.method == 'GET':
        author_id = request.args.get('author_id')
        search_query = request.args.get('search')

        if search_query:
            listings = Listing.query.filter(
                Listing.name.ilike(f'%{search_query}%') |
                Listing.description.ilike(f'%{search_query}%')
            ).all()
        elif author_id:
            listings = Listing.query.filter_by(author_id=author_id).all()
        else:
            listings = Listing.query.all()
        listings_data = [{'id': l.id, 'name': l.name, 'description': l.description, 'image_url': l.image_url, 'author': l.author.username} for l in listings]
        return jsonify(listings_data)

    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        image_url = data.get('image_url')
        author_id = data.get('author_id')

        author = User.query.get(author_id)
        if author:
            new_listing = Listing(name=name, description=description, image_url=image_url, author=author)
            db.session.add(new_listing)
            db.session.commit()
            return jsonify({'message': 'Listing created successfully'}), 201
        else:
            return jsonify({'error': 'Invalid author ID'}), 400

@api_bp.route('/users', methods=['GET'])
@localhost_only
def get_users():
    username = request.args.get('username')
    if username:
        query = f"SELECT * FROM user WHERE username ='{username}'"
        users = db.session.execute(text(query)).fetchall()
        users_data = [{'id': u.id, 'username': u.username} for u in users]
        return jsonify(users_data)
    else:
        users = User.query.all()
        users_data = [{'id': u.id, 'username': u.username} for u in users]
        return jsonify(users_data)

@api_bp.route('/listings/<int:listing_id>', methods=['GET', 'PUT', 'DELETE'])
@localhost_only
def manage_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    if request.method == 'GET':
        listing_data = {'id': listing.id, 'name': listing.name, 'description': listing.description, 'image_url': listing.image_url, 'author': listing.author.username}
        return jsonify(listing_data)

    elif request.method == 'PUT':
        data = request.get_json()
        listing.name = data.get('name')
        listing.description = data.get('description')
        listing.image_url = data.get('image_url')
        db.session.commit()
        return jsonify({'message': 'Listing updated successfully'})

app.register_blueprint(api_bp)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    listings = db.relationship('Listing', backref='author', lazy='dynamic')

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Listing('{self.name}', '{self.description}', '{self.image_url}')"

class Flag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.Text, nullable=False)

def initialize_database():
    db.create_all()

    # Add initial listings
    admin_pass = secrets.token_hex(16)
    user = User(username='admin', password=admin_pass)
    print(f'Admin password is: {admin_pass}')
    db.session.add(user)
    db.session.commit()

    db.session.add(Listing(name="Volcano Lair", description="The ultimate hot spot! This fiery hideout inside an active volcano comes with a built-in lava jacuzzi. Perfect for those who like their plans as hot as their surroundings!", image_url="https://i.imgur.com/n9JEda4.png", author=user))
    db.session.add(Listing(name="Underwater Base", description="Submerge your schemes at this high-tech base deep beneath the ocean. Comes with an aquarium-style villain conference room—watch out for the shark that likes to eavesdrop!", image_url="https://i.imgur.com/WTPlCEU.png", author=user))
    db.session.add(Listing(name="Haunted Castle", description="This spooky medieval castle is not just haunted with ghosts but also with eerily good WiFi. Secret passages lead to a dungeon disco that's perfect for undead dance-offs!", image_url="https://i.imgur.com/43HHyMm.png", author=user))
    db.session.add(Listing(name="Doomsday Diner", description="Enjoy a villainous feast at this retro diner, complete with a secret lair beneath the jukebox. Perfect for plotting over a milkshake!", image_url="https://i.imgur.com/PrnewrF.png", author=user))
    db.session.add(Listing(name="The Hollowed-Out Mountain", description="Channel your inner supervillain in this classic hollowed-out mountain. Includes an echo chamber for practicing your maniacal laugh.", image_url="https://i.imgur.com/71dDJ72.png", author=user))
    db.session.add(Listing(name="The Submarine Sandwich", description="Dive deep in this underwater sub that doubles as a sandwich shop. Perfect for villains who like their plans with a side of pickles.", image_url="https://i.imgur.com/IxiofPQ.png", author=user))
    db.session.add(Listing(name="The Moon Base Bounce", description="Leap high with low gravity in this lunar base. Comes equipped with a giant laser, because why not?", image_url="https://i.imgur.com/XQyz6em.png", author=user))
    db.session.add(Listing(name="Underworld Upside-Down House", description="Turn your villainy on its head in this topsy-turvy house located in the underworld. Warning: May cause disorientation.", image_url="https://i.imgur.com/fFc2X3a.png", author=user))
    db.session.add(Listing(name="The Abandoned Amusement Park", description="Enjoy eerie rides and creepy clowns at your very own amusement park. Great for scare tactics and hide-and-seek.", image_url="https://i.imgur.com/TKGb594.png", author=user))
    db.session.add(Listing(name="Frosty Fortress", description="Chill out in this ice castle on a secluded glacier. Ice sculptures of famous villains included!", image_url="https://i.imgur.com/NJED2R4.png", author=user))
    db.session.add(Listing(name="The Forgotten Library", description="Surround yourself with ancient tomes and forbidden knowledge in a library that time forgot. Dusty, with a hint of mystery!", image_url="https://i.imgur.com/gbWM3NC.png", author=user))
    db.session.add(Listing(name="Catacomb Café", description="Sip espresso among the skulls in this charmingly macabre Parisian café. Bonuses include a labyrinthine basement perfect for escaping heroes.", image_url="https://i.imgur.com/FeHQxzp.png", author=user))
    db.session.add(Listing(name="The Invisible Cottage", description="Disappear into thin air at this completely invisible cottage, hidden in plain sight. Ideal for those seeking ultimate privacy.", image_url="https://i.imgur.com/G8gengl.png", author=user))

    db.session.add(Flag(flag=FLAG))
    db.session.commit()

def validate_image_url(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type')
        if content_type and 'image' in content_type:
            return True
        else:
            return response.text
    except requests.exceptions.RequestException:
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query')
    
    if search_query:
        listings = Listing.query.filter(
            Listing.name.ilike(f'%{search_query}%') |
            Listing.description.ilike(f'%{search_query}%')
        ).all()
    else:
        listings = Listing.query.all()
    
    return render_template('search.html', listings=listings, search_query=search_query)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form['image_url']

        valid_img = validate_image_url(image_url)

        if valid_img != True:
            flash(f'Invalid image URL. Please provide a valid image URL.\n\nResponse was:\n\n{valid_img}', 'danger')
            return redirect(url_for('create_listing'))

        new_listing = Listing(name=name, description=description, image_url=image_url, author=current_user)
        db.session.add(new_listing)
        db.session.commit()
        flash('Listing created successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('create_listing.html')

@app.route('/listings')
@login_required
def user_listings():
    api_url = f"http://127.0.0.1:5000/api/listings?author_id={current_user.id}"
    response = requests.get(api_url)
    listings = response.json()
    return render_template('user_listings.html', listings=listings)

@app.route('/')
def index():
    listings = Listing.query.all()
    listing = choice(listings)
    return render_template('index.html', listing=listing)

@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html'), 401

@app.route('/listings/<int:listing_id>/update', methods=['GET', 'POST'])
@login_required
def update_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.author != current_user:
        abort(403)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form['image_url']

        valid_img = validate_image_url(image_url)

        if valid_img != True:
            flash(f"Invalid image URL. Please provide a valid image URL.\n\nResponse was:\n\n{valid_img}", 'danger')
            return redirect(url_for('update_listing', listing_id=listing_id))

        listing_data = {
            'id': listing_id,
            'name': name,
            'description': description,
            'image_url': image_url,
            'author_id': current_user.id
        }

        api_url = f"http://127.0.0.1:5000/api/listings/{listing_id}"
        response = requests.put(api_url, json=listing_data)

        if response.status_code == 200:
            flash('Listing updated successfully!', 'success')
            return redirect(url_for('user_listings'))
        else:
            flash('Failed to update listing. Please try again.', 'danger')

    return render_template('update_listing.html', listing=listing)


if __name__ == '__main__':
    db_file = os.path.join(app.root_path, 'instance', 'listings.db')
    if not os.path.exists(db_file):
        with app.app_context():
            initialize_database()
    app.run(host='0.0.0.0', debug=True, port=5000)
