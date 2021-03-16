import datetime

from flask import Flask, render_template, request, make_response, session
from werkzeug.utils import redirect

from data import db_session
from data.Users import User
from data.news import News
from forms.user import RegisterForm
from forms.meal import MealOrder

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    # news = db_sess.query(News).filter(News.is_private != True)
    news = db_sess.query(News)
    return render_template("index.html", news=news, title='Передаваемый заголовок')


# @app.route("/cookie_test")
# def cookie_test():
#     visits_count = int(request.cookies.get("visits_count", 0))
#     res = make_response(render_template("entercount.html", cou=visits_count + 1))
#     res.set_cookie("visits_count", str(visits_count + 1), max_age=60 * 60 * 24 * 365 * 2)
#     return res

@app.route("/meal", methods=['GET', 'POST'])
def meal_test():
    print('НАЧАЛО обработки')
    data = session.get('data', "!")
    datas = data.split()
    form = MealOrder()
    if form.validate_on_submit():
        print('БЛОК')
        print("Заказ питания выполнен", form.klass.data, form.bufet.data, form.hot_meal.data)
        session['data'] = form.klass.data + ' ' + str(form.bufet.data) + ' ' + str(form.hot_meal.data)
        session.permanent = True
        print("Заказ питания выполнен", form.klass.data, form.bufet.data, form.hot_meal.data)
        res = make_response("Заказ питания выполнен")
    else:
        if datas[0] != "!":
            form.klass.data = datas[0]
            form.bufet.data = int(datas[1])
            form.hot_meal.data = int(datas[2])
        else:
            form.klass.data = "класс"
            form.bufet.data = 0
            form.hot_meal.data = 0
        res = make_response(render_template("meal.html", form=form))
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    session.permanent = True
    res = make_response(render_template("entercount.html", cou=visits_count + 1))
    return res


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.db")
    # user = User()
    # user.name = "Самоделкин"
    # user.about = "Куча поделок в арсенале"
    # user.email = "Samdel66@email.ru"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # user = User()
    # user.name = "Кричалкина"
    # user.about = "Постоянно будоражит население"
    # user.email = "kricha-Mufa@email.ru"
    # db_sess.add(user)
    # user = User()
    # user.name = "Мечтатель"
    # user.about = "Обзор театральных постановок"
    # user.email = "mecha.secha@yandex.ru"
    # db_sess.add(user)
    # db_sess.commit()
    # for u in db_sess.query(User).all():
    #     u.created_date = datetime.datetime.now()
    # db_sess.commit()
    # for u in db_sess.query(User).all():
    #     print(u)
    app.run()


if __name__ == '__main__':
    main()
