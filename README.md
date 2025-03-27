# LQR Controller for Energy Optimization in Building
This project develops an LQR controller and applies it to a building modeled by a 2R2C thermal network.
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
$T_{setting}=22c$,  $T_{swing}=1c$
<br/>
$Q$ and $R$ matrix:
```math
Q=\begin{bmatrix}
0.1 & 0 \\ 0 & 0
\end{bmatrix}, R=\begin{bmatrix}
0.02 \end{bmatrix}
```
![LQR_TZ_results](https://github.com/user-attachments/assets/a601ab93-456c-43fc-aebc-0dd46f8548de)


