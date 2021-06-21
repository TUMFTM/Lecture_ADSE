; Auto-generated. Do not edit!


(cl:in-package nuscenes2bag-msg)


;//! \htmlinclude RadarObjects.msg.html

(cl:defclass <RadarObjects> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (objects
    :reader objects
    :initarg :objects
    :type (cl:vector nuscenes2bag-msg:RadarObject)
   :initform (cl:make-array 0 :element-type 'nuscenes2bag-msg:RadarObject :initial-element (cl:make-instance 'nuscenes2bag-msg:RadarObject))))
)

(cl:defclass RadarObjects (<RadarObjects>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RadarObjects>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RadarObjects)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name nuscenes2bag-msg:<RadarObjects> is deprecated: use nuscenes2bag-msg:RadarObjects instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <RadarObjects>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:header-val is deprecated.  Use nuscenes2bag-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'objects-val :lambda-list '(m))
(cl:defmethod objects-val ((m <RadarObjects>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:objects-val is deprecated.  Use nuscenes2bag-msg:objects instead.")
  (objects m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RadarObjects>) ostream)
  "Serializes a message object of type '<RadarObjects>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'objects))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'objects))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RadarObjects>) istream)
  "Deserializes a message object of type '<RadarObjects>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'objects) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'objects)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'nuscenes2bag-msg:RadarObject))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RadarObjects>)))
  "Returns string type for a message object of type '<RadarObjects>"
  "nuscenes2bag/RadarObjects")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RadarObjects)))
  "Returns string type for a message object of type 'RadarObjects"
  "nuscenes2bag/RadarObjects")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RadarObjects>)))
  "Returns md5sum for a message object of type '<RadarObjects>"
  "c69401412379392af20b5a4c32b76eca")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RadarObjects)))
  "Returns md5sum for a message object of type 'RadarObjects"
  "c69401412379392af20b5a4c32b76eca")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RadarObjects>)))
  "Returns full string definition for message of type '<RadarObjects>"
  (cl:format cl:nil "std_msgs/Header header~%RadarObject[] objects~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: nuscenes2bag/RadarObject~%geometry_msgs/Vector3 pose~%uint8 dyn_prop~%uint16 id~%float32 rcs~%float32 vx~%float32 vy~%float32 vx_comp~%float32 vy_comp~%uint8 is_quality_valid~%uint8 ambig_state~%uint8 x_rms~%uint8 y_rms~%uint8 invalid_state~%uint8 pdh0~%uint8 vx_rms~%uint8 vy_rms~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RadarObjects)))
  "Returns full string definition for message of type 'RadarObjects"
  (cl:format cl:nil "std_msgs/Header header~%RadarObject[] objects~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: nuscenes2bag/RadarObject~%geometry_msgs/Vector3 pose~%uint8 dyn_prop~%uint16 id~%float32 rcs~%float32 vx~%float32 vy~%float32 vx_comp~%float32 vy_comp~%uint8 is_quality_valid~%uint8 ambig_state~%uint8 x_rms~%uint8 y_rms~%uint8 invalid_state~%uint8 pdh0~%uint8 vx_rms~%uint8 vy_rms~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RadarObjects>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'objects) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RadarObjects>))
  "Converts a ROS message object to a list"
  (cl:list 'RadarObjects
    (cl:cons ':header (header msg))
    (cl:cons ':objects (objects msg))
))
