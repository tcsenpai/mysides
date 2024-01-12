#!/bin/bash
pip install -r requirements.txt
mkdir news
cp .env.example .env
echo "You should now open your .env file and insert your Perplexity API Key."
echo "You can get one at: https://www.perplexity.ai/settings/api"
echo "Then, launch main.py and wait for it to finish."
echo "allsides.html contains an overview of all the news."