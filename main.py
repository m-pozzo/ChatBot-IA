import streamlit as st
from groq import Groq

st.set_page_config(page_title="CHATBOT IA", page_icon="🎃")
st.title("Sitio con python")

nombre = st.text_input("¿Cómo te llamas máquina?")

#Boton con funcionalidad
if st.button("Saludar"):
    if nombre:
        st.write(f"Hola {nombre}")
    
MODELO = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]

#Conecta el sitio a la API
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_secreta) #crea el usuario
       
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [
            {
            "role":"user", 
            "content": mensajeDeEntrada
            }
        ],
        stream = True
    )
   
#historial de mensaje
def inicializar_estado(): #Simula un historial de mensajes
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #Memoria de mensajes
    
    
def actualizar_historial(rol, contenido, avatar):
       #El metodo append() agrega un elemento a una lista
       st.session_state.mensajes.append(
           {"role": rol, "content": contenido, "avatar": avatar}
       )
       
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]) : st.markdown(mensaje["content"])
        
#Contenedor del chat 
def area_chat():
       contenedorDelChat = st.container(height=300, border=True)
       with contenedorDelChat : mostrar_historial()
       
def configurar_sitio():
    st.title("Chatbot !!! :)")
    st.sidebar.title("Configuración")
    seleccion = st.sidebar.selectbox(
        "Elegí un modelo",
        MODELO,
        index = 1
    )
    return seleccion
    
def generar_respuestas(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content  
    return respuesta_completa
 
 
def main():  #Funcion principal
    modelo = configurar_sitio()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat() #se crea el sector para ver los msjs

    mensaje = st.chat_input("Ingrese su mensaje aquí...")
    st.write(f"El modelo elegido es: {modelo}")

    #Verifica si el mensaje tiene contenido
    if mensaje:
        actualizar_historial("user", mensaje, "😛")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant") : 
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "💻")
                st.rerun()
                
#Indica que nuestra funcion principal es main()                
if __name__ == "__main__":
    main()