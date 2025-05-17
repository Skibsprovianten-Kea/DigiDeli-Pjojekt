from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path

bcrypt = None

def create_app():
    global bcrypt
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # Initialiserer extentions
    db.init_app(app)
    bcrypt = Bcrypt(app)
    
    return app

db = SQLAlchemy()
DB_NAME = 'users.db'
app = create_app()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)


    # Loginin manager setup
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

#from my_models import User, Note

    # Database laves
def create_database():
    if not path.exists(DB_NAME): #'website/' + 
        db.create_all()
        print('Created Database')
    else:
        print('Database already exists')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.is_admin:
                if bcrypt.check_password_hash(user.password, password):
                    print("Password correct, attempting to log in and redirect")
                    flash('Logged in successfully!', category='message')
                    login_user(user, remember=True)  
                    return redirect(url_for('back_index'))
                else:  # This else belongs to the password check
                    flash('Incorrect password!', category='error')
                    return redirect(url_for('index'))
            else:  # This else belongs to the admin check
                # Handle non-admin users here
                if bcrypt.check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='message')
                    login_user(user, remember=True)
                    return redirect(url_for('index'))  # or wherever non-admin users should go
                else:
                    flash('Incorrect password!', category='error')
                    return redirect(url_for('index'))       
                
        else: 
            flash('Email does not exist.', category='error')
            return render_template('login.html')
    return render_template('login.html')       

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form.get('brugernavn')
        email = request.form.get('email')
        password1 = request.form.get('password1') 
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
                flash('Email already exists.', category='error')
        elif len(username) < 2:
                flash('Brugernavn skal være længere end 2 tegn', category='error')
        elif len(email) < 4:
                flash('Email skal være længere end 4 tegn', category='error')
        elif password1 != password2:
                flash('Password matcher ikke', category='error')
        elif len(password1) < 7:
                flash('Password skal være længere end 7 tegn', category='error')
        else:
                # Create new user with hashed password
                hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Konto oprettet', category='message')
        return redirect(url_for('dashboard'))

    return render_template('sign_up.html')

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
def index():
    return render_template('index.html') 

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html') 

@app.route('/nyheder_1')
def nyheder_1():
    return render_template('nyheder_1.html')

@app.route('/nyheder_2')
def nyheder_2():
    return render_template('nyheder_2.html')

@app.route('/email')
def email():
    return render_template('email.html')

@app.route('/udvalg')
def udvalg():
    return render_template('udvalg.html')

@app.route('/weather')
def weather(): 
    return render_template('weather.html')

@app.route('/back_index')
def back_index(): 
    return render_template('back_index.html')
        
    return app

if __name__ == '__main__':
    #app = create_app()
    with app.app_context():
        create_database()
    app.run(host='0.0.0.0', debug=True)






"""  
      
def refresh_pictures():
    snaps_folder = "/home/sorent/kea/vhus/static/snaps/"
    if not os.path.exists(snaps_folder):
        print(f"Folder does not exist: {snaps_folder}")
        return []
    file_list = os.listdir(snaps_folder)
    pictures = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(snaps_folder, x)), reverse=True)
    return pictures[:3]

@app.route('/photo')
def shoot():
    try:
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(main={"size": (640, 480)})
        picam2.configure(config)
        picam2.start()
        day = dt.now()
        pic_name = f"{day.strftime('%d%m%y_%H%M%S')}.jpg"
        pic_path = os.path.join("/home/sorent/kea/vhus/static/snaps/", pic_name)
        os.makedirs(os.path.dirname(pic_path), exist_ok=True)
        picam2.capture_file(pic_path)
        picam2.close()
        pics = refresh_pictures()
        return render_template('photo.html', pics=pics, pic_name=pic_name)

    except Exception as e:
        return str(e), 500



"""

