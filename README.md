# LQR controller for building thermal zone
# 2R2C building modeling
![2R2C](https://github.com/user-attachments/assets/1b5595fa-cb77-4f40-846e-9d52526e30ee)

**Model of room temperature:** <br/>
```math
\frac{dT_{r}}{dt}=\frac{1}{C_{r}R_{rm}}(T_{m}-T_{r})+\frac{1}{C_{r}R_{ra}}(T_{a}-T_{r})+\dot{Q}_{ac}
```
**Model of envelope temperature:** <br/>
```math
\frac{dT_{m}}{dt}=\frac{1}{C_{m}R_{rm}}(T_{m}-T_{r})
```
**State and space model of building thermal zone:** <br/>
```math
\begin{bmatrix}
\dot{T}_{r} \\
\dot{T}_{m}
\end{bmatrix}=\begin{bmatrix}
-(\frac{1}{C_{r}R_{rm}}+\frac{1}{C_{r}R_{ra}}) & \frac{1}{C_{r}R_{rm}} \\ \frac{1}{C_{m}R_{rm}}
 & -\frac{1}{C_{m}R_{rm}}
\end{bmatrix}\begin{bmatrix}
T_{r} \\ T_{m}
\end{bmatrix}+\begin{bmatrix}
\dot Q_{ac} \\ 0
\end{bmatrix}+\begin{bmatrix}
\frac{1}{C_{r}R_{ra}} \\0
\end{bmatrix} T_{a}
```
which can be written as:
```math
\dot x=Ax+Bu+Gd
```
```math
B=\begin{bmatrix}
1 \\ 0 \end{bmatrix}
```
where $d$ is the outdoor temperature which is considered as the disturbance term and $G$ is the according system matrix, $u$ is the control input (heater power, $\dot Q_{ac}$)
<br/>

# LQR optimal control
The problem is solved as finite-horizon problem with control horizon: 0.5 hrs
<br/>

**Quadratic cost function:**
```math
J=x^{T}(t_{1})F(t_{1})x(t_{1})+\int_{t_{0}}^{t_{1}}(x^{T}Qx+u^{T}Ru)dt
```
where $x$ is the states of the system, $u$ is the control input, $F(t_{1})$ is the initial cost matrix, $Q$ is the state cost matrix, and $R$ is the control cost matrix
<br/>
Since we only focus on the room temperature, and we only has one control input, the state cost matrix $Q$ and control cost matrix $R$ are given as:
```math
Q=\begin{bmatrix}
q & 0 \\ 0 & 0
\end{bmatrix}
```
```math
R=\begin{bmatrix}
r
\end{bmatrix}
```
where q and r values are decided by tuning
<br/>
<br/>
The feedback control law that minimized the cost function is:
```math
u=-K(x-T_{setting})-KGd
```
where $T_{setting}$ is the setting temperature of thermostat
<br/>
$K$ is given by:
```math
K=R^{-1}B^{T}P
```
$P$ is found by solving the Riccati differential equation:
```math
\frac{dP(t)}{dt}=-[A^{T}P(t)+P(t)A-P(t)BR^{-1}B^{T}P(t)+Q]
```
with the boundary condition:
```math
P(t_{1})=F(t_{1})=Q(t_{1})
```

**Constraints:**
<br/>
The heater input is between [10, 300] Watts

# Results
![LQR_TZ_results](https://github.com/user-attachments/assets/a601ab93-456c-43fc-aebc-0dd46f8548de)

| | $Q_1 [W]$     | $Q_2 [W]$      | $P_{total} [Pa]$      | $t_{fin,1}, t_{fin,2} [mm]$ | $b_{fin,1}, b_{fin,2} [mm]$      | $H_{fin} [mm]$      | $\forall_{air} [m^3/s]$     |
|-----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|
| Single-obj: fmincon | 158 | 116| 90 | 0.6, 1.2 | 3.7, 3.6  | 24.9  |0.0111 |
| Single-obj: ALM | 158  | 158  | 90  | 0.7, 0.3  | 3.8, 2.8  | 25  |0.0123 |
| Multi-obj: goalattain | 212  | 250 | 250  | 0.2, 1.0  | 2.8, 2.0  | 25 |0.015|

