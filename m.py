import streamlit as st
import time
import random
from datetime import datetime
import base64
import os
from pathlib import Path
from streamlit_folium import st_folium
import folium

# =========================
# 🎯 SETTINGS
# =========================
BIRTHDAY_DATE = datetime(2026, 8, 18, 0, 0, 0)
MOM_NAME = "Mom ❤️"
BIRTHDAY_TEXT = "🎉 শুভ জন্মদিন মা! 🎂"

# ---- Initialize session state keys (AVOID AttributeError) ----
if "slideshow_played" not in st.session_state:
    st.session_state.slideshow_played = False
if "gift_opened" not in st.session_state:
    st.session_state.gift_opened = False
if "show_letter" not in st.session_state:
    st.session_state.show_letter = False

# =========================
# 🌸 PAGE CONFIG
# =========================
st.set_page_config(page_title=f"Happy Birthday {MOM_NAME}", layout="centered")

def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        background-color: white;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("imageonline-co-brightnessadjusted (2).jpg")

# =========================
# 🎆 FIREWORKS + LONG-LASTING TEXT
# =========================
fireworks_html = f"""
<canvas id="fireworksCanvas" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index:-1;"></canvas>
<script>
var canvas = document.getElementById('fireworksCanvas');
var ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
var fireworks = [];
var textPoints = [];
var textCanvas = document.createElement('canvas');
var textCtx = textCanvas.getContext('2d');
textCanvas.width = 800;
textCanvas.height = 200;
textCtx.fillStyle = 'white';
textCtx.font = 'bold 48px Arial';
textCtx.fillText("{BIRTHDAY_TEXT}", 50, 100);
var imageData = textCtx.getImageData(0, 0, textCanvas.width, textCanvas.height);
for (var y = 0; y < imageData.height; y += 6) {{
    for (var x = 0; x < imageData.width; x += 6) {{
        var index = (y * imageData.width + x) * 4;
        if (imageData.data[index + 3] > 128) {{
            textPoints.push({{x: x, y: y}});
        }}
    }}
}}

function random(min, max) {{ return Math.random() * (max - min) + min; }}
function Firework(x, y, shape) {{
    this.x = x; this.y = y; this.shape = shape;
    this.particles = [];
    if (shape === 'text') {{
        textPoints.forEach(pt => {{
            this.particles.push({{
                x: x, y: y,
                vx: (pt.x - textCanvas.width/2) / 30,
                vy: (pt.y - textCanvas.height/2) / 30,
                alpha: 1,
                life: 200,
                color: '#FFD700',
                sparkle: Math.random() > 0.5
            }});
        }});
    }} else {{
        for (var i=0; i<50; i++) {{
            var angle = random(0, Math.PI * 2);
            var speed = random(2, 6);
            this.particles.push({{
                x: x, y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                alpha: 1,
                life: 100,
                color: ["#FF0000","#FFD700","#00FF00","#00CED1","#FF69B4"][Math.floor(Math.random()*5)],
                sparkle: Math.random() > 0.5
            }});
        }}
    }}
}}
Firework.prototype.update = function() {{
    this.particles.forEach(p => {{
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.02;
        p.life -= 1;
        if (p.life < 50) p.alpha -= 0.005;
    }});
}};
Firework.prototype.draw = function() {{
    this.particles.forEach(p => {{
        ctx.globalAlpha = p.alpha;
        ctx.fillStyle = p.sparkle && Math.random() > 0.5 ? 'white' : p.color;
        ctx.beginPath();
        ctx.arc(p.x + canvas.width/2 - 400, p.y + canvas.height/2 - 100, 2, 0, Math.PI * 2);
        ctx.fill();
    }});
}};
function loop() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (Math.random() < 0.03) {{
        fireworks.push(new Firework(random(100, canvas.width-100), random(100, canvas.height/2), 'normal'));
    }}
    if (Math.random() < 0.005) {{
        fireworks.push(new Firework(canvas.width/2, canvas.height/2, 'text'));
    }}
    fireworks.forEach(f => {{ f.update(); f.draw(); }});
    fireworks = fireworks.filter(f => f.particles[0].alpha > 0);
    requestAnimationFrame(loop);
}}
loop();
</script>
"""
st.markdown(fireworks_html, unsafe_allow_html=True)

# =========================
# 🎨 RAINBOW TITLE
# =========================
def rainbow_text(text):
    colors = ["#FF69B4", "#FF4500", "#FFD700", "#ADFF2F", "#00CED1", "#1E90FF", "#BA55D3"]
    result = ""
    for letter in text:
        if letter != " ":
            result += f"<span style='color:{random.choice(colors)}; font-size: 48px; font-weight: bold;'>{letter}</span>"
        else:
            result += " "
    return f"<div style='text-align: center;'>{result}</div>"

