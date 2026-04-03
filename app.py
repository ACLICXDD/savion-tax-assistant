from flask import Flask, request, redirect, url_for
import os
import uuid
from savion.parser import load_statement
from savion.rules import load_tax_rules
from savion.analysis import compute_eligible_savings
from savion.report import generate_html_report

app = Flask(__name__, static_folder='savion/static', static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'data/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Savion | Tax Planner</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-emerald: #10B981;
            --accent-violet: #7C3AED;
            --bg-dark: #0B0F19;
            --glass-bg: rgba(17, 24, 39, 0.6);
            --border-light: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            font-family: 'Outfit', sans-serif; 
            background: radial-gradient(circle at top right, #1a153a 0%, var(--bg-dark) 40%);
            color: var(--text-main); 
            min-height: 100vh;
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center;
            overflow-x: hidden;
        }

        /* Ambient glow effects behind card */
        .ambient-glow {
            position: absolute;
            width: 300px;
            height: 300px;
            background: var(--primary-emerald);
            filter: blur(150px);
            opacity: 0.15;
            z-index: 0;
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
        }

        .card { 
            background: var(--glass-bg); 
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            padding: 2.5rem; 
            border-radius: 20px; 
            border: 1px solid var(--border-light); 
            width: 100%; 
            max-width: 480px; 
            text-align: center;
            z-index: 10;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: floatUp 0.8s ease-out forwards;
        }

        @keyframes floatUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .logo-container {
            margin-bottom: 1.5rem;
        }
        
        /* Put the exact file name if you save the logo directly inside savion/static/ */
        .logo-container img {
            height: 80px;
            width: auto;
            object-fit: contain;
            margin-bottom: 0.5rem;
        }

        h2 {
            font-weight: 500;
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(to right, var(--primary-emerald), #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p.subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 2rem;
            line-height: 1.5;
        }

        .instructions-box {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-light);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 2rem;
            text-align: left;
        }

        .instructions-box h3 {
            font-size: 0.85rem;
            color: var(--text-main);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .instructions-box p {
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        .instructions-box code {
            background: rgba(255,255,255,0.05);
            padding: 2px 6px;
            border-radius: 4px;
            color: var(--primary-emerald);
            font-family: monospace;
            font-size: 0.8rem;
        }

        /* File Input Styling */
        .file-upload-wrapper {
            position: relative;
            margin-bottom: 1.5rem;
        }

        .file-upload-wrapper input[type="file"] {
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
            z-index: 2;
        }

        .file-upload-visual {
            background: rgba(16, 185, 129, 0.05);
            border: 1.5px dashed var(--primary-emerald);
            padding: 1.5rem;
            border-radius: 12px;
            color: var(--primary-emerald);
            transition: all 0.3s ease;
            z-index: 1;
        }

        .file-upload-wrapper:hover .file-upload-visual {
            background: rgba(16, 185, 129, 0.1);
            transform: translateY(-2px);
        }

        button { 
            background: linear-gradient(135deg, var(--primary-emerald), var(--accent-violet));
            color: white; 
            border: none; 
            padding: 14px 20px; 
            border-radius: 12px; 
            cursor: pointer; 
            font-size: 1rem; 
            font-family: inherit;
            font-weight: 500;
            width: 100%; 
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        }

        button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
        }
        
        button:active {
            transform: translateY(1px);
        }

        .error-message {
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="ambient-glow"></div>
    <div class="card">
        <div class="logo-container">
            <!-- Ensure you save the provided logo image as 'logo.png' in savion/static/ folder -->
            <img src="/static/logo.png" alt="Savion Logo" onerror="this.onerror=null; this.outerHTML='<h1>Savion</h1>';">
        </div>
        <h2>Tax Optimization Planner</h2>
        <p class="subtitle">Upload your bank statement to instantly discover eligible tax savings under Sections 80C & 80D.</p>
        
        <!-- Flash messages for errors -->
        {% if error_message %}
        <div class="error-message">
            <strong>Action Required:</strong> {{ error_message }}
        </div>
        {% endif %}

        <div class="instructions-box">
            <h3>Required CSV Format</h3>
            <p>Your statement must include exactly these 4 column headers (case-sensitive):</p>
            <p style="margin-top: 0.5rem; text-align: center;"><code>Date</code>, <code>Description</code>, <code>Amount</code>, <code>Type</code></p>
        </div>

        <form method="POST" enctype="multipart/form-data">
            <div class="file-upload-wrapper">
                <input type="file" name="file" accept=".csv" required onchange="document.getElementById('file-name').innerText = this.files[0].name;">
                <div class="file-upload-visual">
                    <span id="file-name">Click or drag CSV here</span>
                </div>
            </div>
            <button type="submit">Generate AI Report</button>
        </form>
    </div>
</body>
</html>
"""

from flask import render_template_string

@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    
    if request.method == "POST":
        if "file" not in request.files:
            return render_template_string(HTML_FORM, error_message="No file uploaded.")
        
        file = request.files["file"]
        if file.filename == "":
            return render_template_string(HTML_FORM, error_message="You must select a file.")
        
        # Save file temporarily to process it
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}.csv")
        file.save(filepath)

        try:
            # Process using the exact same Savion logic
            df = load_statement(filepath)
            rules = load_tax_rules()
            result = compute_eligible_savings(df, rules)

            c_keywords = rules["sections"]["80C"]["instruments"]
            d_keywords = rules["sections"]["80D"]["instruments"]
            all_keywords = c_keywords + d_keywords
            filtered_df = df[df["Description"].str.contains("|".join(all_keywords), case=False, na=False)]

            recommendations = ["Consider investing in ELSS for higher returns.", "Max out your PPF contribution."]
            
            output_report_path = filepath.replace(".csv", "_report.html")
            
            # Generate HTML report
            generate_html_report(result, recommendations, filtered_df, output_path=output_report_path)

            # Read the generated HTML and send it back to the browser
            with open(output_report_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            return html_content
        except ValueError as e:
            # Catch our custom required column error and show it beautifully
            error_message = f"{str(e)}. Please correct your CSV and try again."
            return render_template_string(HTML_FORM, error_message=error_message)
        except Exception as e:
            error_message = f"Error processing file: {str(e)}"
            return render_template_string(HTML_FORM, error_message=error_message)

    return render_template_string(HTML_FORM, error_message=None)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
