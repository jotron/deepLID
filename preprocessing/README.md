## Preprocessing

**Goal:** Split all samples in 5s pieces (padding up to 1.5s). Save all pieces in big Dataset ready for training.

### Distribution of Training data

TOTAL = 100'000 [5s samples]

#### By Split (80%, 10%, 10%)

- 80'000 Training
- 10'000 Validation
- 10'000 Test

#### By Language (1/3, 1/3, 1/3)

- 33'333 EN
- 33'333 FR
- 33'333 DE

#### By Source (50%, 50%)

- 50'000 Youtube
- 50'000 Voxforge

\**Librixox is only used as testdata*