# Documentation Index - Happy-Hare-Modified

Complete guide to all documentation files in this fork.

## 📚 Quick Navigation

| Document | Size | Purpose | Audience |
|----------|------|---------|----------|
| [README.md](README.md) | 17KB | Main overview, quick start | Everyone |
| [CODE_REFERENCE.md](CODE_REFERENCE.md) | 17KB | Code snippets, implementation details | Developers |
| [STEPPER_IDLER_SETUP.md](STEPPER_IDLER_SETUP.md) | 7KB | Complete setup guide | Users |
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | 8KB | Migration from 3D-Druckerplausch | Migrating users |
| [IDLER_BEHAVIOR.md](IDLER_BEHAVIOR.md) | 3KB | Rotary idler behavior explained | Everyone |
| [CHANGELOG_FORK.md](CHANGELOG_FORK.md) | 3KB | What's new in this fork | Everyone |
| [FILES_MODIFIED.md](FILES_MODIFIED.md) | 5KB | List of modified files | Developers/Maintainers |
| [test/TESTING.md](test/TESTING.md) | 6KB | Unit testing guide | Developers/Testers |

## 🚀 Getting Started Path

### For New Users:
1. Start with **[README.md](README.md)** - Understand what this fork does
2. Read **[STEPPER_IDLER_SETUP.md](STEPPER_IDLER_SETUP.md)** - Learn how to set it up
3. Use **[Example Config](config/examples/mmu_stepper_idler_example.cfg)** - Copy and adapt

### For Migrating Users (from 3D-Druckerplausch-Klipper):
1. Read **[README.md](README.md)** - Understand the differences
2. Follow **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Step-by-step conversion
3. Reference **[STEPPER_IDLER_SETUP.md](STEPPER_IDLER_SETUP.md)** - For detailed options

### For Developers:
1. Check **[CODE_REFERENCE.md](CODE_REFERENCE.md)** - See code snippets
2. Review **[FILES_MODIFIED.md](FILES_MODIFIED.md)** - Understand what changed
3. Read **[CHANGELOG_FORK.md](CHANGELOG_FORK.md)** - See feature list
4. Run **[Unit Tests](test/TESTING.md)** - Verify your changes work

## 📖 Document Details

### README.md
**What it contains:**
- Fork modification overview
- Key features comparison
- Quick start (4 steps)
- Installation instructions
- Comparison table: StepperIdlerSelector vs LinearSelector
- Use cases
- Compatibility notes
- Links to all other documentation

**When to read:**
- First time learning about this fork
- Deciding if this fork fits your needs
- Quick reference for installation

---

### CODE_REFERENCE.md
**What it contains:**
- Modified file locations with line numbers
- Code snippets from implementation
- Class structure diagram
- Key method implementations
- Integration points explained
- Configuration examples (minimal, full, stallguard)
- G-code command implementations
- Data flow diagram

**When to read:**
- Understanding the implementation
- Contributing code
- Debugging issues
- Learning Python/Klipper integration

**Highlights:**
- Complete class structure of `StepperIdlerSelector`
- Before/After code comparisons
- Links to exact line numbers in source
- Example configurations at different complexity levels

---

### STEPPER_IDLER_SETUP.md
**What it contains:**
- Complete setup guide
- When to use StepperIdlerSelector
- Architecture explanation
- Step-by-step configuration
- Calibration procedures
- Manual position entry
- G-code command reference
- Troubleshooting guide
- Comparison tables

**When to read:**
- Setting up StepperIdlerSelector for the first time
- Troubleshooting setup issues
- Understanding calibration
- Reference for G-code commands

**Highlights:**
- Clear when-to-use section
- Detailed CAD parameter explanation
- Multiple calibration methods
- Common troubleshooting scenarios

---

### MIGRATION_GUIDE.md
**What it contains:**
- Why migrate from 3D-Druckerplausch-Klipper
- Prerequisites checklist
- Value extraction from old config
- CAD parameter calculation
- Stepper configuration conversion (OLD vs NEW)
- Pin mapping examples
- Macro migration table
- Troubleshooting specific to migration

**When to read:**
- Migrating from 3D-Druckerplausch-Klipper
- Converting existing MMU2S setup
- Understanding differences between systems

**Highlights:**
- Side-by-side configuration comparison
- Formula for calculating CAD values
- Complete macro conversion table
- Migration-specific troubleshooting

---

