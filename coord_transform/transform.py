import math
import cv2
import numpy as np
np.set_printoptions(precision=8, suppress=True)


def get_inv(T):
    """
    :param T: Homogeneous transform matrix
    :return: T^-1 : Inverse matrix of T
    e.g.)
                   T = np.array([[ 0.18877622, -0.92434508, -0.33158666,  0.09341176],
                                 [-0.93929352, -0.26847365,  0.21365763, -0.14570963],
                                 [-0.28651566,  0.27112372, -0.91891278,  0.88386982],
                                 [ 0.        ,  0.        ,  0.        ,  1.        ]])

    inverse T (T^-1) = np.array([[ 0.18877622, -0.93929352, -0.28651566,  0.09874452],
                                 [-0.92434508, -0.26847365,  0.27112372, -0.19241257],
                                 [-0.33158666,  0.21365763, -0.91891279,  0.87430535],
                                 [ 0.        ,  0.        ,  0.        ,  1.        ]])

            T @ T^-1 = np.array([[ 1.,  0.,  0.,  0.],
                                 [ 0.,  1.,  0.,  0.],
                                 [ 0.,  0.,  1.,  0.],
                                 [ 0.,  0.,  0.,  1.]])
    """
    return np.linalg.inv(T)

def get_rt(T):
    """
    Return rotation vector and translation vector.
    Rotation vector is expressed in terms of Rodrigues
    :param T: Homogenous transform matrix
    :return: rotation vector, translation vector
             rotation vector   : [axis[0], axis[1], axis[2]]. not included 'angle'
             translation vector: [x, y, z]
    e.g.)
    T = 4 x 4 matrix
             r(3x3)  | t
        T =  -----------
             0  0  0 | 1

        -> T[:3, :3] (r) : rotation matrix
        -> T[:3,  3] (t) : translation vector
    """
    trans_vec = T[:3, 3]
    rot_vec, _ = cv2.Rodrigues(T[:3, :3])
    return rot_vec.reshape(3), trans_vec

def get_T(rot_vec, trans_vec):
    """

    :param rot_vec  : array of output rotation vectors (@sa Rodrigues)
    :param trans_vec: array of output translation vectors
    :return: Homogeneous matrix: [  R   | t]
                                 [0 0 0 | 1]
    """
    rot_matrix = vec2matrix(rot_vec)
    trans_vec  = trans_vec.astype(float).reshape(3)

    T = np.eye(4)

    T[:3, :3] = rot_matrix
    T[:3,  3] = trans_vec

    return T

def vec2matrix(rotation_vector):
    """
    Translation rotation vector to rotation matrix
    Rotation vector: 1 x 3
    Rotation matrix: 3 x 3
    :param rotation_vector: array of output rotation vectors (@sa Rodrigues)
    :return: array of rotation matrix ( 3 x 3 )
    """
    if not isinstance(rotation_vector, np.ndarray):
        rotation_vector = np.array(rotation_vector)
    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    return rotation_matrix

def matrix2vec(rotation_matrix):
    """
    Translation rotation matrix to rotation vector
    Rotation matrix: 3 x 3
    Rotation vector: 1 x 3
    :param rotation_matrix: array of output rotation matrix
    :return: array of rotation matrix ( 3 x 1 ) (@sa Rodrigues)
    """
    rotation_vector, _ = cv2.Rodrigues(rotation_matrix)
    return rotation_vector

def euler2rodrigues(euler_angle):
    """
    Translation euler angle to rotation vector.
    Size of vector (angle) is ignored.
    :param euler_angle: [R, P, Y] angle. Unit: rad
    :return: rotation vector: [axis[0], axis[1], [axis[2]]
    """
    angle = np.linalg.norm(euler_angle)
    axis = euler_angle / angle

    return axis


def rodrigues2euler(axis, angle=1):
    """
    Translation Rodrigues axis and angle to Euler angle
    :param axis: rotation vector
    :param angle:
    :return: Euler angle ( 3 x 1 )
    """
    return axis * angle

def rad2deg(args):
    """
    Convert degree to radian
    :param args: [rad1, rad2, ..., rad?] or rad
    :return: [deg1, deg2, ..., deg?] or deg
    """
    if isinstance(args, list):
        return [math.degrees(i) for i in args]
    elif isinstance(args, np.ndarray):
        return np.array([math.degrees(i) for i in args])
    else:
        return math.degrees(args)

def deg2rad(args):
    """
    Convert degree to radian
    :param args: [deg1, deg2, ..., deg?] or deg
    :return: [rad1, rad2, ..., rad?] or rad
    """
    if isinstance(args, list) or isinstance(args, tuple):
        return [math.radians(i) for i in args]
    elif isinstance(args, np.ndarray):
        return np.array([math.radians(i) for i in args])
    else:
        return math.radians(args)

def rotate(T, rotation_vector):
    """
    Rotate
    :param T: Homogenoeus
    :param rotation_vector:
    :return:
    """
    rotation_vector = deg2rad(rotation_vector)
    if T.shape == (4, 4):
        rotation_T = get_T(rotation_vector, [0, 0, 0])
    elif T.shape == (3, 3):
        rotation_T = vec2matrix(rotation_vector)
    else:
        raise ValueError('T shape is must be 4x4 or 3x3')
    return T @ rotation_T

def draw_axis(image, intrinsics, dist, r_vec, t_vec, size=0.05):
    """
    Draw axis
    :param image: BGR image
    :param intrinsics: Intrinsic parameters of camera
    :param dist: Distortion coefficients of camera
    :param r_vec: Rotation vector (@sa Rodrigues)
    :param t_vec: Translation vector
    :param size: Drawing axis size
    :return: image: An image with axis
    """
    return cv2.aruco.drawAxis(image, intrinsics, dist, r_vec, t_vec, size)
