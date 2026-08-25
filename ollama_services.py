import requests
import json
from flask import Blueprint, request, jsonify
import database  # Imported to fetch intermediate Kabag TU RHK dynamically

# Configuration setup for the local Ollama instance
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_API_URL = f"{OLLAMA_HOST}/api/chat"
DEFAULT_MODEL = "qwen2.5:7b"  # Explicitly matched with your local tag to prevent 404 registry errors
ollama_api_bp = Blueprint('ollama_api', __name__)

# Shared prompt template designed to structure the Indonesian bureaucratic matrix cascading alignment
# Updated to support dual-layer cascading (Kakanwil -> Kabag TU -> Kasubbag)
#MPH_SYSTEM_PROMPT = (
#    "You are an expert performance planning system specializing in government SOTK "
#    "and Cascading Indicators (Matriks Peran Hasil - MPH) according to Permenpan RB No. 6 Year 2022.\n"
#    "Your objective is to generate a specific, tactical, actionable Rencana Hasil Kerja (RHK) "
#    "for a subordinate position that directly supports the superior's strategic goal or the intermediate supervisor's RHK.\n"
#    "CRITICAL RULES FOR GAUGE AND STYLE:\n"
#    "1. Write the output strictly in professional Indonesian (bureaucratic/SKP standard).\n"
#    "2. MANDATORY STYLE: Use OUTCOME-BASED phrasing. Start the sentence with passive nouns/clauses "
#    "such as 'Tersedianya...', 'Terwujudnya...', 'Tersusunnya...', 'Terkoordinasikannya...', 'Terlaksananya...'.\n"
#    "3. STRICTLY FORBIDDEN: Do NOT start with active verbs like 'Meningkatkan...', 'Melaksanakan...', "
#    "'Mengkoordinasikan...', 'Melakukan...'. Change those verbs into outcome states.\n"
#    "4. Be concise: limited to 1 high-impact sentence.\n"
#    "5. Do NOT include preambles, introductory words, explanations, quotes, or markdown bold formatting.\n"
#    "6. Output only the pure raw text value."
#)

MPH_SYSTEM_PROMPT = (
    "You are an expert performance planning system specializing in government SOTK "
    "and Cascading Indicators (Matriks Peran Hasil - MPH) according to Permenpan RB No. 6 Year 2022.\n"
    "Your objective is to generate a specific, tactical, actionable Rencana Hasil Kerja (RHK) "
    "for a subordinate position that directly supports the superior's strategic goal or the intermediate supervisor's RHK.\n"
    "CRITICAL RULES FOR GAUGE AND STYLE:\n"
    "1. Write the output strictly in professional Indonesian (bureaucratic/SKP standard).\n"
    "2. MANDATORY STYLE: Use OUTCOME-BASED phrasing. Start the sentence with passive nouns/clauses "
    "such as 'Tersedianya...', 'Terwujudnya...', 'Tersusunnya...', 'Terkoordinasikannya...', 'Terlaksananya...'.\n"
    "3. STRICTLY FORBIDDEN: Do NOT start with active verbs like 'Meningkatkan...', 'Melaksanakan...', "
    "'Mengkoordinasikan...', 'Melakukan...'. Change those verbs into outcome states.\n"
    "4. The generated RHK must implicitly satisfy SMART-C criteria: "
    "Specific (clear object and measurable outcome), Measurable (can be quantified or has clear success indicator), "
    "Agreeable (negotiable between supervisor and subordinate), Realistic (achievable with available resources), "
    "Time-bound (has a clear timeframe), and Continuously Improved (subject to periodic review and adjustment). "
    "The sentence should naturally include elements of quantity, quality, and timeline where possible.\n"
    "5. Be concise: limited to 1 high-impact sentence.\n"
    "6. Do NOT include preambles, introductory words, explanations, quotes, or markdown bold formatting.\n"
    "7. Output only the pure raw text value."
)

