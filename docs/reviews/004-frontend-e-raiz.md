# Revisão — Tarefa 004: Frontend e raiz

## Resultado

**Ajustes necessários para fechar todos os critérios de validação.** As mudanças
solicitadas estão implementadas e a tela 004A foi preservada. A conclusão fica
pendente de validações que dependem do estado do ambiente e da decisão sobre as
vulnerabilidades detectadas, sem atualizar dependências fora do escopo aprovado.

## Verificações

| Área | Resultado |
| --- | --- |
| Pacote e lockfile | `pics-frontend`; dependências raiz do lockfile correspondem às declaradas em `frontend/package.json`, sem mudanças de versões. |
| Lint e TypeScript | `npm run lint` e `npm run typecheck` passaram após `npm ci`. |
| Build | `npm run build` passou após pausa autorizada da prévia; a prévia foi reiniciada depois. |
| Auditoria npm | `npm audit --audit-level=high` passa conforme o limiar aprovado por Fagner. Auditoria completa encontrou 16 vulnerabilidades moderadas em dependências de desenvolvimento; `npm audit --omit=dev` encontrou zero. `npm audit fix --dry-run` não ofereceu correção compatível; nenhuma dependência foi alterada. |
| Backend | `ruff check app tests`, `mypy app` passaram; `pytest` passou (8 testes, 1 aviso de depreciação). |
| Compose | YAML do Compose analisado com PyYAML; `docker compose config` não pôde rodar porque Docker CLI não está instalado. Nenhum container/imagem foi iniciado ou baixado. |
| ADRs | ADR-001 a ADR-006 agora correspondem às seis decisões da seção 5 do plano mestre; todos continuam como propostas. |
| Tela 004A | Smoke check local respondeu HTTP 200, `lang=pt-BR` e cabeçalhos de segurança após reiniciar a prévia. Arquivos da interface não foram alterados nesta tarefa. |
| Diff | `git diff --check` passou. |

## Observações

- A primeira tentativa de `npm ci` falhou com `EPERM` porque o servidor mantinha
  um binário nativo aberto. Após autorização para pausar a prévia, `npm ci` passou;
  o servidor foi reiniciado ao fim das verificações.
- `.editorconfig` e `.gitignore` já cobriam os critérios e foram mantidos.
- Os ADRs 001–006 permanecem explicitamente como propostas pendentes, sem aprovar
  decisões ainda não confirmadas.
- O Gitleaks do CI usa a imagem oficial do CLI com versão fixada e redaction, evitando depender da ação comercial licenciada.
- O ambiente bloqueia `git commit`. Não foram executados `git add` ou `git commit`.

## Próximo passo

Validar `docker compose config` quando Docker CLI estiver disponível; depois disso,
fechar a tarefa 004. Os achados moderados em dependências de desenvolvimento
permanecem visíveis na auditoria completa, conforme limiar aprovado.
