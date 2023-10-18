from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField('Cafe location', validators=[URL()])
    cafe_open = StringField('Cafe open', validators=[DataRequired()])
    cafe_close = StringField('Cafe close', validators=[DataRequired()])
    cafe_rating = SelectField('Cafe rating', choices=[("☕"),("☕☕"),("☕☕☕"),("☕☕☕☕"),("☕☕☕☕☕")]
                              ,validators=[DataRequired()], )
    cafe_wifi = SelectField('Cafe wifi', validators=[DataRequired()],
                            choices=[("💪"),("💪💪"),("💪💪💪"),("💪💪💪💪"),("💪💪💪💪💪")])
    cafe_power = SelectField('Cafe power', validators=[DataRequired()],
                             choices=[("🔌"),("🔌🔌"),("🔌🔌🔌"),("🔌🔌🔌🔌"),("🔌🔌🔌🔌🔌")])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        add_data = [form.cafe_name.data, form.cafe_location.data, form.cafe_open.data, form.cafe_close.data,
                    form.cafe_rating.data, form.cafe_wifi.data, form.cafe_power.data]
        with open('cafe-data.csv', mode="a", encoding="utf-8",newline='') as file:
            writer = csv.writer(file)
            writer.writerow(add_data)

        with open('cafe-data.csv', encoding="utf-8") as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            list_of_rows = []
            for row in csv_data:
                list_of_rows.append(row)
            # print(list_of_rows)
        return render_template('cafes.html', cafes=list_of_rows)


    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        # print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
