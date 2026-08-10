# ==========================================================
# INSIGHTFLOW AI
# HOME PAGE
# Version 2.0
# Developed by Swaroop K Samantaray
# ==========================================================

import streamlit as st


def show_home():
    """
    InsightFlow AI landing page.

    The entire visual layout is rendered inside one st.html block so
    the grid/flex CSS is applied consistently to all sections.
    This avoids the isolated-style issue that caused the capability,
    technology and architecture sections to stack vertically.
    """

    st.html(
        """
        <style>
        /* =====================================================
           HOME PAGE - MASTER LAYOUT
           ===================================================== */

        .if-home,
        .if-home * {
            box-sizing: border-box;
        }

        .if-home {
            width: 100%;
            color: #f5f7ff;
            font-family: Inter, -apple-system, BlinkMacSystemFont,
                         "Segoe UI", sans-serif;
        }

        .if-home h1,
        .if-home h2,
        .if-home h3,
        .if-home p {
            margin-top: 0;
        }

        .if-section {
            width: 100%;
            margin: 0 0 42px 0;
        }

        .if-section-header {
            margin-bottom: 24px;
        }

        .if-section-header .if-section-icon {
            font-size: 25px;
            line-height: 1;
            margin-bottom: 12px;
        }

        .if-section-header h2 {
            margin: 0 0 10px 0;
            font-size: 30px;
            line-height: 1.2;
            font-weight: 800;
            color: #f5f7ff;
        }

        .if-section-header p {
            margin: 0;
            color: #9db7dc;
            font-size: 15px;
            line-height: 1.7;
            max-width: 950px;
        }

        .if-divider {
            width: 100%;
            height: 1px;
            background: rgba(140, 165, 210, 0.18);
            margin: 8px 0 42px 0;
        }


        /* =====================================================
           HERO
           ===================================================== */

        .if-hero {
            width: 100%;
            padding: 48px 54px;
            margin-bottom: 28px;
            border-radius: 24px;
            border: 1px solid rgba(120, 160, 230, 0.24);

            background:
                radial-gradient(
                    circle at 88% 18%,
                    rgba(83, 105, 235, 0.22),
                    transparent 44%
                ),
                linear-gradient(
                    135deg,
                    #172640 0%,
                    #101a2c 55%,
                    #1b214b 100%
                );

            box-shadow: 0 18px 45px rgba(0, 0, 0, 0.18);
        }

        .if-hero-badge {
            display: inline-flex;
            align-items: center;
            padding: 9px 17px;
            margin-bottom: 20px;
            border-radius: 999px;
            border: 1px solid rgba(100, 160, 255, 0.38);
            background: rgba(45, 80, 145, 0.24);
            color: #8db7ff;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.65px;
        }

        .if-hero h1 {
            margin: 0 0 14px 0;
            font-size: clamp(48px, 5.5vw, 76px);
            line-height: 1.02;
            font-weight: 850;
            letter-spacing: -2.8px;
            color: #f5f7ff;
        }

        .if-hero h1 span {
            background: linear-gradient(
                90deg,
                #ffffff,
                #9abaff,
                #8ca5ff
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .if-hero h2 {
            margin: 0 0 18px 0;
            font-size: clamp(21px, 2.2vw, 29px);
            line-height: 1.3;
            font-weight: 650;
            color: #f1f4ff;
        }

        .if-hero p {
            margin: 0;
            max-width: 920px;
            font-size: 16px;
            line-height: 1.8;
            color: #9db7dc;
        }


        /* =====================================================
           PLATFORM STATISTICS
           ===================================================== */

        .if-stats-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 18px;
            width: 100%;
            margin-bottom: 42px;
        }

        .if-stat-card {
            min-width: 0;
            min-height: 145px;
            padding: 26px 18px;
            border-radius: 18px;
            border: 1px solid rgba(120, 160, 230, 0.18);

            background: linear-gradient(
                145deg,
                rgba(25, 35, 55, 0.96),
                rgba(15, 21, 35, 0.96)
            );

            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;

            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }

        .if-stat-card:hover {
            transform: translateY(-4px);
            border-color: rgba(110, 160, 255, 0.35);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
        }

        .if-stat-icon {
            font-size: 31px;
            line-height: 1;
            margin-bottom: 11px;
        }

        .if-stat-value {
            font-size: 30px;
            font-weight: 800;
            line-height: 1.1;
            color: #ffffff;
            margin-bottom: 8px;
        }

        .if-stat-label {
            font-size: 14px;
            line-height: 1.4;
            color: #9bb8df;
        }


        /* =====================================================
           CAPABILITIES
           ===================================================== */

        .if-capability-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 18px;
            width: 100%;
        }

        .if-feature-card {
            min-width: 0;
            min-height: 205px;
            padding: 28px;
            border-radius: 18px;
            border: 1px solid rgba(120, 160, 230, 0.16);

            background: linear-gradient(
                145deg,
                rgba(23, 31, 49, 0.98),
                rgba(15, 21, 35, 0.98)
            );

            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }

        .if-feature-card:hover {
            transform: translateY(-4px);
            border-color: rgba(110, 160, 255, 0.35);
            box-shadow: 0 15px 32px rgba(0, 0, 0, 0.18);
        }

        .if-feature-icon {
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            border-radius: 14px;
            border: 1px solid rgba(110, 160, 255, 0.18);
            background: rgba(45, 75, 135, 0.28);
            font-size: 23px;
        }

        .if-feature-card h3 {
            margin: 0 0 11px 0;
            font-size: 18px;
            line-height: 1.3;
            font-weight: 750;
            color: #f5f7ff;
        }

        .if-feature-card p {
            margin: 0;
            color: #9db7dc;
            font-size: 14px;
            line-height: 1.7;
        }


        /* =====================================================
           TECHNOLOGY STACK
           ===================================================== */

        .if-tech-grid {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 14px;
            width: 100%;
        }

        .if-tech-card {
            min-width: 0;
            min-height: 120px;
            padding: 20px 12px;
            border-radius: 16px;
            border: 1px solid rgba(120, 160, 230, 0.16);

            background: linear-gradient(
                145deg,
                rgba(23, 31, 49, 0.98),
                rgba(15, 21, 35, 0.98)
            );

            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;

            transition:
                transform 0.2s ease,
                border-color 0.2s ease;
        }

        .if-tech-card:hover {
            transform: translateY(-4px);
            border-color: rgba(110, 160, 255, 0.35);
        }

        .if-tech-icon {
            font-size: 30px;
            line-height: 1;
            margin-bottom: 12px;
        }

        .if-tech-card strong {
            color: #dfe8ff;
            font-size: 14px;
            font-weight: 700;
        }


        /* =====================================================
           WHY INSIGHTFLOW
           ===================================================== */

        .if-two-column {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 18px;
            width: 100%;
        }

        .if-large-card {
            min-height: 275px;
        }

        .if-large-card ul {
            margin: 18px 0 0 0;
            padding-left: 20px;
            color: #c8d6ee;
        }

        .if-large-card li {
            margin-bottom: 9px;
            font-size: 14px;
            line-height: 1.5;
        }


        /* =====================================================
           ARCHITECTURE
           ===================================================== */

        .if-architecture {
            width: 100%;
            padding: 28px 24px;
            border-radius: 20px;
            border: 1px solid rgba(120, 160, 230, 0.16);

            background: linear-gradient(
                145deg,
                rgba(23, 31, 49, 0.98),
                rgba(15, 21, 35, 0.98)
            );

            display: grid;
            grid-template-columns:
                minmax(0, 1fr)
                auto
                minmax(0, 1fr)
                auto
                minmax(0, 1fr)
                auto
                minmax(0, 1fr);

            gap: 14px;
            align-items: center;
        }

        .if-architecture-step {
            min-width: 0;
            min-height: 135px;
            padding: 20px 16px;
            border-radius: 15px;
            border: 1px solid rgba(110, 160, 255, 0.18);
            background: rgba(27, 40, 67, 0.72);

            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }

        .if-architecture-icon {
            font-size: 30px;
            margin-bottom: 11px;
        }

        .if-architecture-step h3 {
            margin: 0 0 8px 0;
            color: #f4f7ff;
            font-size: 15px;
            font-weight: 750;
        }

        .if-architecture-step span {
            color: #8faad1;
            font-size: 11px;
            line-height: 1.5;
        }

        .if-architecture-arrow {
            color: #78a8ff;
            font-size: 28px;
            font-weight: 400;
            text-align: center;
        }


        /* =====================================================
           CTA
           ===================================================== */

        .if-cta {
            width: 100%;
            padding: 52px 30px;
            border-radius: 22px;
            border: 1px solid rgba(110, 160, 255, 0.18);

            background:
                radial-gradient(
                    circle at 50% 0%,
                    rgba(75, 100, 220, 0.16),
                    transparent 55%
                ),
                rgba(20, 28, 45, 0.86);

            text-align: center;
        }

        .if-cta-icon {
            font-size: 42px;
            line-height: 1;
            margin-bottom: 16px;
        }

        .if-cta h2 {
            margin: 0 0 12px 0;
            font-size: 25px;
            font-weight: 800;
            color: #f5f7ff;
        }

        .if-cta p {
            margin: 0 auto;
            max-width: 760px;
            color: #9db7dc;
            font-size: 15px;
            line-height: 1.7;
        }


        /* =====================================================
           DEVELOPER
           ===================================================== */

        .if-developer {
            width: 100%;
            padding: 48px 20px 28px;
            text-align: center;
        }

        .if-developer-divider {
            width: 100%;
            height: 1px;
            margin-bottom: 36px;
            background: rgba(140, 165, 210, 0.18);
        }

        .if-developer-icon {
            font-size: 28px;
            margin-bottom: 10px;
        }

        .if-developer-built {
            margin: 0 0 8px 0;
            color: #8faad1;
            font-size: 14px;
        }

        .if-developer h2 {
            margin: 0 0 10px 0;
            font-size: 23px;
            font-weight: 800;
            color: #f5f7ff;
        }

        .if-developer-role {
            margin: 0 0 12px 0;
            color: #8faad1;
            font-size: 14px;
            line-height: 1.7;
        }

        .if-developer-project {
            margin: 0;
            color: #657b9d;
            font-size: 12px;
        }


        /* =====================================================
           RESPONSIVE
           ===================================================== */

        @media (max-width: 1200px) {
            .if-tech-grid {
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }

            .if-architecture {
                grid-template-columns: repeat(4, minmax(0, 1fr));
            }

            .if-architecture-arrow {
                display: none;
            }
        }

        @media (max-width: 900px) {
            .if-hero {
                padding: 40px 34px;
            }

            .if-stats-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .if-capability-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .if-two-column {
                grid-template-columns: 1fr;
            }

            .if-architecture {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 600px) {
            .if-hero {
                padding: 32px 24px;
                border-radius: 18px;
            }

            .if-hero h1 {
                font-size: 46px;
                letter-spacing: -1.7px;
            }

            .if-hero h2 {
                font-size: 21px;
            }

            .if-stats-grid,
            .if-capability-grid,
            .if-tech-grid,
            .if-two-column,
            .if-architecture {
                grid-template-columns: 1fr;
            }

            .if-section-header h2 {
                font-size: 26px;
            }

            .if-feature-card,
            .if-large-card {
                min-height: auto;
            }

            .if-architecture-arrow {
                display: none;
            }
        }
        </style>


        <div class="if-home">

            <!-- =================================================
                 HERO
                 ================================================= -->

            <section class="if-hero">

                <div class="if-hero-badge">
                    🚀 &nbsp; AI-POWERED BUSINESS INTELLIGENCE
                </div>

                <h1>
                    InsightFlow <span>AI</span>
                </h1>

                <h2>
                    Turn Business Data Into Better Decisions
                </h2>

                <p>
                    An intelligent business analytics platform that combines
                    interactive dashboards, machine learning, predictive
                    forecasting and generative AI to transform business data
                    into actionable insights.
                </p>

            </section>


            <!-- =================================================
                 PLATFORM STATISTICS
                 ================================================= -->

            <section class="if-stats-grid">

                <div class="if-stat-card">
                    <div class="if-stat-icon">📊</div>
                    <div class="if-stat-value">8</div>
                    <div class="if-stat-label">Analytics Modules</div>
                </div>

                <div class="if-stat-card">
                    <div class="if-stat-icon">🤖</div>
                    <div class="if-stat-value">AI</div>
                    <div class="if-stat-label">Intelligent Insights</div>
                </div>

                <div class="if-stat-card">
                    <div class="if-stat-icon">📈</div>
                    <div class="if-stat-value">ML</div>
                    <div class="if-stat-label">Predictive Analytics</div>
                </div>

                <div class="if-stat-card">
                    <div class="if-stat-icon">📄</div>
                    <div class="if-stat-value">PDF</div>
                    <div class="if-stat-label">Executive Reporting</div>
                </div>

            </section>


            <div class="if-divider"></div>


            <!-- =================================================
                 PLATFORM CAPABILITIES
                 ================================================= -->

            <section class="if-section">

                <div class="if-section-header">
                    <div class="if-section-icon">✨</div>

                    <h2>Platform Capabilities</h2>

                    <p>
                        Explore a complete analytics environment built for
                        business intelligence, predictive analytics and
                        AI-assisted decision making.
                    </p>
                </div>


                <div class="if-capability-grid">

                    <div class="if-feature-card">
                        <div class="if-feature-icon">📈</div>
                        <h3>Sales Analytics</h3>
                        <p>
                            Analyze revenue performance, sales trends,
                            growth patterns and business performance
                            across time.
                        </p>
                    </div>

                    <div class="if-feature-card">
                        <div class="if-feature-icon">📦</div>
                        <h3>Product Analytics</h3>
                        <p>
                            Identify high-performing products, profitability
                            patterns, product contribution and opportunities
                            for product optimization.
                        </p>
                    </div>

                    <div class="if-feature-card">
                        <div class="if-feature-icon">👥</div>
                        <h3>Customer Analytics</h3>
                        <p>
                            Understand customer segments, purchasing behavior
                            and revenue contribution to improve
                            customer-focused decisions.
                        </p>
                    </div>

                    <div class="if-feature-card">
                        <div class="if-feature-icon">🌍</div>
                        <h3>Regional Intelligence</h3>
                        <p>
                            Compare regional performance and identify
                            geographical opportunities using interactive
                            business analytics.
                        </p>
                    </div>

                    <div class="if-feature-card">
                        <div class="if-feature-icon">🔮</div>
                        <h3>Predictive Forecasting</h3>
                        <p>
                            Use machine learning to estimate future sales
                            and support proactive business planning.
                        </p>
                    </div>

                    <div class="if-feature-card">
                        <div class="if-feature-icon">🤖</div>
                        <h3>AI Business Copilot</h3>
                        <p>
                            Ask questions about business performance and
                            receive AI-assisted explanations, insights
                            and recommendations.
                        </p>
                    </div>

                    <div class="if-feature-card">
                        <div class="if-feature-icon">🧠</div>
                        <h3>AI Business Insights</h3>
                        <p>
                            Identify business risks, opportunities and
                            strategic recommendations using intelligent
                            analytics.
                        </p>
                    </div>

                    <div class="if-feature-card">
                        <div class="if-feature-icon">📄</div>
                        <h3>Executive Reporting</h3>
                        <p>
                            Generate professional business reports combining
                            KPIs, analytics and insights into an
                            executive-ready format.
                        </p>
                    </div>

                </div>

            </section>


            <div class="if-divider"></div>


            <!-- =================================================
                 TECHNOLOGY STACK
                 ================================================= -->

            <section class="if-section">

                <div class="if-section-header">
                    <div class="if-section-icon">🛠️</div>

                    <h2>Technology Stack</h2>

                    <p>
                        Built using modern data science, analytics and
                        artificial intelligence technologies.
                    </p>
                </div>


                <div class="if-tech-grid">

                    <div class="if-tech-card">
                        <div class="if-tech-icon">🐍</div>
                        <strong>Python</strong>
                    </div>

                    <div class="if-tech-card">
                        <div class="if-tech-icon">📊</div>
                        <strong>Streamlit</strong>
                    </div>

                    <div class="if-tech-card">
                        <div class="if-tech-icon">📈</div>
                        <strong>Plotly</strong>
                    </div>

                    <div class="if-tech-card">
                        <div class="if-tech-icon">🧮</div>
                        <strong>Pandas</strong>
                    </div>

                    <div class="if-tech-card">
                        <div class="if-tech-icon">🧠</div>
                        <strong>Scikit-learn</strong>
                    </div>

                    <div class="if-tech-card">
                        <div class="if-tech-icon">🤖</div>
                        <strong>Gemini AI</strong>
                    </div>

                </div>

            </section>


            <div class="if-divider"></div>


            <!-- =================================================
                 WHY INSIGHTFLOW AI
                 ================================================= -->

            <section class="if-section">

                <div class="if-section-header">
                    <div class="if-section-icon">🎯</div>

                    <h2>Why InsightFlow AI?</h2>

                    <p>
                        Designed to connect descriptive, diagnostic and
                        predictive analytics in one platform.
                    </p>
                </div>


                <div class="if-two-column">

                    <div class="if-feature-card if-large-card">

                        <div class="if-feature-icon">📊</div>

                        <h3>From Data to Decisions</h3>

                        <p>
                            Transform raw business data into meaningful
                            metrics, trends and visual insights that
                            support faster decision-making.
                        </p>

                        <ul>
                            <li>Interactive business dashboards</li>
                            <li>Multi-dimensional analysis</li>
                            <li>Global data filtering</li>
                            <li>KPI-driven reporting</li>
                        </ul>

                    </div>


                    <div class="if-feature-card if-large-card">

                        <div class="if-feature-icon">🤖</div>

                        <h3>Intelligence Beyond Dashboards</h3>

                        <p>
                            Combine traditional business intelligence
                            with machine learning and generative AI
                            to move from reporting toward intelligent
                            analysis.
                        </p>

                        <ul>
                            <li>AI-powered recommendations</li>
                            <li>Business risk identification</li>
                            <li>Predictive sales forecasting</li>
                            <li>Natural-language business analysis</li>
                        </ul>

                    </div>

                </div>

            </section>


            <div class="if-divider"></div>


            <!-- =================================================
                 PLATFORM ARCHITECTURE
                 ================================================= -->

            <section class="if-section">

                <div class="if-section-header">
                    <div class="if-section-icon">🏗️</div>

                    <h2>Platform Architecture</h2>

                    <p>
                        A modular analytics architecture designed for
                        maintainability and future expansion.
                    </p>
                </div>


                <div class="if-architecture">

                    <div class="if-architecture-step">
                        <div class="if-architecture-icon">📁</div>
                        <h3>Business Data</h3>
                        <span>Sales • Customers • Products</span>
                    </div>

                    <div class="if-architecture-arrow">→</div>

                    <div class="if-architecture-step">
                        <div class="if-architecture-icon">🧹</div>
                        <h3>Data Processing</h3>
                        <span>Cleaning • Transformation • Filtering</span>
                    </div>

                    <div class="if-architecture-arrow">→</div>

                    <div class="if-architecture-step">
                        <div class="if-architecture-icon">📊</div>
                        <h3>Analytics Engine</h3>
                        <span>KPI • EDA • Visualization</span>
                    </div>

                    <div class="if-architecture-arrow">→</div>

                    <div class="if-architecture-step">
                        <div class="if-architecture-icon">🧠</div>
                        <h3>AI &amp; ML</h3>
                        <span>Gemini • Forecasting • Insights</span>
                    </div>

                </div>

            </section>


            <!-- =================================================
                 CALL TO ACTION
                 ================================================= -->

            <section class="if-cta">

                <div class="if-cta-icon">🚀</div>

                <h2>Ready to Explore Your Business Data?</h2>

                <p>
                    Use the navigation panel to explore analytics,
                    discover business insights and generate forecasts.
                </p>

            </section>


            <!-- =================================================
                 DEVELOPER
                 ================================================= -->

            <section class="if-developer">

                <div class="if-developer-divider"></div>

                <div class="if-developer-icon">💻</div>

                <p class="if-developer-built">
                    Built with ❤️ by
                </p>

                <h2>Swaroop K Samantaray</h2>

                <p class="if-developer-role">
                    Data Science • Artificial Intelligence •
                    Machine Learning • Business Intelligence
                </p>

                <p class="if-developer-project">
                    InsightFlow AI • Version 2.0 • © 2026
                </p>

            </section>

        </div>
        """
    )