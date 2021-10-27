import cv2
import os

censor = False

file_path = r"C:\Users\ahmed\Desktop\Capstone1\r2d2\raw\White_Pawn_R2D2_normal.mp4"

file_name = os.path.splitext(file_path)[0] + "_frame%d.jpg"

vidcap = cv2.VideoCapture(file_path)
success,image = vidcap.read()
count = 0
while success:
  #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  #image = image[35:259, 128:352]

  if(censor == True):
    #image = cv2.rectangle(image, (0, 0), (224, 45), (0, 0, 0), -1)
    # diagonal boundry lines
    image = cv2.line(image, (165, 45-45), (115, 95-45), (0, 0, 0), 10)
    image = cv2.line(image, (45, 45-45), (95, 95-45), (0, 0, 0), 10)
    # filling between diagonal lines
    image = cv2.line(image, (45, 45-45), (165, 45-45), (0, 0, 0), 10)
    image = cv2.line(image, (55, 55-45), (155, 55-45), (0, 0, 0), 10)
    image = cv2.line(image, (65, 65-45), (145, 65-45), (0, 0, 0), 10)
    image = cv2.line(image, (75, 75-45), (135, 75-45), (0, 0, 0), 10)
    image = cv2.line(image, (85, 85-45), (125, 85-45), (0, 0, 0), 10)
    image = cv2.line(image, (95, 95-45), (115, 95-45), (0, 0, 0), 10)

  cv2.imwrite(file_name % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1