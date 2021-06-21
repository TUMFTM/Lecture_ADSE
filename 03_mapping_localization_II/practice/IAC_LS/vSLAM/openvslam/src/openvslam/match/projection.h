#ifndef OPENVSLAM_MATCH_PROJECTION_H
#define OPENVSLAM_MATCH_PROJECTION_H

#include "openvslam/type.h"
#include "openvslam/match/base.h"

#include <set>

namespace openvslam {

namespace data {
class frame;
class keyframe;
class landmark;
} // namespace data

namespace match {

class projection final : public base {
public:
    explicit projection(const float lowe_ratio = 0.6, const bool check_orientation = true)
        : base(lowe_ratio, check_orientation) {}

    ~projection() final = default;

    //! Calculates the correspondence between 2-dimensional points and 3-dimensional frames and records the correspondence information in frame.landmarks_.
    unsigned int match_frame_and_landmarks(data::frame& frm, const std::vector<data::landmark*>& local_landmarks, const float margin = 5.0) const;

    //! Reprojects the 3D points observed in the last frame to the current frame and records the corresponding information in frame.landmarks_.
    unsigned int match_current_and_last_frames(data::frame& curr_frm, const data::frame& last_frm, const float margin) const;

    //! Reprojects the 3D points observed by keyframe to the current frame and records the corresponding information in frame.landmarks_.
    //! If the current frame has already been mapped to the current frame, specify "already_matched_lms" to avoid reprojection
    unsigned int match_frame_and_keyframe(data::frame& curr_frm, data::keyframe* keyfrm, const std::set<data::landmark*>& already_matched_lms,
                                          const float margin, const unsigned int hamm_dist_thr) const;

    //! Convert 3D points to coordinates in Sim3, re-project them onto a keyframe, and record the corresponding information in matched_lms_in_keyfrm
    //! If matched_lms_in_keyfrm already contains the corresponding information, it is excluded from the search.
    //! (NOTE: keyframe's feature points and matched_lms_in_keyfrm.size() are the same.)
    unsigned int match_by_Sim3_transform(data::keyframe* keyfrm, const Mat44_t& Sim3_cw, const std::vector<data::landmark*>& landmarks,
                                         std::vector<data::landmark*>& matched_lms_in_keyfrm, const float margin) const;

    //! Using the specified Sim3, the 3D points observed in each keyframe are transformed and reprojected to the other keyframe, and the corresponding points are found
    //! matched_lms_in_keyfrm_1 records the 3D points observed by keyframe2 that correspond to the feature points (index) of keyframe1.
    unsigned int match_keyframes_mutually(data::keyframe* keyfrm_1, data::keyframe* keyfrm_2, std::vector<data::landmark*>& matched_lms_in_keyfrm_1,
                                          const float& s_12, const Mat33_t& rot_12, const Vec3_t& trans_12, const float margin) const;
};

} // namespace match
} // namespace openvslam

#endif // OPENVSLAM_MATCH_PROJECTION_H
