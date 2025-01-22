Staff_identification:
This is an AI Evaluation project. There are instances in video clips whereby persons with name tags (these are staff) walk in a room. The code identifies the clips in which the staff are present. Additionally,  it locates the coordinates of the persons with the name tag.

Setting Up the Environment
1) Install Python (ensure it's Python 3.12).
2) Create a Virtual Environment, type in terminal (bash):

   python -m venv venv
3) Activate the Virtual Environment:
- On macOS/Linux (in bash terminal type as follows):

source venv/bin/activate

- On Windows (in terminal type as follows):

venv\Scripts\activate

4) Install Dependencies:

pip install -r requirements.txt

5) Run the mainfunction.py file

Summary of code below:
1) This program detects staff wearing tags in a video by comparing each frame to multiple pre-loaded reference images. 
2) Each reference image is converted to grayscale, and template matching is applied to identify potential matches in 
   the video frames. 
3) When a match surpasses a confidence threshold, the program records the frame number and bounding box coordinates 
   of the detected area. 
4) Detected frames are visually highlighted with bounding boxes and displayed in real-time during video playback. 
5) Finally, the results, including detected frame indices and coordinates, are saved in a JSON file for further analysis.

How to Use:
1) Place the video file in the data folder.
2) Add reference images of the staff in the data folder.
3) Run the script.
4) View detection results in the displayed video window.
5) Check results.json to see the frames and the coordinates with the staff wearing the name tag.
