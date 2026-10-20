# Proyecto-Final-Sistemas-Embebidos
# 🚨 Alarma de Proximidad con Control Remoto (ESP32 + MQTT)

Sistema de alarma basado en un **ESP32** y un sensor ultrasónico **HC-SR04**
que detecta objetos o personas a menos de 1 metro y activa una sirena. Se puede
**activar y desactivar desde el celular** mediante un dashboard de
**Adafruit IO**, usando el protocolo **MQTT**.

Proyecto desarrollado con **MicroPython** y simulado en **Wokwi**.

## ¿Cómo funciona?

1. El ESP32 se conecta a la red Wi-Fi y al broker MQTT de Adafruit IO.
2. Desde el celular (dashboard de Adafruit IO) se envía el estado de la
   alarma: ON / OFF.
3. Si la alarma está activa, el sensor mide la distancia cada ~1 segundo.
4. Si detecta algo a **menos de 100 cm**:
   - Suena la sirena (buzzer).
   - Se enciende el LED de alarma.
   - Se publica `1` en el feed del sensor para avisar al celular.
5. Si no hay nada cerca, la sirena se apaga y se publica `0`.
6. Si el sistema pierde la conexión, se reinicia automáticamente.

## Componentes

| Componente | Pin ESP32 |
|---|---|
| HC-SR04 (Trigger) | GPIO 13 |
| HC-SR04 (Echo) | GPIO 27 |
| Sirena / Buzzer (PWM) | GPIO 5 |
| LED de alarma (detección) | GPIO 4 |
| LED de estado (alarma activada) | GPIO 22 |

![Circuito](Circuito%20SE.jpeg)

## Feeds MQTT (Adafruit IO)

| Feed | Dirección | Función |
|---|---|---|
| `EstadoAlarma_C1` | Celular → ESP32 | Activa / desactiva la alarma |
| `SensorDist_C1` | ESP32 → Celular | Informa si hay detección (1) o no (0) |

## Tecnologías

- MicroPython
- ESP32
- MQTT (`umqtt.simple`)
- Adafruit IO
- Wokwi (simulación)

## Configuración

1. Creá una cuenta en [Adafruit IO](https://io.adafruit.com) y los dos feeds
   indicados arriba.
2. Armá un dashboard con un botón/switch para `EstadoAlarma_C1` y un indicador
   para `SensorDist_C1`.
3. Reemplazá `user` y `password` en el código por tu usuario y tu AIO Key.
4. Cargá `main.py` y la librería `hcsr04.py` en el ESP32 (o en el proyecto de Wokwi).

## Posibles mejoras

- Notificaciones push al celular al detectar movimiento.
- Distancia de detección configurable desde el dashboard.
- Publicar la distancia real en lugar de solo 0/1.

## Autor

Nicolás Sosa
