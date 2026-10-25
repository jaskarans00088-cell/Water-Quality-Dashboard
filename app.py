import gradio as gr
import joblib
import numpy as np
import pandas as pd
import os
import base64
import plotly.graph_objects as go

# Load model and scaler
model = joblib.load('my_model.pkl')
scaler = joblib.load('my_scaler.pkl')

def predict_with_chart(ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity):
    # Create input dataframe with correct feature order
    input_data = pd.DataFrame([[
        ph, Hardness, Solids, Chloramines, Sulfate, Conductivity,
        Organic_carbon, Trihalomethanes, Turbidity
    ]], columns=[
        'ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity',
        'Organic_carbon', 'Trihalomethanes', 'Turbidity'
    ])

    # Scale input data
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]

    # Zero input validation check
    if (ph == 0 or Hardness == 0 or Solids == 0 or Chloramines == 0 or Sulfate == 0 or Conductivity == 0):
        empty_fig = go.Figure()
        empty_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=100
        )
        error_card = """
        <div class="status-card error-glow">
            <h3>⚠️ Invalid Input</h3>
            <p>Parameters cannot be zero!</p>
        </div>
        """
        return error_card, empty_fig
        
    is_unsafe = (Turbidity > 5 or Trihalomethanes > 0.1 or ph > 8.5 or ph < 6.5 or 
                 Solids > 1000 or Hardness > 500 or Sulfate > 500 or Chloramines > 4 or Organic_carbon > 2)

    conf = max(probability) * 100
    
    if is_unsafe or prediction == 0:
        status_card = f"""
        <div class="status-card danger-glow">
            <div class="status-icon">🚨</div>
            <h3>CRITICAL WARNING</h3>
            <p>Water is <b>NOT SAFE</b> for Consumption!</p>
            <div class="conf-badge">Confidence: {conf:.2f}%</div>
        </div>
        """
        bar_color = "#FF5252"
        status_label = "Not Safe"
    else:
        # Celebration status card with animated firecracker/confetti particles
        status_card = f"""
        <div class="status-card safe-glow celebratory-burst">
            <div class="firecracker-particle f1"></div>
            <div class="firecracker-particle f2"></div>
            <div class="firecracker-particle f3"></div>
            <div class="firecracker-particle f4"></div>
            <div class="firecracker-particle f5"></div>
            <div class="firecracker-particle f6"></div>
            <div class="status-icon">✨</div>
            <h3>SAFE FOR CONSUMPTION</h3>
            <p>Water quality parameters meet safety standards!</p>
            <div class="conf-badge">Confidence: {conf:.2f}%</div>
        </div>
        """
        bar_color = "#00BCD4"
        status_label = "Safe"

    # Build minimalist confidence meter bar chart with smooth transition
    fig = go.Figure(go.Bar(
        x=[conf],
        y=[status_label],
        orientation='h',
        marker=dict(
            color=bar_color,
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f"{conf:.1f}% Match"],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=14, family='sans-serif')
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=5, b=5, l=5, r=5),
        height=100,
        xaxis=dict(range=[0, 100], showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=True, tickfont=dict(color='white', size=13)),
        showlegend=False,
        transition=dict(duration=500, easing='cubic-in-out')
    )

    return status_card, fig

