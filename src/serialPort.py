from serial import Serial
import queue

class serialPort(Serial):

    def __init__(self, port_num, baudrate, timeout = 0.1):
        try:
            Serial.__init__(self, port = port_num, baudrate = baudrate, timeout = timeout)

            self.portnum = port_num
            self.baudrate = baudrate
            self.timeout = timeout

            self.buffer = []

        except Exception as e:
            raise

    def open_comport(self):
        try:
            if Serial.isOpen(self):
                Serial.close(self)

            Serial.open(self)

            self.enqueue("serial port opened : {} with {} bps\n".format(self.portnum, self.baudrate))

        except Exception as e:
            raise

    def close_comport(self):
        try:
            Serial.close(self)

            self.enqueue("serial port {} closed\n".format(self.portnum))

        except Exception as e:
            raise

    def enqueue(self, msg):
        self.buffer.append(msg)

    def dequeue(self):
        if len(self.buffer) < 1:
            return None
        return self.buffer.pop(0)

    def receiveData(self, maxDataSize):
        try:
            receivedData = Serial.read(self, size = maxDataSize)
            if len(receivedData) > 0:
                self.enqueue(receivedData)

        except Exception as e:
            raise
