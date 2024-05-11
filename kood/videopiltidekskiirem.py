import cv2
import os

def extract_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    # Initialize variables
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps) # Extract frame every second
    
    # Create an output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Loop through the video frames
    while True:
        ret, frame = cap.read()
        
        # Check if the frame is read successfully
        if not ret:
            break
        
        frame_count += 1
        
        # Save frame every second
        if frame_count % interval == 0:
            frame_name = f"frame_{frame_count // interval}.jpg"
            cv2.imwrite(os.path.join(output_folder, frame_name), frame)
        
        # Check for 'q' key press to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Example usage
video_path = "loputoo_67.mkv"
output_folder = "frames"
extract_frames(video_path, output_folder)
print("done")