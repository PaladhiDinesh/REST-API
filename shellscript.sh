#!/bin/sh
python scrapingnew.py
curl -i -H "Content-Type: application/json" -X POST http://localhost:5000/dailyupdate