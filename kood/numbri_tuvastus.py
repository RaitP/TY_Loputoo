import cv2
import numpy as np
import os

# Global variables to store selected pixels and their colors
selected_pixels = []
color_labels_per_frame = []

def get_pixel_color(event, x, y, flags, param):
    global selected_pixels
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # Add the selected pixel coordinates
        selected_pixels.append((x, y))
        
        # Draw a circle on the clicked position
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('Frame', frame)

def save_color_labels(frame_folder, frame_files, selected_pixels):
    global color_labels_per_frame

    for frame_name in frame_files:
        # Read the frame
        frame_path = os.path.join(frame_folder, frame_name)
        frame = cv2.imread(frame_path)

        # Check if the frame was read successfully
        if frame is None:
            print(f"Error: Could not read frame '{frame_name}'.")
            continue

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # List to store color labels for this frame
        color_labels = []

        # Extract colors of selected pixels from the frame
        for pixel in selected_pixels:
            x, y = pixel
            color = gray_frame[y, x]

            # Define a threshold to determine if the color is dark or bright
            threshold = 70  # You can adjust this threshold as needed

            # If the color is below the threshold, it is considered dark (label 1), otherwise it is bright (label 0)
            if color < threshold:
                color_labels.append(1)
            else:
                color_labels.append(0)
        
        # Add color labels for this frame to the global list
        color_labels_per_frame.append(color_labels)

# Example usage
frame_folder = "frames"  # Change this to your frame folder

# List all files in the frame folder
frame_files = os.listdir(frame_folder)

# Select the first frame for pixel color selection
frame_name = frame_files[0]

# Read the frame
frame_path = os.path.join(frame_folder, frame_name)
frame = cv2.imread(frame_path)

# Check if the frame was read successfully
if frame is None:
    print(f"Error: Could not read frame '{frame_name}'.")
else:
    # Create a window and set a mouse callback function
    cv2.namedWindow('Frame')
    cv2.setMouseCallback('Frame', get_pixel_color)

    while True:
        # Display the frame
        cv2.imshow('Frame', frame)
        
        # Check for 'q' key press to quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            # Continue with saving color labels
            save_color_labels(frame_folder, frame_files, selected_pixels)
            print("Color labels saved successfully.")
            break

    # Release all resources
    cv2.destroyAllWindows()


print(color_labels_per_frame)


def segments_to_number(segments):
    segment_mapping = {
        (1, 1, 1, 1, 1, 1, 0): 0,
        (0, 1, 1, 0, 0, 0, 0): 1,
        (1, 1, 0, 1, 1, 0, 1): 2,
        (1, 1, 1, 1, 0, 0, 1): 3,
        (0, 1, 1, 0, 0, 1, 1): 4,
        (1, 0, 1, 1, 0, 1, 1): 5,
        (1, 0, 1, 1, 1, 1, 1): 6,
        (1, 1, 1, 0, 0, 0, 0): 7,
        (1, 1, 1, 1, 1, 1, 1): 8,
        (1, 1, 1, 1, 0, 1, 1): 9
    }
    
    for pattern, number in segment_mapping.items():
        if segments == list(pattern):
            return number
    return None  # If no match found

watts = []

# Example usage:
i = 1
for segments in color_labels_per_frame:
    result1 = segments_to_number(segments[0:7])
    result2 = segments_to_number(segments[7:14])
    result3 = segments_to_number(segments[14:])
    if result1 != None and result2 != None and result3 != None:
        print("The number is:", result1,result2,result3)
        print()
        number= (result1 * 10) + result2 + (result3/10)
        watts.append(number)
    else:
        print(segments[0:7])
        print(segments[7:14])
        print(segments[14:])
        print("pilt nr " + str(i))
    i+=1
    
print("summa")    
print(sum(watts)/ len(watts) )
print(selected_pixels)