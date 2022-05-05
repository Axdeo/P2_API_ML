#!/bin/bash
docker image build ./prediction -t api_pred_test:latest
docker image build ./authentication -t api_auth_test:latest
docker image build ./authorization -t api_autho_test:latest
docker-compose up
