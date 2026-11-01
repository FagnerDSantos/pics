---
name: gsap-animation-guidelines
description: Boas práticas de animações performáticas na Web com GSAP (GreenSock).
---
# Diretrizes de Animação com GSAP
- Utilize `gsap.context()` ou hooks como `useGSAP` (React) para limpeza e controle de ciclo de vida das animações.
- Anime prioritariamente propriedades de GPU (`transform`, `opacity`, `scale`, `rotate`) para evitar re-layouts pesados.
- Respeite as preferências de movimento reduzido do usuário (`prefers-reduced-motion`).