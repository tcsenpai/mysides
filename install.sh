#!/bin/bash

pip install -r requirements.txt
cp .env.example .env
echo "You should now open your .env file and insert your Perplexity API Key."
echo "You can get one at: https://www.perplexity.ai/settings/api"
echo "Then, launch main.py and wait for it to finish."
