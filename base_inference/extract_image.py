import cv2
from PIL import Image


def save_image(image, image_name):
    Image.fromarray(image).save(image_name, quality = 20)


def main():

    video_path = '../videos/Rec_20200125_170152_211_S.mp4'

    # Define a video capture object
    cap = cv2.VideoCapture(video_path)


    cap.read()
    cap.read()
    cap.read()
    cap.read()
    cap.read()
    cap.read()
    cap.read()
    _, frame = cap.read()

    #img = Image.fromarray(frame)
    #img.show()
    save_image(frame, "frame_compresso.jpg")
    cap.release()


if __name__ == '__main__':
    main()