st.markdown(rainbow_text(BIRTHDAY_TEXT), unsafe_allow_html=True)
st.balloons()

# =========================
# 📅 COUNTDOWN
# =========================
now = datetime.now()
if now < BIRTHDAY_DATE:
    diff = BIRTHDAY_DATE - now
    countdown_text = f"⏳ পরের জন্মদিন আসতে কতদিন বাকি : {diff.days} days, {diff.seconds//3600} hours, {(diff.seconds//60)%60} minutes, {diff.seconds%60} seconds left!"
    st.markdown(f"<h3 style='color:#00FFFF;'>{countdown_text}</h3>", unsafe_allow_html=True)
else:
    st.markdown("<h3 style='color:#FF69B4;'>🎂 Today is the Big Day! Happy Birthday, Mom! 💐</h3>", unsafe_allow_html=True)
    st.snow()

# =========================
# 🖋 TYPEWRITER MESSAGE
# =========================
message = """
💖 পৃথিবীর সবচেয়ে ভালো মা,  
তোমার অফুরন্ত ভালোবাসা, সহায়তা ও যত্নের জন্য অসীম কৃতজ্ঞতা।  
তুমি আমার পথপ্রদর্শক আলো এবং সবচেয়ে বড় অনুপ্রেরণা।  
তোমার প্রতি আমার গভীর শ্রদ্ধা রয়েছে।  
তোমার জীবন হাসি, আনন্দ ও আশীর্বাদে ভরে উঠুক আজ এবং প্রতিদিন।  

**আমি তোমাকে চিরদিন ভালোবাসব! ❤️**
"""
placeholder = st.empty()
typed = ""
for char in message:
    typed += char
    colored_text = f"<span style='color:#FF69B4; font-size:20px; font-weight:600;'>{typed}</span>"
    placeholder.markdown(colored_text, unsafe_allow_html=True)
    time.sleep(0.03)

# =========================
# 📍 MAP (always render; keep order stable)
# =========================
st.markdown(
    "<h2 style='color:#ff1493; font-weight:bold;'>📌 তোমার জন্মস্থান</h2>", 
    unsafe_allow_html=True
)


# Create Folium map
m = folium.Map(location=[22.4999, 88.3474], zoom_start=16, control_scale=True)
folium.Marker(
    [22.4994, 88.3464],
    popup="MR Bangur Hospital",
    tooltip="MR Bangur Hospital",
    icon=folium.Icon(color="red", icon="heart")
).add_to(m)

with st.container():
    st_folium(m, use_container_width=True, height=500,key="birthplace_map")

