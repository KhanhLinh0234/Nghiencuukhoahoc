from flask import Flask, redirect, url_for, render_template

test = Flask (__name__)

@test.route('/')
def page():
    return render_template('page.html')



@test.route('/base')
def base():
    return render_template('base.html')

if __name__ == "__main__":
    test.run(debug=True)