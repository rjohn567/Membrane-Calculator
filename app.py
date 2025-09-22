import streamlit as st

st.set_page_config(page_title="Membrane Calculator", layout="centered")

st.title("Membrane Calculator")

# Create tabs
pages = st.tabs([
    "Welcome",
    "Single Gas Permeation",
    "Mixed Gas Permeation",
    "Single Gas Sorption"
])

with pages[0]:
    st.header("Welcome!")
    st.write("This is the Membrane Calculator web application. Use the tabs above to navigate between different calculators.")
    st.write("This website was built by Ryan Johnson at the University of Florida in Dr. Moon's lab. (Go Gators!) If you have any questions or feedback, please reach out!")
    st.write("Email: ryan.johnson@ufl.edu")
    st.write("LinkedIn: https://www.linkedin.com/in/ryan-johnson-328441172/")

with pages[1]:
    st.header("Single Gas Permeation")
    st.write("Permeability Calculator: Select the variable to solve for and enter the other values.")
    st.markdown(r"""
        <b>Downstream Volume Permeability Calculator</b><br>
        <span style='font-size: 1.1em;'>
        $$P = 10^{10} \cdot \frac{\frac{\Delta P}{\Delta t} \cdot V_d \cdot l}{p_2 \cdot A \cdot R \cdot T}$$
        </span>
        <br>
        <i>Where:</i><br>
        <ul>
        <li><b>P</b>: Permeability</li>
        <li><b>ΔP/Δt</b>: Pressure change over time</li>
        <li><b>V<sub>d</sub></b>: Downstream volume</li>
        <li><b>l</b>: Thickness</li>
        <li><b>p<sub>2</sub></b>: Feed pressure</li>
        <li><b>A</b>: Area</li>
        <li><b>R</b>: Gas constant</li>
        <li><b>T</b>: Temperature</li>
        </ul>
        """, unsafe_allow_html=True)
    
    variables = {
        "P": "Permeability (barrer)",
        "PressureChange": "Pressure Change (Torr)",
        "Time": "Time (min)",
        "V": "Volume (cm³)",
        "l": "Thickness (cm)",
        "A": "Area (cm²)",
        "dP": "Pressure Difference (atm)",
        "T": "Temperature (C)"
    }

    missing_var = st.selectbox("Select the variable to solve for:", list(variables.keys()), format_func=lambda x: variables[x], key="sgp_missing_var")

    input_values = {}
    cols = st.columns(2)
    for i, (var, label) in enumerate(variables.items()):
        if var != missing_var:
            input_values[var] = cols[i % 2].text_input(label, key=f"sgp_{var}")

    calc_btn = st.button("Calculate", key="sgp_calc_btn")
    result = None
    error = None
    if calc_btn:
        try:
            values = {}
            for var, val in input_values.items():
                if val.strip() == "":
                    raise ValueError(f"Missing value for {variables[var]}")
                values[var] = float(val)
            R = 2.78
            time_seconds = values["Time"] * 60 if "Time" in values else None
            dp_cmhg = values["dP"] * 76 if "dP" in values else None  # Convert atm to cmHg
            T_K = values["T"] + 273.15 if "T" in values else None  # Convert C to K
            if missing_var == "P":
                dpdt = values["PressureChange"] / time_seconds
                result = 1e10 * dpdt * values["V"] * values["l"] / (values["A"] * dp_cmhg * R * T_K)
            elif missing_var == "PressureChange":
                dpdt = 1e10 * values["V"] * values["l"] / (values["A"] * dp_cmhg * R * T_K) * values["P"]
                result = dpdt * time_seconds
            elif missing_var == "Time":
                dpdt = 1e10 * values["PressureChange"] * values["V"] * values["l"] / (values["A"] * dp_cmhg * R * T_K)
                result = values["PressureChange"] / dpdt / 60
            elif missing_var == "V":
                dpdt = values["PressureChange"] / time_seconds
                result = values["P"] * values["A"] * dp_cmhg * R * T_K / (1e10 * dpdt * values["l"])
            elif missing_var == "l":
                dpdt = values["PressureChange"] / time_seconds
                result = values["P"] * values["A"] * dp_cmhg * R * T_K / (1e10 * dpdt * values["V"])
            elif missing_var == "A":
                dpdt = values["PressureChange"] / time_seconds
                result = 1e10 * dpdt * values["V"] * values["l"] / (values["P"] * dp_cmhg * R * T_K)
            elif missing_var == "dP":
                dpdt = values["PressureChange"] / time_seconds
                result = 1e10 * dpdt * values["V"] * values["l"] / (values["A"] * values["P"] * R * T_K)
            elif missing_var == "T":
                dpdt = values["PressureChange"] / time_seconds
                result = 1e10 * dpdt * values["V"] * values["l"] / (values["A"] * dp_cmhg * R * values["P"])
            else:
                raise ValueError("Unknown variable")
        except Exception as e:
            error = f"Invalid input or missing values. {str(e)}"
    if result is not None:
        st.success(f"{variables[missing_var]} = {result:.6g}")
    if error:
        st.error(error)

