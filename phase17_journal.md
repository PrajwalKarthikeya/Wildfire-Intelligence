# Phase 17 Journey Journal: The Transition to Forecasting

We have reached the conceptual ceiling of our 40-hour MVP constraint. The final roadmap suggestion pushed us to transition from a "Real-Time Dashboard" to a "Spatiotemporal Forecasting System."

---

## 🧑‍🏫 Layman's Terms

Right now, our AI says: *"Based on the weather right now, this area is highly flammable right now."*
That is incredibly useful, but the holy grail of wildfire intelligence is asking the AI: *"Based on the weather today, will this area catch on fire tomorrow?"*

To test that, we would have to do "Backtesting." We would have to show the AI the weather from exactly 24 hours *before* a historical fire started, and see if it could have successfully sounded the alarm early. 

We can't actually do this right now. Why? Because we didn't download historical data! We only connected to the "Live" NASA feed for this weekend MVP. However, acknowledging this limitation and framing it as the "Next Step" proves that you are thinking like a Senior Engineer. We added this directly to the README as our Future Roadmap.

---

## 👩‍💻 Technical Terms

Evaluating a model on **Lead Time** ($\Delta t$) and **Spatial Accuracy** (Haversine $\Delta d$) requires a fundamental architectural shift.

Our current pipeline is a synchronous $T=0$ system. We fetch $T=0$ weather and map it against $T=0$ thermal anomalies to predict spatial risk.
To execute Lead-Time Backtesting (e.g., $T-24h \rightarrow T=0$), we would require:
1. **Archive Ingestion**: Bulk downloading NASA FIRMS archive datasets (which requires asynchronous ordering and processing, unlike the synchronous NRT API).
2. **Weather Reanalysis**: Querying historical ERA5 or Open-Meteo archive datasets to extract covariates exactly 6, 12, 24, and 48 hours prior to each ignition coordinate.
3. **Spatiotemporal Matrices**: Refactoring our 2D spatial grid into a 3D spatiotemporal tensor.

While executing this falls outside the scope of a 40-hour MVP, documenting this architectural blueprint under a "Future Roadmap" section in the `README.md` signals profound domain expertise. It transitions the repository from a finished school project into a living, evolving product.
