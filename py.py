import pytesseract
from PIL import Image

# Path to the image file
image_path = "testgrid.png"

# Open the image using PIL
image = Image.open(image_path)

# Convert the image to grayscale
# gray_image = image.convert("L")
# custom_config = r"-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-"


# Apply OCR using pytesseract
# text = pytesseract.image_to_string(image, config=custom_config)
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
