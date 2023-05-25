from .transform import *

class Matrix:
    def __init__(self):

        self.r_vec    = None
        self.t_vec    = None
        self.T        = None
        self.invT     = None

    def from_r_euler(self, r_vec):
        if isinstance(r_vec, list):
            self.r_vec = np.array(r_vec)
        else:
            self.r_vec = r_vec

        self.r_vec = deg2rad(self.r_vec)

        if self.t_vec is not None:
            self.T = get_T(self.r_vec, self.t_vec)
            self.invT = get_inv(self.T)

    def from_r_vector(self, r_vec):
        if isinstance(r_vec, list):
            self.r_vec = np.array(r_vec)
        else:
            self.r_vec = r_vec

        if self.t_vec is not None:
            self.T = get_T(self.r_vec, self.t_vec)
            self.invT = get_inv(self.T)

    def from_t_vector(self, t_vec):
        if isinstance(t_vec, list):
            self.t_vec = np.array(t_vec)
        else:
            self.t_vec = t_vec

        if self.r_vec is not None:
            self.T = get_T(self.r_vec, self.t_vec)
            self.invT = get_inv(self.T)

    def from_T(self, T):
        self.T = T
        self.invT = get_inv(T)

        self.r_vec, self.t_vec = get_rt(T)

    def from_invT(self, invT):
        self.invT = invT
        self.T = get_inv(invT)

        self.r_vec, self.t_vec = get_rt(self.T)

    def get_r_vector(self):
        return self.r_vec

    def get_r_euler(self):
        return rad2deg(self.r_vec)

    def get_r_matrix(self):
        return self.T[:3, :3]

    def get_t_vector(self):
        return self.t_vec

    def get_T(self):
        return self.T

    def get_inv(self):
        return self.invT
