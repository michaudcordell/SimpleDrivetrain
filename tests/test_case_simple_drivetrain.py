import unittest
import numpy as np
from simple_drivetrain import SimpleDrivetrain
from motor import Motor


class TestCaseSimpleDrivetrain(unittest.TestCase):
    def __assertWithinRange(self, expected, observed, percent_range):
        if expected < 0:
            within_range = (observed >= (1.0 + percent_range) * expected) \
                           and (observed <= (1.0 - percent_range) * expected)
            self.assertTrue(within_range)
        elif expected > 0:
            within_range = (observed >= (1.0 - percent_range) * expected) \
                           and (observed <= (1.0 + percent_range) * expected)
            self.assertTrue(within_range)
        else:  # expected == 0
            within_range = (observed >= -percent_range) and (observed <= percent_range)
            self.assertTrue(within_range)

    def test_get_motor_vels_local_translation(self):

        norm_const = np.sqrt(2.0) / 2.0

        const_rot = (0.0, 0.0, 0.0)

        test_inputs = [[norm_const, norm_const, 0.0],
                       [0.0, 1.0, 0.0],
                       [0.0, 0.0, 1.0]]
        test_outputs = [[0.0, 1.0, 0.0, -1.0, 0.0, 0.0],
                        [norm_const, norm_const, -norm_const, -norm_const, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]

        pwm_std = (1100, 1500, 1900)

        fr = [[norm_const, norm_const, 0.0], [-norm_const, norm_const, 0.0], pwm_std]
        fl = [[-norm_const, norm_const, 0.0], [norm_const, norm_const, 0.0], pwm_std]
        bl = [[-norm_const, -norm_const, 0.0], [norm_const, -norm_const, 0.0], pwm_std]
        br = [[norm_const, -norm_const, 0.0], [-norm_const, -norm_const, 0.0], pwm_std]
        fu = [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], pwm_std]
        bu = [[0.0, -1.0, 0.0], [0.0, 0.0, 1.0], pwm_std]

        testbot = SimpleDrivetrain()
        testbot.add_new_motor('fr', fr[0], fr[1], False, fr[2])
        testbot.add_new_motor('fl', fl[0], fl[1], False, fl[2])
        testbot.add_new_motor('bl', bl[0], bl[1], False, bl[2])
        testbot.add_new_motor('br', br[0], br[1], False, br[2])
        testbot.add_new_motor('fu', fu[0], fu[1], False, fu[2])
        testbot.add_new_motor('bu', bu[0], bu[1], False, bu[2])

        for i in range(0, len(test_inputs)):
            testbot.orientation = (0.0, 0.0, np.pi / 2.0)
            observed = testbot.get_motor_vels(test_inputs[i], const_rot)
            testbot.orientation = (0.0, 0.0, 3.0 * np.pi / 2.0)
            observed2 = testbot.get_motor_vels(test_inputs[i], const_rot, True)
            expected = test_outputs[i]

            for j in range(0, len(expected)):
                self.assertAlmostEqual(observed[j], expected[j])
                self.assertAlmostEqual(observed2[j], expected[j])

    def test_get_motor_vels_local_rotation(self):
        norm_const = np.sqrt(2.0) / 2.0

        zero_vector = [0.0, 0.0, 0.0]
        rot_yaw_ccw = [0.0, 0.0, 1.0]
        rot_yaw_cw = [0.0, 0.0, -1.0]
        rot_pitch_ccw = [1.0, 0.0, 0.0]
        rot_pitch_cw = [-1.0, 0.0, 0.0]

        test_inputs = ([zero_vector, rot_yaw_ccw],
                       [zero_vector, rot_yaw_cw])
        test_outputs = ([1.0, -1.0, 1.0, -1.0, 0.0, 0.0],
                        [-1.0, 1.0, -1.0, 1.0, 0.0, 0.0])

        pwm_std = (1100, 1500, 1900)

        fr = [[norm_const, norm_const, 0.0], [-norm_const, norm_const, 0.0], pwm_std]
        fl = [[-norm_const, norm_const, 0.0], [norm_const, norm_const, 0.0], pwm_std]
        bl = [[-norm_const, -norm_const, 0.0], [norm_const, -norm_const, 0.0], pwm_std]
        br = [[norm_const, -norm_const, 0.0], [-norm_const, -norm_const, 0.0], pwm_std]
        fu = [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], pwm_std]
        bu = [[0.0, -1.0, 0.0], [0.0, 0.0, 1.0], pwm_std]

        testbot = SimpleDrivetrain()
        testbot.add_new_motor('fr', fr[0], fr[1], False, fr[2])
        testbot.add_new_motor('fl', fl[0], fl[1], False, fl[2])
        testbot.add_new_motor('bl', bl[0], bl[1], False, bl[2])
        testbot.add_new_motor('br', br[0], br[1], False, br[2])
        testbot.add_new_motor('fu', fu[0], fu[1], False, fu[2])
        testbot.add_new_motor('bu', bu[0], bu[1], False, bu[2])

        for i in range(0, len(test_inputs)):
            testbot.orientation = (0.0, 0.0, np.pi / 2.0)
            observed = testbot.get_motor_vels(test_inputs[i][0], test_inputs[i][1])
            testbot.orientation = (0.0, 0.0, 3.0 * np.pi / 2.0)
            observed2 = testbot.get_motor_vels(test_inputs[i][0], test_inputs[i][1], True)
            expected = test_outputs[i]

            for j in range(0, len(expected)):
                self.__assertWithinRange(observed[j], expected[j], 0.02)
                self.__assertWithinRange(observed2[j], expected[j], 0.02)

    def test_get_motor_vels_field(self):
        norm_const = np.sqrt(2.0) / 2.0

        const_rot = (0.0, 0.0, 0.0)

        north_orientation = (0.0, 0.0, np.pi / 2.0)
        south_orientation = (0.0, 0.0, 3 * np.pi / 2.0)

        test_inputs = [[norm_const, norm_const, 0.0],
                       [0.0, 1.0, 0.0],
                       [0.0, 0.0, 1.0]]

        test_outputs_north = [[0.0, 1.0, 0.0, -1.0, 0.0, 0.0],
                        [norm_const, norm_const, -norm_const, -norm_const, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]

        test_outputs_south = [[0.0, -1.0, 0.0, 1.0, 0.0, 0.0],
                              [-norm_const, -norm_const, norm_const, norm_const, 0.0, 0.0],
                              [0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]

        pwm_std = (1100, 1500, 1900)

        fr = [[norm_const, norm_const, 0.0], [-norm_const, norm_const, 0.0], pwm_std]
        fl = [[-norm_const, norm_const, 0.0], [norm_const, norm_const, 0.0], pwm_std]
        bl = [[-norm_const, -norm_const, 0.0], [norm_const, -norm_const, 0.0], pwm_std]
        br = [[norm_const, -norm_const, 0.0], [-norm_const, -norm_const, 0.0], pwm_std]
        fu = [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], pwm_std]
        bu = [[0.0, -1.0, 0.0], [0.0, 0.0, 1.0], pwm_std]

        testbot = SimpleDrivetrain()
        testbot.add_new_motor('fr', fr[0], fr[1], False, fr[2])
        testbot.add_new_motor('fl', fl[0], fl[1], False, fl[2])
        testbot.add_new_motor('bl', bl[0], bl[1], False, bl[2])
        testbot.add_new_motor('br', br[0], br[1], False, br[2])
        testbot.add_new_motor('fu', fu[0], fu[1], False, fu[2])
        testbot.add_new_motor('bu', bu[0], bu[1], False, bu[2])

        testbot.orientation = north_orientation
        for i in range(0, len(test_inputs)):
            observed = testbot.get_motor_vels(test_inputs[i], const_rot)
            expected = test_outputs_north[i]

            for j in range(0, len(expected)):
                self.assertAlmostEqual(observed[j], expected[j])

        testbot.orientation = south_orientation
        for i in range(0, len(test_inputs)):
            observed = testbot.get_motor_vels(test_inputs[i], const_rot)
            expected = test_outputs_south[i]

            for j in range(0, len(expected)):
                self.assertAlmostEqual(observed[j], expected[j])

    def test_get_motor_vels_scaled(self):
        norm_const = np.sqrt(2.0) / 2.0
        const_rot = [0.0, 0.0, 0.0]
        pwm_bounds = [1100, 1500, 1900]

        test_inputs = [[(norm_const, -norm_const, 0.0), const_rot],
                       [(0.0, 0.0, 0.0), const_rot],
                       [(-norm_const, norm_const, 0.0), const_rot]]

        test_outputs = [[pwm_bounds[0]],
                        [pwm_bounds[1]],
                        [pwm_bounds[2]]]

        fr = [[norm_const, norm_const, 0.0], [-norm_const, norm_const, 0.0], pwm_bounds]

        bot = SimpleDrivetrain()
        bot.add_new_motor('fr', fr[0], fr[1], False, fr[2])

        for i in range(0, len(test_inputs)):
            observed = bot.get_motor_vels_scaled(test_inputs[i][0], test_inputs[i][1])
            expected = test_outputs[i]

            for j in range(0, len(expected)):
                self.assertEqual(expected[j], observed[j])

    def test_load_drivetrain_from_file(self):
        testbot = SimpleDrivetrain()
        filepath = 'drivetrain_test.xml'
        testbot.load_drivetrain_from_file(filepath)

        observed_motors = testbot.motors

        pwm_bounds_std = (1100, 1500, 1900)
        norm_const = np.sqrt(2) / 2
        expected_motors = [Motor('front_right', (1, 1, 0), (-norm_const, norm_const, 0), True, pwm_bounds_std),
                           Motor('front_left', (-1, 1, 0), (norm_const, norm_const, 0), False, pwm_bounds_std),
                           Motor('back_left', (-1, -1, 0), (norm_const, -norm_const, 0), False, pwm_bounds_std),
                           Motor('back_right', (1, -1, 0), (-norm_const, -norm_const, 0), False, pwm_bounds_std),
                           Motor('front_ascent', (0, 0.5, 0), (0, 0, 1), False, pwm_bounds_std),
                           Motor('back_ascent', (0, -0.5, 0), (0, 0, 1), False, pwm_bounds_std)]

        expected_orientation = (0, 0, 0)
        observed_orientation = testbot.orientation

        for i in range(0, len(expected_orientation)):
            self.assertAlmostEqual(expected_orientation[i], observed_orientation[i])

        for i in range(0, len(expected_motors)):
            observed_motor = observed_motors[i]
            expected_motor = expected_motors[i]

            observed_name = observed_motor.name
            expected_name = expected_motor.name

            observed_inverted = observed_motor.inverted
            expected_inverted = expected_motor.inverted

            observed_position = observed_motor.position
            expected_position = expected_motor.position

            observed_direction = observed_motor.direction
            expected_direction = expected_motor.direction

            observed_pwm_bounds = observed_motor.pwm_bounds
            expected_pwm_bounds = expected_motor.pwm_bounds

            self.assertEqual(expected_name, observed_name)
            self.assertEqual(expected_inverted, observed_inverted)
            for j in range(0, len(expected_position)):
                self.__assertWithinRange(expected_position[j], observed_position[j], 0.01)
            for j in range(0, len(expected_direction)):
                self.__assertWithinRange(expected_direction[j], observed_direction[j], 0.01)
            for j in range(0, len(expected_pwm_bounds)):
                self.assertEqual(expected_pwm_bounds[j], observed_pwm_bounds[j], 0.01)
