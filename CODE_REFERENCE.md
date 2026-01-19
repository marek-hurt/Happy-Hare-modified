# Code Reference - StepperIdlerSelector Implementation

This document provides code snippets and references to the implementation of StepperIdlerSelector in this fork.

## Table of Contents
- [Modified Files](#modified-files)
- [New Python Class](#new-python-class)
- [Integration Points](#integration-points)
- [Key Methods](#key-methods)
- [Configuration Examples](#configuration-examples)
- [G-code Commands](#g-code-commands)

---

## Modified Files

### 1. `extras/mmu/mmu_selector.py`

**Location:** Lines 2119-2423
**File:** [extras/mmu/mmu_selector.py](extras/mmu/mmu_selector.py#L2119-L2423)

#### Class Definition

```python
class StepperIdlerSelector(BaseSelector, object):
    """
    Implements selector for MMU's with stepper motor idler (like Prusa MMU2S)
    Uses a stepper motor to move idler to specific positions for each gate
    instead of a servo. Requires manual_stepper configuration for idler.
    """

    # mmu_vars.cfg variables
    VARS_MMU_IDLER_OFFSETS = "mmu_idler_offsets"
    VARS_MMU_SELECTOR_OFFSETS = "mmu_selector_offsets"
    VARS_MMU_SELECTOR_BYPASS = "mmu_selector_bypass"
```

#### Configuration Parameters

```python
def __init__(self, mmu):
    super(StepperIdlerSelector, self).__init__(mmu)

    # Movement speeds
    self.selector_move_speed = mmu.config.getfloat('selector_move_speed', 200, minval=1.)
    self.selector_homing_speed = mmu.config.getfloat('selector_homing_speed', 100, minval=1.)
    self.idler_move_speed = mmu.config.getfloat('idler_move_speed', 100, minval=1.)
    self.idler_homing_speed = mmu.config.getfloat('idler_homing_speed', 80, minval=1.)

    # CAD parameters for selector
    self.cad_gate0_pos = mmu.config.getfloat('cad_gate0_pos', 5.0, minval=0.)
    self.cad_gate_width = mmu.config.getfloat('cad_gate_width', 21.0, above=0.)
    # ...

    # CAD parameters for idler
    self.cad_idler_gate0_pos = mmu.config.getfloat('cad_idler_gate0_pos', 5.0, minval=0.)
    self.cad_idler_gate_width = mmu.config.getfloat('cad_idler_gate_width', 21.0, above=0.)
```

---

### 2. `extras/mmu_machine.py`

**Changes:** 3 modifications for integration

#### Change 1: Selector Type Registration (Line 244)

**File:** [extras/mmu_machine.py](extras/mmu_machine.py#L244)

```python
# Before:
self.selector_type = config.getchoice('selector_type',
    {o: o for o in ['LinearSelector', 'VirtualSelector', 'MacroSelector',
                    'RotarySelector', 'ServoSelector', 'IndexedSelector']},
    selector_type)

# After:
self.selector_type = config.getchoice('selector_type',
    {o: o for o in ['LinearSelector', 'VirtualSelector', 'MacroSelector',
                    'RotarySelector', 'ServoSelector', 'IndexedSelector',
                    'StepperIdlerSelector']},  # ← Added
    selector_type)
```

#### Change 2: Rail Setup (Line 981)

**File:** [extras/mmu_machine.py](extras/mmu_machine.py#L981)

```python
# Before:
if self.mmu_machine.selector_type in ['LinearSelector', 'RotarySelector']:
    self.rails.append(MmuLookupMultiRail(...))

# After:
if self.mmu_machine.selector_type in ['LinearSelector', 'RotarySelector',
                                       'StepperIdlerSelector']:  # ← Added
    self.rails.append(MmuLookupMultiRail(...))
```

#### Change 3: Movement Checking (Line 1046)

**File:** [extras/mmu_machine.py](extras/mmu_machine.py#L1046)

```python
# Before:
if self.mmu_machine.selector_type in ['LinearSelector', 'RotarySelector']:
    limits = self.limits
    # ...

# After:
if self.mmu_machine.selector_type in ['LinearSelector', 'RotarySelector',
                                       'StepperIdlerSelector']:  # ← Added
    limits = self.limits
    # ...
```

---

## New Python Class

### StepperIdlerSelector Class Structure

**Full implementation:** [extras/mmu/mmu_selector.py#L2130](extras/mmu/mmu_selector.py#L2130)

```
StepperIdlerSelector (BaseSelector)
├── __init__()                          # Configuration and setup
├── reinit()                            # Reset grip state
├── handle_connect()                    # Connect to steppers, load offsets
├── home()                              # Home both selector and idler
├── select_gate()                       # Move to gate position
├── restore_gate()                      # Restore gate position
├── filament_drive()                    # Engage idler
├── filament_release()                  # Release idler
├── get_filament_grip_state()          # Get current grip state
├── disable_motors()                    # Disable both motors
├── enable_motors()                     # Enable both motors
├── get_status()                        # Status for queries
│
├── Internal Methods:
│   ├── _home_selector()               # Home selector stepper
│   ├── _home_idler()                  # Home idler stepper
│   ├── _move_selector_to_gate()       # Move selector to position
│   ├── _move_idler_to_gate()          # Move idler to position
│   ├── _get_max_selector_movement()   # Calculate max movement
│   ├── _ensure_list_size()            # Ensure offset list size
│   └── set_position()                 # Set selector position
│
└── G-code Commands:
    ├── cmd_MMU_CALIBRATE_SELECTOR()   # Calibrate selector
    ├── cmd_MMU_CALIBRATE_IDLER()      # Calibrate idler
    └── cmd_MMU_SOAKTEST_SELECTOR()    # Test movements
```

---

## Key Methods

### 1. Homing Sequence

**File:** [extras/mmu/mmu_selector.py#L2224](extras/mmu/mmu_selector.py#L2224)

```python
def home(self, force_unload=None):
    """Home both selector and idler steppers"""
    if self.mmu.check_if_bypass(): return
    with self.mmu.wrap_action(self.mmu.ACTION_HOMING):
        self.mmu.log_info("Homing MMU...")
        if force_unload is not None:
            self.mmu.log_debug("(asked to %s)" %
                ("force unload" if force_unload else "not unload"))
        if force_unload is True:
            self.mmu.unload_sequence(check_state=True)
        elif force_unload is False and \
             self.mmu.filament_pos != self.mmu.FILAMENT_POS_UNLOADED:
            self.mmu.unload_sequence()

        # Home both steppers
        self._home_selector()
        self._home_idler()
```

### 2. Gate Selection

**File:** [extras/mmu/mmu_selector.py#L2237](extras/mmu/mmu_selector.py#L2237)

```python
def select_gate(self, gate):
    """Move selector and idler to gate position"""
    if gate != self.mmu.gate_selected:
        with self.mmu.wrap_action(self.mmu.ACTION_SELECTING):
            # Release filament first
            if self.grip_state == self.mmu.FILAMENT_DRIVE_STATE:
                self.filament_release()

            # Move idler to position
            self._move_idler_to_gate(gate)

            # Move selector to position
            self._move_selector_to_gate(gate)
```

### 3. Idler Movement

**File:** [extras/mmu/mmu_selector.py#L2335](extras/mmu/mmu_selector.py#L2335)

```python
def _move_idler_to_gate(self, gate):
    """Move idler stepper to gate position"""
    if gate >= 0 and gate < len(self.idler_offsets):
        offset = self.idler_offsets[gate]
        if offset >= 0:
            self.mmu.log_trace("Moving idler to gate %d at %.1fmm" %
                              (gate, offset))
            # Use manual_stepper movement
            self.idler_stepper.do_move(
                movepos=offset,
                speed=self.idler_move_speed,
                accel=self.idler_stepper.accel,
                sync=True
            )
        else:
            raise MmuError("Idler offset for gate %d not calibrated" % gate)
```

### 4. Calibration

**File:** [extras/mmu/mmu_selector.py#L2354](extras/mmu/mmu_selector.py#L2354)

```python
def cmd_MMU_CALIBRATE_SELECTOR(self, gcmd):
    """Calibrate selector positions based on CAD parameters"""
    self.mmu.log_to_file(gcmd.get_commandline())
    if self.mmu.check_if_disabled(): return

    gate = gcmd.get_int('GATE', 0, minval=0, maxval=self.mmu.num_gates - 1)
    save = gcmd.get_int('SAVE', 1, minval=0, maxval=1)

    try:
        self.mmu.calibrating = True
        # Calculate positions based on CAD values
        self.selector_offsets = [
            round(self.cad_gate0_pos + i * self.cad_gate_width, 1)
            for i in range(self.mmu.num_gates)
        ]

        if save:
            self.mmu.save_variable(self.VARS_MMU_SELECTOR_OFFSETS,
                                  self.selector_offsets, write=True)
            self.mmu.log_always("Selector offsets calculated and saved: %s" %
                               self.selector_offsets)

        if not any(x == -1 for x in self.selector_offsets):
            self.mmu.calibration_status |= self.mmu.CALIBRATED_SELECTOR
    except MmuError as ee:
        self.mmu.handle_mmu_error(str(ee))
    finally:
        self.mmu.calibrating = False
```

---

## Integration Points

### 1. Idler Stepper Lookup

**File:** [extras/mmu/mmu_selector.py#L2181](extras/mmu/mmu_selector.py#L2181)

```python
def handle_connect(self):
    """Connect to steppers and load calibration data"""
    self.mmu_toolhead = self.mmu.mmu_toolhead
    self.selector_rail = self.mmu_toolhead.get_kinematics().rails[0]
    self.selector_stepper = self.selector_rail.steppers[0]

    # Get idler stepper (manual_stepper)
    self.idler_stepper = None
    if 'manual_stepper idler_stepper' in self.mmu.printer.lookup_objects():
        self.idler_stepper = self.mmu.printer.lookup_object(
            'manual_stepper idler_stepper'
        )
    else:
        raise self.mmu.config.error(
            "StepperIdlerSelector requires [manual_stepper idler_stepper] configuration"
        )
```

### 2. Variable Storage

**File:** [extras/mmu/mmu_selector.py#L2188](extras/mmu/mmu_selector.py#L2188)

```python
# Load selector offsets
self.selector_offsets = self.mmu.save_variables.allVariables.get(
    self.VARS_MMU_SELECTOR_OFFSETS, None
)

# Load idler offsets
self.idler_offsets = self.mmu.save_variables.allVariables.get(
    self.VARS_MMU_IDLER_OFFSETS, None
)

# Load bypass offset
self.bypass_offset = self.mmu.save_variables.allVariables.get(
    self.VARS_MMU_SELECTOR_BYPASS, -1
)
```

---

## Configuration Examples

### Minimal Configuration

```ini
[mmu_machine]
selector_type: StepperIdlerSelector
num_gates: 5

[manual_stepper idler_stepper]
step_pin: mmu:MMU_IDLER_STEP
dir_pin: mmu:MMU_IDLER_DIR
enable_pin: !mmu:MMU_IDLER_ENABLE
rotation_distance: 128
endstop_pin: ^mmu:MMU_IDLER_ENDSTOP

# CAD parameters
cad_idler_gate0_pos: 5.0
cad_idler_gate_width: 21.0
```

### Full Configuration with TMC

```ini
[tmc2209 manual_stepper idler_stepper]
uart_pin: mmu:MMU_IDLER_UART
run_current: 0.4
hold_current: 0.2
interpolate: True
sense_resistor: 0.110
stealthchop_threshold: 0

[manual_stepper idler_stepper]
step_pin: mmu:MMU_IDLER_STEP
dir_pin: mmu:MMU_IDLER_DIR
enable_pin: !mmu:MMU_IDLER_ENABLE
rotation_distance: 128
microsteps: 16
velocity: 100
accel: 80
endstop_pin: ^mmu:MMU_IDLER_ENDSTOP
```

### With Sensorless Homing (Stallguard)

```ini
[tmc2209 manual_stepper idler_stepper]
uart_pin: mmu:MMU_IDLER_UART
diag_pin: mmu:MMU_IDLER_DIAG
run_current: 0.4
driver_SGTHRS: 130  # Stallguard threshold

[manual_stepper idler_stepper]
step_pin: mmu:MMU_IDLER_STEP
dir_pin: mmu:MMU_IDLER_DIR
enable_pin: !mmu:MMU_IDLER_ENABLE
rotation_distance: 128
endstop_pin: tmc2209_manual_stepper idler_stepper:virtual_endstop
homing_retract_dist: 0
```

---

## G-code Commands

### MMU_CALIBRATE_SELECTOR

**Implementation:** [extras/mmu/mmu_selector.py#L2354](extras/mmu/mmu_selector.py#L2354)

```gcode
MMU_CALIBRATE_SELECTOR [GATE=<0-4>] [SAVE=<0|1>]
```

**Example:**
```gcode
MMU_CALIBRATE_SELECTOR SAVE=1
```

**Output to mmu_vars.cfg:**
```ini
mmu_selector_offsets = [5.0, 26.0, 47.0, 68.0, 89.0]
```

### MMU_CALIBRATE_IDLER

**Implementation:** [extras/mmu/mmu_selector.py#L2380](extras/mmu/mmu_selector.py#L2380)

```gcode
MMU_CALIBRATE_IDLER [GATE=<0-4>] [SAVE=<0|1>]
```

**Example:**
```gcode
MMU_CALIBRATE_IDLER SAVE=1
```

**Output to mmu_vars.cfg:**
```ini
mmu_idler_offsets = [4.0, 25.0, 46.0, 67.0, 88.0]
```

### MMU_SOAKTEST_SELECTOR

**Implementation:** [extras/mmu/mmu_selector.py#L2403](extras/mmu/mmu_selector.py#L2403)

```gcode
MMU_SOAKTEST_SELECTOR [LOOP=<count>] [HOME=<0|1>]
```

**Example:**
```gcode
MMU_SOAKTEST_SELECTOR LOOP=50 HOME=1
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Happy Hare Core                          │
│                   (extras/mmu/mmu.py)                       │
└──────────────┬──────────────────────────┬───────────────────┘
               │                          │
               │ Creates selector         │ Calls methods
               │ based on type            │
               ▼                          ▼
┌──────────────────────────────┐   ┌─────────────────────────┐
│   MmuMachine                 │   │  Selector Methods       │
│  (mmu_machine.py)            │   │  - home()               │
│                              │   │  - select_gate()        │
│  selector_type choice:       │   │  - filament_drive()     │
│  - LinearSelector            │   │  - filament_release()   │
│  - StepperIdlerSelector ←───┼───┤                         │
│  - RotarySelector            │   │                         │
│  - ...                       │   │                         │
└──────────────┬───────────────┘   └─────────┬───────────────┘
               │                             │
               │ Instantiates                │
               ▼                             ▼
┌─────────────────────────────────────────────────────────────┐
│            StepperIdlerSelector Class                       │
│           (mmu_selector.py:2130-2423)                       │
│                                                             │
│  ┌─────────────────┐        ┌──────────────────┐          │
│  │ Selector        │        │ Idler            │          │
│  │ (MMU Toolhead)  │        │ (manual_stepper) │          │
│  │                 │        │                  │          │
│  │ - Homing        │        │ - Homing         │          │
│  │ - Positioning   │        │ - Positioning    │          │
│  │ - Endstop       │        │ - Endstop        │          │
│  └─────────────────┘        └──────────────────┘          │
│                                                             │
│  Variables (mmu_vars.cfg):                                 │
│  - mmu_selector_offsets = [5.0, 26.0, 47.0, 68.0, 89.0]   │
│  - mmu_idler_offsets = [4.0, 25.0, 46.0, 67.0, 88.0]      │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Links

### Source Files
- **Main Implementation:** [extras/mmu/mmu_selector.py (Lines 2119-2423)](extras/mmu/mmu_selector.py#L2119-L2423)
- **Integration:** [extras/mmu_machine.py](extras/mmu_machine.py)
- **Example Config:** [config/examples/mmu_stepper_idler_example.cfg](config/examples/mmu_stepper_idler_example.cfg)

### Documentation
- **Setup Guide:** [STEPPER_IDLER_SETUP.md](STEPPER_IDLER_SETUP.md)
- **Migration Guide:** [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Changelog:** [CHANGELOG_FORK.md](CHANGELOG_FORK.md)
- **Files Modified:** [FILES_MODIFIED.md](FILES_MODIFIED.md)

### Original Project
- **Happy Hare Wiki:** https://github.com/moggieuk/Happy-Hare/wiki
- **Happy Hare Source:** https://github.com/moggieuk/Happy-Hare

---

**Last Updated:** 2026-01-19
**Maintainer:** marek-hurt
**Fork:** https://github.com/marek-hurt/Happy-Hare-modified
