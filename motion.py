import cv2
import imutils
import datetime
import time

################################################################
cameraNo = 0  # CAMERA NUMBER
frameWidth = 640  # DISPLAY WIDTH
frameHeight = 480  # DISPLAY HEIGHT
#################################################################


cap = cv2.VideoCapture(cameraNo)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
firstFrame = None

while True:

    text = "None"
    success, img = cap.read()
    img = imutils.resize(img, width=500)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    if firstFrame is None:
        firstFrame = gray
        continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) < 200:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Motion Detected"
        # draw the text and timestamp on the frame
        cv2.putText(
            img,
            "Status: {}".format(text),
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            img,
            datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, img.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 255, 0),
            1,
        )
        cv2.imwrite(
            "saved-images/{}.jpg".format(
                str(datetime.datetime.now()).replace(".", "-").replace(":", "-")
            ),
            img,
        )

    cv2.putText(
        img,
        "Status: {}".format(text),
        (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 255),
        2,
    )
    cv2.putText(
        img,
        datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, img.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (0, 255, 0),
        1,
    )

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", img)
    # cv2.imshow("Thresh", thresh)
    # cv2.imshow("Frame Delta", frameDelta)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    if cv2.waitKey(1) & 0xFF == ord("r"):
        firstFrame = None
    if cv2.waitKey(1) & 0xFF == ord("s"):
        cv2.imwrite(
            "saved-images/{}.jpg".format(
                str(datetime.datetime.now()).replace(".", "-").replace(":", "-")
            ),
            img,
        )
