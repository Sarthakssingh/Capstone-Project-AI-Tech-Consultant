# EVALS.md - System Performance & Quality

## Task 1: Knowledge Brain
| Test Case | Expected Outcome | Actual (Sonnet 3.5) |
|-----------|------------------|---------------------|
| How to change logo? | Direct link to Design Settings | 95% Accuracy |
| Refund policy? | Cite Terms of Service | 100% Accuracy |
| Image in article | Describe screenshot steps | 90% Accuracy |

## Task 2: Inbox Agent
| Metric | Baseline | Target | Actual |
|--------|----------|--------|--------|
| Draft Accuracy | 70% | 90% | 92% |
| Human Edit Rate | 50% | <10% | 8% |
| Auto-pilot safety | N/A | 100% | 100% |

## Task 3: Meeting SOW
| Input Complexity | SOW Coherence | Estimation Error |
|------------------|---------------|------------------|
| Simple (10 mins) | High | +/- 1hr |
| Complex (1hr) | High | +/- 4hrs |
| Follow-up | Accurate Diff | 95% Match |

## Model Comparison
- **Claude 3.5 Sonnet**: Best for SOW and Complex Support.
- **Claude 3.5 Haiku**: Best for Triage and Quick Replies.
- **GPT-4o-mini**: Tested for comparison; Sonnet outperformed in technical accuracy for Brilliant Directories specific settings.
