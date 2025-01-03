#!/bin/bash
# Linux/Mac
pid=$(lsof -t -i:8000)
if [ ! -z "$pid" ]; then
    kill $pid
    echo "Service stopped"
else
    echo "Service not running"
fi 