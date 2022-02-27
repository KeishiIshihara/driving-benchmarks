# Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# CORL experiment set.

from __future__ import print_function


from ...benchmark_tools.experiment import Experiment
from ...carla.sensor import Camera
from ...carla.settings import CarlaSettings
from ...benchmark_tools.experiment_suites.experiment_suite import ExperimentSuite


class CoRL2017Nav(ExperimentSuite):

    @property
    def train_weathers(self):
        return [1, 3, 6, 8]

    @property
    def test_weathers(self):
        return [4, 14]

    def calculate_time_out(self, path_distance):
        """
        Function to return the timeout ,in milliseconds,
        that is calculated based on distance to goal.
        This is the same timeout as used on the CoRL paper.

        * All timeouts can be extended as agent respects traffic lights
        """
        return ((path_distance / 1000.0) / 7.5) * 3600.0 + 20.0

    def _poses_town01(self):
        """
        Each matrix is a new task. We have all the four tasks
        """

        def _poses_navigation():
            return [[105, 29], [27, 130], [102, 87], [132, 27], [24, 44],
                    [96, 26], [34, 67], [28, 1], [140, 134], [105, 9],
                    [148, 129], [65, 18], [21, 16], [147, 97], [42, 51],
                    [30, 41], [18, 107], [69, 45], [102, 95], [18, 145],
                    [111, 64], [79, 45], [84, 69], [73, 31], [37, 81]]

        return [_poses_navigation()]

    def _poses_town02(self):

        def _poses_navigation():
            return [[19, 66], [79, 14], [19, 57], [23, 1],
                    [53, 76], [42, 13], [31, 71], [33, 5],
                    [54, 30], [10, 61], [66, 3], [27, 12],
                    [79, 19], [2, 29], [16, 14], [5, 57],
                    [70, 73], [46, 67], [57, 50], [61, 49], [21, 12],
                    [51, 81], [77, 68], [56, 65], [43, 54]]

        return [_poses_navigation()]


    def build_experiments(self):
        """
        Creates the whole set of experiment objects,
        The experiments created depend on the selected Town.
        """

        # We set the camera
        # This single RGB camera is used on every experiment

        camera_pos = (1.5, 0.0, 1.4)
        camera_rot = (-1.0, 0.0, 0.0)
        size = (384, 160)
        camera = Camera('CameraRGB')
        camera.set(FOV=100)
        camera.set_image_size(*size)
        camera.set_position(*camera_pos)
        camera.set_rotation(*camera_rot)

        DEBUG = 1
        if DEBUG:
            camera_debug = Camera('CameraDebug')
            camera_debug.set(FOV=100)
            camera_debug.set_image_size(640, 480)
            camera_debug.set_position(-5.5, 0.0, 3.0)
            camera_debug.set_rotation(-18.0, 0, 0)

        if self._city_name == 'Town01':
            poses_tasks = self._poses_town01()
            vehicles_tasks = [0,]
            pedestrians_tasks = [0,]

        else:
            poses_tasks = self._poses_town02()
            vehicles_tasks = [0,]
            pedestrians_tasks = [0,]


        experiments_vector = []

        for weather in self.weathers:

            for iteration in range(len(poses_tasks)):
                poses = poses_tasks[iteration]
                vehicles = vehicles_tasks[iteration]
                pedestrians = pedestrians_tasks[iteration]

                conditions = CarlaSettings()
                conditions.set(
                    SendNonPlayerAgentsInfo=True,
                    NumberOfVehicles=vehicles,
                    NumberOfPedestrians=pedestrians,
                    WeatherId=weather
                )
                # Add all the cameras that were set for this experiments
                conditions.set(DisableTwoWheeledVehicles=True) # we disabled two wheeled ve
                conditions.add_sensor(camera)

                if DEBUG:
                    conditions.add_sensor(camera_debug)

                experiment = Experiment()
                experiment.set(
                    Conditions=conditions,
                    Poses=poses,
                    Task=iteration,
                    Repetitions=1,
                )
                experiments_vector.append(experiment)

        return experiments_vector
