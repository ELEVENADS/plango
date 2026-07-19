import React from "react";
import { BackgroundDoodle } from "../component/Background";

/* ========== App Mockup — scaled for realistic viewport ========== */
function AppMockup() {
  return (
    <div style={s.mockupCard}>
      <div style={s.mockupHeader}>
        <div style={s.mockupDots}>
          <span style={{ ...s.dot, background: "#ff5f57" }} />
          <span style={{ ...s.dot, background: "#febc2e" }} />
          <span style={{ ...s.dot, background: "#28c840" }} />
        </div>
        <div style={s.mockupSearchBar} />
      </div>
      <div style={s.mockupBody}>
        {/* priority tags */}
        <div style={s.mockupTagRow}>
          <span style={{ ...s.mockupTag, background: "#ff9999" }} />
          <span style={{ ...s.mockupTag, background: "#83ecff", width: 52 }} />
          <span style={{ ...s.mockupTag, background: "#78faa3", width: 38 }} />
        </div>
        {/* task bars */}
        <div style={{ ...s.bar, width: "100%", background: "#78faa3" }} />
        <div style={{ ...s.bar, width: "74%", background: "#9d89fb" }} />
        <div style={{ ...s.bar, width: "82%", background: "#78faa3" }} />
        <div style={{ ...s.bar, width: "45%", background: "#5dff68" }} />
        <div style={{ ...s.bar, width: "68%", background: "#073ef9" }} />
        <div style={{ ...s.bar, width: "56%", background: "#d9d9d9" }} />
        {/* dashboard card */}
        <div style={s.mockupDash}>
          <div style={s.dashHeader}>
            <span style={{ ...s.dashDot, background: "#d5344a" }} />
            <span style={{ ...s.dashDot, background: "#123dfe" }} />
            <span style={{ ...s.dashDot, background: "#b34afb" }} />
          </div>
          <div style={{ ...s.bar, width: "64%", background: "#d9d9d9", marginTop: 12 }} />
          <div style={{ ...s.bar, width: "80%", background: "#a8ffd9", marginTop: 6 }} />
        </div>
        <div style={{ ...s.bar, width: "90%", background: "#5ddfc5", marginTop: 10 }} />
        <div style={{ ...s.bar, width: "40%", background: "#a9c50b", marginTop: 6 }} />
      </div>
    </div>
  );
}

/* ========== Navbar ========== */
function Navbar() {
  return (
    <nav style={s.navbar}>
      <div style={s.navInner}>
        <span style={s.logo}>PLANGO</span>
        <div style={s.navLinks}>
          <a style={s.navLink}>About</a>
          <a style={s.navLink}>Docs</a>
          <a style={s.navCta}>GET START</a>
        </div>
      </div>
    </nav>
  );
}

/* ========== Hero ========== */
function HeroSection() {
  return (
    <section style={s.hero}>
      <div style={s.heroBgOverlay}>
        <BackgroundDoodle />
      </div>

      <div style={s.heroContent}>
        <p style={s.heroEyebrow}>AI-POWERED SCHEDULE ASSISTANT</p>
        <h1 style={s.heroTitle}>PlanGoDaily</h1>
        <p style={s.heroSubtitle}>打造你的私人日程规划助手，让每一天都井井有条</p>
        <div style={s.heroActions}>
          <button style={s.ctaPrimary}>GET START</button>
          <button style={s.ctaSecondary}>了解更多</button>
        </div>
      </div>

      <div style={s.heroMockup}>
        <AppMockup />
      </div>
    </section>
  );
}

/* ========== Feature Highlights ========== */
const features = [
  { icon: "🎯", title: "智能规划", desc: "AI 理解你的习惯，自动生成个性化日程安排" },
  { icon: "🔔", title: "实时提醒", desc: "多端同步推送，重要事项不错过" },
  { icon: "📊", title: "数据洞察", desc: "可视化你的时间分配，持续优化效率" },
];

