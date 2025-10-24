import requests

def llamar_app1():
    url = "http://mi-servicio2.ecuaalejo2013-dev.svc.cluster.local:8080"
    try:
        response = requests.get(url)
        print("Respuesta de app1:", response.text)
    except Exception as e:
        print("Error al llamar a app1:", e)

if __name__ == "__main__":
    print("Llamando a app1...")
    llamar_app1()