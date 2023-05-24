from typing import List, Dict
from .transform import *

ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

class ArucoDetector:
    def __init__(self,
                 aruco_size:       float,
                 aruco_type:       str,
                 camera_matrix:    np.ndarray,
                 dist_coefficient: np.ndarray):

        self.aruco_size       = aruco_size
        self.aruco_type       = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])
        self.parameters       = cv2.aruco.DetectorParameters_create()
        self.camera_matrix    = camera_matrix
        self.dist_coefficient = dist_coefficient

        self.target_ids       = None
        self.results          = dict()

    def get_pose(self, image:np.ndarray, target_id: List = None, draw: bool = True) -> (Dict, np.ndarray):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, self.aruco_type,
                                                                    parameters=self.parameters,
                                                                    cameraMatrix=self.camera_matrix,
                                                                    distCoeff=self.dist_coefficient)

        if corners:
            ids = ids.flatten().tolist()
            target_ix = []

            # Draw a square around the markers
            if draw:
                image = image[:, :, ::-1]  # RGB to BGR
                cv2.aruco.drawDetectedMarkers(image, corners)

            if target_id is not None:
                try:
                    target_ix = [ids.index(i) for i in target_id]
                except:
                    if draw:
                        image = image[:, :, ::-1]
                    return self.results, image
            else:
                target_ix = [i for i in range(len(ids))]
                target_id = ids

            if target_ix:
                for i, m_id in zip(target_ix, target_id):
                    """
                    Estimating the pose of the marker
                    
                    rotation_vec    : array of output rotation vectors (@sa Rodrigues)
                    translation_vec : array of output translation vectors
                    _ (_objPoints)  : array of object points of all the marker corners
                    """
                    rotation_vec, translation_vec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i],
                                                                                           self.aruco_size,
                                                                                           self.camera_matrix,
                                                                                           self.dist_coefficient)

                    rotation_vec    = np.array([y for y in rotation_vec[0][0][:]])
                    translation_vec = np.array([y for y in translation_vec[0][0][:]])

                    result = dict()
                    result['R'] = rotation_vec
                    result['T'] = translation_vec

                    cTm = get_T(rotation_vec, translation_vec)
                    mTc = get_inv(cTm)

                    result['cTm'] = cTm
                    result['mTc'] = mTc

                    self.results[m_id] = result

                    # Draw Axis
                    if draw:
                        image = draw_axis(image, self.camera_matrix, self.dist_coefficient,
                                          rotation_vec, translation_vec)

            if draw:
                image = image[:, :, ::-1]       # BGR to RGB

        return self.results, image

