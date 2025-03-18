#!/bin/sh
ollama serve &
sleep 10
ollama pull deepseek-r1:7b
wait