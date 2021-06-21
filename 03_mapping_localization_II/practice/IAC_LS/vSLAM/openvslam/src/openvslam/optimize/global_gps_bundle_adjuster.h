#ifndef OPENVSLAM_OPTIMIZE_GLOBAL_GPS_BUNDLE_ADJUSTER_H
#define OPENVSLAM_OPTIMIZE_GLOBAL_GPS_BUNDLE_ADJUSTER_H

namespace openvslam {

namespace data {
class map_database;
} // namespace data

namespace optimize {

class global_gps_bundle_adjuster {
public:
    /**
     * Constructor
     * @param map_db
     * @param num_iter
     * @param use_huber_kernel
     */
    explicit global_gps_bundle_adjuster(data::map_database* map_db,
                                        const unsigned int num_iter = 50,
                                        const unsigned int nr_kfs_to_optim = 150,
                                        const bool use_huber_kernel = true);

    /**
     * Destructor
     */
    virtual ~global_gps_bundle_adjuster() = default;

    /**
     * Perform optimization
     * @param lead_keyfrm_id_in_global_BA
     * @param force_stop_flag
     */
    void optimize(const unsigned int lead_keyfrm_id_in_global_BA = 0, bool* const force_stop_flag = nullptr);

    /**
     * Check if optim is currently running
     * @brief is_running
     * @return bool if it is running
     */
    bool is_running();

private:

    void set_running();
    void set_finished();

    //! mutex for access to pause procedure
    //mutable std::mutex mtx_thread_;

    //! map database
    const data::map_database* map_db_;

    //! number of iterations of optimization
    unsigned int num_iter_;

    //! use Huber loss or not
    const bool use_huber_kernel_;

    //! how many keyframes we want to optimize from the current one
    size_t nr_kfs_to_optim_;

    //! if it is running
    bool is_running_ = false;
};

} // namespace optimize
} // namespace openvslam

#endif // OPENVSLAM_OPTIMIZE_GLOBAL_GPS_BUNDLE_ADJUSTER_H
