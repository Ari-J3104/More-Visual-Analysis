#dice

import numpy as np
import cv2
import random

height = 500
width = 500

image = np.zeros((height, width, 3), dtype=np.uint8)

spacing = 10

num_dices = random.randint(1, 6)

dice_values = [1, 2, 3, 4, 5, 6]

# Keep track of the positions of the previously placed dice
dice_positions = []

for i in range(num_dices):
    # Generate a new position for the dice that does not overlap with any of the existing dice
    while True:
        x = random.randint(0, width - 50)
        y = random.randint(0, height - 50)
        if all(abs(x - prev_x) > 50 + spacing or abs(y - prev_y) > 50 + spacing for prev_x, prev_y in dice_positions):
            break
    dice_positions.append((x, y))

    value = random.choice(dice_values)
    
    cv2.rectangle(image, (x, y), (x+50, y+50), (255, 255, 255), 2)
    
    if value in [1, 3, 5]:
        cv2.circle(image, (x+25, y+25), 5, (255, 255, 255), -1)
    if value in [2, 3, 4, 5, 6]:
        cv2.circle(image, (x+15, y+15), 5, (255, 255, 255), -1)
        cv2.circle(image, (x+35, y+35), 5, (255, 255, 255), -1)
    if value in [4, 5, 6]:
        cv2.circle(image, (x+35, y+15), 5, (255, 255, 255), -1)
        cv2.circle(image, (x+15, y+35), 5, (255, 255, 255), -1)
    
    




gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 50, 200)

contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

dice_values = []
for contour in contours:
    # Calculate the contour area
    area = cv2.contourArea(contour)
    
    # If the contour area is too small or too big, skip it
    if area < 1000 or area > 5000:
        continue
    
    # Approximate the contour as a polygon
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    
    # If the polygon has 4 corners, it's likely a dice
    if len(approx) == 4:
        # Crop the dice from the image
        x, y, w, h = cv2.boundingRect(contour)
        dice_image = gray[y:y+h, x:x+w]
        
        # Calculate the average pixel value of the dice image
        avg_value = np.average(dice_image)
        
        # Based on the average pixel value, determine the dice value
        if avg_value < 60:
            dice_value = 1
        elif avg_value < 70:
            dice_value = 2
        elif avg_value < 80:
            dice_value = 3
        elif avg_value < 85:
            dice_value = 4
        elif avg_value < 90:
            dice_value = 5
        else:
            dice_value = 6
        
        # Add the dice value to the list
        dice_values.append(dice_value)

print('Number of dices:', len(dice_values))
print('Dice values:', dice_values)

cv2.imshow('Dice Image', image)
cv2.waitKey(0)


