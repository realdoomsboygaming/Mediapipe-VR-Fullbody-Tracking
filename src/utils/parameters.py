from scipy.spatial.transform import Rotation as R
import cv2
import json

class Parameters():
    def __init__(self) -> None:
        
        with open("config.json", "r") as f:
            param = json.load(f)
        
        self.advanced = param.get("advanced", False)
        
        self.model = param.get("model_complexity", 1)
        self.smooth_landmarks = param.get("smooth_landmarks", True)
        self.min_tracking_confidence = param.get("min_tracking_confidence", 0.5)
        self.static_image = param.get("static_image", False)

        #PARAMETERS:
        self.maximgsize = param.get("imgsize", 1000)
        self.cameraid = param.get("camid", "0")
        self.hmd_to_neck_offset = param.get("hmd_to_neck_offset", [0,-0.2,0.1])
        self.preview_skeleton = param.get("preview_skeleton", False)
        self.waithmd = param.get("waithmd", False)
        self.rotate_image = param.get("rotate_image", 0)
        self.camera_latency = param.get("camera_latency", 0.0)
        self.smoothing_1 = param.get("smoothing_1", 0.0)
        self.additional_smoothing_1 = param.get("additional_smoothing_1", 0.7)
        self.smoothing_2 = param.get("smoothing_2", 0.5)
        self.additional_smoothing_2 = param.get("additional_smoothing_2", 0.9)
        self.feet_rotation = param.get("feet_rotation", False)
        self.use_hands = param.get("use_hands", False)
        self.ignore_hip = param.get("ignore_hip", False)
        
        self.camera_settings = param.get("camera_settings", False)
        self.camera_width = param.get("camera_width", 0)
        self.camera_height = param.get("camera_height", 0)

        self.backend = param.get("backend", 1)
        self.backend_ip = param.get("backend_ip", "127.0.0.1")
        self.backend_port = param.get("backend_port", 9000)
        
        self.webui = param.get("webui", False)

        self.calib_rot = param.get("calib_rot", True)
        self.calib_tilt = param.get("calib_tilt", True)
        self.calib_scale = param.get("calib_scale", True)

        self.recalibrate = param.get("recalibrate", False)
        
        #rotations in degrees!
        self.euler_rot_y = param.get("euler_rot_y", 180)
        self.euler_rot_x = param.get("euler_rot_x", 90)
        self.euler_rot_z = param.get("euler_rot_z", 180)

        self.posescale = param.get("posescale", 1)

        self.exit_ready = param.get("exit_ready", False)

        self.img_rot_dict = {0: None, 1: cv2.ROTATE_90_CLOCKWISE, 2: cv2.ROTATE_180, 3: cv2.ROTATE_90_COUNTERCLOCKWISE}
        self.img_rot_dict_rev = {None: 0, cv2.ROTATE_90_CLOCKWISE: 1, cv2.ROTATE_180: 2, cv2.ROTATE_90_COUNTERCLOCKWISE: 3}

        self.paused = param.get("paused", False)
        
        self.flip = param.get("flip", False)
        
        self.log_frametime = param.get("log_frametime", False)
        
        self.mirror = param.get("mirror", False)
        
        self.global_rot_y = R.from_euler('y',self.euler_rot_y,degrees=True)
        self.global_rot_x = R.from_euler('x',self.euler_rot_x-90,degrees=True) 
        self.global_rot_z = R.from_euler('z',self.euler_rot_z-180,degrees=True) 
        
        self.smoothing = self.smoothing_1
        self.additional_smoothing = self.additional_smoothing_1
        
        if not self.advanced:
            self.smoothing = 0.0
            self.smoothing_1 = 0.0
            self.camera_latency = 0.0
    
    def save_params(self):
        param = {}
        param["advanced"] = self.advanced
        param["model_complexity"] = self.model
        param["smooth_landmarks"] = self.smooth_landmarks
        param["min_tracking_confidence"] = self.min_tracking_confidence
        param["static_image"] = self.static_image
        param["imgsize"] = self.maximgsize
        param["camid"] = self.cameraid
        param["hmd_to_neck_offset"] = self.hmd_to_neck_offset
        param["preview_skeleton"] = self.preview_skeleton
        param["waithmd"] = self.waithmd
        param["rotate_image"] = self.img_rot_dict_rev[self.rotate_image]
        param["camera_latency"] = self.camera_latency
        param["smoothing_1"] = self.smoothing_1
        param["additional_smoothing_1"] = self.additional_smoothing_1
        param["smoothing_2"] = self.smoothing_2
        param["additional_smoothing_2"] = self.additional_smoothing_2
        param["feet_rotation"] = self.feet_rotation
        param["use_hands"] = self.use_hands
        param["ignore_hip"] = self.ignore_hip
        param["camera_settings"] = self.camera_settings
        param["camera_width"] = self.camera_width
        param["camera_height"] = self.camera_height
        param["backend"] = self.backend
        param["backend_ip"] = self.backend_ip
        param["backend_port"] = self.backend_port
        param["webui"] = self.webui
        param["calib_rot"] = self.calib_rot
        param["calib_tilt"] = self.calib_tilt
        param["calib_scale"] = self.calib_scale
        param["recalibrate"] = self.recalibrate
        param["euler_rot_y"] = self.euler_rot_y
        param["euler_rot_x"] = self.euler_rot_x
        param["euler_rot_z"] = self.euler_rot_z
        param["posescale"] = self.posescale
        param["exit_ready"] = self.exit_ready
        param["paused"] = self.paused
        param["flip"] = self.flip
        param["log_frametime"] = self.log_frametime
        param["mirror"] = self.mirror
        
        with open("config.json", "w") as f:
            json.dump(param, f, indent=4)
        
    def change_recalibrate(self):
        self.recalibrate = True

    def rot_change_y(self, value):
        print(f"INFO: Changed y rotation value to {value}")
        self.euler_rot_y = value
        self.global_rot_y = R.from_euler('y',value,degrees=True)
        self.save_params()
        
    def rot_change_x(self, value):
        print(f"INFO: Changed x rotation value to {value}")
        self.euler_rot_x = value
        self.global_rot_x = R.from_euler('x',value-90,degrees=True)
        self.save_params()
        
    def rot_change_z(self, value):
        print(f"INFO: Changed z rotation value to {value}")
        self.euler_rot_z = value
        self.global_rot_z = R.from_euler('z',value-180,degrees=True)
        self.save_params()
         
    def change_scale(self, value):
        print(f"INFO: Changed scale value to {value}")
        self.posescale = value
        self.save_params()

    def change_img_rot(self, val):
        print(f"INFO: Changed image rotation to {val*90} clockwise")
        self.rotate_image = self.img_rot_dict[val]
        self.save_params()

    def change_smoothing(self, val, paramid = 0):
        print(f"INFO: Changed smoothing value to {val}")
        self.smoothing = val
        
        if paramid == 1:
            self.smoothing_1 = val
        if paramid == 2:
            self.smoothing_2 = val
        self.save_params()
        
    def change_additional_smoothing(self, val, paramid = 0):
        print(f"INFO: Changed additional smoothing value to {val}")
        self.additional_smoothing = val

        if paramid == 1:
            self.additional_smoothing_1 = val
        if paramid == 2:
            self.additional_smoothing_2 = val
        self.save_params()

    def change_camera_latency(self, val):
        print(f"INFO: Changed camera latency to {val}")
        self.camera_latency = val
        self.save_params()

    def change_neck_offset(self,x,y,z):
        print(f"INFO: Hmd to neck offset changed to: [{x},{y},{z}]")
        self.hmd_to_neck_offset = [x,y,z]
        self.save_params()

    def change_mirror(self, mirror):
        print(f"INFO: Image mirror set to {mirror}")
        self.mirror = mirror
        self.save_params()

    def ready2exit(self):
        self.exit_ready = True
        self.save_params()

if __name__ == "__main__":
    print("hehe")
