import miniupnpc
import requests
import socket
import subprocess

def abrir_porta_automatica(porta=5050, nome_app="Ruptura_Temporal"):
    print("[Net] Tentando abrir porta automaticamente...")
    ip_publico = None
    upnp = None
    try:
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200
        n = upnp.discover()
        print(f"[Net] {n} dispositivos UPnP/NAT-PMP encontrados.")
        upnp.selectigd()

        ip_local = upnp.lanaddr
        ip_publico = upnp.externalipaddress()

        # Abre a porta via UPnP
        upnp.addportmapping(porta, 'TCP', ip_local, porta, nome_app, '')
        print(f"[Net] Porta {porta} aberta no roteador ({ip_publico} → {ip_local}).")

        # Também adiciona regra no firewall do Windows (caso bloqueie)
        try:
            subprocess.run(
                ["netsh", "advfirewall", "firewall", "add", "rule",
                 f"name={nome_app}", f"dir=in", f"action=allow", f"protocol=TCP", f"localport={porta}"],
                capture_output=True, text=True
            )
            print(f"[Net] Firewall do Windows liberado para a porta {porta}.")
        except Exception as e:
            print("[Net] Falha ao liberar firewall:", e)

        return upnp, ip_publico, porta

    except Exception as e:
        print("[Net] Falha UPnP:", e)
        try:
            ip_publico = requests.get("https://api.ipify.org").text.strip()
            print(f"[Net] Usando IP público detectado: {ip_publico}")
        except Exception as e2:
            print("[Net] Falha ao obter IP público:", e2)
        return upnp, ip_publico, porta


def fechar_porta_automatica(upnp, porta=5050, nome_app="Ruptura_Temporal"):
    if not upnp:
        return
    try:
        upnp.deleteportmapping(porta, 'TCP')
        print(f"[Net] Porta {porta} fechada no roteador.")
    except Exception as e:
        print("[Net] Falha ao fechar porta:", e)

    try:
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "delete", "rule", f"name={nome_app}"],
            capture_output=True, text=True
        )
        print(f"[Net] Regra de firewall removida.")
    except Exception as e:
        print("[Net] Falha ao remover firewall:", e)
print(abrir_porta_automatica(5050))
