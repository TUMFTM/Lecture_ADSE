; Auto-generated. Do not edit!


(cl:in-package nuscenes2bag-msg)


;//! \htmlinclude RadarObject.msg.html

(cl:defclass <RadarObject> (roslisp-msg-protocol:ros-message)
  ((pose
    :reader pose
    :initarg :pose
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (dyn_prop
    :reader dyn_prop
    :initarg :dyn_prop
    :type cl:fixnum
    :initform 0)
   (id
    :reader id
    :initarg :id
    :type cl:fixnum
    :initform 0)
   (rcs
    :reader rcs
    :initarg :rcs
    :type cl:float
    :initform 0.0)
   (vx
    :reader vx
    :initarg :vx
    :type cl:float
    :initform 0.0)
   (vy
    :reader vy
    :initarg :vy
    :type cl:float
    :initform 0.0)
   (vx_comp
    :reader vx_comp
    :initarg :vx_comp
    :type cl:float
    :initform 0.0)
   (vy_comp
    :reader vy_comp
    :initarg :vy_comp
    :type cl:float
    :initform 0.0)
   (is_quality_valid
    :reader is_quality_valid
    :initarg :is_quality_valid
    :type cl:fixnum
    :initform 0)
   (ambig_state
    :reader ambig_state
    :initarg :ambig_state
    :type cl:fixnum
    :initform 0)
   (x_rms
    :reader x_rms
    :initarg :x_rms
    :type cl:fixnum
    :initform 0)
   (y_rms
    :reader y_rms
    :initarg :y_rms
    :type cl:fixnum
    :initform 0)
   (invalid_state
    :reader invalid_state
    :initarg :invalid_state
    :type cl:fixnum
    :initform 0)
   (pdh0
    :reader pdh0
    :initarg :pdh0
    :type cl:fixnum
    :initform 0)
   (vx_rms
    :reader vx_rms
    :initarg :vx_rms
    :type cl:fixnum
    :initform 0)
   (vy_rms
    :reader vy_rms
    :initarg :vy_rms
    :type cl:fixnum
    :initform 0))
)

(cl:defclass RadarObject (<RadarObject>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RadarObject>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RadarObject)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name nuscenes2bag-msg:<RadarObject> is deprecated: use nuscenes2bag-msg:RadarObject instead.")))

(cl:ensure-generic-function 'pose-val :lambda-list '(m))
(cl:defmethod pose-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:pose-val is deprecated.  Use nuscenes2bag-msg:pose instead.")
  (pose m))

(cl:ensure-generic-function 'dyn_prop-val :lambda-list '(m))
(cl:defmethod dyn_prop-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:dyn_prop-val is deprecated.  Use nuscenes2bag-msg:dyn_prop instead.")
  (dyn_prop m))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:id-val is deprecated.  Use nuscenes2bag-msg:id instead.")
  (id m))

(cl:ensure-generic-function 'rcs-val :lambda-list '(m))
(cl:defmethod rcs-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:rcs-val is deprecated.  Use nuscenes2bag-msg:rcs instead.")
  (rcs m))

(cl:ensure-generic-function 'vx-val :lambda-list '(m))
(cl:defmethod vx-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:vx-val is deprecated.  Use nuscenes2bag-msg:vx instead.")
  (vx m))

(cl:ensure-generic-function 'vy-val :lambda-list '(m))
(cl:defmethod vy-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:vy-val is deprecated.  Use nuscenes2bag-msg:vy instead.")
  (vy m))

(cl:ensure-generic-function 'vx_comp-val :lambda-list '(m))
(cl:defmethod vx_comp-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:vx_comp-val is deprecated.  Use nuscenes2bag-msg:vx_comp instead.")
  (vx_comp m))

(cl:ensure-generic-function 'vy_comp-val :lambda-list '(m))
(cl:defmethod vy_comp-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:vy_comp-val is deprecated.  Use nuscenes2bag-msg:vy_comp instead.")
  (vy_comp m))

(cl:ensure-generic-function 'is_quality_valid-val :lambda-list '(m))
(cl:defmethod is_quality_valid-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:is_quality_valid-val is deprecated.  Use nuscenes2bag-msg:is_quality_valid instead.")
  (is_quality_valid m))

(cl:ensure-generic-function 'ambig_state-val :lambda-list '(m))
(cl:defmethod ambig_state-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:ambig_state-val is deprecated.  Use nuscenes2bag-msg:ambig_state instead.")
  (ambig_state m))

(cl:ensure-generic-function 'x_rms-val :lambda-list '(m))
(cl:defmethod x_rms-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:x_rms-val is deprecated.  Use nuscenes2bag-msg:x_rms instead.")
  (x_rms m))

(cl:ensure-generic-function 'y_rms-val :lambda-list '(m))
(cl:defmethod y_rms-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:y_rms-val is deprecated.  Use nuscenes2bag-msg:y_rms instead.")
  (y_rms m))

(cl:ensure-generic-function 'invalid_state-val :lambda-list '(m))
(cl:defmethod invalid_state-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:invalid_state-val is deprecated.  Use nuscenes2bag-msg:invalid_state instead.")
  (invalid_state m))

(cl:ensure-generic-function 'pdh0-val :lambda-list '(m))
(cl:defmethod pdh0-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:pdh0-val is deprecated.  Use nuscenes2bag-msg:pdh0 instead.")
  (pdh0 m))

(cl:ensure-generic-function 'vx_rms-val :lambda-list '(m))
(cl:defmethod vx_rms-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:vx_rms-val is deprecated.  Use nuscenes2bag-msg:vx_rms instead.")
  (vx_rms m))

(cl:ensure-generic-function 'vy_rms-val :lambda-list '(m))
(cl:defmethod vy_rms-val ((m <RadarObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader nuscenes2bag-msg:vy_rms-val is deprecated.  Use nuscenes2bag-msg:vy_rms instead.")
  (vy_rms m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RadarObject>) ostream)
  "Serializes a message object of type '<RadarObject>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'pose) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'dyn_prop)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'id)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'rcs))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'vx))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'vy))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'vx_comp))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'vy_comp))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'is_quality_valid)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'ambig_state)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'x_rms)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'y_rms)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'invalid_state)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pdh0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'vx_rms)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'vy_rms)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RadarObject>) istream)
  "Deserializes a message object of type '<RadarObject>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'pose) istream)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'dyn_prop)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'rcs) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'vx) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'vy) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'vx_comp) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'vy_comp) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'is_quality_valid)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'ambig_state)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'x_rms)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'y_rms)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'invalid_state)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pdh0)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'vx_rms)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'vy_rms)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RadarObject>)))
  "Returns string type for a message object of type '<RadarObject>"
  "nuscenes2bag/RadarObject")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RadarObject)))
  "Returns string type for a message object of type 'RadarObject"
  "nuscenes2bag/RadarObject")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RadarObject>)))
  "Returns md5sum for a message object of type '<RadarObject>"
  "2dca0314b6fc449f331ba195c716ed10")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RadarObject)))
  "Returns md5sum for a message object of type 'RadarObject"
  "2dca0314b6fc449f331ba195c716ed10")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RadarObject>)))
  "Returns full string definition for message of type '<RadarObject>"
  (cl:format cl:nil "geometry_msgs/Vector3 pose~%uint8 dyn_prop~%uint16 id~%float32 rcs~%float32 vx~%float32 vy~%float32 vx_comp~%float32 vy_comp~%uint8 is_quality_valid~%uint8 ambig_state~%uint8 x_rms~%uint8 y_rms~%uint8 invalid_state~%uint8 pdh0~%uint8 vx_rms~%uint8 vy_rms~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RadarObject)))
  "Returns full string definition for message of type 'RadarObject"
  (cl:format cl:nil "geometry_msgs/Vector3 pose~%uint8 dyn_prop~%uint16 id~%float32 rcs~%float32 vx~%float32 vy~%float32 vx_comp~%float32 vy_comp~%uint8 is_quality_valid~%uint8 ambig_state~%uint8 x_rms~%uint8 y_rms~%uint8 invalid_state~%uint8 pdh0~%uint8 vx_rms~%uint8 vy_rms~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RadarObject>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'pose))
     1
     2
     4
     4
     4
     4
     4
     1
     1
     1
     1
     1
     1
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RadarObject>))
  "Converts a ROS message object to a list"
  (cl:list 'RadarObject
    (cl:cons ':pose (pose msg))
    (cl:cons ':dyn_prop (dyn_prop msg))
    (cl:cons ':id (id msg))
    (cl:cons ':rcs (rcs msg))
    (cl:cons ':vx (vx msg))
    (cl:cons ':vy (vy msg))
    (cl:cons ':vx_comp (vx_comp msg))
    (cl:cons ':vy_comp (vy_comp msg))
    (cl:cons ':is_quality_valid (is_quality_valid msg))
    (cl:cons ':ambig_state (ambig_state msg))
    (cl:cons ':x_rms (x_rms msg))
    (cl:cons ':y_rms (y_rms msg))
    (cl:cons ':invalid_state (invalid_state msg))
    (cl:cons ':pdh0 (pdh0 msg))
    (cl:cons ':vx_rms (vx_rms msg))
    (cl:cons ':vy_rms (vy_rms msg))
))
