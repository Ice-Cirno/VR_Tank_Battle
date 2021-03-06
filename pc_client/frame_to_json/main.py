import Leap, socket, ctypes, struct, frame_to_json
controller = Leap.Controller()
# print controller


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 7777       # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
retry = 0

class LeapEventListener(Leap.Listener):
 
    def on_server_connect(self, controller):
        print "Server Connected"
    def on_connect(self, controller):
        print "Connected"
        controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
        controller.config.save()
 
    def on_disconnect(self, controller):
        print "Disconnected"
 
    def on_frame(self, controller):
        global retry
        frame = controller.frame()
        buffer = frame_to_json.to_json(frame)
        print '\r' + str(len(buffer)),
        try:
            s.sendall(buffer)
            retry = 0
        except Exception as e:
            print(e)
            retry += 1
            if retry > 10:
                s.close()
                exit()


listener = LeapEventListener()
controller.add_listener(listener)

while True:
    pass

s.close()