# Combined CSS: Starfield Galaxy Intro Splash + Back-lit Glowing Aura & Wave Light Structure
custom_css = """
@keyframes waveShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.gradio-container {
    background: linear-gradient(135deg, #0b131a, #0f2027, #203a43, #2c5364);
    background-size: 300% 300%;
    animation: waveShift 18s ease infinite;
    position: relative;
    overflow: hidden;
}

/* --- Galaxy Starfield Intro Splash Screen --- */
@keyframes splashFade {
    0% { opacity: 1; visibility: visible; }
    85% { opacity: 1; visibility: visible; }
    100% { opacity: 0; visibility: hidden; pointer-events: none; }
}

@keyframes galaxySpin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes starTwinkle {
    0%, 100% { opacity: 0.3; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.3); }
}

.splash-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: radial-gradient(circle at center, #1b003a 0%, #090014 60%, #020005 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 99999;
    animation: splashFade 1.8s ease 1.2s forwards;
    overflow: hidden;
}

/* Twinkling Galaxy Nebula Background Effect */
.galaxy-nebula {
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(147, 51, 234, 0.4) 0%, rgba(0, 229, 255, 0.25) 45%, transparent 75%);
    border-radius: 50%;
    animation: galaxySpin 20s linear infinite;
    z-index: 1;
}

/* Dense Starfield Dot Layers */
.star {
    position: absolute;
    background: #ffffff;
    border-radius: 50%;
    animation: starTwinkle 2s infinite ease-in-out;
    z-index: 1;
}

.s1 { width: 3px; height: 3px; top: 15%; left: 20%; animation-delay: 0.2s; box-shadow: 0 0 8px #fff; }
.s2 { width: 2px; height: 2px; top: 25%; left: 80%; animation-delay: 0.8s; box-shadow: 0 0 6px #00e5ff; }
.s3 { width: 4px; height: 4px; top: 75%; left: 15%; animation-delay: 1.2s; box-shadow: 0 0 10px #9333ea; }
.s4 { width: 2px; height: 2px; top: 80%; left: 85%; animation-delay: 0.5s; box-shadow: 0 0 6px #fff; }
.s5 { width: 3px; height: 3px; top: 40%; left: 10%; animation-delay: 1.5s; box-shadow: 0 0 8px #00e5ff; }
.s6 { width: 2px; height: 2px; top: 10%; left: 70%; animation-delay: 0.9s; box-shadow: 0 0 5px #fff; }
.s7 { width: 4px; height: 4px; top: 60%; left: 90%; animation-delay: 0.3s; box-shadow: 0 0 10px #fff; }
.s8 { width: 3px; height: 3px; top: 85%; left: 45%; animation-delay: 1.1s; box-shadow: 0 0 8px #9333ea; }
.s9 { width: 3px; height: 3px; top: 20%; left: 50%; animation-delay: 0.4s; box-shadow: 0 0 8px #00e5ff; }
.s10 { width: 2px; height: 2px; top: 50%; left: 95%; animation-delay: 1.3s; box-shadow: 0 0 6px #fff; }
.s11 { width: 4px; height: 4px; top: 30%; left: 35%; animation-delay: 0.7s; box-shadow: 0 0 10px #9333ea; }
.s12 { width: 3px; height: 3px; top: 90%; left: 25%; animation-delay: 1.0s; box-shadow: 0 0 8px #fff; }
.s13 { width: 2px; height: 2px; top: 12%; left: 92%; animation-delay: 0.6s; box-shadow: 0 0 5px #00e5ff; }
.s14 { width: 3px; height: 3px; top: 65%; left: 5%; animation-delay: 1.4s; box-shadow: 0 0 8px #fff; }
.s15 { width: 4px; height: 4px; top: 45%; left: 88%; animation-delay: 0.2s; box-shadow: 0 0 10px #9333ea; }
.s16 { width: 2px; height: 2px; top: 35%; left: 60%; animation-delay: 0.6s; box-shadow: 0 0 6px #00e5ff; }
.s17 { width: 3px; height: 3px; top: 70%; left: 70%; animation-delay: 1.1s; box-shadow: 0 0 8px #fff; }
.s18 { width: 2px; height: 2px; top: 18%; left: 40%; animation-delay: 0.3s; box-shadow: 0 0 5px #9333ea; }

.holo-container {
    position: relative;
    width: 240px;
    height: 240px;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2;
}

/* Back-lit Plasma Glow Halo around the Logo & Waves */
.holo-container::before {
    content: "";
    position: absolute;
    width: 140px;
    height: 140px;
    background: radial-gradient(circle, rgba(0, 229, 255, 0.5) 0%, rgba(147, 51, 234, 0.3) 50%, transparent 75%);
    border-radius: 50%;
    animation: auraPulse 2s infinite ease-in-out;
    z-index: 2;
}

@keyframes auraPulse {
    0%, 100% { transform: scale(0.9); opacity: 0.6; }
    50% { transform: scale(1.2); opacity: 1; }
}

/* Ocean Ripple Waves Expanding Outward with Bright Light Structure */
@keyframes oceanRipple {
    0% { width: 60px; height: 60px; opacity: 1; transform: scale(0.5); border-color: rgba(0, 229, 255, 1); box-shadow: 0 0 20px rgba(0,229,255,0.8); }
    100% { width: 210px; height: 210px; opacity: 0; transform: scale(1.3); border-color: rgba(147, 51, 234, 0.2); box-shadow: 0 0 5px rgba(147,51,234,0); }
}

.ocean-wave {
    position: absolute;
    border: 2.5px solid rgba(0, 229, 255, 0.9);
    border-radius: 50%;
    animation: oceanRipple 2.2s infinite ease-out;
    z-index: 3;
}

.ocean-wave:nth-child(1) { animation-delay: 0s; }
.ocean-wave:nth-child(2) { animation-delay: 0.75s; }
.ocean-wave:nth-child(3) { animation-delay: 1.5s; }

@keyframes dropletHover {
    0% { transform: scale(0.95) translateY(0px); filter: drop-shadow(0 0 20px rgba(0,229,255,0.9)); }
    50% { transform: scale(1.06) translateY(-8px); filter: drop-shadow(0 0 50px rgba(147,51,234,1)); }
    100% { transform: scale(0.95) translateY(0px); filter: drop-shadow(0 0 20px rgba(0,229,255,0.9)); }
}

.holo-droplet-svg {
    width: 80px;
    height: 100px;
    animation: dropletHover 1.6s infinite ease-in-out;
    position: relative;
    z-index: 5;
}

@keyframes textGlow {
    0% { opacity: 0.6; text-shadow: 0 0 8px rgba(0,229,255,0.6); }
    50% { opacity: 1; text-shadow: 0 0 30px rgba(147,51,234,1), 0 0 10px rgba(0,229,255,1); }
    100% { opacity: 0.6; text-shadow: 0 0 8px rgba(0,229,255,0.6); }
}

.holo-text {
    margin-top: 25px;
    color: #00e5ff;
    font-family: sans-serif;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 3px;
    animation: textGlow 1.5s infinite ease-in-out;
    z-index: 2;
}

/* --- Falling Water Droplets Layer --- */
.droplet-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 999;
    overflow: hidden;
}

.droplet {
    position: absolute;
    top: -50px;
    width: 4px;
    height: 15px;
    background: linear-gradient(to bottom, rgba(0, 188, 212, 0), rgba(0, 188, 212, 0.9));
    border-radius: 50%;
    animation: fall linear infinite;
}

@keyframes fall {
    0% { transform: translateY(-50px); opacity: 0; }
    50% { opacity: 1; }
    95% { opacity: 1; transform: translateY(95vh) scaleX(1) scaleY(1); height: 15px; }
    100% { transform: translateY(95vh) scaleX(3) scaleY(0.2); opacity: 0; }
}

.droplet:nth-child(1) { left: 15%; animation-duration: 2.2s; animation-delay: 0s; }
.droplet:nth-child(2) { left: 35%; animation-duration: 3.1s; animation-delay: 1.2s; }
.droplet:nth-child(3) { left: 55%; animation-duration: 2.5s; animation-delay: 0.5s; }
.droplet:nth-child(4) { left: 75%; animation-duration: 2.8s; animation-delay: 1.8s; }
.droplet:nth-child(5) { left: 90%; animation-duration: 3.5s; animation-delay: 0.8s; }

/* Status card container base */
.status-card {
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-family: sans-serif;
    transition: all 0.4s ease-in-out;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
}

.safe-glow {
    background: rgba(0, 188, 212, 0.18);
    border: 2px solid #00BCD4;
    box-shadow: 0 0 25px rgba(0, 188, 212, 0.5);
}

@keyframes blastShockwave {
    0% { transform: scale(0.98); box-shadow: 0 0 0 0 rgba(255, 82, 82, 0.8), 0 0 20px rgba(255, 82, 82, 0.5); }
    50% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(255, 82, 82, 0), 0 0 40px rgba(255, 82, 82, 0.8); }
    100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 82, 82, 0), 0 0 20px rgba(255, 82, 82, 0.5); }
}

.danger-glow {
    background: rgba(255, 82, 82, 0.2);
    border: 2px solid #FF5252;
    animation: blastShockwave 1.6s infinite ease-in-out;
}

.error-glow {
    background: rgba(255, 193, 7, 0.15);
    border: 2px solid #FFC107;
    box-shadow: 0 0 20px rgba(255, 193, 7, 0.4);
}

/* Celebratory Firecracker Confetti Particles */
.firecracker-particle {
    position: absolute;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    pointer-events: none;
    opacity: 0;
}

@keyframes firecrackerBurst {
    0% { transform: translate(0, 0) scale(1); opacity: 1; }
    50% { opacity: 0.8; }
    100% { transform: var(--burst-dir) scale(0.2); opacity: 0; }
}

.f1 { background: #FFD700; top: 50%; left: 50%; --burst-dir: translate(-70px, -50px); animation: firecrackerBurst 0.8s ease-out infinite; }
.f2 { background: #00E5FF; top: 50%; left: 50%; --burst-dir: translate(80px, -40px); animation: firecrackerBurst 0.9s ease-out 0.1s infinite; }
.f3 { background: #FF4081; top: 50%; left: 50%; --burst-dir: translate(-60px, 45px); animation: firecrackerBurst 0.75s ease-out 0.2s infinite; }
.f4 { background: #76FF03; top: 50%; left: 50%; --burst-dir: translate(70px, 50px); animation: firecrackerBurst 0.85s ease-out 0.15s infinite; }
.f5 { background: #00E676; top: 50%; left: 50%; --burst-dir: translate(0px, -65px); animation: firecrackerBurst 0.8s ease-out 0.05s infinite; }
.f6 { background: #FF9100; top: 50%; left: 50%; --burst-dir: translate(0px, 60px); animation: firecrackerBurst 0.9s ease-out 0.25s infinite; }

.status-icon {
    font-size: 32px;
    margin-bottom: 5px;
    position: relative;
    z-index: 2;
}

.conf-badge {
    margin-top: 10px;
    display: inline-block;
    padding: 5px 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    font-weight: bold;
    font-size: 14px;
    position: relative;
    z-index: 2;
}
"""

