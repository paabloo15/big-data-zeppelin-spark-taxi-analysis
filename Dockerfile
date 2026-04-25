FROM apache/zeppelin:0.11.1
USER root
RUN find /opt/zeppelin/interpreter -name '._*' -delete