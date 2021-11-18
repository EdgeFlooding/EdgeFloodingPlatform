from PIL import Image
from PIL import ImageOps
import numpy as np
import time
import tensorflow as tf
import tensorflow_hub as hub


def run_detector(detector, img, setup = False):
    '''if setup == True -> we are in the empty call, so no print required'''

    start_time = time.time()
    result = detector(img)
    end_time = time.time()

    if setup is False:
        print("Found %d objects." % len(result["detection_scores"]))
        print("Inference time: ", end_time-start_time)

        
        result = {key:value.numpy() for key,value in result.items()}
        
        return result


def resize_image(raw_frame, new_width, new_height):
    '''Transform frame into tensor for detector'''
    pil_image = Image.fromarray(np.uint8(raw_frame))
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")

    img = tf.convert_to_tensor(pil_image_rgb, dtype=tf.uint8)
    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

    return converted_img


def load_model_on_GPU(detector):
    '''To be called before actually using the detector on real frames'''

    img = np.zeros([856, 1280], np.uint8)
    img = resize_image(img, 1280, 856)
    run_detector(detector, img, setup = True)
    print("The model is ready")

def main():

    image = Image.open('frame_prova.jpg')
    np_image = np.asarray(image)

    module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1" # "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
    detector = hub.load(module_handle).signatures['default']

    load_model_on_GPU(detector)

    img = resize_image(np_image, 1280, 856)
    run_detector(detector, img)





    












if __name__ == '__main__':
    main()
