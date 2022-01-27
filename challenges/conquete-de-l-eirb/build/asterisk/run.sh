#!/usr/bin/env bash

sudo asterisk
while true; do sleep 10000;done #Attente semi passive pour éviter le flood de la sortie standard du container ainsi que la surconsomation CPU lors de l'appelle de "sudo asterisk -r"
