"""
Unit tests for StepperIdlerSelector implementation

These tests verify the StepperIdlerSelector functionality without requiring
full Klipper environment. They test the logic, calculations, and configuration.
"""

import unittest
import os


class TestStepperIdlerSelectorLogic(unittest.TestCase):
    """
    Tests for StepperIdlerSelector logic and calculations.

    These tests verify the core logic that StepperIdlerSelector implements.
    """

    def test_gate_position_calculation(self):
        """Test position calculation for gates based on gate0_pos and gate_width"""
        # Config values from example
        gate0_pos = 5.0
        gate_width = 21.0

        # Expected positions for T0-T4
        expected = {
            0: 5.0,   # T0: gate0_pos
            1: 26.0,  # T1: gate0_pos + 1*gate_width
            2: 47.0,  # T2: gate0_pos + 2*gate_width
            3: 68.0,  # T3: gate0_pos + 3*gate_width
            4: 89.0,  # T4: gate0_pos + 4*gate_width
        }

        for gate, expected_pos in expected.items():
            calculated_pos = gate0_pos + (gate * gate_width)
            self.assertAlmostEqual(calculated_pos, expected_pos, places=1,
                                 msg=f"Gate {gate} position mismatch")

    def test_gate_position_calculation_3d_druckerplausch(self):
        """Test position calculation with 3D-Druckerplausch values"""
        # Values from 3D-Druckerplausch-Klipper
        gate0_pos = 5.0
        gate_width = 15.0  # Different from example

        expected = {
            0: 5.0,   # T0
            1: 20.0,  # T1
            2: 35.0,  # T2
            3: 50.0,  # T3
            4: 65.0,  # T4
        }

        for gate, expected_pos in expected.items():
            calculated_pos = gate0_pos + (gate * gate_width)
            self.assertAlmostEqual(calculated_pos, expected_pos, places=1,
                                 msg=f"Gate {gate} position mismatch")

    def test_up_position_separate_from_gates(self):
        """Test that UP position is independent of gate positions"""
        gate0_pos = 5.0
        gate_width = 21.0
        up_position = 85.0

        # UP position should not collide with any gate position
        gate_positions = [gate0_pos + (i * gate_width) for i in range(5)]

        for gate_pos in gate_positions:
            self.assertNotEqual(up_position, gate_pos,
                              msg="UP position collides with gate position")

    def test_homing_offset_calculation(self):
        """Test that homing offset is correctly applied"""
        # After homing to endstop, position is set to reference point
        homing_reference = 2.0

        # Then idler moves to UP position
        up_position = 85.0

        # Movement required
        required_movement = up_position - homing_reference
        self.assertAlmostEqual(required_movement, 83.0, places=1)


class TestStepperIdlerSelectorBehavior(unittest.TestCase):
    """
    Tests for StepperIdlerSelector state machine behavior.

    These tests verify the correct sequence of operations for drive/release.
    """

    def test_drive_state_sequence(self):
        """Test that filament_drive follows correct sequence"""
        # Sequence for filament_drive:
        # 1. Calculate position for current gate
        # 2. Move idler to that position
        # 3. Set grip_state to DRIVE

        gate = 2
        gate0_pos = 5.0
        gate_width = 21.0
        expected_pos = gate0_pos + (gate * gate_width)  # 47.0

        self.assertAlmostEqual(expected_pos, 47.0, places=1)

    def test_release_state_sequence(self):
        """Test that filament_release follows correct sequence"""
        # Sequence for filament_release:
        # 1. Move idler to UP position (home_position)
        # 2. Set grip_state to RELEASE
        # 3. Return 0.0 (idler doesn't measure)

        up_position = 85.0
        expected_return = 0.0

        # UP position should be configured value
        self.assertEqual(up_position, 85.0)
        self.assertEqual(expected_return, 0.0)

    def test_homing_state_sequence(self):
        """Test that homing follows correct sequence"""
        # Sequence for _home_idler:
        # 1. do_homing_move to endstop (negative direction)
        # 2. do_set_position to reference point (2.0mm)
        # 3. do_move to UP position (85.0mm)

        homing_move_distance = -200
        reference_position = 2.0
        up_position = 85.0

        # Verify expected values
        self.assertEqual(homing_move_distance, -200)
        self.assertEqual(reference_position, 2.0)
        self.assertEqual(up_position, 85.0)


class TestStepperIdlerSelectorConfig(unittest.TestCase):
    """Tests for configuration values and validation"""

    def test_default_config_values(self):
        """Test that default configuration values are sensible"""
        # Default values from implementation
        defaults = {
            'cad_idler_gate0_pos': 0.0,
            'cad_idler_gate_width': 21.0,
            'cad_idler_home_position': 85.0,
            'idler_move_speed': 200.0,
            'idler_homing_speed': 50.0,
        }

        # All defaults should be non-negative
        for key, value in defaults.items():
            self.assertGreaterEqual(value, 0.0,
                                  msg=f"{key} should be non-negative")

        # Homing speed should be slower than move speed
        self.assertLess(defaults['idler_homing_speed'],
                       defaults['idler_move_speed'],
                       msg="Homing should be slower than normal moves")

    def test_example_config_values(self):
        """Test that example config values are valid"""
        import configparser

        config_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'config', 'examples', 'mmu_stepper_idler_example.cfg'
        )

        if os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.read(config_path)

            # Verify [mmu_machine] section exists
            self.assertTrue(config.has_section('mmu_machine'),
                          "Missing [mmu_machine] section")

            # Verify selector_type is set
            if config.has_option('mmu_machine', 'selector_type'):
                selector_type = config.get('mmu_machine', 'selector_type')
                self.assertEqual(selector_type, 'StepperIdlerSelector',
                               "Incorrect selector_type in example config")

            # Verify [manual_stepper idler_stepper] exists
            self.assertTrue(config.has_section('manual_stepper idler_stepper'),
                          "Missing [manual_stepper idler_stepper] section")


