from .transform import *

class Matrix:
    def __init__(self):

        self.rmat  = None
        self.rvec  = None
        self.tvec  = None
        self.euler = None
        self.T     = None
        self.invT  = None

    def set_rmat(self, rmat):
        if isinstance(rmat, list):
            self.rmat = np.array(rmat)
        else:
            self.rmat = rmat

        self.update('mat')

    def set_euler(self, euler):
        if isinstance(euler, list):
            self.euler = np.array(euler)
        else:
            self.euler = euler

        self.update('euler')

    def set_rvec(self, rvec, unit: str):
        if isinstance(rvec, list):
            self.rvec = np.array(rvec)
        else:
            self.rvec = rvec

        if unit == 'deg':
            self.rvec = deg2rad(self.rvec)
        elif unit == 'rad':
            self.rvec = self.rvec
        else:
            self.rvec = None
            raise ValueError("Select unit = 'deg' or 'rad'")

        self.update('vec')

    def set_tvec(self, tvec, unit: str = 'm'):
        if isinstance(tvec, list):
            self.tvec = np.array(tvec)
        else:
            self.tvec = tvec

        if unit == 'm':
            pass
        elif unit == 'cm':
            self.tvec /= 100.0
        elif unit == 'mm':
            self.tvec /= 1000.0
        else:
            self.tvec = None
            raise ValueError("Select unit = 'm' or 'cm' or 'mm'")

        self.update('vec')

    def set_T(self, T):
        self.T = T

        self.update('T')

    def set_invT(self, invT):
        self.invT = invT

        self.update('invT')

    def get_rvec(self, unit: str):
        if unit == 'deg':
            return rad2deg(self.rvec)
        elif unit == 'rad':
            return self.rvec
        else:
            raise ValueError("Select unit = 'deg' or 'rad'")

    def get_rmat(self):
        return self.T[:3, :3]

    def get_euler(self, unit: str):
        if unit == 'deg':
            return rad2deg(self.euler)
        elif unit == 'rad':
            return self.euler
        else:
            raise ValueError("Select unit = 'deg' or 'rad'")

    def get_tvec(self, unit: str = 'm'):
        if unit == 'm':
            return self.tvec
        elif unit == 'cm':
            return self.tvec * 100.0
        elif unit == 'mm':
            return self.tvec * 1000.0
        else:
            raise ValueError("Select unit = 'm' or 'cm' or 'mm'")

    def get_T(self):
        return self.T

    def get_invT(self):
        return self.invT

    def update(self, _in):
        if _in == 'vec':
            self.rmat  = vec2matrix(self.rvec)
            self.euler = rodrigues2euler(self.rvec)

            if self.rvec is not None and self.tvec is not None:
                self.T = get_T(self.rvec, self.tvec)
                self.invT = get_inv(self.T)

        elif _in == 'mat':
            self.rvec = matrix2vec(self.rmat)
            self.euler = rodrigues2euler(self.rvec)

            if self.tvec is not None:
                self.T = get_T(self.rvec, self.tvec)
                self.invT = get_inv(self.T)

        elif _in == 'euler':
            self.rvec = euler2rodrigues(self.euler)
            self.rmat = vec2matrix(self.rvec)

            if self.tvec is not None:
                self.T = get_T(self.rvec, self.tvec)
                self.invT = get_inv(self.T)

        elif _in == 'T':
            self.invT = get_inv(self.T)
            self.rvec, self.tvec = get_rt(self.T)
            self.rmat  = vec2matrix(self.rvec)
            self.euler = rodrigues2euler(self.rvec)

        elif _in == 'invT':
            self.T = get_inv(self.invT)
            self.rvec, self.tvec = get_rt(self.T)
            self.rmat = vec2matrix(self.rvec)
            self.euler = rodrigues2euler(self.rvec)
