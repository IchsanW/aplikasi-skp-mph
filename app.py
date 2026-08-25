import os
import csv
from flask import Flask, render_template, jsonify, request, redirect, url_for
from ollama_services import ollama_api_bp
import database

app = Flask(__name__)
app.register_blueprint(ollama_api_bp)

@app.route('/')
def index():
    return render_template('main.html')

# Core route updated to handle manual forms, bulk CSV uploads, and truncation resets
@app.route('/renstra', methods=['GET', 'POST'])
def renstra_management():
    if request.method == 'POST':
        action = request.form.get('action')
        
        # Action 1: Reset and clear database table
        if action == 'clear':
            database.clear_all_iku()
            return redirect(url_for('renstra_management'))
            
        # Action 2: Process Bulk Upload via CSV File
        elif action == 'upload':
            if 'file' in request.files:
                file = request.files['file']
                if file.filename != '' and file.filename.endswith('.csv'):
                    # Read and decode the uploaded CSV file stream
                    stream = file.stream.read().decode("utf-8").splitlines()
                    csv_reader = csv.reader(stream)
                    
                    # Skip header row: level,code,title,aspect,target,owner_post,parent_code
                    next(csv_reader, None) 
                    
                    for row in csv_reader:
                        if len(row) >= 7:
                            database.insert_iku(
                                level=row[0].strip(),
                                code=row[1].strip(),
                                title=row[2].strip(),
                                aspect=row[3].strip(),
                                target=row[4].strip(),
                                owner_post=row[5].strip(),
                                parent_code=row[6].strip() if row[6].strip() else None
                            )
            return redirect(url_for('renstra_management'))
        
        # Action 3: Process Row Update / Edit Form
        elif action == 'update':
            record_id = request.form.get('id')
            level = request.form.get('level')
            code = request.form.get('code')
            title = request.form.get('title')
            aspect = request.form.get('aspect')
            target = request.form.get('target')
            owner_post = request.form.get('owner_post')
            parent_code = request.form.get('parent_code')
            
            database.update_iku(record_id, level, code, title, aspect, target, owner_post, parent_code)
            return redirect(url_for('renstra_management'))  
        
        # Action 4: Process Single Manual Entry Form
        else:
            level = request.form.get('level')
            code = request.form.get('code')
            title = request.form.get('title')
            aspect = request.form.get('aspect')
            target = request.form.get('target')
            owner_post = request.form.get('owner_post')
            parent_code = request.form.get('parent_code')
            
            database.insert_iku(level, code, title, aspect, target, owner_post, parent_code)
            return redirect(url_for('renstra_management'))
        
    iku_list = database.get_all_iku()
    return render_template('input_renstra.html', iku_list=iku_list)

@app.route('/api/cascade', methods=['POST'])
def run_cascade():
    return jsonify({
        "status": "success",
        "message": "AI Cascading process initiated successfully using Qwen2.5 via Ollama."
    })

DIVISION_MAP = {
    "TU": "Bagian Tata Usaha",
    "tu": "Bagian Tata Usaha", # handling lowercase fallback safely
    # You can add other divisions here in the future:
    # "INF": "Bagian Informasi Pertanahan",
}

@app.route('/mph/<division_name>')
def view_mph_matrix(division_name):
    """Renders the Matrix of Role Results (MPH) grid layout for a specific division."""
    # Translate short slug to actual database division name if matched, otherwise keep original
    resolved_division_name = DIVISION_MAP.get(division_name, division_name)
    
    # Fetch all Sasaran Kegiatan (SK) columns from Kakanwil level
    all_iku = database.get_all_iku()
    columns = [row for row in all_iku if row[1] == 'Kanwil' and row[2].startswith('SK')]
    
    # We construct the subordinates list dynamically starting with the Kabag TU
    subordinates = []
    
    # 1. Insert Kepala Bagian Tata Usaha as the first direct subordinate of Kakanwil
    if resolved_division_name == "Bagian Tata Usaha":
        subordinates.append((
            "Kepala Bagian Tata Usaha", 
            "Memimpin dan mengoordinasikan pelayanan administratif serta fasilitatif di lingkungan Kantor Wilayah.", 
            "-"
        ))
    
    # 2. Fetch the Sub-sections (Kasubbag) from the database
    db_subordinates = database.get_sub_units_by_parent(resolved_division_name)
    subordinates.extend(db_subordinates)
    
    # 3. Add the hardcoded Fungsional / Pelaksana row at the absolute bottom
    subordinates.append((
        "Kelompok Jabatan Fungsional / Pelaksana", 
        "Melaksanakan tugas teknis fungsional dan operasional.", 
        "-"
    ))
    
    # Load existing saved cells data from the database using the resolved name
    saved_cells = database.get_mph_matrix_data(resolved_division_name)
    
    return render_template(
        'mph.html', 
        division_name=resolved_division_name, 
        columns=columns, 
        subordinates=subordinates,
        saved_cells=saved_cells
    )