# HTML snippets for rich galaxy starfield intro splash with plasma back-lighting and background droplets
splash_html = """
<div class="splash-overlay">
    <div class="galaxy-nebula"></div>
    <div class="star s1"></div>
    <div class="star s2"></div>
    <div class="star s3"></div>
    <div class="star s4"></div>
    <div class="star s5"></div>
    <div class="star s6"></div>
    <div class="star s7"></div>
    <div class="star s8"></div>
    <div class="star s9"></div>
    <div class="star s10"></div>
    <div class="star s11"></div>
    <div class="star s12"></div>
    <div class="star s13"></div>
    <div class="star s14"></div>
    <div class="star s15"></div>
    <div class="star s16"></div>
    <div class="star s17"></div>
    <div class="star s18"></div>
    <div class="holo-container">
        <div class="ocean-wave"></div>
        <div class="ocean-wave"></div>
        <div class="ocean-wave"></div>
        <svg class="holo-droplet-svg" viewBox="0 0 24 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 0C12 0 24 13.7143 24 20C24 26.6274 18.6274 32 12 32C5.37258 32 0 26.6274 0 20C0 13.7143 12 0Z" fill="url(#dropletGradient)" stroke="rgba(255,255,255,0.95)" stroke-width="0.8"/>
          <defs>
            <radialGradient id="dropletGradient" cx="35%" cy="30%" r="70%">
              <stop offset="0%" stop-color="white" stop-opacity="1"/>
              <stop offset="40%" stop-color="#00E5FF" stop-opacity="0.95"/>
              <stop offset="100%" stop-color="#9333EA" stop-opacity="0.85"/>
            </radialGradient>
          </defs>
        </svg>
    </div>
    <div class="holo-text">INITIALIZING COSMIC WATER AI...</div>
</div>
"""

