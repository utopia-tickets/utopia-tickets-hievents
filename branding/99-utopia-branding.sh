#!/bin/sh
# Marca de Utopia. El entrypoint de la imagen hace «source» de este fichero en un subshell con set -e:
# por eso todo va en un solo comando que nunca falla. Si la marca no se aplica, la app arranca igual (con su aspecto
# original) y el aviso queda en el log del contenedor.
node /branding/patch.mjs --root /app --branding /branding 2>&1 || echo "[utopia-branding] AVISO: patch.mjs terminó con error; la app arranca sin la marca completa"
true
