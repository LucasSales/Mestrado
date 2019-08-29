FROM openjdk:8-jdk-alpine
ADD sourceafis-lite.jar sourceafis-lite.jar
ADD 8000_fingerprints.data 8000_fingerprints.data
ENTRYPOINT [ "sh", "-c", "java -Djava.security.egd=file:/dev/./urandom -jar /sourceafis-lite.jar 192.168.0.88 5672" ]