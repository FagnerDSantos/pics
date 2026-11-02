---
name: cloudflare-security-audit
description: Auditoria de segurança, headers HTTP seguros, prevenção contra vazamento de tokens e validação rigorosa de APIs.
---
# Segurança e Auditoria
- **Headers de Segurança:** Configure `Content-Security-Policy` (CSP), `X-Frame-Options`, `X-Content-Type-Options` e `Strict-Transport-Security`.
- **Validação e Sanitização:** Valide schemas de requisição no backend (zod/pydantic) e sanitize HTML em uploads ou campos de texto.
- **Prevenção de Vazamentos:** Garanta que segredos e `.env` nunca vazem no bundle do cliente.