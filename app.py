from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        # Get the selected text from the request
        selected_text = request.json['selected_text']
        
        # Save the selected text to a file
        with open('selected_text.txt', 'w') as f:
            f.write(selected_text)

        # Run your Python code to generate the video
        subprocess.run(['python', 'main.py'])

        # Check if the video file was generated
        if os.path.exists('final_video.mp4'):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Video generation failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)