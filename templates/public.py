"""
Public Views: Homepage, 16 Solutions Catalog, Tailored Scope Discovery
"""
from typing import List
from templates.base import render_public_base

def render_home(systems: List[dict]) -> str:
    hero = """
    <div style="background: linear-gradient(135deg, #0B1120 0%, #0F172A 50%, #1E293B 100%); color: #FFFFFF; padding: 90px 0; border-bottom: 3px solid var(--z-gold);">
      <div class="container" style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 60px; align-items: center;">
        <div>
          <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(197,155,39,0.15); border: 1px solid var(--z-gold); padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; color: var(--z-gold); margin-bottom: 24px;">
            <span>★</span> ENTERPRISE BUSINESS TRANSFORMATION &bull; KAMPALA, UGANDA
          </div>
          <h1 style="font-size: 44px; font-weight: 900; line-height: 1.15; margin-bottom: 20px;">
            Building Better Businesses. <span style="color: var(--z-gold);">Together.</span>
          </h1>
          <p style="font-size: 16px; color: #CBD5E1; line-height: 1.7; margin-bottom: 32px; max-width: 580px;">
            We engineer integrated digital backbones for African enterprises. From ERPNext rollouts and PostgreSQL analytics to business process re-engineering and executive governance.
          </p>
          <div style="display: flex; gap: 16px; align-items: center;">
            <a href="/tailored-scope" class="btn btn-gold" style="font-size: 15px; padding: 12px 24px;">Request Solution Scoping &rarr;</a>
            <a href="/systems" class="btn btn-navy" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.2); font-size: 15px; padding: 12px 24px;">Explore 16 Systems</a>
          </div>
        </div>

        <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; padding: 32px; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
          <div style="font-size: 12px; font-weight: 800; color: var(--z-gold); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">Institutional Transformation Delivery</div>
          <h3 style="font-size: 20px; font-weight: 800; color: #FFFFFF; margin-bottom: 20px;">Enterprise Scoping Standard</h3>
          <div style="display: flex; flex-direction: column; gap: 16px;">
            <div style="display: flex; gap: 14px;">
              <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(197,155,39,0.2); color: var(--z-gold); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px;">1</div>
              <div>
                <div style="font-weight: 700; color: #FFFFFF; font-size: 14px;">Deep Discovery & Gap Analysis</div>
                <div style="color: #94A3B8; font-size: 12.5px;">Mapping legacy workflows, SOPs, and chart of accounts.</div>
              </div>
            </div>
            <div style="display: flex; gap: 14px;">
              <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(197,155,39,0.2); color: var(--z-gold); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px;">2</div>
              <div>
                <div style="font-weight: 700; color: #FFFFFF; font-size: 14px;">Tailored Architecture Engineering</div>
                <div style="color: #94A3B8; font-size: 12.5px;">Zero cookie-cutter pricing: scoped to your actual scale and integration depth.</div>
              </div>
            </div>
            <div style="display: flex; gap: 14px;">
              <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(197,155,39,0.2); color: var(--z-gold); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px;">3</div>
              <div>
                <div style="font-weight: 700; color: #FFFFFF; font-size: 14px;">Continuous SLA & Local Support</div>
                <div style="color: #94A3B8; font-size: 12.5px;">On-the-ground support team based in Kampala with SMS notifications.</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """

    system_cards = ""
    for s in systems[:6]:
        feats = "".join([f"<li style='margin-bottom: 6px; font-size: 13px; color: #475569;'>✓ {f}</li>" for f in s.get('features', [])[:3]])
        system_cards += f"""
        <div class="z-card">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
            <span class="z-badge">{s.get('pillar')}</span>
            <span class="badge badge-gold">{s.get('tier')}</span>
          </div>
          <div class="z-title">{s.get('name')}</div>
          <div class="z-desc">{s.get('description')}</div>
          <ul style="list-style: none; margin-bottom: 20px;">
            {feats}
          </ul>
          <div style="margin-top: auto; border-top: 1px solid var(--z-border); padding-top: 14px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 12px; font-weight: 700; color: var(--z-gold); text-transform: uppercase;">Tailored Scope</span>
            <a href="/tailored-scope?system={s.get('code')}" style="color: var(--z-navy); font-size: 13px; font-weight: 700;">Inquire &rarr;</a>
          </div>
        </div>
        """

    content = f"""
    {hero}
    <section style="padding: 70px 0; background: #FFFFFF;">
      <div class="container">
        <div style="text-align: center; max-width: 680px; margin: 0 auto 50px;">
          <span style="color: var(--z-gold); font-weight: 800; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Enterprise Solutions Portfolio</span>
          <h2 style="font-size: 32px; font-weight: 800; color: var(--z-navy); margin: 8px 0 16px;">Core Institutional Platforms</h2>
          <p style="color: var(--z-slate); font-size: 15px;">
            Our practices provide 16 battle-tested platforms deployed with zero fixed pricing — every engagement is tailored to your workflow complexity.
          </p>
        </div>
        <div class="card-grid">
          {system_cards}
        </div>
        <div style="text-align: center; margin-top: 40px;">
          <a href="/systems" class="btn btn-navy" style="font-size: 14px;">View All 16 Enterprise Platforms &rarr;</a>
        </div>
      </div>
    </section>
    """
    return render_public_base("Building Better Businesses", content, active_tab='home')

