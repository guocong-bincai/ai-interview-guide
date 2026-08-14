<p align="center">
  <a href="README.md">简体中文</a> ·
  <a href="README_EN.md">English</a> ·
  <a href="README_JA.md">日本語</a> ·
  <a href="README_KO.md">한국어</a> ·
  <a href="README_PT-BR.md">Português do Brasil</a> ·
  <a href="README_ES.md">Español</a> ·
  <b>Bahasa Indonesia</b>
</p>

# Panduan Wawancara Engineer AI

> Panduan wawancara terstruktur untuk peran aplikasi AI, RAG, Agent, pelatihan dan inferensi model, FDE, multimodal, serta keamanan AI.

**568 pertanyaan · 27 topik · 7 jalur belajar berdasarkan peran**

> [!IMPORTANT]
> Halaman ini merupakan terjemahan pengantar proyek. Bank pertanyaan dan jawaban lengkap saat ini dikelola dalam bahasa Mandarin Sederhana. Tautan topik di bawah membuka konten berbahasa Mandarin.

## Mengapa repositori ini berguna

- **Berbasis peran nyata:** membahas kemampuan yang berulang dalam lowongan engineering AI, bukan sekadar trivia.
- **Mengutamakan trade-off engineering:** membahas kualitas, latensi, biaya, keamanan, kompleksitas, dan alternatif.
- **Kualitas dapat diperiksa:** audit repositori mendeteksi tautan rusak, pertanyaan duplikat, dan metrik presisi tanpa sumber.

## Pilih jalurmu

| Peran | Jalur yang disarankan |
|---|---|
| Engineer Aplikasi AI / LLM | [Dasar LLM](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [RAG](docs/03-rag-system/) → [Dasar Agent](docs/05-ai-agent-basics/) → [Produksi](docs/10-production-deployment/) → [Desain Sistem AI](docs/25-system-design-ai/) |
| Engineer RAG | [Dasar LLM](docs/01-basic-concepts/) → [RAG](docs/03-rag-system/) → [Pencarian Vektor](docs/06-vector-index-optimization/) → [RAG Lanjutan](docs/20-rag-advanced-optimization/) → [Keamanan dan Evaluasi](docs/09-ai-safety-evaluation/) |
| Engineer Agent | [Prompt Engineering](docs/02-prompt-engineering/) → [Dasar Agent](docs/05-ai-agent-basics/) → [Perencanaan dan Refleksi](docs/22-agent-planning-reflection/) → [Multi-Agent](docs/13-multi-agent-systems/) → [MCP dan Skills](docs/14-mcp-skill-systems/) |
| Engineer Pelatihan dan Inferensi | [Transformer](docs/04-transformer-architecture/) → [Pelatihan Model](docs/07-model-training/) → [Optimasi Inferensi](docs/08-inference-optimization/) → [Framework Inferensi](docs/19-inference-frameworks/) |
| Forward Deployed Engineer | [Pendalaman Proyek](docs/27-project-experience/) → [Engineering Python](docs/24-python-engineering/) → [Desain Sistem AI](docs/25-system-design-ai/) → [FDE](docs/26-forward-deployed-engineer/) |
| Engineer AI Multimodal | [Transformer](docs/04-transformer-architecture/) → [AI Multimodal](docs/11-multimodal-ai/) → [Agent Multimodal](docs/21-multimodal-agents/) → [Produksi](docs/10-production-deployment/) |
| Engineer Keamanan dan Evaluasi AI | [Dasar LLM](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [Keamanan dan Evaluasi](docs/09-ai-safety-evaluation/) → [Observabilitas](docs/23-agent-observability/) |

## Peta topik

- **Dasar dan model:** dasar LLM, Transformer, pelatihan, optimasi inferensi, dan framework inferensi.
- **RAG dan retrieval:** sistem RAG, indeks vektor, dan RAG produksi tingkat lanjut.
- **Agent dan protokol:** dasar Agent, Multi-Agent, MCP/Skills, perencanaan, dan observabilitas.
- **Engineering dan desain sistem:** evaluasi keamanan, produksi, Python, desain sistem AI, dan FDE.
- **Multimodal dan topik baru:** AI multimodal, alat coding AI, dan topik lanjutan.
- **Persiapan wawancara:** resume, catatan sumber wawancara, dan pendalaman proyek.

Lihat [katalog lengkap pada README berbahasa Mandarin](README.md#catalog).

## Cara berlatih

Siapkan tiga versi untuk setiap jawaban:

1. **30 detik:** sampaikan keputusan dan alasan utama.
2. **3 menit:** jelaskan prinsip, alternatif, dan trade-off.
3. **Pendalaman:** jelaskan validasi, penanganan kegagalan, dan alasan tidak memilih pendekatan lain.

Ganti semua metrik contoh dengan bukti dari pekerjaanmu sendiri. Perilaku produk, harga, dan hasil benchmark dapat berubah; periksa klaim yang sensitif terhadap waktu melalui dokumentasi resmi atau makalah asli.

## Berkontribusi

Baca [kebijakan kualitas konten](CONTENT_QUALITY.md) sebelum menambah atau mengubah pertanyaan. Perbaikan terjemahan sangat diterima. Hingga tersedia terjemahan lengkap yang dipelihara, bank pertanyaan berbahasa Mandarin tetap menjadi sumber utama.

Buka [Issue](https://github.com/guocong-bincai/ai-interview-guide/issues) untuk melaporkan masalah atau kirim [Pull Request](https://github.com/guocong-bincai/ai-interview-guide/pulls) dengan perbaikan.

## Lisensi

[MIT](LICENSE)