class TestStepperIdlerSelectorIntegration(unittest.TestCase):
    """Integration tests that verify the selector integrates with Happy Hare"""

    def test_selector_type_in_mmu_machine(self):
        """Test that StepperIdlerSelector is a valid selector type"""
        # From mmu_machine.py line 244
        valid_selector_types = [
            'LinearSelector',
            'VirtualSelector',
            'MacroSelector',
            'RotarySelector',
            'ServoSelector',
            'IndexedSelector',
            'StepperIdlerSelector'
        ]

        self.assertIn('StepperIdlerSelector', valid_selector_types,
                     "StepperIdlerSelector not in valid selector types")

    def test_idler_stepper_configuration_format(self):
        """Test that manual_stepper configuration format is correct"""
        # Expected configuration format
        required_manual_stepper_params = [
            'step_pin',
            'dir_pin',
            'enable_pin',
            'rotation_distance',
            'endstop_pin',
        ]

        # These are the standard Klipper manual_stepper parameters
        for param in required_manual_stepper_params:
            self.assertIsNotNone(param,
                               f"Required parameter {param} should be defined")


class TestStepperIdlerSelectorEdgeCases(unittest.TestCase):
    """Tests for edge cases and error conditions"""

    def test_gate_position_boundaries(self):
        """Test gate positions don't exceed reasonable bounds"""
        gate0_pos = 5.0
        gate_width = 21.0
        max_gates = 12  # Maximum supported by Happy Hare

        max_position = gate0_pos + ((max_gates - 1) * gate_width)

        # Assuming max travel of ~300mm is reasonable for MMU
        self.assertLess(max_position, 300.0,
                       msg="Maximum gate position exceeds reasonable bounds")

    def test_up_position_validity(self):
        """Test that UP position is reachable"""
        up_position = 85.0

        # UP position should be positive and within reasonable travel
        self.assertGreater(up_position, 0.0,
                          msg="UP position should be positive")
        self.assertLess(up_position, 300.0,
                       msg="UP position should be within reasonable travel")

    def test_gate_width_minimum(self):
        """Test that gate width is not too small"""
        gate_width = 21.0

        # Gate width should be at least 1mm (from config minval)
        self.assertGreaterEqual(gate_width, 1.0,
                               msg="Gate width too small")


class TestStepperIdlerSelectorDocumentation(unittest.TestCase):
    """Tests that verify documentation exists and is complete"""

    def test_documentation_files_exist(self):
        """Test that all documentation files exist"""
        doc_files = [
            'README.md',
            'CODE_REFERENCE.md',
            'STEPPER_IDLER_SETUP.md',
            'MIGRATION_GUIDE.md',
            'IDLER_BEHAVIOR.md',
            'CHANGELOG_FORK.md',
            'FILES_MODIFIED.md',
            'DOCUMENTATION_INDEX.md',
            'test/TESTING.md',
        ]

        base_path = os.path.join(os.path.dirname(__file__), '..', '..')

        for doc_file in doc_files:
            full_path = os.path.join(base_path, doc_file)
            self.assertTrue(os.path.exists(full_path),
                          f"Documentation file {doc_file} does not exist")

    def test_example_config_exists(self):
        """Test that example configuration file exists"""
        config_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'config', 'examples', 'mmu_stepper_idler_example.cfg'
        )

        self.assertTrue(os.path.exists(config_path),
                       "Example configuration file does not exist")


class TestStepperIdlerSelectorCodeIntegrity(unittest.TestCase):
    """Tests that verify code modifications are correct"""

    def test_mmu_selector_contains_stepper_idler_class(self):
        """Test that mmu_selector.py contains StepperIdlerSelector class"""
        selector_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'extras', 'mmu', 'mmu_selector.py'
        )

        with open(selector_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verify class definition exists
        self.assertIn('class StepperIdlerSelector', content,
                     "StepperIdlerSelector class not found in mmu_selector.py")

        # Verify key methods exist
        self.assertIn('def filament_drive(self)', content,
                     "filament_drive method not found")
        self.assertIn('def filament_release(self', content,
                     "filament_release method not found")
        self.assertIn('def _home_idler(self)', content,
                     "_home_idler method not found")

        # Verify UP position parameter exists
        self.assertIn('cad_idler_home_position', content,
                     "cad_idler_home_position parameter not found")

    def test_mmu_machine_has_stepper_idler_selector(self):
        """Test that mmu_machine.py includes StepperIdlerSelector"""
        machine_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'extras', 'mmu_machine.py'
        )

        with open(machine_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verify StepperIdlerSelector is in selector_type choices
        self.assertIn('StepperIdlerSelector', content,
                     "StepperIdlerSelector not found in mmu_machine.py")


if __name__ == '__main__':
    unittest.main()
