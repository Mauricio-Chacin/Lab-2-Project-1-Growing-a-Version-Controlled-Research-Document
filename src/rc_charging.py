import numpy as np
import matplotlib.pyplot as plt

V0 = 5.0
VIH = 0.7 * V0

# Nominal component values
R_nominal = 16e3       # 16 kOhm
C_nominal = 1e-6       # 1 uF

# Component tolerances
R_tolerance = 0.05     # +/- 5%
C_tolerance = 0.20     # +/- 20%

# Calculate tolerance limits
R_low = R_nominal * (1 - R_tolerance)
R_high = R_nominal * (1 + R_tolerance)

C_low = C_nominal * (1 - C_tolerance)
C_high = C_nominal * (1 + C_tolerance)

# Charging equation
def charging(t, R, C):
    tau = R * C
    return V0 * (1 - np.exp(-t / tau))


# Release time at VIH
def release_time(R, C):
    return -R * C * np.log(1 - VIH / V0)


# Calculate release times
t_release_nominal = release_time(R_nominal, C_nominal)

# Fastest case: minimum R and minimum C
t_release_fast = release_time(R_low, C_low)

# Slowest case: maximum R and maximum C
t_release_slow = release_time(R_high, C_high)


# Print results
print(f"Nominal R = {R_nominal/1e3:.1f} kOhm")
print(f"Nominal C = {C_nominal*1e6:.1f} uF")
print()

print(f"Fastest case:")
print(f"  R = {R_low/1e3:.1f} kOhm")
print(f"  C = {C_low*1e6:.1f} uF")
print(f"  t_release = {t_release_fast:.6f} s")
print()

print(f"Nominal case:")
print(f"  t_release = {t_release_nominal:.6f} s")
print()

print(f"Slowest case:")
print(f"  R = {R_high/1e3:.1f} kOhm")
print(f"  C = {C_high*1e6:.1f} uF")
print(f"  t_release = {t_release_slow:.6f} s")


# Time axis based on slowest time constant
tau_slow = R_high * C_high
t = np.linspace(0, 5 * tau_slow, 500)


# Plot the three charging curves
fig, ax = plt.subplots()

# Nominal - solid
ax.plot(
    t,
    charging(t, R_nominal, C_nominal),
    color="black",
    linewidth=2.5,
    label="Nominal R = 16k C = 1 uF"
)

# Fastest - dashed
ax.plot(
    t,
    charging(t, R_low, C_low),
    color="black",
    linestyle="--",
    linewidth=1.5,
    label="Fastest case R=15.2K C= 0.8 uF"
)

# Slowest - dash-dot
ax.plot(
    t,
    charging(t, R_high, C_high),
    color="black",
    linestyle="-.",
    linewidth=1.5,
    label="Slowest case R =16.8K C=1.2uF "
)


# VIH reference line
ax.axhline(
    VIH,
    linestyle=":",
    color="0.4",
    label=r"$V_{IH}$"
)


ax.grid(False)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)")

ax.set_title(
    "Capacitor charging for component tolerances"
)

ax.legend()

fig.savefig(
    "figures/generated/rc_tolerance.pdf",
    bbox_inches="tight"
)

plt.show()