# Custom CSS for map iframe
st.markdown("""
<style>
iframe[title="streamlit_folium.st_folium"] {
    height: 500px !important;
    width: 800px !important;
    max-width: 100%;
    border: none;
    margin: auto;
    display: block;
}
@media only screen and (max-width: 600px) {
    iframe[title="streamlit_folium.st_folium"] {
        width: 100% !important;
        height: 500px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# --- Slideshow (your original autoplay) ---
# =========================
st.markdown("""
<div style='
    text-align: center;
    color: #FF1493;
    font-size: 28px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: -10px;
    padding-top: 10px;
'>
    📸 তোমার কিছু হারিয়ে যাওয়া ছবি
</div>
""", unsafe_allow_html=True)

image_files = [
    Path("IMG_20250814_131006557_HDR (1).jpg"),
    # Path("IMG_20250814_131010777_HDR (1).jpg"),
    # Path("IMG_20250814_131228251_HDR (1).jpg"),
    # Path("IMG_20250814_131240651_HDR (1).jpg"),
    # Path("IMG_20250814_131304967_HDR (1).jpg"),
    # Path("IMG_20250814_131314266_HDR (1).jpg"),
    # Path("IMG_20250814_131333936_HDR (1).jpg"),
    # Path("IMG_20250814_131347993_HDR (1).jpg"),
    # Path("IMG_20250814_131351182_HDR (1).jpg"),
    # Path("IMG_20250814_131357386_HDR (1).jpg"),
    # Path("IMG_20250814_131502428_HDR.jpg"),
    # Path("IMG_20250814_132259749_HDR (1) (1).jpg"),
    # Path("IMG_20250814_132405431_HDR (1).jpg"),
    # Path("IMG_20250814_132724222_HDR (1) (1).jpg"),
    Path("IMG_20250814_132735942_HDR (1).jpg")
]

# Autoplay once, then keep last frame
if not st.session_state.slideshow_played:
    ph = st.empty()
    for img in image_files:
        with open(str(img), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        img_html = f"""
        <div style='text-align:center;'>
            <img src="data:image/jpeg;base64,{encoded_string}" 
                 style="height:400px; border-radius:12px;" />
            <p style='color:#FF69B4; font-weight:bold; font-size:18px;'>❤️ Ma – ছোটো থেকে বড়ো হয়ে ওঠার কিছু মুহূর্ত</p>
        </div>
        """
        ph.markdown(img_html, unsafe_allow_html=True)
        time.sleep(3)
    st.session_state.slideshow_played = True
else:
    # Show the last image (or choose one to persist)
    last_img = image_files[-1]
    with open(str(last_img), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    img_html = f"""
    <div style='text-align:center;'>
        <img src="data:image/jpeg;base64,{encoded_string}" 
             style="height:400px; border-radius:12px;" />
        <p style='color:#FF69B4; font-weight:bold; font-size:18px;'>❤️ Ma – {last_img.name}</p>
    </div>
    """
    st.markdown(img_html, unsafe_allow_html=True)
# =========================
# 📸 IMAGE + CAPTION GALLERY
# =========================

# List of images with captions
# =========================
# 📸 STACKED IMAGE REVEAL
# =========================

# List of (image_path, caption)
import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import os
st.markdown("""
<div style='
    text-align: center;
    color: #FF1493;
    font-size: 28px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: -10px;
    padding-top: 10px;
'>
    মায়ের পরিবারের সদস্যদের সাথে কিছু তোলা মুহূর্ত 👨‍👩‍👧‍👦💖📸
</div>
""", unsafe_allow_html=True)
# Your images with captions
images_with_captions = [
    ("Screenshot_20250814-205048.Google.png", "মায়ের নাচের স্কুলের জায়গা 🗺️."),
    ("didarsathe.jpg", "মা তার মেয়ের সাথে ছবি 👩‍👧❤️"),
    ("mamonirsathe.jpg", "মা তার বড় দিদির সাথে ছবি 👩‍👧‍👧📸"),
    ("mamarsathe.jpg", "মা তার ভাইয়ের সাথে ছবি 👩‍👦‍👦📸"),
    ("manimarstahe.jpg", "মা তার ছোট বোনের সাথে ছবি 👩‍👧‍👧📸")
]

# Function to load, resize, and encode image
def show_image(img_path, size=(300, 300)):
    if os.path.exists(img_path):
        img = Image.open(img_path)

        # Convert RGBA to RGB if needed
        if img.mode == "RGBA":
            img = img.convert("RGB")

        # Resize image to fixed size
        img = img.resize(size)

        # Save to buffer as JPEG
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        encoded = base64.b64encode(buffer.getvalue()).decode()

        return f'''
        <img src="data:image/jpeg;base64,{encoded}" 
             style="width:{size[0]}px; height:{size[1]}px;
                    border-radius: 12px; 
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);"/>
        '''
    else:
        return "<p style='color:red;'>⚠️ Image missing</p>"

# Display zigzag layout
for i, (img_path, caption) in enumerate(images_with_captions):
    col1, col2 = st.columns([1, 2])

    caption_html = f"""
    <div style='
        padding: 20px;
        background-color: #fff0f5;
        border-radius: 12px;
        box-shadow: 2px 2px 15px rgba(255,105,180,0.3);
        color: #FF69B4;
        font-size: 18px;
        font-weight: bold;
    '>
        {caption}
    </div>
    """

    if i % 2 == 0:
        # Image left, caption right
        col1.markdown(show_image(img_path), unsafe_allow_html=True)
        col2.markdown(caption_html, unsafe_allow_html=True)
    else:
        # Caption left, image right
        col1.markdown(caption_html, unsafe_allow_html=True)
        col2.markdown(show_image(img_path), unsafe_allow_html=True)

    # Divider
    st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)




# =========================
# 🎁 GIFT SURPRISE SECTION
# =========================
st.markdown("---")


if "gift_opened" not in st.session_state:
    st.session_state.gift_opened = False
if "video_watched" not in st.session_state:
    st.session_state.video_watched = False
if "show_letter" not in st.session_state:
    st.session_state.show_letter = False

# 🎁 Step 1: Show gift button
if not st.session_state.gift_opened:
    st.markdown("<h2 style='color:#FF69B4;'>🎁 Want a Surprise?</h2>", unsafe_allow_html=True)
    st.markdown("""
<div style='
    text-align: center;
    color: #FF1493;
    font-size: 28px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: -10px;
    padding-top: 10px;
'>
    ভিডিও দেখার জন্য ক্লিক করুন
</div>
""", unsafe_allow_html=True)
    
    if st.button("এখানে ক্লিক করুন 👇"):
        st.session_state.gift_opened = True
        st.rerun()

# 📽 Step 2: Play video
elif st.session_state.gift_opened and not st.session_state.video_watched:
    st.markdown("<h2 style='color:#FF69B4;'>### 💝 তোমার জন্য রয়েছে একটি বিশেষ চমকপ্রদ ভিডিও!</h2>", unsafe_allow_html=True)
    
    video_path = "km_20250814_720p_30f_20250814_142413.mp4"  # Change to your file name
    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        st.video(video_bytes)
        st.markdown("""
<div style="
    background-color: #fff0f5;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #ff69b4;
    color: #ff1493;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    box-shadow: 2px 2px 12px rgba(255,105,180,0.5);">
    💝 “তুমি আমার জীবনের সবচেয়ে মূল্যবান উপহার, মা। <br>
    এখানে একটি ছোট্ট চমক আছে, যা তোমাকে মনে করিয়ে দেবে তুমি কতটা ভালোবাসার মানুষ!”
</div>
""", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FF69B4;'>প্রথমে ভিডিওটি দেখুন তারপর continue বোতামটি ক্লিক করুন।</h2>", unsafe_allow_html=True)

        # audio_path = "শুভ জন্মদিন মা.mp3"
        # if os.path.exists(audio_path):
        #     st.audio(audio_path)
        # else:
        #     st.info("🔇 No audio found. You can add a voice message by placing `gift_audio.mp3` in this folder.")
    else:
        st.error(f"⚠️ Video not found: {video_path}")    

    # Continue button after video
    if st.button("Continue ➡️"):
        st.session_state.video_watched = True
        # st.rerun()

# # 💌 Step 3: Quaking button
# elif st.session_state.video_watched and not st.session_state.show_letter:
#     st.markdown("""
#         <style>
#         @keyframes quake {
#             0%, 100% { transform: translateX(0); }
#             25% { transform: translateX(-5px); }
#             50% { transform: translateX(5px); }
#             75% { transform: translateX(-5px); }
#         }
#         .button-wrapper {
#             text-align: center;
#             margin-top: 40px;
#         }
#         #shake-button {
#             font-size: 140px;
#             background: none;
#             border: none;
#             cursor: pointer;
#             animation: quake 0.8s infinite;
#             color: #d6336c;
#         }
#         #shake-button:hover { color: #ff4d6d; }
#         </style>
#     """, unsafe_allow_html=True)

#     if st.button("💌 Click to open message", key="letter_button"):
        st.session_state.show_letter = True
        st.rerun()

# ✨ Step 4: Show letter (everything else hidden)
elif st.session_state.show_letter:
    st.balloons()
    st.markdown("""
        <div style="
            background-color: #fff8dc;  
            border: 2px solid #f1c40f;  
            border-radius: 12px;  
            padding: 20px;  
            box-shadow: 0px 8px 20px rgba(0,0,0,0.2);
            max-width: 600px;
            margin: 30px auto;
            font-family: 'Georgia', serif;
            font-size: 20px;
            color: #333;
            line-height: 1.6;
            animation: fadeIn 1s ease-in-out;
        ">
            ✨ প্রিয় মা,<br><br>
    এই বিশেষ দিনে তোমাকে জানাই হৃদয়ভরা শুভেচ্ছা ও ভালোবাসা।<br><br>
    প্রতিটা মুহূর্ত তোমার মুখের হাসিতে ভরে উঠুক, আর আগামী দিনগুলো হোক আশীর্বাদময় ও শান্তিময়।<br><br>
    যতবার তোমার সাথে ঝগড়া করি, সব রাগের মাথায় করি — মনে থেকে নয়। তুমি কখনো খারাপ ভাবনা নিও না।<br><br>
    কেউ না থাকলেও আমি থাকব সবসময় মা তোমার পাশে।<br><br>
    তোমার মুনাই বাবা তোমারই থাকবে 💖<br><br>
    ❤️ ভালোবাসা ও শ্রদ্ধা সহ,<br>
    তোমার মুনাই বাবা 💖
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
<div style='
    text-align: center; 
    font-size: 18px; 
    color: #ff1493; 
    background-color: #fff0f5; 
    padding: 8px 12px; 
    border-radius: 8px; 
    font-weight: bold;
'>
    Made with ❤️ love by <span style='color:#ff4500;'>Munai Baba ❤️</span>
</div>
""", unsafe_allow_html=True)