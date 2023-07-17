import cv2
import numpy as np
import pytesseract
from PIL import Image

# Load image
img = cv2.imread("testgrid.png")

# Add black border
border_size = 2
border_color = [0, 0, 0]  # Black color
img_with_border = cv2.copyMakeBorder(
    img,
    border_size,
    border_size,
    border_size,
    border_size,
    cv2.BORDER_CONSTANT,
    None,
    border_color,
)

# Save the image with border
cv2.imwrite("testgrid_border.png", img_with_border)

# Convert image to grayscale
gray = cv2.cvtColor(img_with_border, cv2.COLOR_BGR2GRAY)

# Perform Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Perform Hough Line Transform (parameters are threshold, rho resolution, and theta resolution)
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

# Draw lines on the image
for rho, theta in lines[:, 0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))

    cv2.line(img_with_border, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Save the image with lines
cv2.imwrite("testgrid_lines.png", img_with_border)

# Separate lines into horizontal and vertical
horizontal_lines = []
vertical_lines = []
for rho, theta in lines[:, 0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    if b > 0.5:  # horizontal line
        horizontal_lines.append((rho, theta, x0, y0))
    else:  # vertical line
        vertical_lines.append((rho, theta, x0, y0))


# Sort lines and merge close lines
def merge_lines(lines, threshold):
    if not lines:
        return []
    lines.sort()  # sort by rho
    merged_lines = [lines[0]]
    for current_line in lines[1:]:
        last_line = merged_lines[-1]
        if abs(current_line[0] - last_line[0]) < threshold:  # close lines
            merged_lines[-1] = (
                (last_line[0] + current_line[0]) / 2,
                (last_line[1] + current_line[1]) / 2,
                (last_line[2] + current_line[2]) / 2,
                (last_line[3] + current_line[3]) / 2,
            )  # average
        else:
            merged_lines.append(current_line)
    return merged_lines


horizontal_lines = merge_lines(horizontal_lines, threshold=20)
vertical_lines = merge_lines(vertical_lines, threshold=20)

# Draw merged lines
img_with_merged_lines = img_with_border.copy()
for lines in [horizontal_lines, vertical_lines]:
    for rho, theta, x0, y0 in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(img_with_merged_lines, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Save the image with merged lines
cv2.imwrite("testgrid_merged_lines.png", img_with_merged_lines)

print(len(horizontal_lines), len(vertical_lines))


num_cells = (len(horizontal_lines) - 1) * (len(vertical_lines) - 1)
print(num_cells)
