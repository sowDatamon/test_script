"""
Runner simple para envíos periódicos de correo.

Cómo funciona:
- Lee configuración desde variables de entorno (ver .env.example).
- Ejecuta un loop en segundo plano que llama a sender.send_email() cada INTERVAL_SECONDS.

Usar: configurar las variables de entorno en PowerShell y ejecutar: python hola.py
"""

import os
import time
import threading
import signal
import sys

from sender import send_email

# Intentar cargar variables desde un archivo .env si python-dotenv está instalado.
try:
	from dotenv import load_dotenv
except Exception:
	load_dotenv = None

if load_dotenv:
	try:
		loaded = load_dotenv()
		if loaded:
			print("[hola] Variables de entorno cargadas desde .env")
	except Exception:
		# No fallar si el archivo .env no existe o hay problemas al cargar
		pass


def periodic_sender(interval_seconds: int, stop_event: threading.Event):
	"""Llama a send_email() cada interval_seconds hasta que stop_event esté seteado."""
	next_run = time.time()
	while not stop_event.is_set():
		now = time.time()
		if now >= next_run:
			try:
				print(f"[hola] Enviando correo automático a las {time.strftime('%Y-%m-%d %H:%M:%S')}")
				send_email()
			except Exception as e:
				print(f"[hola] Error al enviar correo: {e}")
			next_run = now + interval_seconds
		# dormir un poco para ser responsivo al stop_event
		stop_event.wait(0.5)


def main():
	# Intervalo en segundos (por defecto 3600s = 1 hora)
	try:
		interval = int(os.environ.get("INTERVAL_SECONDS", "3600"))
	except ValueError:
		print("INTERVAL_SECONDS mal formado, usando 3600")
		interval = 3600

	stop_event = threading.Event()
	thread = threading.Thread(target=periodic_sender, args=(interval, stop_event), daemon=True)
	thread.start()

	def handle_sigint(signum, frame):
		print("\n[hola] Señal de terminación recibida, deteniendo...")
		stop_event.set()

	signal.signal(signal.SIGINT, handle_sigint)
	signal.signal(signal.SIGTERM, handle_sigint)

	print(f"[hola] Servicio de envío en marcha. Intervalo = {interval} segundos. Presiona Ctrl-C para parar.")
	try:
		while thread.is_alive():
			thread.join(timeout=1.0)
	except KeyboardInterrupt:
		handle_sigint(None, None)


if __name__ == "__main__":
	main()

