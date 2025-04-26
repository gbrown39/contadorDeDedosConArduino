#include <LedControl.h>

// Configuración de pines para la matriz (DIN = 12, CS = 11, CLK = 10)
LedControl matriz = LedControl(12, 10, 11, 1);

void setup() {
  Serial.begin(9600);
  matriz.shutdown(0, false);     // Activa la matriz
  matriz.setIntensity(0, 8);     // Configura el brillo (0-15)
  matriz.clearDisplay(0);       // Limpia la matriz
}

void loop() {
  if (Serial.available() > 0) {
    int received_data = Serial.parseInt();
    if (received_data >= 0 && received_data <= 5) {
      displayNumber(received_data);
    }
    // Limpiar el buffer serial después de leer
    while (Serial.available() > 0) {
      Serial.read();
    }
  }
  // Aquí puedes agregar otras tareas que necesite realizar tu Arduino
}

// Función para mostrar un número en la matriz (0-5)
void displayNumber(int num) {
  matriz.clearDisplay(0);
  switch (num) {
    case 0:
      matriz.setRow(0, 0, B00111110);
      matriz.setRow(0, 1, B01000010);
      matriz.setRow(0, 2, B01000010);
      matriz.setRow(0, 3, B01000010);
      matriz.setRow(0, 4, B01000010);
      matriz.setRow(0, 5, B01000010);
      matriz.setRow(0, 6, B01000010);
      matriz.setRow(0, 7, B00111110);
      break;
    case 1:
      matriz.setRow(0, 0, B00000100);
      matriz.setRow(0, 1, B00001100);
      matriz.setRow(0, 2, B00000100);
      matriz.setRow(0, 3, B00000100);
      matriz.setRow(0, 4, B00000100);
      matriz.setRow(0, 5, B00000100);
      matriz.setRow(0, 6, B00000100);
      matriz.setRow(0, 7, B00000100);
      break;
    case 2:
      matriz.setRow(0, 0, B00111110);
      matriz.setRow(0, 1, B01000010);
      matriz.setRow(0, 2, B00000010);
      matriz.setRow(0, 3, B00001100);
      matriz.setRow(0, 4, B00010000);
      matriz.setRow(0, 5, B01000000);
      matriz.setRow(0, 6, B01111110);
      matriz.setRow(0, 7, B00000000);
      break;
    case 3:
      matriz.setRow(0, 0, B00111110);
      matriz.setRow(0, 1, B01000010);
      matriz.setRow(0, 2, B00000010);
      matriz.setRow(0, 3, B00111110);
      matriz.setRow(0, 4, B00000010);
      matriz.setRow(0, 5, B01000010);
      matriz.setRow(0, 6, B00111110);
      matriz.setRow(0, 7, B00000000);
      break;
    case 4:
      matriz.setRow(0, 0, B00011100);
      matriz.setRow(0, 1, B00100100);
      matriz.setRow(0, 2, B01000100);
      matriz.setRow(0, 3, B01111110);
      matriz.setRow(0, 4, B00000100);
      matriz.setRow(0, 5, B00000100);
      matriz.setRow(0, 6, B00000100);
      matriz.setRow(0, 7, B00000000);
      break;
    case 5:
      matriz.setRow(0, 0, B01111110);
      matriz.setRow(0, 1, B01000000);
      matriz.setRow(0, 2, B01111100);
      matriz.setRow(0, 3, B00000010);
      matriz.setRow(0, 4, B00000010);
      matriz.setRow(0, 5, B01000010);
      matriz.setRow(0, 6, B01111110);
      matriz.setRow(0, 7, B00000000);
      break;
    default:
      matriz.clearDisplay(0); // Limpiar si el número está fuera del rango
      break;
  }
  delay(100); // Pequeña pausa para visualización (opcional)
}