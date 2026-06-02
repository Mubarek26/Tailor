import http.server
import socketserver
import os
import urllib.parse

PORT = 8083

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tailor Shop - Customers Directory</title>
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
            --primary: #06b6d4;
            --primary-glow: rgba(6, 182, 212, 0.15);
            --primary-gradient: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
            --success: #10b981;
            --success-bg: rgba(16, 185, 129, 0.1);
            --warning: #f59e0b;
            --warning-bg: rgba(245, 158, 11, 0.1);
            --danger: #ef4444;
            --danger-bg: rgba(239, 68, 68, 0.1);
            --font-main: 'Outfit', sans-serif;
            --shadow-lg: 0 20px 25px -5px rgb(0 0 0 / 0.5), 0 8px 10px -6px rgb(0 0 0 / 0.5);
            --shadow-glow: 0 0 30px rgba(6, 182, 212, 0.2);
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
                radial-gradient(at 0% 0%, rgba(6, 182, 212, 0.12) 0px, transparent 50%),
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
            box-shadow: 0 4px 10px rgba(6, 182, 212, 0.3);
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
            background: rgba(6, 182, 212, 0.15);
            border: 1px solid rgba(6, 182, 212, 0.3);
            color: #8be9fd;
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

        .summary-card.total-custs::before {
            background: linear-gradient(90deg, #06b6d4, #3b82f6);
        }

        .summary-card.active-ords::before {
            background: linear-gradient(90deg, #a855f7, #6366f1);
        }

        .summary-card.revenue-potential::before {
            background: linear-gradient(90deg, #10b981, #059669);
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

        /* Customers Table */
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
            background-color: rgba(6, 182, 212, 0.08);
        }

        .customer-identity {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .avatar-initial {
            width: 2.25rem;
            height: 2.25rem;
            border-radius: 50%;
            background: rgba(6, 182, 212, 0.15);
            color: var(--primary);
            font-weight: 700;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(6, 182, 212, 0.2);
        }

        .customer-name-cell {
            font-weight: 600;
        }

        .customer-code-cell {
            font-family: monospace;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--primary);
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
            box-shadow: 0 4px 10px rgba(6, 182, 212, 0.2);
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
            background: rgba(6, 182, 212, 0.08);
            border: 1px solid rgba(6, 182, 212, 0.2);
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

        /* Profile Editing Form */
        .profile-form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            background: rgba(6, 182, 212, 0.03);
            border: 1px solid rgba(6, 182, 212, 0.15);
            border-radius: 1.25rem;
            padding: 1.25rem;
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
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
        }

        .btn-submit:hover:not(:disabled) {
            opacity: 0.95;
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(6, 182, 212, 0.4);
        }

        .btn-submit:active:not(:disabled) {
            transform: translateY(0);
        }

        .btn-submit:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            box-shadow: none;
        }

        /* Order history details */
        .orders-list {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            max-height: 180px;
            overflow-y: auto;
            padding-right: 0.25rem;
        }

        .order-history-item {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            padding: 0.6rem 0.8rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
        }

        .order-history-info {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .order-id-label {
            font-family: monospace;
            font-weight: 700;
            color: var(--primary);
        }

        .order-status-badge {
            font-size: 0.65rem;
            text-transform: uppercase;
            font-weight: 700;
        }

        .order-price {
            font-weight: 700;
            color: var(--text-primary);
        }

        .no-orders-msg {
            text-align: center;
            padding: 1.5rem;
            border: 1px dashed var(--border-color);
            border-radius: 0.75rem;
            font-size: 0.8rem;
            color: var(--text-muted);
            font-style: italic;
        }

        /* Account Deletion Panel */
        .danger-panel {
            background: rgba(239, 68, 68, 0.03);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 1.25rem;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .danger-title {
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--danger);
        }

        .danger-desc {
            font-size: 0.75rem;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .btn-delete {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fca5a5;
            padding: 0.75rem;
            border-radius: 0.75rem;
            font-size: 0.9rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
        }

        .btn-delete:hover {
            background: var(--danger);
            border-color: transparent;
            color: white;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        }

        .spinner {
            animation: spin 1s linear infinite;
            width: 1.2rem;
            height: 1.2rem;
            display: none;
        }

        .spinner circle {
            stroke: currentColor;
            stroke-width: 4;
            fill: none;
            stroke-dasharray: 42;
            stroke-dashoffset: 14;
        }

        @keyframes spin {
            100% { transform: rotate(360deg); }
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
            box-shadow: 0 8px 20px rgba(6, 182, 212, 0.3);
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
            box-shadow: 0 4px 14px rgba(6, 182, 212, 0.3);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-login:hover {
            opacity: 0.95;
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.45);
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
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="logo-container">
            <div class="logo-icon">
                <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
            </div>
            <span class="logo-text">Tailor Pro</span>
            <span class="terminal-badge">Customer Directory</span>
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
                <div class="summary-card total-custs">
                    <span class="summary-label">Total Customers</span>
                    <span class="summary-value" id="stat-total-custs">0</span>
                </div>
                <div class="summary-card active-ords">
                    <span class="summary-label">Active Orders</span>
                    <span class="summary-value" id="stat-active-ords" style="color: #c084fc;">0</span>
                </div>
                <div class="summary-card revenue-potential">
                    <span class="summary-label">Outstanding Balances</span>
                    <span class="summary-value" id="stat-remaining-revenue" style="color: var(--success);">ETB 0</span>
                </div>
            </div>

            <!-- Customers Table Panel -->
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title-container">
                        <h2 class="panel-title">Customer Ledger</h2>
                        <span class="panel-subtitle">Review contact information and order history profiles</span>
                    </div>
                    <div class="controls-row">
                        <div class="search-wrapper">
                            <span class="search-icon">
                                <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                </svg>
                            </span>
                            <input type="text" class="search-input" id="search-bar" placeholder="Search by name or unique code...">
                        </div>
                    </div>
                </div>

                <div class="table-container">
                    <table id="customers-table">
                        <thead>
                            <tr>
                                <th>Customer Name</th>
                                <th>Code Reference</th>
                                <th>Phone Number</th>
                                <th style="text-align: right;">Action</th>
                            </tr>
                        </thead>
                        <tbody id="table-body">
                            <tr>
                                <td colspan="4" class="empty-table loading-shimmer" style="height: 15rem;"></td>
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
        <div class="panel sidebar" id="customers-sidebar">
            <div class="sidebar-placeholder" id="sidebar-placeholder">
                <div class="placeholder-icon">
                    <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </div>
                <h3 class="placeholder-title">Select Customer Profile</h3>
                <p class="placeholder-text">Click on any customer row or select "Manage" to view details, review order history, edit credentials, or delete records.</p>
            </div>

            <div class="sidebar-content" id="sidebar-content" style="display: none;">
                <div>
                    <h3 class="panel-title" id="side-cust-title" style="margin-bottom: 0.25rem;">Customer Details</h3>
                    <span class="panel-subtitle" id="side-cust-subtitle">Administrative profile controls</span>
                </div>

                <!-- Profile Metadata Info -->
                <div>
                    <h4 class="sidebar-section-title">Unique Reference</h4>
                    <div class="meta-grid">
                        <div class="meta-item">
                            <span class="meta-label">Customer Code</span>
                            <span class="meta-value customer-code-cell" id="side-meta-code">--</span>
                        </div>
                    </div>
                </div>

                <!-- Customer Order History Ledger -->
                <div>
                    <h4 class="sidebar-section-title">Order History Ledger</h4>
                    <div class="orders-list" id="side-orders-history">
                        <!-- Loaded orders lists -->
                    </div>
                </div>

                <!-- Profile Editing Form -->
                <div>
                    <h4 class="sidebar-section-title">Modify Credentials</h4>
                    <form class="profile-form" id="edit-profile-form" onsubmit="handleProfileSubmit(event)">
                        <div class="form-group">
                            <label class="form-label" for="edit-name">Customer Full Name</label>
                            <input type="text" id="edit-name" class="input-text" required placeholder="Customer Name">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="edit-phone">Contact Phone Number</label>
                            <input type="text" id="edit-phone" class="input-text" required placeholder="0912...">
                        </div>

                        <button type="submit" class="btn-submit" id="submit-profile-btn">
                            <svg class="spinner" viewBox="0 0 50 50" id="form-spinner">
                                <circle cx="25" cy="25" r="20" stroke="currentColor" fill="none"></circle>
                            </svg>
                            <span id="submit-btn-text">Save Profile Changes</span>
                        </button>
                    </form>
                </div>

                <!-- Danger Zone Delete Box -->
                <div>
                    <h4 class="sidebar-section-title" style="color: var(--danger); border-color: rgba(239,68,68,0.2);">Danger Zone</h4>
                    <div class="danger-panel">
                        <span class="danger-title">Delete Account Permanent</span>
                        <p class="danger-desc">This action removes all database records associated with this customer. It is irreversible.</p>
                        <button class="btn-delete" onclick="handleDeleteCustomer()">Delete Customer Account</button>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Authentication Overlay Modal -->
    <div class="modal-overlay" id="auth-modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <div class="modal-logo">
                    <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="9" cy="7" r="4"></circle>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                </div>
                <h2 class="modal-title">Identity Verification</h2>
                <p class="modal-subtitle">Sign in with owner/superadmin credentials to access the customer management terminal</p>
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
        let selectedCustomerId = null;
        let allCustomers = [];
        let totalPagesCount = 1;
        let activeSearchQuery = "";

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
            selectedCustomerId = null;
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

                if (response.status === 204) {
                    return null;
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

        // Format Currency utility
        function formatETB(value) {
            const num = Number(value || 0);
            return `ETB ${num.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;
        }

        // Fetch Customer Statistics & Orders Potential
        async function loadCustomerStats() {
            try {
                // Fetch stats based on current database
                const [custRes, analyticsRes] = await Promise.all([
                    fetchAPI("/customers?limit=1000"),
                    fetchAPI("/analytics/summary")
                ]);
                
                const list = custRes.data?.customers ?? custRes.customers ?? [];
                const analytics = analyticsRes.data ?? analyticsRes;

                document.getElementById("stat-total-custs").textContent = list.length;
                document.getElementById("stat-active-ords").textContent = analytics.active_orders_count || 0;
                document.getElementById("stat-remaining-revenue").textContent = formatETB(analytics.total_remaining || 0);
            } catch (e) {
                console.error("Failed loading summary statistics", e);
            }
        }

        // Load customers registry list
        async function loadCustomersDirectory(page = 1) {
            const tableBody = document.getElementById("table-body");
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="empty-table loading-shimmer" style="height: 15rem;"></td>
                </tr>
            `;

            try {
                const limit = 10;
                let endpoint = `/customers?page=${page}&limit=${limit}`;
                if (activeSearchQuery) {
                    endpoint += `&name=${encodeURIComponent(activeSearchQuery)}`;
                }
                
                const res = await fetchAPI(endpoint);
                const customersData = res.data ?? res;
                
                allCustomers = Array.isArray(customersData) ? customersData : customersData.customers ?? [];
                totalPagesCount = customersData.pagination?.totalPages ?? 1;
                currentPage = page;

                renderCustomersTable();
                updatePaginationControls();
            } catch (e) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="empty-table">
                            <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="8" x2="12" y2="12"></line>
                                <line x1="12" y1="16" x2="12.01" y2="16"></line>
                            </svg>
                            <p>Failed to load customer profiles.</p>
                        </td>
                    </tr>
                `;
                console.error("Failed loading customer registry details", e);
            }
        }

        // Render table
        function renderCustomersTable() {
            const tableBody = document.getElementById("table-body");
            tableBody.innerHTML = "";

            if (allCustomers.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="empty-table">
                            <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <circle cx="11" cy="11" r="8"></circle>
                                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                            </svg>
                            <p>No customer records found.</p>
                        </td>
                    </tr>
                `;
                return;
            }

            allCustomers.forEach(c => {
                const name = c.name || "—";
                const phone = c.phone || "—";
                const code = c.unique_code ? `#${c.unique_code}` : "—";
                const initial = name[0]?.toUpperCase() || "?";
                
                const isSelected = c._id === selectedCustomerId;
                const rowClass = isSelected ? 'table-row selected' : 'table-row';
                
                const tr = document.createElement("tr");
                tr.className = rowClass;
                tr.onclick = () => selectCustomer(c._id);
                
                tr.innerHTML = `
                    <td>
                        <div class="customer-identity">
                            <div class="avatar-initial">${initial}</div>
                            <span class="customer-name-cell">${name}</span>
                        </div>
                    </td>
                    <td class="customer-code-cell">${code}</td>
                    <td style="color: var(--text-secondary); font-weight: 500;">${phone}</td>
                    <td style="text-align: right;">
                        <button class="btn-manage" onclick="event.stopPropagation(); selectCustomer('${c._id}')">Manage</button>
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

        // Select Customer profile
        async function selectCustomer(customerId) {
            selectedCustomerId = customerId;
            renderCustomersTable();

            const placeholder = document.getElementById("sidebar-placeholder");
            const content = document.getElementById("sidebar-content");
            
            placeholder.style.display = "none";
            content.style.display = "block";

            // Reset values
            document.getElementById("side-cust-title").textContent = "Loading Profile details...";
            document.getElementById("side-meta-code").textContent = "--";
            document.getElementById("side-orders-history").innerHTML = `<div class="no-orders-msg">Fetching order ledger...</div>`;
            
            try {
                // Fetch customer details and orders concurrently
                const [custsRes, ordersRes] = await Promise.all([
                    fetchAPI(`/customers?limit=1000`),
                    fetchAPI(`/customers/${customerId}/orders`)
                ]);

                // Find specific customer
                const list = custsRes.data?.customers ?? custsRes.customers ?? [];
                const customer = list.find(c => c._id === customerId);

                if (!customer) throw new Error("Customer profile details not found in directory.");

                const ordersData = ordersRes.data ?? ordersRes;
                const ordersList = ordersData.customerOrders || ordersData.orders || [];

                document.getElementById("side-cust-title").textContent = customer.name;
                document.getElementById("side-meta-code").textContent = customer.unique_code ? `#${customer.unique_code}` : "—";
                
                // Form setup
                document.getElementById("edit-name").value = customer.name || "";
                document.getElementById("edit-phone").value = customer.phone || "";

                // Render order lists
                const orderContainer = document.getElementById("side-orders-history");
                orderContainer.innerHTML = "";

                if (ordersList.length === 0) {
                    orderContainer.innerHTML = `<div class="no-orders-msg">No order records registered for this customer.</div>`;
                } else {
                    ordersList.forEach(item => {
                        const o = item.order || item;
                        const codeLabel = o._id.slice(-6).toUpperCase();
                        
                        const div = document.createElement("div");
                        div.className = "order-history-item";
                        div.innerHTML = `
                            <div class="order-history-info">
                                <span class="order-id-label">#${codeLabel}</span>
                                <span class="order-status-badge" style="color: var(--text-secondary);">${o.status}</span>
                            </div>
                            <span class="order-price">${formatETB(o.total_price)}</span>
                        `;
                        orderContainer.appendChild(div);
                    });
                }

            } catch (err) {
                console.error("Failed loading selected customer details", err);
                placeholder.style.display = "flex";
                content.style.display = "none";
                showToast("Could not load contact details or order ledger.", "error");
            }
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
                    throw new Error("Access Denied: Only shop owners and administrators can access the customer records directory.");
                }

                const token = resData.token;
                setToken(token);
                showToast("Identity verified! Loading customer ledger.");
                hideAuthModal();
                
                // Refresh list
                loadCustomerStats();
                loadCustomersDirectory(1);

            } catch (e) {
                showToast(e.message || "Authentication credentials incorrect.", "error");
                console.error("Login verification failed:", e);
            } finally {
                spinner.style.display = "none";
                btnText.textContent = "Sign In & Connect";
                submitBtn.disabled = false;
            }
        }

        // Handle Profile Edit Submission
        async function handleProfileSubmit(event) {
            event.preventDefault();
            
            if (!selectedCustomerId) return;

            const name = document.getElementById("edit-name").value.trim();
            const phone = document.getElementById("edit-phone").value.trim();

            const spinner = document.getElementById("form-spinner");
            const btnText = document.getElementById("submit-btn-text");
            const submitBtn = document.getElementById("submit-profile-btn");

            spinner.style.display = "inline-block";
            btnText.textContent = "Updating...";
            submitBtn.disabled = true;

            try {
                await fetchAPI(`/customers/${selectedCustomerId}`, {
                    method: "PUT",
                    body: JSON.stringify({
                        name,
                        phone
                    })
                });

                showToast("Customer profile details updated successfully!");
                
                await loadCustomerStats();
                await loadCustomersDirectory(currentPage);
                await selectCustomer(selectedCustomerId);
            } catch (err) {
                console.error("Failed updating customer profile", err);
                showToast(err.message || "Failed to update profile details.", "error");
            } finally {
                spinner.style.display = "none";
                btnText.textContent = "Save Profile Changes";
                submitBtn.disabled = false;
            }
        }

        // Handle Customer Account Deletion
        async function handleDeleteCustomer() {
            if (!selectedCustomerId) return;
            
            const confirmed = confirm("Are you sure you want to permanently delete this customer profile? All contact records will be destroyed.");
            if (!confirmed) return;

            try {
                await fetchAPI(`/customers/${selectedCustomerId}`, {
                    method: "DELETE"
                });

                showToast("Customer profile successfully deleted.");
                
                selectedCustomerId = null;
                document.getElementById("sidebar-content").style.display = "none";
                document.getElementById("sidebar-placeholder").style.display = "flex";

                await loadCustomerStats();
                await loadCustomersDirectory(1);
            } catch (err) {
                console.error("Failed deleting customer account", err);
                showToast(err.message || "Failed to delete customer profile details.", "error");
            }
        }

        // Setup Event Handlers
        document.getElementById("prev-page-btn").onclick = () => {
            if (currentPage > 1) {
                loadCustomersDirectory(currentPage - 1);
            }
        };

        document.getElementById("next-page-btn").onclick = () => {
            if (currentPage < totalPagesCount) {
                loadCustomersDirectory(currentPage + 1);
            }
        };

        // Server-side filter triggers instantly on search input typing
        let searchDebounceTimeout = null;
        document.getElementById("search-bar").oninput = (e) => {
            activeSearchQuery = e.target.value;
            clearTimeout(searchDebounceTimeout);
            searchDebounceTimeout = setTimeout(() => {
                loadCustomersDirectory(1);
            }, 300);
        };

        document.getElementById("logout-btn").onclick = () => {
            clearToken();
            showToast("Logged out of customer management terminal.");
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
                loadCustomerStats();
                loadCustomersDirectory(1);
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
        
        # Standardize routing for customers dashboard
        if path in ('/', '/customers', '/customers/', '/index.html'):
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
        print(f"Customers UI Server running at http://localhost:{PORT}/customers")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\nShutting down server...")
