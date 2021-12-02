import tensorflow as tf
import tensorflow_hub as hub
import time
from PIL import Image
from PIL import ImageOps
import numpy as np
import threading



def resize_image(raw_frame, new_width, new_height):
    '''Transform frame into tensor for detector'''
    pil_image = Image.fromarray(np.uint8(raw_frame))
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")

    img = tf.convert_to_tensor(pil_image_rgb, dtype=tf.uint8)
    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

    return converted_img


def run_detector(detector, img):
    '''if setup == True -> we are in the empty call, so no print required'''

    start_time = time.time()
    result = detector(img)
    end_time = time.time()



def load_model_on_GPU(detector):
    '''To be called before actually using the detector on real frames'''

    img = np.zeros([856, 1280], np.uint8)
    img = resize_image(img, 1280, 856)
    run_detector(detector, img)
    print("The model is ready")

def use_GPU(index, detector, run_event):

    while not run_event.is_set():
        print("Thread " + str(index) + " in esecuzione")
        with tf.device('/device:GPU:' + str(index)):
            load_model_on_GPU(detector)


def main():

    module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"
    detectors = []
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        # Replicate your computation on multiple GPUs
        for gpu in gpus:
            #with tf.device(gpu.name):
            physical_string = gpu.name
            components = physical_string.split(':')
            try:
                with tf.device('/device:GPU:' + components[2]):
                    detector = hub.load(module_handle).signatures['default']
                    detectors.append(detector)
            except RuntimeError as e:
                print(e)
    

    print("Starting threads")
    run_event = threading.Event()
    th0 = threading.Thread(target = use_GPU, args = (0, detectors[0], run_event))
    th1 = threading.Thread(target = use_GPU, args = (1, detectors[1], run_event))

    th0.start()
    th1.start()

    try:
        while 1:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nattempting to close threads")
        run_event.set()

        # Waiting for threads to close
        th0.join()
        th1.join()
        print("threads successfully closed")
    


if __name__ == '__main__':
    main()