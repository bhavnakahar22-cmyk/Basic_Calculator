from flask import Flask, render_template, request

app = Flask(__name__)
print('Bhavna')
@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    error = None

    if request.method == "POST":
        expression = request.form.get("expression", "")

        try:
            result = eval(expression)
        except ZeroDivisionError:
            error = "Cannot divide by zero!"
        except:
            error = "Invalid expression!"
            result = ""

    return render_template("calculator.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