with pages[2]:
    st.header("Mixed Gas Permeation")
    st.markdown(r"""
        <b>Mixed Gas Permeability Calculator</b><br>
        <span style='font-size: 1.1em;'>
        $$P = 10^{10} \cdot \frac{x_1 \cdot S \cdot l}{x_{h} \cdot A \cdot (p_2 x_2 - p_1 x_1)}$$
        </span>
        <br>
        <i>Where:</i><br>
        <ul>
        <li><b>P</b>: Permeability</li>
        <li><b>x<sub>1</sub></b>: Mole fraction of gas in permeate</li>
        <li><b>x<sub>h</sub></b>: Mole fraction of carrier gas in permeate</li>
        <li><b>x<sub>2</sub></b>: Mole fraction of gas in feed</li>
        <li><b>S</b>: Sweep gas flow rate</li>
        <li><b>l</b>: Thickness</li>
        <li><b>A</b>: Area</li>
        <li><b>p<sub>2</sub></b>: Upstream pressure</li>
        <li><b>p<sub>1</sub></b>: Downstream pressure</li>
        </ul>
        """, unsafe_allow_html=True)

    mgp_vars = {
        "P": "Permeability (barrer)",
        "x1": "Mole fraction of gas in permeate (x₁)",
        "xhe": "Mole fraction of carrier gas in permeate (xₕ)",
        "x2": "Mole fraction of gas in feed (x₂)",
        "S": "Sweep gas flow rate (sccm)",
        "l": "Thickness (cm)",
        "A": "Area (cm²)",
        "p2": "Upstream pressure (atm)",
        "p1": "Downstream pressure (atm)"
    }

    mgp_missing_var = st.selectbox("Select the variable to solve for:", list(mgp_vars.keys()), format_func=lambda x: mgp_vars[x], key="mgp_missing_var")

    mgp_inputs = {}
    mgp_cols = st.columns(2)
    for i, (var, label) in enumerate(mgp_vars.items()):
        if var != mgp_missing_var:
            mgp_inputs[var] = mgp_cols[i % 2].text_input(label, key=f"mgp_{var}")

    mgp_calc_btn = st.button("Calculate", key="mgp_calc_btn")
    mgp_result = None
    mgp_error = None
    if mgp_calc_btn:
        try:
            vals = {}
            for var, val in mgp_inputs.items():
                if val.strip() == "":
                    raise ValueError(f"Missing value for {mgp_vars[var]}")
                vals[var] = float(val)
                # convert pressures from atm to cmHg
            vals["p1"] = vals["p1"] * 76
            vals["p2"] = vals["p2"] * 76
            # Rearranged formulas for each variable
            if mgp_missing_var == "P":
                numerator = 1e10 * vals["x1"] * vals["S"] * vals["l"]
                denominator = vals["xhe"] * vals["A"] * (vals["p2"] * vals["x2"] - vals["p1"] * vals["x1"])
                if denominator == 0:
                    raise ValueError("Denominator is zero; check your inputs.")
                mgp_result = numerator / denominator
            elif mgp_missing_var == "x1":
                # Solve quadratic: a x1^2 + b x1 + c = 0
                # a = 1e10 * S * l + xhe * A * p1 * P
                # b = -xhe * A * p2 * x2 * P
                # c = 0
                # For practical purposes, use Newton's method or assume p1 x1 << p2 x2
                # Here, we solve for x1 numerically
                import scipy.optimize
                def eq_x1(x1):
                    return 1e10 * x1 * vals["S"] * vals["l"] - vals["xhe"] * vals["A"] * (vals["p2"] * vals["x2"] - vals["p1"] * x1) * vals["P"]
                sol = scipy.optimize.root_scalar(eq_x1, bracket=[1e-8, 1], method='bisect')
                if not sol.converged:
                    raise ValueError("Could not solve for x₁ numerically.")
                mgp_result = sol.root
            elif mgp_missing_var == "xhe":
                mgp_result = 1e10 * vals["x1"] * vals["S"] * vals["l"] / (vals["P"] * vals["A"] * (vals["p2"] * vals["x2"] - vals["p1"] * vals["x1"]))
            elif mgp_missing_var == "x2":
                mgp_result = (mgp_result := (vals["xhe"] * vals["A"] * vals["P"] * vals["p1"] * vals["x1"] + 1e10 * vals["x1"] * vals["S"] * vals["l"])) / (vals["xhe"] * vals["A"] * vals["P"] * vals["p2"])
            elif mgp_missing_var == "S":
                mgp_result = vals["xhe"] * vals["A"] * (vals["p2"] * vals["x2"] - vals["p1"] * vals["x1"]) * vals["P"] / (1e10 * vals["x1"] * vals["l"])
            elif mgp_missing_var == "l":
                mgp_result = vals["xhe"] * vals["A"] * (vals["p2"] * vals["x2"] - vals["p1"] * vals["x1"]) * vals["P"] / (1e10 * vals["x1"] * vals["S"])
            elif mgp_missing_var == "A":
                mgp_result = 1e10 * vals["x1"] * vals["S"] * vals["l"] / (vals["xhe"] * (vals["p2"] * vals["x2"] - vals["p1"] * vals["x1"]) * vals["P"])
            elif mgp_missing_var == "p2":
                mgp_result = ((mgp_result := 1e10 * vals["x1"] * vals["S"] * vals["l"] / (vals["xhe"] * vals["A"] * vals["P"])) + vals["p1"] * vals["x1"]) / vals["x2"]
            elif mgp_missing_var == "p1":
                mgp_result = (vals["p2"] * vals["x2"] - (1e10 * vals["x1"] * vals["S"] * vals["l"] / (vals["xhe"] * vals["A"] * vals["P"]))) / vals["x1"]
            else:
                raise ValueError("Unknown variable")
        except Exception as e:
            mgp_error = f"Invalid input or missing values. {str(e)}"
    if mgp_result is not None:
        st.success(f"{mgp_vars[mgp_missing_var]} = {mgp_result:.6g}")
    if mgp_error:
        st.error(mgp_error)

