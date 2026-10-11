from __future__ import annotations
import os
from pathlib import Path
import pymysql
import streamlit as st
from dotenv import dotenv_values
from app.config import Settings


def apply_theme():
    st.markdown(
        '''
        <style>
            /* Import Modern Typography */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            :root {
                --bg-main: #0b0f17;
                --bg-card: rgba(22, 30, 46, 0.75);
                --bg-card-hover: rgba(30, 41, 64, 0.85);
                --border-color: rgba(255, 255, 255, 0.1);
                --border-highlight: rgba(56, 189, 248, 0.35);
                --text-primary: #f8fafc;
                --text-secondary: #94a3b8;
                --sidebar-text: #e2e8f0;
                --sidebar-text-active: #ffffff;
                --accent-blue: #38bdf8;
                --accent-green: #34d399;
                --primary-btn: #2563eb;
                --primary-btn-hover: #1d4ed8;
            }

            /* Global App Layout */
            .stApp {
                background-color: var(--bg-main);
                background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(37, 99, 235, 0.08) 0px, transparent 50%);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                color: var(--text-primary);
            }

            /* Hide default footer and main menu, but keep the header container alive for the toggle button */
            #MainMenu, footer {
                visibility: hidden !important;
            }

            header[data-testid="stHeader"] {
                background: transparent !important;
                z-index: 99999 !important;
            }

            /* Container Padding */
            .block-container {
                max-width: 1280px;
                padding: 2.5rem 2rem 4rem 2rem;
            }

            /* ========================================================= */
            /* SIDEBAR TOGGLE BUTTON (VISIBLE WHEN COLLAPSED OR EXPANDED) */
            /* ========================================================= */
            [data-testid="stSidebarCollapseButton"],
            [data-testid="stSidebarExpandButton"],
            button[aria-label="Toggle sidebar"],
            button[title="Expand sidebar"],
            button[title="Collapse sidebar"],
            button[data-testid="baseButton-header"] {
                visibility: visible !important;
                display: flex !important;
                opacity: 1 !important;
                color: #f8fafc !important;
                background-color: rgba(22, 30, 46, 0.85) !important;
                border: 1px solid var(--border-color) !important;
                border-radius: 8px !important;
                padding: 4px !important;
                transition: all 0.2s ease !important;
            }

            [data-testid="stSidebarCollapseButton"]:hover,
            [data-testid="stSidebarExpandButton"]:hover,
            button[aria-label="Toggle sidebar"]:hover {
                background-color: rgba(30, 41, 64, 1) !important;
                border-color: var(--border-highlight) !important;
                color: var(--accent-blue) !important;
            }

            [data-testid="stSidebarCollapseButton"] svg,
            [data-testid="stSidebarExpandButton"] svg {
                fill: currentColor !important;
                stroke: currentColor !important;
            }

            /* ========================================================= */
            /* SIDEBAR & NAVIGATION CONTROLS (HIGH CONTRAST)            */
            /* ========================================================= */
            [data-testid='stSidebar'] {
                background-color: #070a0f !important;
                border-right: 1px solid var(--border-color);
                min-width: 280px !important;
                max-width: 280px !important;
            }

            /* Target all text in sidebar */
            [data-testid='stSidebar'] *, 
            [data-testid='stSidebar'] .stText, 
            [data-testid='stSidebar'] label,
            [data-testid='stSidebar'] p,
            [data-testid='stSidebar'] span {
                color: var(--sidebar-text) !important;
            }

            /* Native Sidebar Navigation Links */
            [data-testid='stSidebarNav'] a {
                color: var(--sidebar-text) !important;
                border-radius: 8px;
                margin: 2px 0;
                transition: all 0.2s ease;
            }

            [data-testid='stSidebarNav'] a:hover {
                background-color: rgba(255, 255, 255, 0.06) !important;
                color: var(--sidebar-text-active) !important;
            }

            [data-testid='stSidebarNav'] a[aria-current="page"] {
                background-color: rgba(56, 189, 248, 0.12) !important;
                color: var(--accent-blue) !important;
                font-weight: 600 !important;
                border-left: 3px solid var(--accent-blue);
            }

            /* Custom Radio/Select Navigations in Sidebar */
            [data-testid='stSidebar'] div[role="radiogroup"] label p {
                font-size: 0.92rem !important;
                font-weight: 500 !important;
                color: var(--sidebar-text) !important;
            }

            [data-testid='stSidebar'] div[role="radiogroup"] label:hover p {
                color: var(--accent-blue) !important;
            }

            /* ========================================================= */
            /* MAIN CONTENT CARDS & COMPONENTS                           */
            /* ========================================================= */

            /* Hero Section */
            .hero {
                position: relative;
                padding: 2.5rem;
                border-radius: 20px;
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid var(--border-color);
                box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
                margin-bottom: 2rem;
            }

            .eyebrow {
                color: var(--accent-blue);
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.1em;
                text-transform: uppercase;
            }

            .hero h1 {
                margin: 0.4rem 0 0.6rem 0;
                font-size: 2.25rem;
                font-weight: 700;
                letter-spacing: -0.025em;
                color: var(--text-primary);
            }

            .hero p {
                margin: 0;
                color: var(--text-secondary);
                font-size: 1rem;
                line-height: 1.5;
            }

            /* Status Badge */
            .status {
                float: right;
                margin-top: -2.5rem;
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                color: var(--accent-green);
                background: rgba(52, 211, 153, 0.1);
                border: 1px solid rgba(52, 211, 153, 0.2);
                padding: 0.35rem 0.85rem;
                border-radius: 9999px;
                font-size: 0.78rem;
                font-weight: 600;
            }

            /* Metric Cards */
            .metric-card {
                min-height: 120px;
                padding: 1.25rem 1.5rem;
                border-radius: 16px;
                background: var(--bg-card);
                backdrop-filter: blur(8px);
                border: 1px solid var(--border-color);
                transition: all 0.25s ease;
            }

            .metric-card:hover {
                background: var(--bg-card-hover);
                border-color: var(--border-highlight);
                transform: translateY(-2px);
                box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.4);
            }

            .metric-name {
                color: var(--text-secondary);
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .metric-value {
                color: var(--text-primary);
                font-size: 2rem;
                font-weight: 700;
                letter-spacing: -0.02em;
                margin-top: 0.4rem;
            }

            .metric-detail {
                color: var(--accent-green);
                font-size: 0.825rem;
                font-weight: 500;
                margin-top: 0.35rem;
            }

            /* Section Titles */
            .section-title {
                color: var(--text-primary);
                font-size: 1.25rem;
                font-weight: 600;
                letter-spacing: -0.01em;
                margin: 2rem 0 1rem 0;
            }

            /* Primary Button Styling */
            .stButton > button {
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                background: var(--primary-btn);
                color: #ffffff;
                font-weight: 600;
                font-size: 0.9rem;
                padding: 0.55rem 1.25rem;
                transition: all 0.2s ease;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
            }

            .stButton > button:hover {
                background: var(--primary-btn-hover);
                border-color: rgba(255, 255, 255, 0.2);
                box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
                transform: translateY(-1px);
            }

            /* Dataframes & Tables */
            div[data-testid='stDataFrame'] {
                border: 1px solid var(--border-color);
                border-radius: 14px;
                overflow: hidden;
                background: var(--bg-card);
                backdrop-filter: blur(8px);
            }
        </style>
        ''',
        unsafe_allow_html=True
    )


