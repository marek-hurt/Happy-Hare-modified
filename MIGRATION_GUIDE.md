# Migration Guide - From 3D-Druckerplausch-Klipper to Happy-Hare-Modified

This guide helps you migrate from the 3D-Druckerplausch-Klipper MMU2S configuration to Happy-Hare with StepperIdlerSelector.

## Why Migrate?

Happy Hare offers:
- ✅ Better error handling and recovery
- ✅ Advanced features (Spoolman, LED effects, tip forming, etc.)
- ✅ Active development and community support
- ✅ Better sensor support
- ✅ Multi-MMU capability
- ✅ Extensive documentation and tools

## Prerequisites

Before you start, make sure you have:
1. Your current 3D-Druckerplausch-Klipper config backed up
2. The values from your `mmu2s_variables.cfg`:
   - `variable_idler` array (e.g., `[4.0, 25.0, 46.0, 67.0, 88.0]`)
   - `variable_colorselector` array (e.g., `[5.0, 26.0, 47.0, 68.0, 89.0]`)
3. Your MCU board pin definitions
4. Your stepper motor settings (rotation_distance, current, etc.)

## Step-by-Step Migration

### Step 1: Extract Your Current Values

From your `mmu2s_variables.cfg`, note these values:

```python
[gcode_macro _VAR_MMU2S]
variable_idler: [4.0, 25.0, 46.0, 67.0, 88.0]
variable_colorselector: [5.0, 26.0, 47.0, 68.0, 89.0]
variable_idler_home_position: 85
variable_selector_home_position: 1
```

### Step 2: Calculate CAD Parameters

From your arrays, calculate:

```python
# Idler parameters
idler_gate0_pos = idler[0]  # First value: 4.0
idler_gate_width = idler[1] - idler[0]  # Difference: 25.0 - 4.0 = 21.0

# Selector parameters
selector_gate0_pos = colorselector[0]  # First value: 5.0
selector_gate_width = colorselector[1] - colorselector[0]  # Difference: 26.0 - 5.0 = 21.0
```

### Step 3: Install Happy-Hare-Modified

```bash
cd ~
# Backup your current config
cp -r ~/printer_data/config ~/printer_data/config_backup_$(date +%Y%m%d)

# Clone Happy-Hare-Modified
git clone https://github.com/marek-hurt/Happy-Hare-modified.git Happy-Hare

# Run installer
cd Happy-Hare
./install.sh
```

### Step 4: Configure MMU Machine

Create or edit `mmu.cfg`:

```ini
[mmu_machine]
# Number of gates (typically 5 for MMU2S)
num_gates: 5

# Use custom selector type
mmu_vendor: Other
mmu_version: 1.0
selector_type: StepperIdlerSelector

# MMU design parameters (for MMU2S-like designs)
variable_rotation_distances: 1
variable_bowden_lengths: 0
require_bowden_move: 1
filament_always_gripped: 0
has_bypass: 0
```

### Step 5: Convert Stepper Configurations

#### OLD (3D-Druckerplausch):
```ini
[manual_stepper selector_stepper]
step_pin: PC13
dir_pin: PF0
enable_pin: !PF1
# ...

[manual_stepper idler_stepper]
step_pin: PE2
dir_pin: PE3
enable_pin: !PD4
# ...

[manual_stepper gear_stepper]
step_pin: PE6
dir_pin: PA14
enable_pin: !PE0
# ...
```

#### NEW (Happy-Hare-Modified):

**Selector becomes part of MMU toolhead:**
```ini
[stepper_mmu_selector]
step_pin: mmu:MMU_SEL_STEP
dir_pin: !mmu:MMU_SEL_DIR
enable_pin: !mmu:MMU_SEL_ENABLE
rotation_distance: 8
gear_ratio: 1:1
microsteps: 16
full_steps_per_rotation: 200
endstop_pin: ^mmu:MMU_SEL_ENDSTOP
endstop_name: mmu_sel_home

[tmc2209 stepper_mmu_selector]
uart_pin: mmu:MMU_SEL_UART
run_current: 0.4
hold_current: 0.2
# ... copy your TMC settings
```

**Idler stays as manual_stepper:**
```ini
[manual_stepper idler_stepper]
step_pin: mmu:MMU_IDLER_STEP
dir_pin: mmu:MMU_IDLER_DIR
enable_pin: !mmu:MMU_IDLER_ENABLE
rotation_distance: 128  # Use your value
microsteps: 16
velocity: 100
accel: 80
endstop_pin: ^mmu:MMU_IDLER_ENDSTOP

[tmc2209 manual_stepper idler_stepper]
uart_pin: mmu:MMU_IDLER_UART
run_current: 0.4
hold_current: 0.2
# ... copy your TMC settings
```

**Gear becomes part of MMU toolhead:**
```ini
[stepper_mmu_gear]
step_pin: mmu:MMU_GEAR_STEP
dir_pin: !mmu:MMU_GEAR_DIR
enable_pin: !mmu:MMU_GEAR_ENABLE
rotation_distance: 22.7316868  # Or your value
gear_ratio: 80:20  # Adjust to your setup
microsteps: 16
full_steps_per_rotation: 200

[tmc2209 stepper_mmu_gear]
uart_pin: mmu:MMU_GEAR_UART
run_current: 0.5
hold_current: 0.1
# ... copy your TMC settings
```

