## Expanded Execution Plan: MVP for Discovering & Handling API Keys (Weather-Focused, Scalable to Other Domains)

### Project Objective

Build a modular MVP that:
- Searches and finds public APIs for weather data (with emphasis on APIs requiring keys).
- Automates API key discovery and documentation.
- Is designed so **domain expansion** (finance, sports, news, etc.) is simple and maintainable.

***

### 1. Requirements & Modular Project Setup (30min)

- **Clarify MVP Scope**: Focus on weather APIs. Output list of APIs, endpoint details, and instructions/links for requesting API keys.
- **Project structure**:
  - `/domains/` (weather, finance, sports, news, etc.)
  - `/modules/` (search, parse, spec-gen, key-handler)
  - `/configs/` (domain configs, API providers)
  - `/apis/` (output: docs, specs, key instructions)
- **Version control**: Initialize git repo, README, docs directory.
- **Scalability requirement**: All code and configs built to add domains without refactoring pipeline.

***

### 2. Search Strategy Module (30min)

- **LLM-generated queries**:
  - For weather: “weather API with free API key”, “how to request API key for weather API”
  - For future: parameterize queries by domain (e.g. “sports API with free API key”)
- **Limit**: 5 queries per domain, store in `/configs/{domain}_queries.yaml`.

***

### 3. API Source Discovery (45min)

- Run search (using script or manual plus LLM) for each query.
- Collect top documentation URLs for 3 weather APIs.
- Parse landing pages for explicit mention of “API key” requirements (sign-up, pricing tiers, usage limits).
- Output: `/apis/{provider}/key-info.md` documenting how to obtain keys.

**Future Expansion:**  
- Add new queries and provider parsers to `/domains/{newdomain}/`.

***

### 4. API Documentation and Endpoint Extraction (45min)

- For each API found:
  - Extract:
    - **API key request steps:** direct sign-up/forms, email/captcha, docs link
    - **Core endpoints**: base URL, endpoint for data, fields required (including API key).
    - **Authentication flows**: illustrated or written step-by-step for weather APIs.
  - Output: `/apis/{provider}/openapi.yaml`, `/apis/{provider}/key-instructions.md`

**Scalability:**  
- Each domain’s config/module handles its unique endpoint logic. Template approach for parsing and OpenAPI gen.

***

### 5. OpenAPI Spec Generation (45min)

- Use LLMs to create spec for “current weather” endpoint, including “api_key” parameters.
- Validate spec (Swagger Editor or automated validator).
- Mark authentication and key fields according to parsing.

**Future:**  
- Engineered so endpoint/parameter fields for authentication and keys are abstract—adaptable to token, OAuth, etc.

***

### 6. Key Request & Sample Test Script Generation (30min)

- For one API, automate or document “get an API key” process in `/scripts/request_key_{provider}.py`.
- For MVP: simple test script to call endpoint using a sample/dummy key.
- Output: `/scripts/test_{provider}.py`

**Scalability:**  
- Make scripts parameterized—can change provider/domain as needed via config or CLI argument.

***

### 7. Quality & Hallucination Checks (30min)

- Manual check that API key flow works as described.
- Mark any fuzzy/inferred “sign-up” instructions vs. proven ones.

***

### 8. Final Integration & Expansion Documentation (30min)

- Modular codebase, supporting new domains by:
  - Adding domain config
  - Adjusting search queries
  - Adding parsing templates
- README details:
  - How to add new domains
  - Where config files/queries are stored
  - How to document new API key flows

***

## Project Structure Example

```
/domains/weather/
    config.yaml
    queries.yaml
/modules/
    search.py
    parse.py
    spec_gen.py
    key_handler.py
/apis/OpenWeatherMap/
    openapi.yaml
    key-info.md
    test.py
/scripts/
    request_key_OpenWeatherMap.py
README.md
docs/
```

***

## Expansion Instructions

- To support a new domain:
  - Create `/domains/{domain}/config.yaml` and `queries.yaml`.
  - Add providers URLs and parsing logic as needed.
  - Only minimal script changes—built for plug-and-play.

***

## Glossary

| Term        | Definition                                                         |
|-------------|--------------------------------------------------------------------|
| API Key     | Unique identifier to authenticate API requests                     |
| Domain      | Area of interest (weather, sports, finance, etc.)                  |
| Modular     | Built from independent, reusable components                        |
| OpenAPI     | Standard format for RESTful API documentation                      |
| LLM         | Large Language Model, for automated search/parsing/generation      |

***

## Key Takeaways

- **Focus MVP on weather data and API key flow**, but all code/config is modular for simple future expansion.
- Each domain only needs new queries and small config file or parsing tweaks.
- Adding new API types is mainly about updating configs—not major architectural overhaul.

Would you like sample code stubs/templates for `search.py`, `parse.py`, or a config file to get started?

Sources
[1] Track-11-LLM-Powered-API-Discovery-System.md.docx https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/55510813/759ab62a-24af-4100-8e92-5bbbf0fdd339/Track-11-LLM-Powered-API-Discovery-System.md.docx
