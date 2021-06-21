
(cl:in-package :asdf)

(defsystem "nuscenes2bag-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "RadarObject" :depends-on ("_package_RadarObject"))
    (:file "_package_RadarObject" :depends-on ("_package"))
    (:file "RadarObjects" :depends-on ("_package_RadarObjects"))
    (:file "_package_RadarObjects" :depends-on ("_package"))
  ))