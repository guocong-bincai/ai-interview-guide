<p align="center">
  <a href="README.md">简体中文</a> ·
  <a href="README_EN.md">English</a> ·
  <b>日本語</b> ·
  <a href="README_KO.md">한국어</a> ·
  <a href="README_PT-BR.md">Português do Brasil</a> ·
  <a href="README_ES.md">Español</a> ·
  <a href="README_ID.md">Bahasa Indonesia</a>
</p>

# AI エンジニア面接ハンドブック

> AI アプリケーション、RAG、Agent、モデル学習・推論、FDE、マルチモーダル、AI セーフティ職向けの体系的な面接ガイドです。

**662 問 · 28 トピック · 職種別 7 学習ルート**

> [!IMPORTANT]
> このページはプロジェクト紹介の翻訳版です。質問と回答の本文は現在、簡体字中国語で管理されています。以下のリンクから中国語版の各トピックへ移動できます。

## このリポジトリの特徴

- **実際の職種を基準に構成：** 単発の雑学ではなく、AI エンジニア求人で繰り返し求められる能力を扱います。
- **技術的なトレードオフを重視：** 品質、レイテンシ、コスト、安全性、複雑性、代替案まで説明します。
- **品質を継続的に検査：** リンク切れ、重複問題、根拠のない精密な数値、問題と図解の 1 対 1 対応を自動監査します。

## 図解で学ぶ

28 トピック・662 問のすべてに、クリック可能な専用の 16:9 学習図を用意しました。仕組み、処理フロー、トレードオフ、境界条件、記憶の手がかりを 1 枚にまとめています。図中のラベルは正本に合わせて中国語ですが、標準的な技術用語と図の流れから内容を追えます。

<table>
  <tr>
    <td width="33%" align="center"><a href="docs/01-basic-concepts/"><img src="assets/illustrations/01-basic-concepts/q25-kv-cache.webp" width="100%" alt="LLM 基礎の図解：KV Cache"></a><br><b>LLM 基礎</b></td>
    <td width="33%" align="center"><a href="docs/03-rag-system/"><img src="assets/illustrations/03-rag-system/q02-rag-pipeline.webp" width="100%" alt="RAG システムの図解：本番パイプライン"></a><br><b>RAG システム</b></td>
    <td width="33%" align="center"><a href="docs/04-transformer-architecture/"><img src="assets/illustrations/04-transformer-architecture/q03-self-attention.webp" width="100%" alt="Transformer の図解：Self-Attention の仕組み"></a><br><b>Transformer</b></td>
  </tr>
  <tr>
    <td width="33%" align="center"><a href="docs/05-ai-agent-basics/"><img src="assets/illustrations/05-ai-agent-basics/q02-react-loop.webp" width="100%" alt="AI Agent の図解：ReAct の推論と行動ループ"></a><br><b>AI Agent</b></td>
    <td width="33%" align="center"><a href="docs/08-inference-optimization/"><img src="assets/illustrations/08-inference-optimization/q05-pagedattention.webp" width="100%" alt="推論最適化の図解：PagedAttention のメモリ管理"></a><br><b>学習・推論</b></td>
    <td width="33%" align="center"><a href="docs/10-production-deployment/"><img src="assets/illustrations/10-production-deployment/q12-llm-gateway.webp" width="100%" alt="本番 AI の図解：LLM Gateway アーキテクチャ"></a><br><b>安全性・本番運用</b></td>
  </tr>
</table>

<p align="center"><b>28 トピック · 662 問 · 全問 1 問 1 図の対応が完了</b></p>

## 職種別の学習ルート

| 職種 | 推奨ルート |
|---|---|
| AI / LLM アプリケーションエンジニア | [LLM 基礎](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [RAG](docs/03-rag-system/) → [Agent 基礎](docs/05-ai-agent-basics/) → [本番運用](docs/10-production-deployment/) → [AI システム設計](docs/25-system-design-ai/) |
| RAG エンジニア | [LLM 基礎](docs/01-basic-concepts/) → [RAG](docs/03-rag-system/) → [ベクトル検索](docs/06-vector-index-optimization/) → [高度な RAG](docs/20-rag-advanced-optimization/) → [安全性・評価](docs/09-ai-safety-evaluation/) → [可観測性](docs/23-agent-observability/) |
| Agent エンジニア | [Prompt Engineering](docs/02-prompt-engineering/) → [Agent 基礎](docs/05-ai-agent-basics/) → [計画・内省](docs/22-agent-planning-reflection/) → [Multi-Agent](docs/13-multi-agent-systems/) → [MCP・Skills](docs/14-mcp-skill-systems/) → [可観測性](docs/23-agent-observability/) |
| 学習・推論エンジニア | [Transformer](docs/04-transformer-architecture/) → [モデル学習](docs/07-model-training/) → [推論最適化](docs/08-inference-optimization/) → [推論フレームワーク](docs/19-inference-frameworks/) |
| Forward Deployed Engineer | [プロジェクト深掘り](docs/27-project-experience/) → [Python エンジニアリング](docs/24-python-engineering/) → [AI システム設計](docs/25-system-design-ai/) → [FDE](docs/26-forward-deployed-engineer/) |
| マルチモーダル AI エンジニア | [Transformer](docs/04-transformer-architecture/) → [マルチモーダル AI](docs/11-multimodal-ai/) → [マルチモーダル Agent](docs/21-multimodal-agents/) → [本番運用](docs/10-production-deployment/) |
| AI セーフティ・評価エンジニア | [LLM 基礎](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [安全性・評価](docs/09-ai-safety-evaluation/) → [Test Harness・評価](docs/28-test-harness-evaluation/) → [可観測性](docs/23-agent-observability/) → [本番運用](docs/10-production-deployment/) |

## トピック構成

- **基礎とモデル：** LLM 基礎、Transformer、モデル学習、推論最適化、推論フレームワーク。
- **RAG と検索：** RAG システム、ベクトルインデックス、高度な本番 RAG。
- **Agent とプロトコル：** Agent 基礎、Multi-Agent、MCP/Skills、計画、可観測性。
- **エンジニアリングと設計：** 安全性評価、本番運用、Python、AI システム設計、FDE、[Test Harness・評価](docs/28-test-harness-evaluation/)。
- **マルチモーダルと先端領域：** マルチモーダル AI、AI コーディング、先端トピック。
- **面接準備：** 履歴書、面接情報、プロジェクト深掘り。

[中国語 README の全トピック一覧](README.md#catalog)も参照してください。

## 効果的な使い方

各問題について、次の 3 種類の回答を準備します。

1. **30 秒版：** 結論と判断理由を先に述べる。
2. **3 分版：** 原理、代替案、トレードオフを説明する。
3. **深掘り版：** 検証方法、障害時の対応、別案を採用しなかった理由を説明する。

例示された数値は、自分のプロジェクトで確認したデータに置き換えてください。製品仕様、価格、ベンチマークは変化するため、公式ドキュメントや原論文を確認してください。

## コントリビューション

問題を追加・修正する前に、[コンテンツ品質基準](CONTENT_QUALITY.md)を確認してください。翻訳の改善も歓迎します。完全な翻訳版が継続管理されるまでは、中国語版を正本とします。

問題の報告は [Issue](https://github.com/guocong-bincai/ai-interview-guide/issues)、修正の提案は [Pull Request](https://github.com/guocong-bincai/ai-interview-guide/pulls) からお願いします。

## ライセンス

[MIT](LICENSE)
