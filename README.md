# KOMIR_proj: 광물종합지수 이상징후 탐지 PoC

## 1. 프로젝트 개요

본 프로젝트는 한국광해광업공단의 광물종합지수 데이터를 활용하여 광물 가격의 급등락, 변동성 확대, 추세 전환 가능성 등을 자동으로 탐지하는 이상징후 탐지 PoC입니다.

광물 가격과 지수 데이터는 시장 상황, 수급 불안, 글로벌 경기, 원자재 가격, 환율 등 다양한 요인의 영향을 받습니다. 따라서 담당자가 수작업으로 가격 변동을 확인하는 방식은 모니터링 부담이 크고, 급격한 변화나 복합적인 이상 패턴을 놓칠 수 있습니다.

본 프로젝트는 통계적 기준, 기술적 지표, 머신러닝 기반 이상탐지 모델을 함께 활용하여 광물종합지수의 이상구간을 탐지하고, 이상등급과 탐지사유를 함께 산출하는 것을 목표로 합니다.

---

## 2. 주요 기능

- 광물종합지수 데이터 로드
- 날짜 및 수치형 컬럼 전처리
- 등락율 기반 급등락 탐지
- 이동평균 대비 이격도 탐지
- 볼린저밴드 상·하단 이탈 탐지
- 표준편차 기반 변동성 확대 탐지
- RSI 기반 과매수·과매도 구간 탐지
- MACD 골든크로스·데드크로스 탐지
- Isolation Forest 기반 다변량 이상치 탐지
- 이상점수 및 이상등급 산출
- 이상징후 목록 CSV 저장
- 시계열 그래프 및 이상등급별 시각화 저장

---
## 3. 이상징후 탐지 기준 요약

본 프로젝트는 광물종합지수의 이상징후를 단일 기준이 아닌 여러 탐지 기준의 조합으로 판단합니다.

| 탐지 기준 | 판단 방식 |
|---|---|
| 등락율 Z-score | 등락율이 평균 대비 3표준편차 이상 벗어나면 이상 |
| 이격도 | 20일 이동평균 대비 85 이하 또는 115 이상이면 이상 |
| 볼린저밴드 | 지수가 상한선을 초과하거나 하한선을 이탈하면 이상 |
| 변동성 | 20일 표준편차의 Z-score가 2.5 이상이면 이상 |
| RSI | RSI가 20 이하 또는 80 이상이면 이상 |
| MACD | Golden Cross 또는 Dead Cross 발생 시 추세 전환 신호 |
| Isolation Forest | 여러 지표 조합상 비정상 패턴이면 이상 |

각 기준에 해당하면 1점씩 부여하며, 점수 합계에 따라 이상등급을 산정합니다.

| 점수 | 등급 |
|---:|---|
| 0 | 정상 |
| 1~2 | 주의 |
| 3~4 | 경계 |
| 5 이상 | 심각 |
---
## 4. 프로젝트 구조

```text
KOMIR_proj/
│
├── data/
│   └── 한국광해광업공단_파생지수_광물종합지수.csv
│
├── result/
│   ├── mineral_composite_index_anomaly_detection_full_result.csv
│   ├── mineral_composite_index_anomaly_list.csv
│   ├── plot_index_with_bands.png
│   ├── plot_anomaly_grade.png
│   ├── plot_return_rate.png
│   └── plot_volatility.png
│
├── fonts/
│   └── NanumGothic.ttf
│
└── src/
    ├── __init__.py
    ├── config.py
    ├── data_loader.py
    ├── preprocessing.py
    ├── anomaly_rules.py
    ├── save_results.py
    ├── visualization.py
    ├── main.py
    └── prototype.ipynb