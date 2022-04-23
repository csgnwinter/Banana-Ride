from Website import create_app

# This is the file where you run the program
app = create_app()

# Running flask app application
if __name__ == '__main__':
    # Running flask application
    app.run(debug=True)
