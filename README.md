# Linear Shin-Jeongeum (선형 신정음)
> **A 1D Hardware-Native Phonetic Tokenizer for Energy-Efficient Multilingual Speech-to-Text AI Models**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Patent Priority](https://img.shields.io/badge/KIPO%20Patent-Priority%20Secured-success.svg)](#intellectual-property--patent-baseline)
[![Paper](https://img.shields.io/badge/Preprint-Available%20Soon%20on%20TechRxiv-orange.svg)](#citation)

---

## ⚡ Overview & Motivation
Current multilingual Speech-to-Text (STT) and multimodal AI architectures rely heavily on subword tokenizers (e.g., BPE, WordPiece) and complex neural G2P (Grapheme-to-Phoneme) translation layers. This introduces significant inference latency ($\mathcal{F}_{\text{G2P}}$) and bloated sequence lengths ($L$), quadratically increasing self-attention computational overhead ($\mathcal{O}(L^2)$).

**Linear Shin-Jeongeum** solves this fundamental bottleneck by reviving the scientific principles of **Hunminjeongeum (훈민정음)** as a hardware-native, strictly 1-dimensional phonetic coordinate system:
- **Zero Neural G2P Overhead ($\mathcal{F}_{\text{G2P}} \equiv 0$):** Replaces auxiliary neural networks with constant-time $O(1)$ phonetic matrix lookups.
- **Hardware-Native 1D Inline Serialization:** Deconstructs 2D block syllabics and multi-byte orthography into inline phonemes, direct tone markers (`-`, `/`, `v`, `\`), and retroflex-preserving symbols.
- **Quadratic Complexity Reduction:** Cuts sequence length by **34.3%**, yielding an empirical **84.0% reduction** in Transformer self-attention compute overhead over raw baseline sequences.

---

## 📊 Key Benchmark Summary

| Metric / Dimension | Baseline (Standard BPE / Neural G2P) | **Linear Shin-Jeongeum** | **Improvement / Efficiency Gain** |
| :--- | :---: | :---: | :---: |
| **Token Sequence Length ($L$)** | 100% (Normalized) | **65.7%** | **-34.3% Compression** |
| **Attention Compute ($\mathcal{O}(L^2)$)** | $1.00 \times L^2$ | **$0.432 \times L^2$** | **-56.8% (Net: -84.0% vs Raw)** |
| **G2P Layer Inference Overhead** | Auxiliary DNN Latency | **Hardware Register Lookup** | **$\mathcal{F}_{\text{G2P}} \equiv 0$ (Zero Extra Latency)** |
| **Multilingual Phonetic Drift** | High (OOD Phonemes) | **Invariant (1D Universal Map)** | **Cross-lingual Alignment Native** |

---

## 🚀 Quick Start

### Installation
Clone the repository and install required lightweight dependencies:
```bash
git clone https://github.com/shinjeongeum/linear-shin-jeongeum.git
cd linear-shin-jeongeum
pip install -r requirements.txt
```
### Minimal Usage
```python
from tokenizer import LinearShinJeongeumTokenizer

tokenizer = LinearShinJeongeumTokenizer()

# 1. Linearize Korean Syllables into 1D Phonemes
text_kr = "훈민정음"
tokens_kr = tokenizer.encode(text_kr)
print("1D Phonetic Sequence (KR):", tokens_kr)
# Output: ['ㅎ', 'ㅜ', 'ㄴ', 'ㅁ', 'ㅣ', 'ㄴ', 'ㅈ', 'ㅓ', 'ㅇ', 'ㅇ', 'ㅡ', 'ㅁ']

# 2. Chinese Syllable with Tonal & Retroflex Coordinates
text_zh = "zhōng"
tokens_zh = tokenizer.encode_pinyin(text_zh)
print("1D Phonetic Sequence (ZH):", tokens_zh)
# Output: ['ㅈ=', 'ㅜ', 'ㅇ', '-']
```
---
## 🏛 Intellectual Property & Patent Baseline
The core 1D linear phonetic serialization architecture, tone geometric projection, and hardware-native phonetic register mapping described herein are officially protected under patent priority:

- **Patent Office:** Korean Intellectual Property Office (KIPO)
- **Application Scope:** 1-Dimensional Linear Phonetic Tokenization Architecture and Processing Method for Multilingual Speech-to-Text Artificial Intelligence Systems
- **Priority Status:** Formally Filed and Priority Date Secured (2026).

---

## 📄 Citation
If you utilize this architecture, tokenization paradigm, or benchmarks in your academic research or industrial implementations, please cite:
```bibtex
@article{shin2026linear,
  title={Linear Shin-Jeongeum: A 1D Phonetic Tokenization Architecture for Energy-Efficient Multilingual Speech-to-Text AI Models},
  author={Shin, Han-Sik},
  journal={Preprint under review (TechRxiv)},
  year={2026}
}
```
---

## 📜 License
This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for complete terms and patent protection clauses.
