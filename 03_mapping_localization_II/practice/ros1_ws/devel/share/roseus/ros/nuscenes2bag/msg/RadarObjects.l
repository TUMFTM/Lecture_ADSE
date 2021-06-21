;; Auto-generated. Do not edit!


(when (boundp 'nuscenes2bag::RadarObjects)
  (if (not (find-package "NUSCENES2BAG"))
    (make-package "NUSCENES2BAG"))
  (shadow 'RadarObjects (find-package "NUSCENES2BAG")))
(unless (find-package "NUSCENES2BAG::RADAROBJECTS")
  (make-package "NUSCENES2BAG::RADAROBJECTS"))

(in-package "ROS")
;;//! \htmlinclude RadarObjects.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass nuscenes2bag::RadarObjects
  :super ros::object
  :slots (_header _objects ))

(defmethod nuscenes2bag::RadarObjects
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:objects __objects) (let (r) (dotimes (i 0) (push (instance nuscenes2bag::RadarObject :init) r)) r))
    )
   (send-super :init)
   (setq _header __header)
   (setq _objects __objects)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:objects
   (&rest __objects)
   (if (keywordp (car __objects))
       (send* _objects __objects)
     (progn
       (if __objects (setq _objects (car __objects)))
       _objects)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; nuscenes2bag/RadarObject[] _objects
    (apply #'+ (send-all _objects :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; nuscenes2bag/RadarObject[] _objects
     (write-long (length _objects) s)
     (dolist (elem _objects)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; nuscenes2bag/RadarObject[] _objects
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _objects (let (r) (dotimes (i n) (push (instance nuscenes2bag::RadarObject :init) r)) r))
     (dolist (elem- _objects)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get nuscenes2bag::RadarObjects :md5sum-) "c69401412379392af20b5a4c32b76eca")
(setf (get nuscenes2bag::RadarObjects :datatype-) "nuscenes2bag/RadarObjects")
(setf (get nuscenes2bag::RadarObjects :definition-)
      "std_msgs/Header header
RadarObject[] objects
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: nuscenes2bag/RadarObject
geometry_msgs/Vector3 pose
uint8 dyn_prop
uint16 id
float32 rcs
float32 vx
float32 vy
float32 vx_comp
float32 vy_comp
uint8 is_quality_valid
uint8 ambig_state
uint8 x_rms
uint8 y_rms
uint8 invalid_state
uint8 pdh0
uint8 vx_rms
uint8 vy_rms
================================================================================
MSG: geometry_msgs/Vector3
# This represents a vector in free space. 
# It is only meant to represent a direction. Therefore, it does not
# make sense to apply a translation to it (e.g., when applying a 
# generic rigid transformation to a Vector3, tf2 will only apply the
# rotation). If you want your data to be translatable too, use the
# geometry_msgs/Point message instead.

float64 x
float64 y
float64 z
")



(provide :nuscenes2bag/RadarObjects "c69401412379392af20b5a4c32b76eca")


