#!/bin/sh
# Crea .env con secretos nuevos (si no existe) a partir de env.template y arranca.
# Ejecútalo en la carpeta de instalación, donde están docker-compose.yml, env.template y branding/.
set -eu
cd "$(dirname "$0")"
[ -f branding/patch.mjs ] || { echo "falta branding/ junto al docker-compose.yml"; exit 1; }
umask 077
if [ ! -f .env ]; then
  K=$(python3 -c 'import secrets,base64;print(base64.b64encode(secrets.token_bytes(32)).decode())')
  J=$(python3 -c 'import secrets,base64;print(base64.b64encode(secrets.token_bytes(32)).decode())')
  P=$(python3 -c 'import secrets;print(secrets.token_hex(24))')
  sed -e "s|__APP_KEY__|base64:$K|" -e "s|__JWT_SECRET__|$J|" -e "s|__PG_PASSWORD__|$P|" env.template > .env
fi
chmod 600 .env
if grep -q '__STRIPE_' .env; then echo "aviso: faltan las claves de Stripe en .env"; fi
if grep -v '__STRIPE_' .env | grep -q '__'; then echo "quedan marcadores en .env"; exit 1; fi
docker compose pull -q
docker compose up -d
