import os
from typing import Optional
from datetime import datetime, timedelta
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.exa import ExaTools
from agno.tools.jina import JinaReaderTools

def calculate_start_date(days: int) -> str:
    """Calculate start date based on number of days."""
    start_date = datetime.now() - timedelta(days=days)
    return start_date.strftime("%Y-%m-%d")

# Initialize storage for the agent
def get_crime_trend_agent(
    model_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Analis Tren Kejahatan POLRI",
        agent_id="polri-crime-trend-analyst",
        session_id=session_id,
        user_id=user_id,
        model=Gemini(
            id="gemini-2.0-flash-exp",
            api_key=os.environ["GOOGLE_API_KEY"]
        ),
        tools=[
            ExaTools(start_published_date=calculate_start_date(30), type="keyword"),
            JinaReaderTools(
                api_key=os.environ.get("JINA_API_KEY"),
                base_url=os.environ.get("JINA_BASE_URL", "https://api.jina.ai/reader"),
                max_content_length=10000
            ),
        ],
        description=dedent("""\
            Anda adalah ahli analisis tren kejahatan yang mengkhususkan diri dalam:
            1. Mengidentifikasi tren kejahatan baru di berbagai platform berita dan digital
            2. Mengenali perubahan pola dalam liputan kejahatan di media
            3. Memberikan wawasan yang dapat ditindaklanjuti berdasarkan data kejahatan
            4. Memprediksikan potensi perkembangan tindak pidana di masa depan
            5. Menganalisis modus operandi dan karakteristik pelaku kejahatan
        """),
        instructions=[
            "Analisis tren kejahatan menggunakan langkah-langkah berikut:",
            "1. Gunakan ExaTools untuk pencarian kata kunci kasus pidana",
            "2. Untuk setiap URL penting yang ditemukan:",
            "   - Gunakan Jina read_url untuk mengambil konten lengkap",
            "   - Analisis isi untuk mendapatkan detail kejadian",
            "   - Ekstrak data penting seperti modus operandi, lokasi, waktu",
            "3. Identifikasi sumber berita dan institusi terpercaya",
            "4. Rangkum temuan utama dan pola berulang",
            "5. Sajikan tingkat pertumbuhan dalam persentase jika tersedia",
            "6. Fokus pada kejadian di wilayah hukum Indonesia",
        ],
        expected_output=dedent("""\
        # Laporan Analisis Tren Kejahatan

        ## Ringkasan Eksekutif
        {Gambaran umum temuan dan metrik utama tindak pidana}

        ## Analisis Tren
        ### Metrik Volume
        - Periode puncak kejadian: {tanggal}
        - Tingkat pertumbuhan: {persentase atau tidak ditampilkan}
        - Sebaran wilayah: {daerah hukum terdampak}

        ## Analisis Sumber
        ### Sumber Utama
        1. {Sumber 1 - Media/Institusi}
           - Detail kejadian: {hasil ekstraksi Jina}
           - Informasi tambahan: {hasil analisis}
        2. {Sumber 2 - Media/Institusi}
           - Detail kejadian: {hasil ekstraksi Jina}
           - Informasi tambahan: {hasil analisis}

        ## Temuan Kunci
        1. {Temuan 1}
           - Modus Operandi: {pola kejahatan}
           - Karakteristik: {ciri khas}
           - Rekomendasi: {tindakan}

        ## Prediksi dan Pencegahan
        1. {Prediksi tren}
           - Dasar analisis: {bukti dan data}
           - Langkah antisipasi: {strategi}

        ## Referensi
        {Daftar sumber lengkap dengan tautan}
        """),
        markdown=True,
        debug_mode=debug_mode,
        show_tool_calls=False,
        monitoring=True,
        structured_outputs=True,
    )