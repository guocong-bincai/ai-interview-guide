<p align="center">
  <a href="README.md">简体中文</a> ·
  <a href="README_EN.md">English</a> ·
  <a href="README_JA.md">日本語</a> ·
  <a href="README_KO.md">한국어</a> ·
  <b>Português do Brasil</b> ·
  <a href="README_ES.md">Español</a> ·
  <a href="README_ID.md">Bahasa Indonesia</a>
</p>

# Manual de Entrevistas para Engenharia de IA

> Um guia estruturado para vagas de aplicações de IA, RAG, Agents, treinamento e inferência de modelos, FDE, multimodalidade e segurança de IA.

**568 perguntas · 27 tópicos · 7 trilhas por função**

> [!IMPORTANT]
> Esta página é uma tradução da apresentação do projeto. O banco completo de perguntas e respostas é mantido atualmente em chinês simplificado. Os links abaixo abrem o conteúdo em chinês.

## Por que usar este repositório

- **Orientado a vagas reais:** cobre competências recorrentes em funções de engenharia de IA, não apenas curiosidades isoladas.
- **Foco em decisões de engenharia:** discute qualidade, latência, custo, segurança, complexidade e alternativas.
- **Qualidade verificável:** uma auditoria identifica links quebrados, perguntas duplicadas e métricas precisas sem fonte.

## Escolha sua trilha

| Função | Trilha recomendada |
|---|---|
| Engenharia de Aplicações de IA / LLM | [Fundamentos de LLM](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [RAG](docs/03-rag-system/) → [Agents](docs/05-ai-agent-basics/) → [Produção](docs/10-production-deployment/) → [System Design de IA](docs/25-system-design-ai/) |
| Engenharia de RAG | [Fundamentos de LLM](docs/01-basic-concepts/) → [RAG](docs/03-rag-system/) → [Busca Vetorial](docs/06-vector-index-optimization/) → [RAG Avançado](docs/20-rag-advanced-optimization/) → [Segurança e Avaliação](docs/09-ai-safety-evaluation/) |
| Engenharia de Agents | [Prompt Engineering](docs/02-prompt-engineering/) → [Agents](docs/05-ai-agent-basics/) → [Planejamento e Reflexão](docs/22-agent-planning-reflection/) → [Multi-Agent](docs/13-multi-agent-systems/) → [MCP e Skills](docs/14-mcp-skill-systems/) |
| Engenharia de Treinamento e Inferência | [Transformer](docs/04-transformer-architecture/) → [Treinamento](docs/07-model-training/) → [Otimização de Inferência](docs/08-inference-optimization/) → [Frameworks de Inferência](docs/19-inference-frameworks/) |
| Forward Deployed Engineer | [Projetos em Profundidade](docs/27-project-experience/) → [Engenharia Python](docs/24-python-engineering/) → [System Design de IA](docs/25-system-design-ai/) → [FDE](docs/26-forward-deployed-engineer/) |
| Engenharia de IA Multimodal | [Transformer](docs/04-transformer-architecture/) → [IA Multimodal](docs/11-multimodal-ai/) → [Agents Multimodais](docs/21-multimodal-agents/) → [Produção](docs/10-production-deployment/) |
| Engenharia de Segurança e Avaliação | [Fundamentos de LLM](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [Segurança e Avaliação](docs/09-ai-safety-evaluation/) → [Observabilidade](docs/23-agent-observability/) |

## Mapa de tópicos

- **Fundamentos e modelos:** LLM, Transformer, treinamento, otimização e frameworks de inferência.
- **RAG e recuperação:** sistemas RAG, índices vetoriais e RAG avançado em produção.
- **Agents e protocolos:** fundamentos de Agents, Multi-Agent, MCP/Skills, planejamento e observabilidade.
- **Engenharia e system design:** segurança, produção, Python, system design de IA e FDE.
- **Multimodal e temas emergentes:** IA multimodal, ferramentas de programação com IA e tópicos avançados.
- **Preparação para entrevistas:** currículo, fontes de entrevistas e aprofundamento de projetos.

Veja o [catálogo completo no README em chinês](README.md#catalog).

## Como praticar

Prepare três versões para cada resposta:

1. **30 segundos:** apresente a decisão e o raciocínio central.
2. **3 minutos:** explique princípios, alternativas e trade-offs.
3. **Aprofundamento:** explique validação, tratamento de falhas e por que não escolheu outra abordagem.

Substitua métricas de exemplo por evidências do seu próprio trabalho. Comportamentos de produtos, preços e benchmarks mudam; confira informações temporais na documentação oficial ou no artigo original.

## Como contribuir

Leia a [política de qualidade de conteúdo](CONTENT_QUALITY.md) antes de alterar perguntas. Melhorias de tradução são bem-vindas. Até existir uma tradução completa com manutenção contínua, o banco em chinês é a fonte oficial.

Abra uma [Issue](https://github.com/guocong-bincai/ai-interview-guide/issues) para relatar problemas ou envie um [Pull Request](https://github.com/guocong-bincai/ai-interview-guide/pulls) com correções.

## Licença

[MIT](LICENSE)
