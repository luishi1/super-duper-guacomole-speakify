import os
import sys
import time

# LIBRERÍAS 
import sounddevice as sd
import speech_recognition as sr
import pyttsx3

# CONSOLA
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

console = Console()

def hablar(texto):
    rprint(f"[bold green]🤖 Speakify:[/bold green] {texto}")
    
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()


def escuchar(duracion=4, samplerate=44100):
    rprint("[bold blue]🎤 Escuchando...[/bold blue]")
    
    recording = sd.rec(
        int(duracion * samplerate), 
        samplerate=samplerate, 
        channels=1,
        dtype='int16'
    )
    
    sd.wait()
    rprint("[bold blue]✅ Grabación finalizada.[/bold blue]")
    
    audio_bytes = recording.tobytes()
    
    return sr.AudioData(
        audio_bytes, 
        samplerate, 
        2 
    )


if __name__ == "__main__":
    
    ejecutar = True
    r = sr.Recognizer()
    
    while ejecutar:
        audio = escuchar(duracion=4)
        
        try:
            texto = r.recognize_google(audio, language="es-ES")
            
            hablar(f"Has dicho: {texto}")
            
            if "salir" in texto.lower() or "adiós" in texto.lower() or "terminar" in texto.lower():
                hablar("Hasta luego.")
                ejecutar = False
                
        except sr.UnknownValueError:
            hablar("No entendí lo que dijiste.")
        except sr.RequestError as e:
            hablar("Hubo un problema con el servicio de reconocimiento de voz.")
            rprint(f"[bold red]Error de conexión:[/bold red] {e}")
        
        time.sleep(0.5)