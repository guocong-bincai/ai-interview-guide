<p align="center">
  <a href="README.md">简体中文</a> ·
  <a href="README_EN.md">English</a> ·
  <a href="README_JA.md">日本語</a> ·
  <b>한국어</b> ·
  <a href="README_PT-BR.md">Português do Brasil</a> ·
  <a href="README_ES.md">Español</a> ·
  <a href="README_ID.md">Bahasa Indonesia</a>
</p>

# AI 엔지니어 면접 핸드북

> AI 애플리케이션, RAG, Agent, 모델 학습·추론, FDE, 멀티모달, AI 안전 직무를 위한 체계적인 면접 가이드입니다.

**619개 질문 · 28개 주제 · 직무별 7개 학습 경로**

> [!IMPORTANT]
> 이 페이지는 프로젝트 소개 번역본입니다. 전체 질문과 답변은 현재 중국어 간체로 관리됩니다. 아래 주제 링크는 중국어 콘텐츠로 연결됩니다.

## 이 저장소의 특징

- **실제 직무 중심:** 단편적인 상식이 아니라 AI 엔지니어 채용에서 반복적으로 요구되는 역량을 다룹니다.
- **엔지니어링 트레이드오프 중심:** 품질, 지연 시간, 비용, 안전, 복잡성, 대안을 함께 설명합니다.
- **지속적인 품질 검사:** 깨진 링크, 중복 질문, 근거 없는 정밀 수치와 질문-삽화의 1:1 대응을 자동으로 점검합니다.

## 그림으로 학습하기

28개 주제와 619개 질문 모두에 클릭 가능한 전용 16:9 학습 삽화가 있습니다. 각 그림은 핵심 메커니즘, 흐름, 트레이드오프, 경계 조건과 기억 문장을 한 장에 정리합니다. 그림의 라벨은 원본 질문 은행과 동일한 중국어이지만 표준 기술 용어와 시각적 흐름으로 내용을 따라갈 수 있습니다.

<table>
  <tr>
    <td width="33%" align="center"><a href="docs/01-basic-concepts/"><img src="assets/illustrations/01-basic-concepts/q25-kv-cache.webp" width="100%" alt="LLM 기초 삽화: KV Cache"></a><br><b>LLM 기초</b></td>
    <td width="33%" align="center"><a href="docs/03-rag-system/"><img src="assets/illustrations/03-rag-system/q02-rag-pipeline.webp" width="100%" alt="RAG 시스템 삽화: 프로덕션 파이프라인"></a><br><b>RAG 시스템</b></td>
    <td width="33%" align="center"><a href="docs/04-transformer-architecture/"><img src="assets/illustrations/04-transformer-architecture/q03-self-attention.webp" width="100%" alt="Transformer 삽화: Self-Attention 메커니즘"></a><br><b>Transformer</b></td>
  </tr>
  <tr>
    <td width="33%" align="center"><a href="docs/05-ai-agent-basics/"><img src="assets/illustrations/05-ai-agent-basics/q02-react-loop.webp" width="100%" alt="AI Agent 삽화: ReAct 추론과 행동 루프"></a><br><b>AI Agent</b></td>
    <td width="33%" align="center"><a href="docs/08-inference-optimization/"><img src="assets/illustrations/08-inference-optimization/q05-pagedattention.webp" width="100%" alt="추론 최적화 삽화: PagedAttention 메모리 관리"></a><br><b>학습·추론</b></td>
    <td width="33%" align="center"><a href="docs/10-production-deployment/"><img src="assets/illustrations/10-production-deployment/q12-llm-gateway.webp" width="100%" alt="프로덕션 AI 삽화: LLM Gateway 아키텍처"></a><br><b>안전·프로덕션</b></td>
  </tr>
</table>

<p align="center"><b>28개 주제 · 619개 질문 · 모든 질문에 1개씩 삽화 제공 완료</b></p>

## 직무별 학습 경로