def render_sidebar():
    with st.sidebar:
        st.markdown('### 👥 Person ReID')
        st.caption('Control Center')
        st.page_link('streamlit_app.py', label='Home', icon='⌂')
        st.page_link('/analytics', label='Analytics', icon='📊')
        st.page_link('/admin', label='Admin', icon='⚙️')
        st.divider()
        st.caption('Presence intelligence')


def connection():
    settings = Settings()
    return pymysql.connect(host=settings.mysql_host, port=settings.mysql_port, user=settings.mysql_user,
                           password=settings.mysql_password, database=settings.mysql_database,
                           cursorclass=pymysql.cursors.DictCursor, connect_timeout=5, read_timeout=10, autocommit=True)


@st.cache_data(ttl=3)
def load_runs() -> list[dict]:
    db = connection()
    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT id, source, started_at, completed_at FROM reid_runs WHERE deleted_at IS NULL ORDER BY id DESC LIMIT 100')
            return list(cursor.fetchall())
    finally:
        db.close()


@st.cache_data(ttl=3)
def load_run_details(run_id: int) -> tuple[list[dict], list[dict]]:
    db = connection()
    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT person_name, total_seconds, entries_count, exits_count FROM person_presence WHERE run_id=%s AND deleted_at IS NULL ORDER BY person_name', (run_id,))
            summary = list(cursor.fetchall())
            cursor.execute('SELECT person_name, event_type, occurred_at FROM person_presence_events WHERE run_id=%s AND deleted_at IS NULL ORDER BY occurred_at', (run_id,))
            return summary, list(cursor.fetchall())
    finally:
        db.close()


def delete_run(run_id: int) -> None:
    db = connection()
    try:
        with db.cursor() as cursor:
            cursor.execute('UPDATE person_presence_events SET deleted_at=NOW() WHERE run_id=%s AND deleted_at IS NULL', (run_id,))
            cursor.execute('UPDATE person_presence SET deleted_at=NOW() WHERE run_id=%s AND deleted_at IS NULL', (run_id,))
            cursor.execute('UPDATE reid_runs SET deleted_at=NOW() WHERE id=%s AND deleted_at IS NULL', (run_id,))
    finally:
        db.close()


def admin_authenticated() -> bool:
    password = dotenv_values(Path(__file__).resolve().parents[2] / '.env').get('REID_ADMIN_PASSWORD') or os.getenv('REID_ADMIN_PASSWORD', '')
    if not password:
        st.warning('Set `REID_ADMIN_PASSWORD` in `.env` to enable administration.')
        return False
    if st.session_state.get('admin_authenticated'):
        return True
    entered = st.text_input('Admin password', type='password')
    if st.button('Sign in'):
        if entered == password:
            st.session_state.admin_authenticated = True
            st.rerun()
        st.error('Incorrect admin password.')
    return False