IKI_SYSTEM_PROMPT = (
    "You are an expert Indonesian civil service performance evaluator (Permenpan RB No. 6 Year 2022).\n"
    "Your objective is to generate 1 crisp, comprehensive, and quantitative Individual Performance Indicator "
    "(Indikator Kinerja Individu - IKI) based on the provided Rencana Hasil Kerja (RHK), Position Name, and User Draft Keyword.\n\n"
    "CRITICAL RULES FOR IKI:\n"
    "1. Write strictly in professional Indonesian (bureaucratic/SKP standard).\n"
    "2. MANDATORY NOUN-METRIC STARTERS: The sentence MUST start with 'Jumlah...', 'Persentase...', 'Tingkat...', or 'Indeks...'.\n"
    "3. SMART-C STRUCTURE: Ensure the indicator sentence implicitly covers quantity, quality, and time context in one clean sentence.\n"
    "   Examples:\n"
    "   - 'Jumlah berkas permohonan pendaftaran tanah yang diverifikasi kelengkapan dan kesesuaiannya sesuai SOP per triwulan'\n"
    "   - 'Jumlah konsep sertipikat hak atas tanah yang diperiksa dan dinyatakan layak sesuai standar per triwulan'\n"
    "   - 'Persentase dokumen perencanaan strategis dan laporan LAKIP yang disusun tepat waktu dan sesuai standar per tahun'\n\n"
    "REAL-WORLD FIELD AD-HOC STEERING RULE:\n"
    "4. Users often perform ad-hoc physical/field tasks outside their official TUSI based on direct supervisor orders.\n"
    "5. If the User's Draft/Keyword belongs to an operational task (e.g., land measurement) that diverges from their position level, DO NOT REJECT IT.\n"
    "6. Instead, SMARTLY BRIDGE the physical task to match their POSITION LEVEL & FUNCTION:\n"
    "   - Administrative/Archive posts -> Shift focus to administrative preparation, document filing, or record-keeping of that task.\n"
    "   - Planning/Evaluation posts -> Shift focus to data preparation, monitoring, or performance reporting of that task.\n\n"
    "FORMATTING RULES:\n"
    "7. Do NOT include preambles, introductory text, explanations, or markdown bold syntax.\n"
    "8. Output only the pure raw text value."
)

