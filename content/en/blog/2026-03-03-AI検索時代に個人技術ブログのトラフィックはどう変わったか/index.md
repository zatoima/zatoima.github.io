---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How AI Search Has Changed Traffic to a Personal Tech Blog"
subtitle: ""
summary: "The impact of AI search through GA4 data. Over 33 months from June 2023 to February 2026, real data showing a 72% decline from peak traffic due to the rise of ChatGPT, Google AI Overview, and Perplexity, with phase-by-phase analysis."
tags: ["GA4", "Blog Management", "SEO", "AI", "Google Analytics"]
categories: ["Blog"]
url: personal-tech-blog-traffic-ai-search-impact
date: 2026-03-03
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

## Introduction

I'm publishing the GA4 data for this blog. The period covered is approximately 2 years and 8 months, from June 2023 to February 2026. By tracking the monthly trend of sessions from the start of measurement to the present, I examine how the rise of generative AI search tools like ChatGPT, Google AI Overview, and Perplexity has impacted traffic using my own data.

Let me state the conclusion upfront: I lost approximately 72% of sessions from peak. However, I see this not as the defeat of a personal blog, but as an inevitable result of a structural shift in how people search.

## The Overall Traffic Picture

![Monthly session trend (June 2023 – February 2026)](/images/ga4-session-trend-2023-2026.png)
*zatoima.github.io - GA4 monthly session trend. Vertical lines indicate major AI-related events*

| Metric | Value |
|--------|-------|
| Measurement start | June 2023 (12,574 sessions) |
| Effective peak | February 2025 (16,640 sessions) |
| Latest value | February 2026 (4,669 sessions) |
| Change from peak | **-71.9%** |
| Largest single-month decline | March 2025 (-27.5%) |

Looking at the monthly data as a whole, this wasn't a simple downward trend but rather a progression through multiple phases.

## The Transition in 5 Phases

### Phase 1: Stable Period (June–July 2023)

Monthly average of 12,474 sessions. ChatGPT had already gained widespread adoption, but at this point there was still a workflow of "I checked with ChatGPT, but let me also verify with an article just to be sure." Trust in AI accuracy was insufficient for it to fully replace search, and traffic to tech blogs was maintained.

### Phase 2: Post-Measurement Restart Decline (September 2023–April 2024)

```
2023/09: 20,183 (right after measurement restart - outlier)
2023/10: 17,008  -15.7%
2023/11: 15,215  -10.5%
2023/12: 13,818   -9.2%
2024/01: 12,307  -10.9%
2024/02: 11,955   -2.9%
2024/04: 11,729 (plateaued from here)
```

Approximately 8,500 sessions lost over 7 months (-41.9%). This coincided with the period when Google's SGE (Search Generative Experience) began experimental rollout in the US in May 2023. While the direct impact on Japanese-language content was limited, changes in the SEO landscape were beginning to form the baseline for the decline.

### Phase 3: Unexpected Recovery (May–October 2024)

Immediately after Google AI Overview officially launched in the US in May 2024, there was a -12.2% dip. However, this was followed by an unexpected recovery.

```
2024/05: 10,303  -12.2%
2024/07: 10,878  +7.3%
2024/08: 11,695  +7.5%
2024/09: 13,389  +14.5%
2024/10: 16,836  +25.7% (all-time high)
```

The likely reason behind this recovery was the nature of the content at the time. Articles on DB/infrastructure topics like PostgreSQL, Oracle, and AWS covered areas that AI in 2024 struggled to replace — version-specific behaviors, concrete error case studies, and the like. First-hand information from actual testing environments was trusted more than AI inference from training data in certain situations.

### Phase 4: Lull Period (November 2024–February 2025)

Monthly average of 14,641 sessions. In February 2025, the blog reached an effective peak of 16,640. It would have been reasonable to feel that "we've weathered the AI search impact" — but this turned out to be the edge of a cliff.

### Phase 5: Sharp Decline and Structural Shift (March 2025–Present)

```
2025/02: 16,640 (peak)
2025/03: 12,065  -27.5%
2025/04:  8,992  -25.5%
2025/05:  7,722  -14.1%
2025/06:  6,750  -12.6%
2025/08:  5,390  -23.2%
2025/09:  5,031 (bottom)
2026/02:  4,669  -9.7%
```

Approximately 69.8% decline in 7 months from peak. On average, about 1,600 sessions were lost each month. This decline was fundamentally different in nature from previous phases.

