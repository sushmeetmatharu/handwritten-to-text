import cv2 as cv
import numpy as np
from PIL import Image
import pytesseract

# Set the Tesseract executable path if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def calculate_skew_angle(image):
    # Convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv.Canny(gray, 50, 150, apertureSize=3)
    
    # Use Hough Transform to detect lines
    lines = cv.HoughLines(edges, 1, np.pi / 180, 200)
    
    angles = []
    if lines is not None:
        for rho, theta in lines[:, 0]:
            angle = (theta * 180 / np.pi) - 90
            angles.append(angle)

    # Return the median angle to minimize the effect of outliers
    if angles:
        return np.median(angles)
    else:
        return 0

def rotate_image(rgb_image):
    # Calculate the skew angle
    angle = calculate_skew_angle(rgb_image)
    
    # Get the image dimensions
    rows, cols = rgb_image.shape[:2]
    
    # Get the rotation matrix and apply the rotation
    M_rotation = cv.getRotationMatrix2D((cols / 2, rows / 2), angle, 1.0)  # Use the calculated angle
    rotated_image = cv.warpAffine(rgb_image, M_rotation, (cols, rows))
    return rotated_image

def extract_text_from_image(image_path):
    # Load the image using OpenCV
    img = cv.imread(image_path)

    # Rotate the image to correct skewness
    img = rotate_image(img)

    # Convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding
    _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # Perform OCR on the processed image
    text = pytesseract.image_to_string(thresh)
    return text

# Alternative method using PIL
def extract_text_using_pil(image_path):
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img)
    return text
