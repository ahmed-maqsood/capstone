import cv2

image = cv2.imread(r'C:\Users\ahmed\Desktop\Capstone\image tests\image test 4\frame84.jpg')#, cv2.IMREAD_GRAYSCALE)
image = image[0:224, 128:352]

#upper rectangle
image = cv2.rectangle(image, (0,0), (224,45), (0,0,0), -1)

#diagonal boundry lines
image = cv2.line(image, (165, 45), (115, 95), (0,0,0), 10)
image = cv2.line(image, (45, 45), (95, 95), (0,0,0), 10)

#filling between diagonal lines
image = cv2.line(image, (45, 45), (165, 45), (0,0,0), 10)
image = cv2.line(image, (55, 55), (155, 55), (0,0,0), 10)
image = cv2.line(image, (65, 65), (145, 65), (0,0,0), 10)
image = cv2.line(image, (75, 75), (135, 75), (0,0,0), 10)
image = cv2.line(image, (85, 85), (125, 85), (0,0,0), 10)
image = cv2.line(image, (95, 95), (115, 95), (0,0,0), 10)

cv2.imshow('test', image)
cv2.waitKey(0)