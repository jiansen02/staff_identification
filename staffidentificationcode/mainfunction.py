import cv2
import numpy as np
import json

"""
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

"""


# Paths to the video and reference images
video_path = "data/sampleA.mp4"
#these reference images contain multiple images used to reference the staff with a tag
reference_images = [
    "data/manA.png",  
    "data/manB.png",  
    "data/manC.png",  
    "data/manE.png",  
    "data/manF.png"   
]

# Load reference images
templates = []
for ref_path in reference_images:
    template = cv2.imread(ref_path, cv2.IMREAD_COLOR)
    if template is not None:
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        templates.append((template_gray, template.shape[1], template.shape[0]))  # Add width and height

# Initialize video capture
cap = cv2.VideoCapture(video_path)

# Output variables
detected_frames = []
coordinates = []

frame_index = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    best_match_val = 0
    best_bbox = None

    # Loop through all templates
    for template_gray, template_width, template_height in templates:
        # Perform template matching
        result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Update the best match if the current one is better
        if max_val > best_match_val:
            best_match_val = max_val
            best_bbox = (max_loc, (max_loc[0] + template_width, max_loc[1] + template_height))

    # Set a threshold for detection
    threshold = 0.67  # Adjust as needed
    if best_match_val >= threshold:
        # Save frame index and bounding box coordinates
        detected_frames.append(frame_index)
        coordinates.append({"frame": frame_index, "bbox": best_bbox})

        # Draw the bounding box on the frame (optional for visualization)
        cv2.rectangle(frame, best_bbox[0], best_bbox[1], (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Detected (Conf: {best_match_val:.2f})",
            (best_bbox[0][0], best_bbox[0][1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )

    # Show the frame (default playback speed)
    cv2.imshow("Staff Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):  # Wait 1ms for the next frame, adjust as needed
        break

    frame_index += 1

# Release resources
cap.release()
cv2.destroyAllWindows()

# Save results to a JSON file. These results have the frames and the coordinates of the staff wearing the tag.
results = {"detected_frames": detected_frames, "coordinates": coordinates}
with open("results.json", "w") as f:
     json.dump(results, f, indent=4)

