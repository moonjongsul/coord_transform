# coord_transform
coordinate transform library


## Installation
~~~
$ cd </root>
$ git clone https://github.com/moonjongsul/coord_transform.git
$ cd coord_transform
$ ./install.sh
~~~

## Usage
### coordinate transform
~~~
import coord_transform as ct

cTm = ct.Matrix()
cTm.set_rvec([10, 20, 30], 'deg')
cTm.set_tvec([0.1, 0.2, 0.3])

print(cTm.get_tvec('m'))
print(cTm.get_tvec('mm'))
print(cTm.get_rvec('rad'))
print(cTm.get_rvec('deg'))
print(cTm.get_T())
print(cTm.get_invT())
~~~

### ArucoDetector
~~~
from pprint import pprint
import cv2
import numpy as np

from ketisdk.sensor.realsense_sensor import RSSensor
from coord_transform import ArucoDetector
import coord_transform as ct


if __name__ == '__main__':

    sensor = RSSensor()
    sensor.start()

    marker_size = 0.16  # unit: meter
    # marker_type = "DICT_5X5_100"
    marker_type = "DICT_7X7_1000"

    k = [[sensor.info.fx, 0, sensor.info.cx],
         [0, sensor.info.fy, sensor.info.cy],
         [0, 0, 1]]
    k = np.array(k)
    d = np.array([[0.0, 0.0, 0.0, 0.0, 0.0]])

    aruco = ArucoDetector(marker_size, marker_type, k, d)

    while True:
        image, depth = sensor.get_data()

        results, result_img = aruco.get_pose(image)

        pprint(results)
        cv2.imshow('Estimated Pose', result_img[:, :, ::-1])

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

~~~s