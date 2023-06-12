import cv2
import numpy as np
import motor as mM
import distance as dist

motor = mM.Motor(2, 3, 4, 17, 22, 27)
maxThrottle = -0.1

# Bestimmen der Kamera
cap = cv2.VideoCapture(0)

# Setzen des Bereiches der Box, um die Reaktionszeit des Roboters zu bestimmen
box_width = 20
box_height = 400

while True:
    distance = dist.distance()
    # Emfangen vom Kamera Bild
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    
    # Konvertieren der Farbe von HUE auf RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Bestimmen der unteren und oberen Grenze für die Farberkennung
    lower = np.array([0, 0, 0], dtype=np.uint8)
    upper = np.array([80, 90, 100], dtype=np.uint8)

    # Erstellen einer Maske um den augewählten Bereich
    mask = cv2.inRange(rgb, lower, upper)

    # Einsetzen von Morphologischen Operation im auf die Maske
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Suchen der Konturen im Bild
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filtern der größten Kontur
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)

        # bestimmen von der mitte der größten Konture
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0

        # erstellen von einem grünen Kreis in der Mitte der Kontur (Visualisierung)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Zeichnen der Konturen auf dem Bild (Visualisierung)
        cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)

        # Mittelpunkt bestimmen
        middle_point = (cx, cy)

        # Berechnen von den x und y Koordinaten der Box
        box_x = int(frame.shape[1] / 2- box_width / 2)
        box_y = int(frame.shape[0] / 2 - box_height / 2)

        # zeichnen der Box im Bild (Visualisierung)
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), (255, 0, 0), 2)

        # je nach dem wo sich der Mittelpunkt befindet fahre geradeaus, links, recht oder stoppe ggf.
        if box_x <= middle_point[0] <= box_x + box_width and box_y <= middle_point[1] <= box_y + box_height and distance >= 10:
            motor.move(maxThrottle, 0, 0)
            print("Forward")
        elif middle_point[0] < box_x and distance >= 10:
            motor.move(maxThrottle, 0.1, 0)
            print("Left")
        elif middle_point[0] > box_x + box_width and distance >= 10:
            motor.move(maxThrottle, -0.1, 0)
            print("Right")
        elif distance <= 10:
            motor.move(0, 0, 0)
            print("stop")
    # zeigen des Fensters auf dem Bildschirm
    cv2.imshow('Result', frame)

    # Schließe Fenster wenn der "q" Knopf gedrückt ist
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# gebe Kamera frei und schließe alle Fenster
cap.release()
cv2.destroyAllWindows()

