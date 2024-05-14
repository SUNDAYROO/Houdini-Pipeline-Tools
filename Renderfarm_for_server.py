

import sys
import socket
from socket import gethostbyaddr
import threading
import json
from ping3 import ping
import time
from zeroconf import ServiceInfo, Zeroconf
import netifaces as ni
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Signal, Slot, QObject, QRect, QCoreApplication, QThread, QMetaObject

class ServerThread(QObject):
    update_signal = Signal(dict)  # Signal 객체 추가

    def __init__(self, connection, update_callback):
        super().__init__()  # QObject의 초기화
        self.connection = connection
        self.empty_data_count = 0
        self.last_update_times = {}
        self.update_callback = update_callback


    def run(self):
        last_update_times = {}  # 마지막 업데이트 시간 저장을 위한 딕셔너리

        while True:
            try:
                print("Waiting for data from client...")
                data = self.connection.recv(1024)
                print(f"Raw data received: {data}")  # 원시 데이터 출력
                if not data:
                    print("No data received. Client may have disconnected.")
                    self.empty_data_count += 1
                    if self.empty_data_count > 5:
                        print("Too many empty data received. Closing connection.")
                        break
                else:
                    self.process_data(data)
                    self.empty_data_count = 0


                print(f"Data received: {data}")

                if data:
                    addr = self.connection.getpeername()
                    _, _, _ = gethostbyaddr(addr[0])
                    ping_result = self.calculate_ping(addr[0])
                    client_data = json.loads(data.decode('utf-8'))
                    client_hostname = client_data.get('hostname')
                    print(f"Client hostname received: {client_hostname}")  # 클라이언트로부터 받은 hostname 출력

                    lowercase_hostname = client_hostname.lower()
                    print(
                        f"Lowercase hostname for internal processing: {lowercase_hostname}")  # 내부 처리용 소문자 변환된 hostname 출력

                    # 마지막 업데이트 시간 계산
                    if lowercase_hostname in self.last_update_times:
                        last_update = time.time() - self.last_update_times[lowercase_hostname]
                    else:
                        last_update = 0
                    self.last_update_times[lowercase_hostname] = time.time()

                    print(f"Last update times dictionary: {self.last_update_times}")  # last_update_times 사전 상태 출력

                    client_info = {
                        'hostname': client_hostname,  # 대소문자 변경 없이 원본 그대로 사용
                        'addr': addr,
                        'ping': ping_result,
                        'last_update': last_update,
                        'status': client_data['status']
                    }
                    print(
                        f"Client info: Hostname: {client_hostname}, Last Update: {client_info['last_update']}, Ping: {ping_result}")
                    self.update_signal.emit(client_info)

                if not data:
                    self.empty_data_count += 1
                    print("Received empty data. Count:", self.empty_data_count)
                    if self.empty_data_count > 5:  # 조건 수정 가능
                        print("Too many empty data received. Closing connection.")
                        self.connection.close()  # 연결 종료
                        break
                    continue

                self.empty_data_count = 0  # 유효한 데이터 수신 시 카운터 초기화
                message = json.loads(data.decode('utf-8'))
                print(f"Decoded message: {message}")
                self.update_signal.emit(message['status'])
                self.update_callback(client_info)

            except socket.timeout:
                print("Socket timeout. Waiting for next data...")
                continue
            except socket.error as e:
                print(f"Socket Error: {e}")
                if e.errno in [10053, 10054, 10038]:
                    print("Client disconnected or invalid socket.")
                    break
                else:
                    print(f"Connection closed unexpectedly on port {self.connection.getpeername()[1]}")
                    break
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                break
            except Exception as e:
                print(f"General Error: {e}")
                break
            finally:
                print("Connection potentially closing.")
        self.connection.close()
        print("Connection closed")
        print("Thread ending")

    def process_data(self, data):
        try:
            # JSON 형식의 데이터를 디코딩
            client_message = json.loads(data.decode('utf-8'))


            # 클라이언트 정보 추출
            status = client_message.get('status')
            hostname = client_message.get('hostname')  # 대소문자 변경 없이 원본 그대로 사용
            last_update_time = client_message.get('last_update_time')

            # 호스트 이름 및 IP 주소 획득
            addr = self.connection.getpeername()
            hostname_resolved, _, _ = gethostbyaddr(addr[0])

            # 호스트 이름이 일치하지 않는 경우 업데이트하지 않음
            if hostname != hostname_resolved:
                print(f"Hostname mismatch: {hostname} vs {hostname_resolved}")
                return

            # 클라이언트의 핑을 계산
            ping_result = self.calculate_ping(addr[0])

            # 업데이트 정보 생성
            client_info = {
                'hostname': hostname,
                'addr': addr,
                'ping': ping_result,
                'last_update': time.time() - last_update_time,
                'status': status
            }

            # 업데이트 신호 발송
            self.update_signal.emit(client_info)
            print(f"Client info updated: {client_info}")
            self.update_callback(client_info)  # update_signal 대신 update_callback 사용

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")

        # 오류 발생 시 콜백 함수 호출을 하지 않습니다.

    def calculate_ping(self, ip_address):
        return ping(ip_address)  # ping3 라이브러리를 사용한 핑 계산