| 직무 | 추천 경로 |
|---|---|
| AI / LLM 애플리케이션 엔지니어 | [LLM 기초](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [RAG](docs/03-rag-system/) → [Agent 기초](docs/05-ai-agent-basics/) → [프로덕션 배포](docs/10-production-deployment/) → [AI 시스템 설계](docs/25-system-design-ai/) |
| RAG 엔지니어 | [LLM 기초](docs/01-basic-concepts/) → [RAG](docs/03-rag-system/) → [벡터 검색](docs/06-vector-index-optimization/) → [고급 RAG](docs/20-rag-advanced-optimization/) → [안전·평가](docs/09-ai-safety-evaluation/) → [관측 가능성](docs/23-agent-observability/) |
| Agent 엔지니어 | [Prompt Engineering](docs/02-prompt-engineering/) → [Agent 기초](docs/05-ai-agent-basics/) → [계획·성찰](docs/22-agent-planning-reflection/) → [Multi-Agent](docs/13-multi-agent-systems/) → [MCP·Skills](docs/14-mcp-skill-systems/) → [관측 가능성](docs/23-agent-observability/) |
| 모델 학습·추론 엔지니어 | [Transformer](docs/04-transformer-architecture/) → [모델 학습](docs/07-model-training/) → [추론 최적화](docs/08-inference-optimization/) → [추론 프레임워크](docs/19-inference-frameworks/) |
| Forward Deployed Engineer | [프로젝트 심층 분석](docs/27-project-experience/) → [Python 엔지니어링](docs/24-python-engineering/) → [AI 시스템 설계](docs/25-system-design-ai/) → [FDE](docs/26-forward-deployed-engineer/) |
| 멀티모달 AI 엔지니어 | [Transformer](docs/04-transformer-architecture/) → [멀티모달 AI](docs/11-multimodal-ai/) → [멀티모달 Agent](docs/21-multimodal-agents/) → [프로덕션 배포](docs/10-production-deployment/) |
| AI 안전·평가 엔지니어 | [LLM 기초](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [안전·평가](docs/09-ai-safety-evaluation/) → [Test Harness·평가](docs/28-test-harness-evaluation/) → [관측 가능성](docs/23-agent-observability/) → [프로덕션 배포](docs/10-production-deployment/) |

## 주제 구성

- **기초와 모델:** LLM 기초, Transformer, 모델 학습, 추론 최적화, 추론 프레임워크.
- **RAG와 검색:** RAG 시스템, 벡터 인덱스 최적화, 프로덕션 RAG.
- **Agent와 프로토콜:** Agent 기초, Multi-Agent, MCP/Skills, 계획, 관측 가능성.
- **엔지니어링과 시스템 설계:** 안전 평가, 프로덕션 배포, Python, AI 시스템 설계, FDE, [Test Harness·평가](docs/28-test-harness-evaluation/).
- **멀티모달과 최신 주제:** 멀티모달 AI, AI 코딩 도구, 고급 주제.
- **면접 준비:** 이력서, 면접 출처 정리, 프로젝트 심층 질문.

[중국어 README의 전체 주제 목록](README.md#catalog)을 확인할 수 있습니다.

## 활용 방법

각 질문마다 세 가지 답변을 준비하세요.

1. **30초 답변:** 결론과 핵심 판단을 먼저 말합니다.
2. **3분 답변:** 원리, 대안, 트레이드오프를 설명합니다.
3. **심층 답변:** 검증 방법, 실패 대응, 다른 방식을 선택하지 않은 이유를 설명합니다.

예시 수치는 반드시 자신의 실제 프로젝트 데이터로 바꾸세요. 제품 동작, 가격, 벤치마크 결과는 변할 수 있으므로 공식 문서나 원 논문을 확인해야 합니다.

## 기여하기

질문을 추가하거나 수정하기 전에 [콘텐츠 품질 정책](CONTENT_QUALITY.md)을 확인하세요. 번역 개선도 환영합니다. 유지 관리되는 전체 번역본이 마련되기 전까지 중국어 질문 은행을 기준본으로 사용합니다.

문제는 [Issue](https://github.com/guocong-bincai/ai-interview-guide/issues)에 보고하고, 수정 사항은 [Pull Request](https://github.com/guocong-bincai/ai-interview-guide/pulls)로 보내 주세요.

## 라이선스

[MIT](LICENSE)
