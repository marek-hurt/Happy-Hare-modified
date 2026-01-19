# Happy Hare - StepperIdlerSelector Setup Guide

## Přehled

`StepperIdlerSelector` je nový typ selectoru pro Happy Hare, který umožňuje použít **krokový motor** místo serva pro pohyb idleru. Tento design je inspirován Prusa MMU2S a podobnými systémy.

## Kdy použít StepperIdlerSelector

Použij StepperIdlerSelector pokud:
- Máš MMU s krokovým motorem pro idler (namísto PWM serva)
- Chceš přesnější a spolehlivější ovládání idleru
- Máš setup podobný Prusa MMU2S
- Přecházíš z 3D-Druckerplausch-Klipper konfigurace na Happy Hare

## Architektura

StepperIdlerSelector používá:
1. **Selector stepper** - Lineární pohyb pro výběr gate (součást MMU toolhead)
2. **Idler stepper** - Krokový motor pro přitlačení/uvolnění filamentu (manual_stepper)
3. **Gear stepper** - Pohon filamentu (součást MMU toolhead)

## Instalace a konfigurace

### 1. Základní konfigurace MMU

V souboru `mmu.cfg` nebo `mmu_hardware.cfg`:

```ini
[mmu_machine]
num_gates: 5
mmu_vendor: Other
mmu_version: 1.0

# DŮLEŽITÉ: Nastav selector_type na StepperIdlerSelector
selector_type: StepperIdlerSelector

variable_rotation_distances: 1
variable_bowden_lengths: 0
require_bowden_move: 1
filament_always_gripped: 0
has_bypass: 0
```

### 2. Konfigurace Selector stepperu

```ini
[tmc2209 stepper_mmu_selector]
uart_pin: mmu:MMU_SEL_UART
run_current: 0.4
hold_current: 0.2
interpolate: True
sense_resistor: 0.110
stealthchop_threshold: 100

[stepper_mmu_selector]
step_pin: mmu:MMU_SEL_STEP
dir_pin: !mmu:MMU_SEL_DIR
enable_pin: !mmu:MMU_SEL_ENABLE
rotation_distance: 8
microsteps: 16
gear_ratio: 1:1
full_steps_per_rotation: 200
endstop_pin: ^mmu:MMU_SEL_ENDSTOP
endstop_name: mmu_sel_home
```

### 3. Konfigurace Idler stepperu (KLÍČOVÉ!)

**Idler MUSÍ být konfigurován jako `manual_stepper idler_stepper`:**

```ini
[tmc2209 manual_stepper idler_stepper]
uart_pin: mmu:MMU_IDLER_UART
run_current: 0.4
hold_current: 0.2
interpolate: True
sense_resistor: 0.110

[manual_stepper idler_stepper]
step_pin: mmu:MMU_IDLER_STEP
dir_pin: mmu:MMU_IDLER_DIR
enable_pin: !mmu:MMU_IDLER_ENABLE
rotation_distance: 128          # Přizpůsob podle tvého motoru
microsteps: 16
velocity: 100
accel: 80
endstop_pin: ^mmu:MMU_IDLER_ENDSTOP
```

### 4. Nastavení parametrů

V `mmu_parameters.cfg` nebo `mmu.cfg`:

```ini
# Rychlosti pohybu
selector_move_speed: 200
selector_homing_speed: 100
idler_move_speed: 100
idler_homing_speed: 80

# CAD parametry pro selector
cad_gate0_pos: 5.0              # Vzdálenost od home k prvnímu gate
cad_gate_width: 21.0            # Vzdálenost mezi gates
cad_last_gate_offset: 2.0
cad_selector_tolerance: 10.0

# CAD parametry pro idler
cad_idler_gate0_pos: 5.0        # Pozice idleru pro gate 0
cad_idler_gate_width: 21.0      # Vzdálenost mezi pozicemi idleru
cad_idler_tolerance: 10.0
```

## Kalibrace

### Krok 1: Zjisti své pozice

Pokud máš existující konfiguraci (např. z 3D-Druckerplausch-Klipper), můžeš použít známé hodnoty:

```python
# Příklad z mmu2s_variables.cfg:
idler = [4.0, 25.0, 46.0, 67.0, 88.0]  # 5 pozic pro T0-T4
colorselector = [5.0, 26.0, 47.0, 68.0, 89.0]
```

Nastav:
- `cad_idler_gate0_pos: 4.0` (první hodnota z pole idler)
- `cad_idler_gate_width: 21.0` (rozdíl mezi hodnotami: 25-4=21)
- `cad_gate0_pos: 5.0`
- `cad_gate_width: 21.0`

