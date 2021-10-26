#@title Imports and function definitions

# import the opencv library
import cv2
import time

# For running inference on the TF-Hub module.
import tensorflow as tf
import tensorflow_hub as hub

# For downloading the image.
import matplotlib.pyplot as plt

# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

from frame_slot import FrameSlot

import threading

def resize_image(raw_frame, new_width, new_height):
  
  pil_image = Image.fromarray(np.uint8(raw_frame))
  pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
  pil_image_rgb = pil_image.convert("RGB")

  img = tf.convert_to_tensor(pil_image_rgb, dtype=tf.uint8)
  converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

  return converted_img


def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
  """Adds a bounding box to an image."""
  draw = ImageDraw.Draw(image)
  im_width, im_height = image.size
  (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                ymin * im_height, ymax * im_height)
  draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
             (left, top)],
            width=thickness,
            fill=color)

  # If the total height of the display strings added to the top of the bounding
  # box exceeds the top of the image, stack the strings below the bounding box
  # instead of above.
  display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
  # Each display_str has a top and bottom margin of 0.05x.
  total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

  if top > total_display_str_height:
    text_bottom = top
  else:
    text_bottom = bottom + total_display_str_height
  # Reverse list and print from bottom to top.
  for display_str in display_str_list[::-1]:
    text_width, text_height = font.getsize(display_str)
    margin = np.ceil(0.05 * text_height)
    draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                    (left + text_width, text_bottom)],
                   fill=color)
    draw.text((left + margin, text_bottom - text_height - margin),
              display_str,
              fill="black",
              font=font)
    text_bottom -= text_height - 2 * margin


def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
  """Overlay labeled boxes on an image with formatted scores and label names."""
  colors = list(ImageColor.colormap.values())

  try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf", 25)
  except IOError:
    print("Font not found, using default font.")
    font = ImageFont.load_default()

  for i in range(min(boxes.shape[0], max_boxes)):
    if scores[i] >= min_score:
      ymin, xmin, ymax, xmax = tuple(boxes[i])
      display_str = "{}: {}%".format(class_names[i].decode("ascii"),
                                     int(100 * scores[i]))
      color = colors[hash(class_names[i]) % len(colors)]
      image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
      draw_bounding_box_on_image(
          image_pil,
          ymin,
          xmin,
          ymax,
          xmax,
          color,
          font,
          display_str_list=[display_str])
      np.copyto(image, np.array(image_pil))
  return image


def save_image(image, image_name):
  plt.grid(False)
  plt.imshow(image)
  plt.savefig(image_name)


def load_model_on_GPU(detector):
  
  img = np.zeros([856, 1280], np.uint8)
  img = resize_image(img, 1280, 856)
  run_detector(detector, img, setup = True)
  print("The model is ready")


# if Setup == True -> we are in the empty call, so no print required
def run_detector(detector, img, setup = False):
  
  start_time = time.time()
  result = detector(img)
  end_time = time.time()

  result = {key:value.numpy() for key,value in result.items()}

  if setup is False:
    print("Found %d objects." % len(result["detection_scores"]))
    print("Inference time: ", end_time-start_time)

    '''
    image_with_boxes = draw_boxes(
        resized_frame.numpy(), result["detection_boxes"],
        result["detection_class_entities"], result["detection_scores"]
        )
    '''
    #save_image(image_with_boxes, "result.jpg")
    

def consume(detector, fs, run_event):
  print("Consuming...") # DEBUG
  i = 0 # DEBUG

  while run_event.is_set():
    
    frame_object = fs.consume_frame()

    if frame_object == None:
        print("Frame slot was empty")
        time.sleep(1)
        continue
    
    img = resize_image(frame_object.raw_frame, 1280, 856)
    run_detector(detector, img)

    print("Analysed: ", str(i), "Frames, it was the one with id: ", frame_object.id) # DEBUG
    i = i + 1 # DEBUG

    # Attention: the frames analysed are not saved anywhere!
    frame_object.completion_timestamp = time.time()
    

def produce(fs, run_event): # TODO
  video_path = 'Rec_20200125_170152_211_S.mp4'

  # define a video capture object
  cap = cv2.VideoCapture(video_path)

  print("Producing...") # DEBUG
  i = 0 # DEBUG

  while cap.isOpened() and run_event.is_set():
    

    # Get a new frame
    ret, frame = cap.read()

    # No more frames
    if not ret:
      print("The frames of the video are finished -> Producer exiting")
      break

    fs.update_frame(frame)

    print("Inserted frame: ", str(i)) # DEBUG
    i = i + 1 # DEBUG
    time.sleep(0.5) # DEBUG

  # After the loop release the cap object
  cap.release()
    


def main():
  # Print Tensorflow version
  print(tf.__version__)

  # Check available GPU devices.
  print("The following GPU devices are available: %s" % tf.test.gpu_device_name())

  # Get the detector
  module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1" #@param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]
  detector = hub.load(module_handle).signatures['default']

  # Prepare the frameslot(s)
  fs = FrameSlot(1)
  
  # Event to terminate threads with ctrl + C
  run_event = threading.Event()
  run_event.set()

  # Preparing threads
  t_p = threading.Thread(target = produce, args = (fs, run_event))
  t_c = threading.Thread(target = consume, args = (detector, fs, run_event))

  # Load the detector on the GPU via a call on an empty tensor
  load_model_on_GPU(detector)

  
  t_p.start()
  time.sleep(.5)
  t_c.start()

  try:
      while 1:
          time.sleep(.1)
  except KeyboardInterrupt:
      print("attempting to close threads")
      run_event.clear()
      t_p.join()
      t_c.join()
      print("threads successfully closed")
  
  
if __name__ == '__main__':
  main()

