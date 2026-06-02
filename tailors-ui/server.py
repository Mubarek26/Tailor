import http.server
import socketserver
import os
import urllib.parse

PORT = 8084

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tailor Shop - Workshop Team Directory</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #07080e;
            --bg-surface: rgba(16, 18, 35, 0.65);
            --bg-card: rgba(22, 25, 49, 0.5);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --primary: #ec4899;
            --primary-glow: rgba(236, 72, 153, 0.15);
            --primary-gradient: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
            --success: #10b981;
            --success-bg: rgba(16, 185, 129, 0.1);
            --warning: #f59e0b;
            --warning-bg: rgba(245, 158, 11, 0.1);
            --danger: #ef4444;
            --danger-bg: rgba(239, 68, 68, 0.1);
            --font-main: 'Outfit', sans-serif;
            --shadow-lg: 0 20px 25px -5px rgb(0 0 0 / 0.5), 0 8px 10px -6px rgb(0 0 0 / 0.5);
            --shadow-glow: 0 0 30px rgba(236, 72, 153, 0.2);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-main);
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(at 0% 0%, rgba(236, 72, 153, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(239, 68, 68, 0.05) 0px, transparent 50%),
                radial-gradient(at 50% 0%, rgba(16, 185, 129, 0.03) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
        }

        /* Scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.25);
        }

        /* Header Bar */
        header {
            background: rgba(10, 11, 20, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo-container {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-icon {
            background: var(--primary-gradient);
            width: 2.25rem;
            height: 2.25rem;
            border-radius: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 10px rgba(236, 72, 153, 0.3);
        }

        .logo-icon svg {
            width: 1.25rem;
            height: 1.25rem;
            stroke: white;
            fill: none;
        }

        .logo-text {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .terminal-badge {
            background: rgba(236, 72, 153, 0.15);
            border: 1px solid rgba(236, 72, 153, 0.3);
            color: #fbcfe8;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .user-menu {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .api-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.8rem;
            font-weight: 500;
            color: var(--text-secondary);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--success);
            box-shadow: 0 0 10px var(--success);
        }

        .status-dot.disconnected {
            background-color: var(--danger);
            box-shadow: 0 0 10px var(--danger);
        }

        .btn-logout {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.5rem 1rem;
            border-radius: 0.75rem;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-logout:hover {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            border-color: rgba(239, 68, 68, 0.2);
        }

        /* Layout Grid */
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: 1fr;
            gap: 2rem;
            flex-grow: 1;
        }

        @media (min-width: 1024px) {
            .container {
                grid-template-columns: 1.8fr 1.2fr;
            }
        }

        /* Left Side: Summary and Table */
        .main-content {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        /* Summary Cards */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(1, 1fr);
            gap: 1rem;
        }

        @media (min-width: 640px) {
            .summary-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }

        .summary-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 1.25rem;
            padding: 1.25rem;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }

        .summary-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: transparent;
        }

        .summary-card.total-team::before {
            background: linear-gradient(90deg, #ec4899, #f472b6);
        }

        .summary-card.active-jobs::before {
            background: linear-gradient(90deg, #a855f7, #6366f1);
        }

        .summary-card.completed-jobs::before {
            background: linear-gradient(90deg, #10b981, #06b6d4);
        }

        .summary-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        }

        .summary-value {
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }

        /* Dashboard Panel */
        .panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 1.5rem;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: var(--shadow-lg);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .panel-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        @media (min-width: 640px) {
            .panel-header {
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
            }
        }

        .panel-title-container {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .panel-title {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.015em;
        }

        .panel-subtitle {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        /* Panel actions button */
        .btn-panel-action {
            background: var(--primary-gradient);
            border: none;
            color: white;
            padding: 0.6rem 1.2rem;
            border-radius: 0.75rem;
            font-size: 0.85rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 10px rgba(236, 72, 153, 0.2);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-panel-action:hover {
            opacity: 0.95;
            transform: translateY(-1px);
        }

        /* Search input */
        .controls-row {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            width: 100%;
        }

        @media (min-width: 640px) {
            .controls-row {
                width: auto;
                max-width: 320px;
            }
        }

        .search-wrapper {
            position: relative;
            flex-grow: 1;
            display: flex;
            align-items: center;
        }

        .search-input {
            width: 100%;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.6rem 1rem 0.6rem 2.25rem;
            border-radius: 0.75rem;
            font-size: 0.9rem;
            font-family: var(--font-main);
            transition: all 0.2s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px var(--primary-glow);
        }

        .search-icon {
            position: absolute;
            left: 0.75rem;
            color: var(--text-muted);
            pointer-events: none;
        }

        .search-icon svg {
            width: 1rem;
            height: 1rem;
            stroke: currentColor;
            fill: none;
        }

        /* Tailors Table */
        .table-container {
            overflow-x: auto;
            flex-grow: 1;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background: rgba(0, 0, 0, 0.1);
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
        }

        td {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
            vertical-align: middle;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr.table-row {
            cursor: pointer;
            transition: background-color 0.15s ease;
        }

        tr.table-row:hover {
            background-color: rgba(255, 255, 255, 0.02);
        }

        tr.table-row.selected {
            background-color: rgba(236, 72, 153, 0.08);
        }

        .tailor-identity {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .avatar-initial {
            width: 2.25rem;
            height: 2.25rem;
            border-radius: 50%;
            background: rgba(236, 72, 153, 0.15);
            color: var(--primary);
            font-weight: 700;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(236, 72, 153, 0.2);
        }

        .tailor-name-cell {
            font-weight: 600;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }

        .status-badge.active, .status-badge.approved {
            background-color: var(--success-bg);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        .status-badge.pending {
            background-color: var(--warning-bg);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.2);
        }

        .badge-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: currentColor;
        }

        .btn-manage {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.35rem 0.75rem;
            border-radius: 0.5rem;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-manage:hover {
            background: var(--primary-gradient);
            border-color: transparent;
            box-shadow: 0 4px 10px rgba(236, 72, 153, 0.2);
        }

        tr.selected .btn-manage {
            background: var(--primary-gradient);
            border-color: transparent;
        }

        /* Pagination */
        .pagination-container {
            padding: 1.25rem 1.5rem;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(0, 0, 0, 0.05);
        }

        .pagination-text {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .pagination-actions {
            display: flex;
            gap: 0.5rem;
        }

        .btn-page {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.4rem 0.8rem;
            border-radius: 0.5rem;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-page:hover:not(:disabled) {
            background: rgba(255, 255, 255, 0.1);
        }

        .btn-page:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        /* Right Side: Sidebar */
        .sidebar {
            display: flex;
            flex-direction: column;
            height: fit-content;
            position: sticky;
            top: 5.5rem;
        }

        .sidebar-placeholder {
            padding: 4rem 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 1.5rem;
            color: var(--text-secondary);
        }

        .placeholder-icon {
            width: 4rem;
            height: 4rem;
            background: rgba(236, 72, 153, 0.08);
            border: 1px solid rgba(236, 72, 153, 0.2);
            border-radius: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
            box-shadow: var(--shadow-glow);
        }

        .placeholder-icon svg {
            width: 2rem;
            height: 2rem;
            stroke: currentColor;
            fill: none;
        }

        .placeholder-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .placeholder-text {
            font-size: 0.85rem;
            max-width: 260px;
            line-height: 1.5;
        }

        /* Sidebar Content Loaded */
        .sidebar-content {
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .sidebar-section-title {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin-bottom: 0.75rem;
        }

        .meta-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.75rem;
        }

        .meta-item {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .meta-label {
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.02em;
            color: var(--text-muted);
        }

        .meta-value {
            font-size: 0.9rem;
            font-weight: 600;
        }

        /* Dialog overlays */
        .dialog-overlay {
            position: fixed;
            inset: 0;
            background: rgba(4, 5, 10, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 500;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }

        .dialog-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .dialog {
            background: rgba(20, 22, 42, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 1.5rem;
            width: 90%;
            max-width: 520px;
            padding: 2rem;
            box-shadow: var(--shadow-lg);
            transform: scale(0.95);
            transition: transform 0.3s ease;
            position: relative;
        }

        .dialog-overlay.active .dialog {
            transform: scale(1);
        }

        .dialog-close {
            position: absolute;
            top: 1.25rem;
            right: 1.25rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            width: 2rem;
            height: 2rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.2s ease;
        }

        .dialog-close:hover {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.1);
        }

        /* Tabs list */
        .tabs-header {
            display: grid;
            grid-template-columns: 1fr 1fr;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 0.75rem;
            padding: 0.25rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border-color);
        }

        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 0.5rem;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s ease;
        }

        .tab-btn.active {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }

        /* Forms */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        @media (min-width: 640px) {
            .form-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        .form-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        }

        .input-text {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 0.75rem;
            font-size: 0.9rem;
            font-family: var(--font-main);
            transition: all 0.2s ease;
        }

        .input-text:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px var(--primary-glow);
        }

        .btn-submit {
            background: var(--primary-gradient);
            border: none;
            color: white;
            padding: 0.85rem;
            border-radius: 0.75rem;
            font-size: 0.95rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
        }

        .btn-submit:hover:not(:disabled) {
            opacity: 0.95;
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(236, 72, 153, 0.4);
        }

        .btn-submit:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            box-shadow: none;
        }

        .lookup-box {
            display: flex;
            gap: 0.5rem;
        }

        .btn-lookup {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.75rem 1.25rem;
            border-radius: 0.75rem;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-lookup:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .tailor-card-preview {
            background: rgba(236, 72, 153, 0.05);
            border: 1px solid rgba(236, 72, 153, 0.2);
            border-radius: 1rem;
            padding: 1.25rem;
            margin-top: 1rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .preview-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        /* Login Modal overlay */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(4, 5, 10, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }

        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .modal {
            background: rgba(20, 22, 42, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 2rem;
            width: 90%;
            max-width: 440px;
            padding: 2.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), var(--shadow-glow);
            transform: scale(0.95);
            transition: transform 0.3s ease;
        }

        .modal-overlay.active .modal {
            transform: scale(1);
        }

        .modal-header {
            text-align: center;
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
        }

        .modal-logo {
            width: 3.5rem;
            height: 3.5rem;
            background: var(--primary-gradient);
            border-radius: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 20px rgba(236, 72, 153, 0.3);
        }

        .modal-logo svg {
            width: 1.75rem;
            height: 1.75rem;
            stroke: white;
            fill: none;
        }

        .modal-title {
            font-size: 1.75rem;
            font-weight: 900;
            letter-spacing: -0.025em;
        }

        .modal-subtitle {
            font-size: 0.9rem;
            color: var(--text-secondary);
            max-width: 280px;
        }

        .modal-form {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .input-field {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.85rem 1.2rem;
            border-radius: 0.85rem;
            font-size: 0.95rem;
            font-family: var(--font-main);
            transition: all 0.2s ease;
        }

        .input-field:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px var(--primary-glow);
        }

        .btn-login {
            background: var(--primary-gradient);
            border: none;
            color: white;
            padding: 0.9rem;
            border-radius: 0.85rem;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(236, 72, 153, 0.3);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-login:hover {
            opacity: 0.95;
            box-shadow: 0 6px 20px rgba(236, 72, 153, 0.45);
        }

        /* Toast Container */
        #toast-container {
            position: fixed;
            top: 2rem;
            right: 2rem;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            pointer-events: none;
        }

        .toast {
            background: rgba(18, 20, 38, 0.9);
            border: 1px solid var(--border-color);
            border-radius: 1rem;
            padding: 1rem 1.5rem;
            color: var(--text-primary);
            font-size: 0.9rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            transform: translateX(120%);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            pointer-events: auto;
            backdrop-filter: blur(12px);
        }

        .toast.show {
            transform: translateX(0);
        }

        .toast-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 1.5rem;
            height: 1.5rem;
            border-radius: 50%;
        }

        .toast.success {
            border-left: 4px solid var(--success);
        }

        .toast.success .toast-icon {
            background-color: var(--success-bg);
            color: var(--success);
        }

        .toast.error {
            border-left: 4px solid var(--danger);
        }

        .toast.error .toast-icon {
            background-color: var(--danger-bg);
            color: var(--danger);
        }

        /* Loading Shimmers */
        .loading-shimmer {
            background: linear-gradient(
                90deg,
                rgba(255, 255, 255, 0.03) 25%,
                rgba(255, 255, 255, 0.08) 50%,
                rgba(255, 255, 255, 0.03) 75%
            );
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
        }

        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        /* Empty state styles */
        .empty-table {
            text-align: center;
            padding: 3rem;
            color: var(--text-secondary);
        }

        .empty-table svg {
            width: 2.5rem;
            height: 2.5rem;
            margin-bottom: 1rem;
            stroke: var(--text-muted);
            fill: none;
        }

        .spinner {
            animation: spin 1s linear infinite;
            width: 1.2rem;
            height: 1.2rem;
            display: none;
        }

        @keyframes spin {
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="logo-container">
            <div class="logo-icon">
                <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <line x1="6" y1="3" x2="6" y2="21"></line>
                    <line x1="18" y1="3" x2="18" y2="21"></line>
                    <line x1="6" y1="12" x2="18" y2="12"></line>
                    <circle cx="6" cy="12" r="3"></circle>
                    <circle cx="18" cy="12" r="3"></circle>
                </svg>
            </div>
            <span class="logo-text">Tailor Pro</span>
            <span class="terminal-badge">Workshop Directory</span>
        </div>
        <div class="user-menu">
            <div class="api-status">
                <div class="status-dot" id="status-dot"></div>
                <span id="status-text">Connecting...</span>
            </div>
            <button class="btn-logout" id="logout-btn">Sign Out</button>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="container">
        
        <!-- Left Side Dashboard -->
        <div class="main-content">
            
            <!-- Summary stats row -->
            <div class="summary-grid">
                <div class="summary-card total-team">
                    <span class="summary-label">Total Workshop Staff</span>
                    <span class="summary-value" id="stat-total-team">0</span>
                </div>
                <div class="summary-card active-jobs">
                    <span class="summary-label">Active Orders</span>
                    <span class="summary-value" id="stat-active-jobs" style="color: #f472b6;">0</span>
                </div>
                <div class="summary-card completed-jobs">
                    <span class="summary-label">Workshop Utilization</span>
                    <span class="summary-value" id="stat-utilization" style="color: var(--success);">100%</span>
                </div>
            </div>

            <!-- Tailors Table Panel -->
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title-container">
                        <h2 class="panel-title">Workshop Team</h2>
                        <span class="panel-subtitle">Review workshop assignees and link team members</span>
                    </div>
                    <button class="btn-panel-action" id="open-add-dialog-btn">
                        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
                            <line x1="12" y1="5" x2="12" y2="19"></line>
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                        </svg>
                        Add Tailor Account
                    </button>
                </div>

                <div class="table-container">
                    <table id="tailors-table">
                        <thead>
                            <tr>
                                <th>Tailor Name</th>
                                <th>Phone Number</th>
                                <th>Email</th>
                                <th>Status</th>
                                <th style="text-align: right;">Action</th>
                            </tr>
                        </thead>
                        <tbody id="table-body">
                            <tr>
                                <td colspan="5" class="empty-table loading-shimmer" style="height: 15rem;"></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Table Pagination -->
                <div class="pagination-container">
                    <span class="pagination-text" id="pagination-info">Showing Page -- of --</span>
                    <div class="pagination-actions">
                        <button class="btn-page" id="prev-page-btn" disabled>Previous</button>
                        <button class="btn-page" id="next-page-btn" disabled>Next</button>
                    </div>
                </div>
            </div>

        </div>

        <!-- Right Side: Sidebar Panel -->
        <div class="panel sidebar" id="tailors-sidebar">
            <div class="sidebar-placeholder" id="sidebar-placeholder">
                <div class="placeholder-icon">
                    <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
                <h3 class="placeholder-title">Select Team Member</h3>
                <p class="placeholder-text">Click on any tailor row or select "Manage" to review profile credentials and system details.</p>
            </div>

            <div class="sidebar-content" id="sidebar-content" style="display: none;">
                <div>
                    <h3 class="panel-title" id="side-tailor-title" style="margin-bottom: 0.25rem;">Tailor Profile</h3>
                    <span class="panel-subtitle" id="side-tailor-subtitle">Workshop assignee details</span>
                </div>

                <!-- Profile Metadata Info -->
                <div>
                    <h4 class="sidebar-section-title">Unique Reference</h4>
                    <div class="meta-grid">
                        <div class="meta-item">
                            <span class="meta-label">Assigned Database ID</span>
                            <span class="meta-value" id="side-meta-id" style="font-family: monospace; font-size: 0.8rem; word-break: break-all;">--</span>
                        </div>
                    </div>
                </div>

                <!-- Account info -->
                <div>
                    <h4 class="sidebar-section-title">Contact & System details</h4>
                    <div class="meta-grid" style="gap: 0.75rem;">
                        <div class="meta-item">
                            <span class="meta-label">Phone Number</span>
                            <span class="meta-value" id="side-meta-phone">--</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Email Address</span>
                            <span class="meta-value" id="side-meta-email">--</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Account Status</span>
                            <span class="meta-value" id="side-meta-status">--</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Add/Assign Tailor Dialog Overlay -->
    <div class="dialog-overlay" id="add-dialog-overlay">
        <div class="dialog">
            <div class="dialog-close" id="close-dialog-btn">✕</div>
            
            <h3 class="panel-title" style="margin-bottom: 1rem;">Add Tailor Account</h3>
            
            <!-- Tab switches -->
            <div class="tabs-header">
                <button class="tab-btn active" id="tab-create-btn">Create New Account</button>
                <button class="tab-btn" id="tab-assign-btn">Assign Existing</button>
            </div>

            <!-- TAB 1: Create new Tailor -->
            <div id="tab-create-content">
                <form id="create-tailor-form" onsubmit="handleCreateTailor(event)">
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label" for="create-name">Full Name</label>
                            <input type="text" id="create-name" class="input-text" required placeholder="Tailor Name">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="create-phone">Phone Number</label>
                            <input type="text" id="create-phone" class="input-text" required placeholder="0911...">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="create-email">Email (Optional)</label>
                            <input type="email" id="create-email" class="input-text" placeholder="name@example.com">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="create-address">Address (Optional)</label>
                            <input type="text" id="create-address" class="input-text" placeholder="Addis Ababa">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="create-pass">Password</label>
                            <input type="password" id="create-pass" class="input-text" required minlength="8" placeholder="Password">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="create-confirm">Confirm Password</label>
                            <input type="password" id="create-confirm" class="input-text" required minlength="8" placeholder="Confirm">
                        </div>
                    </div>
                    
                    <button type="submit" class="btn-submit" id="create-submit-btn" style="width: 100%; margin-top: 1.5rem;">
                        <svg class="spinner" viewBox="0 0 50 50" id="create-spinner">
                            <circle cx="25" cy="25" r="20" stroke="currentColor" fill="none"></circle>
                        </svg>
                        <span>Create Workshop Account</span>
                    </button>
                </form>
            </div>

            <!-- TAB 2: Assign Existing tailor by Phone -->
            <div id="tab-assign-content" style="display: none;">
                <div class="form-group">
                    <label class="form-label">Search Tailor by Phone</label>
                    <div class="lookup-box">
                        <input type="text" id="assign-phone-input" class="input-text" placeholder="e.g. 0911...">
                        <button class="btn-lookup" id="btn-lookup-phone">Find Account</button>
                    </div>
                </div>

                <!-- Found Tailor Preview -->
                <div class="tailor-card-preview" id="tailor-preview-card" style="display: none;">
                    <div class="preview-header">
                        <div class="avatar-initial" id="preview-avatar">T</div>
                        <div>
                            <div class="customer-name-cell" id="preview-name">Tailor Name</div>
                            <div class="user-email-cell" id="preview-phone">0911...</div>
                        </div>
                    </div>
                    <button class="btn-submit" id="btn-confirm-assign" style="width: 100%;">
                        <svg class="spinner" viewBox="0 0 50 50" id="assign-spinner">
                            <circle cx="25" cy="25" r="20" stroke="currentColor" fill="none"></circle>
                        </svg>
                        <span>Link Tailor Account to Shop</span>
                    </button>
                </div>
            </div>

        </div>
    </div>

    <!-- Authentication Overlay Modal -->
    <div class="modal-overlay" id="auth-modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <div class="modal-logo">
                    <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <line x1="6" y1="3" x2="6" y2="21"></line>
                        <line x1="18" y1="3" x2="18" y2="21"></line>
                        <line x1="6" y1="12" x2="18" y2="12"></line>
                        <circle cx="6" cy="12" r="3"></circle>
                        <circle cx="18" cy="12" r="3"></circle>
                    </svg>
                </div>
                <h2 class="modal-title">Identity Verification</h2>
                <p class="modal-subtitle">Sign in with owner/superadmin credentials to access the tailors management terminal</p>
            </div>
            
            <form class="modal-form" onsubmit="handleLoginSubmit(event)">
                <input type="text" id="login-identifier" class="input-field" placeholder="Email or Phone Number" required autocomplete="username">
                <input type="password" id="login-password" class="input-field" placeholder="Access Password" required autocomplete="current-password">
                <button type="submit" class="btn-login" id="login-btn-submit">
                    <svg class="spinner" viewBox="0 0 50 50" id="login-spinner">
                        <circle cx="25" cy="25" r="20" stroke="currentColor" fill="none"></circle>
                    </svg>
                    <span id="login-btn-text">Sign In & Connect</span>
                </button>
            </form>
        </div>
    </div>

    <!-- Toast Notifications Area -->
    <div id="toast-container"></div>

    <!-- Page Logic & API Client integration -->
    <script>
        const API_BASE = "http://localhost:5000/api";
        const TOKEN_KEY = "tsms_token";
        
        let currentPage = 1;
        let selectedTailorId = null;
        let allTailors = [];
        let totalPagesCount = 1;
        let foundTailorObj = null;

        // Toast Helper
        function showToast(message, type = "success") {
            const container = document.getElementById("toast-container");
            const toast = document.createElement("div");
            toast.className = `toast ${type}`;
            
            const icon = type === "success" 
                ? `<div class="toast-icon">✓</div>` 
                : `<div class="toast-icon">✗</div>`;
                
            toast.innerHTML = `
                ${icon}
                <span>${message}</span>
            `;
            
            container.appendChild(toast);
            
            // Trigger animation
            setTimeout(() => toast.classList.add("show"), 10);
            
            // Auto dismiss
            setTimeout(() => {
                toast.classList.remove("show");
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }

        // Token Management
        function getToken() {
            return localStorage.getItem(TOKEN_KEY);
        }

        function setToken(token) {
            localStorage.setItem(TOKEN_KEY, token);
        }

        function clearToken() {
            localStorage.removeItem(TOKEN_KEY);
            selectedTailorId = null;
            document.getElementById("sidebar-content").style.display = "none";
            document.getElementById("sidebar-placeholder").style.display = "flex";
        }

        // Authenticated API request wrapper
        async function fetchAPI(endpoint, options = {}) {
            const token = getToken();
            const headers = {
                "Content-Type": "application/json",
                ...options.headers
            };
            
            if (token) {
                headers["Authorization"] = `Bearer ${token}`;
            }

            try {
                const response = await fetch(`${API_BASE}${endpoint}`, {
                    ...options,
                    headers
                });

                if (response.status === 401) {
                    clearToken();
                    updateStatusDisplay(false, "Session Expired");
                    showAuthModal();
                    throw new Error("Unauthorized - JWT token expired or invalid");
                }

                if (!response.ok) {
                    const errorDetails = await response.json().catch(() => ({}));
                    throw new Error(errorDetails.message || `API error - status: ${response.status}`);
                }

                updateStatusDisplay(true, "Connected");
                return await response.json();
            } catch (err) {
                console.error("API Call failure:", err);
                if (err.message.includes("Failed to fetch") || err.message.includes("NetworkError")) {
                    updateStatusDisplay(false, "Server Offline");
                    showToast("Cannot connect to backend API server. Verify it is running.", "error");
                }
                throw err;
            }
        }

        // Update top status indicator
        function updateStatusDisplay(connected, text) {
            const dot = document.getElementById("status-dot");
            const label = document.getElementById("status-text");
            if (connected) {
                dot.classList.remove("disconnected");
                label.textContent = text;
            } else {
                dot.classList.add("disconnected");
                label.textContent = text;
            }
        }

        // Modal triggers
        function showAuthModal() {
            document.getElementById("auth-modal-overlay").classList.add("active");
        }

        function hideAuthModal() {
            document.getElementById("auth-modal-overlay").classList.remove("active");
        }

        // Statistics helper
        async function loadTailorStats() {
            try {
                const [tailorsRes, analyticsRes] = await Promise.all([
                    fetchAPI("/users/tailors?limit=1000"),
                    fetchAPI("/analytics/summary")
                ]);

                const list = tailorsRes.data?.tailors ?? tailorsRes.tailors ?? [];
                const analytics = analyticsRes.data ?? analyticsRes;

                document.getElementById("stat-total-team").textContent = list.length;
                document.getElementById("stat-active-jobs").textContent = analytics.active_orders_count || 0;
            } catch (e) {
                console.error("Failed loading stats", e);
            }
        }

        // Load tailors registry list
        async function loadTailorsDirectory(page = 1) {
            const tableBody = document.getElementById("table-body");
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="empty-table loading-shimmer" style="height: 15rem;"></td>
                </tr>
            `;

            try {
                const limit = 10;
                const endpoint = `/users/tailors?page=${page}&limit=${limit}`;
                const res = await fetchAPI(endpoint);
                const tailorsData = res.data ?? res;
                
                allTailors = Array.isArray(tailorsData) ? tailorsData : tailorsData.tailors ?? [];
                totalPagesCount = tailorsData.pagination?.totalPages ?? 1;
                currentPage = page;

                renderTailorsTable();
                updatePaginationControls();
            } catch (e) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="empty-table">
                            <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="8" x2="12" y2="12"></line>
                                <line x1="12" y1="16" x2="12.01" y2="16"></line>
                            </svg>
                            <p>Failed to load tailor accounts registry.</p>
                        </td>
                    </tr>
                `;
                console.error("Failed loading tailor details", e);
            }
        }

        // Render table
        function renderTailorsTable() {
            const tableBody = document.getElementById("table-body");
            tableBody.innerHTML = "";

            if (allTailors.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="empty-table">
                            <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <circle cx="11" cy="11" r="8"></circle>
                                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                            </svg>
                            <p>No workshop staff records found.</p>
                        </td>
                    </tr>
                `;
                return;
            }

            allTailors.forEach(t => {
                const name = t.fullName || "—";
                const phone = t.phoneNumber || "—";
                const email = t.email || "—";
                const initial = name[0]?.toUpperCase() || "?";
                
                const isSelected = t._id === selectedTailorId;
                const rowClass = isSelected ? 'table-row selected' : 'table-row';
                
                const tr = document.createElement("tr");
                tr.className = rowClass;
                tr.onclick = () => selectTailor(t._id);
                
                tr.innerHTML = `
                    <td>
                        <div class="tailor-identity">
                            <div class="avatar-initial">${initial}</div>
                            <span class="tailor-name-cell">${name}</span>
                        </div>
                    </td>
                    <td style="color: var(--text-secondary); font-weight: 500;">${phone}</td>
                    <td style="color: var(--text-muted);">${email}</td>
                    <td>
                        <span class="status-badge ${t.status || 'active'}">
                            <span class="badge-dot"></span>
                            ${t.status || 'active'}
                        </span>
                    </td>
                    <td style="text-align: right;">
                        <button class="btn-manage" onclick="event.stopPropagation(); selectTailor('${t._id}')">Manage</button>
                    </td>
                `;
                tableBody.appendChild(tr);
            });
        }

        // Pagination updates
        function updatePaginationControls() {
            document.getElementById("pagination-info").textContent = `Showing Page ${currentPage} of ${totalPagesCount}`;
            document.getElementById("prev-page-btn").disabled = currentPage <= 1;
            document.getElementById("next-page-btn").disabled = currentPage >= totalPagesCount;
        }

        // Select Tailor profile
        function selectTailor(tailorId) {
            selectedTailorId = tailorId;
            renderTailorsTable();

            const placeholder = document.getElementById("sidebar-placeholder");
            const content = document.getElementById("sidebar-content");
            
            placeholder.style.display = "none";
            content.style.display = "block";

            const tailor = allTailors.find(t => t._id === tailorId);
            if (!tailor) return;

            document.getElementById("side-tailor-title").textContent = tailor.fullName;
            document.getElementById("side-meta-id").textContent = tailor._id;
            document.getElementById("side-meta-phone").textContent = tailor.phoneNumber || "—";
            document.getElementById("side-meta-email").textContent = tailor.email || "—";
            document.getElementById("side-meta-status").textContent = tailor.status || "active";
        }

        // Handle Admin Login
        async function handleLoginSubmit(event) {
            event.preventDefault();
            
            const identifier = document.getElementById("login-identifier").value.trim();
            const password = document.getElementById("login-password").value;
            
            const spinner = document.getElementById("login-spinner");
            const btnText = document.getElementById("login-btn-text");
            const submitBtn = document.getElementById("login-btn-submit");

            spinner.style.display = "inline-block";
            btnText.textContent = "Verifying...";
            submitBtn.disabled = true;

            try {
                const response = await fetch(`${API_BASE}/auth/login`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ identifier, password })
                });

                if (!response.ok) {
                    const err = await response.json().catch(() => ({}));
                    throw new Error(err.message || "Failed to authenticate.");
                }

                const resData = await response.json();
                
                // Check if user is owner/superadmin
                const userObj = resData.data?.user ?? resData.user ?? {};
                if (userObj.role !== "owner" && userObj.role !== "superadmin") {
                    throw new Error("Access Denied: Only shop owners and administrators can access the tailors list.");
                }

                const token = resData.token;
                setToken(token);
                showToast("Identity verified! Loading workshop staff directory.");
                hideAuthModal();
                
                // Refresh list
                loadTailorStats();
                loadTailorsDirectory(1);

            } catch (e) {
                showToast(e.message || "Authentication credentials incorrect.", "error");
                console.error("Login verification failed:", e);
            } finally {
                spinner.style.display = "none";
                btnText.textContent = "Sign In & Connect";
                submitBtn.disabled = false;
            }
        }

        // Create New Tailor account
        async function handleCreateTailor(event) {
            event.preventDefault();

            const fullName = document.getElementById("create-name").value.trim();
            const phoneNumber = document.getElementById("create-phone").value.trim();
            const email = document.getElementById("create-email").value.trim();
            const address = document.getElementById("create-address").value.trim();
            const password = document.getElementById("create-pass").value;
            const passwordConfirm = document.getElementById("create-confirm").value;

            if (password !== passwordConfirm) {
                showToast("Passwords do not match.", "error");
                return;
            }

            const spinner = document.getElementById("create-spinner");
            const submitBtn = document.getElementById("create-submit-btn");

            spinner.style.display = "inline-block";
            submitBtn.disabled = true;

            try {
                await fetchAPI("/users/create-tailor", {
                    method: "POST",
                    body: JSON.stringify({
                        fullName,
                        phoneNumber,
                        email,
                        address,
                        password
                    })
                });

                showToast("Workshop tailor account created successfully!");
                document.getElementById("create-tailor-form").reset();
                document.getElementById("add-dialog-overlay").classList.remove("active");
                
                await loadTailorStats();
                await loadTailorsDirectory(1);
            } catch (err) {
                console.error("Failed creating tailor", err);
                showToast(err.message || "Failed to create tailor account.", "error");
            } finally {
                spinner.style.display = "none";
                submitBtn.disabled = false;
            }
        }

        // Search Existing Tailor by Phone lookup
        document.getElementById("btn-lookup-phone").onclick = async () => {
            const assignPhone = document.getElementById("assign-phone-input").value.trim();
            if (!assignPhone) return;

            try {
                const res = await fetchAPI(`/users/tailors/by-phone/${assignPhone}`);
                const data = res.data ?? res;
                foundTailorObj = data.tailor ?? data.user ?? data;

                if (foundTailorObj) {
                    document.getElementById("preview-name").textContent = foundTailorObj.fullName;
                    document.getElementById("preview-phone").textContent = foundTailorObj.phoneNumber;
                    document.getElementById("preview-avatar").textContent = foundTailorObj.fullName[0]?.toUpperCase() || "T";
                    document.getElementById("tailor-preview-card").style.display = "block";
                    showToast("Tailor account located!");
                } else {
                    throw new Error("No tailor account located with this phone number.");
                }
            } catch (err) {
                console.error("Tailor lookup failed", err);
                showToast(err.message || "Failed to find existing tailor account.", "error");
                document.getElementById("tailor-preview-card").style.display = "none";
                foundTailorObj = null;
            }
        };

        // Confirm assign linking existing tailor
        document.getElementById("btn-confirm-assign").onclick = async () => {
            if (!foundTailorObj) return;

            const spinner = document.getElementById("assign-spinner");
            const submitBtn = document.getElementById("btn-confirm-assign");

            spinner.style.display = "inline-block";
            submitBtn.disabled = true;

            try {
                await fetchAPI("/auth/assign-tailor-by-phone", {
                    method: "POST",
                    body: JSON.stringify({ phoneNumber: foundTailorObj.phoneNumber })
                });

                showToast("Tailor account successfully linked to workshop!");
                document.getElementById("tailor-preview-card").style.display = "none";
                document.getElementById("assign-phone-input").value = "";
                document.getElementById("add-dialog-overlay").classList.remove("active");

                await loadTailorStats();
                await loadTailorsDirectory(1);
            } catch (err) {
                console.error("Assigning tailor linking failed", err);
                showToast(err.message || "Failed to link tailor account.", "error");
            } finally {
                spinner.style.display = "none";
                submitBtn.disabled = false;
            }
        };

        // Dialog toggle handlers
        document.getElementById("open-add-dialog-btn").onclick = () => {
            document.getElementById("add-dialog-overlay").classList.add("active");
        };

        document.getElementById("close-dialog-btn").onclick = () => {
            document.getElementById("add-dialog-overlay").classList.remove("active");
        };

        // Dialog tab toggle handlers
        document.getElementById("tab-create-btn").onclick = () => {
            document.getElementById("tab-create-btn").className = "tab-btn active";
            document.getElementById("tab-assign-btn").className = "tab-btn";
            document.getElementById("tab-create-content").style.display = "block";
            document.getElementById("tab-assign-content").style.display = "none";
        };

        document.getElementById("tab-assign-btn").onclick = () => {
            document.getElementById("tab-create-btn").className = "tab-btn";
            document.getElementById("tab-assign-btn").className = "tab-btn active";
            document.getElementById("tab-create-content").style.display = "none";
            document.getElementById("tab-assign-content").style.display = "block";
        };

        // Pagination setup
        document.getElementById("prev-page-btn").onclick = () => {
            if (currentPage > 1) {
                loadTailorsDirectory(currentPage - 1);
            }
        };

        document.getElementById("next-page-btn").onclick = () => {
            if (currentPage < totalPagesCount) {
                loadTailorsDirectory(currentPage + 1);
            }
        };

        document.getElementById("logout-btn").onclick = () => {
            clearToken();
            showToast("Logged out of tailor workshop terminal.");
            showAuthModal();
        };

        // Initialize App
        window.addEventListener("DOMContentLoaded", () => {
            const token = getToken();
            if (!token) {
                updateStatusDisplay(false, "Offline");
                showAuthModal();
            } else {
                updateStatusDisplay(true, "Connected");
                loadTailorStats();
                loadTailorsDirectory(1);
            }
        });
    </script>
</body>
</html>
"""

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Standardize routing for tailors directory
        if path in ('/', '/tailors', '/tailors/', '/index.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Path Not Found")

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Tailors UI Server running at http://localhost:{PORT}/tailors")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\nShutting down server...")