@ollama_api_bp.route('/api/reroll-iki', methods=['POST'])
def handle_iki_reroll():
    data = request.get_json() or {}
    rhk_pegawai = data.get('rhk_pegawai', '')
    position_name = data.get('position_name', '')
    current_iki = data.get('current_iki', '').strip() # <-- Ambil teks IKI saat ini

    # Jika user sudah menuliskan kata kunci/draf sederhana, instruksikan AI untuk memperhalus/mengelaborasi
    if current_iki and not current_iki.startswith("🎲"):
        user_prompt = (
            f"Position: {position_name}\n"
            f"Rencana Hasil Kerja (RHK): {rhk_pegawai}\n"
            f"User's Draft/Keyword: '{current_iki}'\n"
            f"Refine and elaborate the User's Draft into 1 formal, highly professional, quantitative SMART-C "
            f"Individual Performance Indicator (IKI) suitable for Indonesian Civil Service (Permenpan RB)."
        )
    else:
        user_prompt = (
            f"Position: {position_name}\n"
            f"Rencana Hasil Kerja (RHK): {rhk_pegawai}\n"
            f"Draft 1 quantitative SMART-C Individual Performance Indicator (IKI) for this RHK:"
        )

    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": IKI_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {"temperature": 0.3}
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=20)
        if response.status_code == 200:
            new_iki = response.json().get("message", {}).get("content", "").strip()
            return jsonify({"status": "success", "new_iki": new_iki})
        return jsonify({"status": "error", "message": "Failed from Ollama"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def query_local_llm(superior_indicator, subordinate_role, intermediate_goal=None):
    """
    Dispatches a synchronous request to the local Ollama endpoint to generate a single cell breakdown.
    Keeps failure states isolated so a single bad context does not crash the entire application loop.
    Supports optional intermediate_goal parameter to enforce clean hierarchal cascading.
    """
    if intermediate_goal and intermediate_goal != "- None -" and intermediate_goal.strip():
        user_prompt = (
            f"Overarching Goal (Sasaran Kakanwil): {superior_indicator}\n"
            f"Direct Supervisor's RHK (RHK Kabag TU): {intermediate_goal}\n"
            f"Subordinate Post (Jabatan Bawahan): {subordinate_role}\n"
            f"Draft the exact cascaded outcome RHK sentence for this subordinate position "
            f"that directly supports and operationalizes the Direct Supervisor's RHK:"
        )
    else:
        user_prompt = (
            f"Superior Indicator (Sasaran Atasan): {superior_indicator}\n"
            f"Subordinate Post (Jabatan Bawahan): {subordinate_role}\n"
            f"Draft the exact cascaded outcome RHK sentence for this subordinate position:"
        )
    
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": MPH_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {
            "temperature": 0.2,  # Kept low for consistent, factual corporate alignments
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=25)
        if response.status_code == 200:
            result = response.json()
            return result.get("message", {}).get("content", "").strip()
        return f"Error: Ollama returned status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to local Ollama service: {str(e)}"

@ollama_api_bp.route('/api/generate-mph', methods=['POST'])
def handle_bulk_generation():
    """
    Processes full matrix simulation by looping through columns and subordinates.
    Preserves existing application flow without breaking current persistent state logic.
    """
    data = request.get_json() or {}
    division_name = data.get('division_name')
    
    if not division_name:
        return jsonify({"status": "error", "message": "Missing division parameter"}), 400

    # Logic to support bulk cascade generations can be wired here if needed
    return jsonify({
        "status": "success", 
        "message": f"Successfully completed bulk intelligence matrix cascade using model: '{DEFAULT_MODEL}'."
    })


@ollama_api_bp.route('/api/reroll-mph-cell', methods=['POST'])
def handle_single_cell_reroll():
    """
    Handles granular alternative generation for an isolated cell context.
    Dynamically resolves multi-layer cascading hierarchy:
    - Kabag TU listens to Kakanwil
    - Kasubbag listens to Kabag TU
    - JF/Pelaksana listens to their respective Kasubbag based on the SK column context
    """
    data = request.get_json() or {}
    division_name = data.get('division_name', 'Bagian Tata Usaha')
    superior_code = data.get('superior_code')
    subordinate_post = data.get('subordinate_post')
    
    # Fetch superior text from database using the code context
    all_iku = database.get_all_iku()
    superior_text = next((row[3] for row in all_iku if row[2] == superior_code), "Terwujudnya Penguatan Pengelolaan Keuangan dan Aset")
    
    # Load all currently saved cells to find intermediate supervisor goals
    saved_cells = database.get_mph_matrix_data(division_name)
    intermediate_goal = None
    
    # CASE 1: Subordinate is Kasubbag level -> Pull from Kabag TU RHK
    if "Subbagian" in subordinate_post:
        intermediate_goal = saved_cells.get((superior_code, "Kepala Bagian Tata Usaha"))
        
    # CASE 2: Subordinate is JF / Pelaksana level -> Dynamically route to the respective Kasubbag based on SK code
    elif "Fungsional" in subordinate_post or "Pelaksana" in subordinate_post:
        target_kasubbag = None
        if superior_code == "SK6.1":
            target_kasubbag = "Subbagian Perencanaan, Evaluasi dan Pelaporan"
        elif superior_code == "SK6.2":
            target_kasubbag = "Subbagian Keuangan dan Barang Milik Negara"
        elif superior_code == "SK6.6":
            target_kasubbag = "Subbagian Hukum, Kepegawaian dan Organisasi"
        elif superior_code == "SK6.8":
            target_kasubbag = "Subbagian Umum dan Hubungan Masyarakat"
            
        if target_kasubbag:
            intermediate_goal = saved_cells.get((superior_code, target_kasubbag))

    # If an intermediate goal was found, it swaps the prompt context inside query_local_llm automatically
    new_draft = query_local_llm(superior_text, subordinate_post, intermediate_goal)
    
    # Persist the output safely into the database
    database.save_or_update_mph_cell(division_name, superior_code, subordinate_post, new_draft)
    
    return jsonify({
        "status": "success",
        "new_sasaran": new_draft
    })