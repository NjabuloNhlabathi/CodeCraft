import cv2
import numpy as np

# Start the submarine's camera (0 is usually your built-in webcam)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
        
    # 1. Check Water "Murkiness" (Turbidity)
    # We do this by checking the contrast/sharpness of the image. 
    # Murky water scatters light, making the image blurry.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    murkiness_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # 2. Detect Foreign Materials (e.g., Rust, Algae, or Chemical Spills)
    # Convert to HSV color space which is much better for isolating specific colors
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Example: Looking for unnatural bright Orange/Red (Rust or Chemical leak)
    # You can change these numbers to detect neon green algae or white plastics!
    lower_hazard = np.array([10, 100, 100])
    upper_hazard = np.array([25, 255, 255])
    
    # Create a mask that only looks at the hazard colors
    mask = cv2.inRange(hsv, lower_hazard, upper_hazard)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Default safe status
    system_status = "CLEAR"
    status_color = (0, 255, 0) # Green

    # If the visibility score drops too low, the water is too murky
    if murkiness_score < 80: 
        system_status = "HIGH TURBIDITY (MURKY)"
        status_color = (0, 165, 255) # Orange Warning
        
    # Draw boxes around the detected foreign materials
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000: # Only trigger if the material patch is large enough
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, "FOREIGN MATERIAL DETECTED", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            system_status = "CONTAMINATION DETECTED"
            status_color = (0, 0, 255) # Red Alert!

    # Display the HUD (Heads Up Display) on the video feed
    cv2.putText(frame, f"STATUS: {system_status}", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
    cv2.putText(frame, f"Visibility Score: {int(murkiness_score)}", (20, 80), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Show the live scanner window
    cv2.imshow('M.I.M.I. Submarine Vision', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()