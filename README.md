# Textbasierte Prozessanalyse

## Beschreibung

Mithilfe dieser Anwendung und einer kompatiblen Datenbank ist es möglich, eine LDA-Analyse sowie zwei verschiedene
Wörterbuchanalysen durchzuführen.

## Installationsanleitung

Um die Anwendung zu installieren und zu starten, sind bei Vorhandensein dieses Repositories und einer installierten Version von Docker und Docker-Compose
zwei weitere Arbeitsschritte und eine kompatible SQLite-Datenbank notwendig.

#### 1) Die SQLite Datenbank in das richtige Verzeichnis einfügen

Die vorhandene Datenbank muss in den Ordner 
"backend" eingefügt werden, womit das übergeordnete Verzeichnis gemeint ist. Die Datei muss somit 
im gleichen Verzeichnis wie die Datei "manage.py" liegen. 

#### 2) Docker-Container konstruieren und hochfahren

Wurde die Datenbank in das richtige Verzeichnis eingefügt, muss im Terminal im Verzeichnis dieses Repositories (im gleichen
Verzeichnis wie docker-compose.yml) folgender Befehl ausgeführt werden:

```
docker-compose up --build
```

Damit werden sowohl Backend als auch Frontend konstruiert und hochgefahren.

Die Anwendung ist anschließend im Browser unter localhost:3000 erreichbar.

## Wörterbuchanreicherung

Die Anreicherung der Wörterbücher wird über sogenannte Django Management Commands gestartet.
Dazu muss die Anwendung gestartet sein.
Anschließend wird mithilfe des Befehls

```
docker exec -it ma-textb-prozessanalyse-backend bash
```

in den laufenden Docker Container navigiert.
Hier kann nun die Wörterbuchanreicherung gestartet werden.

Emotion:
```
python manage.py enrich_emotion_dictionary
```
Inhalt: 
```
python manage.py enrich_inhalt_dictionary
```

Dabei ist anzumerken, dass als Grundlage jeweils die Dateien woerterbuch_emotion.csv und woerterbuch_inhalt.csv dienen.
Die Dateien müssen entweder überschrieben werden 
oder die Befehle müssen im Code abgeändert werden, damit eine andere Grundlage akzeptiert wird.
