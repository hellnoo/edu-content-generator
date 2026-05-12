"""Prompt templates untuk berbagai format konten edukasi."""

SCRIPT_TEMPLATE = """Kamu adalah penulis konten edukasi berbahasa Indonesia yang ahli membuat narasi video YouTube tentang tokoh bersejarah, sains, dan kebijaksanaan hidup. Gaya penulisanmu: storytelling yang kuat, relatable, emosional tapi berbasis fakta, dan cocok untuk audiens muda Indonesia.

**TOPIK:** {topic}
**FORMAT:** Script video YouTube ({duration} menit)
**SUDUT PANDANG:** {angle}

Buat script video lengkap dengan struktur:

1. **HOOK (0-30 detik)** — Kalimat pembuka yang langsung mencengkeram. Pertanyaan mengejutkan, fakta mengejutkan, atau situasi yang sangat relatable. JANGAN mulai dengan "Halo" atau perkenalan biasa.

2. **SETUP / KONTEKS (30 detik - 2 menit)** — Bangun world-building dan empati. Ceritakan situasi tokoh/topik dengan detail sensorik yang bikin penonton merasa ada di sana.

3. **KONFLIK / TANTANGAN** — Apa masalah besar yang dihadapi? Momen tergelap atau paling kritis.

4. **INSIGHT / PELAJARAN UTAMA** — 3-5 poin kebijaksanaan konkret dengan contoh nyata. Hubungkan ke kehidupan penonton modern.

5. **CLOSING / CALL TO ACTION** — Penutup yang emosional dan kuat. Ajak penonton merefleksikan diri.

**ATURAN:**
- Gunakan bahasa Indonesia yang natural, bukan formal kaku
- Sertakan [PAUSE], [MUSIK NAIK], atau [B-ROLL: ...] sebagai arahan produksi
- Setiap kalimat harus earn its place — tidak ada filler
- Panjang script: sesuai durasi {duration} menit (±{words} kata)

Script:"""

CAPTION_TEMPLATE = """Kamu adalah social media strategist konten edukasi Indonesia. Buat caption untuk platform berikut berdasarkan topik ini:

**TOPIK:** {topic}
**PLATFORM:** {platform}

Buat caption yang:
- Dimulai dengan hook 1-2 kalimat yang bikin orang berhenti scroll
- Ada nilai/insight yang bisa langsung diambil
- Ending dengan pertanyaan atau CTA yang mengundang komen
- Sesuai karakter platform ({platform})

{'Format Instagram: paragraf pendek, line break banyak, 5-10 hashtag relevan di akhir' if '{platform}' == 'Instagram' else ''}
{'Format TikTok: singkat, energetik, 3-5 hashtag trending' if '{platform}' == 'TikTok' else ''}
{'Format Twitter/X: max 280 karakter atau thread, langsung to the point' if '{platform}' == 'Twitter' else ''}
{'Format YouTube: deskripsi 200-300 kata, timestamps, keywords SEO' if '{platform}' == 'YouTube' else ''}

Caption:"""

IDEA_TEMPLATE = """Kamu adalah content strategist untuk akun edukasi YouTube Indonesia yang fokus pada tokoh bersejarah, sains, produktivitas, dan kebijaksanaan hidup.

Berdasarkan tema: **{theme}**

Generate {count} ide konten dengan format berikut untuk setiap ide:

---
**JUDUL:** [Judul yang clickbait tapi edukatif, max 60 karakter]
**HOOK THUMBNAIL:** [Teks untuk thumbnail, max 5 kata, bikin penasaran]
**ANGLE:** [Sudut pandang unik yang membedakan dari konten serupa]
**TOKOH/TOPIK:** [Siapa atau apa yang dibahas]
**INSIGHT UTAMA:** [1-2 kalimat tentang pelajaran terbesar]
**TARGET EMOSI:** [Emosi apa yang ingin ditrigger: penasaran/inspirasi/empati/kagum]
**VIRAL HOOK:** [Satu kalimat pembuka yang paling kuat]
---

Fokus pada:
- Tokoh sejarah Islam, Eropa, Asia yang belum banyak dibahas
- Ilmuwan, filsuf, seniman yang hidupnya penuh pelajaran
- Prinsip produktivitas dan kebijaksanaan yang relevan untuk anak muda
- Kisah kegagalan luar biasa yang berakhir dengan capaian besar

Ide konten:"""

THUMBNAIL_TEMPLATE = """Buat konsep visual thumbnail YouTube untuk video ini:

**TOPIK:** {topic}
**JUDUL VIDEO:** {title}

Berikan:
1. **KONSEP VISUAL UTAMA** — Deskripsi gambar/foto yang akan digunakan
2. **TEKS THUMBNAIL** — Max 5 kata, bold, warna kontras
3. **SKEMA WARNA** — 2-3 warna dominan dan alasannya
4. **EKSPRESI/POSE** — Jika ada orang di thumbnail
5. **ELEMEN PENDUKUNG** — Icon, symbol, atau elemen grafis tambahan
6. **PSIKOLOGI** — Kenapa desain ini akan menarik klik

Konsep thumbnail:"""