droplet_html = """
<div class="droplet-background">
    <div class="droplet"></div>
    <div class="droplet"></div>
    <div class="droplet"></div>
    <div class="droplet"></div>
    <div class="droplet"></div>
</div>
"""

# Build the dashboard layout
with gr.Blocks(theme=gr.themes.Soft(primary_hue="cyan", secondary_hue="teal"), css=custom_css) as demo:
    gr.HTML(splash_html)
    gr.HTML(droplet_html)
    
    gr.Markdown("# 💧 Water Quality 🛡️ Safety Predictor Dashboard")
    
    if os.path.exists("water_banner.png"):
        with open("water_banner.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        gr.Markdown(f'<img src="data:image/png;base64,{encoded_string}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">')
    
    gr.Markdown("Enter the physical and chemical parameters of the water sample and click Submit to predict water safety.")
    
    with gr.Row():
        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.TabItem("🧪 Physical & Minerals"):
                    ph = gr.Slider(minimum=0.0, maximum=14.0, step=0.1, value=7.2, label="pH Level")
                    hardness = gr.Slider(minimum=0.0, maximum=1000.0, step=1.0, value=150.0, label="Hardness (mg/L)")
                    solids = gr.Slider(minimum=0.0, maximum=3000.0, step=10.0, value=300.0, label="Solids / TDS (mg/L)")
                    conductivity = gr.Slider(minimum=0.0, maximum=2000.0, step=10.0, value=400.0, label="Conductivity (µS/cm)")
                
                with gr.TabItem("⚗️ Chemical & Organics"):
                    chloramines = gr.Slider(minimum=0.0, maximum=12.0, step=0.1, value=2.0, label="Chloramines (mg/L)")
                    sulfate = gr.Slider(minimum=0.0, maximum=1000.0, step=5.0, value=100.0, label="Sulfate (mg/L)")
                    organic_carbon = gr.Slider(minimum=0.0, maximum=30.0, step=0.1, value=1.0, label="Organic Carbon / TOC (mg/L)")
                    trihalomethanes = gr.Slider(minimum=0.0, maximum=0.5, step=0.01, value=0.05, label="Trihalomethanes / THMs (mg/L)")
                    turbidity = gr.Slider(minimum=0.0, maximum=10.0, step=0.1, value=0.5, label="Turbidity (NTU)")

            submit_btn = gr.Button("🔍 Predict Water Safety", variant="primary", size="lg")
            
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Prediction Result")
            output_html = gr.HTML(value="<div class='status-card' style='background: rgba(255,255,255,0.05); border: 1px dashed rgba(255,255,255,0.2);'><p>Awaiting prediction...</p></div>")
            output_plot = gr.Plot(label="")

    submit_btn.click(
        fn=predict_with_chart,
        inputs=[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity],
        outputs=[output_html, output_plot]
    )

if __name__ == "__main__":
    port= int(os.environ.get("PORT",7860))
    demo.launch(server_name="0.0.0.0",server_port=port)            
