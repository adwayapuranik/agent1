# PurpleMerit – SmartRecommendations v2.1 Release Notes

## Release Overview
**Feature:** SmartRecommendations v2.1  
**Release Date:** 2025-01-14  
**Rollout Strategy:** Gradual (10% → 50% → 100% over 7 days)  
**Current Rollout:** ~60% of active user base  
**Team:** Product, Engineering (Platform + ML), Design, Data

---

## What Changed

### New Capabilities
- **Personalised recommendation engine** powered by a new ML model (v2.1) trained on 90-day purchase and browse history
- **Recommendation carousel** embedded on Home, Product Detail, and Checkout pages
- **Dynamic ranking** — recommendations re-rank in real time based on session signals
- **Cross-sell integration** — first release linking recommendations directly to checkout flow

### Infrastructure Changes
- New `recommendations-service` microservice deployed alongside existing monolith
- Recommendation calls are **synchronous** in this release (async version planned for v2.2)
- Checkout page now calls recommendations API before rendering payment form
- ML model inference runs on shared CPU cluster (dedicated GPU cluster planned for v2.2)

---

## Known Issues at Launch

| ID   | Severity | Description | Status |
|------|----------|-------------|--------|
| KI-1 | Medium   | Recommendations timeout (>3s) silently fail on low-bandwidth connections | Open |
| KI-2 | Low      | Recommendations carousel flickers on first load in Safari iOS < 16 | Open |
| KI-3 | Medium   | Personalisation cold-start: new users (<7 days) get generic recommendations | Open |
| KI-4 | High     | Checkout page blocked if recommendations API responds with 5xx — fallback not implemented | **CRITICAL – not caught in QA** |
| KI-5 | Low      | Duplicate items occasionally appear in carousel for users with limited history | Open |

---

## Rollback Plan
- Feature flag `smart_recommendations_v2_enabled` can be set to `false` in config service within ~5 minutes
- Rollback removes the carousel and restores the original checkout flow
- ML model and database changes are backward-compatible
- **Estimated rollback time:** < 10 minutes
- **Data risk:** None — no schema migrations were applied

---

## Success Criteria (as defined pre-launch)
- Activation conversion rate ≥ 46% (baseline: 41%)
- Feature funnel completion ≥ 70%
- Error rate < 0.5% (baseline: 0.12%)
- p95 API latency < 400ms
- Support ticket volume increase < 2× baseline
- No degradation to payment success rate (must stay ≥ 97.5%)

---

## Dependencies & Risks (Pre-Launch Assessment)
- **Dependency:** recommendations-service must be available for checkout to complete (KI-4 — known but deprioritised)
- **Risk:** ML model inference latency under high concurrency was only load-tested to 30% traffic
- **Risk:** Shared CPU cluster has no autoscaling configured yet
- **Risk:** No circuit breaker on the recommendations API call in checkout path
