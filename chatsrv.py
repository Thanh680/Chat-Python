import socket
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("IP", help="Adresse IP sur laquelle le serveur écoute", type=str, default="127.0.0.1")
parser.add_argument("PORT", help="Numéro du port sur lequel le serveur écoute", type=int, default=5555)
parser.add_argument("PROTOCOLE", help="Protocole TCP ou UDP", type=str, default="UDP")
parser.add_argument("LOG", help="Nom d'un fichier de log", type=str, default="chatsrv.log")
args = parser.parse_args()

# Crée une socket datagramme ou TCP
if args.PROTOCOLE == "UDP":
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ouverture d'un fichier de log 
logFile = 0
if args.LOG != "":
                logFile = open( args.LOG, "a" ) ;

# Lier à l'adresse IP et le port
s.bind((args.IP, args.PORT))
print( "Le serveur de chat écoute en mode ", args.PROTOCOLE, " sur l'adresse IP" ,args.IP, " et sur le port n°: ", args.PORT)

# Ecoute les demande de cpnnect
if args.PROTOCOLE == "TCP":
        s.listen(5)

# Écoutez les trame entrantes
boucle = True
spamDetect = ""
counter = 0
while( boucle ):
        if args.PROTOCOLE == "TCP":
                client, adresse = s.accept()
                data = client.recv(1024)
                # Detecter spam
                if spamDetect == str(data):
                        counter+= 1
                else:
                        spamDetect = str(data)
                        counter = 0
                if counter > 5:
                        continue
                print( adresse, ": ", data )

                # Ecrit le message dans le fichier de log
                if logFile != 0:
                        logFile.write( str(adresse) + ": " + str(data) + "\n" )

                client.close()
        else:
                data = s.recvfrom(1024)
                # Detecter spam
                if spamDetect == str(data[0]):
                        counter+= 1
                else:
                        spamDetect = str(data[0])
                        counter = 0
                if counter > 5:
                        continue
                print( data[1], ": ", data[0] )

                # Ecrit le message dans le fichier de log
                if logFile != 0:
                        logFile.write( str(data[1]) + ": " + str(data[0]) + "\n" )
                        logFile.flush()

                # Arret du serveur à distance
                message = str(data[0])
                if message == "b'QUIT'":
                        boucle = False

# Fermeture de la socket
s.close() 

# Fermeture du fichier de log
if logFile != 0:
                logFile.close()

