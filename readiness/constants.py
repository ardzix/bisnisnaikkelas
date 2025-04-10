SUGGESTIONS = {
    'has_website': "Buat website profesional untuk meningkatkan kredibilitas dan visibilitas usaha Anda.",
    'has_social_media': "Buat akun media sosial bisnis di Instagram/Facebook/TikTok untuk mulai menjangkau audiens.",
    'is_social_media_active': "Posting konten secara rutin di media sosial agar audiens tetap engaged.",
    'uses_digital_ads': "Mulai gunakan iklan digital untuk meningkatkan jangkauan pemasaran Anda.",
    'uses_crm_or_marketing_tools': "Gunakan CRM untuk mengelola pelanggan dan mempertahankan loyalitas.",
    'has_financial_records': "Catat semua pemasukan dan pengeluaran usaha secara terstruktur.",
    'has_invoice_system': "Gunakan sistem invoice untuk pencatatan penjualan dan pembayaran yang rapi.",
    'uses_financial_software': "Gunakan software akuntansi untuk kemudahan laporan keuangan dan pengawasan.",
    'has_cashflow_forecast': "Buat proyeksi arus kas untuk memastikan kelancaran keuangan jangka pendek.",
    'has_tax_calculation_practice': "Hitung dan arsipkan kewajiban pajak secara rutin dan benar.",
    'has_npwp': "Urus NPWP atas nama usaha agar bisa mengakses layanan perbankan dan pajak.",
    'has_business_license': "Lengkapi legalitas usaha dengan perizinan seperti NIB/IUMK.",
    'has_profit_loss_statement': "Susun laporan laba rugi untuk mengetahui untung-rugi usaha secara periodik.",
    'has_balance_sheet': "Buat neraca keuangan untuk melihat posisi aset, liabilitas, dan ekuitas.",
    'has_contract_templates': "Siapkan template kontrak standar untuk kerja sama dan transaksi usaha.",
    'has_sop_documentation': "Susun SOP untuk proses penting seperti pelayanan pelanggan dan produksi.",
    'has_team_structure': "Tentukan struktur tim agar tanggung jawab antar anggota lebih jelas.",
    'has_vision_and_mission': "Tulis visi dan misi usaha untuk memberi arah strategis jangka panjang.",
    'has_business_plan': "Rancang rencana bisnis 1–3 tahun sebagai panduan pertumbuhan.",
    'has_defined_target_market': "Tentukan siapa target pelanggan ideal Anda agar pemasaran lebih efektif.",
    'has_unique_value_proposition': "Identifikasi keunikan produk/jasa dibanding pesaing.",
    'has_data_backup': "Lakukan backup data penting secara berkala untuk menghindari kehilangan data.",
    'has_internal_controls': "Terapkan kontrol internal untuk mengurangi risiko kesalahan dan kecurangan.",
    'has_been_audited': "Lakukan audit internal/eksternal untuk memastikan kepatuhan dan akurasi keuangan.",
    'can_operate_remotely': "Bangun infrastruktur kerja remote agar tim bisa bekerja dari mana saja.",
    'uses_inventory_software': "Gunakan software inventaris untuk pencatatan stok dan pengadaan barang.",
    'uses_automation_or_integration': "Otomatisasi proses rutin agar lebih efisien dan scalable.",
    'has_internal_dashboard_or_kpi_system': "Gunakan dashboard KPI untuk memantau performa secara real-time.",
    'sells_nationally_or_internationally': "Perluas jangkauan penjualan ke luar kota atau luar negeri.",
    'attends_trade_expos': "Ikuti pameran dagang untuk membangun jaringan dan mengenalkan brand.",
    'has_reseller_or_distributor': "Bangun jaringan reseller untuk memperluas distribusi.",
    'has_partnership_program': "Ciptakan program kemitraan strategis untuk pertumbuhan kolaboratif.",
    'has_payroll_system': "Gunakan sistem penggajian digital untuk efisiensi dan transparansi.",
    'has_quality_control_process': "Terapkan proses kontrol kualitas untuk produk/jasa yang lebih konsisten.",
    'has_employee_handbook_or_sop': "Buat buku panduan kerja untuk onboarding dan standarisasi.",
    'has_formal_onboarding': "Susun proses onboarding resmi agar karyawan baru cepat adaptasi.",
    'employee_count': "Evaluasi kebutuhan tim dan struktur organisasi sesuai pertumbuhan bisnis.",
    'year_started': "Bisnis Anda masih tergolong baru, pertimbangkan untuk memperkuat fondasi proses operasional.",
    'annual_revenue': "Optimalkan pendapatan agar usaha dapat naik kelas dan mengakses pendanaan."
}

