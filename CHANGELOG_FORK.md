# Changelog - Happy-Hare-Modified Fork

This file documents changes made in this fork compared to the original Happy Hare project.

## [2026-01-19] - Initial Fork Release

### Added
- **StepperIdlerSelector** - New selector type for stepper motor based idler control
  - Added `StepperIdlerSelector` class in `extras/mmu/mmu_selector.py`
  - Integrated into `extras/mmu_machine.py` for selector type selection
  - Support for `[manual_stepper idler_stepper]` configuration

- **New G-code Commands**
  - `MMU_CALIBRATE_SELECTOR` - Automatically calculate and save selector positions
  - `MMU_CALIBRATE_IDLER` - Automatically calculate and save idler positions
  - `MMU_SOAKTEST_SELECTOR` - Test selector and idler movement with configurable loops

- **Configuration Parameters**
  - `selector_type: StepperIdlerSelector` option in `[mmu_machine]`
  - `idler_move_speed` - Speed for idler movement
  - `idler_homing_speed` - Speed for idler homing
  - `cad_idler_gate0_pos` - Position of idler for gate 0
  - `cad_idler_gate_width` - Distance between idler positions
  - `cad_idler_tolerance` - Safety margin for idler movement

- **Documentation**
  - `STEPPER_IDLER_SETUP.md` - Comprehensive setup and migration guide
  - `config/examples/mmu_stepper_idler_example.cfg` - Full example configuration
  - Updated `README.md` with fork modifications section

- **Variables Storage**
  - `mmu_idler_offsets` - Calibrated idler positions stored in `mmu_vars.cfg`
  - Compatible with existing `mmu_selector_offsets` variable

### Features
- Stepper motor control for idler (precision over servo)
- Homing support for both selector and idler
- Sensorless homing capability via TMC stallguard
- Linear position calibration (mm) instead of servo angles
- Full compatibility with existing Happy Hare features
- Easy migration from 3D-Druckerplausch-Klipper configs

### Compatibility
- ✅ Fully compatible with original Happy Hare
- ✅ Can switch between selector types via configuration
- ✅ No breaking changes to existing configurations
- ✅ All original Happy Hare features remain functional

### Use Cases
- Prusa MMU2S and clones
- Custom MMU builds with stepper-based idler
- Migration from servo to stepper idler
- Users of 3D-Druckerplausch-Klipper MMU2S configurations

---

## Original Happy Hare Upstream

For changes in the base Happy Hare project, see:
https://github.com/moggieuk/Happy-Hare/wiki/Change-Log

## Contributing

This fork is maintained for specific stepper idler use cases. For general Happy Hare improvements, please contribute to the upstream project: https://github.com/moggieuk/Happy-Hare

## Credits

- **Original Happy Hare:** moggieuk (https://github.com/moggieuk/Happy-Hare)
- **StepperIdlerSelector Implementation:** marek-hurt
- **Inspiration:** 3D-Druckerplausch-Klipper community and Prusa MMU2S design