@app.route('/api/save-mph-cell', methods=['POST'])
def api_save_mph_cell():
    """Handles manual inline inline edits submitted by the performance administrator."""
    data = request.json
    database.save_or_update_mph_cell(
        division_name=data['division_name'],
        superior_code=data['superior_code'],
        subordinate_post=data['subordinate_post'],
        cascaded_sasaran=data['cascaded_sasaran']
    )
    return jsonify({"status": "success", "message": "Cell updated successfully"})

# Route to render Individual SKP Dashboard with dynamic RHK fetched from MPH database
# Route to render Individual SKP Dashboard with dynamic multi-IKI support
@app.route('/skp/<path:position_name>')
def view_individual_skp(position_name):
    division_name = "Bagian Tata Usaha"
    all_iku = database.get_all_iku()
    columns = [row for row in all_iku if row[1] == 'Kanwil' and row[2].startswith('SK')]
    
    saved_cells = database.get_mph_matrix_data(division_name)
    skp_rows = []
    row_counter = 1
    
    for col in columns:
        superior_code = col[2]
        superior_rhk = col[3]
        
        if position_name == "Kepala Bagian Tata Usaha":
            pimpinan_rhk = superior_rhk
        else:
            pimpinan_rhk = saved_cells.get((superior_code, "Kepala Bagian Tata Usaha"), superior_rhk)
            
        pegawai_rhk = saved_cells.get((superior_code, position_name), "").strip()
        
        # FILTER: Only include row if employee actually has an intervention/RHK assigned
        if pegawai_rhk and pegawai_rhk != "- None -":
            skp_rows.append({
                "no": row_counter,
                "superior_code": superior_code,
                "rhk_pimpinan": pimpinan_rhk,
                "rhk_pegawai": pegawai_rhk,
                # Initial default list containing 1 starting SMART-C IKI
                "iki_list": [
                    {
                        "id": 1,
                        "iki_text": f"Jumlah {pegawai_rhk.lower()} yang diselesaikan sesuai standar per triwulan",
                        "target": "100%"
                    }
                ]
            })
            row_counter += 1

    return render_template(
        'skp.html',
        position_name=position_name,
        division_name=division_name,
        skp_rows=skp_rows
    )

# @app.route('/api/generate-mph', methods=['POST'])
# def api_generate_mph():
#     """Stubs out the massive LLM generation context. Real LLM inference integration comes next."""
#     data = request.json
#     division_name = data['division_name']
    
#     # Fetch requirements to feed context
#     all_iku = database.get_all_iku()
#     columns = [row for row in all_iku if row[1] == 'Kanwil' and row[2].startswith('SK')]
#     subordinates = database.get_sub_units_by_parent(division_name)
#     subordinates.append(("Kelompok Jabatan Fungsional / Pelaksana", "Melaksanakan tugas teknis fungsional.", "-"))
    
#     # Temporary placeholder generation text before we hook up the active LLM prompt engine
#     for col in columns:
#         superior_code = col[2]
#         superior_title = col[3]
#         for sub in subordinates:
#             sub_post = sub[0]
#             placeholder_text = f"Drafting objective for {sub_post} supporting {superior_code} ({superior_title})"
#             database.save_or_update_mph_cell(division_name, superior_code, sub_post, placeholder_text)
            
#     return jsonify({"status": "success", "message": "Full matrix successfully pre-generated!"})

# @app.route('/api/reroll-mph-cell', methods=['POST'])
# def api_reroll_mph_cell():
#     """Stubs out a single cell LLM reroll invocation."""
#     data = request.json
#     # Placeholder response to verify connectivity before building the final prompt structure
#     new_draft = f"New AI Reroll Alternative Draft for {data['subordinate_post']} under {data['superior_code']}"
#     database.save_or_update_mph_cell(data['division_name'], data['superior_code'], data['subordinate_post'], new_draft)
#     return jsonify({"status": "success", "new_sasaran": new_draft})

if __name__ == '__main__':
    app.run(debug=True, port=5000)