def render_public_systems(systems: List[dict]) -> str:
    system_cards = ""
    for s in systems:
        feats = "".join([f"<li style='margin-bottom: 6px; font-size: 13px; color: #475569;'>✓ {f}</li>" for f in s.get('features', [])])
        system_cards += f"""
        <div class="z-card">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
            <span class="z-badge">{s.get('pillar')}</span>
            <span class="badge badge-gold">{s.get('tier')}</span>
          </div>
          <div class="z-title">{s.get('name')}</div>
          <div class="z-desc">{s.get('description')}</div>
          <ul style="list-style: none; margin-bottom: 20px;">
            {feats}
          </ul>
          <div style="margin-top: auto; border-top: 1px solid var(--z-border); padding-top: 14px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 12px; font-weight: 700; color: var(--z-gold); text-transform: uppercase;">Tailored Scope Only</span>
            <a href="/tailored-scope?system={s.get('code')}" class="btn btn-navy" style="font-size: 12.5px; padding: 6px 14px;">Scope Solution &rarr;</a>
          </div>
        </div>
        """

    content = f"""
    <div style="background: #0F172A; color: #FFFFFF; padding: 50px 0; border-bottom: 2px solid var(--z-gold);">
      <div class="container">
        <span style="color: var(--z-gold); font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">Solutions Architecture</span>
        <h1 style="font-size: 34px; font-weight: 800; margin-top: 8px;">16 Enterprise Systems Portfolio</h1>
        <p style="color: #94A3B8; font-size: 15px; margin-top: 8px; max-width: 600px;">
          Engineered for manufacturing, logistics, retail, finance, education, and healthcare enterprises across Uganda.
        </p>
      </div>
    </div>

    <div class="container" style="padding: 60px 20px;">
      <div class="card-grid">
        {system_cards}
      </div>
    </div>
    """
    return render_public_base("16 Enterprise Systems", content, active_tab='systems')

def render_tailored_scope_page(system_code: str = '') -> str:
    content = f"""
    <div style="background: #0F172A; color: #FFFFFF; padding: 50px 0; border-bottom: 2px solid var(--z-gold);">
      <div class="container">
        <span style="color: var(--z-gold); font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">Consultative Discovery</span>
        <h1 style="font-size: 34px; font-weight: 800; margin-top: 8px;">Request Tailored Scope Discovery</h1>
        <p style="color: #94A3B8; font-size: 15px; margin-top: 8px; max-width: 640px;">
          Zureka Solutions Limited operates with zero off-the-shelf sticker pricing. Every engagement receives a formal architectural discovery session.
        </p>
      </div>
    </div>

    <div class="container" style="padding: 60px 20px; max-width: 760px;">
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 14px; padding: 36px; box-shadow: var(--card-shadow);">
        <form action="/api/inquiries" method="POST">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
            <div>
              <label style="display: block; font-size: 13px; font-weight: 700; color: #334155; margin-bottom: 6px;">Enterprise / Company Name *</label>
              <input type="text" name="company_name" required placeholder="e.g. Victoria Manufacturing Ltd" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
            </div>
            <div>
              <label style="display: block; font-size: 13px; font-weight: 700; color: #334155; margin-bottom: 6px;">Contact Person *</label>
              <input type="text" name="contact_name" required placeholder="e.g. Grace Nakalema" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
            <div>
              <label style="display: block; font-size: 13px; font-weight: 700; color: #334155; margin-bottom: 6px;">Official Email Address *</label>
              <input type="email" name="email" required placeholder="e.g. grace@victoriamfg.ug" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
            </div>
            <div>
              <label style="display: block; font-size: 13px; font-weight: 700; color: #334155; margin-bottom: 6px;">Phone Number (for SMS Confirmation) *</label>
              <input type="text" name="phone" required placeholder="e.g. +256 772 000 000" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
            </div>
          </div>

          <div style="margin-bottom: 20px;">
            <label style="display: block; font-size: 13px; font-weight: 700; color: #334155; margin-bottom: 6px;">Primary System of Interest</label>
            <input type="text" name="system_interest" value="{system_code}" placeholder="e.g. ERPNext Multi-Plant Manufacturing / BI Analytics" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
          </div>

          <div style="margin-bottom: 24px;">
            <label style="display: block; font-size: 13px; font-weight: 700; color: #334155; margin-bottom: 6px;">Key Operational Requirements & Scope Objectives</label>
            <textarea name="requirements" rows="4" placeholder="Describe current pain points, existing software, user counts, multi-branch needs..." style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;"></textarea>
          </div>

          <button type="submit" class="btn btn-gold" style="width: 100%; font-size: 15px; padding: 12px;">
            Submit Discovery Request (Instant SMS Confirmation via Pandora) &rarr;
          </button>
        </form>
      </div>
    </div>
    """
    return render_public_base("Tailored Scope Discovery", content, active_tab='scope')
