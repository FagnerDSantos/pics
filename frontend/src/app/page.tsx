type IconName = "overview" | "gallery" | "album" | "clients" | "settings" | "search" | "bell" | "arrow" | "photos" | "clock" | "more";

const iconPaths: Record<IconName, string> = {
  overview: "M3 3h8v8H3zM13 3h8v5h-8zM13 10h8v11h-8zM3 13h8v8H3z",
  gallery: "M3 5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM8.5 10a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM21 15l-5-5L5 21",
  album: "M4 4h16v16H4zM9 4v16M9 8h11M9 12h11M9 16h11",
  clients: "M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M10 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM20 8v6M23 11h-6",
  settings: "M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8ZM19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-1.6 2.8-.2-.1a1.7 1.7 0 0 0-1.9.3l-.1.1h-3.2l-.1-.2a1.7 1.7 0 0 0-1.5-1 1.7 1.7 0 0 0-1.5 1l-.1.2H6.4l-.1-.1a1.7 1.7 0 0 0-1.9-.3l-.2.1-1.6-2.8.1-.1A1.7 1.7 0 0 0 3 15l-.1-.2v-3.2L3 11.5a1.7 1.7 0 0 0-.3-1.9l-.1-.1 1.6-2.8.2.1a1.7 1.7 0 0 0 1.9-.3l.1-.1h3.2l.1.2a1.7 1.7 0 0 0 1.5 1 1.7 1.7 0 0 0 1.5-1l.1-.2h3.2l.1.1a1.7 1.7 0 0 0 1.9.3l.2-.1 1.6 2.8-.1.1a1.7 1.7 0 0 0-.3 1.9l.1.2v3.2z",
  search: "m20 20-4.5-4.5M18 10.5a7.5 7.5 0 1 1-15 0 7.5 7.5 0 0 1 15 0Z",
  bell: "M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9ZM10 21h4",
  arrow: "M5 12h14M13 6l6 6-6 6",
  photos: "M4 4h16v16H4zM8 9h.01M4 16l5-5 4 4 3-3 4 4",
  clock: "M12 8v4l3 2M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z",
  more: "M5 12h.01M12 12h.01M19 12h.01",
};

function Icon({ name, size = 20 }: { name: IconName; size?: number }) {
  return (
    <svg aria-hidden="true" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
      <path d={iconPaths[name]} />
    </svg>
  );
}

const navigation: { label: string; icon: IconName; href: string; active?: boolean }[] = [
  { label: "Visão geral", icon: "overview", href: "#inicio", active: true },
  { label: "Galerias", icon: "gallery", href: "#galerias" },
  { label: "Atividade", icon: "clock", href: "#atividade" },
  { label: "Sobre", icon: "clients", href: "#sobre" },
];

const galleries = [
  { title: "Luz de outono", client: "Marina & Caio", date: "18 out, 2026", count: "128 fotos", style: "autumn", status: "Em seleção", tone: "warm" },
  { title: "Jardim ao entardecer", client: "Estúdio Aurora", date: "16 out, 2026", count: "86 fotos", style: "garden", status: "Prévia pronta", tone: "green" },
  { title: "Pequenos momentos", client: "Família Nogueira", date: "12 out, 2026", count: "64 fotos", style: "soft", status: "Em seleção", tone: "lavender" },
];

