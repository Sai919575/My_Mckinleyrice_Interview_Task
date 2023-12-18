#I used Python language for the given task
'''                                                              LogScrap 
Here, we are assigning a task to establish a WebSocket connection and play a live-streaming 
video
1st step : Make url request to http://3.16.113.127:8000/websocket_test/ and it doesn't return 
anything its will be in a loading state then proceed to the second step
2nd step : Establish a WebSocket connection using the following URL ws://3.16.113.127:8000/
ws/live_stream/1234/. The connection returns video bytes, and these bytes are utilized to play the 
video
Write a script for the above problem and send it
'''
#Open Source Computer Vision library used for working with video frames
import cv2
#working with WebSocket connections in Python specifically used to create a WebSocket client to establish a connection to a WebSocket server.
import websocket
#To import the NumPy library - work on arrays effectively
import numpy as np
#To work with binary data 
from io import BytesIO
import threading
import queue
#To hit the url
import requests

frame_queue = queue.Queue()
#comments
''' on_message function is a function for handling messages received through a WebSocket connection. It decodes binary image data, converts it into a frame,
and adds that frame to a queue for further processing or display. I used queue to separate the WebSocket communication and frame processing, which allows for 
more efficient and organized handling of the received frames.
'''
def on_message(ws, message)
    try:
        # Decode the binary data received from the WebSocket connection
        image_data = BytesIO(message)
        frame = cv2.imdecode(np.frombuffer(image_data.read(), dtype=np.uint8), cv2.IMREAD_COLOR)
        # Put the frame in the queue
        frame_queue.put(frame)
    except Exception as e:
        print(f"Error processing frame: {e}")
#if any error
def on_error(ws, error):
    print(f"Error: {error}")
#close
def on_close(ws, close_status_code, close_msg):
    print(f"Connection closed with status code {close_status_code}, message: {close_msg}")
    #cap.release()
    cv2.destroyAllWindows()
#Open 
def on_open(ws):
    print("Connection opened")
    # Start a thread to handle frame display
    display_thread = threading.Thread(target=display_frames)
    display_thread.start()

#function to display frames in the main thread
def display_frames():
    while True:
        # Get a frame from the queue
        frame = frame_queue.get()
        # Display the video frame
        cv2.imshow("Video", frame)
        cv2.waitKey(1)

def main():
    # Step 1: Make url request to http://3.16.113.127:8000/websocket_test/
      url_step1 = "http://3.16.113.127:8000/websocket_test/"
      response_step1 = requests.get(url_step1)  
      # Step 2: Establish a WebSocket connection
      url = "ws://3.16.113.127:8000/ws/live_stream/1234/"
      # Create a WebSocket connection
      websocket.enableTrace(True)  # Enable trace for debugging purposes
      ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
      ws.on_open = on_open

      #Run the WebSocket connection
      ws.run_forever()

if __name__ == "__main__":
    main()
