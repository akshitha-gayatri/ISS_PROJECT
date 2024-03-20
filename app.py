from flask import Flask, render_template, request, redirect, url_for, flash,session,Response,send_file
import json
import bcrypt
import mysql.connector
import jwt  
import base64
import time  
import cv2
import numpy as np
from io import BytesIO
from PIL import Image  # Import Pillow for image processing
import base64  # Import for base64 encoding
from urllib.request import urlretrieve
import io
import os
from moviepy.editor import ImageSequenceClip,concatenate_videoclips,ImageClip
import moviepy.editor
app = Flask(__name__)

app.secret_key = '$$$$##)($'
db = mysql.connector.connect(
    host="localhost",
    user="Nikhil",
    password="Nikhil@1234",
    database="mydatabase"
)
cursor =db.cursor()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Nikhil'
app.config['MYSQL_PASSWORD'] = 'Nikhil@1234'
app.config['MYSQL_DB'] = 'mydatabase'
mysq = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)


@app.route('/display')
def display():
    user_details = session.get('user_details')
    token = session.get('jwt_token')
    if user_details :
        username = user_details['username']
        payload = verify_jwt_token(token)
        if payload and payload['username'] == username:
            user_data = find_user_details(username)
            print(user_data)
    cursor = mysq.cursor()
    cursor.execute("SELECT image FROM Images WHERE user_name = %s", (username,))
    image_data = cursor.fetchall()
    cursor.close()
    uploaded_images = []
    for data in image_data:
        try:
            encoded_image = base64.b64encode(data[0]).decode('utf-8')
            uploaded_image = f"data:image/jpeg;base64,{encoded_image}"
            uploaded_images.append(uploaded_image)
        except Exception as e:
            print(f"Error decoding image data: {e}")
    return render_template('display.html', uploaded_images=uploaded_images)

db_params = {
    'host': 'localhost',
    'user': 'Nikhil',
    'password': 'Nikhil@1234',
    'database': 'mydatabase'
}

@app.route('/playaudio/<int:song_id>')
def playaudio(song_id):
    # Connect to the database
    connection = mysql.connector.connect(**db_params)
    cursor = connection.cursor()
    # Fetch the BlobData for the selected song
    cursor.execute("SELECT BlobData FROM AudioFiles WHERE id = %s", (song_id,))
    blob_data = cursor.fetchone()[0]
    # Close the database connection
    cursor.close()
    connection.close()
    return send_file(io.BytesIO(blob_data), mimetype='audio/mpeg')

@app.route('/dis')
def dis():
    user_details = session.get('user_details')
    token = session.get('jwt_token')
    if user_details :
        username = user_details['username']
        payload = verify_jwt_token(token)
        if payload and payload['username'] == username:
            user_data = find_user_details(username)
            print(user_data)
    cursor = mysq.cursor()
    cursor.execute("SELECT image FROM Images WHERE user_name = %s", (username,))
    image_data = cursor.fetchall()
    cursor.close()
    connection = mysql.connector.connect(**db_params)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, file_name FROM AudioFiles")
    songs = cursor.fetchall()
    cursor.close()
    connection.close()
    uploaded_images = []
    for data in image_data:
        try:
            encoded_image = base64.b64encode(data[0]).decode('utf-8')
            uploaded_image = f"data:image/jpeg;base64,{encoded_image}"
            uploaded_images.append(uploaded_image)
        except Exception as e:
            print(f"Error decoding image data: {e}")    
    return render_template('create.html',uploaded_images=uploaded_images,songs=songs)

from flask import jsonify  # Add this import for JSON responses
def generate_jwt_token(username):
    payload = {'username': username}
    secret_key = '$$$$##)($'
    expiration_time = 36000  # Set your desired expiration time in seconds
    token = jwt.encode({'exp': time.time() + expiration_time, **payload}, secret_key, algorithm='HS256')
    # Store token and user details in the session
    session['jwt_token'] = token
    session['user_details'] = {'username': username}
    return {'username': username, 'token': token}

@app.route('/upload', methods=['POST'])
def upload():
    user_details = session.get('user_details')
    token = session.get('jwt_token')
    if user_details:
        username = user_details['username']
        payload = verify_jwt_token(token)
        if payload and payload['username'] == username:
            user_data = find_user_details(username)
            print(user_data)
    if request.method == 'POST':
        print("yes")
        images = request.files.getlist('images')
        # print(images)
        try:
            cursor=mysq.cursor()
            # print(images)
            for image in images:
                image_bytes = image.read()
                # print(image_bytes)
                # print(username)
                cursor.execute("""
                    INSERT INTO Images (image, user_name)
                    VALUES (%s, %s)""", ((image_bytes), username))
                print("oo\n")
                mysq.commit()
            cursor.close()
            # mysq.connect().close()
            print("iMages uploaded")
            return redirect(url_for('uploadedimages'))
        except Exception as e:
            return f'An error occurred: {str(e)}'
    return 'No images were uploaded'

def verify_jwt_token(token):
    secret_key = '$$$$##)($'
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None 
    except jwt.InvalidTokenError:
        return None 

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cursor = db.cursor()
        if username == "admin" and password == "admin":
            # Fetch all usernames and emails from the database
            cursor.execute("SELECT Username, Email FROM users")
            users = [{'username': row[0], 'email': row[1]} for row in cursor.fetchall()]
            return render_template('admin.html', users=users)
        query = f'SELECT * FROM users WHERE Username="{username}"'
        cursor.execute(query)
        data = cursor.fetchone()
        if data and bcrypt.checkpw(password.encode(), data[2].encode()):
                # Generate JWT token and redirect to success route
                user_info = generate_jwt_token(username)
                session["user_details"] = {"username": username}
                session["jwt_token"] = user_info["token"]
                return redirect(url_for("success"))
        else:
            flash("Invalid credentials", "error")
            return render_template("m.html")
    session.pop("_flashes", None)
    return render_template("m.html")

