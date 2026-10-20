import time
import machine
import micropython
import network
from hcsr04 import HCSR04
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# Red Wi-Fi y clave
ssid = 'Wokwi-GUEST'
wifipassword = ''

# Datos MQTT
mqtt_server = 'io.adafruit.com'
port = 1883
user = 'NicoSosa29'
password = 'TU_AIO_KEY'

# ID y Tópicos
client_id = 'AlarmaProximidad_C1'
topic_ALARMA_C1='NicoSosa29/feeds/EstadoAlarma_C1'
topic_Sens_C1='NicoSosa29/feeds/SensorDist_C1'

# Variable Estado de alarma
Alarma_activa = False 
LEDESTADO = Pin(22,Pin.OUT)

# Definimos modo Station
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

# Conectamos a Wi-Fi
sta_if.connect(ssid, wifipassword)
print("Conectando")
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print("Conectado a Wi-Fi")
print("IP:", sta_if.ifconfig())  # IP


# Función que detecta cambios en los tópicos
def callback_alarma(topic, msg):
    global Alarma_activa,LEDESTADO
    dato = msg.decode('utf-8')
    topicrec = topic.decode('utf-8')
    print("Cambio en: "+topicrec+":"+dato)
    if topicrec == topic_ALARMA_C1 and "OFF" in dato:
        Alarma_activa = False
    else:
        Alarma_activa = True
    LEDESTADO.value(Alarma_activa)

# Conexión con el broker MQTT
try:
    conexionMQTT = MQTTClient(client_id, mqtt_server, user=user, password=password, port=int(port))
    conexionMQTT.set_callback(callback_alarma)
    conexionMQTT.connect()
    conexionMQTT.subscribe(topic_ALARMA_C1)  # Suscripción al tópico correcto
    print("Conectado con Broker MQTT")
except OSError as e:
    print("Fallo la conexión al Broker, reiniciando...")
    time.sleep(5)
    machine.reset()

#
#PROGRAMA PRINCIPAL
#
Sensor = HCSR04(trigger_pin=13,echo_pin=27)
Sirena = PWM(Pin(5), freq=1200, duty_u16=0)
LEDALARMA = Pin(4,Pin.OUT)
Sirena.duty(0)  # Apaga la sirena al iniciar
print("Comenzando monitoreo")
while True:  # Bucle continuo para monitoreo constante
        # Verificar si hay mensajes nuevos publicados por el broker
    try:
        conexionMQTT.check_msg()
        time.sleep_ms(500)
        distancia = Sensor.distance_cm()
        print("Distancia: "+str(distancia))
        # Si la alarma está activa y la distancia es menor a 100 cm, activar la sirena
        if Alarma_activa:
            print("Alarma activa, Buscando movimiento...")
            if distancia<100:
                Sirena.duty(512)  # Activa la sirena
                conexionMQTT.publish(topic_Sens_C1,str(1))
                print("Alarma activada - Sirena encendida")
                LEDALARMA.value(1)
            else:
                Sirena.duty(0)  #apaga la sirena
                conexionMQTT.publish(topic_Sens_C1,str(0))
                LEDALARMA.value(0)
        else:
            Sirena.duty(0)  # Apaga la sirena
            print("Alarma desactivada - Sirena apagada")
        
        time.sleep(0.5)  # Espera para evitar sobrecarga en el loop     
    except OSError as e:
        print("Error:", e)
        time.sleep(5)
        machine.reset()
