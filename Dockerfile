FROM ollama/ollama:latest

ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV NVIDIA_VISIBLE_DEVICES=all

WORKDIR /root

EXPOSE 11434

RUN apt-get update && apt-get install -y curl

COPY <<'EOF' /root/start.sh.tmp
#!/bin/bash
ollama serve &


until curl -s -f http://localhost:11434/api/version >/dev/null 2>&1; do
    echo "Waiting for Ollama to start..."
    sleep 2
done

echo "Ollama is ready. Pulling Qwen model..."
ollama pull qwen2.5:7b

tail -f /dev/null
EOF

RUN tr -d '\r' < /root/start.sh.tmp > /root/start.sh && \
    rm /root/start.sh.tmp && \
    chmod +x /root/start.sh

ENTRYPOINT ["/bin/bash"]
CMD ["/root/start.sh"]


