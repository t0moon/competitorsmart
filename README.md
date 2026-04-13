# CompetitorSmart - Multilingual README

<details>
  <summary>🌐 Language / 语言</summary>

- [简体中文](#lang-zh)
- [English](#lang-en)
- [Español](#lang-es)
- [Français](#lang-fr)
- [Deutsch](#lang-de)
- [日本語](#lang-ja)
- [한국어](#lang-ko)
- [Português (Brasil)](#lang-pt-br)

</details>

---

<a id="lang-zh"></a>
## 简体中文

面向 **产品经理 / PMM** 的 AI 辅助竞争情报工具。主流程为 **LangGraph ReAct Agent**：通过 DuckDuckGo 检索与网页抓取收集证据，调用 **智谱 GLM**（OpenAI 兼容接口）自主补全信息，最终输出 **11 章** Markdown 深度报告（市场、竞品分层、能力、商业化、增长、SWOT、壁垒与机会等）。

默认模型与 API Base 在 `src/constants.py` 统一维护（当前默认：`glm-4.7`）。

### 功能概览

| 项目 | 说明 |
|------|------|
| Agent 流程 | 搜索 -> 抓取 -> 推理；关键结论需附来源 URL，报告有字数与章节完整性约束 |
| 报告输出 | `outputs/agent/<timestamp>_agent_report.md` |
| 模型与 Key | 智谱；支持 `ZHIPU_API_KEY_1` 到 `ZHIPU_API_KEY_4`（任一生效即可用于 Agent） |
| 输入方式 | 命令行竞品列表，或 `competitors_input.json` 结构化上下文（市场、品类、官网文案等） |

`requirements.txt` 中还包含 CRM、Notion、表格等集成依赖供扩展使用；**一键跑通报告仅需智谱 Key + Agent 相关包**（见下文）。

### 环境准备

- **Python**：建议 3.10+
- **复制环境模板**：将 `.env.example` 复制为 `.env`，至少填写 `ZHIPU_API_KEY_1`
- **可选**：通过 `ZHIPU_API_BASE_URL` 覆盖默认智谱 OpenAI 兼容地址

**安全**：不要将 `.env` 提交到版本库。仓库已忽略 `.env`；若使用 Git，可设置 `git config core.hooksPath githooks` 启用预提交钩子，避免误提交密钥文件。

### 安装

```bash
pip install -r requirements.txt
```

若仅 Agent 报错缺包，可针对性安装：

```bash
pip install langgraph langchain-openai duckduckgo-search
```

### 使用方式

```bash
# 根目录已有 competitors_input.json 且其中包含竞品列表时
python main.py

# 快速指定竞品（逗号分隔），可选赛道描述
python main.py --competitors "竞品A,竞品B" --market "SaaS CRM"

# 指定 JSON 输入文件（推荐：可带 website_copy、sales_notes 等）
python main.py --input competitors_input.json

# 仅校验配置与依赖，不调用 API
python main.py --dry-run
```

**报告目录**：`outputs/agent/`。

### 报告结构（Agent 模板）

最终 Markdown 固定包含以下二级章节（详见 `src/agent/graph.py` 内 `SYSTEM_PROMPT`）：

1. 报告概述
2. 市场与赛道分析
3. 竞品选择与分层
4. 核心能力拆解（每竞品单独小节）
5. 商业模式分析
6. 增长与分发策略
7. 用户与场景分析
8. 优劣势对比（SWOT / 对比矩阵）
9. 关键差异与壁垒
10. 机会点与策略建议
11. 数据附录（含来源列表等）

单次运行可能耗时较长；若遇额度或限流，可更换 Key 或稍后重试。

### 输入说明

- **`--competitors`**：仅名称，适合试跑；Agent 自行检索官网与第三方信息。
- **`competitors_input.json`**：可包含 `market`、`product_category`、`geography`、`our_product`、`competitors[].name`、`category`、`website`、`website_copy`、`sales_notes` 等字段，与 `src/config.py` 中 `Config` 加载逻辑一致。
- 人工整理竞品档案时可参考 `src/templates/competitor_profile.md`。

### 仓库目录（核心）

```text
main.py                    CLI 入口
competitors_input.json     结构化输入示例（可自命名并通过 --input 指定）
outputs/agent/             Agent 生成的 Markdown 报告

src/
  constants.py             默认模型名、智谱 API Base
  config.py                环境变量与 JSON 输入解析
  agent/                   LangGraph Agent（工具、图、校验）
  integrations/ai/         智谱 OpenAI 兼容客户端与 Key 选择
  models/                  竞品等数据模型
  prompts/                 历史多步流程提示模板（当前主流程未使用）
  templates/               竞品资料填写参考

skills/                    PM 方法论技能库（Claude / Lenny 等），供人或 AI 辅助分析时引用
AGENTS.md                  给协作者与 AI 的详细说明（技能索引、启动命令）
```

### 方法论提示

- 叙事与功能并重，结论尽量有买家语境。
- 先承认对手强项，再谈差异化更可信。
- 多用可验证来源；AI 加速搜集，业务判断仍需人工交叉验证。
- 竞品情报应持续更新，单次报告是快照而非终稿。

### 延伸阅读

- 环境变量逐项说明：`.env.example`
- 技能库与项目约定：**[AGENTS.md](AGENTS.md)**

---

<a id="lang-en"></a>
## English

An AI-assisted competitive intelligence toolkit for **Product Managers / PMMs**. The core workflow is a **LangGraph ReAct Agent**: it gathers evidence through DuckDuckGo search and web scraping, uses **Zhipu GLM** (OpenAI-compatible API) to fill missing context, and produces an **11-section** in-depth Markdown report (market, competitor tiers, capabilities, monetization, growth, SWOT, moats, and opportunities).

The default model and API base are managed centrally in `src/constants.py` (current default: `glm-4.7`).

### Feature Overview

| Item | Description |
|------|-------------|
| Agent workflow | Search -> Fetch -> Reason; key conclusions must include source URLs, and report length/section completeness is enforced |
| Report output | `outputs/agent/<timestamp>_agent_report.md` |
| Model & keys | Zhipu; supports `ZHIPU_API_KEY_1` to `ZHIPU_API_KEY_4` (any valid key can run the Agent) |
| Input options | CLI competitor list, or structured context via `competitors_input.json` (market, category, website copy, etc.) |

`requirements.txt` also includes CRM, Notion, spreadsheet, and other integration dependencies for extension scenarios; **to run report generation end-to-end, you only need a Zhipu key plus Agent-related packages** (see below).

### Environment Setup

- **Python**: 3.10+ recommended
- **Copy env template**: copy `.env.example` to `.env`, and fill at least `ZHIPU_API_KEY_1`
- **Optional**: override the default Zhipu OpenAI-compatible endpoint with `ZHIPU_API_BASE_URL`

**Security**: never commit `.env` to version control. This repo already ignores `.env`; if using Git, you can set `git config core.hooksPath githooks` to enable pre-commit hooks and reduce accidental key exposure.

### Installation

```bash
pip install -r requirements.txt
```

If only Agent packages are missing:

```bash
pip install langgraph langchain-openai duckduckgo-search
```

### Usage

```bash
# When competitors_input.json exists in the root and includes competitors
python main.py

# Quickly pass competitors (comma-separated) with optional market description
python main.py --competitors "CompetitorA,CompetitorB" --market "SaaS CRM"

# Specify a JSON input file (recommended: include website_copy, sales_notes, etc.)
python main.py --input competitors_input.json

# Validate config and dependencies only (no API calls)
python main.py --dry-run
```

**Report directory**: `outputs/agent/`.

### Report Structure (Agent Template)

Final Markdown always contains the following H2 sections (see `SYSTEM_PROMPT` in `src/agent/graph.py`):

1. Executive Overview
2. Market and Category Analysis
3. Competitor Selection and Segmentation
4. Core Capability Breakdown (one subsection per competitor)
5. Business Model Analysis
6. Growth and Distribution Strategy
7. User and Use-Case Analysis
8. Strengths/Weaknesses Comparison (SWOT / comparison matrix)
9. Key Differentiators and Moats
10. Opportunity Areas and Strategic Recommendations
11. Data Appendix (including sources)

A run may take time. If you hit quota or rate limits, switch keys or retry later.

### Input Notes

- **`--competitors`**: names only, suitable for quick runs; the Agent finds official and third-party information autonomously.
- **`competitors_input.json`**: can include `market`, `product_category`, `geography`, `our_product`, `competitors[].name`, `category`, `website`, `website_copy`, `sales_notes`, etc., aligned with `Config` loading logic in `src/config.py`.
- For manually curated competitor profiles, refer to `src/templates/competitor_profile.md`.

### Repository Structure (Core)

```text
main.py                    CLI entry point
competitors_input.json     Structured input example (custom filename supported via --input)
outputs/agent/             Agent-generated Markdown reports

src/
  constants.py             Default model name and Zhipu API base
  config.py                Environment and JSON input parsing
  agent/                   LangGraph Agent (tools, graph, validation)
  integrations/ai/         Zhipu OpenAI-compatible client and key selection
  models/                  Data models (competitors, etc.)
  prompts/                 Legacy multi-step prompt templates (not used by current main flow)
  templates/               Competitor profile reference template

skills/                    PM methodology skill library (Claude / Lenny, etc.) for human or AI-assisted analysis
AGENTS.md                  Detailed instructions for collaborators and AI (skill index, startup commands)
```

### Methodology Notes

- Balance narrative and feature facts; frame conclusions in buyer context where possible.
- Acknowledge competitor strengths first, then discuss differentiation for higher credibility.
- Prefer verifiable sources; AI speeds up collection, but business judgment still requires human cross-validation.
- Competitive intelligence should be updated continuously; each report is a snapshot, not a final truth.

### Further Reading

- Environment variable reference: `.env.example`
- Skill library and project conventions: **[AGENTS.md](AGENTS.md)**

---

<a id="lang-es"></a>
## Español

Herramienta de inteligencia competitiva asistida por IA para **Product Managers / PMM**. El flujo principal usa un **LangGraph ReAct Agent**: recopila evidencia mediante búsqueda en DuckDuckGo y scraping web, utiliza **Zhipu GLM** (API compatible con OpenAI) para completar contexto faltante y genera un informe Markdown profundo de **11 secciones** (mercado, segmentación competitiva, capacidades, monetización, crecimiento, SWOT, barreras y oportunidades).

El modelo por defecto y la API base se mantienen en `src/constants.py` (valor actual: `glm-4.7`).

### Resumen de Funcionalidades

| Elemento | Descripción |
|----------|-------------|
| Flujo del Agent | Buscar -> Obtener -> Razonar; las conclusiones clave deben incluir URL de fuente y se valida longitud/completitud del informe |
| Salida del informe | `outputs/agent/<timestamp>_agent_report.md` |
| Modelo y claves | Zhipu; compatible con `ZHIPU_API_KEY_1` a `ZHIPU_API_KEY_4` (cualquier clave válida sirve) |
| Entradas | Lista de competidores por CLI o contexto estructurado en `competitors_input.json` (mercado, categoría, textos de web, etc.) |

`requirements.txt` también incluye dependencias de CRM, Notion, hojas de cálculo y otras integraciones para escenarios extendidos; **para ejecutar el informe de punta a punta solo necesitas clave de Zhipu + paquetes del Agent**.

### Preparación del Entorno

- **Python**: se recomienda 3.10+
- **Copiar plantilla**: copia `.env.example` a `.env` y completa al menos `ZHIPU_API_KEY_1`
- **Opcional**: sobrescribe el endpoint por defecto con `ZHIPU_API_BASE_URL`

**Seguridad**: no subas `.env` al repositorio. Este proyecto ya ignora `.env`; si usas Git, puedes habilitar hooks con `git config core.hooksPath githooks` para reducir riesgos de exponer claves.

### Instalación

```bash
pip install -r requirements.txt
```

Si faltan solo paquetes del Agent:

```bash
pip install langgraph langchain-openai duckduckgo-search
```

### Uso

```bash
# Si existe competitors_input.json en la raíz y contiene competidores
python main.py

# Definir competidores rápidamente (separados por coma), con mercado opcional
python main.py --competitors "CompetidorA,CompetidorB" --market "SaaS CRM"

# Especificar un JSON de entrada (recomendado: website_copy, sales_notes, etc.)
python main.py --input competitors_input.json

# Validar configuración y dependencias sin llamar API
python main.py --dry-run
```

**Directorio de informes**: `outputs/agent/`.

### Estructura del Informe (Plantilla del Agent)

El Markdown final contiene siempre estas secciones de nivel 2 (ver `SYSTEM_PROMPT` en `src/agent/graph.py`):

1. Resumen ejecutivo
2. Análisis de mercado y categoría
3. Selección y segmentación de competidores
4. Desglose de capacidades clave (subsección por competidor)
5. Análisis de modelo de negocio
6. Estrategia de crecimiento y distribución
7. Análisis de usuarios y escenarios
8. Comparación de fortalezas y debilidades (SWOT / matriz comparativa)
9. Diferenciadores clave y barreras
10. Oportunidades y recomendaciones estratégicas
11. Apéndice de datos (incluye fuentes)

Una ejecución puede tardar. Si encuentras límites de cuota o tasa, cambia de clave o reintenta más tarde.

### Notas de Entrada

- **`--competitors`**: solo nombres; ideal para pruebas rápidas. El Agent busca información oficial y de terceros automáticamente.
- **`competitors_input.json`**: puede incluir `market`, `product_category`, `geography`, `our_product`, `competitors[].name`, `category`, `website`, `website_copy`, `sales_notes`, etc., alineado con la carga `Config` en `src/config.py`.
- Para fichas manuales de competidores, consulta `src/templates/competitor_profile.md`.

### Estructura del Repositorio (Núcleo)

```text
main.py                    Punto de entrada CLI
competitors_input.json     Ejemplo de entrada estructurada (nombre personalizable via --input)
outputs/agent/             Informes Markdown generados por el Agent

src/
  constants.py             Modelo por defecto y API base de Zhipu
  config.py                Variables de entorno y parseo de JSON
  agent/                   LangGraph Agent (herramientas, grafo, validación)
  integrations/ai/         Cliente compatible OpenAI de Zhipu y selección de clave
  models/                  Modelos de datos (competidores, etc.)
  prompts/                 Plantillas legacy de flujo multi-paso (no usadas por el flujo principal actual)
  templates/               Plantilla de referencia para perfiles de competidores

skills/                    Biblioteca de habilidades PM (Claude / Lenny, etc.) para análisis asistido por humano o IA
AGENTS.md                  Guía detallada para colaboradores y agentes de IA (índice de skills, comandos)
```

### Notas Metodológicas

- Equilibra narrativa y capacidades; intenta ubicar conclusiones en contexto comprador.
- Reconocer primero los puntos fuertes del competidor mejora la credibilidad de la diferenciación.
- Prioriza fuentes verificables; la IA acelera la recolección, pero el juicio de negocio requiere validación humana.
- La inteligencia competitiva es continua; cada informe es una foto temporal.

### Lecturas Relacionadas

- Referencia de variables de entorno: `.env.example`
- Skills y convenciones del proyecto: **[AGENTS.md](AGENTS.md)**

---

<a id="lang-fr"></a>
## Français

Boite a outils d'intelligence concurrentielle assistee par IA pour les **Product Managers / PMM**. Le flux principal repose sur un **agent LangGraph ReAct** : il collecte des preuves via recherche DuckDuckGo et extraction web, utilise **Zhipu GLM** (API compatible OpenAI) pour completer le contexte manquant, puis produit un rapport Markdown approfondi en **11 sections** (marche, segmentation concurrentielle, capacites, monetisation, croissance, SWOT, barrieres et opportunites).

Le modele par defaut et l'API base sont centralises dans `src/constants.py` (defaut actuel : `glm-4.7`).

### Vue d'Ensemble des Fonctions

| Element | Description |
|---------|-------------|
| Flux Agent | Rechercher -> Recuperer -> Raisonner ; les conclusions cles doivent citer des URL sources, avec controles de longueur et de completude |
| Sortie rapport | `outputs/agent/<timestamp>_agent_report.md` |
| Modele et cles | Zhipu ; prend en charge `ZHIPU_API_KEY_1` a `ZHIPU_API_KEY_4` (une seule cle valide suffit) |
| Entrees | Liste de concurrents en CLI ou contexte structure via `competitors_input.json` (marche, categorie, texte web, etc.) |

`requirements.txt` contient aussi des dependances CRM, Notion, tableurs et autres integrations ; **pour lancer le rapport de bout en bout, seule une cle Zhipu + les paquets Agent sont necessaires**.

### Preparation de l'Environnement

- **Python** : version 3.10+ recommandee
- **Copier le modele** : copier `.env.example` vers `.env` et renseigner au minimum `ZHIPU_API_KEY_1`
- **Optionnel** : remplacer l'endpoint par defaut via `ZHIPU_API_BASE_URL`

**Securite** : ne jamais committer `.env`. Ce depot ignore deja `.env` ; avec Git, vous pouvez activer les hooks de pre-commit via `git config core.hooksPath githooks`.

### Installation

```bash
pip install -r requirements.txt
```

Si seuls les paquets Agent manquent :

```bash
pip install langgraph langchain-openai duckduckgo-search
```

### Utilisation

```bash
# Si competitors_input.json existe a la racine et contient des concurrents
python main.py

# Fournir rapidement des concurrents (separes par des virgules), avec marche optionnel
python main.py --competitors "ConcurrentA,ConcurrentB" --market "SaaS CRM"

# Specifier un fichier JSON d'entree (recommande : website_copy, sales_notes, etc.)
python main.py --input competitors_input.json

# Verifier configuration et dependances sans appel API
python main.py --dry-run
```

**Dossier des rapports** : `outputs/agent/`.

### Structure du Rapport (Template Agent)

Le Markdown final contient toujours les sections H2 suivantes (voir `SYSTEM_PROMPT` dans `src/agent/graph.py`) :

1. Resume executif
2. Analyse marche et categorie
3. Selection et segmentation des concurrents
4. Decomposition des capacites cle (une sous-section par concurrent)
5. Analyse du modele economique
6. Strategie de croissance et de distribution
7. Analyse des utilisateurs et cas d'usage
8. Comparatif forces/faiblesses (SWOT / matrice)
9. Differenciateurs cle et barrieres
10. Opportunites et recommandations strategiques
11. Annexe de donnees (sources incluses)

Une execution peut etre longue. En cas de quota ou de limitation de debit, changez de cle ou reessayez plus tard.

### Notes sur les Entrees

- **`--competitors`** : noms uniquement ; utile pour un test rapide. L'agent trouve automatiquement les informations officielles et tierces.
- **`competitors_input.json`** : peut inclure `market`, `product_category`, `geography`, `our_product`, `competitors[].name`, `category`, `website`, `website_copy`, `sales_notes`, etc., coherent avec la logique `Config` dans `src/config.py`.
- Pour des fiches concurrentielles manuelles, voir `src/templates/competitor_profile.md`.

### Structure du Depot (Noyau)

```text
main.py                    Point d'entree CLI
competitors_input.json     Exemple d'entree structuree (nom personnalisable via --input)
outputs/agent/             Rapports Markdown generes par l'agent

src/
  constants.py             Modele par defaut et API base Zhipu
  config.py                Variables d'environnement et parsing JSON
  agent/                   Agent LangGraph (outils, graphe, validation)
  integrations/ai/         Client OpenAI-compatible Zhipu et selection de cle
  models/                  Modeles de donnees (concurrents, etc.)
  prompts/                 Templates legacy multi-etapes (non utilises par le flux principal actuel)
  templates/               Reference pour completer les fiches concurrentielles

skills/                    Bibliotheque de methodes PM (Claude / Lenny, etc.) pour analyses assistees
AGENTS.md                  Guide detaille pour collaborateurs et IA (index des skills, commandes)
```

### Notes Methodologiques

- Equilibrer narration et fonctionnalites ; placer les conclusions dans le contexte acheteur.
- Reconnaitre d'abord les forces du concurrent rend la differenciation plus credible.
- Privilegier des sources verifiables ; l'IA accelere la collecte, mais l'analyse business doit etre validee humainement.
- L'intelligence concurrentielle est continue ; chaque rapport est un instantane.

### Lectures Complementaires

- Detail des variables d'environnement : `.env.example`
- Skills et conventions du projet : **[AGENTS.md](AGENTS.md)**

---

<a id="lang-de"></a>
## Deutsch

KI-unterstuetztes Competitive-Intelligence-Toolkit fur **Product Manager / PMM**. Der Kernablauf ist ein **LangGraph ReAct Agent**: Er sammelt Belege per DuckDuckGo-Suche und Web-Scraping, nutzt **Zhipu GLM** (OpenAI-kompatible API) zum Schliessen von Informationsluecken und erzeugt einen tiefen Markdown-Bericht mit **11 Abschnitten** (Markt, Wettbewerbssegmentierung, Faehigkeiten, Monetarisierung, Wachstum, SWOT, Burggraeben und Chancen).

Standardmodell und API-Basis werden zentral in `src/constants.py` gepflegt (aktueller Default: `glm-4.7`).

### Funktionsueberblick

| Punkt | Beschreibung |
|------|--------------|
| Agent-Ablauf | Suchen -> Abrufen -> Schlussfolgern; zentrale Aussagen brauchen Quellen-URLs, Laenge und Vollstaendigkeit werden geprueft |
| Berichtsausgabe | `outputs/agent/<timestamp>_agent_report.md` |
| Modell & Keys | Zhipu; unterstuetzt `ZHIPU_API_KEY_1` bis `ZHIPU_API_KEY_4` (ein gueltiger Key reicht) |
| Eingaben | Wettbewerberliste per CLI oder strukturierter Kontext via `competitors_input.json` (Markt, Kategorie, Website-Texte usw.) |

`requirements.txt` enthaelt auch Integrationsabhaengigkeiten fuer CRM, Notion, Tabellen usw.; **fuer den End-to-End-Report braucht man nur einen Zhipu-Key plus Agent-Pakete**.

### Umgebung vorbereiten

- **Python**: empfohlen 3.10+
- **Env-Vorlage kopieren**: `.env.example` nach `.env` kopieren und mindestens `ZHIPU_API_KEY_1` setzen
- **Optional**: Standard-Endpunkt via `ZHIPU_API_BASE_URL` ueberschreiben

**Sicherheit**: `.env` niemals committen. Das Repo ignoriert `.env` bereits; bei Git kann `git config core.hooksPath githooks` Pre-Commit-Hooks aktivieren.

### Installation

```bash
pip install -r requirements.txt
```

Falls nur Agent-Pakete fehlen:

```bash
pip install langgraph langchain-openai duckduckgo-search
```

### Nutzung

```bash
# Wenn competitors_input.json im Projektstamm existiert und Wettbewerber enthaelt
python main.py

# Wettbewerber schnell per Komma trennen, optional mit Marktbeschreibung
python main.py --competitors "WettbewerberA,WettbewerberB" --market "SaaS CRM"

# JSON-Eingabedatei angeben (empfohlen: website_copy, sales_notes usw.)
python main.py --input competitors_input.json

# Nur Konfiguration/Abhaengigkeiten pruefen, ohne API-Aufrufe
python main.py --dry-run
```

**Berichtsordner**: `outputs/agent/`.

### Berichtsstruktur (Agent-Template)

Der finale Markdown-Bericht enthaelt immer diese H2-Abschnitte (siehe `SYSTEM_PROMPT` in `src/agent/graph.py`):

1. Executive Summary
2. Markt- und Kategorieanalyse
3. Wettbewerberauswahl und Segmentierung
4. Analyse der Kernfaehigkeiten (ein Unterabschnitt pro Wettbewerber)
5. Geschaeftsmodellanalyse
6. Wachstums- und Distributionsstrategie
7. Nutzer- und Use-Case-Analyse
8. Vergleich von Staerken/Schwaechen (SWOT / Vergleichsmatrix)
9. Zentrale Differenzierungsmerkmale und Burggraeben
10. Chancenfelder und strategische Empfehlungen
11. Datenanhang (inklusive Quellen)

Ein Lauf kann laenger dauern. Bei Quoten- oder Rate-Limits bitte Key wechseln oder spaeter erneut versuchen.

### Hinweise zu Eingaben

- **`--competitors`**: nur Namen, gut fuer Schnelltests; der Agent recherchiert offizielle und Drittquellen selbststaendig.
- **`competitors_input.json`**: kann `market`, `product_category`, `geography`, `our_product`, `competitors[].name`, `category`, `website`, `website_copy`, `sales_notes` usw. enthalten; entspricht der `Config`-Logik in `src/config.py`.
- Fuer manuell gepflegte Wettbewerberprofile siehe `src/templates/competitor_profile.md`.

### Repository-Struktur (Kern)

```text
main.py                    CLI-Einstieg
competitors_input.json     Strukturiertes Eingabebeispiel (eigener Dateiname via --input moeglich)
outputs/agent/             Vom Agent erzeugte Markdown-Berichte

src/
  constants.py             Standardmodell und Zhipu API-Basis
  config.py                Umgebungsvariablen und JSON-Parsing
  agent/                   LangGraph Agent (Tools, Graph, Validierung)
  integrations/ai/         Zhipu OpenAI-kompatibler Client und Key-Auswahl
  models/                  Datenmodelle (Wettbewerber usw.)
  prompts/                 Legacy-Templates fuer Mehrschritt-Flow (im aktuellen Hauptablauf ungenutzt)
  templates/               Referenz fuer Wettbewerberprofil-Befuellung

skills/                    PM-Methodenbibliothek (Claude / Lenny usw.) fuer menschlich oder KI-gestuetzte Analyse
AGENTS.md                  Detaillierte Anleitung fuer Mitarbeitende und KI (Skill-Index, Startkommandos)
```

### Methodische Hinweise

- Story und Funktionsfakten ausbalancieren; Schlussfolgerungen moeglichst im Kaufkontext formulieren.
- Erst Staerken des Wettbewerbers anerkennen, dann Differenzierung herausarbeiten.
- Verifizierbare Quellen priorisieren; KI beschleunigt Sammlung, Business-Urteil braucht menschliche Plausibilisierung.
- Competitive Intelligence ist kontinuierlich; jeder Bericht ist nur eine Momentaufnahme.

### Weiterfuehrende Links

- Umgebungsvariablen im Detail: `.env.example`
- Skill-Bibliothek und Projektkonventionen: **[AGENTS.md](AGENTS.md)**

---

<a id="lang-ja"></a>
## 日本語

**プロダクトマネージャー / PMM** 向けの AI 競合インテリジェンスツールです。中核は **LangGraph ReAct Agent** で、DuckDuckGo 検索と Web スクレイピングで根拠を収集し、**Zhipu GLM**（OpenAI 互換 API）で不足情報を補完、最終的に **11 章構成** の詳細な Markdown レポート（市場、競合レイヤー、機能、収益化、成長、SWOT、参入障壁、機会）を生成します。

デフォルトモデルと API Base は `src/constants.py` で一元管理されています（現在の既定値: `glm-4.7`）。

### 機能概要

| 項目 | 説明 |
|------|------|
| Agent フロー | 検索 -> 取得 -> 推論。重要結論には出典 URL が必須で、文字数と章の完全性を検証 |
| レポート出力 | `outputs/agent/<timestamp>_agent_report.md` |
| モデルとキー | Zhipu。`ZHIPU_API_KEY_1` から `ZHIPU_API_KEY_4` をサポート（有効なキー 1 つで実行可能） |
| 入力方法 | CLI の競合一覧、または `competitors_input.json` の構造化コンテキスト（市場、カテゴリ、Web文言など） |

`requirements.txt` には CRM、Notion、表計算連携など拡張向け依存も含まれます。**レポート生成を一気通貫で実行するには、Zhipu キーと Agent 関連パッケージだけで十分です**。

### 環境準備

- **Python**: 3.10 以上を推奨
- **環境テンプレート複製**: `.env.example` を `.env` にコピーし、最低でも `ZHIPU_API_KEY_1` を設定
- **任意**: `ZHIPU_API_BASE_URL` で既定エンドポイントを上書き可能

**セキュリティ**: `.env` をリポジトリへコミットしないでください。このリポジトリは `.env` を無視済みです。Git を使う場合は `git config core.hooksPath githooks` で pre-commit フックを有効化できます。

### インストール

```bash
pip install -r requirements.txt
```

Agent 関連のみ不足する場合:

```bash
pip install langgraph langchain-openai duckduckgo-search
```

### 使い方

```bash
# ルートに competitors_input.json があり、競合一覧が含まれる場合
python main.py

# 競合をカンマ区切りで指定（市場説明は任意）
python main.py --competitors "競合A,競合B" --market "SaaS CRM"

# JSON 入力ファイルを指定（website_copy、sales_notes などを含める運用を推奨）
python main.py --input competitors_input.json

# API を呼ばずに設定と依存関係のみ検証
python main.py --dry-run
```

**レポート出力先**: `outputs/agent/`。

### レポート構成（Agent テンプレート）

最終 Markdown には次の H2 セクションが必ず含まれます（`src/agent/graph.py` の `SYSTEM_PROMPT` を参照）:

1. レポート概要
2. 市場・カテゴリ分析
3. 競合選定とレイヤリング
4. コア能力分解（競合ごとのサブセクション）
5. ビジネスモデル分析
6. 成長・流通戦略
7. ユーザーと利用シーン分析
8. 強み・弱み比較（SWOT / 比較マトリクス）
9. 主要差別化要因と参入障壁
10. 機会領域と戦略提案
11. データ付録（出典一覧を含む）

1 回の実行には時間がかかる場合があります。クォータやレート制限に当たった場合は、キーを変更するか時間を空けて再実行してください。

### 入力に関する補足

- **`--competitors`**: 名前のみ。試験実行向けで、公式情報と第三者情報は Agent が自動収集します。
- **`competitors_input.json`**: `market`、`product_category`、`geography`、`our_product`、`competitors[].name`、`category`、`website`、`website_copy`、`sales_notes` などを含められ、`src/config.py` の `Config` 読み込みロジックと整合します。
- 手動で競合プロフィールを整理する場合は `src/templates/competitor_profile.md` を参照してください。

### リポジトリ構成（主要）

```text
main.py                    CLI エントリ
competitors_input.json     構造化入力の例（--input で任意名ファイル指定可）
outputs/agent/             Agent が生成する Markdown レポート

src/
  constants.py             デフォルトモデル名と Zhipu API Base
  config.py                環境変数と JSON 入力の解析
  agent/                   LangGraph Agent（ツール、グラフ、検証）
  integrations/ai/         Zhipu OpenAI 互換クライアントとキー選択
  models/                  データモデル（競合など）
  prompts/                 旧マルチステップ用プロンプト（現行メインフローでは未使用）
  templates/               競合情報記入の参照テンプレート

skills/                    PM メソドロジースキル集（Claude / Lenny など）。人手または AI 支援分析で参照
AGENTS.md                  協働者と AI 向け詳細ガイド（スキル索引、起動コマンド）
```

### 方法論メモ

- ストーリーと機能事実の両方を重視し、結論は可能な限り買い手文脈で示す。
- まず競合の強みを認めた上で差別化を述べると説得力が高まる。
- 検証可能な情報源を優先する。収集は AI で高速化できるが、事業判断は人手での相互検証が必要。
- 競合情報は継続更新が前提。単発レポートは最終版ではなくスナップショット。

### 関連ドキュメント

- 環境変数の詳細: `.env.example`
- スキルライブラリとプロジェクト規約: **[AGENTS.md](AGENTS.md)**

---

<a id="lang-ko"></a>
## 한국어

**프로덕트 매니저 / PMM** 를 위한 AI 경쟁 인텔리전스 도구입니다. 핵심 흐름은 **LangGraph ReAct Agent** 로, DuckDuckGo 검색과 웹 스크래핑으로 근거를 수집하고 **Zhipu GLM**(OpenAI 호환 API)으로 누락 정보를 보강하여, 시장/경쟁사 계층/핵심 역량/수익화/성장/SWOT/진입장벽/기회 등을 포함한 **11개 섹션** Markdown 보고서를 생성합니다.

기본 모델과 API Base 는 `src/constants.py` 에서 통합 관리됩니다(현재 기본값: `glm-4.7`).

### 기능 개요

| 항목 | 설명 |
|------|------|
| Agent 흐름 | 검색 -> 수집 -> 추론. 핵심 결론에는 출처 URL 필수, 보고서 길이/섹션 완결성 검증 |
| 보고서 출력 | `outputs/agent/<timestamp>_agent_report.md` |
| 모델 및 키 | Zhipu. `ZHIPU_API_KEY_1` 부터 `ZHIPU_API_KEY_4` 까지 지원(유효 키 1개면 실행 가능) |
| 입력 방식 | CLI 경쟁사 목록 또는 `competitors_input.json` 구조화 컨텍스트(시장, 카테고리, 웹 카피 등) |

`requirements.txt` 에는 CRM, Notion, 스프레드시트 연동 등 확장용 의존성도 포함됩니다. **보고서 생성만 빠르게 실행하려면 Zhipu 키와 Agent 관련 패키지만 있으면 됩니다**.

### 환경 준비

- **Python**: 3.10+ 권장
- **환경 템플릿 복사**: `.env.example` 을 `.env` 로 복사하고 최소 `ZHIPU_API_KEY_1` 입력
- **선택 사항**: `ZHIPU_API_BASE_URL` 로 기본 엔드포인트 재정의 가능

**보안**: `.env` 를 버전 관리에 커밋하지 마세요. 저장소는 이미 `.env` 를 ignore 합니다. Git 사용 시 `git config core.hooksPath githooks` 로 pre-commit 훅을 설정할 수 있습니다.

### 설치

```bash
pip install -r requirements.txt
```

Agent 관련 패키지만 누락된 경우:

```bash
pip install langgraph langchain-openai duckduckgo-search
```

### 사용 방법

```bash
# 루트에 competitors_input.json 이 있고 경쟁사 목록이 포함된 경우
python main.py

# 경쟁사 이름을 쉼표로 전달, 시장 설명은 선택
python main.py --competitors "경쟁사A,경쟁사B" --market "SaaS CRM"

# JSON 입력 파일 지정(website_copy, sales_notes 포함 권장)
python main.py --input competitors_input.json

# API 호출 없이 설정/의존성만 점검
python main.py --dry-run
```

**보고서 디렉터리**: `outputs/agent/`.

### 보고서 구조(Agent 템플릿)

최종 Markdown 은 다음 H2 섹션을 고정 포함합니다(`src/agent/graph.py` 의 `SYSTEM_PROMPT` 참고):

1. 보고서 개요
2. 시장 및 카테고리 분석
3. 경쟁사 선정 및 계층화
4. 핵심 역량 분해(경쟁사별 하위 섹션)
5. 비즈니스 모델 분석
6. 성장 및 유통 전략
7. 사용자 및 사용 시나리오 분석
8. 강점/약점 비교(SWOT / 비교 매트릭스)
9. 핵심 차별점 및 진입장벽
10. 기회 영역 및 전략 제안
11. 데이터 부록(출처 목록 포함)

실행에는 시간이 걸릴 수 있습니다. 할당량 또는 속도 제한이 발생하면 키를 교체하거나 잠시 후 재시도하세요.

### 입력 설명

- **`--competitors`**: 이름만 입력하는 빠른 실행용 옵션. 공식/서드파티 정보는 Agent 가 자동 수집합니다.
- **`competitors_input.json`**: `market`, `product_category`, `geography`, `our_product`, `competitors[].name`, `category`, `website`, `website_copy`, `sales_notes` 등을 포함할 수 있으며 `src/config.py` 의 `Config` 로딩 로직과 일치합니다.
- 수동 경쟁사 프로필 정리는 `src/templates/competitor_profile.md` 를 참고하세요.

### 저장소 구조(핵심)

```text
main.py                    CLI 진입점
competitors_input.json     구조화 입력 예시(--input 으로 파일명 변경 가능)
outputs/agent/             Agent 생성 Markdown 보고서

src/
  constants.py             기본 모델명 및 Zhipu API Base
  config.py                환경 변수 및 JSON 입력 파싱
  agent/                   LangGraph Agent(도구, 그래프, 검증)
  integrations/ai/         Zhipu OpenAI 호환 클라이언트 및 키 선택
  models/                  데이터 모델(경쟁사 등)
  prompts/                 과거 다단계 프롬프트 템플릿(현재 메인 흐름 미사용)
  templates/               경쟁사 정보 작성 참고 템플릿

skills/                    PM 방법론 스킬 라이브러리(Claude / Lenny 등), 사람/AI 보조 분석에 활용
AGENTS.md                  협업자 및 AI 용 상세 안내(스킬 인덱스, 실행 명령)
```

### 방법론 팁

- 스토리와 기능 사실을 균형 있게 다루고, 결론은 구매자 맥락으로 제시합니다.
- 먼저 경쟁사의 강점을 인정한 뒤 차별화를 설명하면 신뢰도가 높아집니다.
- 검증 가능한 출처를 우선 사용하세요. AI 는 수집을 가속하지만 사업 판단은 사람의 교차 검증이 필요합니다.
- 경쟁 인텔리전스는 지속 업데이트가 핵심이며, 단일 보고서는 스냅샷입니다.

### 추가 문서

- 환경 변수 상세: `.env.example`
- 스킬 라이브러리 및 프로젝트 규칙: **[AGENTS.md](AGENTS.md)**

---

<a id="lang-pt-br"></a>
## Português (Brasil)

Ferramenta de inteligencia competitiva com IA para **Product Managers / PMM**. O fluxo principal usa um **LangGraph ReAct Agent**: coleta evidencias via busca DuckDuckGo e scraping web, usa **Zhipu GLM** (API compativel com OpenAI) para preencher lacunas de contexto e gera um relatorio Markdown aprofundado com **11 secoes** (mercado, segmentacao de concorrentes, capacidades, monetizacao, crescimento, SWOT, barreiras e oportunidades).

O modelo padrao e a API base ficam centralizados em `src/constants.py` (padrao atual: `glm-4.7`).

### Visao Geral de Funcionalidades

| Item | Descricao |
|------|-----------|
| Fluxo do Agent | Buscar -> Coletar -> Raciocinar; conclusoes-chave exigem URL de fonte e ha validacao de tamanho/completude |
| Saida de relatorio | `outputs/agent/<timestamp>_agent_report.md` |
| Modelo e chaves | Zhipu; suporta `ZHIPU_API_KEY_1` ate `ZHIPU_API_KEY_4` (qualquer chave valida funciona) |
| Formas de entrada | Lista de concorrentes via CLI ou contexto estruturado em `competitors_input.json` (mercado, categoria, texto de site etc.) |

`requirements.txt` tambem inclui dependencias de CRM, Notion, planilhas e outras integracoes para extensoes; **para rodar o relatorio de ponta a ponta, basta chave Zhipu + pacotes do Agent**.

### Preparacao do Ambiente

- **Python**: recomendado 3.10+
- **Copiar template de ambiente**: copie `.env.example` para `.env` e preencha ao menos `ZHIPU_API_KEY_1`
- **Opcional**: sobrescreva o endpoint padrao com `ZHIPU_API_BASE_URL`

**Seguranca**: nunca versione `.env`. O repositorio ja ignora `.env`; com Git, voce pode usar `git config core.hooksPath githooks` para ativar hooks de pre-commit.

### Instalacao

```bash
pip install -r requirements.txt
```

Se faltarem apenas pacotes do Agent:

```bash
pip install langgraph langchain-openai duckduckgo-search
```

### Uso

```bash
# Quando existir competitors_input.json na raiz com lista de concorrentes
python main.py

# Informar concorrentes rapidamente (separados por virgula), com mercado opcional
python main.py --competitors "ConcorrenteA,ConcorrenteB" --market "SaaS CRM"

# Especificar arquivo JSON de entrada (recomendado incluir website_copy, sales_notes etc.)
python main.py --input competitors_input.json

# Validar configuracao e dependencias sem chamar API
python main.py --dry-run
```

**Diretorio de relatorios**: `outputs/agent/`.

### Estrutura do Relatorio (Template do Agent)

O Markdown final sempre contem as secoes H2 abaixo (veja `SYSTEM_PROMPT` em `src/agent/graph.py`):

1. Visao geral executiva
2. Analise de mercado e categoria
3. Selecao e segmentacao de concorrentes
4. Decomposicao de capacidades centrais (uma subsecao por concorrente)
5. Analise de modelo de negocio
6. Estrategia de crescimento e distribuicao
7. Analise de usuarios e cenarios
8. Comparacao de forcas e fraquezas (SWOT / matriz comparativa)
9. Diferenciais-chave e barreiras
10. Oportunidades e recomendacoes estrategicas
11. Apendice de dados (inclui lista de fontes)

Uma execucao pode levar tempo. Se houver limite de cota ou taxa, troque a chave ou tente novamente depois.

### Notas de Entrada

- **`--competitors`**: apenas nomes; ideal para testes rapidos. O Agent busca informacoes oficiais e de terceiros automaticamente.
- **`competitors_input.json`**: pode incluir `market`, `product_category`, `geography`, `our_product`, `competitors[].name`, `category`, `website`, `website_copy`, `sales_notes` etc., em linha com a logica de carregamento `Config` em `src/config.py`.
- Para perfis de concorrentes montados manualmente, consulte `src/templates/competitor_profile.md`.

### Estrutura do Repositorio (Nucleo)

```text
main.py                    Entrada CLI
competitors_input.json     Exemplo de entrada estruturada (nome customizavel via --input)
outputs/agent/             Relatorios Markdown gerados pelo Agent

src/
  constants.py             Modelo padrao e API base da Zhipu
  config.py                Variaveis de ambiente e parsing de JSON
  agent/                   LangGraph Agent (ferramentas, grafo, validacao)
  integrations/ai/         Cliente Zhipu compativel com OpenAI e selecao de chave
  models/                  Modelos de dados (concorrentes etc.)
  prompts/                 Templates legados de fluxo multi-etapas (nao usados no fluxo principal atual)
  templates/               Referencia para preenchimento de perfil de concorrente

skills/                    Biblioteca de skills de metodologia PM (Claude / Lenny etc.) para analise assistida
AGENTS.md                  Guia detalhado para colaboradores e IA (indice de skills, comandos de inicializacao)
```

### Notas Metodologicas

- Equilibre narrativa e fatos de produto; formule conclusoes no contexto do comprador sempre que possivel.
- Reconhecer primeiro os pontos fortes do concorrente aumenta a credibilidade da diferenciacao.
- Priorize fontes verificaveis; IA acelera a coleta, mas julgamento de negocio exige validacao humana cruzada.
- Inteligencia competitiva e um processo continuo; cada relatorio e um retrato momentaneo.

### Leitura Complementar

- Detalhes de variaveis de ambiente: `.env.example`
- Biblioteca de skills e convencoes do projeto: **[AGENTS.md](AGENTS.md)**