export default function Home() {
  return (
    <div className="dashboard-shell">
      <a className="skip-link" href="#main-content">Pular para o conteúdo principal</a>
      <aside className="sidebar" aria-label="Navegação principal">
        <a className="brand" href="#inicio" aria-label="Pics, início">
          <span className="brand-mark" aria-hidden="true"><span /></span>
          <span className="brand-name">pics<span>.</span></span>
        </a>

        <div className="workspace-label">ESPAÇO DE TRABALHO</div>
        <nav className="main-nav" aria-label="Navegação do espaço de trabalho">
          {navigation.map((item) => (
            <a key={item.label} className={`nav-link${item.active ? " is-active" : ""}`} href={item.href} aria-current={item.active ? "page" : undefined}>
              <Icon name={item.icon} size={19} /><span>{item.label}</span>
              {item.label === "Galerias" && <span className="nav-count">8</span>}
            </a>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="profile-card">
            <div className="avatar avatar-owner" aria-hidden="true">A</div>
            <div className="profile-copy"><strong>Ateliê Aurora</strong><span>Plano demonstrativo</span></div>
            <span className="profile-more" aria-hidden="true"><Icon name="more" size={19} /></span>
          </div>
        </div>
      </aside>

      <main className="main-content" id="main-content" tabIndex={-1}>
        <header className="topbar" id="inicio">
          <div className="breadcrumb"><span>Painel</span><span className="breadcrumb-divider">/</span><strong>Visão geral</strong></div>
          <div className="topbar-actions">
            <span className="demo-pill"><span /> Prévia demonstrativa</span>
            <span className="topbar-divider" aria-hidden="true" />
            <a className="icon-link" href="#atividade" aria-label="Ver atividade recente"><Icon name="bell" size={19} /><span className="notification-dot" /></a>
            <div className="avatar avatar-top" aria-hidden="true">A</div>
          </div>
        </header>

        <div className="page-wrap">
          <section className="welcome-section" aria-labelledby="welcome-title">
            <div>
              <p className="eyebrow">DOMINGO, 1 DE NOVEMBRO DE 2026</p>
              <h1 id="welcome-title">Um espaço para suas histórias<span>.</span></h1>
              <p className="welcome-copy">Acompanhe suas galerias e transforme momentos em lembranças.</p>
            </div>
            <div className="welcome-note"><span className="note-sparkle" aria-hidden="true">✳</span><span>Uma prévia visual do painel Pics.<br /><strong>Nenhuma ação está conectada.</strong></span></div>
          </section>

          <section className="metrics-grid" aria-label="Resumo demonstrativo">
            <article className="metric-card">
              <div className="metric-top"><span>Galerias no espaço</span><span className="metric-icon icon-lilac"><Icon name="gallery" size={18} /></span></div>
              <div className="metric-value">08</div><p><span className="metric-muted">3</span> em andamento <span className="metric-separator">·</span> dados fictícios</p>
            </article>
            <article className="metric-card">
              <div className="metric-top"><span>Fotos organizadas</span><span className="metric-icon icon-peach"><Icon name="photos" size={18} /></span></div>
              <div className="metric-value">1.284</div><p>nas galerias demonstrativas</p>
            </article>
            <article className="metric-card">
              <div className="metric-top"><span>Seleções recebidas</span><span className="metric-icon icon-mint"><Icon name="album" size={18} /></span></div>
              <div className="metric-value">12</div><p>número ilustrativo</p>
            </article>
            <article className="metric-card metric-deadline">
              <div className="metric-top"><span>Prévia expira em breve</span><span className="metric-icon icon-sand"><Icon name="clock" size={18} /></span></div>
              <div className="metric-value">02 <small>dias</small></div><p>prazo apenas demonstrativo</p>
            </article>
          </section>

          <section className="galleries-section" id="galerias" aria-labelledby="galleries-title">
            <div className="section-heading">
              <div><p className="eyebrow">SEU ACERVO</p><h2 id="galleries-title">Galerias recentes</h2><p className="section-subtitle">Histórias fictícias para ilustrar a experiência.</p></div>
              <span className="gallery-count">3 exemplos</span>
            </div>

            <div className="gallery-grid">
              {galleries.map((gallery) => (
                <article className="gallery-card" key={gallery.title}>
                  <div className={`gallery-art art-${gallery.style}`} aria-hidden="true">
                    <span className="art-orb" /><span className="art-shape art-shape-one" /><span className="art-shape art-shape-two" /><span className="art-line" />
                    <span className="art-caption">P I C S <i>•</i> ESTUDO VISUAL</span>
                    <span className={`status-tag status-${gallery.tone}`}><span />{gallery.status}</span>
                  </div>
                  <div className="gallery-info">
                    <div className="gallery-title-row"><div><h3>{gallery.title}</h3><p>{gallery.client}</p></div><span className="card-more" aria-hidden="true"><Icon name="more" size={18} /></span></div>
                    <div className="gallery-meta"><span><Icon name="photos" size={15} />{gallery.count}</span><span className="meta-dot" /><span>{gallery.date}</span></div>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <div className="lower-grid">
            <section className="activity-card" id="atividade" aria-labelledby="activity-title">
              <div className="compact-heading"><div><p className="eyebrow">ACOMPANHAMENTO</p><h2 id="activity-title">Atividade recente</h2></div><span className="demo-label">FICTÍCIO</span></div>
              <div className="activity-list">
                <div className="activity-item"><span className="activity-symbol activity-lilac"><Icon name="gallery" size={17} /></span><div><p><strong>Jardim ao entardecer</strong> foi criada</p><span>Há 2 horas <i>·</i> demonstração</span></div></div>
                <div className="activity-item"><span className="activity-symbol activity-peach"><Icon name="album" size={17} /></span><div><p>Seleção ilustrativa recebida em <strong>Luz de outono</strong></p><span>Ontem <i>·</i> demonstração</span></div></div>
                <div className="activity-item"><span className="activity-symbol activity-mint"><Icon name="clients" size={17} /></span><div><p><strong>Família Nogueira</strong> adicionada como cliente</p><span>28 out, 2026 <i>·</i> demonstração</span></div></div>
              </div>
            </section>

            <aside className="preview-card" id="sobre" aria-labelledby="preview-title">
              <div className="preview-decoration" aria-hidden="true"><span /><span /><span /></div>
              <p className="eyebrow">FEITO PARA GUARDAR</p>
              <h2 id="preview-title">Cada história merece seu próprio espaço.</h2>
              <p>Organize, compartilhe e transforme suas imagens em álbuns cheios de significado.</p>
              <span className="preview-footnote">Prévia conceitual · funcionalidades indisponíveis</span>
            </aside>
          </div>

          <footer className="page-footer"><span>© 2026 Pics <i>·</i> conceito demonstrativo</span><span>Feito com cuidado, para boas histórias.</span></footer>
        </div>
      </main>
    </div>
  );
}
