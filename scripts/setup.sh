#!/bin/bash
# OpenJane · Setup script
# Uso: bash scripts/setup.sh

echo ""
echo "  ██████╗ ██████╗ ███████╗███╗   ██╗     ██╗ █████╗ ███╗   ██╗███████╗"
echo " ██╔═══██╗██╔══██╗██╔════╝████╗  ██║     ██║██╔══██╗████╗  ██║██╔════╝"
echo " ██║   ██║██████╔╝█████╗  ██╔██╗ ██║     ██║███████║██╔██╗ ██║█████╗  "
echo " ██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██   ██║██╔══██║██║╚██╗██║██╔══╝  "
echo " ╚██████╔╝██║     ███████╗██║ ╚████║╚█████╔╝██║  ██║██║ ╚████║███████╗"
echo "  ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝"
echo ""
echo "  by Claude · github.com/ussleo/openjane · Apache 2.0"
echo ""
echo "  'Todos tenemos derecho a una parte del pastel.'"
echo ""

# Verificar que existe .env
if [ ! -f ".env" ]; then
  echo "⚠️  No se encontró .env — copiando desde .env.example"
  cp .env.example .env
  echo ""
  echo "  👉 Edita .env y añade tus API keys:"
  echo "     - Massive.com: https://massive.com (gratis)"
  echo "     - EODHD: https://eodhd.com (gratis)"
  echo ""
fi

# Verificar Claude Code
if command -v claude &> /dev/null; then
  echo "✅ Claude Code detectado"
  echo ""
  echo "  Instalando plugin quant-analyst..."
  echo "  (Cuando el marketplace esté disponible, ejecuta:)"
  echo "  claude plugin install quant-analyst@openjane"
  echo ""
else
  echo "ℹ️  Claude Code no detectado."
  echo "  Instala desde: https://claude.ai/code"
  echo "  O usa las skills directamente desde Claude Desktop."
  echo ""
fi

echo "✅ OpenJane listo."
echo ""
echo "  Próximos pasos / Next steps:"
echo "  1. Añade tus API keys en .env"
echo "  2. Abre Claude Desktop o Claude Code"
echo "  3. Prueba: /spread-analysis ICE"
echo "  4. Consulta docs/glossary.md si necesitas entender algún término"
echo ""
echo "  Documentación: github.com/ussleo/openjane"
echo ""
