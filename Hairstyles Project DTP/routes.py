from flask import Flask, render_template
import sqlite3  # Used to connect to the database

app = Flask(__name__)  # Create the Flask app

# Home page
@app.route('/')
def home():
    conn = sqlite3.connect('Hairstyles.db')
    cursor = conn.cursor()

    # Join Hairstyles with Images table to get image URLs
    cursor.execute("""
        SELECT Hairstyles.hairstyle_id, Hairstyles.hairstyle_name, Hairstyles.hairstyle_length, Images.image_url
        FROM Hairstyles
        JOIN Images ON Hairstyles.image_id = Images.image_id
        LIMIT 3
    """)
    hairstyles = cursor.fetchall()
    conn.close()

    return render_template('home.html', title='HOME', hairstyles=hairstyles)


# About me page
@app.route('/me')
def me():
    title = 'ME'
    return render_template('me.html', title=title)

@app.route('/all_hairstyles')
def all_hairstyles():
    conn = sqlite3.connect('Hairstyles.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT h.hairstyle_id, h.hairstyle_name, i.image_url
        FROM Hairstyles h
        LEFT JOIN Images i ON i.image_id = h.image_id
    """)
    hairstyles = cur.fetchall()
    conn.close()

    # Clean image paths (remove 'static/images/' if it's included in the DB)
    cleaned_hairstyles = []
    for h in hairstyles:
        image_filename = h[2].replace("static/images/", "") if h[2] else None
        cleaned_hairstyles.append((h[0], h[1], image_filename))

    return render_template('all_hairstyles.html', hairstyles=cleaned_hairstyles)


@app.route("/hairstyle/<int:id>")
def hairstyle(id):
    conn = sqlite3.connect('Hairstyles.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT h.hairstyle_id, h.hairstyle_name, h.hairstyle_length, h.hair_type, i.image_url
        FROM Hairstyles h
        LEFT JOIN Images i ON i.image_id = h.image_id
        WHERE h.hairstyle_id = ?
    """, (id,))
    hairstyle = cur.fetchone()
    print(hairstyle)
    conn.close()
    title = 'Hairstyle - ' + str(hairstyle[1])
    return render_template('hairstyles.html', title=title, hairstyle=hairstyle)


# List of all faceshapes
@app.route('/faceshapes')
def all_faceshapes():
    conn = sqlite3.connect('Hairstyles.db')
    cur = conn.cursor()
    cur.execute("SELECT faceshape_id, faceshape_name FROM Faceshapes")
    faceshapes = cur.fetchall()
    conn.close()
    return render_template('all_faceshapes.html', faceshapes=faceshapes)


# Hairstyles for a given faceshape
@app.route('/faceshape/<int:id>')
def faceshape(id):
    conn = sqlite3.connect('Hairstyles.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT h.hairstyle_id, h.hairstyle_name, i.image_url
        FROM Hairstyles h
        LEFT JOIN Images i ON i.image_id = h.image_id
        WHERE h.faceshape_id = ?
    """, (id,))
    hairstyles = cur.fetchall()

    # Get faceshape name for title
    cur.execute("SELECT faceshape_name FROM Faceshapes WHERE faceshape_id = ?", (id,))
    faceshape_name = cur.fetchone()
    conn.close()

    # Clean image paths
    cleaned_hairstyles = []
    for h in hairstyles:
        image_filename = h[2].replace("static/images/", "") if h[2] else None
        cleaned_hairstyles.append((h[0], h[1], image_filename))

    return render_template('faceshape_hairstyles.html', faceshape_name=faceshape_name[0], hairstyles=cleaned_hairstyles)


# Start the app
if __name__ == '__main__':
    app.run(debug=True)
