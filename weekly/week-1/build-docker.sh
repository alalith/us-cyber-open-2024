#!/bin/bash
docker rm -f uscg_web_bobs_zippers
docker build --tag=uscg_web_bobs_zippers .
docker run -p 1337:80 --rm --name=uscg_web_bobs_zippers uscg_web_bobs_zippers