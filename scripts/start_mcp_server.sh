#!/bin/bash

# Ensure the virtual environment is activated if necessary, then start the server

pm2 start python3 --name "mcp-codegen-server" -- mcp_codegen/server.py

pm2 save

pm2 startup

