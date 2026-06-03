import streamlit as st 
import base64
 
#----------- Config --------------
st.set_page_config(
    page_title="Raspadinha do Amor ❤️❤️❤️❤️",
    page_icon="❤️",
    layout="centered"
)
 
st.title("❤️ Raspe para revelar ❤️")
st.write("Arraste o mouse ou o dedo sobre a tela para revelar.")
 
#controle interno
if "surpresa" not in st.session_state:
    st.session_state.surpresa = False
 
 
 
#-------------- Função Base ----------------
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
 
 
foto = image_to_base64("foto_praia_01.jpg")       # imagem secreta
cover = image_to_base64("cover.JPG")     # camada da raspadinha
 
 
# ---------------- HTML + JS DA RASPADINHA ----------------
html_code = f"""
<!DOCTYPE html>
<html>
<body style="margin:0;">
 
<!-- Wrapper com position:relative para empilhar os dois canvas -->
<div style="display:flex; justify-content:center;">
  <div style="position:relative; width:600px; height:400px;">
 
    <!-- Canvas de baixo: foto secreta (não recebe eventos) -->
    <canvas id="canvasFoto"
      width="600" height="400"
      style="
        position:absolute; top:0; left:0;
        border-radius:20px;
      ">
    </canvas>
 
    <!-- Canvas de cima: cobertura raspável (recebe eventos) -->
    <canvas id="canvasCover"
      width="600" height="400"
      style="
        position:absolute; top:0; left:0;
        border-radius:20px;
        touch-action:none;
        cursor:pointer;
      ">
    </canvas>
 
  </div>
</div>
 
<script>
 
// --- Canvas da foto secreta (fundo) ---
const canvasFoto  = document.getElementById("canvasFoto");
const ctxFoto     = canvasFoto.getContext("2d");
 
// --- Canvas da cobertura (cima) ---
const canvasCover = document.getElementById("canvasCover");
const ctxCover    = canvasCover.getContext("2d");
 
const imgFoto  = new Image();
const imgCover = new Image();
 
let raspando = false;
let surpresaLiberada = false;
 
// Carrega a foto secreta no canvas de baixo
imgFoto.onload = () => {{
    ctxFoto.drawImage(imgFoto, 0, 0, canvasFoto.width, canvasFoto.height);
 
    // Depois carrega a cobertura no canvas de cima
    imgCover.onload = () => {{
        ctxCover.drawImage(imgCover, 0, 0, canvasCover.width, canvasCover.height);
    }};
    imgCover.src = "data:image/jpeg;base64,{cover}";
}};
 
imgFoto.src = "data:image/jpeg;base64,{foto}";
 
 
// --- Posição do cursor/toque ---
function getPos(e) {{
    const rect = canvasCover.getBoundingClientRect();
    if (e.touches) {{
        return {{
            x: e.touches[0].clientX - rect.left,
            y: e.touches[0].clientY - rect.top
        }};
    }}
    return {{
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    }};
}}
 
 
// --- Verifica quanto foi raspado ---
function verificarProgresso() {{
 
    if (surpresaLiberada) return;
 
    const imgData = ctxCover.getImageData(
        0, 0, canvasCover.width, canvasCover.height
    );
 
    let transparentes = 0;
    for (let i = 3; i < imgData.data.length; i += 4) {{
        if (imgData.data[i] < 10) transparentes++;
    }}
 
    const porcentagem = transparentes / (canvasCover.width * canvasCover.height);
 
    if (porcentagem > 0.80) {{
        surpresaLiberada = true;
 
        const botao = document.createElement("button");
        botao.innerText = "✨ Clique para ver sua surpresa ❤️";
        botao.style.display    = "block";
        botao.style.margin     = "20px auto 0";
        botao.style.padding    = "12px 20px";
        botao.style.fontSize   = "16px";
        botao.style.borderRadius = "10px";
        botao.style.cursor     = "pointer";
 
        botao.onclick = () => {{
            window.open('https://diadosnamorados.streamlit.app', '_blank');
        }};
 
        document.body.appendChild(botao);
    }}
}}
 
 
// --- Raspagem: apaga pixels do canvas de cima ---
function raspar(e) {{
    if (!raspando) return;
 
    const pos = getPos(e);
 
    ctxCover.globalCompositeOperation = "destination-out";
    ctxCover.beginPath();
    ctxCover.arc(pos.x, pos.y, 35, 0, Math.PI * 2);
    ctxCover.fill();
 
    verificarProgresso();
}}
 
 
// Eventos de mouse (no canvas de cima)
canvasCover.addEventListener("mousedown",  () => raspando = true);
canvasCover.addEventListener("mouseup",    () => raspando = false);
canvasCover.addEventListener("mouseleave", () => raspando = false);
canvasCover.addEventListener("mousemove",  raspar);
 
// Eventos de toque
canvasCover.addEventListener("touchstart", () => raspando = true);
canvasCover.addEventListener("touchend",   () => raspando = false);
canvasCover.addEventListener("touchmove",  raspar);
 
</script>
 
</body>
</html>
"""
 
st.components.v1.html(html_code, height=500)
 
 
#---------------- Redirecionamento Final --------------------