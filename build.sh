#!/usr/bin/env bash
set -e

apt-get update
apt-get install -y postgresql-client
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
make install
psql -a -d "$DATABASE_URL" -f database.sql
