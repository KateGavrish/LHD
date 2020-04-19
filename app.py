from flask import Flask, render_template, redirect, request
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User, Mistakes
from data.forms import *
from func_mod import *
import tensorflow

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/user_data.sqlite")
WORDS = []
ADMIN = [1]


@app.route('/', methods=['GET', 'POST'])
def index():
    global WORDS
    form = CheckForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.text.data:
            if current_user.is_authenticated:
                session = db_session.create_session()
                user = session.query(User).get(current_user.id)
                user.last = form.text.data
                session.commit()
            percent = pred(form.text.data)
            if percent == 'FAKE':
                percent = 100
            else:
                percent = 1
            WORDS = analyz(form.text.data)
            return redirect(f'/info/{percent}')
    return render_template('index_aut.html', form=form)


@app.route('/info/<int:a>', methods=['GET', 'POST'])
def info(a):
    form = MistakeForm()
    if request.method == 'POST' and form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).get(current_user.id)
        mistake = Mistakes()
        mistake.text = user.last
        mistake.comment = form.text.data
        session.add(mistake)
        session.commit()
        return redirect('/')
    return render_template('analitic.html', per=a, words=WORDS, form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form, message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.last = ''
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    else:
        return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/account')
@login_required
def account():
    if current_user.is_authenticated and current_user.id in ADMIN:
        session = db_session.create_session()
        mistakes = session.query(Mistakes).all()
        return render_template('account.html', mistakes=mistakes, count=len(mistakes))
    return redirect('/')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    if current_user.is_authenticated and current_user.id in ADMIN:
        session = db_session.create_session()
        mistakes = session.query(Mistakes).get(id)
        if mistakes:
            session.delete(mistakes)
            session.commit()
        return redirect('/account')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='127.0.0.1')