### Krok 2: Spusť kalibraci

```gcode
# Kalibrace selector pozic
MMU_CALIBRATE_SELECTOR

# Kalibrace idler pozic
MMU_CALIBRATE_IDLER
```

Tyto příkazy vypočítají pozice na základě CAD parametrů a uloží je do `mmu_vars.cfg`.

### Krok 3: Ověř hodnoty

Zkontroluj `mmu_vars.cfg`:
```ini
mmu_selector_offsets = [5.0, 26.0, 47.0, 68.0, 89.0]
mmu_idler_offsets = [4.0, 25.0, 46.0, 67.0, 88.0]
```

Pokud potřebuješ upravit, můžeš hodnoty editovat ručně.

### Krok 4: Test

```gcode
# Test pohybu selectoru a idleru
MMU_SOAKTEST_SELECTOR LOOP=10 HOME=1
```

## Manuální zadání pozic

Pokud již znáš přesné pozice z předchozí konfigurace, můžeš je zadat přímo do `mmu_vars.cfg`:

```ini
[Variables]
mmu_selector_offsets = [5.0, 26.0, 47.0, 68.0, 89.0]
mmu_idler_offsets = [4.0, 25.0, 46.0, 67.0, 88.0]
```

## Převod z 3D-Druckerplausch-Klipper

Pokud migruješ z 3D-Druckerplausch-Klipper:

1. **Najdi své hodnoty** v `mmu2s_variables.cfg`:
   ```python
   variable_idler: [4.0, 25.0, 46.0, 67.0, 88.0]
   variable_colorselector: [5.0, 26.0, 47.0, 68.0, 89.0]
   ```

2. **Převeď board konfigurace**:
   - `[manual_stepper idler_stepper]` → zůstává stejně
   - `[manual_stepper selector_stepper]` → změň na `[stepper_mmu_selector]`
   - `[manual_stepper gear_stepper]` → změň na `[stepper_mmu_gear]`

3. **Použij hodnoty**:
   ```ini
   cad_idler_gate0_pos: 4.0
   cad_idler_gate_width: 21.0
   cad_gate0_pos: 5.0
   cad_gate_width: 21.0
   ```

## Příkazy G-code

StepperIdlerSelector poskytuje tyto příkazy:

- `MMU_CALIBRATE_SELECTOR` - Vypočítá a uloží pozice selectoru
- `MMU_CALIBRATE_IDLER` - Vypočítá a uloží pozice idleru
- `MMU_SOAKTEST_SELECTOR [LOOP=100] [HOME=0|1]` - Test pohybu

## Troubleshooting

### Chyba: "StepperIdlerSelector requires [manual_stepper idler_stepper]"
- Ujisti se, že máš sekci `[manual_stepper idler_stepper]` v konfiguraci

### Idler se nepohybuje
- Zkontroluj `rotation_distance` a směr (`dir_pin`)
- Ověř, že endstop funguje (pro homing)

### Selector se pohybuje, ale idler ne
- Zkontroluj, že `idler_offsets` jsou správně nastaveny
- Použij `MMU_CALIBRATE_IDLER` pro přegenerování

### Pozice jsou nepřesné
- Uprav `cad_idler_gate_width` a `cad_gate_width`
- Nebo ručně edituj pozice v `mmu_vars.cfg`

## Příklad kompletní konfigurace

Viz [mmu_stepper_idler_example.cfg](Happy-Hare/config/examples/mmu_stepper_idler_example.cfg)

## Klíčové rozdíly oproti LinearSelector

| Vlastnost | LinearSelector | StepperIdlerSelector |
|-----------|----------------|---------------------|
| Idler ovládání | PWM Servo | Krokový motor |
| Idler konfigurace | `[mmu_servo selector_servo]` | `[manual_stepper idler_stepper]` |
| Přesnost | Závisí na servu | Vysoká (krokový motor) |
| Kalibrace | Úhly serva | Lineární pozice (mm) |
| Homing idleru | Ne | Ano (endstop/stallguard) |

## Výhody StepperIdlerSelector

✅ Vyšší přesnost a opakovatelnost
✅ Možnost použít sensorless homing (stallguard)
✅ Žádné problémy s servo kickback
✅ Lepší kontrola síly přítlaku
✅ Kompatibilní s Prusa MMU2S hardwarem

## Podpora

Pro dotazy a pomoc:
- Discord: Happy Hare community
- GitHub: https://github.com/moggieuk/Happy-Hare

---
**Autor:** Custom implementation pro Happy Hare
**Datum:** 2026-01-19
**Verze:** 1.0
