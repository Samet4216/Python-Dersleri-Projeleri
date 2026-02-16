"""16.02.26
Amac:
Bir robot nesnesi olacak ve farkli bilesenlerden olusacak. Bu bilesenleri degistirdiginde Robot sinifini degistirmeden sistem calismaya devam etmeli.
Bir Robot sinifi tasarlayacaksin.
Robot:
has a Sensor
has a Controller
has a MotorDriver
has a Logger
Her biri ayri sinif olacak.
Adim 1 — Sensor Katmani:En az 2 farkli sensor yaz:
DistanceSensor
TemperatureSensor
Her sensorde su metod olacak:read()
DistanceSensor sahte mesafe uretsin (random).
TemperatureSensor sahte sicaklik uretsin.
Adim 2 — Controller KatmaniEn az 2 controller yaz:
SimpleController
ThresholdController
SimpleController:sensorden gelen degeri direkt motora iletsin.
ThresholdController:Eger deger belli esigin ustundeyse motoru durdursun.
Controller’in metodu：
control(sensor_value)Controller motoru direkt kontrol etmeyecek.
MotorDriver’a karar dondurecek (ornegin speed degeri).
Adim 3 — MotorDriver:MotorDriver sinifi:
set_speed(value)
Gercek motor yok, sadece print yapacak.
Adim 4 — Logger:2 farkli logger yaz:
ConsoleLogger
SilentLogger (hicbir sey yazmasin)
Logger metodu:log(message)
Adim 5 — Robot Sinifi
Robot constructor’i soyle olacak:
Robot(sensor, controller, motor_driver, logger)
Robot.run() metodu:
sensorden veri oku
controller’a gonder
motor_driver’a sonucu gonder
logger’a log yaz
Beklenen Özellik=
Asagidaki gibi farkli kombinasyonlar sorunsuz calismali:
robot1 = Robot(DistanceSensor(), SimpleController(), MotorDriver(), ConsoleLogger())
robot2 = Robot(TemperatureSensor(), ThresholdController(50), MotorDriver(), SilentLogger())
"""
import random
class Robot:
    def __init__(self, sensor, controller, motor_driver, logger):
        self.sensor = sensor
        self.controller = controller
        self.motor_driver = motor_driver
        self.logger = logger
    def run(self):
        sensor_value = self.sensor.read() #veri okuma islemi icin ayri bir read methodu kullaniliyor.  
        control_result = self.controller.control(sensor_value)#***
        self.motor_driver.set_speed(control_result)
        self.logger.log(f"Sensor value: {sensor_value}, Control result: {control_result}")#***
class DistanceSensor:
    def read(self):
        return random.randint(1, 100)
class TemperatureSensor:
    def read(self):
        return random.randint(0, 100)
class SimpleController:
    def control(self, sensor_value):
        return sensor_value
class ThresholdController:
    def __init__(self, threshold):# Sinir deger olusturur(treshold)
        self.threshold = threshold
    def control(self, sensor_value):
        if sensor_value > self.threshold:
            return 0  # Motoru durdur
        return sensor_value # Motoru calistirmaya devam et
class MotorDriver:
    def set_speed(self, value):
        if value == 0:
            print("Motor DURDU")
        else:
            print(f"Motor speed: {value}")
class ConsoleLogger:
    def log(self, message):
        print(f"[LOG] {message}")
class SilentLogger:
    def log(self, message):
        pass

robot1 = Robot(DistanceSensor(), ThresholdController(50), MotorDriver(), ConsoleLogger())
robot1.run()

print(50*"=")

robot2 = Robot(TemperatureSensor(), ThresholdController(40), MotorDriver(), SilentLogger())# ikinci slient oldugu icin loglama yazdirilmez.
robot2.run()    