class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(604, 416)
        self.Title_T = QLabel(Dialog)
        self.Title_T.setObjectName(u"Title_T")
        self.Title_T.setGeometry(QRect(170, 50, 121, 16))
        self.Statement_1_T = QLabel(Dialog)
        self.Statement_1_T.setObjectName(u"Statement_1_T")
        self.Statement_1_T.setGeometry(QRect(60, 100, 71, 16))
        self.Run_B = QPushButton(Dialog)
        self.Run_B.setObjectName(u"Run_B")
        self.Run_B.setGeometry(QRect(130, 180, 51, 24))
        self.Statement_1_E = QLineEdit(Dialog)
        self.Statement_1_E.setObjectName(u"Statement_1_E")
        self.Statement_1_E.setGeometry(QRect(140, 100, 61, 20))
        self.ClientListTree = QTreeWidget(Dialog)
        QTreeWidgetItem(self.ClientListTree)
        QTreeWidgetItem(self.ClientListTree)
        QTreeWidgetItem(self.ClientListTree)
        self.ClientListTree.setObjectName(u"ClientListTree")
        self.ClientListTree.setGeometry(QRect(10, 210, 581, 211))
        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.Title_T.setText(QCoreApplication.translate("Dialog", u"Render Farm Server", None))
        self.Statement_1_T.setText(QCoreApplication.translate("Dialog", u"1_Statement", None))
        self.Run_B.setText(QCoreApplication.translate("Dialog", u"Run", None))

        ___qtreewidgetitem = self.ClientListTree.headerItem()
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("Dialog", u"IP", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("Dialog", u"Ping", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"Last Status Update", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Status ", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Machine Name", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Worker Name", None));

        __sortingEnabled = self.ClientListTree.isSortingEnabled()
        self.ClientListTree.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.ClientListTree.topLevelItem(0)
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("Dialog", u"72", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("Dialog", u"3.3 s ago", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Dialog", u"Idle", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Dialog", u"DESKTOP-N5BDMQI", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"1", None));
        ___qtreewidgetitem2 = self.ClientListTree.topLevelItem(1)
        ___qtreewidgetitem2.setText(4, QCoreApplication.translate("Dialog", u"30", None));
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("Dialog", u"5.1 s ago", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("Dialog", u"Rendering", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("Dialog", u"DESKTOP-LPNJ54", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Dialog", u"2", None));
        ___qtreewidgetitem3 = self.ClientListTree.topLevelItem(2)
        ___qtreewidgetitem3.setText(2, QCoreApplication.translate("Dialog", u"Offline", None));
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("Dialog", u"DESKTOP-K5UBJ21", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("Dialog", u"3", None));
        self.ClientListTree.setSortingEnabled(__sortingEnabled)
        self.ClientListTree.clear()

    # retranslateUi



class ServerApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.start_server()
        self.client_names = set()  # 클라이언트 이름을 저장하는 집합
        self.client_connections = {}  # 클라이언트 연결 정보를 저장하는 딕셔너리
        self.ui.Run_B.clicked.connect(self.send_houdini_command)
        self.zeroconf = Zeroconf()
        self.server_service_info = None
        self.start_zeroconf_service()

    def start_zeroconf_service(self):
        # 로컬 머신의 호스트 이름을 가져옴
        hostname = socket.gethostname()

        # 사용 가능한 IPv4 주소 찾기
        valid_ip = None
        for iface in ni.interfaces():
            addresses = ni.ifaddresses(iface)
            ipv4_info = addresses.get(ni.AF_INET)
            if ipv4_info and ipv4_info[0]['addr'] != "127.0.0.1":
                valid_ip = ipv4_info[0]['addr']
                break

        if valid_ip:
            # Zeroconf 서비스 정보 생성 (_CFX 추가)
            self.server_service_info = ServiceInfo(
                "_http._tcp.local.",
                f"{hostname}_CFX._http._tcp.local.",
                addresses=[socket.inet_aton(valid_ip)],
                port=8080,
                properties={},
            )
            self.zeroconf.register_service(self.server_service_info)
        else:
            print("No valid IPv4 address found for any interface.")

    def add_service(self, zeroconf, type, name):
        # _CFX를 이름에 포함하는 서비스만 고려
        if "_CFX" in name:
            info = zeroconf.get_service_info(type, name)
            if info:
                server_ip = socket.inet_ntoa(info.addresses[0])
                server_port = info.port
                # 연결된 서비스 정보 저장
                self.connected_service_info = (server_ip, server_port)
                print(f"Connecting to {_CFX} service at {server_ip}:{server_port}")
                # 서비스에 연결
                self.connect_to_service(server_ip, server_port)

    def closeEvent(self, event):
        if self.zeroconf:
            self.zeroconf.unregister_service(self.server_service_info)
            self.zeroconf.close()
        super().closeEvent(event)

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('', 8080))
        self.server_socket.listen()
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                hostname, _, _ = gethostbyaddr(addr[0])
                self.client_connections[hostname] = client_socket

                server_worker = ServerThread(client_socket, self.update_status)
                worker_thread = threading.Thread(target=server_worker.run)
                worker_thread.start()

            except socket.error as e:
                print(f"Accept Error: {e}")
                time.sleep(1)

    @Slot(dict)
    def update_status(self, client_info):

        client_hostname = client_info.get('hostname', '')
        lowercase_hostname = client_hostname.lower()  # 내부 처리용 소문자 변환
        print(f"Client info received for update: {client_info}")  # 업데이트를 위해 받은 클라이언트 정보 출력

        # 소문자 변환된 이름으로 기존 클라이언트 이름 검색
        existing_name = next((name for name in self.client_names if name.lower() == lowercase_hostname), None)

        if existing_name:
            # 기존에 저장된 이름이 있는 경우 그 이름을 사용
            display_name = existing_name
        else:
            # 새로운 클라이언트인 경우, 원래 이름을 저장하고 사용
            self.client_names.add(client_hostname)
            display_name = client_hostname
        if not display_name:
            return
        print("Updating status for:", client_info)

        # hostname이 없거나 비어있는 경우 처리하지 않음
        if not client_info.get('hostname'):
            return

        print("Updating status for:", client_info)  # 디버깅: 업데이트할 클라이언트 정보 출력

        found_item = None

        for i in range(self.ui.ClientListTree.topLevelItemCount()):
            item = self.ui.ClientListTree.topLevelItem(i)
            if item and item.text(1).lower() == lowercase_hostname:  # 비교 시 소문자 변환 사용
                found_item = item
                print(f"Found existing item for {display_name}")
                break

        # 기존 항목을 찾지 못한 경우 새로운 항목을 생성
        if not found_item:
            found_item = QTreeWidgetItem(self.ui.ClientListTree)
            print(f"Created new item for {client_info.get('hostname')}")

        # Worker Name 설정
        worker_name = str(self.ui.ClientListTree.indexOfTopLevelItem(found_item) + 1) if found_item else ''
        found_item.setText(0, worker_name)
        found_item.setText(1, display_name)  # 원래 호스트 이름 사용
        found_item.setText(2, client_info.get('status', ''))

        # Last Status Update 및 Ping 설정
        if client_info.get('last_update') is not None:
            last_update_sec = round(client_info.get('last_update', 0), 1)
            found_item.setText(3, f"{last_update_sec} s ago")

        ping_ms = round(client_info.get('ping', 0) * 1000)
        found_item.setText(4, str(ping_ms))

        # IP 주소와 포트 번호 표시
        if client_info.get('addr'):
            ip_port_str = f"{client_info['addr'][0]}:{client_info['addr'][1]}"
        else:
            ip_port_str = "N/A"
        found_item.setText(5, ip_port_str)

    def send_houdini_command(self):
        for i in range(self.ui.ClientListTree.topLevelItemCount()):
            item = self.ui.ClientListTree.topLevelItem(i)
            client_hostname = item.text(1)
            self.send_command_to_client(client_hostname, "run_houdini")

    def send_command_to_client(self, hostname, command):
        # 클라이언트에게 명령을 보내는 로직
        client_socket = self.client_connections.get(hostname)
        if client_socket:
            try:
                message = json.dumps({"command": command})
                client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending command to {hostname}: {e}")
        else:
            print(f"Client {hostname} not found or not connected.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerApp()
    window.show()
    sys.exit(app.exec())
