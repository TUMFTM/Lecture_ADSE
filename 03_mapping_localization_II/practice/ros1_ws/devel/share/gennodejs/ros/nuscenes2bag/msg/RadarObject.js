// Auto-generated. Do not edit!

// (in-package nuscenes2bag.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class RadarObject {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.pose = null;
      this.dyn_prop = null;
      this.id = null;
      this.rcs = null;
      this.vx = null;
      this.vy = null;
      this.vx_comp = null;
      this.vy_comp = null;
      this.is_quality_valid = null;
      this.ambig_state = null;
      this.x_rms = null;
      this.y_rms = null;
      this.invalid_state = null;
      this.pdh0 = null;
      this.vx_rms = null;
      this.vy_rms = null;
    }
    else {
      if (initObj.hasOwnProperty('pose')) {
        this.pose = initObj.pose
      }
      else {
        this.pose = new geometry_msgs.msg.Vector3();
      }
      if (initObj.hasOwnProperty('dyn_prop')) {
        this.dyn_prop = initObj.dyn_prop
      }
      else {
        this.dyn_prop = 0;
      }
      if (initObj.hasOwnProperty('id')) {
        this.id = initObj.id
      }
      else {
        this.id = 0;
      }
      if (initObj.hasOwnProperty('rcs')) {
        this.rcs = initObj.rcs
      }
      else {
        this.rcs = 0.0;
      }
      if (initObj.hasOwnProperty('vx')) {
        this.vx = initObj.vx
      }
      else {
        this.vx = 0.0;
      }
      if (initObj.hasOwnProperty('vy')) {
        this.vy = initObj.vy
      }
      else {
        this.vy = 0.0;
      }
      if (initObj.hasOwnProperty('vx_comp')) {
        this.vx_comp = initObj.vx_comp
      }
      else {
        this.vx_comp = 0.0;
      }
      if (initObj.hasOwnProperty('vy_comp')) {
        this.vy_comp = initObj.vy_comp
      }
      else {
        this.vy_comp = 0.0;
      }
      if (initObj.hasOwnProperty('is_quality_valid')) {
        this.is_quality_valid = initObj.is_quality_valid
      }
      else {
        this.is_quality_valid = 0;
      }
      if (initObj.hasOwnProperty('ambig_state')) {
        this.ambig_state = initObj.ambig_state
      }
      else {
        this.ambig_state = 0;
      }
      if (initObj.hasOwnProperty('x_rms')) {
        this.x_rms = initObj.x_rms
      }
      else {
        this.x_rms = 0;
      }
      if (initObj.hasOwnProperty('y_rms')) {
        this.y_rms = initObj.y_rms
      }
      else {
        this.y_rms = 0;
      }
      if (initObj.hasOwnProperty('invalid_state')) {
        this.invalid_state = initObj.invalid_state
      }
      else {
        this.invalid_state = 0;
      }
      if (initObj.hasOwnProperty('pdh0')) {
        this.pdh0 = initObj.pdh0
      }
      else {
        this.pdh0 = 0;
      }
      if (initObj.hasOwnProperty('vx_rms')) {
        this.vx_rms = initObj.vx_rms
      }
      else {
        this.vx_rms = 0;
      }
      if (initObj.hasOwnProperty('vy_rms')) {
        this.vy_rms = initObj.vy_rms
      }
      else {
        this.vy_rms = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type RadarObject
    // Serialize message field [pose]
    bufferOffset = geometry_msgs.msg.Vector3.serialize(obj.pose, buffer, bufferOffset);
    // Serialize message field [dyn_prop]
    bufferOffset = _serializer.uint8(obj.dyn_prop, buffer, bufferOffset);
    // Serialize message field [id]
    bufferOffset = _serializer.uint16(obj.id, buffer, bufferOffset);
    // Serialize message field [rcs]
    bufferOffset = _serializer.float32(obj.rcs, buffer, bufferOffset);
    // Serialize message field [vx]
    bufferOffset = _serializer.float32(obj.vx, buffer, bufferOffset);
    // Serialize message field [vy]
    bufferOffset = _serializer.float32(obj.vy, buffer, bufferOffset);
    // Serialize message field [vx_comp]
    bufferOffset = _serializer.float32(obj.vx_comp, buffer, bufferOffset);
    // Serialize message field [vy_comp]
    bufferOffset = _serializer.float32(obj.vy_comp, buffer, bufferOffset);
    // Serialize message field [is_quality_valid]
    bufferOffset = _serializer.uint8(obj.is_quality_valid, buffer, bufferOffset);
    // Serialize message field [ambig_state]
    bufferOffset = _serializer.uint8(obj.ambig_state, buffer, bufferOffset);
    // Serialize message field [x_rms]
    bufferOffset = _serializer.uint8(obj.x_rms, buffer, bufferOffset);
    // Serialize message field [y_rms]
    bufferOffset = _serializer.uint8(obj.y_rms, buffer, bufferOffset);
    // Serialize message field [invalid_state]
    bufferOffset = _serializer.uint8(obj.invalid_state, buffer, bufferOffset);
    // Serialize message field [pdh0]
    bufferOffset = _serializer.uint8(obj.pdh0, buffer, bufferOffset);
    // Serialize message field [vx_rms]
    bufferOffset = _serializer.uint8(obj.vx_rms, buffer, bufferOffset);
    // Serialize message field [vy_rms]
    bufferOffset = _serializer.uint8(obj.vy_rms, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type RadarObject
    let len;
    let data = new RadarObject(null);
    // Deserialize message field [pose]
    data.pose = geometry_msgs.msg.Vector3.deserialize(buffer, bufferOffset);
    // Deserialize message field [dyn_prop]
    data.dyn_prop = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [id]
    data.id = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [rcs]
    data.rcs = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [vx]
    data.vx = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [vy]
    data.vy = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [vx_comp]
    data.vx_comp = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [vy_comp]
    data.vy_comp = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [is_quality_valid]
    data.is_quality_valid = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [ambig_state]
    data.ambig_state = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [x_rms]
    data.x_rms = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [y_rms]
    data.y_rms = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [invalid_state]
    data.invalid_state = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [pdh0]
    data.pdh0 = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [vx_rms]
    data.vx_rms = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [vy_rms]
    data.vy_rms = _deserializer.uint8(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 55;
  }

  static datatype() {
    // Returns string type for a message object
    return 'nuscenes2bag/RadarObject';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '2dca0314b6fc449f331ba195c716ed10';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new RadarObject(null);
    if (msg.pose !== undefined) {
      resolved.pose = geometry_msgs.msg.Vector3.Resolve(msg.pose)
    }
    else {
      resolved.pose = new geometry_msgs.msg.Vector3()
    }

    if (msg.dyn_prop !== undefined) {
      resolved.dyn_prop = msg.dyn_prop;
    }
    else {
      resolved.dyn_prop = 0
    }

    if (msg.id !== undefined) {
      resolved.id = msg.id;
    }
    else {
      resolved.id = 0
    }

    if (msg.rcs !== undefined) {
      resolved.rcs = msg.rcs;
    }
    else {
      resolved.rcs = 0.0
    }

    if (msg.vx !== undefined) {
      resolved.vx = msg.vx;
    }
    else {
      resolved.vx = 0.0
    }

    if (msg.vy !== undefined) {
      resolved.vy = msg.vy;
    }
    else {
      resolved.vy = 0.0
    }

    if (msg.vx_comp !== undefined) {
      resolved.vx_comp = msg.vx_comp;
    }
    else {
      resolved.vx_comp = 0.0
    }

    if (msg.vy_comp !== undefined) {
      resolved.vy_comp = msg.vy_comp;
    }
    else {
      resolved.vy_comp = 0.0
    }

    if (msg.is_quality_valid !== undefined) {
      resolved.is_quality_valid = msg.is_quality_valid;
    }
    else {
      resolved.is_quality_valid = 0
    }

    if (msg.ambig_state !== undefined) {
      resolved.ambig_state = msg.ambig_state;
    }
    else {
      resolved.ambig_state = 0
    }

    if (msg.x_rms !== undefined) {
      resolved.x_rms = msg.x_rms;
    }
    else {
      resolved.x_rms = 0
    }

    if (msg.y_rms !== undefined) {
      resolved.y_rms = msg.y_rms;
    }
    else {
      resolved.y_rms = 0
    }

    if (msg.invalid_state !== undefined) {
      resolved.invalid_state = msg.invalid_state;
    }
    else {
      resolved.invalid_state = 0
    }

    if (msg.pdh0 !== undefined) {
      resolved.pdh0 = msg.pdh0;
    }
    else {
      resolved.pdh0 = 0
    }

    if (msg.vx_rms !== undefined) {
      resolved.vx_rms = msg.vx_rms;
    }
    else {
      resolved.vx_rms = 0
    }

    if (msg.vy_rms !== undefined) {
      resolved.vy_rms = msg.vy_rms;
    }
    else {
      resolved.vy_rms = 0
    }

    return resolved;
    }
};

module.exports = RadarObject;
