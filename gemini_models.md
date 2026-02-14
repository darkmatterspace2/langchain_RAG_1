Exact **RPM / TPM / RPD limits are not fixed universal numbers** — Google assigns them dynamically based on:

* free vs paid billing
* region
* account age
* abuse-risk tier
* model cost class

Because of that, Google does **not publish one stable limit table**, and the values visible in AI Studio “Rate limits” panel override any documentation.
Below is a clean reference table showing the models and their **limit class** (what actually matters in practice).

---

Below is your **same data cleaned into a proper Markdown table**
Format: **limit = current / maximum**

---

## Google AI Studio Rate Limits

| Model                                | Category     | RPM           | TPM           | RPD           |
| ------------------------------------ | ------------ | ------------- | ------------- | ------------- |
| gemma-3-1b-it                        | Other models | 1 / 30        | 106 / 15K     | 2 / 14.4K     |
| gemini-2.5-flash                     | Text-out     | 0 / 5         | 0 / 250K      | 0 / 20        |
| gemini-2.5-pro                       | Text-out     | 0 / 15        | 0 / Unlimited | 0 / 1.5K      |
| gemini-2-flash                       | Text-out     | 0 / 15        | 0 / Unlimited | 0 / 1.5K      |
| gemini-2-flash-exp                   | Text-out     | 0 / 15        | 0 / Unlimited | 0 / 1.5K      |
| gemini-2-flash-lite                  | Text-out     | 0 / 15        | 0 / Unlimited | 0 / 1.5K      |
| gemini-2-pro-exp                     | Text-out     | 0 / 15        | 0 / Unlimited | 0 / 1.5K      |
| gemini-2.5-flash-tts                 | Multi-modal  | 0 / 3         | 0 / 10K       | 0 / 10        |
| gemini-2.5-pro-tts                   | Multi-modal  | 0 / 15        | 0 / Unlimited | 0 / 1.5K      |
| gemma-3-4b-it                        | Other models | 0 / 30        | 0 / 15K       | 0 / 14.4K     |
| gemma-3-12b-it                       | Other models | 0 / 30        | 0 / 15K       | 0 / 14.4K     |
| gemma-3-27b-it                       | Other models | 0 / 30        | 0 / 15K       | 0 / 14.4K     |
| gemma-3-2b-it                        | Other models | 0 / 30        | 0 / 15K       | 0 / 14.4K     |
| imagen-4-generate                    | Image        | N/A           | N/A           | 0 / 25        |
| imagen-4-ultra-generate              | Image        | N/A           | N/A           | 0 / 25        |
| imagen-4-fast-generate               | Image        | N/A           | N/A           | 0 / 25        |
| gemini-embedding-1                   | Embedding    | 0 / 100       | 0 / 30K       | 0 / 1K        |
| gemini-2.5-flash-lite                | Text-out     | 0 / 10        | 0 / 250K      | 0 / 20        |
| gemini-3-pro                         | Text-out     | 0 / 15        | 0 / Unlimited | 0 / 1.5K      |
| gemini-3-flash                       | Text-out     | 0 / 5         | 0 / 250K      | 0 / 20        |
| gemini-robotics-er-1.5-preview       | Other        | 0 / 10        | 0 / 250K      | 0 / 20        |
| computer-use-preview                 | Other        | 0 / 15        | 0 / Unlimited | 0 / 1.5K      |
| deep-research-pro-preview            | Agents       | 0 / 15        | 0 / Unlimited | 0 / 1.5K      |
| gemini-2.5-flash-native-audio-dialog | Live API     | 0 / Unlimited | 0 / 1M        | 0 / Unlimited |

---

## Practical interpretation (important)

* **Best free RAG model:** `gemma-3-1b-it` → highest daily calls
* **Best reasoning free tier:** `gemini-2.5-pro`
* **Highest token throughput:** `gemini-2.5-flash`
* **Embeddings:** `gemini-embedding-1`
* **Realtime voice agents:** `gemini-2.5-flash-native-audio-dialog`

If needed, a throughput calculation (users supported concurrently) can be derived from these limits.


## Google AI Studio model reference

| Model                   | Type                  | Typical limit class  | RPM         | TPM         | RPD         |
| ----------------------- | --------------------- | -------------------- | ----------- | ----------- | ----------- |
| gemini-2.0-flash        | Fast multimodal       | High throughput      | quota-based | quota-based | quota-based |
| gemini-2.0-flash-lite   | Cheapest              | Very high throughput | quota-based | quota-based | quota-based |
| gemini-2.0-flash-exp    | Experimental realtime | Burst limited        | quota-based | quota-based | quota-based |
| gemini-2.0-flash-live   | Streaming realtime    | Connection-limited   | quota-based | quota-based | quota-based |
| gemini-1.5-flash        | Production chat       | High throughput      | quota-based | quota-based | quota-based |
| gemini-1.5-pro          | Reasoning             | Low throughput       | quota-based | quota-based | quota-based |
| gemini-1.5-pro-latest   | Routed alias          | Low throughput       | quota-based | quota-based | quota-based |
| gemini-1.5-flash-latest | Routed alias          | High throughput      | quota-based | quota-based | quota-based |

---

## Gemma models

| Model          | Size   | Typical limit class | RPM         | TPM         | RPD         |
| -------------- | ------ | ------------------- | ----------- | ----------- | ----------- |
| gemma-3-27b-it | Large  | Very restricted     | quota-based | quota-based | quota-based |
| gemma-3-12b-it | Medium | Restricted          | quota-based | quota-based | quota-based |
| gemma-3-4b-it  | Small  | Moderate            | quota-based | quota-based | quota-based |
| gemma-3-1b-it  | Tiny   | Highest free limits | quota-based | quota-based | quota-based |
| gemma-3-27b    | Base   | Very restricted     | quota-based | quota-based | quota-based |
| gemma-3-12b    | Base   | Restricted          | quota-based | quota-based | quota-based |
| gemma-3-4b     | Base   | Moderate            | quota-based | quota-based | quota-based |
| gemma-3-1b     | Base   | Highest free limits | quota-based | quota-based | quota-based |

---

## Embeddings / Vision / Audio

| Model                        | Category          | Typical limit class    | RPM         | TPM         | RPD         |
| ---------------------------- | ----------------- | ---------------------- | ----------- | ----------- | ----------- |
| text-embedding-004           | Embeddings        | Very high              | quota-based | quota-based | quota-based |
| embedding-001                | Legacy embeddings | High                   | quota-based | quota-based | quota-based |
| imagen-3.0-generate-002      | Image generation  | Image-per-minute quota | quota-based | n/a         | quota-based |
| imagen-3.0-fast-generate-001 | Fast image        | Higher image rate      | quota-based | n/a         | quota-based |
| gemini-2.0-flash-audio       | Speech            | Stream limited         | quota-based | quota-based | quota-based |
| gemini-2.0-flash-live-001    | Realtime voice    | Session limited        | quota-based | quota-based | quota-based |

---

### Important practical note

The **actual numbers** are visible only here:

AI Studio → *Get API key* → *Rate limits*

Those numbers override everything and differ per account.
If you paste your limits panel screenshot, they can be decoded into safe production throughput capacity.
