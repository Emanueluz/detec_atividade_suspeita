#!/usr/bin/env bash
mvn clean install -U
mvn clean compile assembly:single
cp target/demo-0.0.1-SNAPSHOT-jar-with-dependencies.jar ./demo.jar
sudo docker build -t container-imagem .