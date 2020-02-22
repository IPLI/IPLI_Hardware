Image Processing Living Intelligence_Hardware
------

This is a repository for Hardware module of Image Processing Living Intelligence.</br>

This project requires a subnet configuration between the server, the hardware and the Android module.</br>


### **Requirements**</br>

* H/W
  * RaspberryPi 3 b+
  * HC-SR04
  * Picanera 8mp v2
  * Road cell hx711
  * Road cell ADC

* S/W
  * Raspbian buster with desktop
  * Python 3.7
  * MJPG Streamer


1. 라즈비안 이미지 굽기
https://edw216.github.io/rasp/
2. 파이썬 3.7버전 다운로드
https://edw216.github.io/rasp/


### **Raspbian Autostart**</br>

1.  `sudo nano /etc/rc.local` 파일에 실행파일 지정<br/>
`/home/pi/start.sh `


### **How to communicate with the Server**</br>
C로 작성되어져 있는 서버와 같은 서브넷망으로 구성된 무선랜에 연결하여 서버와 tcp/ip 소켓통신을 통해 스트링 데이터를 주고 받는다.</br>



### **How it works**</br>
카트에 부착되어진 초음파 거리 센서는 일정 범위 안에 들어오는 물체를 인식한다. 즉, 사용자가 카트에 상품을 넣게 되면 초음파 거리 센서는 물체가 카트 안에 들어옴을 인지 한 뒤 카트의 ip를 사용해 mjpgestreamer 이미지 스트리밍 서버를 생성한다. 카트 클라이언트는 서버에게 카메라 스트리밍을 시작한다는 `tmpStr = 'darknet.exe detector demo data/obj.data data/yolo-obj.cfg yolo-obj_last.weights http://'+my_ip+':8091/?action=stream'` 해당 스트링 데이터를 서버에게 전송 한다. 스트링 데이터를 전송받은 서버는 카트가 생성한 서버에 접속한 뒤, 스트리밍 데이터를 받는다. 서버에 의해 인식된 물체가 카트위에 놓여지면 카트 밑에 부착된 로드셀은 무게의 증감을 판단하여 해당 증감 데이터를 서버에게 전송한다.