def find_user_details(user_id):
    cursor.execute("SELECT * FROM users WHERE username = %s", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return {'username': user_data[1], 'email': user_data[2], 'password': user_data[3]}
    return None

@app.route('/success')
def success():
    token = session.get('jwt_token')
    if token:
        payload = verify_jwt_token(token)
        if payload:
            username = payload['username']
            print(username)
            user_data = find_user_details(username)
            return render_template('login.html', data=user_data, token=token)
        else:
            flash("Invalid or expired token", "error")
    else:
        flash("Token not provided", "error")
    return render_template('m.html')

@app.route('/',methods=['GET','POST'])
def strat():
     return render_template('m.html')
@app.route('/signi', methods=['GET', 'POST'])
def signi():
    user_data = request.args.get('user_data')
    data = json.loads(user_data)
    return render_template('login.html', data=data)  
@app.route('/display.html')
def display_page():
    token = request.args.get('token')
    if token:
        payload = verify_jwt_token(token)
        if payload:
            username = payload['username']
            user_data = find_user_details(username)
            print(user_data)
    return render_template('databasee.html', data=None,token=token) 

@app.route('/uploadedimages',methods=['GET','POST'])
def uploadedimages():
    print("uploaded\n")
    user_details = session.get('user_details')
    token = session.get('jwt_token')
    if user_details :
        username = user_details['username']
        payload = verify_jwt_token(token)
        if payload and payload['username'] == username:
            user_data = find_user_details(username)
            print(user_data)
    cursor = mysq.cursor()
    cursor.execute("SELECT image FROM Images WHERE user_name = %s", (username,))
    image_data = cursor.fetchall()
    print(image_data)
    cursor.close()
    uploaded_images = []
    for data in image_data:
        try:
            encoded_image = base64.b64encode(data[0]).decode('utf-8')
            uploaded_image = f"data:image/jpeg;base64,{encoded_image}"
            uploaded_images.append(uploaded_image)
        except Exception as e:
            print(f"Error decoding image data: {e}")
    return render_template('uploaded.html', uploaded_images=uploaded_images)
 
@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("Username already exists. Please choose a different username.", "error")
            return render_template('m.html')
        salt_hash = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password.encode(), salt_hash)
        # Insert the new user if the username is unique
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hash_password))
        mysq.commit()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        data1 = cursor.fetchone()
        user_data = {'username': data1[1], 'email': data1[3], 'password': data1[2]}
        # Generate JWT token for the user information
        token = generate_jwt_token(username)
        # Redirect to a page where the token can be used, passing the token as a parameter
        return redirect(url_for("signi", user_data=json.dumps(user_data), token=token))
    session.pop('_flashes', None)
    return render_template('m.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return render_template('m.html')

def generate_video(selected_images, photo_duration=2):
    temp_dir = 'temp_images'
    # Create the temporary directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)
    # Convert images to PNG format and save them in the temporary directory
    image_paths = []
    for i, image_data in enumerate(selected_images):
        try:
            # Extract the base64 encoded data (if applicable)
            if ',' in image_data:
                _, encoded_data = image_data.split(',')
                image_data = base64.b64decode(encoded_data)
            else:
                image_path = os.path.join(temp_dir, f'image_{i}.png')
                urlretrieve(image_data, image_path)  # Download image if URL
            image_path = os.path.join(temp_dir, f'image_{i}.png')
            with open(image_path, 'wb') as f:
                f.write(image_data)
            image_paths.append(image_path)
        except Exception as e:
            print(f"Error saving image {i}: {e}")
    # Create video from image sequence with individual clip durations
    clips = []
    for image_path in image_paths:
        clip = ImageClip(image_path).set_duration(photo_duration)
        clips.append(clip)
    clip = concatenate_videoclips(clips)
    # Generate video filename with timestamp for uniqueness
    video_filename = f'output_video_{int(time.time())}.mp4'  # Import time for timestamp
    video_path = os.path.join(temp_dir, video_filename)
    clip.write_videofile(video_path,fps=24)
    # Cleanup temporary images
    for filename in os.listdir(temp_dir):
        if filename.endswith('.png') and filename != video_filename:
            os.remove(os.path.join(temp_dir, filename))
    # Read the generated video as bytes
    with open(video_path, 'rb') as f:
        video_data = f.read()
        video_data_base64 = base64.b64encode(video_data).decode('utf-8')
    return jsonify({'videoData': video_data_base64})

@app.route('/create_video', methods=['POST'])
def create_video():
    try:
        selected_images = request.json.get('selectedImages', [])
        if len(selected_images) > 0:
            print(len(selected_images),end="\n")
            video_data = generate_video(selected_images)
            return video_data
        else:
            return jsonify({'error': 'No images provided'}), 400  # Handle missing images
    except Exception as e:
        print(f"Error creating video: {e}")
        return jsonify({'error': 'Internal server error'}), 500  # Handle internal errors                                                                                    

@app.route('/video',methods=['GET','POST'])
def video():
    # Get the selected images from the session
    selected_images = session.get('selected_images', [])
    print(selected_images)
    return render_template('video.html', selected_images=selected_images)

if __name__ == '__main__':
    app.run(debug=True, port=5565)