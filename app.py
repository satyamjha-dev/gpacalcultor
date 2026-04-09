from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Result, Review

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-goes-here'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Grading Logic Ported from gptcalculator.py (preserved)
def get_grade_point(marks):
    if marks >= 90: return 10
    elif marks >= 80: return 9
    elif marks >= 70: return 8
    elif marks >= 60: return 7
    elif marks >= 55: return 6
    elif marks >= 50: return 5.5
    elif marks > 40: return 5
    elif marks == 40: return 4
    else: return 0

def get_practical_gp(marks):
    if marks >= 45: return 10
    elif marks >= 39: return 9
    elif marks >= 35: return 8
    elif marks >= 30: return 7
    elif marks >= 25: return 6
    elif marks >= 22: return 5
    else: return 0

# --- Authentication Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login failed. Check your email and password.')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.')
            return redirect(url_for('signup'))
        new_user = User(email=email, password=generate_password_hash(password, method='scrypt'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    results = Result.query.filter_by(user_id=current_user.id).order_by(Result.timestamp.desc()).all()
    return render_template('dashboard.html', results=results)

@app.route('/rules')
def rules():
    return render_template('rules.html')

# --- GPA Routes (Modified for Login & Saving Results) ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sgpa', methods=['GET', 'POST'])
@login_required
def sgpa():
    if request.method == 'POST':
        try:
            n_theory = int(request.form.get('n_theory', 0))
            n_practical = int(request.form.get('n_practical', 0))
            total_weighted_gp = 0
            total_credits = 0
            
            for i in range(1, n_theory + 1):
                marks = float(request.form.get(f'th_marks_{i}', 0))
                credit = float(request.form.get(f'th_credit_{i}', 0))
                total_weighted_gp += get_grade_point(marks) * credit
                total_credits += credit
            
            for i in range(1, n_practical + 1):
                marks = float(request.form.get(f'pr_marks_{i}', 0))
                credit = float(request.form.get(f'pr_credit_{i}', 0))
                total_weighted_gp += get_practical_gp(marks) * credit
                total_credits += credit
            
            if total_credits > 0:
                result_val = round(total_weighted_gp / total_credits, 2)
                # Store in DB
                new_result = Result(type='SGPA', value=result_val, user_id=current_user.id)
                db.session.add(new_result)
                db.session.commit()
                return render_template('result.html', type='SGPA', result=result_val)
            return render_template('sgpa.html', error='Total credits must be greater than 0.')
        except ValueError:
            return render_template('sgpa.html', error='Invalid input values.')
    return render_template('sgpa.html')

@app.route('/cgpa', methods=['GET', 'POST'])
@login_required
def cgpa():
    if request.method == 'POST':
        try:
            n_sem = int(request.form.get('n_sem', 0))
            total_sgpa_weighted = 0
            total_sem_credits = 0
            
            for i in range(1, n_sem + 1):
                sgpa_val = float(request.form.get(f'sem_sgpa_{i}', 0))
                credits = float(request.form.get(f'sem_credit_{i}', 0))
                total_sgpa_weighted += sgpa_val * credits
                total_sem_credits += credits
            
            if total_sem_credits > 0:
                result_val = round(total_sgpa_weighted / total_sem_credits, 2)
                # Store in DB
                new_result = Result(type='CGPA', value=result_val, user_id=current_user.id)
                db.session.add(new_result)
                db.session.commit()
                return render_template('result.html', type='CGPA', result=result_val)
            return render_template('cgpa.html', error='Total credits must be greater than 0.')
        except ValueError:
            return render_template('cgpa.html', error='Invalid input values.')
    return render_template('cgpa.html')

# --- Review Routes ---

@app.route('/reviews')
def reviews():
    all_reviews = Review.query.order_by(Review.timestamp.desc()).all()
    user_review = None
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(user_id=current_user.id).first()
    return render_template('reviews.html', reviews=all_reviews, user_review=user_review)

@app.route('/add-review', methods=['POST'])
@login_required
def add_review():
    review_text = request.form.get('review_text')
    rating = request.form.get('rating')
    
    if not review_text or not rating:
        flash('Please provide both a review and a rating.')
        return redirect(url_for('reviews'))
    
    # Check if user already has a review
    existing_review = Review.query.filter_by(user_id=current_user.id).first()
    if existing_review:
        flash('You have already submitted a review. You can edit your existing one.')
        return redirect(url_for('reviews'))

    new_review = Review(review_text=review_text, rating=int(rating), user_id=current_user.id)
    db.session.add(new_review)
    db.session.commit()
    flash('Thank you for your feedback!')
    return redirect(url_for('reviews'))

@app.route('/edit-review/<int:id>', methods=['POST'])
@login_required
def edit_review(id):
    review = Review.query.get_or_404(id)
    if review.user_id != current_user.id:
        flash('You are not authorized to edit this review.')
        return redirect(url_for('reviews'))
    
    review_text = request.form.get('review_text')
    rating = request.form.get('rating')
    
    if review_text and rating:
        review.review_text = review_text
        review.rating = int(rating)
        db.session.commit()
        flash('Review updated successfully!')
    else:
        flash('All fields are required.')
        
    return redirect(url_for('reviews'))

@app.route('/delete-review/<int:id>', methods=['POST'])
@login_required
def delete_review(id):
    review = Review.query.get_or_404(id)
    if review.user_id != current_user.id:
        flash('You are not authorized to delete this review.')
        return redirect(url_for('reviews'))
    
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.')
    return redirect(url_for('reviews'))

# Initialize DB on start
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
