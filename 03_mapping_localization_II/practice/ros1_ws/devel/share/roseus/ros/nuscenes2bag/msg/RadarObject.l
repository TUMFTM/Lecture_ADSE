;; Auto-generated. Do not edit!


(when (boundp 'nuscenes2bag::RadarObject)
  (if (not (find-package "NUSCENES2BAG"))
    (make-package "NUSCENES2BAG"))
  (shadow 'RadarObject (find-package "NUSCENES2BAG")))
(unless (find-package "NUSCENES2BAG::RADAROBJECT")
  (make-package "NUSCENES2BAG::RADAROBJECT"))

(in-package "ROS")
;;//! \htmlinclude RadarObject.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass nuscenes2bag::RadarObject
  :super ros::object
  :slots (_pose _dyn_prop _id _rcs _vx _vy _vx_comp _vy_comp _is_quality_valid _ambig_state _x_rms _y_rms _invalid_state _pdh0 _vx_rms _vy_rms ))

(defmethod nuscenes2bag::RadarObject
  (:init
   (&key
    ((:pose __pose) (instance geometry_msgs::Vector3 :init))
    ((:dyn_prop __dyn_prop) 0)
    ((:id __id) 0)
    ((:rcs __rcs) 0.0)
    ((:vx __vx) 0.0)
    ((:vy __vy) 0.0)
    ((:vx_comp __vx_comp) 0.0)
    ((:vy_comp __vy_comp) 0.0)
    ((:is_quality_valid __is_quality_valid) 0)
    ((:ambig_state __ambig_state) 0)
    ((:x_rms __x_rms) 0)
    ((:y_rms __y_rms) 0)
    ((:invalid_state __invalid_state) 0)
    ((:pdh0 __pdh0) 0)
    ((:vx_rms __vx_rms) 0)
    ((:vy_rms __vy_rms) 0)
    )
   (send-super :init)
   (setq _pose __pose)
   (setq _dyn_prop (round __dyn_prop))
   (setq _id (round __id))
   (setq _rcs (float __rcs))
   (setq _vx (float __vx))
   (setq _vy (float __vy))
   (setq _vx_comp (float __vx_comp))
   (setq _vy_comp (float __vy_comp))
   (setq _is_quality_valid (round __is_quality_valid))
   (setq _ambig_state (round __ambig_state))
   (setq _x_rms (round __x_rms))
   (setq _y_rms (round __y_rms))
   (setq _invalid_state (round __invalid_state))
   (setq _pdh0 (round __pdh0))
   (setq _vx_rms (round __vx_rms))
   (setq _vy_rms (round __vy_rms))
   self)
  (:pose
   (&rest __pose)
   (if (keywordp (car __pose))
       (send* _pose __pose)
     (progn
       (if __pose (setq _pose (car __pose)))
       _pose)))
  (:dyn_prop
   (&optional __dyn_prop)
   (if __dyn_prop (setq _dyn_prop __dyn_prop)) _dyn_prop)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:rcs
   (&optional __rcs)
   (if __rcs (setq _rcs __rcs)) _rcs)
  (:vx
   (&optional __vx)
   (if __vx (setq _vx __vx)) _vx)
  (:vy
   (&optional __vy)
   (if __vy (setq _vy __vy)) _vy)
  (:vx_comp
   (&optional __vx_comp)
   (if __vx_comp (setq _vx_comp __vx_comp)) _vx_comp)
  (:vy_comp
   (&optional __vy_comp)
   (if __vy_comp (setq _vy_comp __vy_comp)) _vy_comp)
  (:is_quality_valid
   (&optional __is_quality_valid)
   (if __is_quality_valid (setq _is_quality_valid __is_quality_valid)) _is_quality_valid)
  (:ambig_state
   (&optional __ambig_state)
   (if __ambig_state (setq _ambig_state __ambig_state)) _ambig_state)
  (:x_rms
   (&optional __x_rms)
   (if __x_rms (setq _x_rms __x_rms)) _x_rms)
  (:y_rms
   (&optional __y_rms)
   (if __y_rms (setq _y_rms __y_rms)) _y_rms)
  (:invalid_state
   (&optional __invalid_state)
   (if __invalid_state (setq _invalid_state __invalid_state)) _invalid_state)
  (:pdh0
   (&optional __pdh0)
   (if __pdh0 (setq _pdh0 __pdh0)) _pdh0)
  (:vx_rms
   (&optional __vx_rms)
   (if __vx_rms (setq _vx_rms __vx_rms)) _vx_rms)
  (:vy_rms
   (&optional __vy_rms)
   (if __vy_rms (setq _vy_rms __vy_rms)) _vy_rms)
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Vector3 _pose
    (send _pose :serialization-length)
    ;; uint8 _dyn_prop
    1
    ;; uint16 _id
    2
    ;; float32 _rcs
    4
    ;; float32 _vx
    4
    ;; float32 _vy
    4
    ;; float32 _vx_comp
    4
    ;; float32 _vy_comp
    4
    ;; uint8 _is_quality_valid
    1
    ;; uint8 _ambig_state
    1
    ;; uint8 _x_rms
    1
    ;; uint8 _y_rms
    1
    ;; uint8 _invalid_state
    1
    ;; uint8 _pdh0
    1
    ;; uint8 _vx_rms
    1
    ;; uint8 _vy_rms
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Vector3 _pose
       (send _pose :serialize s)
     ;; uint8 _dyn_prop
       (write-byte _dyn_prop s)
     ;; uint16 _id
       (write-word _id s)
     ;; float32 _rcs
       (sys::poke _rcs (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _vx
       (sys::poke _vx (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _vy
       (sys::poke _vy (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _vx_comp
       (sys::poke _vx_comp (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _vy_comp
       (sys::poke _vy_comp (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; uint8 _is_quality_valid
       (write-byte _is_quality_valid s)
     ;; uint8 _ambig_state
       (write-byte _ambig_state s)
     ;; uint8 _x_rms
       (write-byte _x_rms s)
     ;; uint8 _y_rms
       (write-byte _y_rms s)
     ;; uint8 _invalid_state
       (write-byte _invalid_state s)
     ;; uint8 _pdh0
       (write-byte _pdh0 s)
     ;; uint8 _vx_rms
       (write-byte _vx_rms s)
     ;; uint8 _vy_rms
       (write-byte _vy_rms s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Vector3 _pose
     (send _pose :deserialize buf ptr-) (incf ptr- (send _pose :serialization-length))
   ;; uint8 _dyn_prop
     (setq _dyn_prop (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint16 _id
     (setq _id (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; float32 _rcs
     (setq _rcs (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _vx
     (setq _vx (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _vy
     (setq _vy (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _vx_comp
     (setq _vx_comp (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _vy_comp
     (setq _vy_comp (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; uint8 _is_quality_valid
     (setq _is_quality_valid (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _ambig_state
     (setq _ambig_state (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _x_rms
     (setq _x_rms (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _y_rms
     (setq _y_rms (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _invalid_state
     (setq _invalid_state (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _pdh0
     (setq _pdh0 (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _vx_rms
     (setq _vx_rms (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _vy_rms
     (setq _vy_rms (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get nuscenes2bag::RadarObject :md5sum-) "2dca0314b6fc449f331ba195c716ed10")
(setf (get nuscenes2bag::RadarObject :datatype-) "nuscenes2bag/RadarObject")
(setf (get nuscenes2bag::RadarObject :definition-)
      "geometry_msgs/Vector3 pose
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



(provide :nuscenes2bag/RadarObject "2dca0314b6fc449f331ba195c716ed10")


