# Quick Start - StepperIdlerSelector Minimální Konfigurace

Tento dokument obsahuje **minimální funkční konfiguraci** pro StepperIdlerSelector, která ti pomůže rychle rozjet systém.

## Krok 1: Minimální konfigurace pro test

Vytvoř nebo uprav soubor `~/printer_data/config/mmu/mmu_hardware.cfg`:

```ini
# ====================================================================
# MMU MACHINE - Základní nastavení
# ====================================================================
[mmu_machine]
num_gates: 5
selector_type: StepperIdlerSelector
mmu_vendor: Other
mmu_version: 1.0

# ====================================================================
# SELECTOR STEPPER (standardní, měl bys už mít)
# ====================================================================
[stepper_mmu_selector]
step_pin: mmu:MMU_SEL_STEP          # ZMĚŇ podle tvého HW
dir_pin: !mmu:MMU_SEL_DIR           # ZMĚŇ podle tvého HW
enable_pin: !mmu:MMU_SEL_ENABLE     # ZMĚŇ podle tvého HW
rotation_distance: 8
microsteps: 16
endstop_pin: ^mmu:MMU_SEL_ENDSTOP   # ZMĚŇ podle tvého HW
endstop_name: mmu_sel_home

[tmc2209 stepper_mmu_selector]
uart_pin: mmu:MMU_SEL_UART          # ZMĚŇ podle tvého HW
run_current: 0.4
sense_resistor: 0.110
stealthchop_threshold: 100

# ====================================================================
# IDLER STEPPER - TOHLE TI CHYBÍ!
# ====================================================================
[manual_stepper idler_stepper]
step_pin: mmu:MMU_IDLER_STEP        # ZMĚŇ podle tvého HW
dir_pin: mmu:MMU_IDLER_DIR          # ZMĚŇ podle tvého HW
enable_pin: !mmu:MMU_IDLER_ENABLE   # ZMĚŇ podle tvého HW
rotation_distance: 128               # ZMĚŇ podle tvého převodu
microsteps: 16
velocity: 100
accel: 80
endstop_pin: ^mmu:MMU_IDLER_ENDSTOP # ZMĚŇ podle tvého HW - fyzický endstop!

[tmc2209 manual_stepper idler_stepper]
uart_pin: mmu:MMU_IDLER_UART        # ZMĚŇ podle tvého HW
run_current: 0.4
sense_resistor: 0.110
stealthchop_threshold: 0

# ====================================================================
# GEAR STEPPER (standardní, měl bys už mít)
# ====================================================================
[stepper_mmu_gear]
step_pin: mmu:MMU_GEAR_STEP         # ZMĚŇ podle tvého HW
dir_pin: !mmu:MMU_GEAR_DIR          # ZMĚŇ podle tvého HW
enable_pin: !mmu:MMU_GEAR_ENABLE    # ZMĚŇ podle tvého HW
rotation_distance: 22.7
gear_ratio: 80:20
microsteps: 16

[tmc2209 stepper_mmu_gear]
uart_pin: mmu:MMU_GEAR_UART         # ZMĚŇ podle tvého HW
run_current: 0.5
sense_resistor: 0.110

# ====================================================================
# PARAMETRY - v mmu_parameters.cfg nebo zde
# ====================================================================
[mmu_config_setup]
# Selector rychlosti
selector_move_speed: 200
selector_homing_speed: 100

# Idler rychlosti
idler_move_speed: 100
idler_homing_speed: 80

# CAD pozice selectoru
cad_gate0_pos: 5.0
cad_gate_width: 21.0
cad_last_gate_offset: 2.0

# CAD pozice idleru - DŮLEŽITÉ!
cad_idler_gate0_pos: 5.0            # Pozice T0
cad_idler_gate_width: 21.0          # Vzdálenost mezi branami
cad_idler_home_position: 85.0       # UP pozice - žádné ložisko v kontaktu
```

## Krok 2: Najdi své piny

### Pokud migruješ z 3D-Druckerplausch-Klipper:

Podívej se do své staré konfigurace a najdi idler stepper piny. Měly by vypadat nějak takto:

```ini
# Ve staré konfiguraci hledej něco jako:
[stepper_idler]
# nebo
[manual_stepper idler]
# nebo podobné
```

### Typické piny pro různé boardy:

**BTT Octopus:**
```ini
MMU_IDLER_STEP=PE2
MMU_IDLER_DIR=PE3
MMU_IDLER_ENABLE=PD4
MMU_IDLER_UART=PE1
MMU_IDLER_ENDSTOP=PG14
```

**SKR 1.4:**
```ini
MMU_IDLER_STEP=P2.8
MMU_IDLER_DIR=P2.6
MMU_IDLER_ENABLE=P2.1
```

**ERCF Easy BRD:**
```ini
MMU_IDLER_STEP=gpio21
MMU_IDLER_DIR=gpio20
MMU_IDLER_ENABLE=gpio22
```

## Krok 3: Test

Po uložení konfigurace a `RESTART`:

```gcode
# 1. Zkontroluj že stepper vidí
QUERY_ENDSTOPS

# 2. Zkus manuální pohyb idlerem (jen pokud je safe!)
# MANUAL_STEPPER STEPPER=idler_stepper MOVE=10 SPEED=50

# 3. Zkus homovat idler
MMU_HOME
```

## Častý problém: rotation_distance

Pokud nevíš jakou `rotation_distance` použít pro idler:

1. **Prusa MMU2S**: 128mm
2. **Pokud máš GT2 řemenici 20 zubů**: `rotation_distance = 40` (20 zubů × 2mm)
3. **Pokud máš převod**: `rotation_distance = obvod_řemenice / převod`

## Další kroky po úspěšném startu

1. Kalibrace: `MMU_CALIBRATE_IDLER`
2. Test: `MMU_SOAKTEST_SELECTOR LOOP=5`
3. Nastavení rotary idler pozic podle tvého hardware

## Troubleshooting

### "Unknown pin chip name 'tmc2209_manual_stepper idler_stepper'"

❌ **Špatně:**
```ini
endstop_pin: tmc2209_manual_stepper idler_stepper:virtual_endstop
```

✅ **Správně (s mezerami nahrazenými podtržítky):**
```ini
endstop_pin: tmc2209_manual_stepper_idler_stepper:virtual_endstop
```

✅ **Nebo ještě lépe - použij fyzický endstop:**
```ini
endstop_pin: ^mmu:MMU_IDLER_ENDSTOP
```

### "StepperIdlerSelector requires [manual_stepper idler_stepper] configuration"

Chybí ti celá sekce `[manual_stepper idler_stepper]` - viz Krok 1 výše.

### "Option 'endstop_pin' in section 'manual_stepper idler_stepper' must be specified"

Zapomněl jsi nastavit `endstop_pin` v sekci `[manual_stepper idler_stepper]`.

### Idler se nepohybuje

1. Zkontroluj enable_pin (zkus `!mmu:MMU_IDLER_ENABLE` nebo bez `!`)
2. Zkontroluj dir_pin (zkus přidat nebo odebrat `!`)
3. Zkontroluj že máš správný `rotation_distance`

## Další pomoc

Viz kompletní dokumentaci:
- [STEPPER_IDLER_SETUP.md](STEPPER_IDLER_SETUP.md) - Detailní setup
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Migrace z 3D-Druckerplausch
- [IDLER_BEHAVIOR.md](IDLER_BEHAVIOR.md) - Jak rotary idler funguje
