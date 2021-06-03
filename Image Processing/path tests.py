import os

file_path = r"C:\Users\ahmed\Desktop\Capstone\New Data\Normal\March 19, 2021\N_100_cylinder_30_temp200.mp4"
file_name = os.path.splitext(file_path)[0] + "_frame%d.jpg"

print(file_name)