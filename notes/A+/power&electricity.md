# 1. Electricity & Power Fundamentals

Electricity is the backbone of all computer components. Understanding how voltage, current, resistance, and power interact will make hardware, power supplies, and troubleshooting far clearer.

---

## 1.1 Atomic Structure & Charge

Everything electrical begins with the **atom**:

- **Protons** → Positive charge
- **Electrons** → Negative charge
- **Neutrons** → Neutral

**Key points:**

- Electrons orbit the nucleus in "shells"
- The **valence shell** (outermost shell) determines how tightly electrons are held
- Materials with loosely held outer electrons conduct electricity well

---

## 1.2 Conductors vs Insulators

| Material Type | Behavior | Examples |
|---------------|----------|----------|
| **Conductors** | Allow free electron movement | Copper, silver, gold, aluminum |
| **Insulators** | Block electron flow | Rubber, plastic, glass |

Computers use **copper** for almost all internal wiring and traces because it is cheap and highly conductive.

---

## 1.3 Voltage, Current, and Resistance

These three variables define electrical behavior:

### ⚡ Voltage (V) – "Electrical Pressure"

- The force pushing electrons through a conductor
- It's like water pressure in a pipe
- Higher voltage = stronger push

### 🔌 Current (I, measured in Amps)

- Flow of electrons through a circuit
- 1 Amp = **1 Coulomb of electrons per second**
- Computer components draw only the current they need

### 🛑 Resistance (R, measured in Ohms)

- Restriction to electron flow
- Every component and cable has some amount of resistance

---

## 1.4 Ohm's Law (Must Know)

This fundamental law defines the relationship between voltage, current, and resistance:

```
V = I × R
```

**Meaning:**

- Increase voltage → current increases
- Increase resistance → current decreases
- Decrease resistance (short circuit) → current spikes → dangerous

---

## 1.5 Power (Watts) – The Work Being Done

Power represents the **rate of energy use**.

```
P = V × I
```

**Examples:**

- A CPU that pulls **1.2V at 80A** = **96 Watts**
- A GPU that pulls **12V at 20A** = **240 Watts**

This is why high-performance GPUs require powerful PSUs with strong 12V rails.

---

## 1.6 AC vs DC Power

Computers use **DC power only** internally.

### AC (Alternating Current)

- Comes from the wall outlet
- Alternates polarity (120V in the U.S.)
- Travels long distances efficiently

### DC (Direct Current)

- Constant polarity
- Required by all computer components
- PSU converts AC → DC

---

## 1.7 The Power Supply Unit (PSU)

The PSU converts household AC into multiple DC output rails:

| Rail | Voltage | Purpose |
|------|---------|---------|
| **+12V** | CPU, GPU, fans, drives | Most important / highest load |
| **+5V** | Legacy devices, some logic circuits | |
| **+3.3V** | RAM, chipsets, motherboard logic | |

Modern systems use the **+12V rail** for most power delivery (especially CPU/GPU).

### PSU Considerations:

- Wattage rating (e.g., 550W, 750W, 1000W)
- Efficiency rating (80+ Bronze, Silver, Gold, Platinum)
- Modular vs semi-modular vs non-modular
- Protection:
  - OCP (over-current)
  - OVP (over-voltage)
  - OTP (over-temperature)
  - SCP (short-circuit)

---

## 1.8 "Power Good" Signal

When you press the power button:

1. PSU stabilizes voltages
2. Then sends a **Power Good** signal to the motherboard
3. Only then does the CPU begin executing firmware instructions

If the PSU fails this step → system will not boot.

---

## 1.9 Free Electrons & Electron Flow

Important to remember:

- Electrons flow from **negative → positive**
- Electricity moves through conductors via "free electrons"
- Materials with more free electrons = better conductors

This underlies all computer power and signal behavior.

---

## 1.10 Safety Fundamentals

Computers generally operate at **safe low voltages**, but hazards come from:

- **Capacitors** in PSUs (can hold charge even when unplugged)
- **Incorrect PSU wattage** (unstable systems)
- **Damaged cables** (shorts, sparks)
- **Improper grounding** (electrostatic discharge)

**Best practices:**

- Always unplug before working on internals
- Press power button after unplugging to drain capacitors
- Use an anti-static wrist strap when possible
- Keep metal tools clear of energized circuits

---

## 1.11 Quick Reference Summary

- **Voltage** pushes electrons
- **Current** is electron flow
- **Resistance** slows flow
- **Power** is work done
- **PSU converts AC → DC**
- **12V rail** powers nearly everything important
- **Power Good** = PSU to motherboard "green light"
- **Conductors** = metals; **insulators** = rubber/glass

---