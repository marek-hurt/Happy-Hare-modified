# Modified Files - Happy-Hare-Modified Fork

This document lists all files that were modified or added in this fork compared to the original Happy Hare project.

## Modified Files

### Core Implementation

1. **`extras/mmu/mmu_selector.py`**
   - **Lines added:** 2119-2423 (305 lines)
   - **Changes:** Added new `StepperIdlerSelector` class
   - **Purpose:** Implements stepper motor based idler control
   - **Key methods:**
     - `__init__()` - Configuration and setup
     - `home()` - Homes both selector and idler steppers
     - `select_gate()` - Moves selector and idler to gate position
     - `filament_drive()` / `filament_release()` - Control idler grip
     - `_home_selector()` / `_home_idler()` - Homing routines
     - `_move_selector_to_gate()` / `_move_idler_to_gate()` - Movement commands
     - `cmd_MMU_CALIBRATE_SELECTOR()` - Calibration command
     - `cmd_MMU_CALIBRATE_IDLER()` - Idler calibration command
     - `cmd_MMU_SOAKTEST_SELECTOR()` - Testing command

2. **`extras/mmu_machine.py`**
   - **Line 244:** Added `'StepperIdlerSelector'` to selector type choices
   - **Line 981:** Added `'StepperIdlerSelector'` to LinearSelector/RotarySelector rail setup
   - **Line 1046:** Added `'StepperIdlerSelector'` to movement checking
   - **Purpose:** Integrates StepperIdlerSelector into MMU toolhead system

## New Files

### Documentation

1. **`README.md`**
   - **Section added:** "🔧 Modifications in This Fork"
   - **Content:** Feature description, quick start, comparison table, documentation links
   - **Purpose:** Inform users about fork modifications

2. **`STEPPER_IDLER_SETUP.md`**
   - **Size:** ~400 lines
   - **Content:** Complete setup guide for StepperIdlerSelector
   - **Sections:**
     - Overview and when to use
     - Architecture explanation
     - Installation and configuration
     - Calibration procedures
     - Migration from 3D-Druckerplausch-Klipper
     - G-code commands reference
     - Troubleshooting
     - Comparison tables

3. **`MIGRATION_GUIDE.md`**
   - **Size:** ~300 lines
   - **Content:** Step-by-step migration from 3D-Druckerplausch-Klipper
   - **Sections:**
     - Why migrate
     - Prerequisites
     - Value extraction from old config
     - CAD parameter calculation
     - Stepper configuration conversion
     - Pin mapping
     - Macro migration table
     - Troubleshooting

4. **`CHANGELOG_FORK.md`**
   - **Size:** ~80 lines
   - **Content:** Changelog specific to this fork
   - **Sections:**
     - Added features
     - New G-code commands
     - Configuration parameters
     - Compatibility notes

5. **`FILES_MODIFIED.md`** (this file)
   - **Content:** List of all modified and new files
   - **Purpose:** Track fork changes for maintenance

### Example Configuration

6. **`config/examples/mmu_stepper_idler_example.cfg`**
   - **Size:** ~200 lines
   - **Content:** Complete example configuration for StepperIdlerSelector
   - **Sections:**
     - MMU machine configuration
     - Selector stepper config (with TMC2209)
     - Idler stepper config (manual_stepper with TMC2209)
     - Gear stepper config
     - Position parameters (CAD values)
     - Calibration instructions
     - Sensor configuration examples
     - Pin mapping examples

## Files NOT Modified

The following original Happy Hare files remain unchanged:
- All files in `extras/mmu/` except `mmu_selector.py`
- All files in `config/` except new example
- All installation scripts
- All utility scripts
- All test files
- All component definitions

## Summary Statistics

- **Modified existing files:** 2
- **New files created:** 6
- **Total lines added:** ~1,600
- **Core implementation:** ~310 lines
- **Documentation:** ~1,000 lines
- **Example configs:** ~200 lines
- **Integration changes:** ~5 lines

## Maintenance Notes

When syncing with upstream Happy Hare:
1. Check for changes in `mmu_selector.py` base classes
2. Check for changes in `mmu_machine.py` selector handling
3. Verify selector type list remains compatible
4. Test StepperIdlerSelector after merge
5. Update documentation if Happy Hare adds new features

## Version Compatibility

This fork is based on Happy Hare as of:
- **Date:** January 2026
- **Upstream commit:** (check at time of fork)
- **Compatible versions:** Happy Hare v3.x and later

## Testing Checklist

Before releasing updates:
- [ ] Test homing (selector and idler)
- [ ] Test gate selection (all gates)
- [ ] Test calibration commands
- [ ] Test with different gate counts (3, 4, 5)
- [ ] Test with stallguard homing
- [ ] Test with physical endstops
- [ ] Verify positions saved to mmu_vars.cfg
- [ ] Run soak test successfully
- [ ] Test with actual filament loading
- [ ] Verify no conflicts with other selectors

## Git Diff Summary

To see exact changes from upstream:
```bash
cd Happy-Hare-modified
git remote add upstream https://github.com/moggieuk/Happy-Hare.git
git fetch upstream
git diff upstream/main extras/mmu/mmu_selector.py
git diff upstream/main extras/mmu_machine.py
```

---

**Last updated:** 2026-01-19
**Fork maintainer:** marek-hurt
