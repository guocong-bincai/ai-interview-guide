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

**619 pertanyaan · 28 topik · 7 jalur belajar berdasarkan peran**

> [!IMPORTANT]
> Halaman ini merupakan terjemahan pengantar proyek. Bank pertanyaan dan jawaban lengkap saat ini dikelola dalam bahasa Mandarin Sederhana. Tautan topik di bawah membuka konten berbahasa Mandarin.

## Mengapa repositori ini berguna

- **Berbasis peran nyata:** membahas kemampuan yang berulang dalam lowongan engineering AI, bukan sekadar trivia.
- **Mengutamakan trade-off engineering:** membahas kualitas, latensi, biaya, keamanan, kompleksitas, dan alternatif.
- **Kualitas dapat diperiksa:** audit repositori mendeteksi tautan rusak, pertanyaan duplikat, metrik presisi tanpa sumber, serta cakupan 1:1 antara pertanyaan dan ilustrasi.

## Belajar secara visual

Seluruh 28 topik dan 619 pertanyaan kini memiliki ilustrasi pembelajaran 16:9 khusus yang dapat diklik. Setiap gambar merangkum mekanisme, alur, trade-off, batasan, dan kalimat pengingat. Label gambar tetap berbahasa Mandarin sesuai bank soal sumber, tetapi istilah teknis standar dan alur visualnya tetap mudah dikenali.

<table>
  <tr>
    <td width="33%" align="center"><a href="docs/01-basic-concepts/"><img src="assets/illustrations/01-basic-concepts/q25-kv-cache.webp" width="100%" alt="Ilustrasi dasar LLM: KV Cache"></a><br><b>Dasar LLM</b></td>
    <td width="33%" align="center"><a href="docs/03-rag-system/"><img src="assets/illustrations/03-rag-system/q02-rag-pipeline.webp" width="100%" alt="Ilustrasi sistem RAG: pipeline produksi"></a><br><b>Sistem RAG</b></td>
    <td width="33%" align="center"><a href="docs/04-transformer-architecture/"><img src="assets/illustrations/04-transformer-architecture/q03-self-attention.webp" width="100%" alt="Ilustrasi Transformer: mekanisme Self-Attention"></a><br><b>Transformer</b></td>
  </tr>
  <tr>
    <td width="33%" align="center"><a href="docs/05-ai-agent-basics/"><img src="assets/illustrations/05-ai-agent-basics/q02-react-loop.webp" width="100%" alt="Ilustrasi Agent AI: loop penalaran dan tindakan ReAct"></a><br><b>Agent AI</b></td>
    <td width="33%" align="center"><a href="docs/08-inference-optimization/"><img src="assets/illustrations/08-inference-optimization/q05-pagedattention.webp" width="100%" alt="Ilustrasi inferensi: manajemen memori PagedAttention"></a><br><b>Pelatihan dan Inferensi</b></td>
    <td width="33%" align="center"><a href="docs/10-production-deployment/"><img src="assets/illustrations/10-production-deployment/q12-llm-gateway.webp" width="100%" alt="Ilustrasi AI produksi: arsitektur LLM Gateway"></a><br><b>Keamanan dan Produksi</b></td>
  </tr>
</table>

<p align="center"><b>28 topik · 619 pertanyaan · seluruh pertanyaan memiliki satu ilustrasi khusus</b></p>

## Pilih jalurmu

| Peran | Jalur yang disarankan |
|---|---|
| Engineer Aplikasi AI / LLM | [Dasar LLM](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [RAG](docs/03-rag-system/) → [Dasar Agent](docs/05-ai-agent-basics/) → [Produksi](docs/10-production-deployment/) → [Desain Sistem AI](docs/25-system-design-ai/) |
| Engineer RAG | [Dasar LLM](docs/01-basic-concepts/) → [RAG](docs/03-rag-system/) → [Pencarian Vektor](docs/06-vector-index-optimization/) → [RAG Lanjutan](docs/20-rag-advanced-optimization/) → [Keamanan dan Evaluasi](docs/09-ai-safety-evaluation/) → [Observabilitas](docs/23-agent-observability/) |
| Engineer Agent | [Prompt Engineering](docs/02-prompt-engineering/) → [Dasar Agent](docs/05-ai-agent-basics/) → [Perencanaan dan Refleksi](docs/22-agent-planning-reflection/) → [Multi-Agent](docs/13-multi-agent-systems/) → [MCP dan Skills](docs/14-mcp-skill-systems/) → [Observabilitas](docs/23-agent-observability/) |
| Engineer Pelatihan dan Inferensi | [Transformer](docs/04-transformer-architecture/) → [Pelatihan Model](docs/07-model-training/) → [Optimasi Inferensi](docs/08-inference-optimization/) → [Framework Inferensi](docs/19-inference-frameworks/) |
| Forward Deployed Engineer | [Pendalaman Proyek](docs/27-project-experience/) → [Engineering Python](docs/24-python-engineering/) → [Desain Sistem AI](docs/25-system-design-ai/) → [FDE](docs/26-forward-deployed-engineer/) |
| Engineer AI Multimodal | [Transformer](docs/04-transformer-architecture/) → [AI Multimodal](docs/11-multimodal-ai/) → [Agent Multimodal](docs/21-multimodal-agents/) → [Produksi](docs/10-production-deployment/) |
| Engineer Keamanan dan Evaluasi AI | [Dasar LLM](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [Keamanan dan Evaluasi](docs/09-ai-safety-evaluation/) → [Test Harness dan Evaluasi](docs/28-test-harness-evaluation/) → [Observabilitas](docs/23-agent-observability/) → [Produksi](docs/10-production-deployment/) |

## Peta topik

- **Dasar dan model:** dasar LLM, Transformer, pelatihan, optimasi inferensi, dan framework inferensi.
- **RAG dan retrieval:** sistem RAG, indeks vektor, dan RAG produksi tingkat lanjut.
- **Agent dan protokol:** dasar Agent, Multi-Agent, MCP/Skills, perencanaan, dan observabilitas.
- **Engineering dan desain sistem:** evaluasi keamanan, produksi, Python, desain sistem AI, FDE, dan [Test Harness dan Evaluasi](docs/28-test-harness-evaluation/).
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
