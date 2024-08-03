#!/bin/bash
docker rm -f s4_web_cat_gpt
docker build --tag=s4_web_cat_gpt .
docker run -p 1337:1337 --rm --name=s4_web_cat_gpt s4_web_cat_gpt