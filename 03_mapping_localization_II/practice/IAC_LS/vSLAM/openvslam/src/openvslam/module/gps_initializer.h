#ifndef OPENVSLAM_MODULE_GPS_INITIALIZER_H
#define OPENVSLAM_MODULE_GPS_INITIALIZER_H

#include "openvslam/data/frame.h"
#include "openvslam/initialize/base.h"
#include "openvslam/gps/data.h"

namespace openvslam {

namespace data {
class frame;
class map_database;
} // namespace data

class mapping_module;

// initializer state
enum class gps_initializer_state_t {
    NotReady,
    AwaitingScaleInit,
    ScaleInitSucceeded,
    AwaitingRotationInit,
    RotationInitSucceeded
};


namespace module {

class gps_initializer {
public:
    gps_initializer() = delete;

    //! Constructor
    gps_initializer(data::map_database* map_db);

    /**
     * Destructor
     */
    ~gps_initializer() = default;

    //! Reset initializer
    void reset();

    //!
    void abort();

    //!
    bool is_running() const;

    /**
     * Enable loop detection
     */
    void enable_gps_initializer();

    /**
     * Disable loop detection
     */
    void disable_gps_initializer();

    /**
     * Get the loop detector status
     */
    bool is_enabled() const;

    /**
     * Get the loop detector status
     */
    bool is_map_scale_initialized() const;


    /**
     * Set the mapping module
     */
    void set_mapping_module(mapping_module* mapper);

    //! Get initialization state
    gps_initializer_state_t get_state() const;

    //! Initialize the map scale using GPS
    bool start_map_scale_initalization();

    //! Initialize the map rotation using GPS
    bool start_map_rotation_initalization();
private:
    //! map database
    data::map_database* map_db_ = nullptr;

    //! mapping module
    mapping_module* mapper_ = nullptr;

    //! current state of gps initializer
    gps_initializer_state_t state_ = gps_initializer_state_t::NotReady;

    //! Scaling up or down a initial map
    void scale_map(const double scale);

    //! gps data
    std::vector<gps::data> gps_data_;

    //! min traveled distance for scale init in [m]
    double min_traveled_distance_ = 0.01;

    //! min variance in trajectory for rotation init
    double min_variance_for_rot_init_ = 1.0;

    //-----------------------------------------
    // thread management

    //! mutex for access to pause procedure
    mutable std::mutex mtx_thread_;

    //! number of times loop BA is performed
    unsigned int num_exec_loop_BA_ = 0;

    //! flag to abort the scaling
    bool abort_gps_scaling_ = false;

    //! flag which indicates that gps scaling is running
    bool gps_scaling_is_running_ = false;

    //! is enabled flag
    bool is_initializer_enabled_ = false;

    //! map initialized
    bool map_scale_initialized_ = false;

    //! map initialized
    bool map_alignment_initialized_ = false;

    //! last initialized scale
    double last_scale_estimate_ = 0.0;
};

} // namespace module
} // namespace openvslam

#endif // OPENVSLAM_MODULE_INITIALIZER_H
