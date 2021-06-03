import cv2

image = cv2.imread(r'C:\Users\ahmed\Desktop\Capstone\Image Data\Normal\Feb 20, 2021\N_feb20_100_cube_30\N_feb20_100_cube_30_frame87.jpg')
print(image.shape)

imgCropped = image[0:224, 128:352]
print(imgCropped.shape)
cv2.imshow('cropped', imgCropped)
cv2.waitKey(0)