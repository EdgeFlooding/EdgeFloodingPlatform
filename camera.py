import grpc

# import the generated classes
import grpc_services_pb2
import grpc_services_pb2_grpc

# import the opencv library
import cv2
import time
import sys
import ipaddress
import base64

'''
This is a single thread producer script emulating a camera
Input: id of the frameslot for which it produces, Ip address of consumer 
Output: stream of frames to send to the consumer
Frames must be produced at the same frame rate of the mp4 video
and extracted cyclically
'''


def produce(stub, id_frame_slot, ip_consumer, channel):
    video_path = 'videos/Rec_20200125_170152_211_S.mp4'

    # Define a video capture object
    cap = cv2.VideoCapture(video_path)

    # For cyclical playback of videos
    total_num_frames = cap.get(7)
    frame_count = 0

    # To playback at the right framerate
    fps = cap.get(cv2.CAP_PROP_FPS)
    prev_update_timestamp = 0


    print("Producing...", str(id_frame_slot)) # DEBUG
    print("Waiting for server...")
    id_frame = 1

    while cap.isOpened():

        # How much time from the extraction of the last frame?
        time_elapsed = time.time() - prev_update_timestamp

        if time_elapsed > 1./fps: # Time to produce another frame

            frame_count = frame_count + 1

            if frame_count == total_num_frames: # For cyclical extraction
                print("========= Producer", str(id_frame_slot), "is restarting the video reproduction =======") # DEBUG
                frame_count = 1
                cap.release()
                cap = cv2.VideoCapture(video_path)

            # Get a new frame
            ret, frame = cap.read()

            # No more frames
            if not ret:
                print("The frames of the video are finished -> Producer",str(id_frame_slot), "exiting")
                break


            b64_frame = base64.b64encode(frame)
            frame_req = grpc_services_pb2.Frame(id=id_frame, id_slot=id_frame_slot, b64image=b64_frame, width=frame.shape[1],
             height=frame.shape[0], creation_timestamp=time.time())
            
            # make the call
            while True:
                try:
                    stub.HandleNewFrame(frame_req)
                except:
                    print(".")
                    time.sleep(5)
                    # recreate the channel
                    channel.close()
                    channel = grpc.insecure_channel(f'{ip_consumer}:5005')
                    stub = grpc_services_pb2_grpc.FrameProcedureStub(channel)
                    continue
                break

            prev_update_timestamp = time.time()

            print("Sent frame:", str(id_frame), "from producer", str(id_frame_slot)) # DEBUG
            id_frame = id_frame + 1


    # After the loop release the cap object
    cap.release()


def check_int(int_str):

    try:
        int(int_str)

    except ValueError:
        print("{} not an int!".format(int_str))
        return False

    return True


def check_ip_address(address_str):

    try:
        ip = ipaddress.ip_address(address_str)

        if not isinstance(ip, ipaddress.IPv4Address) and not isinstance(ip, ipaddress.IPv6Address):
            print("{} is not an IPv4 nor an IPv6 address".format(address_str))
            return False

    except ValueError:
        print("{} is an invalid IP address".format(address_str))
        return False

    return True


def main():

    # Check number of arguments
    n_arguments = len(sys.argv)
    if n_arguments != 3:
        exit("The number of argument is not correct\nPlease provide: ID frame slot and IP consumer node")

    # Check type of arguments
    if not check_int(sys.argv[1]) or not check_ip_address(sys.argv[2]):
        # Error prints are already in the check functions
        exit()

    id_frame_slot = int(sys.argv[1])
    ip_consumer = sys.argv[2]

    print("All good, extracting frames...")
    try:
        # open a gRPC channel
        channel = grpc.insecure_channel(f'{ip_consumer}:5005')
        # create a stub (client)
        stub = grpc_services_pb2_grpc.FrameProcedureStub(channel)
        produce(stub, id_frame_slot, ip_consumer, channel)
    except KeyboardInterrupt:
        exit("\nExiting...")
    except Exception as e:
        print(e)
        exit("Exiting...")


if __name__ == '__main__':
    main()
