import cv2
from djitellopy import Tello


def handle_video(drone, run_flag):
    drone.streamoff()
    drone.streamon()
    while run_flag.is_set():
        frame = drone.get_frame_read().frame
        if frame is not None:
            cv2.putText(frame, f"Battery: {drone.get_battery()} %", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Height: {drone.get_height} cm", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#            cv2.imshow("Tello Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Kein Bild vom Stream erhalten.")
    drone.streamoff()
    cv2.destroyAllWindows()