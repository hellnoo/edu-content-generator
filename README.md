# edu-content-generator

Auto-generate konten edukasi Indonesia berkualitas tinggi menggunakan Claude AI — script narasi YouTube, caption multi-platform, ide konten, dan konsep thumbnail, semua dalam satu perintah.

Cocok untuk mengembangkan akun edukasi YouTube/Instagram/TikTok dengan konten tentang tokoh bersejarah, sains, produktivitas, dan kebijaksanaan hidup.

---

## Apa yang bisa di-generate?

| Tipe | Deskripsi |
|------|-----------|
| **Script** | Narasi video YouTube lengkap dengan arahan produksi ([PAUSE], [B-ROLL], dll) |
| **Caption** | Caption siap posting untuk YouTube, Instagram, TikTok, Twitter |
| **Ideas** | Batch ide konten dengan judul, angle, hook, dan thumbnail text |
| **Package** | Semua di atas sekaligus dalam satu folder terorganisir |

---

## Setup

```bash
git clone https://github.com/hellnoo/edu-content-generator
cd edu-content-generator

pip install -r requirements.txt

cp .env.example .env
# Edit .env dan isi ANTHROPIC_API_KEY
```

Dapatkan API key di: https://console.anthropic.com

---

## Cara Pakai

### Generate script video (10 menit)
```bash
python main.py script "Ibnu Sina" --duration 10
```

### Generate script dengan angle spesifik
```bash
python main.py script "Al-Khawarizmi" --duration 8 --angle "cara kerja matematikawan saat menghadapi tekanan politik"
```

### Generate caption Instagram
```bash
python main.py caption "Ibnu Sina" --platform instagram
```

### Generate caption semua platform (YouTube, Instagram, TikTok, Twitter)
```bash
python main.py caption "Nikola Tesla" --platform tiktok
```

### Generate 10 ide konten
```bash
python main.py ideas --theme "ilmuwan islam abad pertengahan" --count 10
```

### Generate paket lengkap (script + caption + thumbnail)
```bash
python main.py package "Ibnu Sina: Cara Kerja Orang Jenius Saat Hidup Kacau" --duration 10
```

---

## Output

Semua hasil disimpan otomatis di folder `outputs/`:

```
outputs/
├── scripts/          # Script narasi .md
├── captions/         # Caption per platform .md
├── ideas/            # Ide konten .md
└── packages/         # Paket lengkap per topik/
    └── 20260513_ibnu-sina/
        ├── script.md
        ├── caption_youtube.md
        ├── caption_instagram.md
        ├── caption_tiktok.md
        ├── thumbnail_concept.md
        └── meta.json
```

---

## Contoh Topik yang Bagus

**Tokoh Islam:**
- Ibnu Sina (kedokteran, produktivitas)
- Al-Khawarizmi (matematika, algoritma)
- Al-Biruni (sains, perjalanan)
- Ibn Khaldun (sosiologi, sejarah)
- Al-Ghazali (filsafat, spiritualitas)

**Tokoh Dunia:**
- Nikola Tesla (ketekunan, inovasi)
- Marie Curie (ketabahan, sains)
- Leonardo da Vinci (kreativitas, multidisiplin)
- Seneca (stoicism, kehidupan)
- Marcus Aurelius (kepemimpinan, filosofi)

**Tema Produktivitas:**
- "Cara kerja orang jenius saat hidup sedang kacau"
- "Metode belajar tokoh-tokoh terbaik sepanjang masa"
- "Rahasia produktivitas sebelum ada smartphone"

---

## Pengembangan Lanjutan

Roadmap yang bisa dikembangkan:
- [ ] Batch generate dari daftar topik (CSV/JSON)
- [ ] Integration dengan ElevenLabs untuk narasi audio
- [ ] Auto-post ke platform sosmed via API
- [ ] Web UI dengan Flask/FastAPI
- [ ] Template per niche (sains, sejarah, motivasi, bisnis)
- [ ] Scheduling konten mingguan otomatis

---

## Lisensi

MIT — bebas digunakan dan dikembangkan.
