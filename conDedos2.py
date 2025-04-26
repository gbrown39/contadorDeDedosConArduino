import cv2
import mediapipe as mp
import serial
import time

# Configuración de MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

# Configuración de la cámara
cap = cv2.VideoCapture(0)  # 0 para la cámara predeterminada

# Configuración del puerto serial (¡CAMBIA ESTO AL PUERTO DE TU ARDUINO!)
arduino_port = 'COM3'        # Ejemplo para Windows
baud_rate = 9600
ser = None  # Inicializar la variable serial

try:
    ser = serial.Serial(arduino_port, baud_rate)
    print(f"Conexión serial establecida con Arduino en {arduino_port}")
except serial.SerialException as e:
    print(f"Error al conectar con Arduino: {e}")

def send_to_arduino(data):
    if ser and ser.is_open:
        try:
            ser.write(str(data).encode('utf-8'))
            time.sleep(0.1)  # Pequeña pausa para asegurar la transmisión
        except serial.SerialException as e:
            print(f"Error al enviar datos al Arduino: {e}")

if __name__ == "__main__":
    last_finger_count = -1  # Variable para evitar enviar datos repetidos

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Voltear la imagen horizontalmente para una vista más intuitiva
        image = cv2.flip(image, 1)

        # Convertir la imagen a RGB para MediaPipe
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Volver a convertir la imagen a BGR para OpenCV
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        finger_count = 0  # Inicializar el conteo de dedos

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar los puntos de referencia de la mano
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                fingers = []
                # Pulgar
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
                if thumb_tip.x < thumb_ip.x:  # Considera la orientación horizontal
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Otros dedos
                for finger_tip_id, finger_dip_id in [(mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_DIP),
                                                    (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_DIP),
                                                    (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_DIP),
                                                    (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_DIP)]:
                    if hand_landmarks.landmark[finger_tip_id].y < hand_landmarks.landmark[finger_dip_id].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                finger_count = sum(fingers)
                break  # Considerar solo la primera mano detectada si hay varias

        # Enviar el conteo al Arduino solo si ha cambiado
        if finger_count != last_finger_count:
            send_to_arduino(finger_count)
            last_finger_count = finger_count

        # Mostrar el conteo en la ventana
        cv2.putText(image, f"Dedos: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Mostrar la imagen con las detecciones
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(5) & 0xFF == 27:  # Presionar ESC para salir
            break

    # Liberar la cámara y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

    # Cerrar la conexión serial si está abierta
    if ser and ser.is_open:
        ser.close()
        print("Conexión serial cerrada.")