# Per-level and per-category weighted checklists
EXPECTED_CHECKS = {
    'micro': {
        'digital': {
            'has_website': 50,
            'has_social_media': 25,
            'is_social_media_active': 25,
        },
        'financial': {
            'has_financial_records': 60,
            'has_invoice_system': 40,
        },
        'legal': {
            'has_npwp': 60,
            'has_business_license': 40,
        },
        'operational': {
            'has_sop_documentation': 60,
            'has_team_structure': 40,
        },
        'strategy': {
            'has_vision_and_mission': 100,
        }
    },
    'small': {
        'digital': {
            'has_website': 30,
            'has_social_media': 20,
            'is_social_media_active': 20,
            'uses_digital_ads': 15,
            'uses_crm_or_marketing_tools': 15,
        },
        'financial': {
            'has_financial_records': 30,
            'has_invoice_system': 25,
            'uses_financial_software': 25,
            'has_tax_calculation_practice': 20,
        },
        'legal': {
            'has_npwp': 40,
            'has_business_license': 30,
            'has_profit_loss_statement': 15,
            'has_balance_sheet': 15,
        },
        'operational': {
            'has_sop_documentation': 40,
            'has_team_structure': 30,
            'year_started': 30,
        },
        'strategy': {
            'has_vision_and_mission': 30,
            'has_business_plan': 35,
            'has_defined_target_market': 35,
        }
    },
    'medium': {
        'digital': {
            'has_website': 25,
            'has_social_media': 20,
            'is_social_media_active': 15,
            'uses_digital_ads': 20,
            'uses_crm_or_marketing_tools': 20,
        },
        'financial': {
            'has_financial_records': 25,
            'has_invoice_system': 20,
            'uses_financial_software': 20,
            'has_cashflow_forecast': 20,
            'has_tax_calculation_practice': 15,
        },
        'legal': {
            'has_npwp': 25,
            'has_business_license': 25,
            'has_profit_loss_statement': 20,
            'has_balance_sheet': 20,
            'has_contract_templates': 10,
        },
        'operational': {
            'has_sop_documentation': 30,
            'has_team_structure': 30,
            'year_started': 40,
        },
        'strategy': {
            'has_vision_and_mission': 25,
            'has_business_plan': 25,
            'has_defined_target_market': 25,
            'has_unique_value_proposition': 25,
        },
        'compliance': {
            'has_data_backup': 40,
            'has_internal_controls': 30,
            'has_been_audited': 30,
        },
        'technology': {
            'can_operate_remotely': 25,
            'uses_inventory_software': 25,
            'uses_automation_or_integration': 25,
            'has_internal_dashboard_or_kpi_system': 25,
        },
        'market': {
            'sells_nationally_or_internationally': 50,
            'attends_trade_expos': 25,
            'has_reseller_or_distributor': 25,
        },
        'process': {
            'has_payroll_system': 25,
            'has_quality_control_process': 25,
            'has_employee_handbook_or_sop': 25,
            'has_formal_onboarding': 25,
        }
    },
    'large': {
        # Same structure as 'medium' but weights may differ for larger expectations
        'digital': {
            'has_website': 20,
            'has_social_media': 15,
            'is_social_media_active': 10,
            'uses_digital_ads': 25,
            'uses_crm_or_marketing_tools': 30,
        },
        'financial': {
            'has_financial_records': 20,
            'has_invoice_system': 15,
            'uses_financial_software': 20,
            'has_cashflow_forecast': 20,
            'has_tax_calculation_practice': 15,
            'annual_revenue': 10,
        },
        'legal': {
            'has_npwp': 20,
            'has_business_license': 20,
            'has_profit_loss_statement': 20,
            'has_balance_sheet': 20,
            'has_contract_templates': 20,
        },
        'operational': {
            'has_sop_documentation': 25,
            'has_team_structure': 25,
            'year_started': 25,
            'employee_count': 25,
        },
        'strategy': {
            'has_vision_and_mission': 20,
            'has_business_plan': 20,
            'has_defined_target_market': 30,
            'has_unique_value_proposition': 30,
        },
        'compliance': {
            'has_data_backup': 30,
            'has_internal_controls': 30,
            'has_been_audited': 40,
        },
        'technology': {
            'can_operate_remotely': 20,
            'uses_inventory_software': 20,
            'uses_automation_or_integration': 30,
            'has_internal_dashboard_or_kpi_system': 30,
        },
        'market': {
            'sells_nationally_or_internationally': 30,
            'attends_trade_expos': 30,
            'has_reseller_or_distributor': 20,
            'has_partnership_program': 20,
        },
        'process': {
            'has_payroll_system': 25,
            'has_quality_control_process': 25,
            'has_employee_handbook_or_sop': 25,
            'has_formal_onboarding': 25,
        }
    }
}
