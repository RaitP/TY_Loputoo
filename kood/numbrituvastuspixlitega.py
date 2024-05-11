import cv2
import numpy as np
import os

# Global variables to store selected pixels and their colors
selected_pixels = []
color_labels_per_frame = []
selected_pixels_saved = [(593, 324), (658, 398), (642, 584), (561, 673), (507, 582), (512, 402), (574, 498), (863, 315), (946, 402), (927, 594), (854, 677), (761, 595), (795, 380), (865, 503), (1172, 324), (1240, 405), (1227, 597), (1150, 685), (1081, 602), (1099, 399), (1161, 510)]
selected_pixels_saved_vanem_2 = [(643, 292), (719, 375), (702, 574), (620, 648), (549, 569), (566, 361), (627, 471), (933, 296), (998, 378), (980, 565), (911, 646), (837, 568), (858, 376), (918, 475), (1234, 301), (1299, 384), (1284, 562), (1202, 655), (1133, 572), (1153, 378), (1218, 476)]
selected_pixels_saved_vanem_1 = [(637, 310), (708, 400), (695, 585), (607, 674), (543, 586), (548, 390), (619, 497), (919, 328), (987, 406), (972, 593), (896, 677), (822, 606), (840, 395), (902, 502), (1220, 327), (1291, 420), (1264, 605), (1185, 680), (1115, 602), (1142, 398), (1204, 506)]
selected_pixels_saved_vanem = [(638, 397), (703, 477), (688, 672), (613, 751), (545, 667), (561, 463), (625, 577), (922, 401), (989, 481), (968, 678), (899, 745), (830, 685), (840, 480), (907, 584), (1218, 409), (1285, 497), (1265, 679), (1188, 755), (1128, 694), (1134, 487), (1198, 596)]
selected_pixels_saved_orig = [(641, 419), (711, 498), (694, 687), (617, 767), (553, 679), (563, 481), (633, 594), (928, 420), (999, 504), (977, 696), (897, 773), (832, 692), (851, 497), (918, 598), (1228, 435), (1293, 518), (1270, 698), (1186, 780), (1128, 710), (1149, 502), (1204, 603)]

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
            threshold = 90# You can adjust this threshold as needed

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
    #cv2.namedWindow('Frame')
    #cv2.setMouseCallback('Frame', get_pixel_color)

    while True:
#         # Display the frame
#         cv2.imshow('Frame', frame)
#         
#         # Check for 'q' key press to quit
#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('q'):
#             break
#         elif key == ord('c'):
#             # Continue with saving color labels
        save_color_labels(frame_folder, frame_files, selected_pixels_saved)
        print("Color labels saved successfully.")
        break

    # Release all resources
    cv2.destroyAllWindows()


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
    
print(sum(watts)/ len(watts) )