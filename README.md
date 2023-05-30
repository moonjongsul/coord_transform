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

print('1: ', cTm.get_tvec('m'))
print('2: ', cTm.get_tvec('mm'))
print('3: ', cTm.get_rvec('rad'))
print('4: ', cTm.get_rvec('deg'))
print('5: ', cTm.get_T())
print('6: ', cTm.get_invT())
~~~
~~~
1:  [0.1 0.2 0.3]
2:  [100. 200. 300.]
3:  [0.17453293 0.34906585 0.52359878]
4:  [10. 20. 30.]
5:  [[ 0.80893611 -0.45777385  0.36887053  0.1       ]
 [ 0.51656274  0.85302778 -0.0742061   0.2       ]
 [-0.2806872   0.25057276  0.92651389  0.3       ]
 [ 0.          0.          0.          1.        ]]
6:  [[ 0.80893611  0.51656274 -0.2806872  -0.1       ]
 [-0.45777385  0.85302778  0.25057276 -0.2       ]
 [ 0.36887053 -0.0742061   0.92651389 -0.3       ]
 [ 0.          0.          0.          1.        ]]
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

~~~