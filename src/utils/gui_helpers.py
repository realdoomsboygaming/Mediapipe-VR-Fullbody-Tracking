import customtkinter
import json
import sys

def getparams():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    root = customtkinter.CTk()
    root.title("Initial settings")
    
    main_frame = customtkinter.CTkFrame(root)
    main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    notebook = customtkinter.CTkTabview(main_frame)
    notebook.pack(padx=10, pady=10, fill="both", expand=True)

    tab1 = notebook.add("General")
    tab2 = notebook.add("Camera")

    #
    # Gneral settings
    #
    
    general_frame = customtkinter.CTkFrame(tab1)
    general_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # camera ID
    customtkinter.CTkLabel(general_frame, text="IP or ID of camera:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    camid = customtkinter.CTkEntry(general_frame)
    camid.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    # backend
    customtkinter.CTkLabel(general_frame, text="Backend:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    backends = ["Dummy", "SteamVR", "VRChatOSC"]
    backendvar = customtkinter.StringVar(value=backends[1])
    backendmenu = customtkinter.CTkOptionMenu(general_frame, variable=backendvar, values=backends)
    backendmenu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    
    # IP and port
    customtkinter.CTkLabel(general_frame, text="IP:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    backendip = customtkinter.CTkEntry(general_frame)
    backendip.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    
    customtkinter.CTkLabel(general_frame, text="Port:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    backendport = customtkinter.CTkEntry(general_frame)
    backendport.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    # advanced
    advan = customtkinter.BooleanVar(value=False)
    customtkinter.CTkCheckBox(general_frame, text="Enable advanced mode", variable=advan).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")
    
    # foot rotation
    feetrot = customtkinter.BooleanVar(value=False)
    customtkinter.CTkCheckBox(general_frame, text="Enable experimental foot rotation", variable=feetrot).grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")
    
    # hand tracking
    usehands = customtkinter.BooleanVar(value=False)
    customtkinter.CTkCheckBox(general_frame, text="Enable hand tracking (requires additional setup)", variable=usehands).grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")
    
    # hip tracking
    ignorehip = customtkinter.BooleanVar(value=False)
    customtkinter.CTkCheckBox(general_frame, text="Disable hip tracker (for owotrack)", variable=ignorehip).grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")
    
    # webui
    webui = customtkinter.BooleanVar(value=False)
    customtkinter.CTkCheckBox(general_frame, text="Enable WebUI", variable=webui).grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    #
    # Camera settings
    #
    
    camera_frame = customtkinter.CTkFrame(tab2)
    camera_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # resolution
    customtkinter.CTkLabel(camera_frame, text="Camera width:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    camwidth = customtkinter.CTkEntry(camera_frame)
    camwidth.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    customtkinter.CTkLabel(camera_frame, text="Camera height:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    camheight = customtkinter.CTkEntry(camera_frame)
    camheight.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    # settings
    camsettings = customtkinter.BooleanVar(value=False)
    customtkinter.CTkCheckBox(camera_frame, text="Attempt to open camera settings", variable=camsettings).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
    
    # mediapipe settings
    customtkinter.CTkLabel(camera_frame, text="Model complexity:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    modelcomp = customtkinter.CTkEntry(camera_frame)
    modelcomp.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    customtkinter.CTkLabel(camera_frame, text="Min tracking confidence:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    mintrack = customtkinter.CTkEntry(camera_frame)
    mintrack.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
    
    customtkinter.CTkLabel(camera_frame, text="Smooth landmarks:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    smooth = customtkinter.BooleanVar(value=True)
    customtkinter.CTkCheckBox(camera_frame, text="", variable=smooth).grid(row=5, column=1, padx=5, pady=5, sticky="w")

    customtkinter.CTkLabel(camera_frame, text="Static image mode:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
    static = customtkinter.BooleanVar(value=False)
    customtkinter.CTkCheckBox(camera_frame, text="", variable=static).grid(row=6, column=1, padx=5, pady=5, sticky="w")

    customtkinter.CTkLabel(camera_frame, text="Max image size:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
    imgsize = customtkinter.CTkEntry(camera_frame)
    imgsize.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
    
    try:
        with open("config.json", "r") as f:
            param = json.load(f)
    except:
        print("INFO: No config file used")
        param = {}

    camid.insert(0, param.get("camid", "0"))
    advan.set(param.get("advanced", False))
    feetrot.set(param.get("feet_rotation", False))
    usehands.set(param.get("use_hands", False))
    ignorehip.set(param.get("ignore_hip", False))
    webui.set(param.get("webui", False))
    camwidth.insert(0, param.get("camera_width", 0))
    camheight.insert(0, param.get("camera_height", 0))
    camsettings.set(param.get("camera_settings", False))
    modelcomp.delete(0, customtkinter.END)
    modelcomp.insert(0, param.get("model_complexity", 1))
    mintrack.delete(0, customtkinter.END)
    mintrack.insert(0, param.get("min_tracking_confidence", 0.5))
    smooth.set(param.get("smooth_landmarks", True))
    static.set(param.get("static_image", False))
    imgsize.delete(0, customtkinter.END)
    imgsize.insert(0, param.get("imgsize", 1000))
    backendvar.set(backends[param.get("backend", 1)])
    backendip.delete(0, customtkinter.END)
    backendip.insert(0, param.get("backend_ip", "127.0.0.1"))
    backendport.delete(0, customtkinter.END)
    backendport.insert(0, param.get("backend_port", 9000))

    param_return = {}
    
    def on_closing():
        #get all parameters
        param_return["camid"] = camid.get()
        param_return["camera_settings"] = camsettings.get()

        try:
            param_return["camera_width"] = int(camwidth.get())
        except:
            param_return["camera_width"] = 0
            
        try:
            param_return["camera_height"] = int(camheight.get())
        except:
            param_return["camera_height"] = 0
            
        param_return["advanced"] = advan.get()

        param_return["model_complexity"] = int(modelcomp.get())
        param_return["smooth_landmarks"] = smooth.get()
        param_return["min_tracking_confidence"] = float(mintrack.get())
        param_return["static_image"] = static.get()
        param_return["imgsize"] = int(imgsize.get())
        
        param_return["feet_rotation"] = feetrot.get()
        param_return["use_hands"] = usehands.get()
        param_return["ignore_hip"] = ignorehip.get()

        param_return["backend"] = backends.index(backendvar.get())
        
        param_return["backend_ip"] = backendip.get()
        try:
            param_return["backend_port"] = int(backendport.get())
        except:
            param_return["backend_port"] = 9000
            
        param_return["webui"] = webui.get()
        
        param_return["hmd_to_neck_offset"] = [0, -0.2, 0.1]
        param_return["preview_skeleton"] = False
        param_return["waithmd"] = False
        
        with open("config.json", "w") as f:
            json.dump(param_return, f, indent=4)

        root.destroy()
        
    def save_close():
        on_closing()

    def just_exit():
        sys.exit()

    button_frame = customtkinter.CTkFrame(main_frame)
    button_frame.pack(pady=10)
    customtkinter.CTkButton(button_frame, text="Save and continue", command=save_close).grid(row=0, column=0, padx=5)
    customtkinter.CTkButton(button_frame, text="Exit", command=just_exit).grid(row=0, column=1, padx=5)
    
    root.protocol("WM_DELETE_WINDOW", just_exit)

    root.mainloop()
    return param_return
