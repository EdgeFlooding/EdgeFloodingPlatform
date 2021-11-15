# import the opencv library
import cv2
import time

def rescale_frame(frame, width, height):
    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


video_path = '../videos/Rec_20200207_142322_151_M.mp4'

# define a video capture object
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
total_num_frames = cap.get(7)
frame_count = 0

prev = 0

while cap.isOpened():

    time_elapsed = time.time() - prev

    if time_elapsed > 1./fps:
        print(time_elapsed)

        frame_count = frame_count + 1
        if frame_count == total_num_frames:
            print("Riparto da capo")
            frame_count = 1
            cap.release()
            cap = cv2.VideoCapture(video_path)

        # Get a new frame
        ret, frame = cap.read()

        #print(type(frame))

        # No more frames
        if not ret:
            break


        prev = time.time()
        cv2.imshow('frame_resized', rescale_frame(frame, 1280, 856))


    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()