## Correlation with AI Search

### Timing Alignment

| AI-Related Event | Timing | Impact on Traffic |
|-----------------|--------|-------------------|
| ChatGPT launch | November 2022 | Outside measurement period (latent impact) |
| Google SGE experiment (US) | May 2023– | Correlated with Phase 2 decline |
| Google AI Overview US official launch | May 2024 | Temporary dip followed by recovery |
| Google AI Overview full-scale Japanese rollout | Early 2025 | Aligned with Phase 5 sharp decline |
| Perplexity/Claude Japanese market penetration | 2025– | Ongoing attrition |

Here are the estimated factors behind the structural shift starting with the March 2025 sharp decline (-27.5%), listed by importance.

**Factor 1: Google AI Overview's Japanese-language rollout**
How-to and troubleshooting queries like "PostgreSQL connection method," "ORA-00001 error cause," and "AWS S3 list CLI" fall squarely in AI Overview's sweet spot. Users could get their answers without ever leaving the search results page.

**Factor 2: Changes in Google's evaluation of personal blogs through core updates**
The tightening of E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) criteria may have worked against personal blogs.

**Factor 3: Normalization of AI search via Perplexity and others**
A behavioral shift from "search on Google" to "ask Perplexity" or "ask Claude" when researching technical information became standard among engineers. My blog's target readership happens to be the segment that adopted AI search earliest.

### The Reality of Zero-Click

The mechanism by which AI search creates "zero-click" results is straightforward: users get the information they need entirely within the AI chat or search results page, so clicks to the original site never occur.

**Queries prone to zero-click (likely to lose inbound traffic):**
- `PostgreSQL check version command`
- `psql connection arguments`
- `ORA-12154 cause`
- `AWS CLI S3 list buckets`

These are queries where AI can return a complete answer in just a few dozen characters.

**Queries resistant to zero-click (likely to retain inbound traffic):**
- `PostgreSQL replication hands-on experience`
- `Aurora PostgreSQL version upgrade failure story`
- `OCI Always Free ARM64 benchmark actual measurements`

First-hand experiences, failure stories, and test results from specific environments are precisely the areas where AI inferring from training data struggles most.

## What the Remaining 28% Tells Us

The current monthly session count (approximately 4,700) is not zero. Let me analyze the breakdown of this remaining traffic from recent data.

Looking at the traffic source channels for the top 3 articles by pageviews recently, DuckDB-related articles and the Snowflake MCP article have Direct traffic accounting for 80–86%. This consists of bookmarks, direct URL entry, and chat tool referrals (dark social). On the other hand, an Excel article (544 PV/month) is primarily Organic, showing that generic how-to articles still retain some search traffic.

What remains after the structural shift falls mainly into two categories:

1. **Readers arriving in search of specific testing environments and first-hand information** — Combinations like "OCI Free + PostgreSQL" or "Snow CLI actual measurements" require source references even for AI to generate summaries, so access to the articles themselves still occurs.
2. **Direct followers** — People who became aware of the blog through social media or previous articles and visit regularly.

These two categories are maintained regardless of fluctuations in Google Search.

## Conclusion

Let me organize what can be gleaned from 33 months of data.

| Phase | Period | Avg. Monthly Sessions | Context |
|-------|--------|----------------------|---------|
| Stable | 2023/06–07 | 12,474 | Early ChatGPT adoption, limited impact |
| Decline | 2023/10–2024/04 | 13,800→11,700 | SGE experiment, SEO landscape changes |
| Recovery | 2024/05–10 | 10,300→16,800 | Demand for first-hand information persisted |
| Lull | 2024/11–2025/02 | 14,641 | Final stable period |
| Structural shift | 2025/03– | 7,000→4,700 | AI Overview Japanese rollout, behavioral change established |

I lost 72%, but 28% remained. Whether you view this number as "collapse" or "the core survived" depends on your perspective, but I personally see it as the latter.

Traffic from how-to articles dependent on Google search results will not structurally return. This isn't unique to this blog — it's a turning point that all personal tech blogs in the Japanese-language space are facing. What will hold value in the next phase, I believe, is the accumulation of first-hand information that AI would want to cite as a source, and building relationships with readers who visit directly without going through search.

## References

{{< linkcard "https://blog.google/products-and-platforms/products/search/generative-ai-google-search-may-2024/" >}}

{{< linkcard "https://blog.google/products/search/ai-overviews-update-may-2024/" >}}