function FeaturesSection() {
  return (
    <section style={s.features}>
      <div style={s.sectionHeader}>
        <h2 style={s.sectionTitle}>为什么选择 PlanGoDaily</h2>
        <p style={s.sectionDesc}>不只是计划工具，更是你的私人效率顾问</p>
      </div>
      <div style={s.featureGrid}>
        {features.map((f) => (
          <div key={f.title} style={s.featureCard}>
            <span style={s.featureIcon}>{f.icon}</span>
            <h3 style={s.featureTitle}>{f.title}</h3>
            <p style={s.featureDesc}>{f.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

/* ========== Preview Section ========== */
function PreviewSection() {
  return (
    <section style={s.preview}>
      <div style={s.sectionHeader}>
        <h2 style={s.sectionTitle}>简洁直观的操作界面</h2>
        <p style={s.sectionDesc}>一目了然的日历视图，拖拽即可调整计划</p>
      </div>
      <div style={s.previewCard}>
        <svg width="100%" height="100%" viewBox="0 0 878 460" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="878" height="460" rx="12" fill="#0d1117" />
          {/* header */}
          <rect x="28" y="24" width="822" height="32" rx="8" fill="#161b22" />
          <circle cx="48" cy="40" r="8" fill="#30363d" />
          <rect x="68" y="33" width="160" height="14" rx="4" fill="#30363d" />
          {/* sidebar */}
          <rect x="28" y="72" width="180" height="364" rx="8" fill="#161b22" />
          <rect x="44" y="92" width="148" height="10" rx="4" fill="#21262d" />
          <rect x="44" y="114" width="120" height="10" rx="4" fill="#21262d" />
          <rect x="44" y="136" width="140" height="10" rx="4" fill="#21262d" />
          <rect x="44" y="166" width="100" height="10" rx="4" fill="#1f6feb" />
          <rect x="44" y="188" width="130" height="10" rx="4" fill="#21262d" />
          {/* main area */}
          <rect x="224" y="72" width="626" height="364" rx="8" fill="#161b22" />
          {/* calendar grid */}
          {[0, 1, 2, 3].map((row) =>
            [0, 1, 2, 3, 4, 5, 6].map((col) => (
              <rect
                key={`${row}-${col}`}
                x={244 + col * 88}
                y={92 + row * 78}
                width={78}
                height={68}
                rx="6"
                fill={row === 1 && col === 2 ? "#1f6feb" : row === 2 && col === 4 ? "rgba(31,111,235,0.15)" : "#0d1117"}
                stroke={row === 1 && col === 2 ? "#1f6feb" : "rgba(48,54,61,0.5)"}
                strokeWidth="1"
              />
            ))
          )}
          {/* day labels */}
          {["一","二","三","四","五","六","日"].map((d, i) => (
            <text key={d} x={283 + i * 88} y={86} fill="#8b949e" fontSize="11" textAnchor="middle" fontFamily="Inter,sans-serif">{d}</text>
          ))}
          {/* event dots */}
          <circle cx={283} cy={138} r="3" fill="#f78166" />
          <circle cx="459" cy="138" r="3" fill="#f78166" />
          <circle cx="547" cy="216" r="3" fill="#7ee787" />
          <circle cx="371" cy="294" r="3" fill="#f78166" />
          <circle cx="459" cy="294" r="3" fill="#a371f7" />
          {/* bottom stats */}
          <rect x="244" y="400" width="140" height="8" rx="4" fill="#f78166" />
          <rect x="400" y="400" width="90" height="8" rx="4" fill="#21262d" />
          <rect x="506" y="400" width="70" height="8" rx="4" fill="#7ee787" />
        </svg>
      </div>
    </section>
  );
}

/* ========== Footer ========== */
function Footer() {
  return (
    <footer style={s.footer}>
      <div style={s.footerInner}>
        <div style={s.footerBrand}>
          <span style={s.footerLogo}>PLANGO</span>
          <span style={s.footerTagline}>Smart scheduling, better living.</span>
        </div>
        <div style={s.footerLinks}>
          <div style={s.footerCol}>
            <span style={s.footerColTitle}>Product</span>
            <a style={s.footerLink}>Features</a>
            <a style={s.footerLink}>Pricing</a>
            <a style={s.footerLink}>Changelog</a>
          </div>
          <div style={s.footerCol}>
            <span style={s.footerColTitle}>Resources</span>
            <a style={s.footerLink}>Docs</a>
            <a style={s.footerLink}>API</a>
            <a style={s.footerLink}>Blog</a>
          </div>
          <div style={s.footerCol}>
            <span style={s.footerColTitle}>Company</span>
            <a style={s.footerLink}>About</a>
            <a style={s.footerLink}>Contact</a>
            <a style={s.footerLink}>Privacy</a>
          </div>
        </div>
      </div>
      <div style={s.footerBottom}>
        <span>© 2025 PlanGoDaily. All rights reserved.</span>
      </div>
    </footer>
  );
}

/* ========== Portal Page ========== */
export default function PortalPage() {
  return (
    <div style={s.page}>
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <PreviewSection />
      <Footer />
    </div>
  );
}

/* ========== Styles ========== */
const s: Record<string, React.CSSProperties> = {
  page: {
    width: "100%",
    background: "#08080a",
    color: "#e6e6e6",
    fontFamily: "Inter, system-ui, -apple-system, sans-serif",
    overflowX: "hidden",
  },

  /* ---- Navbar ---- */
  navbar: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    zIndex: 100,
    height: 64,
    background: "rgba(8,8,10,0.85)",
    backdropFilter: "blur(16px)",
    WebkitBackdropFilter: "blur(16px)",
    borderBottom: "1px solid rgba(255,255,255,0.06)",
  },
  navInner: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    height: "100%",
    maxWidth: 1200,
    margin: "0 auto",
    padding: "0 48px",
  },
  logo: {
    fontSize: 20,
    fontWeight: 700,
    color: "#fff",
    letterSpacing: 3,
  },
  navLinks: {
    display: "flex",
    alignItems: "center",
    gap: 32,
  },
  navLink: {
    fontSize: 15,
    fontWeight: 400,
    color: "rgba(255,255,255,0.7)",
    cursor: "pointer",
    textDecoration: "none",
  },
  navCta: {
    fontSize: 14,
    fontWeight: 600,
    color: "#000",
    background: "#d9d9d9",
    padding: "8px 20px",
    borderRadius: 20,
    cursor: "pointer",
    textDecoration: "none",
    transition: "background 150ms ease-out",
  },

  /* ---- Hero ---- */
  hero: {
    position: "relative",
    width: "100%",
    minHeight: 560,
    marginTop: 64,
    overflow: "hidden",
    background: "linear-gradient(160deg, #0c0c10 0%, #14141c 40%, #1a1a24 100%)",
    display: "flex",
    alignItems: "center",
  },
  heroBgOverlay: {
    position: "absolute",
    inset: 0,
    opacity: 0.18,
    zIndex: 1,
    overflow: "hidden",
  },
  heroContent: {
    position: "relative",
    zIndex: 10,
    flex: "0 0 50%",
    paddingLeft: "max(48px, calc((100vw - 1200px) / 2 + 48px))",
    paddingRight: 48,
  },
  heroEyebrow: {
    fontSize: 12,
    fontWeight: 600,
    color: "rgba(255,255,255,0.4)",
    letterSpacing: 4,
    textTransform: "uppercase",
    margin: 0,
  },
  heroTitle: {
    fontSize: 48,
    fontWeight: 700,
    color: "#fff",
    margin: "12px 0 16px",
    lineHeight: 1.1,
    letterSpacing: -1,
  },
  heroSubtitle: {
    fontSize: 18,
    fontWeight: 400,
    color: "rgba(255,255,255,0.55)",
    margin: "0 0 32px",
    lineHeight: 1.6,
    maxWidth: 420,
  },
  heroActions: {
    display: "flex",
    gap: 16,
    alignItems: "center",
  },
  ctaPrimary: {
    height: 48,
    padding: "0 32px",
    borderRadius: 24,
    border: "none",
    background: "#d9d9d9",
    color: "#000",
    fontSize: 15,
    fontWeight: 600,
    cursor: "pointer",
    fontFamily: "Inter, system-ui, sans-serif",
    letterSpacing: 0.5,
    transition: "transform 150ms ease-out, box-shadow 150ms ease-out",
    boxShadow: "0 2px 12px rgba(217,217,217,0.15)",
  },
  ctaSecondary: {
    height: 48,
    padding: "0 32px",
    borderRadius: 24,
    border: "1px solid rgba(255,255,255,0.15)",
    background: "transparent",
    color: "rgba(255,255,255,0.75)",
    fontSize: 15,
    fontWeight: 500,
    cursor: "pointer",
    fontFamily: "Inter, system-ui, sans-serif",
    transition: "border-color 150ms ease-out",
  },
  heroMockup: {
    position: "relative",
    zIndex: 10,
    flex: "0 0 50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    paddingRight: "max(48px, calc((100vw - 1200px) / 2 + 48px))",
    paddingLeft: 24,
  },

  /* ---- Mockup ---- */
  mockupCard: {
    width: "100%",
    maxWidth: 440,
    background: "rgba(22,22,30,0.85)",
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.08)",
    padding: 20,
    boxShadow: "0 8px 40px rgba(0,0,0,0.4)",
    backdropFilter: "blur(8px)",
    WebkitBackdropFilter: "blur(8px)",
  },
  mockupHeader: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    marginBottom: 16,
  },
  mockupDots: {
    display: "flex",
    gap: 6,
    flexShrink: 0,
  },
  dot: {
    width: 10,
    height: 10,
    borderRadius: "50%",
    display: "inline-block",
  },
  mockupSearchBar: {
    flex: 1,
    height: 26,
    backgroundColor: "rgba(255,255,255,0.08)",
    borderRadius: 6,
  },
  mockupBody: {
    display: "flex",
    flexDirection: "column",
    gap: 0,
  } as React.CSSProperties,
  mockupTagRow: {
    display: "flex",
    gap: 8,
    marginBottom: 12,
  },
  mockupTag: {
    height: 7,
    borderRadius: 4,
    width: 28,
    display: "inline-block",
  },
  bar: {
    height: 8,
    borderRadius: 4,
    marginTop: 7,
  } as React.CSSProperties,
  mockupDash: {
    marginTop: 10,
    padding: 14,
    background: "rgba(255,255,255,0.03)",
    borderRadius: 10,
    border: "1px solid rgba(255,255,255,0.04)",
  },
  dashHeader: {
    display: "flex",
    gap: 6,
    justifyContent: "flex-end",
  },
  dashDot: {
    width: 26,
    height: 8,
    borderRadius: 4,
    display: "inline-block",
  },

  /* ---- Features ---- */
  features: {
    padding: "100px 48px",
    maxWidth: 1200,
    margin: "0 auto",
  },
  sectionHeader: {
    textAlign: "center",
    marginBottom: 56,
  },
  sectionTitle: {
    fontSize: 28,
    fontWeight: 700,
    color: "#fff",
    margin: "0 0 12px",
    letterSpacing: -0.5,
  },
  sectionDesc: {
    fontSize: 16,
    fontWeight: 400,
    color: "rgba(255,255,255,0.4)",
    margin: 0,
  },
  featureGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: 24,
  },
  featureCard: {
    background: "rgba(255,255,255,0.02)",
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.06)",
    padding: "36px 28px",
    transition: "border-color 200ms ease-out, transform 200ms ease-out",
  },
  featureIcon: {
    fontSize: 32,
    display: "block",
    marginBottom: 16,
  },
  featureTitle: {
    fontSize: 17,
    fontWeight: 600,
    color: "#fff",
    margin: "0 0 8px",
  },
  featureDesc: {
    fontSize: 14,
    fontWeight: 400,
    color: "rgba(255,255,255,0.45)",
    margin: 0,
    lineHeight: 1.6,
  },

  /* ---- Preview ---- */
  preview: {
    padding: "0 48px 100px",
    maxWidth: 1200,
    margin: "0 auto",
  },
  previewCard: {
    width: "100%",
    maxWidth: 878,
    margin: "0 auto",
    borderRadius: 12,
    overflow: "hidden",
    boxShadow: "0 4px 32px rgba(0,0,0,0.5)",
    border: "1px solid rgba(255,255,255,0.06)",
  },

  /* ---- Footer ---- */
  footer: {
    borderTop: "1px solid rgba(255,255,255,0.05)",
    background: "#060608",
  },
  footerInner: {
    maxWidth: 1200,
    margin: "0 auto",
    padding: "64px 48px 40px",
    display: "flex",
    justifyContent: "space-between",
  },
  footerBrand: {
    display: "flex",
    flexDirection: "column",
    gap: 8,
  },
  footerLogo: {
    fontSize: 20,
    fontWeight: 700,
    color: "rgba(255,255,255,0.5)",
    letterSpacing: 3,
  },
  footerTagline: {
    fontSize: 13,
    color: "rgba(255,255,255,0.25)",
  },
  footerLinks: {
    display: "flex",
    gap: 64,
  },
  footerCol: {
    display: "flex",
    flexDirection: "column",
    gap: 10,
  } as React.CSSProperties,
  footerColTitle: {
    fontSize: 13,
    fontWeight: 600,
    color: "rgba(255,255,255,0.5)",
    marginBottom: 4,
  },
  footerLink: {
    fontSize: 13,
    color: "rgba(255,255,255,0.3)",
    cursor: "pointer",
    textDecoration: "none",
  },
  footerBottom: {
    borderTop: "1px solid rgba(255,255,255,0.04)",
    padding: "20px 48px",
    maxWidth: 1200,
    margin: "0 auto",
    fontSize: 12,
    color: "rgba(255,255,255,0.2)",
  },
};
