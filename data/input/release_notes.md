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
| KI-1 | Low      | Recommendations timeout (>3s) silently fail on low-bandwidth connections | Open |
| KI-2 | Low      | Recommendations carousel flickers on first load in Safari iOS < 16 | Open |
| KI-3 | Low      | Personalisation cold-start: new users (<7 days) get generic recommendations | Open |
| KI-4 | Medium   | Checkout page shows fallback UI if recommendations API responds with 5xx | Open |
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
- p95 API latency < 400ms (baseline: 211ms)
- Support ticket volume increase < 2× baseline (baseline: 32/day)
- No degradation to payment success rate (must stay ≥ 97.5%, baseline: 98.8%)
- DAU/WAU ratio ≥ 0.42 (baseline: 0.38)

---

## Current Metrics Being Tracked
- **Activation Conversion Rate**: % of users who activate SmartRecommendations after seeing the prompt
- **Error Rate**: API error rate (5xx responses / total requests)
- **Payment Success Rate**: % of payment transactions that succeed
- **Support Ticket Volume**: Daily support tickets opened, feature-tagged
- **DAU/WAU Ratio**: Daily Active Users / Weekly Active Users (stickiness metric)
- **API Latency P95**: 95th percentile API response time for recommendations endpoint
- **Feature Adoption Funnel**: % of users who complete the 3-step onboarding process

---

## Dependencies & Risks (Pre-Launch Assessment)
- **Dependency:** recommendations-service availability for optimal user experience
- **Risk:** ML model inference latency under high concurrency was load-tested to 60% traffic
- **Risk:** Shared CPU cluster has monitoring and alerting configured
- **Risk:** Circuit breaker planned for v2.2 release

---

## Technical Architecture Details
- **Microservice**: `recommendations-service` deployed alongside existing monolith
- **API Calls**: Synchronous in v2.1 (asynchronous planned for v2.2)
- **ML Infrastructure**: Shared CPU cluster (dedicated GPU cluster planned for v2.2)
- **Integration Points**: Home page, Product Detail page, Checkout page
- **Fallback Behavior**: Graceful degradation when recommendations unavailable
- **Monitoring**: Real-time metrics, alerting, and performance dashboards

---

## Business Context
- **Revenue Impact**: Cross-sell integration expected to increase conversion
- **User Experience**: Personalized recommendations based on 90-day history
- **Competitive Advantage**: Real-time dynamic ranking of recommendations
- **Market Timing**: Strategic launch aligned with Q1 growth targets
- **Customer Segments**: All active users, with focus on high-value customers
