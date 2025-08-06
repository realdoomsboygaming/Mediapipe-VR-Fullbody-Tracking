import customtkinter
import numpy as np
from scipy.spatial.transform import Rotation as R
from utils.helpers import shutdown, sendToSteamVR

class InferenceWindow(customtkinter.CTkFrame):
    def __init__(self, master, params, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.params = params
        params.gui = self
        self.master = master

        main_frame = customtkinter.CTkFrame(self.master)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # calibrate rotation
        self.calib_rot_var = customtkinter.BooleanVar(value=self.params.calib_rot)
        self.calib_flip_var = customtkinter.BooleanVar(value=self.params.flip)
        self.rot_y_var = customtkinter.DoubleVar(value=self.params.euler_rot_y)

        self.calibrate_rotation_frame(main_frame)

        # calibrate tilt
        self.calib_tilt_var = customtkinter.BooleanVar(value=self.params.calib_tilt)
        self.rot_x_var = customtkinter.DoubleVar(value=self.params.euler_rot_x)
        self.rot_z_var = customtkinter.DoubleVar(value=self.params.euler_rot_z)

        self.calibrate_tilt_frame(main_frame)

        # calibrate scale
        self.calib_scale_var = customtkinter.BooleanVar(value=self.params.calib_scale)
        self.scale_var = customtkinter.DoubleVar(value=self.params.posescale)

        self.calibrate_scale_frame(main_frame)

        # recalibrate
        customtkinter.CTkButton(main_frame, text='Recalibrate', command=self.autocalibrate).pack(pady=5)
                    
        # pause tracking
        customtkinter.CTkButton(main_frame, text='Pause/Unpause tracking', command=self.pause_tracking).pack(pady=5)
                  
        # smoothing
        self.change_smoothing_frame(main_frame)

        # rotate image 
        self.change_image_rotation_frame(main_frame)
        
        # neck offset
        if params.advanced:
            self.change_neck_offset_frame(main_frame)
        
        #frametime log
        self.log_frametime_var = customtkinter.BooleanVar(value=self.params.log_frametime)
        customtkinter.CTkCheckBox(main_frame, text="Log frametimes to console", variable=self.log_frametime_var, command=self.change_log_frametime).pack(pady=5)

        # exit
        customtkinter.CTkButton(main_frame, text='Exit', command=self.params.ready2exit).pack(pady=5)

        master.protocol("WM_DELETE_WINDOW", self.params.ready2exit)

    def calibrate_rotation_frame(self, parent):
        frame = customtkinter.CTkFrame(parent)
        frame.pack(padx=10, pady=10, fill="x")

        customtkinter.CTkCheckBox(frame, text = "Enable automatic rotation calibration", variable = self.calib_rot_var, command=self.change_rot_auto).pack(anchor="w")
        customtkinter.CTkCheckBox(frame, text = "Flip calibration", variable = self.calib_flip_var, command=self.change_rot_flip).pack(anchor="w")

        customtkinter.CTkLabel(frame, text="Rotation Y:").pack(anchor="w")
        customtkinter.CTkSlider(frame, from_=-40, to=400, variable=self.rot_y_var).pack(fill="x")
        self.rot_y_var.trace_add('write', lambda var, index, mode: self.params.rot_change_y(self.rot_y_var.get()))

    def calibrate_tilt_frame(self, parent):
        frame = customtkinter.CTkFrame(parent)
        frame.pack(padx=10, pady=10, fill="x")

        customtkinter.CTkCheckBox(frame, text="Enable automatic tilt calibration", variable=self.calib_tilt_var, command=self.change_tilt_auto).pack(anchor="w")

        customtkinter.CTkLabel(frame, text="Rotation X:").pack(anchor="w")
        customtkinter.CTkSlider(frame, from_=0, to=180, variable=self.rot_x_var).pack(fill="x")
        self.rot_x_var.trace_add('write', lambda var, index, mode: self.params.rot_change_x(self.rot_x_var.get()))
        
        customtkinter.CTkLabel(frame, text="Rotation Z:").pack(anchor="w")
        customtkinter.CTkSlider(frame, from_=90, to=270, variable=self.rot_z_var).pack(fill="x")
        self.rot_z_var.trace_add('write', lambda var, index, mode: self.params.rot_change_z(self.rot_z_var.get()))

    def calibrate_scale_frame(self, parent):
        frame = customtkinter.CTkFrame(parent)
        frame.pack(padx=10, pady=10, fill="x")

        customtkinter.CTkCheckBox(frame, text ="Enable automatic scale calibration", variable=self.calib_scale_var, command=self.change_scale_auto).pack(anchor="w")
        
        customtkinter.CTkLabel(frame, text="Scale:").pack(anchor="w")
        customtkinter.CTkSlider(frame, from_=0.5, to=2.0, variable=self.scale_var).pack(fill="x")
        self.scale_var.trace_add('write', lambda var, index, mode: self.params.change_scale(self.scale_var.get()))

    def change_smoothing_frame(self, parent):
        frame = customtkinter.CTkFrame(parent)
        frame.pack(padx=10, pady=10, fill="x")

        customtkinter.CTkLabel(frame, text="Smoothing window:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        smoothingtext1 = customtkinter.CTkEntry(frame, width=120)
        smoothingtext1.grid(row=0, column=1, padx=5, pady=5)
        smoothingtext1.insert(0, self.params.smoothing_1)
        customtkinter.CTkButton(frame, text='Update', command=lambda: self.params.change_smoothing(float(smoothingtext1.get()),1)).grid(row=0, column=2, padx=5, pady=5)

        if self.params.advanced:
            smoothingtext2 = customtkinter.CTkEntry(frame, width=120)
            smoothingtext2.grid(row=0, column=3, padx=5, pady=5)
            smoothingtext2.insert(0, self.params.smoothing_2)
            customtkinter.CTkButton(frame, text='Update', command=lambda: self.params.change_smoothing(float(smoothingtext2.get()),2)).grid(row=0, column=4, padx=5, pady=5)

        customtkinter.CTkButton(frame, text='Disable', command=lambda: self.params.change_smoothing(0.0)).grid(row=0, column=5, padx=5, pady=5)

        customtkinter.CTkLabel(frame, text="Additional smoothing:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        lat1 = customtkinter.CTkEntry(frame, width=120)
        lat1.grid(row=1, column=1, padx=5, pady=5)
        lat1.insert(0, self.params.additional_smoothing_1)
        customtkinter.CTkButton(frame, text='Update', command=lambda: self.params.change_additional_smoothing(float(lat1.get()),1)).grid(row=1, column=2, padx=5, pady=5)
        
        if self.params.advanced:
            lat2 = customtkinter.CTkEntry(frame, width=120)
            lat2.grid(row=1, column=3, padx=5, pady=5)
            lat2.insert(0, self.params.additional_smoothing_2)
            customtkinter.CTkButton(frame, text='Update', command=lambda: self.params.change_additional_smoothing(float(lat2.get()),2)).grid(row=1, column=4, padx=5, pady=5)
        
        customtkinter.CTkButton(frame, text='Disable', command=lambda: self.params.change_additional_smoothing(0.0)).grid(row=1, column=5, padx=5, pady=5)

        if self.params.advanced:
            customtkinter.CTkLabel(frame, text="Camera latency:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            lat = customtkinter.CTkEntry(frame, width=120)
            lat.grid(row=2, column=1, padx=5, pady=5)
            lat.insert(0, self.params.camera_latency)
            customtkinter.CTkButton(frame, text='Update', command=lambda: self.params.change_camera_latency(float(lat.get()))).grid(row=2, column=2, padx=5, pady=5)

    def change_image_rotation_frame(self, parent):
        frame = customtkinter.CTkFrame(parent)
        frame.pack(padx=10, pady=10, fill="x")
        
        rot_img_var = customtkinter.IntVar(value=self.params.img_rot_dict_rev.get(self.params.rotate_image, 0))
        customtkinter.CTkLabel(frame, text="Rotation:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        customtkinter.CTkRadioButton(frame, text="0°", variable = rot_img_var, value = 0).grid(row=0, column=1)
        customtkinter.CTkRadioButton(frame, text="90°",  variable = rot_img_var, value = 1).grid(row=0, column=2)
        customtkinter.CTkRadioButton(frame, text="180°",  variable = rot_img_var, value = 2).grid(row=0, column=3)
        customtkinter.CTkRadioButton(frame, text="270°",  variable = rot_img_var, value = 3).grid(row=0, column=4)

        rot_img_var.trace_add('write', lambda var, index, mode: self.params.change_img_rot(rot_img_var.get()))

        img_mirror_var = customtkinter.BooleanVar(value=self.params.mirror)
        customtkinter.CTkCheckBox(frame, text="Mirror", variable=img_mirror_var, command=lambda: self.params.change_mirror(img_mirror_var.get())).grid(row=0, column=5, padx=5, pady=5)

    def change_neck_offset_frame(self, parent):
        frame = customtkinter.CTkFrame(parent)
        frame.pack(padx=10, pady=10, fill="x")
        
        customtkinter.CTkLabel(frame, text="X:").grid(row=0, column=0, padx=5, pady=5)
        text1 = customtkinter.CTkEntry(frame, width=60)
        text1.grid(row=0, column=1, padx=5, pady=5)
        text1.insert(0, self.params.hmd_to_neck_offset[0])
        
        customtkinter.CTkLabel(frame, text="Y:").grid(row=0, column=2, padx=5, pady=5)
        text2 = customtkinter.CTkEntry(frame, width=60)
        text2.grid(row=0, column=3, padx=5, pady=5)
        text2.insert(0, self.params.hmd_to_neck_offset[1])
        
        customtkinter.CTkLabel(frame, text="Z:").grid(row=0, column=4, padx=5, pady=5)
        text3 = customtkinter.CTkEntry(frame, width=60)
        text3.grid(row=0, column=5, padx=5, pady=5)
        text3.insert(0, self.params.hmd_to_neck_offset[2])

        customtkinter.CTkButton(frame, text='Update', command=lambda: self.params.change_neck_offset(float(text1.get()), float(text2.get()), float(text3.get()))).grid(row=0, column=6, padx=5, pady=5)

    def change_log_frametime(self):
        self.params.log_frametime = self.log_frametime_var.get()
        print(f"INFO: Frametime logging {'enabled' if self.params.log_frametime else 'disabled'}")

    def change_rot_auto(self):
        self.params.calib_rot = self.calib_rot_var.get()
        print(f"Mark rotation to{'' if self.params.calib_rot else ' NOT'} be automatically calibrated")
        
    def change_rot_flip(self):
        self.params.flip = self.calib_flip_var.get()
        print("changed flip to: ", self.params.flip)

    def change_tilt_auto(self):
        self.params.calib_tilt = self.calib_tilt_var.get()
        print(f"Mark tilt to{'' if self.params.calib_tilt else ' NOT'} be automatically calibrated")
    
    def change_scale_auto(self):
        self.params.calib_scale = self.calib_scale_var.get()
        print(f"Mark scale to{'' if self.params.calib_scale else ' NOT'} be automatically calibrated")

    def autocalibrate(self):
        use_steamvr = self.params.backend == 1

        if use_steamvr:
            array = sendToSteamVR("getdevicepose 0")
            if array is None or len(array) < 10:
                shutdown(self.params)
            headsetpos = [float(array[3]),float(array[4]),float(array[5])]
            headsetrot = R.from_quat([float(array[7]),float(array[8]),float(array[9]),float(array[6])])
            neckoffset = headsetrot.apply(self.params.hmd_to_neck_offset)
        
        try:
            feet_middle = (self.params.pose3d_og[0] + self.params.pose3d_og[5])/2
        except (AttributeError, TypeError):
            print("INFO: No pose detected, try to autocalibrate again.")
            return

        if self.params.calib_tilt:
            value = np.arctan2(feet_middle[0],-feet_middle[1]) * 57.295779513
            self.params.rot_change_z(-value+180)
            self.rot_z_var.set(self.params.euler_rot_z)
            
            for j in range(self.params.pose3d_og.shape[0]):
                self.params.pose3d_og[j] = self.params.global_rot_z.apply(self.params.pose3d_og[j])
                
            feet_middle = (self.params.pose3d_og[0] + self.params.pose3d_og[5])/2
            value = np.arctan2(feet_middle[2],-feet_middle[1]) * 57.295779513
            self.params.rot_change_x(value+90)
            self.rot_x_var.set(self.params.euler_rot_x)
        
            for j in range(self.params.pose3d_og.shape[0]):
                self.params.pose3d_og[j] = self.params.global_rot_x.apply(self.params.pose3d_og[j])

        if use_steamvr and self.params.calib_rot:
            feet_rot = self.params.pose3d_og[0] - self.params.pose3d_og[5]
            value = np.arctan2(feet_rot[0],feet_rot[2])
            value_hmd = np.arctan2(headsetrot.as_matrix()[0][0],headsetrot.as_matrix()[2][0])
            value = value - value_hmd
            value = -value
            self.params.rot_change_y(value * 57.295779513)
            self.rot_y_var.set(self.params.euler_rot_y)

        if use_steamvr and self.params.calib_scale:
            skelSize = np.max(self.params.pose3d_og, axis=0)-np.min(self.params.pose3d_og, axis=0)
            self.params.posescale = headsetpos[1]/skelSize[1]
            self.scale_var.set(self.params.posescale)

        self.params.recalibrate = False

    def pause_tracking(self):
        self.params.paused = not self.params.paused
        print(f"INFO: Pose estimation {'paused' if self.params.paused else 'unpaused'}")

def make_inference_gui(_params):
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    
    root = customtkinter.CTk()
    root.title("Inference Settings")
    InferenceWindow(root, _params)
    root.mainloop()
    
if __name__ == "__main__":
    print("hehe")