### CHANGELOG_FORK.md
**What it contains:**
- All modifications made in this fork
- New features added
- New G-code commands
- Configuration parameters
- Compatibility information
- Credits

**When to read:**
- Seeing what's new in this fork
- Understanding fork scope
- Contributing credits

**Highlights:**
- Chronological list of changes
- Clear attribution to original authors
- Compatibility statements

---

### FILES_MODIFIED.md
**What it contains:**
- Complete list of modified files
- Line numbers and changes
- New files created
- Statistics (lines added, files changed)
- Maintenance notes
- Testing checklist
- Git diff commands

**When to read:**
- Understanding fork scope
- Reviewing before updates
- Contributing to the fork
- Syncing with upstream

**Highlights:**
- Testing checklist for QA
- Maintenance procedures
- Exact change locations

---

## 🔧 Configuration Files

### config/examples/mmu_stepper_idler_example.cfg
**What it contains:**
- Complete working configuration example
- All required sections
- TMC2209 configuration
- Pin mapping examples
- Calibration instructions embedded
- Comments explaining each setting

**When to use:**
- Starting point for your config
- Reference for pin mappings
- Understanding required sections
- Verifying your configuration

---

## 🔗 External Resources

### Original Happy Hare Documentation
- **Wiki:** https://github.com/moggieuk/Happy-Hare/wiki
- **GitHub:** https://github.com/moggieuk/Happy-Hare
- **Discord:** https://discord.gg/aABQUjkZPk

### Related Projects
- **3D-Druckerplausch-Klipper:** https://github.com/3D-Druckerplausch/Klipper_cfg (archived)
- **Prusa MMU2S:** https://www.prusa3d.com/product/original-prusa-i3-mmu3-upgrade-kit-for-mk3s-mk2-5s/

---

## 📋 Quick Reference Tables

### File Purpose Matrix

| File | User | Developer | Migrator | Maintainer |
|------|------|-----------|----------|------------|
| README.md | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| CODE_REFERENCE.md | ⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| STEPPER_IDLER_SETUP.md | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ |
| MIGRATION_GUIDE.md | ⭐ | ⭐ | ⭐⭐⭐ | ⭐ |
| IDLER_BEHAVIOR.md | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| CHANGELOG_FORK.md | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| FILES_MODIFIED.md | ⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| test/TESTING.md | ⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ |

⭐ = Relevant | ⭐⭐ = Important | ⭐⭐⭐ = Essential

### Documentation Depth

| File | Depth | Technical Level | Time to Read |
|------|-------|-----------------|--------------|
| README.md | Overview | Low | 5 min |
| CODE_REFERENCE.md | Deep | High | 20 min |
| STEPPER_IDLER_SETUP.md | Detailed | Medium | 15 min |
| MIGRATION_GUIDE.md | Step-by-step | Medium | 30 min |
| IDLER_BEHAVIOR.md | Detailed | Medium | 5 min |
| CHANGELOG_FORK.md | Summary | Low | 2 min |
| FILES_MODIFIED.md | Reference | High | 5 min |
| test/TESTING.md | Tutorial | High | 10 min |

---

## 🆘 Common Scenarios

### "I just want to get started"
→ [README.md](README.md) → [STEPPER_IDLER_SETUP.md](STEPPER_IDLER_SETUP.md) → [Example Config](config/examples/mmu_stepper_idler_example.cfg)

### "I'm migrating from 3D-Druckerplausch-Klipper"
→ [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) → [STEPPER_IDLER_SETUP.md](STEPPER_IDLER_SETUP.md)

### "I want to understand the code"
→ [CODE_REFERENCE.md](CODE_REFERENCE.md) → [Source Files](extras/mmu/mmu_selector.py)

### "Something isn't working"
→ [STEPPER_IDLER_SETUP.md#troubleshooting](STEPPER_IDLER_SETUP.md) → [MIGRATION_GUIDE.md#troubleshooting](MIGRATION_GUIDE.md)

### "I want to contribute"
→ [CODE_REFERENCE.md](CODE_REFERENCE.md) → [FILES_MODIFIED.md](FILES_MODIFIED.md)

---

## 📞 Support

1. Check the **Troubleshooting** section in relevant docs
2. Review the **Example Configuration**
3. Search the **Happy Hare Wiki**
4. Ask in **Happy Hare Discord:** https://discord.gg/aABQUjkZPk
5. Open an **Issue** on GitHub

---

**Last Updated:** 2026-01-19
**Documentation Version:** 1.0
**Fork Maintainer:** marek-hurt
