import streamlit as st
import numpy as np
import plotly.graph_objects as go

GRAPH_HEIGHT_PX = 500

st.title("Signal Generator with Noise")
col1, col2 = st.columns([1,4])

@st.cache_data
def generate_noise(mean, cov, size):
    return np.random.normal(mean, cov, size)

def generate_clean(x, amp, freq, phase):
    return amp * np.sin(2 * np.pi * freq * x + phase)

def easy_mean(signal: np.ndarray, s_k=0.2, max_k=0.9, d=1.5) -> np.ndarray:
    filtered = np.zeros_like(signal)
    filtered[0] = signal[0]
    for i in range(1, len(signal)):
        diff = signal[i] - filtered[i-1]
        k = s_k if abs(diff) < d else max_k
        filtered[i] = filtered[i-1] + diff * k
    return filtered



x = np.linspace(0, 10, 1000)

with col1:
    amp = st.slider("Amplitude", 0.0, 2.0, 1.0, 0.01)
    freq = st.slider("Frequency", 0.1, 5.0, 1.0, 0.01)
    phase = st.slider("Phase", 0.0, 2*np.pi, 0.0, 0.01)
    noise_mean = st.slider("Noise Mean", -1.0, 1.0, 0.0, 0.01)
    noise_cov = st.slider("Noise Covariance", 0.0, 1.0, 0.2, 0.01)
    show_noise = st.checkbox("Show Noise", value=True)

clean_signal = generate_clean(x, amp, freq, phase)
noise = generate_noise(noise_mean, noise_cov, len(x))
noisy_signal = clean_signal + noise
filtered_signal = easy_mean(noisy_signal)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=clean_signal, mode='lines', name='Clean Signal',
                            line=dict(color='blue', dash='dash')))
    if show_noise:
        fig.add_trace(go.Scatter(x=x, y=noisy_signal, mode='lines', name='Noisy Signal',
                                line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=x, y=filtered_signal, mode='lines', name='Filtered Signal',
                                line=dict(color='purple')))
        
    fig.update_layout(
        title="Signal Visualization",
        height=GRAPH_HEIGHT_PX,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )

    st.plotly_chart(fig, use_container_width=True)
