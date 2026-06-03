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

<div style="display:flex;justify-content:center;">
<canvas id="canvas"
width="600"
height="400"
style="
border-radius:20px;
touch-action:none;
cursor:pointer;
"></canvas>
</div>

<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const foto = new Image();
const cover = new Image();

let raspando = false;
let surpresaLiberada = false;

foto.onload = () => {{

    cover.onload = () => {{

        // desenha a foto secreta primeiro
        ctx.drawImage(
            foto,
            0,
            0,
            canvas.width,
            canvas.height
        );

        // desenha a cobertura por cima
        ctx.drawImage(
            cover,
            0,
            0,
            canvas.width,
            canvas.height
        );

    }};

    cover.src = "data:image/jpeg;base64,{cover}";
}};

foto.src = "data:image/jpeg;base64,{foto}";


function getPos(e) {{
    const rect = canvas.getBoundingClientRect();

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


function verificarProgresso() {{

    if (surpresaLiberada) return;

    const imgData = ctx.getImageData(
        0,
        0,
        canvas.width,
        canvas.height
    );

    let transparentes = 0;

    for (let i = 3; i < imgData.data.length; i += 4) {{
        if (imgData.data[i] < 10) {{
            transparentes++;
        }}
    }}

    const porcentagem = transparentes / (canvas.width * canvas.height);

    if (porcentagem > 0.80) {{

    surpresaLiberada = true;

    const botao = document.createElement("button");

    botao.innerText = "✨ Clique para ver sua surpresa ❤️";
    botao.style.padding = "12px 20px";
    botao.style.fontSize = "16px";
    botao.style.marginTop = "20px";
    botao.style.borderRadius = "10px";
    botao.style.cursor = "pointer";

    botao.onclick = () => {{
        window.location.href = "https://diadosnamorados.streamlit.app";
    }};

    document.body.appendChild(botao);
}}

function raspar(e) {{

    if (!raspando) return;

    const pos = getPos(e);

    ctx.globalCompositeOperation = "destination-out";

    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 35, 0, Math.PI * 2);
    ctx.fill();

    verificarProgresso();
}}


// eventos mouse
canvas.addEventListener("mousedown", () => raspando = true);
canvas.addEventListener("mouseup", () => raspando = false);
canvas.addEventListener("mouseleave", () => raspando = false);
canvas.addEventListener("mousemove", raspar);

// eventos touch
canvas.addEventListener("touchstart", () => raspando = true);
canvas.addEventListener("touchend", () => raspando = false);
canvas.addEventListener("touchmove", raspar);

</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=500)


#---------------- Redirecionamento Final --------------------