### Step 6: Set Position Parameters

In `mmu_parameters.cfg` or your config file:

```ini
# Speeds (adjust to your preference)
selector_move_speed: 200
selector_homing_speed: 100
idler_move_speed: 100
idler_homing_speed: 80

# CAD parameters from Step 2
cad_gate0_pos: 5.0              # From colorselector[0]
cad_gate_width: 21.0            # Calculated
cad_last_gate_offset: 2.0
cad_selector_tolerance: 10.0

cad_idler_gate0_pos: 4.0        # From idler[0]
cad_idler_gate_width: 21.0      # Calculated
cad_idler_tolerance: 10.0
```

### Step 7: Setup Pin Aliases

Create board_pins for your MCU (example for BTT Octopus):

```ini
[mcu mmu]
serial: /dev/serial/by-id/YOUR_MMU_MCU_ID

[board_pins mmu_pins]
mcu: mmu
aliases:
    # Selector stepper
    MMU_SEL_STEP=PC13,
    MMU_SEL_DIR=PF0,
    MMU_SEL_ENABLE=PF1,
    MMU_SEL_UART=PE4,
    MMU_SEL_ENDSTOP=PG12,

    # Idler stepper
    MMU_IDLER_STEP=PE2,
    MMU_IDLER_DIR=PE3,
    MMU_IDLER_ENABLE=PD4,
    MMU_IDLER_UART=PE1,
    MMU_IDLER_ENDSTOP=PG14,

    # Gear stepper
    MMU_GEAR_STEP=PE6,
    MMU_GEAR_DIR=PA14,
    MMU_GEAR_ENABLE=PE0,
    MMU_GEAR_UART=PD3,
```

### Step 8: Calibrate

Instead of manually entering values into `mmu_vars.cfg`, let Happy-Hare calculate them:

```gcode
MMU_CALIBRATE_SELECTOR
MMU_CALIBRATE_IDLER
```

This will create entries in `mmu_vars.cfg`:
```ini
mmu_selector_offsets = [5.0, 26.0, 47.0, 68.0, 89.0]
mmu_idler_offsets = [4.0, 25.0, 46.0, 67.0, 88.0]
```

**Verify these match your original values!** If not, adjust the CAD parameters and re-run calibration.

### Step 9: Test

```gcode
# Home the MMU
MMU_HOME

# Test individual gates
MMU_SELECT_TOOL TOOL=0
MMU_SELECT_TOOL TOOL=1
# etc.

# Run soak test
MMU_SOAKTEST_SELECTOR LOOP=10 HOME=1
```

## Configuration Comparison Table

| 3D-Druckerplausch | Happy-Hare-Modified | Notes |
|-------------------|---------------------|-------|
| `[manual_stepper selector_stepper]` | `[stepper_mmu_selector]` | Now part of MMU toolhead |
| `[manual_stepper idler_stepper]` | `[manual_stepper idler_stepper]` | Stays the same |
| `[manual_stepper gear_stepper]` | `[stepper_mmu_gear]` | Now part of MMU toolhead |
| `variable_idler` array | `mmu_idler_offsets` in vars | Auto-generated from CAD params |
| `variable_colorselector` array | `mmu_selector_offsets` in vars | Auto-generated from CAD params |
| `CHANGE_TOOL VALUE=X` | `MMU_SELECT_TOOL TOOL=X` | Different command name |
| `HOME_MMU` | `MMU_HOME` | Different command name |

## Macro Migration

Most 3D-Druckerplausch macros need to be replaced with Happy-Hare equivalents:

| Old Macro | Happy-Hare Equivalent |
|-----------|----------------------|
| `CHANGE_TOOL VALUE=X` | `T0`, `T1`, etc. or `MMU_CHANGE_TOOL TOOL=X` |
| `HOME_MMU` | `MMU_HOME` |
| `FORCE_MOVE_SELECTOR` | Built-in to selector |
| `FORCE_MOVE_IDLER` | Built-in to selector |
| `SELECT_TOOL VALUE=X` | `MMU_SELECT_TOOL TOOL=X` |
| Custom load/unload macros | `MMU_LOAD`, `MMU_UNLOAD` |

## Troubleshooting

### "StepperIdlerSelector requires [manual_stepper idler_stepper]"
- Make sure you have `[manual_stepper idler_stepper]` section
- Check section name is exactly `idler_stepper`

### Positions don't match original
- Verify CAD parameters are calculated correctly
- Manually edit `mmu_vars.cfg` if needed
- Check `rotation_distance` on steppers

### Direction is reversed
- Add or remove `!` from `dir_pin` in stepper config
- Test with `MMU_SELECT_TOOL TOOL=0` then `TOOL=1`

### Motors don't move
- Check enable pins (should be `!` for active low)
- Verify MCU pin aliases match your board
- Test TMC UART communication

## Final Notes

- Keep your old config backed up until you're sure everything works
- Start with a single filament change test before a full print
- Read the [full setup guide](STEPPER_IDLER_SETUP.md) for more details
- Join Happy Hare Discord for support: https://discord.gg/aABQUjkZPk

## Need Help?

1. Check your `mmu.log` file for errors
2. Compare your config with the [example](config/examples/mmu_stepper_idler_example.cfg)
3. Review the [setup guide](STEPPER_IDLER_SETUP.md)
4. Ask in Happy Hare Discord community

Good luck with your migration! 🐰
