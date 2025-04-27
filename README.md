# contadorDeDedosConArduino
Este mini proyecto sirve para que por medio de la camara se pueda contar el numero de dedos de una mano que este levantada de 0 -5 y asi imprimirlo en la matris de 8x8 con ayuda de arduino uno.

descripcion
Sistema de Contador de dedos por camara de la computadora y con Arduino
Descripción del Proyecto
Este proyecto implementa un sistema de visión por computadora capaz de detectar el número de dedos levantados en una imagen de video en tiempo real. Luego, el número identificado es enviado a un Arduino mediante comunicación serial, donde se actualiza una matriz de LED 8x8 que muestra una suma acumulativa.
Componentes Utilizados
Software:
- Python 3.x (Lenguaje principal)
- OpenCV (pip install opencv-python) - Procesamiento de imágenes
- MediaPipe (pip install mediapipe) - Detección de manos y dedos
- PySerial (pip install pyserial) - Comunicación serial con Arduino
- Arduino IDE - Programación de la placa

Hardware:
- Placa Arduino UNO
- Matriz LED 8x8 (Controlada mediante la biblioteca LedControl)
- Resistencias y cables jumper
- Protoboard (Para pruebas y conexiones)


Funcionamiento
- Captura de video en tiempo real usando OpenCV.
- Procesamiento de imagen con MediaPipe para identificar una mano y contar los dedos levantados.
- Comparación y detección de cambios para evitar envíos repetidos de datos al Arduino.
- Envío del número de dedos al Arduino mediante comunicación serial (USB).
- Actualización de la matriz LED 8x8, donde el número recibido se agrega al valor acumulado.