with pages[3]:
    st.header("Single Gas Sorption")
    st.markdown(r"""
        <b>Single Gas Sorption Calculator</b><br>
        <span style='font-size: 1.1em;'>
        $$S = \frac{n_m}{V_p \cdot P_f}$$   
        <br>
        $$n_m = \frac{\Delta P \cdot (V_s + V_c)}{R \cdot T} \cdot 22400$$
        </span>
        <br>
        <i>Where:</i><br>
        <ul>
        <li><b>S</b>: Sorption</li>
        <li><b>n<sub>m</sub></b>: Moles of gas sorbed</li>
        <li><b>ΔP</b>: Pressure drop</li>
        <li><b>V<sub>s</sub></b>: Sample chamber volume </li>
        <li><b>V<sub>c</sub></b>: Charge volume</li>
        <li><b>R</b>: Gas constant</li>
        <li><b>T</b>: Temperature</li>
        <li><b>V<sub>p</sub></b>: Volume of polymer</li>
        <li><b>P<sub>f</sub></b>: Final pressure</li>
        </ul>
        """, unsafe_allow_html=True)

    s_vars = {
        "S": "Sorption (cm³(STP)/cm³ polymer)",
        "DP": "Pressure drop (ΔP, psi)",
        "Vs": "Sample chamber volume (Vₛ, cm³)",
        "Vc": "Charge volume (V_c, cm³)",
        "T": "Temperature (K)",
        "Vp": "Volume of polymer (Vₚ, cm³)",
        "Pf": "Final pressure (P_f, atm)"
    }

    s_missing_var = st.selectbox("Select the variable to solve for:", list(s_vars.keys()), format_func=lambda x: s_vars[x], key="s_missing_var")

    s_inputs = {}
    s_cols = st.columns(2)
    for i, (var, label) in enumerate(s_vars.items()):
        if var != s_missing_var:
            s_inputs[var] = s_cols[i % 2].text_input(label, key=f"s_{var}")

    s_calc_btn = st.button("Calculate", key="s_calc_btn")
    s_result = None
    s_error = None
    R_CONST = 1206.2379
    if s_calc_btn:
        try:
            vals = {}
            for var, val in s_inputs.items():
                if val.strip() == "":
                    raise ValueError(f"Missing value for {s_vars[var]}")
                vals[var] = float(val)
            # Calculation logic
            if s_missing_var == "S":
                nm = vals["DP"] * (vals["Vs"] + vals["Vc"]) / (R_CONST * vals["T"])
                s_result = nm * 22.4 * 1000 / (vals["Vp"] * vals["Pf"])
            elif s_missing_var == "DP":
                S = vals["S"]
                # Rearranged: nm = S * Vp * Pf / (22.4 * 1000)
                nm = S * vals["Vp"] * (vals["Pf"]) / (22.4 * 1000)
                s_result = nm * R_CONST * vals["T"] / (vals["Vs"] + vals["Vc"])
            elif s_missing_var == "Vs":
                S = vals["S"]
                nm = S * vals["Vp"] * (vals["Pf"]) / (22.4 * 1000)
                s_result = (nm * R_CONST * vals["T"] / vals["DP"]) - vals["Vc"]
            elif s_missing_var == "Vc":
                S = vals["S"]
                nm = S * vals["Vp"] * (vals["Pf"]) / (22.4 * 1000)
                s_result = (nm * R_CONST * vals["T"] / vals["DP"]) - vals["Vs"]
            elif s_missing_var == "T":
                S = vals["S"]
                nm = S * vals["Vp"] * (vals["Pf"]) / (22.4 * 1000)
                s_result = nm * R_CONST / (vals["DP"] * (vals["Vs"] + vals["Vc"]))
            elif s_missing_var == "Vp":
                nm = vals["DP"] * (vals["Vs"] + vals["Vc"]) / (R_CONST * vals["T"])
                s_result = nm * 22.4 * 1000 / (vals["S"] * vals["Pf"])
            elif s_missing_var == "Pf":
                nm = vals["DP"] * (vals["Vs"] + vals["Vc"]) / (R_CONST * vals["T"])
                s_result = nm * 22.4 * 1000 / (vals["Vp"] * vals["S"])
            else:
                raise ValueError("Unknown variable")
        except Exception as e:
            s_error = f"Invalid input or missing values. {str(e)}"
    if s_result is not None:
        st.success(f"{s_vars[s_missing_var]} = {s_result:.6g}")
    if s_error:
        st.error(s_error)
