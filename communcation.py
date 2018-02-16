import socket
import select
import time
import json

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread

from global_declarations import General


class Communication(QThread):

    signal_status_update = pyqtSignal('QString')

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self._exiting = False
        self._port = 5005
        self._udp_ip = '127.0.0.1'
        self._sock = None
        self._client_address = None
        self._message_id = 1
        self._communication_thread_keep_running = True
        self._is_connected = False
        self._reconnection_counter = 0

        self._init_communication()
        self.start()

    def __del__(self):
        self._communication_thread_keep_running = False
        self.exiting = True
        self.wait()

    def _init_communication(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        self._log('Start communication thread')
        self._initial_communication_wait_for_connection()
        self._do_communication()


    @pyqtSlot('QString')
    def send(self, message):
        if self._is_connected:
            sent = self._sock.sendto(message.encode(), (self._udp_ip, self._port))
            self._log('sending {}'.format(message))
        else:
            self._log('can\'t send message, not connected yat')


    def _initial_communication_wait_for_connection(self):
        connection_counter = 0
        while not self._is_connected:
            connection_counter += 1
            sent = self._sock.sendto('connect'.encode(), (self._udp_ip, self._port))
            readable, writable, exceptional = select.select([self._sock], [], [], 1)
            if readable:
                data, self._client_address = self._sock.recvfrom(1024)

                data = data.decode()
                self._log("received message: {}".format(data))

                if data == 'connect':
                    print('Established communication from {}'.format(self._client_address))
                    self._is_connected = True
            else:
                if connection_counter%5 == 0:
                    self._log('not yet connected')

            time.sleep(1)

    def _do_communication(self):
        connection_counter = 0
        while self._communication_thread_keep_running:
            connection_counter += 1
            readable, writable, exceptional = select.select([self._sock], [], [])
            if readable:
                data, self._client_address = self._sock.recvfrom(1024)

                data = data.decode()
                self._log("received message: {}".format(data))

                if data == 'connect':
                    print('Reconnect reuquest from {}'.format(self._client_address))
                    sent = self._sock.sendto('connect'.encode(), (self._udp_ip, self._port))
                    self._reconnection_counter += 1
                else:
                    print('received message, emiting status: {}'.format(data))
                    self.signal_status_update.emit(data)
            else:
                pass

            time.sleep(0.001) # Pass CPU

        self._log('Communication thread exited')

    def _log(self, message):
        print('{}: {}'.format('communication', message))

instance = Communication()