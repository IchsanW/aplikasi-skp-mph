# seed_sotk.py
# Pure English code and comments as requested by Coder
import database

def inject_sotk_regulations():
    """Seeds the official SOTK mandates from Ministerial Regulation No. 17/2020 into the database."""
    print("Starting SOTK data injection...")
    
    # 1. Main Parent Unit: Bagian Tata Usaha
    database.insert_sotk(
        unit_level="Bagian",
        post_name="Bagian Tata Usaha",
        parent_post="Kantor Wilayah",
        main_duty="Melaksanakan pembinaan dan pemberian dukungan administrasi di lingkungan Kantor Wilayah.",
        functions=(
            "a. Pelaksanaan penyusunan rencana, program dan anggaran, serta pemantauan, evaluasi dan pelaporan; "
            "b. Pelaksanaan urusan organisasi, ketatalaksanaan, analisis jabatan, pengelolaan urusan kepegawaian dan pembinaan jabatan fungsional; "
            "c. Pengoordinasian dan pelaksanaan fasilitasi reformasi birokrasi di Kantor Wilayah dan Kantor Pertanahan; "
            "d. Pengoordinasian dan fasilitasi advokasi hukum dan peraturan perundang-undangan; "
            "e. Pengelolaan urusan keuangan dan barang milik negara; "
            "f. Pelaksanaan urusan ketatausahaan, digitalisasi arsip, rumah tangga, protokol, perlengkapan, dan penyelenggaraan layanan pengadaan; "
            "g. Pengoordinasian dan fasilitasi pengelolaan pelayanan pertanahan; "
            "h. Pelaksanaan urusan hubungan masyarakat, pelayanan informasi, dan pengelolaan pengaduan masyarakat; "
            "i. Pemantauan, evaluasi, dan pelaporan pelaksanaan kegiatan pertanahan serta pengoordinasian penyelesaian tindaklanjut temuan hasil pengawasan."
        )
    )

    # 2. Sub-unit: Subbagian Perencanaan, Evaluasi dan Pelaporan
    database.insert_sotk(
        unit_level="Subbagian",
        post_name="Subbagian Perencanaan, Evaluasi dan Pelaporan",
        parent_post="Bagian Tata Usaha",
        main_duty=(
            "Melakukan penyiapan penyusunan rencana, program, anggaran dan pelaporan, "
            "pelaksanaan pemantauan, evaluasi, dan pelaporan program strategis pertanahan, "
            "dan kegiatan pertanahan serta pengoordinasian penyelesaian tindak lanjut temuan hasil pengawasan "
            "di Kantor Wilayah dan Kantor Pertanahan."
        ),
        functions="-"
    )

    # 3. Sub-unit: Subbagian Keuangan dan Barang Milik Negara
    database.insert_sotk(
        unit_level="Subbagian",
        post_name="Subbagian Keuangan dan Barang Milik Negara",
        parent_post="Bagian Tata Usaha",
        main_duty="Melakukan penyiapan pengelolaan urusan keuangan dan pengelolaan barang milik negara.",
        functions="-"
    )

    # 4. Sub-unit: Subbagian Hukum, Kepegawaian dan Organisasi
    database.insert_sotk(
        unit_level="Subbagian",
        post_name="Subbagian Hukum, Kepegawaian dan Organisasi",
        parent_post="Bagian Tata Usaha",
        main_duty=(
            "Melakukan penyiapan, pengoordinasian dan fasilitasi urusan advokasi hukum dan peraturan perundang-undangan, "
            "penyiapan bahan urusan penataan organisasi, ketatalaksanaan, analisis jabatan, dan pengelolaan urusan kepegawaian "
            "serta pengoordinasian dan fasilitasi pelaksanaan reformasi birokrasi di Kantor Wilayah dan Kantor Pertanahan."
        ),
        functions="-"
    )

    # 5. Sub-unit: Subbagian Umum dan Hubungan Masyarakat
    database.insert_sotk(
        unit_level="Subbagian",
        post_name="Subbagian Umum dan Hubungan Masyarakat",
        parent_post="Bagian Tata Usaha",
        main_duty=(
            "Melakukan penyiapan pelaksanaan ketatausahaan, pengelolaan dan digitalisasi arsip, rumah tangga, perlengkapan, "
            "penyelenggaraan layanan pengadaan, pengoordinasian dan fasilitasi pengelolaan pelayanan pertanahan dan informasi, "
            "pelaksanaan urusan hubungan masyarakat, protokol, serta penanganan pengaduan masyarakat."
        ),
        functions="-"
    )

    print("SOTK mandates successfully injected into the master database records!")

if __name__ == "__main__":
    inject_sotk_regulations()