# Groupe:
RANIA GUERDOU 

Yoël MAINCENT

# Agent Client Python (Analyse Technique)

##  Description générale

Ce projet est un **agent client écrit en Python** . 
Il met en œuvre plusieurs mécanismes techniques courants tels que :

- Communication réseau via sockets
- Identification unique de la machine
- Journalisation distante
- Chiffrement et déchiffrement de fichiers
- Exécution de commandes à distance

---

# – Serveur de Commande et Contrôle (C2)

##  Description générale

Ce script Python représente la **partie serveur (C2 – Command & Control)** . 
Il permet de :

- Accepter des connexions clientes
- Recevoir des identifiants et des logs distants
- Envoyer des commandes au client
- Gérer des transferts de fichiers
- Centraliser les journaux d’activité

---

## Journalisation serveur – `c2_master.log`

Le fichier **`c2_master.log`** est généré automatiquement par le serveur C2.  
Il contient notamment :

- Les connexions clientes entrantes
- Les identifiants reçus (UUID, clés éventuelles)
- Les journaux distants envoyés par les agents
- Les actions effectuées :
  - Upload
  - Download
  - Commandes exécutées
  - Erreurs rencontrées

Ce fichier permet une **analyse post‑expérimentation** du comportement global du système.

---

## Fichier de test – `TEST12.txt`

Le fichier **`TEST12.txt`** est un fichier de test volontairement simple, utilisé uniquement à des fins expérimentales.  

Il sert à :

- Vérifier le bon fonctionnement du chiffrement et du déchiffrement
- Observer les modifications binaires du contenu
- Tester les commandes `ENCRYPT` et `DECRYPT` sans risque

> Ce fichier n’a aucune valeur fonctionnelle réelle et ne contient aucune donnée sensible.

---

## Objectifs 

Ce projet permet d’acquérir et de consolider des connaissances sur :

- Les bases des architectures **client / serveur**
- La communication réseau **TCP**
- La centralisation et l’analyse des logs
- Les principes du **chiffrement symétrique**
- Le fonctionnement d’un **agent distant contrôlé**
- La séparation des rôles entre client et serveur (C2)

---


##  Dépendances utilisées

```python
import os
import socket
import time


